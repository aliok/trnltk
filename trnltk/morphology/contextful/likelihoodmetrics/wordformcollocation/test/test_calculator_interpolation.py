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
from xml.dom.minidom import parse
from mockito import *
from hamcrest import *
import pymongo
from trnltk.morphology.contextful.likelihoodmetrics.hidden.database import DatabaseIndexBuilder
from trnltk.morphology.contextful.likelihoodmetrics.hidden.targetformgivencontextcounter import  InMemoryCachingTargetFormGivenContextCounter
from trnltk.morphology.contextful.likelihoodmetrics.wordformcollocation.contextparsingcalculator import logger as query_logger
from trnltk.morphology.contextful.likelihoodmetrics.wordformcollocation.contextparsingcalculator import logger as collocation_likelihood_calculator_logger, ContextParsingLikelihoodCalculator
from trnltk.morphology.contextful.likelihoodmetrics.wordformcollocation.interpolatingcalculator import InterpolatingLikelihoodCalculator
from trnltk.morphology.contextful.likelihoodmetrics.wordformcollocation.ngramfrequencysmoother import CachedSimpleGoodTuringNGramFrequencySmoother
from trnltk.morphology.contextful.likelihoodmetrics.wordformcollocation.parsecontext import MockMorphemeContainerBuilder
from trnltk.morphology.contextful.parser.sequencelikelihoodcalculator import UniformSequenceLikelihoodCalculator
from trnltk.morphology.contextless.parser.parser import UpperCaseSupportingContextlessMorphologicalParser
from trnltk.morphology.contextless.parser.rootfinder import WordRootFinder, DigitNumeralRootFinder, TextNumeralRootFinder, ProperNounFromApostropheRootFinder, ProperNounWithoutApostropheRootFinder
from trnltk.morphology.lexicon.lexiconloader import LexiconLoader
from trnltk.morphology.lexicon.rootgenerator import RootGenerator, RootMapGenerator
from trnltk.morphology.model import formatter
from trnltk.morphology.morphotactics.basicsuffixgraph import BasicSuffixGraph
from trnltk.morphology.morphotactics.copulasuffixgraph import CopulaSuffixGraph
from trnltk.morphology.morphotactics.numeralsuffixgraph import NumeralSuffixGraph
from trnltk.morphology.morphotactics.predefinedpaths import PredefinedPaths
from trnltk.morphology.morphotactics.propernounsuffixgraph import ProperNounSuffixGraph
from trnltk.parseset.xmlbindings import ParseSetBinding

