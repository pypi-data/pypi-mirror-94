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
import webbrowser
import os
import logging

import great_expectations as ge
import pandas as pd
from json2html import Json2Html

from providah.factories.package_factory import PackageFactory as pf


class Validator:
    """Class that holds the validate method"""

    @classmethod
    def _get_logger(cls):
        return logging.getLogger(cls.__name__)

    def __init__(self, configuration: dict):
        self._logger = self._get_logger()
        # row count validation
        self.row_count_valid = ""
        # row hash validation
        self.row_hash_valid = ""
        # hash df
        self.hash_df = None
        # json string to generate html report
        self.json_str = str

        # initiate source and sink objects
        # specific objects initialized depending on config values
        self.__sink = pf.create(key=configuration['resources'][configuration['validations']['to']]['type'], configuration=configuration['resources'][configuration['validations']['to']]['conf'])
        self.__source = pf.create(key=configuration['resources'][configuration['validations']['from']]['type'], configuration=configuration['resources'][configuration['validations']['from']]['conf'])

        # retrieve source and sink dataframes to run validations
        self.__sink_df = self.__sink.retrieve_dataframe()
        self.__source_df = self.__source.retrieve_dataframe()

    def run(self):
        """validation method: runs expectations on row count and row hash values between source and target tables"""
        try:

            self.order_columns()
            # run row count expectation on dataframes
            self.count_df_rows()

            # run row hash comparison expectation on dataframes
            self.compare_row_hashes()

            # create a json string from validation results
            self.json_str = '{"row_count_expectation": ' + self.row_count_valid + ', "row_hash_expectation": ' + self.row_hash_valid + "}"

            # generate html report from json string (.html file gets created from directory where the method is run)
            self.generate_html_report()

            # open the .html report
            return webbrowser.open('file://' + os.path.realpath('validation_report.html'))

        except Exception as e:
            self._logger.error(e)
            return False

    def generate_hash_list(self, df: pd.DataFrame):
        """generates a list of hash tuples over the rows in a dataframe"""
        hash_list = df.apply(lambda x: hash(tuple(x)), axis=1).tolist()

        return hash_list

    def order_columns(self):
        """order columns for hash comparison"""
        # assumes column names in both dataframes the same
        source_columns = self.__source_df.columns.tolist()
        sink_columns = self.__sink_df.columns.tolist()
        source_columns.sort()
        sink_columns.sort()

        self.__sink_df = self.__sink_df[sink_columns]
        self.__source_df = self.__source_df[source_columns]
        return

    def count_df_rows(self):
        """expectation to count dataframe rows"""

        # create a great expectations dataframe from the snowflake dataframe for row count expectation
        ge_df = ge.from_pandas(self.__sink_df)

        # run row count expectation
        self.row_count_valid = str(ge_df.expect_table_row_count_to_equal(len(self.__source_df.index)))

    def compare_row_hashes(self):
        """expectation to compare row hash strings"""

        # construct df from source hash list
        source_df = pd.DataFrame(pd.Series(self.generate_hash_list(self.__source_df), name='hashes'))
        # create a placeholder column to validate
        source_df['source_true'] = source_df['hashes'].apply(lambda x: True)

        # construct df from sink hash list
        sink_df = pd.DataFrame(pd.Series(self.generate_hash_list(self.__sink_df), name='hashes'))
        # create a placeholder column to validate
        sink_df['sink_true'] = sink_df['hashes'].apply(lambda x: True)

        # merge dataframes based on hash values
        # get length of dataframe so merge keeps NaN values for accurate validation
        if len(sink_df.index) > len(source_df.index):
            merged_df = sink_df.merge(source_df, how="left",
                                        left_on=['hashes', 'sink_true'],
                                        right_on=['hashes', 'source_true'])

        else:
            merged_df = source_df.merge(sink_df, how="left",
                                        left_on=['hashes', 'source_true'],
                                        right_on=['hashes', 'sink_true']
                                        )

        # create the hash dataframe to be used in the hash expectation through concatenation and convert pandas dataframe to a great expectations dataframe
        self.hash_df = ge.from_pandas(merged_df)

        # run hash comparison expectation
        self.row_hash_valid = str(self.hash_df.expect_column_pair_values_to_be_equal(column_A='source_true',
                                                                                     column_B='sink_true',
                                                                                     ignore_row_if='both_values_are_missing',
                                                                                     result_format='BASIC'))

    def generate_html_report(self):
        """converts json string to html and writes to html file"""

        # initiate json2html object
        j2h = Json2Html()

        # convert json to html
        table_str = j2h.convert(json=self.json_str, table_attributes="class=\"table table-bordered table-hover\"")

        # insert table string into html string
        html_str = f'<!doctype html><html lang="en"><head><!-- Required meta tags --><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no"><!-- Bootstrap CSS -->' \
                    '<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous"><title>Hashmap-Data-Validator</title></head>' \
                    '<header class="navbar navbar-expand-lg navbar-dark bg-dark"><div class="collapse navbar-collapse"><div class="mx-auto my-2 text-white"><h3>Hashmap Data Validator</h3></div></div></header>' \
                    f'<body>{table_str}<!-- Optional JavaScript --><!-- jQuery first, then Popper.js, then Bootstrap JS -->' \
                    f'<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>' \
                    f'<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>' \
                    f'<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>' \
                    f'</body></html>'

        # write html string to file
        with open(os.path.realpath('validation_report.html'), "w") as html_report:
            html_report.write(html_str)
            html_report.close()
        return
