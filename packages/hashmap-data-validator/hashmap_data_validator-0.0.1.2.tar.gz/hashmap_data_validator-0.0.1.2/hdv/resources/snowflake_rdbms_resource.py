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

import pandas as pd

from hdv.resources.rdbms_resource import RDBMSResource
from hdv.dao.db_snowflake import Snowflake


class SnowflakeResource(RDBMSResource):
    """Base class for all Snowflake Object types.
    This object holds the methods needed to connect to Snowflake and configure Snowflake credentials."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__connection_choice = kwargs['env']
        self.__table = kwargs['table_name']
        self.__chunk_size = kwargs['chunk_size']
        self.__offset = kwargs['offset']

    def retrieve_dataframe(self):
        """Reads data from a Snowflake table as a pandas dataframe."""
        try:
            with Snowflake(connection=self.__connection_choice).connection as conn:
                cursor = conn.cursor()

                if self.__chunk_size and self.__offset:
                    generated_df = pd.concat((self.generate_df(connection=conn)))
                    return generated_df

                else:
                    # select the sf table
                    cursor.execute(
                        f"select * from {self.__table};")

                    # fetch sf table as pandas dataframe
                    return cursor.fetch_pandas_all()

        except Exception as e:
            return e

    def generate_df(self, connection):
        """grabs samples from the snowflake table and returns sample as a generator object"""

        # original offset value
        original = self.__offset

        # query the length of the Snowflake table
        check_df = pd.read_sql_query(
            sql=f"select count(*) from {self.__table};",
            con=connection)

        # check that the chunk_size and offset fit within the dataframe
        if int(check_df.iloc[0] / 2) <= self.__chunk_size + self.__offset:
            log_message = f"Please ensure the Snowflake table row count is at least 2x larger than the sum of the" \
                               f" given chunk_size and offset values. Or, enter smaller chunk_size and offset values."
            self._logger.error(log_message)
            return False

        while True:

            # generate a generator object of df batch
            p_df = pd.read_sql_query(
                sql=f"select * from {self.__table} limit {self.__chunk_size} offset {self.__offset};",
                con=connection)

            # if empty, break
            if not len(p_df.index):
                break

            # yield generator object
            yield p_df

            # breaks if at the end of the table
            if len(p_df.index) < self.__chunk_size:
                break

            # set offset to grab next batch from df
            self.__offset += self.__chunk_size + original

            # the last batch of the table is grabbed to ensure row count integrity
            if self.__offset > int(check_df.iloc[0]):
                self.__offset -= original
