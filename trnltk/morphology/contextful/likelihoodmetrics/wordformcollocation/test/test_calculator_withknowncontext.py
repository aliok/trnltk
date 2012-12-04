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
import unittest
from xml.dom.minidom import parse
import pymongo
from trnltk.morphology.contextful.likelihoodmetrics.hidden.database import DatabaseIndexBuilder
from trnltk.morphology.contextful.likelihoodmetrics.hidden.targetformgivencontextcounter import TargetFormGivenContextCounter
from trnltk.morphology.contextful.likelihoodmetrics.wordformcollocation.ngramfrequencysmoother import CachedSimpleGoodTuringNGramFrequencySmoother
from trnltk.morphology.contextful.likelihoodmetrics.wordformcollocation.parsecontext import MockMorphemeContainerBuilder
from trnltk.morphology.contextful.parser.sequencelikelihoodcalculator import UniformSequenceLikelihoodCalculator
from trnltk.morphology.contextless.parser.parser import  UpperCaseSupportingContextlessMorphologicalParser
from trnltk.morphology.contextless.parser.rootfinder import WordRootFinder, DigitNumeralRootFinder, ProperNounFromApostropheRootFinder, ProperNounWithoutApostropheRootFinder, TextNumeralRootFinder
from trnltk.morphology.model import formatter
from trnltk.morphology.morphotactics.basicsuffixgraph import BasicSuffixGraph
from trnltk.morphology.morphotactics.copulasuffixgraph import CopulaSuffixGraph
from trnltk.morphology.morphotactics.numeralsuffixgraph import NumeralSuffixGraph
from trnltk.morphology.morphotactics.predefinedpaths import PredefinedPaths
from trnltk.morphology.lexicon.lexiconloader import LexiconLoader
from trnltk.morphology.lexicon.rootgenerator import RootGenerator, RootMapGenerator
from trnltk.morphology.morphotactics.propernounsuffixgraph import ProperNounSuffixGraph
from trnltk.parseset.xmlbindings import ParseSetBinding
from trnltk.morphology.contextful.likelihoodmetrics.wordformcollocation.contextparsingcalculator import logger as collocation_likelihood_calculator_logger, ContextParsingLikelihoodCalculator
from trnltk.morphology.contextful.likelihoodmetrics.wordformcollocation.contextparsingcalculator import logger as query_logger

dom = parse(os.path.join(os.path.dirname(__file__), 'morphology_contextless_statistics_sample_parseset.xml'))
parseset = ParseSetBinding.build(dom.getElementsByTagName("parseset")[0])
parse_set_word_list = []
for sentence in parseset.sentences:
    parse_set_word_list.extend(sentence.words)

class LikelihoodCalculatorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(LikelihoodCalculatorTest, cls).setUpClass()
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
        target_form_given_context_counter = TargetFormGivenContextCounter(cls.collection_map)
        ngram_frequency_smoother = CachedSimpleGoodTuringNGramFrequencySmoother()
        sequence_likelihood_calculator = UniformSequenceLikelihoodCalculator()

        cls.generator = ContextParsingLikelihoodCalculator(database_index_builder, target_form_given_context_counter, ngram_frequency_smoother, sequence_likelihood_calculator)

    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        query_logger.setLevel(logging.INFO)
        collocation_likelihood_calculator_logger.setLevel(logging.INFO)

    def _test_generate_likelihood(self, surface, leading_context=None, following_context=None):
        assert leading_context or following_context

        likelihoods = []
        results = self.contextless_parser.parse(surface)

        for result in results:
            formatted_parse_result = formatter.format_morpheme_container_for_parseset(result)
            likelihood = 0.0
            if leading_context and following_context:
                likelihood = self.generator.calculate_likelihood(result, leading_context, following_context)
            elif leading_context:
                likelihood = self.generator.calculate_oneway_likelihood(result, leading_context, True)
            elif following_context:
                likelihood = self.generator.calculate_oneway_likelihood(result, following_context, False)

            likelihoods.append((formatted_parse_result, likelihood))

        for item in likelihoods:
            print item

    def test_generate_likelihood_of_one_word_given_one_leading_context_word_sc0(self):