class InterpolatingLikelihoodCalculatorTest(unittest.TestCase):
    def setUp(self):
        super(InterpolatingLikelihoodCalculatorTest, self).setUp()

    def test_calculate_one_way_likelihood_bigram_and_target_comes_after(self):
        mock_context_item_0 = mock()
        context = [mock_context_item_0]

        target = mock()

        wrapped_calculator = mock()

        calculation_context = None

        when(wrapped_calculator).calculate_oneway_likelihood(target, [mock_context_item_0], True, calculation_context).thenReturn(0.5)

        interpolating_calculator = InterpolatingLikelihoodCalculator(wrapped_calculator)

        interpolated_likelihood = interpolating_calculator.calculate_oneway_likelihood(target, context, True, calculation_context)

        assert_that(interpolated_likelihood, equal_to(0.5))

        verify(wrapped_calculator).calculate_oneway_likelihood(target, [mock_context_item_0], True, calculation_context)
        verifyNoMoreInteractions(wrapped_calculator)

    def test_calculate_one_way_likelihood_bigram_and_target_comes_before(self):
        mock_context_item_0 = mock()
        context = [mock_context_item_0]

        target = mock()

        wrapped_calculator = mock()

        calculation_context = None

        when(wrapped_calculator).calculate_oneway_likelihood(target, [mock_context_item_0], False, calculation_context).thenReturn(0.5)

        interpolating_calculator = InterpolatingLikelihoodCalculator(wrapped_calculator)

        interpolated_likelihood = interpolating_calculator.calculate_oneway_likelihood(target, context, False, calculation_context)

        assert_that(interpolated_likelihood, equal_to(0.5))

        verify(wrapped_calculator).calculate_oneway_likelihood(target, [mock_context_item_0], False, calculation_context)
        verifyNoMoreInteractions(wrapped_calculator)

    def test_calculate_one_way_likelihood_trigram_and_target_comes_after(self):
        mock_context_item_0 = mock()
        mock_context_item_1 = mock()
        context = [mock_context_item_0, mock_context_item_1]

        target = mock()

        wrapped_calculator = mock()

        calculation_context = None

        when(wrapped_calculator).calculate_oneway_likelihood(target, [mock_context_item_1], True, calculation_context).thenReturn(0.5)
        when(wrapped_calculator).calculate_oneway_likelihood(target, [mock_context_item_0, mock_context_item_1], True, calculation_context).thenReturn(0.2)

        interpolating_calculator = InterpolatingLikelihoodCalculator(wrapped_calculator)

        interpolated_likelihood = interpolating_calculator.calculate_oneway_likelihood(target, context, True, calculation_context)

        assert_that(interpolated_likelihood, equal_to(0.5 * 1 / 11 + 0.2 * 10 / 11))

        verify(wrapped_calculator).calculate_oneway_likelihood(target, [mock_context_item_1], True, calculation_context)
        verify(wrapped_calculator).calculate_oneway_likelihood(target, [mock_context_item_0, mock_context_item_1], True, calculation_context)
        verifyNoMoreInteractions(wrapped_calculator)

    def test_calculate_one_way_likelihood_trigram_and_target_comes_before(self):
        mock_context_item_0 = mock()
        mock_context_item_1 = mock()
        context = [mock_context_item_0, mock_context_item_1]

        target = mock()

        wrapped_calculator = mock()

        calculation_context = None

        when(wrapped_calculator).calculate_oneway_likelihood(target, [mock_context_item_0], False, calculation_context).thenReturn(0.5)
        when(wrapped_calculator).calculate_oneway_likelihood(target, [mock_context_item_0, mock_context_item_1], False, calculation_context).thenReturn(0.2)

        interpolating_calculator = InterpolatingLikelihoodCalculator(wrapped_calculator)

        interpolated_likelihood = interpolating_calculator.calculate_oneway_likelihood(target, context, False, calculation_context)

        assert_that(interpolated_likelihood, equal_to(0.5 * 1 / 11 + 0.2 * 10 / 11))

        verify(wrapped_calculator).calculate_oneway_likelihood(target, [mock_context_item_0], False, calculation_context)
        verify(wrapped_calculator).calculate_oneway_likelihood(target, [mock_context_item_0, mock_context_item_1], False, calculation_context)
        verifyNoMoreInteractions(wrapped_calculator)

    def test_calculate_one_way_likelihood_4gram_and_target_comes_after(self):
        # not practical but just try
        mock_context_item_0 = mock()
        mock_context_item_1 = mock()
        mock_context_item_2 = mock()
        context = [mock_context_item_0, mock_context_item_1, mock_context_item_2]

        target = mock()

        wrapped_calculator = mock()

        calculation_context = None

        when(wrapped_calculator).calculate_oneway_likelihood(target, [mock_context_item_2], True, calculation_context).thenReturn(0.5)
        when(wrapped_calculator).calculate_oneway_likelihood(target, [mock_context_item_1, mock_context_item_2], True, calculation_context).thenReturn(0.2)
        when(wrapped_calculator).calculate_oneway_likelihood(target, [mock_context_item_0, mock_context_item_1, mock_context_item_2], True,
            calculation_context).thenReturn(0.05)

        interpolating_calculator = InterpolatingLikelihoodCalculator(wrapped_calculator)

        interpolated_likelihood = interpolating_calculator.calculate_oneway_likelihood(target, context, True, calculation_context)

        assert_that(interpolated_likelihood, equal_to(0.5 * 1 / 111 + 0.2 * 10 / 111 + 0.05 * 100 / 111))

        verify(wrapped_calculator).calculate_oneway_likelihood(target, [mock_context_item_2], True, calculation_context)
        verify(wrapped_calculator).calculate_oneway_likelihood(target, [mock_context_item_1, mock_context_item_2], True, calculation_context)
        verify(wrapped_calculator).calculate_oneway_likelihood(target, [mock_context_item_0, mock_context_item_1, mock_context_item_2], True,
            calculation_context)
        verifyNoMoreInteractions(wrapped_calculator)

