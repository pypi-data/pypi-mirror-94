# -*- coding: utf-8 -*-

#    Copyright (C) 2019  Marcus Rickert
#
#    See https://github.com/marcus67/little_brother
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import unittest

from little_brother import app_control
from little_brother import master_connector
from little_brother import prometheus
from little_brother import client_stats
from little_brother.test import test_persistence
from little_brother.test import test_rule_handler
from python_base_app.test import base_test

HOSTNAME = "hostname"
USERNAME = "username"
PROCESS_NAME = "processname"
PID = 123


class TestAppControl(base_test.BaseTestCase):

    def test_constructor(self):
        config = app_control.AppControlConfigModel()

        ac = app_control.AppControl(p_config=config, p_debug_mode=False,
                                    p_persistence=test_persistence.TestPersistence.create_dummy_persistence(
                                        self._logger))

        self.assertIsNotNone(ac)

    def test_constructor2(self):
        config = app_control.AppControlConfigModel()

        config.hostname = HOSTNAME

        rule_set_configs = test_rule_handler.TestRuleHandler.create_dummy_ruleset_configs()

        dummy_persistence = p_persistence = test_persistence.TestPersistence.create_dummy_persistence(self._logger)

        ac = app_control.AppControl(p_config=config, p_debug_mode=False,
                                    p_rule_handler=test_rule_handler.TestRuleHandler.create_dummy_rule_handler(
                                        p_persistence=dummy_persistence),
                                    p_persistence=dummy_persistence)

        self.assertIsNotNone(ac)

    def test_constructor3(self):
        some_client_stats = client_stats.ClientStats()
        ci = app_control.ClientInfo(p_is_master=True, p_host_name=HOSTNAME, p_client_stats=some_client_stats)

        self.assertIsNotNone(ci)

        self.assertTrue(ci.is_master)
        self.assertEqual(ci.host_name, HOSTNAME)
        self.assertIsNone(ci.last_message)
        self.assertEqual(ci.client_stats, some_client_stats)

    def test_get_number_of_monitored_users_function(self):
        config = app_control.AppControlConfigModel()

        ac = app_control.AppControl(p_config=config, p_debug_mode=False,
                                    p_persistence=test_persistence.TestPersistence.create_dummy_persistence(
                                        self._logger))

        func = ac.get_number_of_monitored_users_function()
        self.assertIsNotNone(func)

        self.assertEqual(func(), 0)

    def test_retrieve_user_mappings(self):
        config = app_control.AppControlConfigModel()

        ac = app_control.AppControl(p_config=config, p_debug_mode=False,
                                    p_persistence=test_persistence.TestPersistence.create_dummy_persistence(
                                        self._logger))

        ac.retrieve_user_mappings()

    def test_is_slave(self):
        mc_config = master_connector.MasterConnectorConfigModel()
        mc_config.host_url = "http://master.domain/"
        config = app_control.AppControlConfigModel()

        mc = master_connector.MasterConnector(p_config=mc_config)

        ac = app_control.AppControl(p_config=config, p_debug_mode=False,
                                    p_master_connector=mc,
                                    p_persistence=test_persistence.TestPersistence.create_dummy_persistence(
                                        self._logger))

        self.assertFalse(ac.is_master())

    def test_is_master(self):
        mc_config = master_connector.MasterConnectorConfigModel()
        config = app_control.AppControlConfigModel()

        mc = master_connector.MasterConnector(p_config=mc_config)

        ac = app_control.AppControl(p_config=config, p_debug_mode=False,
                                    p_master_connector=mc,
                                    p_persistence=test_persistence.TestPersistence.create_dummy_persistence(
                                        self._logger))

        self.assertTrue(ac.is_master())

    def test_set_metrics(self):
        pc_config = prometheus.PrometheusClientConfigModel()

        config = app_control.AppControlConfigModel()

        pc = prometheus.PrometheusClient(p_logger=self._logger, p_config=pc_config)

        ac = app_control.AppControl(p_config=config, p_debug_mode=False,
                                    p_prometheus_client=pc,
                                    p_persistence=test_persistence.TestPersistence.create_dummy_persistence(
                                        self._logger))

        ac.set_prometheus_http_requests_summary(p_duration=1.0, p_hostname=HOSTNAME, p_service="/app")
        ac.set_metrics()

        pc.stop()

    def test_check_interval(self):
        config = app_control.AppControlConfigModel()
        config.check_interval = 123

        ac = app_control.AppControl(p_config=config, p_debug_mode=False,
                                    p_persistence=test_persistence.TestPersistence.create_dummy_persistence(
                                        self._logger))

        self.assertIsNotNone(ac)

        check_interval = ac.check_interval

        self.assertEqual(check_interval, 123)


if __name__ == "__main__":
    unittest.main()
