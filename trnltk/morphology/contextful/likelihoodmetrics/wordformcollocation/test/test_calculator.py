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
import os
import pprint
import unittest
import pymongo
from hamcrest import *
from mock import Mock
from trnltk.morphology.contextful.likelihoodmetrics.hidden.database import DatabaseIndexBuilder
from trnltk.morphology.contextful.likelihoodmetrics.hidden.targetformgivencontextcounter import TargetFormGivenContextCounter
from trnltk.morphology.contextful.likelihoodmetrics.wordformcollocation.ngramfrequencysmoother import CachedSimpleGoodTuringNGramFrequencySmoother
from trnltk.morphology.contextful.likelihoodmetrics.wordformcollocation.noncontextparsingcalculator import NonContextParsingLikelihoodCalculator
from trnltk.morphology.contextful.parser.sequencelikelihoodcalculator import SequenceLikelihoodCalculator, UniformSequenceLikelihoodCalculator
from trnltk.morphology.contextless.parser.parser import ContextlessMorphologicalParser
from trnltk.morphology.contextless.parser.rootfinder import WordRootFinder, DigitNumeralRootFinder, ProperNounFromApostropheRootFinder, ProperNounWithoutApostropheRootFinder, TextNumeralRootFinder
from trnltk.morphology.model import formatter
from trnltk.morphology.morphotactics.basicsuffixgraph import BasicSuffixGraph
from trnltk.morphology.morphotactics.copulasuffixgraph import CopulaSuffixGraph
from trnltk.morphology.morphotactics.numeralsuffixgraph import NumeralSuffixGraph
from trnltk.morphology.morphotactics.predefinedpaths import PredefinedPaths
from trnltk.morphology.lexicon.lexiconloader import LexiconLoader
from trnltk.morphology.lexicon.rootgenerator import RootGenerator, RootMapGenerator
from trnltk.morphology.morphotactics.propernounsuffixgraph import ProperNounSuffixGraph
from trnltk.morphology.contextful.likelihoodmetrics.wordformcollocation.contextparsingcalculator import  ContextParsingLikelihoodCalculator
from trnltk.morphology.contextful.likelihoodmetrics.wordformcollocation.contextparsingcalculator import logger as collocation_likelihood_calculator_logger
from trnltk.morphology.contextful.likelihoodmetrics.wordformcollocation.contextparsingcalculator import query_logger

class _LikelihoodCalculatorTest(object):
    @classmethod
    def setUpClass(cls):
        super(_LikelihoodCalculatorTest, cls).setUpClass()
        all_roots = []

        lexemes = LexiconLoader.load_from_file(os.path.join(os.path.dirname(__file__), '../../../../../resources/master_dictionary.txt'))
        for di in lexemes:
            all_roots.extend(RootGenerator.generate(di))

        root_map_generator = RootMapGenerator()
        cls.root_map = root_map_generator.generate(all_roots)

        suffix_graph = CopulaSuffixGraph(NumeralSuffixGraph(ProperNounSuffixGraph(BasicSuffixGraph())))
        suffix_graph.initialize()

        predefined_paths = PredefinedPaths(cls.root_map, suffix_graph)
        predefined_paths.create_predefined_paths()

        word_root_finder = WordRootFinder(cls.root_map)
        digit_numeral_root_finder = DigitNumeralRootFinder()
        text_numeral_root_finder = TextNumeralRootFinder(cls.root_map)
        proper_noun_from_apostrophe_root_finder = ProperNounFromApostropheRootFinder()
        proper_noun_without_apostrophe_root_finder = ProperNounWithoutApostropheRootFinder()

        cls.contextless_parser = ContextlessMorphologicalParser(suffix_graph, predefined_paths,
            [word_root_finder, digit_numeral_root_finder, text_numeral_root_finder,
             proper_noun_from_apostrophe_root_finder, proper_noun_without_apostrophe_root_finder])

        cls.mongodb_connection = pymongo.Connection(host='127.0.0.1')
        cls.collection_map = {
            1: cls.mongodb_connection['trnltk']['wordUnigrams999'],
            2: cls.mongodb_connection['trnltk']['wordBigrams999'],
            3: cls.mongodb_connection['trnltk']['wordTrigrams999']
        }

        cls.generator = None

    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        query_logger.setLevel(logging.INFO)
        collocation_likelihood_calculator_logger.setLevel(logging.INFO)

    def _test_generate_likelihood(self, surface, leading_context=None, following_context=None, create_calculation_context=False):
        self.generator.build_indexes()

        assert leading_context or following_context

        leading_context = self._get_context(leading_context)
        following_context = self._get_context(following_context)

        likelihoods = []
        results = self.contextless_parser.parse(surface)
        for result in results:
            calculation_context = None
            if create_calculation_context:
                calculation_context = {}

            formatted_parse_result = formatter.format_morpheme_container_for_parseset(result)
            likelihood = 0.0
            if leading_context and following_context:
                likelihood = self.generator.calculate_likelihood(result, leading_context, following_context, calculation_context)
            elif leading_context:
                likelihood = self.generator.calculate_oneway_likelihood(result, leading_context, True, calculation_context)
            elif following_context:
                likelihood = self.generator.calculate_oneway_likelihood(result, following_context, False, calculation_context)

            likelihoods.append((formatted_parse_result, likelihood, calculation_context))

        for item in likelihoods:
            pprint.pprint(item)

    def _get_context(self, context):
        raise NotImplementedError()

    def test_generate_likelihood_of_one_word_given_one_leading_context_word(self
    ):
        context = [u'bir']
        surface = u'erkek'

        self._test_generate_likelihood(surface=surface, leading_context=context, following_context=None, create_calculation_context=True)

    def test_generate_likelihood_of_one_word_given_two_leading_context_words(self):
        context = [u'gençten', u'bir']
        surface = u'erkek'

        self._test_generate_likelihood(surface=surface, leading_context=context, following_context=None)

    def test_generate_likelihood_of_one_word_given_one_following_context_word(self):
        context = [u'girdi']
        surface = u'erkek'

        self._test_generate_likelihood(surface=surface, leading_context=None, following_context=context)

    def test_generate_likelihood_of_one_word_given_one_context_word(self):
        leading_context = [u'bir']
        surface = u'erkek'
        following_context = [u'girdi']

        self._test_generate_likelihood(surface=surface, leading_context=leading_context, following_context=following_context)

    def test_generate_likelihood_of_one_word_given_two_context_words(self):
        leading_context = [u'gençten', u'bir']
        surface = u'erkek'
        following_context = [u'girdi', u'.']

        self._test_generate_likelihood(surface=surface, leading_context=leading_context, following_context=following_context)