dom = parse(os.path.join(os.path.dirname(__file__), 'morphology_contextless_statistics_sample_parseset.xml'))
parseset = ParseSetBinding.build(dom.getElementsByTagName("parseset")[0])
parse_set_word_list = []
for sentence in parseset.sentences:
    parse_set_word_list.extend(sentence.words)

class InterpolatingLikelihoodCalculatorCalculationContextTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(InterpolatingLikelihoodCalculatorCalculationContextTest, cls).setUpClass()
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

        cls.contextless_parser = UpperCaseSupportingContextlessMorphologicalParser(suffix_graph, predefined_paths,
            [word_root_finder, digit_numeral_root_finder, text_numeral_root_finder,
             proper_noun_from_apostrophe_root_finder, proper_noun_without_apostrophe_root_finder])

        mongodb_connection = pymongo.Connection(host='127.0.0.1')
        cls.collection_map = {
            1: mongodb_connection['trnltk']['wordUnigrams999'],
            2: mongodb_connection['trnltk']['wordBigrams999'],
            3: mongodb_connection['trnltk']['wordTrigrams999']
        }

        database_index_builder = DatabaseIndexBuilder(cls.collection_map)
        target_form_given_context_counter = InMemoryCachingTargetFormGivenContextCounter(cls.collection_map)
        ngram_frequency_smoother = CachedSimpleGoodTuringNGramFrequencySmoother()
        sequence_likelihood_calculator = UniformSequenceLikelihoodCalculator()

        wrapped_generator = ContextParsingLikelihoodCalculator(database_index_builder, target_form_given_context_counter, ngram_frequency_smoother, sequence_likelihood_calculator)

        cls.generator = InterpolatingLikelihoodCalculator(wrapped_generator)

    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        query_logger.setLevel(logging.INFO)
        collocation_likelihood_calculator_logger.setLevel(logging.INFO)

    def _test_generate_likelihood(self, surface, leading_context=None, following_context=None, calculation_context=None):
        assert leading_context or following_context

        likelihoods = []
        results = self.contextless_parser.parse(surface)

        for result in results:
            formatted_parse_result = formatter.format_morpheme_container_for_parseset(result)
            likelihood = 0.0
            if leading_context and following_context:
                likelihood = self.generator.calculate_likelihood(result, leading_context, following_context, calculation_context)
            elif leading_context:
                likelihood = self.generator.calculate_oneway_likelihood(result, leading_context, True, calculation_context)
            elif following_context:
                likelihood = self.generator.calculate_oneway_likelihood(result, following_context, False, calculation_context)

            likelihoods.append((formatted_parse_result, likelihood))

        for item in likelihoods:
            print item

    def test_generate_likelihood_of_one_word_given_one_leading_context_word(self):
        context = [[MockMorphemeContainerBuilder.builder(None, u"bir", "Det").build()]]
        surface = u'erkek'

        calculation_context = {}

        self._test_generate_likelihood(surface=surface, leading_context=context, calculation_context=calculation_context)

        pprint.pprint(calculation_context)

    def test_generate_likelihood_of_one_word_given_two_context_words(self):
        leading_context = [[MockMorphemeContainerBuilder.builder(None, u"gençten", "Noun").stem(u"genç", "Noun").lexeme(u"genç", "Adj").build()],[MockMorphemeContainerBuilder.builder(None, u"bir", "Det").build()]]
        surface = u'erkek'
        following_context = [[MockMorphemeContainerBuilder.builder(None, u"girdi", "Verb").stem(u"gir", "Verb").lexeme(u"gir", "Verb").build()], [MockMorphemeContainerBuilder.builder(None, u".", "Punc").build()]]

        calculation_context = {}

        self._test_generate_likelihood(surface=surface, leading_context=leading_context, following_context=following_context, calculation_context=calculation_context)

        pprint.pprint(calculation_context)

if __name__ == '__main__':
    unittest.main()
