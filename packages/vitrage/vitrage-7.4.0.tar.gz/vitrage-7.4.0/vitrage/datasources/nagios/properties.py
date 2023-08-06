# Copyright 2016 - Nokia
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


class NagiosProperties(object):
    NUM_COLUMNS = 7
    RESOURCE_TYPE = 'resource_type'
    RESOURCE_NAME = 'resource_name'
    SERVICE = 'service'
    STATUS = 'status'
    LAST_CHECK = 'last_check'
    DURATION = 'duration'
    ATTEMPT = 'attempt'
    STATUS_INFO = 'status_info'
    NAGIOS = 'nagios'


class NagiosTestStatus(object):
    OK = 'OK'
    WARNING = 'WARNING'
    CRITICAL = 'CRITICAL'
    UNKNOWN = 'UNKNOWN'
