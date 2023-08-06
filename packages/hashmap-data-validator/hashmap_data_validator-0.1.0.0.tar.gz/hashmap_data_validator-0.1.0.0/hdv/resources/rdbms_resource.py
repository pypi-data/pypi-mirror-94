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

from hdv.resources.resource import Resource


class RDBMSResource(Resource):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _validate_configuration(self) -> bool:
        return super()._validate_configuration()

    def retrieve_dataframe(self):
        super().retrieve_dataframe()

    def _generate_df(self):
        super()._generate_jdbc_df()
