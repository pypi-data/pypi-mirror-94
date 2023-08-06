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
import yaml
from hdv.validator import Validator

from providah.factories.package_factory import PackageFactory as pf


pf.fill_registry()


if not os.getenv('HDV_HOME'):
    if platform.system().lower() != 'windows':
        os.environ['HDV_HOME'] = os.getenv('HOME')
    else:
        os.environ['HDV_HOME'] = os.getenv('USERPROFILE')

# Create configuration
configuration_path = os.path.join(os.getenv("HDV_HOME"), ".hashmap_data_validator/hdv_configuration.yml")
profiles_path = os.path.join(os.getenv("HDV_HOME"), ".hashmap_data_validator/hdv_profiles.yml")
default_profiles_path: str = os.path.join(os.path.dirname(__file__),
                                          'configurations/default_hdv_profiles.yml')
default_config_path: str = os.path.join(os.path.dirname(__file__),
                                          'configurations/default_hdv_config.yml')

#  If the configuration path does not exist - then a default configuration will be created
if not os.path.exists(profiles_path):

    # Set the path for the default configuration if it does not exist
    hdv_profiles = os.path.join(os.getenv("HDV_HOME"), ".hashmap_data_validator")
    if not os.path.exists(hdv_profiles):
        os.mkdir(hdv_profiles)

    # Load the default configuration
    with open(default_profiles_path, 'r') as default_stream:
        profiles_configuration = yaml.safe_load(default_stream)

    # Write the default configuration
    with open(profiles_path, 'w') as stream:
        _ = yaml.dump(profiles_configuration, stream)


#  If the configuration path does not exist - then a default configuration will be created
if not os.path.exists(configuration_path):

    # Set the path for the default configuration if it does not exist
    hdv_config = os.path.join(os.getenv("HDV_HOME"), ".hashmap_data_validator")
    if not os.path.exists(hdv_config):
        os.mkdir(hdv_profiles)

    # Load the default configuration
    with open(default_config_path, 'r') as default_stream:
        validation_configuration = yaml.safe_load(default_stream)

    # Write the default configuration
    with open(configuration_path, 'w') as stream:
        _ = yaml.dump(validation_configuration, stream)
