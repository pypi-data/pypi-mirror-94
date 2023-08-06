# Copyright © 2021 Hashmap, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
from unittest import TestCase

from hdv.utils.project_config import ProjectConfig


class TestProjectConfig(TestCase):

    def test_hdv_home(self):
        os.environ['HDV_HOME'] = os.getcwd()
        self.assertEqual(os.getcwd(), ProjectConfig.hdv_home())

    def test_hdv_env(self):
        self.assertEqual('dev', ProjectConfig.hdv_env())
        os.environ['HDV_ENV'] = 'prod'
        self.assertEqual('prod', ProjectConfig.hdv_env())

    def test_profile_path(self):
        self.assertEqual(ProjectConfig.profile_path(), ".hashmap_data_validator/hdv_profiles.yml")

    def test_configuration_path(self):
        self.assertEqual(ProjectConfig.configuration_path(), ".hashmap_data_validator/hdv_configuration.yml")

    def test_connection_max_attempts(self):
        self.assertEqual(3, ProjectConfig.connection_max_attempts())

    def test_connection_timeout(self):
        self.assertEqual(3, ProjectConfig.connection_timeout())
