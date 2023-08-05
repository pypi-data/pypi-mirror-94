# -*- coding: utf-8 -*-

# Copyright (C) 2019  Marcus Rickert
#
# See https://github.com/marcus67/little_brother
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import os.path

import alembic.config
import alembic.util.messaging
import psutil

from little_brother import app_control
from little_brother import client_device_handler
from little_brother import client_process_handler
from little_brother import constants
from little_brother import db_migrations
from little_brother import master_connector
from little_brother import persistence
from little_brother import popup_handler
from little_brother import prometheus
from little_brother import rule_handler
from little_brother import status_server
from little_brother import login_mapping
from little_brother.alembic.versions import version_0_3_added_tables_for_configuration_gui as alembic_version_gui

from python_base_app import audio_handler
from python_base_app import base_app
from python_base_app import configuration
from python_base_app import locale_helper
from python_base_app import unix_user_handler

APP_NAME = 'LittleBrother'
DIR_NAME = 'little-brother'
PACKAGE_NAME = 'little_brother'

DEFAULT_USER_HANDLER = unix_user_handler.HANDLER_NAME
DEFAULT_CLEAN_HISTORY_INTERVAL = 24 * 60 * 60 # seconds


class AppConfigModel(base_app.BaseAppConfigModel):

    def __init__(self):
        super(AppConfigModel, self).__init__(APP_NAME)

        self.check_interval = base_app.DEFAULT_TASK_INTERVAL
        self.clean_history_interval = DEFAULT_CLEAN_HISTORY_INTERVAL


def get_argument_parser(p_app_name):
    parser = base_app.get_argument_parser(p_app_name=p_app_name)
    parser.add_argument('--create-databases', dest='create_databases', action='store_const', const=True, default=False,
                        help='Creates database and database tables')
    parser.add_argument('--upgrade-databases', action="store", dest='upgrade_databases',
                        help='Upgrades database to specific alembic version', default="head")
    parser.add_argument('--stamp-databases', action="store", dest='stamp_databases',
                        help='Sets alembic database version to a specific value')
    return parser


class ProcessIteratorFactory(object):

    @staticmethod
    def process_iter():
        return psutil.process_iter()


