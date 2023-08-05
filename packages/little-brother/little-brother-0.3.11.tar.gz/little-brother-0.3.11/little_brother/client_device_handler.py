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

import re
import shlex
import subprocess

from little_brother import admin_event
from little_brother import persistence
from little_brother import process_handler
from python_base_app import configuration
from python_base_app import log_handling
from python_base_app import stats
from python_base_app import tools

SECTION_NAME = "ClientDeviceHandler"

CLIENT_DEVICE_SECTION_PREFIX = "ClientDevice"

DEFAULT_PING_COMMAND = "/bin/ping"
DEFAULT_MIN_ACTIVITY_DURATION = 60  # seconds
DEFAULT_MAX_ACTIVE_PING_DELAY = 100  # milliseconds
DEFAULT_PING_RESULT_REGEX = r"rtt min/avg/max/mdev = [\d\.]+/([\d\.]+)/[\d\.]+/[\d\.]+ ms"
DEFAULT_SAMPLE_SIZE = 10
DEFAULT_SERVER_GROUP = "default-group"


class ClientDeviceHandlerConfigModel(process_handler.ProcessHandlerConfigModel):

    def __init__(self):
        super(ClientDeviceHandlerConfigModel, self).__init__(p_section_name=SECTION_NAME)

        self.ping_command = DEFAULT_PING_COMMAND
        self.ping_result_regex = DEFAULT_PING_RESULT_REGEX


class ClientDeviceConfigModel(configuration.ConfigModel):

    def __init__(self, p_section_name):
        super(ClientDeviceConfigModel, self).__init__(p_section_name=p_section_name)

        self.name = None
        self.username = None
        self.hostname = None

        self.min_activity_duration = DEFAULT_MIN_ACTIVITY_DURATION
        self.max_active_ping_delay = DEFAULT_MAX_ACTIVE_PING_DELAY
        self.sample_size = DEFAULT_SAMPLE_SIZE

    def __str__(self):
        return "ClientDevice (name=%s, user=%s, host=%s)" % (self.name, self.username, self.hostname)


class ClientDeviceSectionHandler(configuration.ConfigurationSectionHandler):

    def __init__(self):
        super(ClientDeviceSectionHandler, self).__init__(p_section_prefix=CLIENT_DEVICE_SECTION_PREFIX)
        self.client_device_configs = {}

    def handle_section(self, p_section_name):
        client_device_section = ClientDeviceConfigModel(p_section_name=p_section_name)

        self.scan(p_section=client_device_section)
        tools.check_config_value(p_config=client_device_section, p_config_attribute_name="username")
        tools.check_config_value(p_config=client_device_section, p_config_attribute_name="hostname")

        configs = self.client_device_configs.get(client_device_section.name)

        if configs is None:
            configs = []
            self.client_device_configs[client_device_section.name] = client_device_section

        configs.append(client_device_section)


