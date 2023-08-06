# Copyright 2017 - Nokia
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import abc


class MachineLearningBase(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def process_event(self, data, event_type):
        pass

    @staticmethod
    @abc.abstractmethod
    def get_plugin_name():
        pass
