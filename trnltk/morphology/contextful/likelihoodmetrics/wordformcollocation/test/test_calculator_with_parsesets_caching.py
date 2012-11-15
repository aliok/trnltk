# coding=utf-8
"""
There is no verification -yet- in test of this class.
The tests are there for making sure there is no run time exceptions
"""
import unittest
import pymongo
from trnltk.morphology.contextful.likelihoodmetrics.wordformcollocation.calculator import CachingContextParsingLikelihoodCalculator, InMemoryCachingContextParsingLikelihoodCalculator
from trnltk.morphology.contextful.likelihoodmetrics.wordformcollocation.hidden.database import QueryCacheCollectionCreator
from trnltk.morphology.contextful.likelihoodmetrics.wordformcollocation.test.test_calculator_with_parsesets import _BaseLikelihoodCalculatorTest

class CachingLikelihoodCalculatorTest(_BaseLikelihoodCalculatorTest):
    @classmethod
    def create_calculator(cls, parseset_index):
        mongodb_connection = pymongo.Connection(host='127.0.0.1')
        collection_map = {
            1: mongodb_connection['trnltk']['wordUnigrams{}'.format(parseset_index)],
            2: mongodb_connection['trnltk']['wordBigrams{}'.format(parseset_index)],
            3: mongodb_connection['trnltk']['wordTrigrams{}'.format(parseset_index)]
        }

        query_cache_collection = QueryCacheCollectionCreator(mongodb_connection['trnltk']).build(drop=False)

        return CachingContextParsingLikelihoodCalculator(collection_map, query_cache_collection)

    def test_contextstats_with_parseset_001_with_1leading(self):
        self._test_contextstats_with_parseset_n("001", 1, 0)

    def test_contextstats_with_parseset_001(self):
        self._test_contextstats_with_parseset_n("001", 2, 2)

    def test_contextstats_with_parseset_002(self):
        self._test_contextstats_with_parseset_n("002", 2, 2)

    def test_contextstats_with_parseset_003(self):
        self._test_contextstats_with_parseset_n("003", 2, 2)

    def test_contextstats_with_parseset_004(self):
        self._test_contextstats_with_parseset_n("004", 2, 2)

    def test_contextstats_with_parseset_005(self):
        self._test_contextstats_with_parseset_n("005", 2, 2)

    def test_contextstats_with_parseset_999(self):
        self._test_contextstats_with_parseset_n("999", 2, 2)

class InMemoryCachingLikelihoodCalculatorTest(_BaseLikelihoodCalculatorTest):
    @classmethod
    def create_calculator(cls, parseset_index):
        mongodb_connection = pymongo.Connection(host='127.0.0.1')
        collection_map = {
            1: mongodb_connection['trnltk']['wordUnigrams{}'.format(parseset_index)],
            2: mongodb_connection['trnltk']['wordBigrams{}'.format(parseset_index)],
            3: mongodb_connection['trnltk']['wordTrigrams{}'.format(parseset_index)]
        }

        return InMemoryCachingContextParsingLikelihoodCalculator(collection_map)

    def test_contextstats_with_parseset_001_with_1leading(self):
        self._test_contextstats_with_parseset_n("001", 1, 0)

    def test_contextstats_with_parseset_001(self):
        self._test_contextstats_with_parseset_n("001", 2, 2)

    def test_contextstats_with_parseset_002(self):
        self._test_contextstats_with_parseset_n("002", 2, 2)

    def test_contextstats_with_parseset_003(self):
        self._test_contextstats_with_parseset_n("003", 2, 2)

    def test_contextstats_with_parseset_004(self):
        self._test_contextstats_with_parseset_n("004", 2, 2)

    def test_contextstats_with_parseset_005(self):
        self._test_contextstats_with_parseset_n("005", 2, 2)

    def test_contextstats_with_parseset_999(self):
        self._test_contextstats_with_parseset_n("999", 2, 2)

if __name__ == '__main__':
    unittest.main()
