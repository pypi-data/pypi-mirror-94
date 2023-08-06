# Copyright 2016 - Nokia
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,  software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND,  either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from oslo_config import cfg
from vitrage.common.constants import DatasourceOpts as DSOpts
from vitrage.common.constants import UpdateMethod

ZABBIX_DATASOURCE = 'zabbix'

OPTS = [
    cfg.StrOpt(DSOpts.TRANSFORMER,
               default='vitrage.datasources.zabbix.transformer.'
                       'ZabbixTransformer',
               help='Zabbix transformer class path',
               required=True),
    cfg.StrOpt(DSOpts.DRIVER,
               default='vitrage.datasources.zabbix.driver.ZabbixDriver',
               help='Zabbix driver class path',
               required=True),
    cfg.StrOpt(DSOpts.UPDATE_METHOD,
               default=UpdateMethod.PUSH,
               help='None: updates only via Vitrage periodic snapshots.'
                    'Pull: updates every [changes_interval] seconds.'
                    'Push: updates by getting notifications from the'
                    ' datasource itself.',
               required=True),
    cfg.IntOpt(DSOpts.CHANGES_INTERVAL,
               default=20,
               min=10,
               help='interval between checking changes in zabbix data source'),
    cfg.StrOpt('user', default='admin',
               help='Zabbix user name'),
    cfg.StrOpt('password', default='zabbix',
               help='Zabbix user password'),
    cfg.StrOpt('url', default='',
               help='Zabbix url'),
    cfg.StrOpt(DSOpts.CONFIG_FILE, default='/etc/vitrage/zabbix_conf.yaml',
               help='Zabbix configuration file'),
]