class DeviceInfo(object):

    def __init__(self, p_device_name, p_max_active_ping_delay, p_min_activity_duration, p_sample_size,
                 p_hostname):

        self._device_name = p_device_name
        self._max_active_ping_delay = p_max_active_ping_delay
        self._min_activity_duration = p_min_activity_duration
        self._sample_size = p_sample_size
        self._hostname = p_hostname
        self._moving_average = None
        self._active = None
        self._response_time = None
        self._moving_average_response_time = None
        self._up_start_time = None

    @property
    def device_name(self):

        return self._device_name

    @property
    def hostname(self):

        return self._hostname

    def update_hostname(self, p_hostname):

        if self._hostname is not None and p_hostname != self._hostname:
            self.clear_moving_average()

        self._hostname = p_hostname

    def update_max_active_ping_delay(self, p_max_active_ping_delay):

        self._max_active_ping_delay = p_max_active_ping_delay

    def update_min_activity_duration(self, p_min_activity_duration):

        self._min_activity_duration = p_min_activity_duration

    def update_sample_size(self, p_sample_size):

        if self._sample_size is not None and p_sample_size != self._sample_size:
            self.clear_moving_average()

        self._sample_size = p_sample_size

    @property
    def moving_average_response_time(self):

        if self._moving_average is None:
            return None

        else:
            return self._moving_average.get_value()

    @property
    def response_time(self):

        if self._moving_average is None:
            return None

        else:
            return self._moving_average.get_latest_value()

    def add_ping_delay(self, p_reference_time, p_delay):

        if self._moving_average is None:
            self._moving_average = stats.MovingAverage(p_sample_size=self._sample_size)

        was_up = self.is_up

        self._moving_average.add_value(p_value=p_delay)

        if self.is_up and not was_up:
            self._up_start_time = p_reference_time

    def clear_moving_average(self):

        self._moving_average = None

    @property
    def is_active(self):
        return self._moving_average is not None

    @property
    def is_up(self):

        if not self.is_active:
            return False

        if self.moving_average_response_time is None:
            return False

        return self.moving_average_response_time < self._max_active_ping_delay

    def requires_process_start_event(self, p_reference_time):

        if not self.is_up:
            return False

        return (p_reference_time - self.    _up_start_time).total_seconds() > self._min_activity_duration


