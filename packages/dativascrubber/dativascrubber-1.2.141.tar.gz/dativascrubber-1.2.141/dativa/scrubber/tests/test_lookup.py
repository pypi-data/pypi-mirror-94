# (c) 2012-2018 Dativa, all rights reserved
# -----------------------------------------
# Usage subject to license agreement
# hello@dativa.com for more information

from newtools import CSVDoggo
from dativa.scrubber.tests import _BaseTest
from dativa.scrubber import Scrubber, ScrubberValidationError


class LookupTests(_BaseTest):

    def test_blacklist(self):
        self._test_filter(dirty_file="lookup/test_cities_dirty.csv",
                          clean_file="lookup/test_cities_dirty_blacklist.csv",
                          config={
                              "rules": [
                                  {
                                      "append_results": False,
                                      "params": {
                                          "attempt_closest_match": True,
                                          "blacklist": True,
                                          "fallback_mode": "remove_record",
                                          "original_reference": "lookup/test_cities_reference.csv",
                                          "reference_field": 0
                                      },
                                      "rule_type": "Lookup",
                                      "field": "1"
                                  }
                              ]
                          },
                          report=[
                              {

                                  'field': 'city',
                                  'rule': 'Lookup',
                                  'number_records': 64,
                                  'category': 'replaced',
                                  'description': 'Best match',
                                  'df': [['Bristol', 'Bsitrol'],
                                         ['London', 'Lndon'],
                                         ['Bristol', 'Bsitrol'],
                                         ['Bristol', 'Bsitrol'],
                                         ['Bristol', 'Bsitrol'],
                                         ['Bristol', 'Bsitrol'],
                                         ['Bristol', 'Bsitrol'],
                                         ['Bristol', 'Bsitrol'],
                                         ['Bristol', 'Bsitrol'],
                                         ['Bristol', 'Bsitrol'],
                                         ['Bristol', 'Bsitrol'],
                                         ['Bristol', 'Bsitrol'],
                                         ['Bristol', 'Bsitrol'],
                                         ['London', 'Lndon'],
                                         ['London', 'Lndon'],
                                         ['London', 'Lndon'],
                                         ['London', 'Lndon'],
                                         ['London', 'Lndon'],
                                         ['London', 'Lndon'],
                                         ['London', 'Lndon'],
                                         ['London', 'Lndon'],
                                         ['London', 'Lndon'],
                                         ['London', 'Lndon'],
                                         ['London', 'Lndon'],
                                         ['London', 'Lndon'],
                                         ['London', 'Lndon'],
                                         ['London', 'Lndon'],
                                         ['London', 'Lndon'],
                                         ['London', 'Lndon'],
                                         ['London', 'Lndon'],
                                         ['London', 'Lndon'],
                                         ['London', 'Lndon'],
                                         ['London', 'Lndon'],
                                         ['London', 'Lndon'],
                                         ['Liverpool', 'Lverpool'],
                                         ['Liverpool', 'Lverpool'],
                                         ['Liverpool', 'Lverpool'],
                                         ['Liverpool', 'Lverpool'],
                                         ['Liverpool', 'Lverpool'],
                                         ['Liverpool', 'Lverpool'],
                                         ['Liverpool', 'Lverpool'],
                                         ['Liverpool', 'Lverpool'],
                                         ['Liverpool', 'Lverpool'],
                                         ['Liverpool', 'Lverpool'],
                                         ['Liverpool', 'Lverpool'],
                                         ['Liverpool', 'Lverpool'],
                                         ['Liverpool', 'Lverpool'],
                                         ['Liverpool', 'Lverpool'],
                                         ['Liverpool', 'Lverpool'],
                                         ['Liverpool', 'Lverpool'],
                                         ['Liverpool', 'Lverpool'],
                                         ['Liverpool', 'Lverpool'],
                                         ['Liverpool', 'Lverpool'],
                                         ['Liverpool', 'Lverpool'],
                                         ['Liverpool', 'Lverpool'],
                                         ['Liverpool', 'Lverpool'],
                                         ['Liverpool', 'Lverpool'],
                                         ['Liverpool', 'Lverpool'],
                                         ['Liverpool', 'Lverpool'],
                                         ['Liverpool', 'Lverpool'],
                                         ['Liverpool', 'Lverpool'],
                                         ['Liverpool', 'Lverpool'],
                                         ['Liverpool', 'Lverpool'],
                                         ['Liverpool', 'Lverpool']],

                              },
                          ])

    def test_lookup(self):
        self._test_filter(dirty_file="lookup/test_cities_dirty.csv",
                          clean_file="lookup/test_cities_dirty_no_banana.csv",
                          config={
                              "rules": [
                                  {
                                      "append_results": False,
                                      "params": {
                                          "attempt_closest_match": True,
                                          "default_value": "Banana",
                                          "fallback_mode": "do_not_replace",
                                          "lookalike_match": False,
                                          "original_reference": "lookup/test_cities_reference.csv",

                                          "reference_field": "-1",
                                          "skip_blank": False,
                                          "string_distance_threshold": 0.7
                                      },
                                      "rule_type": "Lookup",
                                      "field": "1"
                                  }
                              ]
                          },
                          report=[
                              {

                                  'field': 'city',
                                  'rule': 'Lookup',
                                  'number_records': 4,
                                  'category': 'replaced',
                                  'description': 'Best match',
                                  'df': [['Bsitrol', 'Bristol'],
                                         ['Lverpool', 'Liverpool'],
                                         ['méémlent', 'élément'],
                                         ],

                              },
                              {

                                  'field': 'city',
                                  'rule': 'Lookup',
                                  'number_records': 2,
                                  'category': 'ignored',
                                  'description': 'No changes made',
                                  'df': [['Bath', 'Bath'],
                                         ['Btha', 'Btha']],

                              },
                          ])

    def test_lookup_1(self):
        self._test_filter(dirty_file="lookup/test_cities_dirty.csv",
                          clean_file="lookup/test_cities_dirty_banana.csv",
                          config={
                              "rules": [
                                  {
                                      "append_results": False,
                                      "params": {
                                          "attempt_closest_match": True,
                                          "default_value": "Banana",
                                          "fallback_mode": "use_default",
                                          "lookalike_match": False,
                                          "original_reference": "lookup/test_cities_reference.csv",

                                          "reference_field": "-1",
                                          "skip_blank": False,
                                          "string_distance_threshold": 0.7
                                      },
                                      "rule_type": "Lookup",
                                      "field": "1"
                                  }
                              ]
                          },
                          report=[
                              {

                                  'field': 'city',
                                  'rule': 'Lookup',
                                  'number_records': 4,
                                  'category': 'replaced',
                                  'description': 'Best match',
                                  'df': [['Bsitrol', 'Bristol'],
                                         ['Lverpool', 'Liverpool'],
                                         ['méémlent', 'élément']],

                              },
                              {

                                  'field': 'city',
                                  'rule': 'Lookup',
                                  'number_records': 2,
                                  'category': 'replaced',
                                  'description': 'Replaced with default value',
                                  'df': [['Bath', 'Banana'],
                                         ['Btha', 'Banana']],

                              },
                          ])

    def test_lookup_2(self):
        self._test_filter(dirty_file="lookup/test_cities_dirty.csv",
                          clean_file="lookup/test_cities_dirty_deleted_banana.csv",
                          config={
                              "rules": [
                                  {
                                      "append_results": False,
                                      "params": {
                                          "attempt_closest_match": True,
                                          "default_value": "Banana",
                                          "fallback_mode": "remove_record",
                                          "lookalike_match": False,
                                          "original_reference": "lookup/test_cities_reference.csv",

                                          "reference_field": "-1",
                                          "skip_blank": False,
                                          "string_distance_threshold": 0.7
                                      },
                                      "rule_type": "Lookup",
                                      "field": "1"
                                  }
                              ]
                          },
                          report=[
                              {

                                  'field': 'city',
                                  'rule': 'Lookup',
                                  'number_records': 4,
                                  'category': 'replaced',
                                  'description': 'Best match',
                                  'df': [['Bsitrol', 'Bristol'],
                                         ['Lverpool', 'Liverpool'],
                                         ['méémlent', 'élément']],

                              },
                              {

                                  'field': 'city',
                                  'rule': 'Lookup',
                                  'number_records': 2,
                                  'category': 'quarantined',
                                  'description': 'Data quarantined',
                                  'df': [['Bath'],
                                         ['Btha']],

                              },
                          ])

    def test_lookup_short(self):
        self._test_filter(dirty_file="lookup/test_short_original.csv",
                          clean_file="lookup/test_short_cleaned.csv",
                          config={
                              "rules": [
                                  {"field": "word",
                                   "append_results": False,
                                   "rule_type": "Lookup",
                                   "params": {
                                       "fallback_mode": "remove_record",
                                       "reference_field": 0,
                                       "original_reference": "lookup/test_short_reference.csv",
                                   }
                                   }
                              ]
                          },
                          report=[
                              {

                                  'field': 'word',
                                  'rule': 'Lookup',
                                  'number_records': 1,
                                  'category': 'quarantined',
                                  'description': 'Data quarantined',
                                  'df': [['E']],

                              },
                          ])

    def test_lookup_short_bad_field(self):
        self._test_filter(dirty_file="lookup/test_short_original.csv",
                          clean_file="lookup/test_short_cleaned.csv",
                          config={
                              "rules": [
                                  {"field": "word",
                                   "append_results": False,
                                   "rule_type": "Lookup",
                                   "params": {
                                       "fallback_mode": "remove_record",
                                       "reference_field": "word_not_there",
                                       "original_reference": "lookup/test_short_reference.csv",
                                   }
                                   }
                              ]
                          },
                          expected_error=KeyError)

    def test_df_dict_error(self):
        csv = CSVDoggo(base_path=self.test_dir)

        df = csv.load_df("lookup/test_short_original.csv")

        scrubber = Scrubber()

        try:
            scrubber.run(df=df,
                         config={
                             "rules": [
                                 {"field": "word",
                                  "append_results": False,
                                  "rule_type": "Lookup",
                                  "params": {
                                      "fallback_mode": "remove_record",
                                      "reference_field": "word",
                                      "original_reference": "lookup/test_short_reference.csv",
                                  }
                                  }
                             ]
                         }, df_dict=[])
        except ScrubberValidationError:
            self.assertTrue(True)

    def test_duplicates_in_lookup(self):

        self._test_filter(dirty_file="lookup/test_duplicates_original.csv",
                          clean_file="lookup/test_duplicates_cleaned.csv",
                          config={
                              "rules": [
                                  {"field": "word",
                                   "append_results": False,
                                   "rule_type": "Lookup",
                                   "params": {
                                       "fallback_mode": "remove_record",
                                       "reference_field": 0,
                                       "original_reference": "lookup/test_duplicates_reference.csv",
                                   }
                                   }
                              ]
                          },
                          report=[
                              {

                                  'field': 'word',
                                  'rule': 'Lookup',
                                  'number_records': 1,
                                  'category': 'quarantined',
                                  'description': 'Data quarantined',
                                  'df': [['E']],

                              },
                          ])