#        query_logger.setLevel(logging.DEBUG)
#        collocation_likelihood_calculator_logger.setLevel(logging.DEBUG)

        context = [[MockMorphemeContainerBuilder.builder(None, u"bir", "Det").build()]]
        surface = u'erkek'

        self._test_generate_likelihood(surface=surface, leading_context=context, following_context=None)

    def test_generate_likelihood_of_one_word_given_one_leading_context_word_sc1(self):
    #        query_logger.setLevel(logging.DEBUG)
    #        collocation_likelihood_calculator_logger.setLevel(logging.DEBUG)

        context = [[MockMorphemeContainerBuilder.builder(None, u"bir", "Adj").build()]]
        surface = u'erkek'

        self._test_generate_likelihood(surface=surface, leading_context=context, following_context=None)

    def test_generate_likelihood_of_one_word_given_one_leading_context_word_sc2(self):
    #        query_logger.setLevel(logging.DEBUG)
    #        collocation_likelihood_calculator_logger.setLevel(logging.DEBUG)

        context = [[MockMorphemeContainerBuilder.builder(None, u".", "Punc").build()]]
        surface = u'Saçları'

        self._test_generate_likelihood(surface=surface, leading_context=context, following_context=None)

    def test_generate_likelihood_of_one_word_given_one_leading_context_word_sc3(self):
    #        query_logger.setLevel(logging.DEBUG)
    #        collocation_likelihood_calculator_logger.setLevel(logging.DEBUG)

        context = [[MockMorphemeContainerBuilder.builder(None, u".", "Punc").build()]]
        surface = u'Kerem'

        self._test_generate_likelihood(surface=surface, leading_context=context, following_context=None)

    def test_generate_likelihood_of_one_word_given_one_leading_context_word_sc4(self):
    #        query_logger.setLevel(logging.DEBUG)
    #        collocation_likelihood_calculator_logger.setLevel(logging.DEBUG)

        context = [[MockMorphemeContainerBuilder.builder(None, u"Kerem", "Noun", "Prop").build()]]
        surface = u'ter'

        self._test_generate_likelihood(surface=surface, leading_context=context, following_context=None)

    def test_generate_likelihood_of_one_word_given_two_leading_context_words_sc0(self):
    #        query_logger.setLevel(logging.DEBUG)
    #        collocation_likelihood_calculator_logger.setLevel(logging.DEBUG)

        context = [[MockMorphemeContainerBuilder.builder(None, u"gençten", "Noun").stem(u"genç", "Noun").lexeme(None, u"genç", "Adj").build()],[MockMorphemeContainerBuilder.builder(None, u"bir", "Det").build()]]
        surface = u'erkek'

        self._test_generate_likelihood(surface=surface, leading_context=context, following_context=None)

    def test_generate_likelihood_of_one_word_given_two_leading_context_words_sc1(self):
    #        query_logger.setLevel(logging.DEBUG)
    #        collocation_likelihood_calculator_logger.setLevel(logging.DEBUG)

        context = [[MockMorphemeContainerBuilder.builder(None, u"gençten", "Noun").stem(u"genç", "Noun").lexeme(None, u"genç", "Adj").build()],[MockMorphemeContainerBuilder.builder(None, u"bir", "Adj").build()]]
        surface = u'erkek'

        self._test_generate_likelihood(surface=surface, leading_context=context, following_context=None)

    def test_generate_likelihood_of_one_word_given_one_following_context_word_sc0(self):
    #        query_logger.setLevel(logging.DEBUG)
    #        collocation_likelihood_calculator_logger.setLevel(logging.DEBUG)

        context = [[MockMorphemeContainerBuilder.builder(None, u"girdi", "Verb").stem(u"gir", "Verb").lexeme(u"gir", "Verb").build()]]
        surface = u'erkek'

        self._test_generate_likelihood(surface=surface, leading_context=None, following_context=context)

    def test_generate_likelihood_of_one_word_given_one_following_context_word_sc1(self):
    #        query_logger.setLevel(logging.DEBUG)
    #        collocation_likelihood_calculator_logger.setLevel(logging.DEBUG)

        context = [[MockMorphemeContainerBuilder.builder(None, u"girdi", "Noun").stem(u"gir", "Verb").lexeme(u"gir", "Verb").build()]]
        surface = u'erkek'

        self._test_generate_likelihood(surface=surface, leading_context=None, following_context=context)

    def test_generate_likelihood_of_one_word_given_one_context_word(self):
    #        query_logger.setLevel(logging.DEBUG)
    #        collocation_likelihood_calculator_logger.setLevel(logging.DEBUG)

        leading_context = [[MockMorphemeContainerBuilder.builder(None, u"bir", "Det").build()]]
        surface = u'erkek'
        following_context = [[MockMorphemeContainerBuilder.builder(None, u"girdi", "Verb").stem(u"gir", "Verb").lexeme(u"gir", "Verb").build()]]

        self._test_generate_likelihood(surface=surface, leading_context=leading_context, following_context=following_context)

    def test_generate_likelihood_of_one_word_given_two_context_words(self):
    #        query_logger.setLevel(logging.DEBUG)
    #        collocation_likelihood_calculator_logger.setLevel(logging.DEBUG)

        leading_context = [[MockMorphemeContainerBuilder.builder(None, u"gençten", "Noun").stem(u"genç", "Noun").lexeme(u"genç", "Adj").build()],[MockMorphemeContainerBuilder.builder(None, u"bir", "Det").build()]]
        surface = u'erkek'
        following_context = [[MockMorphemeContainerBuilder.builder(None, u"girdi", "Verb").stem(u"gir", "Verb").lexeme(u"gir", "Verb").build()], [MockMorphemeContainerBuilder.builder(None, u".", "Punc").build()]]

        self._test_generate_likelihood(surface=surface, leading_context=leading_context, following_context=following_context)

if __name__ == '__main__':
    unittest.main()
