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
import click

from hdv.utils.parse_config import ParseConfig
from hdv.utils.project_config import ProjectConfig
from hdv.validator import Validator


@click.command()
@click.option("-e", "--env", type=str, help="environment to take connection information from in hdm_profiles.yml")
def cli_validate(env: str = None):
    """ - makes hdv method callable via cli
        - configured in setup.py to be callable with 'hdv' command """

    # Validator instance
    os.environ['HDV_MANIFEST'] = f"{ProjectConfig.hdv_home()}/{ProjectConfig.configuration_path()}"
    os.environ['HDV_ENV'] = env
    cli_validation = Validator(configuration=ParseConfig.parse(config_path=os.getenv('HDV_MANIFEST')))

    # calls hdv method from cli
    cli_validation.run()
