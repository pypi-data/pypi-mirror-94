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

from oslo_policy import policy

from vitrage.common.policies import base

TOPOLOGY = 'get topology'

rules = [
    policy.DocumentedRuleDefault(
        name=TOPOLOGY,
        check_str=base.UNPROTECTED,
        description='Get the topology for the OpenStack cluster with optional '
                    'query parameters',
        operations=[
            {
                'path': '/topology',
                'method': 'GET'
            }
        ]
    ),
    policy.DocumentedRuleDefault(
        name=TOPOLOGY + ':all_tenants',
        check_str=base.ROLE_ADMIN,
        description='Get the topology for the OpenStack cluster with optional '
                    'query parameters. Return resources of all tenants (if the'
                    ' user has the permissions).',
        operations=[
            {
                'path': '/topology',
                'method': 'GET'
            }
        ]
    )
]


def list_rules():
    return rules
