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
import unittest
import pymongo
from trnltk.morphology.contextful.likelihoodmetrics.hidden.targetformgivencontextcounter import CachingTargetFormGivenContextCounter, InMemoryCachingTargetFormGivenContextCounter
from trnltk.morphology.contextful.likelihoodmetrics.wordformcollocation.contextparsingcalculator import  ContextParsingLikelihoodCalculator
from trnltk.morphology.contextful.likelihoodmetrics.hidden.database import QueryCacheCollectionCreator, DatabaseIndexBuilder
from trnltk.morphology.contextful.likelihoodmetrics.wordformcollocation.ngramfrequencysmoother import CachedSimpleGoodTuringNGramFrequencySmoother
from trnltk.morphology.contextful.likelihoodmetrics.wordformcollocation.test.test_calculator_with_parsesets import _BaseLikelihoodCalculatorTest
from trnltk.morphology.contextful.parser.sequencelikelihoodcalculator import UniformSequenceLikelihoodCalculator

class LikelihoodCalculatorCachingTest(_BaseLikelihoodCalculatorTest):
    @classmethod
    def create_calculator(cls, parseset_index):
        mongodb_connection = pymongo.Connection(host='127.0.0.1')
        collection_map = {
            1: mongodb_connection['trnltk']['wordUnigrams{}'.format(parseset_index)],
            2: mongodb_connection['trnltk']['wordBigrams{}'.format(parseset_index)],
            3: mongodb_connection['trnltk']['wordTrigrams{}'.format(parseset_index)]
        }

        query_cache_collection = QueryCacheCollectionCreator(mongodb_connection['trnltk']).build(drop=False)

        database_index_builder = DatabaseIndexBuilder(collection_map)
        target_form_given_context_counter = CachingTargetFormGivenContextCounter(collection_map, query_cache_collection)
        ngram_frequency_smoother = CachedSimpleGoodTuringNGramFrequencySmoother()
        sequence_likelihood_calculator = UniformSequenceLikelihoodCalculator()

        return ContextParsingLikelihoodCalculator(database_index_builder, target_form_given_context_counter, ngram_frequency_smoother,
            sequence_likelihood_calculator)

    def test_calculate_with_parseset_001_with_1leading(self):
        self._test_calculate_with_parseset_n("001", 1, 0)

    def test_calculate_with_parseset_001(self):
        self._test_calculate_with_parseset_n("001", 2, 2)

    def test_calculate_with_parseset_002(self):
        self._test_calculate_with_parseset_n("002", 2, 2)

    def test_calculate_with_parseset_003(self):
        self._test_calculate_with_parseset_n("003", 2, 2)

    def test_calculate_with_parseset_004(self):
        self._test_calculate_with_parseset_n("004", 2, 2)

    def test_calculate_with_parseset_005(self):
        self._test_calculate_with_parseset_n("005", 2, 2)

    def test_calculate_with_parseset_999(self):
        self._test_calculate_with_parseset_n("999", 2, 2)


class LikelihoodCalculatorInMemoryCachingTest(_BaseLikelihoodCalculatorTest):
    @classmethod
    def create_calculator(cls, parseset_index):
        mongodb_connection = pymongo.Connection(host='127.0.0.1')
        collection_map = {
            1: mongodb_connection['trnltk']['wordUnigrams{}'.format(parseset_index)],
            2: mongodb_connection['trnltk']['wordBigrams{}'.format(parseset_index)],
            3: mongodb_connection['trnltk']['wordTrigrams{}'.format(parseset_index)]
        }

        database_index_builder = DatabaseIndexBuilder(collection_map)
        target_form_given_context_counter = InMemoryCachingTargetFormGivenContextCounter(collection_map)
        ngram_frequency_smoother = CachedSimpleGoodTuringNGramFrequencySmoother()
        sequence_likelihood_calculator = UniformSequenceLikelihoodCalculator()

        return ContextParsingLikelihoodCalculator(database_index_builder, target_form_given_context_counter, ngram_frequency_smoother,
            sequence_likelihood_calculator)

    def test_calculate_with_parseset_001_with_1leading(self):
        self._test_calculate_with_parseset_n("001", 1, 0)

    def test_calculate_with_parseset_001(self):
        self._test_calculate_with_parseset_n("001", 2, 2)

    def test_calculate_with_parseset_002(self):
        self._test_calculate_with_parseset_n("002", 2, 2)

    def test_calculate_with_parseset_003(self):
        self._test_calculate_with_parseset_n("003", 2, 2)

    def test_calculate_with_parseset_004(self):
        self._test_calculate_with_parseset_n("004", 2, 2)

    def test_calculate_with_parseset_005(self):
        self._test_calculate_with_parseset_n("005", 2, 2)

    def test_calculate_with_parseset_999(self):
        self._test_calculate_with_parseset_n("999", 2, 2)

if __name__ == '__main__':
    unittest.main()
