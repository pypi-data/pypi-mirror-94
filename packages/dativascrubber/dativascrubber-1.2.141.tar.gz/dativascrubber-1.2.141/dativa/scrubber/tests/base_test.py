# (c) 2012-2018 Dativa, all rights reserved
# -----------------------------------------
# Usage subject to license agreement
# hello@dativa.com for more information

import sys
import logging
import os
import pandas as pd
import numpy as np
from newtools import CSVDoggo, BaseTest
from dativa.scrubber import Scrubber

logger = logging.getLogger("dativa.scrubber.tests")


class _BaseTest(BaseTest):
    create_test_data = False

    test_dir = os.path.join(os.path.dirname(__file__), "test-data")
    ScrubberClass = Scrubber

    def _compare_df_to_file(self, csv, df, clean_file):
        """

        :param csv: an instance of a CSVHandler class
        :param df: the dataframe to compare
        :param clean_file: the file to compare
        :return: raises an exception if they not the same
        """

        if self.create_test_data:
            csv.save_df(df, clean_file)

        print(clean_file)

        pd.testing.assert_frame_equal(csv.load_df(clean_file,
                                                  dtype=str,
                                                  na_values='',
                                                  skip_blank_lines=False,
                                                  keep_default_na=False).fillna("N/A").reset_index(drop=True),
                                      df.reset_index(drop=True).replace('', pd.NA).fillna("N/A").astype(str),
                                      check_like=True,
                                      check_dtype=False)

    def _test_filter_actual(self,
                            dirty_file,
                            clean_file,
                            config,
                            expected_report,
                            encoding,
                            delimiter,
                            quotechar,
                            report_writer,
                            profile,
                            expected_df_dict,
                            dirty_df):

        csv = CSVDoggo(encoding=encoding,
                       delimiter=delimiter,
                       quotechar=quotechar,
                       base_path=self.test_dir,
                       line_terminator="\n")

        scrubber = self.ScrubberClass(report_writer, profile)

        dataframe_dict = {}
        for file in scrubber.get_files_from_config(config):
            dataframe_dict[file] = csv.load_df(file, force_dtype=np.str, header=None, skip_blank_lines=False)
        if isinstance(dirty_df, pd.DataFrame):
            df = dirty_df
        else:
            print(dirty_file)
            df = csv.load_df(dirty_file, skip_blank_lines=False)

        report = scrubber.run(df, config, dataframe_dict)

        print(",")
        print("report = [")
        np.set_printoptions(threshold=sys.maxsize)
        for r in report:
            print("{")
            print("""
            'field': '{0}',
                   'rule': '{1}',
                   'number_records': {2},
                   'category': '{3}',
                   'description': '{4}',
                   'df': {5},
                   """.format(r.field, r.rule, r.number_records, r.category, r.description,
                              repr(r.df.values).replace("array(", "").replace(", dtype=object)", "").replace(
                                  "dtype=object),", "").replace("Timestamp", "_to_time")).replace("nan", "None"))
            print("},")
        print("]")

        self._compare_df_to_file(csv, df, clean_file)

        if expected_report is not None:

            self.assertEqual(len(report), len(expected_report))
            for i in range(0, len(report)):
                self.assertEqual(report[i].field, expected_report[i]["field"])
                self.assertEqual(report[i].rule, expected_report[i]["rule"])
                self.assertEqual(report[i].number_records, expected_report[i]["number_records"])
                self.assertEqual(report[i].category, expected_report[i]["category"])
                self.assertEqual(report[i].description, expected_report[i]["description"])
                np.array_equal(report[i].df.values, expected_report[i]["df"], )

        if expected_df_dict is not None:
            for file in expected_df_dict:
                try:
                    expected_df = csv.load_df(expected_df_dict[file])
                    actual_df = dataframe_dict[file]
                    pd.testing.assert_frame_equal(expected_df, actual_df)
                except TypeError:
                    expected_df = csv.load_df(file)
                    actual_df = dataframe_dict[file]
                    pd.testing.assert_frame_equal(expected_df, actual_df)

    def _test_filter(self,
                     dirty_file,
                     clean_file,
                     config,
                     report=None,
                     encoding="UTF-8",
                     delimiter=",",
                     quotechar='"',
                     report_writer=None,
                     profile=None,
                     expected_error=None,
                     expected_df_dict=None,
                     dirty_df=False):

        logger.debug("testing {0}".format(dirty_file))

        if expected_error is None:
            self._test_filter_actual(dirty_file,
                                     clean_file,
                                     config,
                                     report,
                                     encoding,
                                     delimiter,
                                     quotechar,
                                     report_writer,
                                     profile,
                                     expected_df_dict=expected_df_dict,
                                     dirty_df=dirty_df
                                     )

            if report is None:
                raise ValueError("Report not set for test")

            return

        with self.assertRaises(expected_error):
            return self._test_filter_actual(dirty_file,
                                            clean_file,
                                            config,
                                            report,
                                            encoding,
                                            delimiter,
                                            quotechar,
                                            report_writer,
                                            profile,
                                            expected_df_dict=expected_df_dict,
                                            dirty_df=dirty_df)
