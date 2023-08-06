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

from hdv.dao.oracle import Oracle
from hdv.resources.rdbms_resource import RDBMSResource


class OracleResource(RDBMSResource):
    """Base class for all JDBC Object types.
    This object holds the methods needed to connect to JDBC and configure JDBC credentials."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__connection_choice = kwargs['env']
        self.__table = kwargs['table_name']
        self.__chunk_size = kwargs['chunk_size']
        self.__offset = kwargs['offset']

    def retrieve_dataframe(self):
        """Reads data from a JDBC table as a pandas dataframe."""

        # connect to oracle db and retrieve dataframe
        with Oracle(connection=self.__connection_choice).connection as conn:

            if self.__chunk_size and self.__offset:
                return pd.concat((self.generate_df(connection=conn)))

            # run default query
            else:
                return pd.read_sql_query(sql=f"select * from {self.__table}", con=conn)

    def generate_df(self, connection=None):
        """grabs samples from the jdbc table and returns sample as a generator object"""

        # original offset value
        original = self.__offset

        # query the row length of the JDBC table
        check_df = pd.read_sql_query(
            sql=f"select count(*) from {self.__table}",
            con=connection)

        # check that the chunk_size and offset fit within the dataframe
        if int(check_df.iloc[0] / 2) <= self.__chunk_size + self.__offset:
            log_message = f"Please ensure the JDBC table row count is at least 2x larger than the sum of the " \
                               f"given chunk_size and offset values. Or, enter smaller chunk_size and offset values."
            self._logger.error(log_message)
            return False

        while True:

            # generate a generator object of df batch
            # order by to ensure integrity of validation
            p_df = pd.read_sql_query(
                sql=f"select * from {self.__table} offset {self.__offset} ROWS FETCH NEXT {self.__chunk_size} ROWS ONLY",
                con=connection)

            # if batch is empty, break
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