class NonContextParsingLikelihoodCalculatorTest(_LikelihoodCalculatorTest, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(NonContextParsingLikelihoodCalculatorTest, cls).setUpClass()

        cls.generator = NonContextParsingLikelihoodCalculator(cls.collection_map)

    def test_generate_likelihood_of_one_word_given_two_context_words(self):
#        query_logger.setLevel(logging.DEBUG)
#        collocation_likelihood_calculator_logger.setLevel(logging.DEBUG)
        # don't override anything. added for better IDE support while running individual tests
        super(NonContextParsingLikelihoodCalculatorTest, self).test_generate_likelihood_of_one_word_given_two_context_words()

    def test_generate_likelihood_of_one_word_given_one_leading_context_word(self):
#        query_logger.setLevel(logging.DEBUG)
#        collocation_likelihood_calculator_logger.setLevel(logging.DEBUG)
        # don't override anything. added for better IDE support while running individual tests
        super(NonContextParsingLikelihoodCalculatorTest, self).test_generate_likelihood_of_one_word_given_one_leading_context_word()

    def test_generate_likelihood_of_one_word_given_two_leading_context_words(self):
#        query_logger.setLevel(logging.DEBUG)
#        collocation_likelihood_calculator_logger.setLevel(logging.DEBUG)
        # don't override anything. added for better IDE support while running individual tests
        super(NonContextParsingLikelihoodCalculatorTest, self).test_generate_likelihood_of_one_word_given_two_leading_context_words()

    def test_generate_likelihood_of_one_word_given_one_following_context_word(self):
#        query_logger.setLevel(logging.DEBUG)
#        collocation_likelihood_calculator_logger.setLevel(logging.DEBUG)
        # don't override anything. added for better IDE support while running individual tests
        super(NonContextParsingLikelihoodCalculatorTest, self).test_generate_likelihood_of_one_word_given_one_following_context_word()

    def test_generate_likelihood_of_one_word_given_one_context_word(self):
#        query_logger.setLevel(logging.DEBUG)
#        collocation_likelihood_calculator_logger.setLevel(logging.DEBUG)
        # don't override anything. added for better IDE support while running individual tests
        super(NonContextParsingLikelihoodCalculatorTest, self).test_generate_likelihood_of_one_word_given_one_context_word()

    def _get_context(self, context):
        return context if context else []

class ContextParsingLikelihoodCalculatorTest(_LikelihoodCalculatorTest, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(ContextParsingLikelihoodCalculatorTest, cls).setUpClass()

        database_index_builder = DatabaseIndexBuilder(cls.collection_map)
        target_form_given_context_counter = TargetFormGivenContextCounter(cls.collection_map)
        ngram_frequency_smoother = CachedSimpleGoodTuringNGramFrequencySmoother()
        sequence_likelihood_calculator = UniformSequenceLikelihoodCalculator()

        cls.generator = ContextParsingLikelihoodCalculator(database_index_builder, target_form_given_context_counter, ngram_frequency_smoother, sequence_likelihood_calculator)

    def test_generate_likelihood_of_one_word_given_two_context_words(self):
        #        query_logger.setLevel(logging.DEBUG)
        #        collocation_likelihood_calculator_logger.setLevel(logging.DEBUG)
        # don't override anything. added for better IDE support while running individual tests
        super(ContextParsingLikelihoodCalculatorTest, self).test_generate_likelihood_of_one_word_given_two_context_words()

    def test_generate_likelihood_of_one_word_given_one_leading_context_word(self):
    #        query_logger.setLevel(logging.DEBUG)
    #        collocation_likelihood_calculator_logger.setLevel(logging.DEBUG)
        # don't override anything. added for better IDE support while running individual tests
        super(ContextParsingLikelihoodCalculatorTest, self).test_generate_likelihood_of_one_word_given_one_leading_context_word()

    def test_generate_likelihood_of_one_word_given_two_leading_context_words(self):
    #        query_logger.setLevel(logging.DEBUG)
    #        collocation_likelihood_calculator_logger.setLevel(logging.DEBUG)
        # don't override anything. added for better IDE support while running individual tests
        super(ContextParsingLikelihoodCalculatorTest, self).test_generate_likelihood_of_one_word_given_two_leading_context_words()

    def test_generate_likelihood_of_one_word_given_one_following_context_word(self):
    #        query_logger.setLevel(logging.DEBUG)
    #        collocation_likelihood_calculator_logger.setLevel(logging.DEBUG)
        # don't override anything. added for better IDE support while running individual tests
        super(ContextParsingLikelihoodCalculatorTest, self).test_generate_likelihood_of_one_word_given_one_following_context_word()

    def test_generate_likelihood_of_one_word_given_one_context_word(self):
    #        query_logger.setLevel(logging.DEBUG)
    #        collocation_likelihood_calculator_logger.setLevel(logging.DEBUG)
        # don't override anything. added for better IDE support while running individual tests
        super(ContextParsingLikelihoodCalculatorTest, self).test_generate_likelihood_of_one_word_given_one_context_word()

    def _get_context(self, context):
        return [self.contextless_parser.parse(cw) for cw in context] if context else []


class ParseResultsCartesianProductTest(unittest.TestCase):
    def setUp(self):
        ngram_frequency_smoother = CachedSimpleGoodTuringNGramFrequencySmoother()
        self.generator = ContextParsingLikelihoodCalculator(None, None, ngram_frequency_smoother, None)

    def test_should_get_cartesian_products_of_parse_results_when_context_is_empty(self):
        assert_that(self.generator._get_cartesian_products_of_context_parse_results(None), equal_to([]))
        assert_that(self.generator._get_cartesian_products_of_context_parse_results([]), equal_to([]))
        assert_that(self.generator._get_cartesian_products_of_context_parse_results([[]]), equal_to([]))
        assert_that(self.generator._get_cartesian_products_of_context_parse_results([[],[]]), equal_to([]))

    def test_should_get_cartesian_products_of_parse_results_when_context_has_one_item(self):
        morpheme_container_a = Mock()
        morpheme_container_b = Mock()
        assert_that(self.generator._get_cartesian_products_of_context_parse_results([[morpheme_container_a]]), equal_to([[morpheme_container_a]]))
        assert_that(self.generator._get_cartesian_products_of_context_parse_results([[morpheme_container_a, morpheme_container_b]]), equal_to([[morpheme_container_a],[morpheme_container_b]]))
        assert_that(self.generator._get_cartesian_products_of_context_parse_results([[morpheme_container_a],[]]), equal_to([[morpheme_container_a]]))
        assert_that(self.generator._get_cartesian_products_of_context_parse_results([[morpheme_container_a, morpheme_container_b],[]]), equal_to([[morpheme_container_a],[morpheme_container_b]]))
        assert_that(self.generator._get_cartesian_products_of_context_parse_results([[],[morpheme_container_a]]), equal_to([[morpheme_container_a]]))
        assert_that(self.generator._get_cartesian_products_of_context_parse_results([[],[morpheme_container_a, morpheme_container_b]]), equal_to([[morpheme_container_a],[morpheme_container_b]]))

    def test_should_get_cartesian_products_of_parse_results_when_context_has_two_items(self):
        morpheme_container_a_0 = Mock()
        morpheme_container_a_1 = Mock()
        morpheme_container_b_0 = Mock()
        morpheme_container_b_1 = Mock()

        assert_that(self.generator._get_cartesian_products_of_context_parse_results([
            [morpheme_container_a_0],
            [morpheme_container_b_0]
        ]), equal_to([
            [morpheme_container_a_0, morpheme_container_b_0]
        ]))

        assert_that(self.generator._get_cartesian_products_of_context_parse_results([
            [morpheme_container_a_0, morpheme_container_a_1],
            [morpheme_container_b_0]
        ]), equal_to([
            [morpheme_container_a_0, morpheme_container_b_0],
            [morpheme_container_a_1, morpheme_container_b_0]

        ]))

        assert_that(self.generator._get_cartesian_products_of_context_parse_results([
            [morpheme_container_a_0],
            [morpheme_container_b_0, morpheme_container_b_1]
        ]), equal_to([
            [morpheme_container_a_0, morpheme_container_b_0],
            [morpheme_container_a_0, morpheme_container_b_1]

        ]))

        assert_that(self.generator._get_cartesian_products_of_context_parse_results([
            [morpheme_container_a_0, morpheme_container_a_1],
            [morpheme_container_b_0, morpheme_container_b_1]
        ]), equal_to([
            [morpheme_container_a_0, morpheme_container_b_0],
            [morpheme_container_a_0, morpheme_container_b_1],
            [morpheme_container_a_1, morpheme_container_b_0],
            [morpheme_container_a_1, morpheme_container_b_1]

        ]))

    def test_should_get_cartesian_products_of_parse_results_when_context_has_two_items_and_blank_ones(self):
        morpheme_container_a_0 = Mock()
        morpheme_container_a_1 = Mock()
        morpheme_container_b_0 = Mock()
        morpheme_container_b_1 = Mock()

        assert_that(self.generator._get_cartesian_products_of_context_parse_results([
            [morpheme_container_a_0],
            [morpheme_container_b_0],
            []
        ]), equal_to([
            [morpheme_container_a_0, morpheme_container_b_0]
        ]))

        assert_that(self.generator._get_cartesian_products_of_context_parse_results([
            [],
            [morpheme_container_a_0, morpheme_container_a_1],
            [morpheme_container_b_0]
        ]), equal_to([
            [morpheme_container_a_0, morpheme_container_b_0],
            [morpheme_container_a_1, morpheme_container_b_0]

        ]))

        assert_that(self.generator._get_cartesian_products_of_context_parse_results([
            [morpheme_container_a_0],
            [],
            [morpheme_container_b_0, morpheme_container_b_1]
        ]), equal_to([
            [morpheme_container_a_0, morpheme_container_b_0],
            [morpheme_container_a_0, morpheme_container_b_1]

        ]))

        assert_that(self.generator._get_cartesian_products_of_context_parse_results([
            [morpheme_container_a_0, morpheme_container_a_1],
            [morpheme_container_b_0, morpheme_container_b_1],
            []
        ]), equal_to([
            [morpheme_container_a_0, morpheme_container_b_0],
            [morpheme_container_a_0, morpheme_container_b_1],
            [morpheme_container_a_1, morpheme_container_b_0],
            [morpheme_container_a_1, morpheme_container_b_1]

        ]))

    def test_should_get_cartesian_products_of_parse_results_when_context_has_three(self):
        morpheme_container_a_0 = Mock()
        morpheme_container_b_0 = Mock()
        morpheme_container_c_0 = Mock()
        morpheme_container_a_1 = Mock()
        morpheme_container_b_1 = Mock()
        morpheme_container_c_1 = Mock()

        assert_that(self.generator._get_cartesian_products_of_context_parse_results([
            [morpheme_container_a_0],
            [morpheme_container_b_0],
            [morpheme_container_c_0]
        ]), equal_to([
            [morpheme_container_a_0, morpheme_container_b_0, morpheme_container_c_0]
        ]))

        assert_that(self.generator._get_cartesian_products_of_context_parse_results([
            [],
            [morpheme_container_a_0],
            [morpheme_container_b_0],
            [morpheme_container_c_0]
        ]), equal_to([
            [morpheme_container_a_0, morpheme_container_b_0, morpheme_container_c_0]
        ]))

        assert_that(self.generator._get_cartesian_products_of_context_parse_results([
            [morpheme_container_a_0],
            [],
            [morpheme_container_b_0],
            [morpheme_container_c_0]
        ]), equal_to([
            [morpheme_container_a_0, morpheme_container_b_0, morpheme_container_c_0]
        ]))

        assert_that(self.generator._get_cartesian_products_of_context_parse_results([
            [morpheme_container_a_0],
            [morpheme_container_b_0],
            [],
            [morpheme_container_c_0]
        ]), equal_to([
            [morpheme_container_a_0, morpheme_container_b_0, morpheme_container_c_0]
        ]))

        assert_that(self.generator._get_cartesian_products_of_context_parse_results([
            [morpheme_container_a_0],
            [],
            [morpheme_container_b_0],
            [],
            [morpheme_container_c_0],
            []
        ]), equal_to([
            [morpheme_container_a_0, morpheme_container_b_0, morpheme_container_c_0]
        ]))

        assert_that(self.generator._get_cartesian_products_of_context_parse_results([
            [morpheme_container_a_0, morpheme_container_a_1],
            [],
            [morpheme_container_b_0],
            [morpheme_container_c_0, morpheme_container_c_1],
            []
        ]), equal_to([
            [morpheme_container_a_0, morpheme_container_b_0, morpheme_container_c_0],
            [morpheme_container_a_0, morpheme_container_b_0, morpheme_container_c_1],
            [morpheme_container_a_1, morpheme_container_b_0, morpheme_container_c_0],
            [morpheme_container_a_1, morpheme_container_b_0, morpheme_container_c_1],
        ]))

        assert_that(self.generator._get_cartesian_products_of_context_parse_results([
            [],
            [],
            [morpheme_container_a_0],
            [morpheme_container_b_0, morpheme_container_b_1],
            [morpheme_container_c_0, morpheme_container_c_1],
        ]), equal_to([
            [morpheme_container_a_0, morpheme_container_b_0, morpheme_container_c_0],
            [morpheme_container_a_0, morpheme_container_b_0, morpheme_container_c_1],
            [morpheme_container_a_0, morpheme_container_b_1, morpheme_container_c_0],
            [morpheme_container_a_0, morpheme_container_b_1, morpheme_container_c_1],
        ]))

        assert_that(self.generator._get_cartesian_products_of_context_parse_results([
            [morpheme_container_a_0, morpheme_container_a_1],
            [morpheme_container_b_0, morpheme_container_b_1],
            [],
            [morpheme_container_c_0],
        ]), equal_to([
            [morpheme_container_a_0, morpheme_container_b_0, morpheme_container_c_0],
            [morpheme_container_a_0, morpheme_container_b_1, morpheme_container_c_0],
            [morpheme_container_a_1, morpheme_container_b_0, morpheme_container_c_0],
            [morpheme_container_a_1, morpheme_container_b_1, morpheme_container_c_0],
        ]))

        assert_that(self.generator._get_cartesian_products_of_context_parse_results([
            [morpheme_container_a_0, morpheme_container_a_1],
            [morpheme_container_b_0, morpheme_container_b_1],
            [morpheme_container_c_0, morpheme_container_c_1],
            [],
            [],
        ]), equal_to([
            [morpheme_container_a_0, morpheme_container_b_0, morpheme_container_c_0],
            [morpheme_container_a_0, morpheme_container_b_0, morpheme_container_c_1],
            [morpheme_container_a_0, morpheme_container_b_1, morpheme_container_c_0],
            [morpheme_container_a_0, morpheme_container_b_1, morpheme_container_c_1],
            [morpheme_container_a_1, morpheme_container_b_0, morpheme_container_c_0],
            [morpheme_container_a_1, morpheme_container_b_0, morpheme_container_c_1],
            [morpheme_container_a_1, morpheme_container_b_1, morpheme_container_c_0],
            [morpheme_container_a_1, morpheme_container_b_1, morpheme_container_c_1],
        ]))


    def test_should_get_cartesian_products_of_parse_results_when_context_has_four(self):
        morpheme_container_a_0 = Mock()
        morpheme_container_b_0 = Mock()
        morpheme_container_c_0 = Mock()
        morpheme_container_d_0 = Mock()

        assert_that(self.generator._get_cartesian_products_of_context_parse_results([
            [morpheme_container_a_0],
            [morpheme_container_b_0],
            [morpheme_container_c_0],
            [morpheme_container_d_0]
        ]), equal_to([
            [morpheme_container_a_0, morpheme_container_b_0, morpheme_container_c_0, morpheme_container_d_0]
        ]))

if __name__ == '__main__':
    unittest.main()
