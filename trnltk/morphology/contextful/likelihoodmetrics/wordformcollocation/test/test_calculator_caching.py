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
from trnltk.morphology.contextful.likelihoodmetrics.hidden.targetformgivencontextcounter import CachingTargetFormGivenContextCounter
from trnltk.morphology.contextful.likelihoodmetrics.wordformcollocation.contextparsingcalculator import  ContextParsingLikelihoodCalculator
from trnltk.morphology.contextful.likelihoodmetrics.hidden.database import  QueryCacheCollectionCreator, DatabaseIndexBuilder
from trnltk.morphology.contextful.likelihoodmetrics.wordformcollocation.ngramfrequencysmoother import CachedSimpleGoodTuringNGramFrequencySmoother
from trnltk.morphology.contextful.likelihoodmetrics.wordformcollocation.noncontextparsingcalculator import CachingNonContextParsingLikelihoodCalculator
from trnltk.morphology.contextful.likelihoodmetrics.wordformcollocation.test.test_calculator import _LikelihoodCalculatorTest
from trnltk.morphology.contextful.parser.sequencelikelihoodcalculator import UniformSequenceLikelihoodCalculator

class CachingNonContextParsingLikelihoodCalculatorTest(_LikelihoodCalculatorTest, unittest.TestCase):
    def setUp(self):
        super(CachingNonContextParsingLikelihoodCalculatorTest, self).setUp()
        database = self.mongodb_connection['trnltk']

        query_cache_collection = QueryCacheCollectionCreator(database).build(drop=True)

        self.generator = CachingNonContextParsingLikelihoodCalculator(self.collection_map, query_cache_collection)

    def test_generate_likelihood_of_one_word_given_two_context_words(self):
#        query_logger.setLevel(logging.DEBUG)
#        collocation_likelihood_calculator_logger.setLevel(logging.DEBUG)
        # don't override anything. added for better IDE support while running individual tests
        super(CachingNonContextParsingLikelihoodCalculatorTest, self).test_generate_likelihood_of_one_word_given_two_context_words()

    def test_generate_likelihood_of_one_word_given_one_leading_context_word(self):
#        query_logger.setLevel(logging.DEBUG)
#        collocation_likelihood_calculator_logger.setLevel(logging.DEBUG)
        # don't override anything. added for better IDE support while running individual tests
        super(CachingNonContextParsingLikelihoodCalculatorTest, self).test_generate_likelihood_of_one_word_given_one_leading_context_word()

    def test_generate_likelihood_of_one_word_given_two_leading_context_words(self):
#        query_logger.setLevel(logging.DEBUG)
#        collocation_likelihood_calculator_logger.setLevel(logging.DEBUG)
        # don't override anything. added for better IDE support while running individual tests
        super(CachingNonContextParsingLikelihoodCalculatorTest, self).test_generate_likelihood_of_one_word_given_two_leading_context_words()

    def test_generate_likelihood_of_one_word_given_one_following_context_word(self):
#        query_logger.setLevel(logging.DEBUG)
#        collocation_likelihood_calculator_logger.setLevel(logging.DEBUG)
        # don't override anything. added for better IDE support while running individual tests
        super(CachingNonContextParsingLikelihoodCalculatorTest, self).test_generate_likelihood_of_one_word_given_one_following_context_word()

    def test_generate_likelihood_of_one_word_given_one_context_word(self):
#        query_logger.setLevel(logging.DEBUG)
#        collocation_likelihood_calculator_logger.setLevel(logging.DEBUG)
        # don't override anything. added for better IDE support while running individual tests
        super(CachingNonContextParsingLikelihoodCalculatorTest, self).test_generate_likelihood_of_one_word_given_one_context_word()

    def _get_context(self, context):
        return context if context else []

class ContextParsingLikelihoodCalculatorCachingTest(_LikelihoodCalculatorTest, unittest.TestCase):
    def setUp(self):
        super(ContextParsingLikelihoodCalculatorCachingTest, self).setUp()

        database = self.mongodb_connection['trnltk']

        query_cache_collection = QueryCacheCollectionCreator(database).build(drop=True)

        database_index_builder = DatabaseIndexBuilder(self.collection_map)
        target_form_given_context_counter = CachingTargetFormGivenContextCounter(self.collection_map, query_cache_collection)
        ngram_frequency_smoother = CachedSimpleGoodTuringNGramFrequencySmoother()
        sequence_likelihood_calculator = UniformSequenceLikelihoodCalculator()

        self.generator = ContextParsingLikelihoodCalculator(database_index_builder, target_form_given_context_counter, ngram_frequency_smoother, sequence_likelihood_calculator)

    def test_generate_likelihood_of_one_word_given_two_context_words(self):
#        query_logger.setLevel(logging.DEBUG)
        #        collocation_likelihood_calculator_logger.setLevel(logging.DEBUG)
        # don't override anything. added for better IDE support while running individual tests
        super(ContextParsingLikelihoodCalculatorCachingTest, self).test_generate_likelihood_of_one_word_given_two_context_words()

    def test_generate_likelihood_of_one_word_given_one_leading_context_word(self):
    #        query_logger.setLevel(logging.DEBUG)
    #        collocation_likelihood_calculator_logger.setLevel(logging.DEBUG)
        # don't override anything. added for better IDE support while running individual tests
        super(ContextParsingLikelihoodCalculatorCachingTest, self).test_generate_likelihood_of_one_word_given_one_leading_context_word()

    def test_generate_likelihood_of_one_word_given_two_leading_context_words(self):
    #        query_logger.setLevel(logging.DEBUG)
    #        collocation_likelihood_calculator_logger.setLevel(logging.DEBUG)
        # don't override anything. added for better IDE support while running individual tests
        super(ContextParsingLikelihoodCalculatorCachingTest, self).test_generate_likelihood_of_one_word_given_two_leading_context_words()

    def test_generate_likelihood_of_one_word_given_one_following_context_word(self):
    #        query_logger.setLevel(logging.DEBUG)
    #        collocation_likelihood_calculator_logger.setLevel(logging.DEBUG)
        # don't override anything. added for better IDE support while running individual tests
        super(ContextParsingLikelihoodCalculatorCachingTest, self).test_generate_likelihood_of_one_word_given_one_following_context_word()

    def test_generate_likelihood_of_one_word_given_one_context_word(self):
    #        query_logger.setLevel(logging.DEBUG)
    #        collocation_likelihood_calculator_logger.setLevel(logging.DEBUG)
        # don't override anything. added for better IDE support while running individual tests
        super(ContextParsingLikelihoodCalculatorCachingTest, self).test_generate_likelihood_of_one_word_given_one_context_word()

    def _get_context(self, context):
        return [self.contextless_parser.parse(cw) for cw in context] if context else []

if __name__ == '__main__':
    unittest.main()