class ClientDeviceHandler(process_handler.ProcessHandler):

    def __init__(self, p_config, p_persistence):

        super().__init__(p_config=p_config)
        self._persistence = p_persistence
        #self._session_context = persistence.SessionContext(p_persistence=self._persistence, p_register=True)

        try:
            self.ping_result_regex = re.compile(self._config.ping_result_regex)

        except Exception:
            fmt = "Invalid regular expression '{regex}' in [{section}]ping_result_regex"
            raise configuration.ConfigurationException(
                fmt.format(regex=self._config.ping_result_regex, section=SECTION_NAME))

        self._logger = log_handling.get_logger(self.__class__.__name__)

        self._process_infos = {}
        self._device_infos = {}

    @property
    def device_infos(self):
        return self._device_infos

    def get_device_info(self, p_device_name):

        with persistence.SessionContext(p_persistence=self._persistence) as session_context:
            device_info = self._device_infos.get(p_device_name)
            device = self._persistence.device_map(session_context).get(p_device_name)

        if device is not None:
            if device_info is None:
                device_info = DeviceInfo(p_device_name=p_device_name,
                                         p_max_active_ping_delay=device.max_active_ping_delay,
                                         p_min_activity_duration=device.min_activity_duration,
                                         p_sample_size=device.sample_size,
                                         p_hostname=device.hostname)
                self._device_infos[p_device_name] = device_info

            else:
                device_info.update_max_active_ping_delay(device.max_active_ping_delay)
                device_info.update_min_activity_duration(device.min_activity_duration)
                device_info.update_hostname(device.hostname)
                device_info.update_sample_size(device.sample_size)

        return device_info

    # https://stackoverflow.com/questions/2953462/pinging-servers-in-python
    def ping(self, p_host):
        """
        Returns True if host (str) responds to a ping request.
        Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
        """

        fmt = "{ping_command} -w 1 {c_option} {host}"
        raw_command = fmt.format(ping_command=self._config.ping_command,
                                 # Ping command count option as function of OS
                                 c_option='-n 1' if tools.is_windows() else '-c 1',
                                 host=shlex.quote(p_host))

        command = shlex.split(raw_command)
        delay = None

        fmt = "Executing command {cmd} in Popen"
        self._logger.debug(fmt.format(cmd=command))

        proc = subprocess.Popen(command, stdout=subprocess.PIPE)

        for line in proc.stdout:
            result = self.ping_result_regex.match(line.decode("UTF-8"))

            if result:
                delay = float(result.group(1))
                break

        fmt = "Host {host} is {status}"
        self._logger.debug(
            fmt.format(host=p_host, status="responding (%.1f ms)" % delay if delay is not None else "down"))

        return delay

    def ping_device(self, p_reference_time, p_device):

        fmt = "Pinging {device}..."
        self._logger.debug(fmt.format(device=p_device.hostname))

        delay = self.ping(p_device.hostname)
        device_info = self.get_device_info(p_device_name=p_device.device_name)

        if delay is not None:
            device_info.add_ping_delay(p_reference_time=p_reference_time, p_delay=delay)
            fmt = "Moving average={delay:.0f}"
            self._logger.debug(fmt.format(delay=device_info.moving_average_response_time))
        else:
            device_info.clear_moving_average()

        fmt = "{device} is {status}"
        self._logger.debug(fmt.format(device=p_device.device_name, status="up" if device_info.is_up else "down"))

    def get_current_active_pinfo(self, p_hostname, p_username):

        max_start_time = None
        most_recent_pinfo = None

        for pinfo in self._process_infos.values():
            if pinfo.hostname == p_hostname and pinfo.username == p_username:
                if max_start_time is None or pinfo.start_time > max_start_time:
                    max_start_time = pinfo.start_time
                    most_recent_pinfo = pinfo

        if most_recent_pinfo is not None:
            if most_recent_pinfo.end_time is None:
                return most_recent_pinfo

        return None

    def get_number_of_monitored_devices(self):

        with persistence.SessionContext(p_persistence=self._persistence) as session_context:
            return len(self._persistence.devices(session_context))

    def scan_processes(self, p_session_context, p_reference_time, p_server_group, p_login_mapping, p_host_name,
                       p_process_regex_map):

        events = []

        with persistence.SessionContext(p_persistence=self._persistence) as session_context:

            for device in self._persistence.devices(p_session_context):
                self.ping_device(p_reference_time=p_reference_time, p_device=device)

            for device_info in self._device_infos.values():
                if device_info.device_name not in self._persistence.device_map(session_context):
                    # Clear statistics for old device names so that they are correctly reported in Prometheus
                    device_info.clear_moving_average()

            for device in self._persistence.devices(session_context):
                device_info = self.get_device_info(p_device_name=device.device_name)

                if device_info.requires_process_start_event(p_reference_time=p_reference_time):
                    # Send process start event for monitored users (if required)
                    for user2device in device.users:
                        current_pinfo = self.get_current_active_pinfo(device.hostname, p_username=user2device.user.username)

                        if user2device.active:
                            if current_pinfo is None:
                                event = admin_event.AdminEvent(
                                    p_event_type=admin_event.EVENT_TYPE_PROCESS_START,
                                    p_hostname=device_info.hostname,
                                    p_hostlabel=device_info.device_name,
                                    p_processhandler=self.id,
                                    p_username=user2device.user.username,
                                    p_percent=user2device.percent,
                                    p_process_start_time=p_reference_time)
                                events.append(event)

                        else:
                            if current_pinfo is not None:
                                event = self.create_admin_event_process_end_from_pinfo(
                                    p_pinfo=current_pinfo,
                                    p_reference_time=p_reference_time)
                                events.append(event)


                else:
                    # Send process stop event for non monitored users (if required)
                    for user2device in device.users:
                        current_pinfo = self.get_current_active_pinfo(device.hostname, p_username=user2device.user.username)

                        if current_pinfo is not None:
                            event = self.create_admin_event_process_end_from_pinfo(
                                p_pinfo=current_pinfo,
                                p_reference_time=p_reference_time)
                            events.append(event)

            active_hostnames = [device_info.hostname for device_info in self._device_infos.values() if device_info.is_up]

            for pinfo in self._process_infos.values():
                # If the end time of a current entry is None AND the process was started on the local host AND
                # the process is no longer running THEN send an EVENT_TYPE_PROCESS_END event!
                if pinfo.end_time is None and pinfo.hostname not in active_hostnames:
                    event = self.create_admin_event_process_end_from_pinfo(
                        p_pinfo=pinfo,
                        p_reference_time=p_reference_time)
                    events.append(event)

        return events
