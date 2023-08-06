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
from mock import patch
import pandas as pd

from hdv.validator import Validator


class TestValidator(TestCase):

    def test_generate_hash_list(self):
        def __init__(configuration):
            self.configuration = configuration
        with patch.object(Validator, '__init__', __init__):
            df = pd.DataFrame.from_dict({'Col_1': ['hello', 'there'], 'Col_2': ['test', 'journey']})
            result = Validator.generate_hash_list(self, df)
            assert isinstance(result, list)

            assert isinstance(result[0], int)