class App(base_app.BaseApp):

    def __init__(self, p_pid_file, p_arguments, p_app_name):

        super(App, self).__init__(p_pid_file=p_pid_file, p_arguments=p_arguments, p_app_name=p_app_name,
                                  p_dir_name=constants.DIR_NAME, p_languages=constants.LANGUAGES)

        self._notification_handlers = []
        self._status_server = None
        self._persistence = None
        self._process_handlers = None
        self._client_device_handler = None
        self._app_control = None
        self._rule_handler = None
        self._master_connector = None
        self._rule_set_section_handler = None
        self._client_device_section_handler = None
        self._prometheus_client = None
        self._user_handler = None
        self._locale_helper = None

    def prepare_configuration(self, p_configuration):

        app_control_section = app_control.AppControlConfigModel()
        p_configuration.add_section(app_control_section)

        audio_handler_section = audio_handler.AudioHandlerConfigModel()
        audio_handler_section.spool_dir = os.path.join("/var/spool", constants.DIR_NAME)
        p_configuration.add_section(audio_handler_section)

        popup_handler_section = popup_handler.PopupHandlerConfigModel()
        p_configuration.add_section(popup_handler_section)

        persistence_section = persistence.PersistenceConfigModel()
        persistence_section.sqlite_dir = os.path.join("/var/spool", constants.DIR_NAME)
        p_configuration.add_section(persistence_section)

        rule_handler_section = rule_handler.RuleHandlerConfigModel()
        p_configuration.add_section(rule_handler_section)

        self._rule_set_section_handler = rule_handler.RuleSetSectionHandler()
        p_configuration.register_section_handler(p_section_handler=self._rule_set_section_handler)

        client_process_handler_section = client_process_handler.ClientProcessHandlerConfigModel()
        p_configuration.add_section(client_process_handler_section)

        client_device_handler_section = client_device_handler.ClientDeviceHandlerConfigModel()
        p_configuration.add_section(client_device_handler_section)

        self._client_device_section_handler = client_device_handler.ClientDeviceSectionHandler()
        p_configuration.register_section_handler(p_section_handler=self._client_device_section_handler)

        status_server_section = status_server.StatusServerConfigModel()
        p_configuration.add_section(status_server_section)

        master_connector_section = master_connector.MasterConnectorConfigModel()
        p_configuration.add_section(master_connector_section)

        prometheus_client_section = prometheus.PrometheusClientConfigModel()
        p_configuration.add_section(prometheus_client_section)

        self.app_config = AppConfigModel()
        p_configuration.add_section(self.app_config)

        user_handler_section = unix_user_handler.BaseUserHandlerConfigModel()
        p_configuration.add_section(user_handler_section)

        self._login_mapping_section_handler = login_mapping.LoginMappingSectionHandler()
        p_configuration.register_section_handler(p_section_handler=self._login_mapping_section_handler)

        return super(App, self).prepare_configuration(p_configuration=p_configuration)

    def is_master(self):

        return self._config[master_connector.SECTION_NAME].host_url is None

    def check_migrations(self):

        db_mig = db_migrations.DatabaseMigrations(p_logger=self._logger, p_persistence=self._persistence)

        current_version = db_mig.get_current_version()

        msg = "Database is on alembic version {version}"
        self._logger.info(msg.format(version=current_version))

        if db_mig.check_if_version_is_active(p_version=alembic_version_gui.revision):
            session = self._persistence.get_session()
            rows = session.query(persistence.User).count()

            if rows == 0:
                # if there are no users in the database yet we assume that the migration has never run yet
                db_mig.migrate_ruleset_configs(
                    p_ruleset_configs=self._rule_set_section_handler.rule_set_configs)

                db_mig.migrate_client_device_configs(
                    p_client_device_configs=self._client_device_section_handler.client_device_configs)

            else:
                if len(self._rule_set_section_handler.rule_set_configs) > 0:
                    msg = "Remove {count} migrated ruleset sections 'RuleSet*'"
                    self._logger.warning(
                        msg.format(count=len(self._rule_set_section_handler.rule_set_configs)))

                if len(self._client_device_section_handler.client_device_configs) > 0:
                    msg = "Remove {count} migrated device sections 'Device*'"
                    self._logger.warning(
                        msg.format(count=len(self._client_device_section_handler.client_device_configs)))

            session.close()

    def prepare_services(self, p_full_startup=True):

        super().prepare_services(p_full_startup=p_full_startup)

        # TODO: Activate in memory sqlite backend for slaves
        self._persistence = persistence.Persistence(
            p_config=self._config[persistence.SECTION_NAME])

        if not p_full_startup:
            return

        if self.is_master():
            self._rule_handler = rule_handler.RuleHandler(
                p_config=self._config[rule_handler.SECTION_NAME],
                p_persistence=self._persistence)

        self._master_connector = master_connector.MasterConnector(
            p_config=self._config[master_connector.SECTION_NAME])

        config = self._config[audio_handler.SECTION_NAME]

        if config.is_active():
            self._notification_handlers.append(audio_handler.AudioHandler(p_config=config))

        config = self._config[popup_handler.SECTION_NAME]

        if config.is_active():
            self._notification_handlers.append(popup_handler.PopupHandler(p_config=config))

        self.check_migrations()

        process_handler = client_process_handler.ClientProcessHandler(
            p_config=self._config[client_process_handler.SECTION_NAME],
            p_process_iterator_factory=ProcessIteratorFactory())

        self._client_device_handler = client_device_handler.ClientDeviceHandler(
            p_config=self._config[client_device_handler.SECTION_NAME],
            p_persistence=self._persistence)

        self._process_handlers = {
            process_handler.id: process_handler,
            self._client_device_handler.id: self._client_device_handler
        }

        config = self._config[prometheus.SECTION_NAME]

        if config.is_active():
            self._prometheus_client = prometheus.PrometheusClient(
                p_logger=self._logger, p_config=config)

        unix_user_handler_config = self._config[unix_user_handler.SECTION_NAME]
        status_server_config = self._config[status_server.SECTION_NAME]

        self.init_babel(p_localeselector=self.get_request_locale)

        localedir = os.path.join(os.path.dirname(__file__), "translations")
        a_locale_helper = locale_helper.LocaleHelper(p_locale_selector=self.get_request_locale,
                                                     p_locale_dir=localedir)
        self.add_locale_helper(a_locale_helper)

        if self.is_master():
            if status_server_config.is_active():
                if status_server_config.admin_password is not None:
                    msg = "admin_user and admin_password in section [StatusSever] " \
                          "should be moved to section [UnixUserHandler]"
                    self._logger.warning(msg)

                    if not unix_user_handler_config.is_active():
                        unix_user_handler_config.admin_username = status_server_config.admin_username
                        unix_user_handler_config.admin_password = status_server_config.admin_password

                if self.is_master() and not unix_user_handler_config.is_active():
                    msg = "admin_user and admin_password must be supplied in section [UnixUserHandler]"
                    raise configuration.ConfigurationException(msg)

                if unix_user_handler_config.is_active():
                    self._user_handler = unix_user_handler.UnixUserHandler(p_config=unix_user_handler_config,
                                                                           p_exclude_user_list=[
                                                                               constants.APPLICATION_USER])

        else:
            self._user_handler = unix_user_handler.UnixUserHandler(p_config=unix_user_handler_config)

        self._login_mapping = login_mapping.LoginMapping()
        self._login_mapping.read_from_configuration(p_login_mapping_section_handler=self._login_mapping_section_handler)

        self._app_control = app_control.AppControl(
            p_config=self._config[app_control.SECTION_NAME],
            p_debug_mode=self._app_config.debug_mode,
            p_process_handlers=self._process_handlers,
            p_device_handler=self._client_device_handler,
            p_persistence=self._persistence,
            p_rule_handler=self._rule_handler,
            p_notification_handlers=self._notification_handlers,
            p_master_connector=self._master_connector,
            p_prometheus_client=self._prometheus_client,
            p_user_handler=self._user_handler,
            p_locale_helper=self.locale_helper,
            p_login_mapping=self._login_mapping)

        if self._config[app_control.SECTION_NAME].scan_active:
            task = base_app.RecurringTask(p_name="app_control.scan_processes(ProcessHandler)",
                                          p_handler_method=lambda: self._app_control.scan_processes(
                                              p_process_handler=process_handler),
                                          p_interval=process_handler.check_interval)
            self.add_recurring_task(p_recurring_task=task)

        else:
            fmt = "Process scanning for this host has been deactivated in configuration"
            self._logger.warning(fmt)

        if self._client_device_handler:
            task = base_app.RecurringTask(
                p_name="app_control.scan_processes(DeviceHandler)",
                p_handler_method=lambda: self._app_control.scan_processes(
                    p_process_handler=self._client_device_handler),
                p_interval=self._client_device_handler.check_interval)
            self.add_recurring_task(p_recurring_task=task)

        if self.is_master():
            task = base_app.RecurringTask(
                p_name="app_control.clean_history",
                p_handler_method=lambda: self._app_control.clean_history(),
                p_interval=self._app_config.clean_history_interval)
            self.add_recurring_task(p_recurring_task=task)


        if status_server_config.is_active():
            self._status_server = status_server.StatusServer(
                p_config=self._config[status_server.SECTION_NAME],
                p_package_name=PACKAGE_NAME,
                p_app_control=self._app_control,
                p_master_connector=self._master_connector,
                p_persistence=self._persistence,
                p_is_master=self.is_master(),
                p_locale_helper=self._locale_helper,
                p_base_gettext=self.gettext,
                p_languages=constants.LANGUAGES,
                p_user_handler=self._user_handler
            )

        elif self.is_master():
            msg = "Master instance requires port number for web server"
            raise configuration.ConfigurationException(msg)

        else:
            msg = "Slave instance will not start web server due to missing port number"
            self._logger.warn(msg)

        task = base_app.RecurringTask(p_name="app_control.check", p_handler_method=self._app_control.check,
                                      p_interval=self._app_control.check_interval)
        self.add_recurring_task(p_recurring_task=task)

    def run_special_commands(self, p_arguments):

        if p_arguments.stamp_databases:
            self.basic_init(p_full_startup=False)
            self.stamp_databases(p_alembic_version=p_arguments.stamp_databases)
            return True

        if p_arguments.create_databases:
            self.basic_init(p_full_startup=False)
            self._persistence.check_schema(p_create_tables=False)

        if p_arguments.upgrade_databases:
            self.basic_init(p_full_startup=False)
            db_mig = db_migrations.DatabaseMigrations(p_logger=self._logger, p_persistence=self._persistence)
            db_mig.upgrade_databases(p_alembic_version=p_arguments.upgrade_databases)

        return False

    def stamp_databases(self, p_alembic_version):

        url = self._persistence.build_url()
        alembic_working_dir = os.path.dirname(__file__)

        fmt = "Stamping database to revision '{revision}' using alembic with working directory {working_dir}..."
        self._logger.info(fmt.format(revision=p_alembic_version,
                                     working_dir=alembic_working_dir))

        alembic_argv = ["-x", url,
                        "stamp", p_alembic_version]
        os.chdir(alembic_working_dir)
        alembic.config.main(alembic_argv, prog="alembic.config.main")

    def start_services(self):

        if self._status_server is not None:
            self._status_server.start_server()

        if self._app_control is not None:
            self._app_control.start()

        if self._prometheus_client is not None:
            self._prometheus_client.start()

    def stop_services(self):

        fmt = "Shutting down services -- START"
        self._logger.info(fmt)

        if self._status_server is not None:
            self._status_server.stop_server()
            self._status_server = None

        if self._app_control is not None:
            self._app_control.stop()
            self._app_control = None

        for handler in self._notification_handlers:
            handler.stop_engine()

        fmt = "Shutting down services -- END"
        self._logger.info(fmt)

    def handle_downtime(self, p_downtime):

        self._app_control.handle_downtime(p_downtime=p_downtime)


def main():
    parser = get_argument_parser(p_app_name=APP_NAME)

    return base_app.main(p_app_name=APP_NAME, p_app_class=App, p_argument_parser=parser)


if __name__ == '__main__':
    exit(main())
