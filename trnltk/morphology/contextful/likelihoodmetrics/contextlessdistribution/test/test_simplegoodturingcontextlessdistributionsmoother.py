# coding=utf-8
"""
Copyright  2012  Ali Ok (aliokATapacheDOTorg)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
"""
There is no verification -yet- in test of this class.
The tests are there for making sure there is no run time exceptions
"""
import logging
from pprint import pprint
import unittest
import pymongo
from trnltk.morphology.contextful.likelihoodmetrics.contextlessdistribution.contextlessdistributionsmoother import SimpleGoodTuringContextlessDistributionSmoother
from trnltk.morphology.contextful.likelihoodmetrics.hidden.simplegoodturing import logger as sgt_logger
from trnltk.morphology.contextful.likelihoodmetrics.contextlessdistribution.contextlessdistributionsmoother import logger

class SimpleGoodTuringContextlessDistributionSmootherTestWithDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(SimpleGoodTuringContextlessDistributionSmootherTestWithDatabase, cls).setUpClass()

        cls.mongodb_connection = pymongo.Connection(host='127.0.0.1')

    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        logger.setLevel(logging.DEBUG)
        sgt_logger.setLevel(logging.INFO)

        self.unigram_collection = self.mongodb_connection['trnltk']['wordUnigrams999']

    def test_smooth(self):
        K = 5

        smoother = SimpleGoodTuringContextlessDistributionSmoother(K, self.unigram_collection)

        smoother.initialize()

        smoothed_parse_result_count_map = {}
        smoothed_word_count_map = {}

        up = K + 5

        for c in range(0, up + 1):
            smooth_c = smoother.smooth_parse_result_occurrence_count(c)
            smoothed_parse_result_count_map[c] = smooth_c

        for c in range(0, up + 1):
            smooth_c = smoother.smooth_word_occurrence_count(c)
            smoothed_word_count_map[c] = smooth_c

        pprint(smoothed_parse_result_count_map)
        pprint(smoothed_word_count_map)

if __name__ == '__main__':
    unittest.main()
