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
import unittest
from unittest import TestCase

from hdv.dao.oracle import Oracle


class TestSnowflake(TestCase):

    def setUp(self) -> None:
        config = {
            'user': 'user',
            'password': 'password',
            'sid': 'sid',
            'port': 'port',
            'host': 'host',
            'client_library_dir': 'client_library_dir'
        }

        self._dao = Oracle(**config)

    @unittest.skip
    def test_cotr(self):
        conn = Oracle(**{})

    @unittest.skip
    def test_load_data_fail(self):
        with self.assertRaises(ConnectionError):
            with self._dao.connection as conn:
                pass