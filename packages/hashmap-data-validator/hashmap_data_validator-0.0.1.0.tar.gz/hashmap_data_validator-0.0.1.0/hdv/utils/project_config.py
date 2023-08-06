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

import platform
import os


class ProjectConfig:
    @classmethod
    def hdv_home(cls):
        if not os.getenv('HDV_HOME'):
            if platform.system().lower() != 'windows':
                os.environ['HDV_HOME'] = os.getenv('HOME')
            else:
                os.environ['HDV_HOME'] = os.getenv('USERPROFILE')
        return os.getenv('HDV_HOME')

    @classmethod
    def hdv_env(cls):
        env = os.getenv('HDV_ENV')
        if not env:
            env = 'dev'
            os.environ['HDV_ENV'] = env
        return env

    @classmethod
    def profile_path(cls):
        return ".hashmap_data_validator/hdv_profiles.yml"

    @classmethod
    def configuration_path(cls):
        return ".hashmap_data_validator/hdv_configuration.yml"

    @classmethod
    def connection_max_attempts(cls):
        return 3

    @classmethod
    def connection_timeout(cls):
        return 3


