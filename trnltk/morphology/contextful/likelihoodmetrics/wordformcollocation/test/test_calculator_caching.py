# coding=utf-8
"""
There is no verification -yet- in test of this class.
The tests are there for making sure there is no run time exceptions
"""
import unittest
from trnltk.morphology.contextful.likelihoodmetrics.wordformcollocation.contextparsingcalculator import  CachingContextParsingLikelihoodCalculator
from trnltk.morphology.contextful.likelihoodmetrics.wordformcollocation.hidden.database import  QueryCacheCollectionCreator
from trnltk.morphology.contextful.likelihoodmetrics.wordformcollocation.noncontextparsingcalculator import CachingNonContextParsingLikelihoodCalculator
from trnltk.morphology.contextful.likelihoodmetrics.wordformcollocation.test.test_calculator import _LikelihoodCalculatorTest

class CachingNonContextParsingLikelihoodCalculatorTest(_LikelihoodCalculatorTest, unittest.TestCase):
    def setUp(self):
        super(CachingNonContextParsingLikelihoodCalculatorTest, self).setUp()
        database = self.mongodb_connection['trnltk']

        query_cache_collection = QueryCacheCollectionCreator(database).build(drop=True)

        self.generator = CachingNonContextParsingLikelihoodCalculator(self.collection_map, query_cache_collection)

    def test_generate_likelihood_of_one_word_given_two_context_words(self):
#        query_logger.setLevel(logging.DEBUG)
#        context_stats_logger.setLevel(logging.DEBUG)
        # don't override anything. added for better IDE support while running individual tests
        super(CachingNonContextParsingLikelihoodCalculatorTest, self).test_generate_likelihood_of_one_word_given_two_context_words()

    def test_generate_likelihood_of_one_word_given_one_leading_context_word(self):
#        query_logger.setLevel(logging.DEBUG)
#        context_stats_logger.setLevel(logging.DEBUG)
        # don't override anything. added for better IDE support while running individual tests
        super(CachingNonContextParsingLikelihoodCalculatorTest, self).test_generate_likelihood_of_one_word_given_one_leading_context_word()

    def test_generate_likelihood_of_one_word_given_two_leading_context_words(self):
#        query_logger.setLevel(logging.DEBUG)
#        context_stats_logger.setLevel(logging.DEBUG)
        # don't override anything. added for better IDE support while running individual tests
        super(CachingNonContextParsingLikelihoodCalculatorTest, self).test_generate_likelihood_of_one_word_given_two_leading_context_words()

    def test_generate_likelihood_of_one_word_given_one_following_context_word(self):
#        query_logger.setLevel(logging.DEBUG)
#        context_stats_logger.setLevel(logging.DEBUG)
        # don't override anything. added for better IDE support while running individual tests
        super(CachingNonContextParsingLikelihoodCalculatorTest, self).test_generate_likelihood_of_one_word_given_one_following_context_word()

    def test_generate_likelihood_of_one_word_given_one_context_word(self):
#        query_logger.setLevel(logging.DEBUG)
#        context_stats_logger.setLevel(logging.DEBUG)
        # don't override anything. added for better IDE support while running individual tests
        super(CachingNonContextParsingLikelihoodCalculatorTest, self).test_generate_likelihood_of_one_word_given_one_context_word()

    def _get_context(self, context):
        return context if context else []

class CachingContextParsingLikelihoodCalculatorTest(_LikelihoodCalculatorTest, unittest.TestCase):
    def setUp(self):
        super(CachingContextParsingLikelihoodCalculatorTest, self).setUp()

        database = self.mongodb_connection['trnltk']

        query_cache_collection = QueryCacheCollectionCreator(database).build(drop=True)

        self.generator = CachingContextParsingLikelihoodCalculator(self.collection_map, query_cache_collection)

    def test_generate_likelihood_of_one_word_given_two_context_words(self):
#        query_logger.setLevel(logging.DEBUG)
        #        context_stats_logger.setLevel(logging.DEBUG)
        # don't override anything. added for better IDE support while running individual tests
        super(CachingContextParsingLikelihoodCalculatorTest, self).test_generate_likelihood_of_one_word_given_two_context_words()

    def test_generate_likelihood_of_one_word_given_one_leading_context_word(self):
    #        query_logger.setLevel(logging.DEBUG)
    #        context_stats_logger.setLevel(logging.DEBUG)
        # don't override anything. added for better IDE support while running individual tests
        super(CachingContextParsingLikelihoodCalculatorTest, self).test_generate_likelihood_of_one_word_given_one_leading_context_word()

    def test_generate_likelihood_of_one_word_given_two_leading_context_words(self):
    #        query_logger.setLevel(logging.DEBUG)
    #        context_stats_logger.setLevel(logging.DEBUG)
        # don't override anything. added for better IDE support while running individual tests
        super(CachingContextParsingLikelihoodCalculatorTest, self).test_generate_likelihood_of_one_word_given_two_leading_context_words()

    def test_generate_likelihood_of_one_word_given_one_following_context_word(self):
    #        query_logger.setLevel(logging.DEBUG)
    #        context_stats_logger.setLevel(logging.DEBUG)
        # don't override anything. added for better IDE support while running individual tests
        super(CachingContextParsingLikelihoodCalculatorTest, self).test_generate_likelihood_of_one_word_given_one_following_context_word()

    def test_generate_likelihood_of_one_word_given_one_context_word(self):
    #        query_logger.setLevel(logging.DEBUG)
    #        context_stats_logger.setLevel(logging.DEBUG)
        # don't override anything. added for better IDE support while running individual tests
        super(CachingContextParsingLikelihoodCalculatorTest, self).test_generate_likelihood_of_one_word_given_one_context_word()

    def _get_context(self, context):
        return [self.contextless_parser.parse(cw) for cw in context] if context else []

if __name__ == '__main__':
    unittest.main()
