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
from operator import itemgetter
import os
import unittest
from xml.dom.minidom import parse
import pymongo
import datetime
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
from trnltk.ngrams.ngramgenerator import WordNGramGenerator
from trnltk.parseset.xmlbindings import ParseSetBinding, UnparsableWordBinding
from trnltk.morphology.contextful.likelihoodmetrics.wordformcollocation.contextparsingcalculator import logger as collocation_likelihood_calculator_logger, ContextParsingLikelihoodCalculator
from trnltk.morphology.contextful.likelihoodmetrics.wordformcollocation.contextparsingcalculator import logger as query_logger

class _BaseLikelihoodCalculatorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(_BaseLikelihoodCalculatorTest, cls).setUpClass()
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

    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        query_logger.setLevel(logging.INFO)
        collocation_likelihood_calculator_logger.setLevel(logging.INFO)

    def _test_calculate_with_parseset_n(self, parseset_index, leading_context_size, following_context_size):
        start_time = datetime.datetime.today()

        self.generator = self.create_calculator(parseset_index)

        dom = parse(os.path.join(os.path.dirname(__file__), '../../../../../testresources/parsesets/parseset{}.xml'.format(parseset_index)))
        parseset = ParseSetBinding.build(dom.getElementsByTagName("parseset")[0])
        self.parse_set_word_list = []
        for sentence in parseset.sentences:
            self.parse_set_word_list.extend(sentence.words)

        self._test_generate_likelihoods(leading_context_size, following_context_size)

        end_time = datetime.datetime.today()
        print u'Done in {} seconds for {} words'.format(end_time-start_time, len(self.parse_set_word_list)-1)
        print u'Average in {} seconds'.format((end_time-start_time)/(len(self.parse_set_word_list)-1))

    def _test_generate_likelihoods(self, leading_context_size, following_context_size):
        for index,word in enumerate(self.parse_set_word_list):
            print u'Checking word {} {}'.format(index, word.str)
            if index < leading_context_size:
                continue
            if index > len(self.parse_set_word_list)-following_context_size:
                continue

            if isinstance(word, UnparsableWordBinding):
                print u'Word is unparsable, skipped'
                continue

            leading_context_words = self.parse_set_word_list[index-leading_context_size : index]
            following_context_words = self.parse_set_word_list[index+1 : index+following_context_size+1]

            leading_context = None
            if len(leading_context_words)>0:
                leading_context = [self._create_mock_container(leading_context_word) for leading_context_word in leading_context_words]
                leading_context = [[leading_context_word] for leading_context_word in leading_context if leading_context_word]

            following_context = None
            if len(following_context_words)>0:
                following_context = [self._create_mock_container(following_context_word) for following_context_word in following_context_words]
                following_context = [[following_context_word] for following_context_word in following_context if following_context_word]

            if not leading_context and not following_context:
                print u'No context information found, skipped'
                continue

            surface = word.str
            likelihoods = self._generate_likelihood(surface=surface, leading_context=leading_context, following_context=following_context)

            for item in likelihoods:
                print u'\t' + str(item)

            most_probable_parse_result = max(likelihoods, key=itemgetter(1))
            most_probable_parse_results = filter(lambda t : t[1]==most_probable_parse_result[1], likelihoods)
            print u'Most probable parse results are {}'.format(most_probable_parse_results)
            print u'Correct parse result is {}'.format(word.parse_result)
            if word.parse_result in [t[0] for t in most_probable_parse_results]:
                print u'Correct result is found in statistical parse results'
            else:
            #                 self.fail(u'Correct result is NOT found in statistical parse results')
                print u'Correct result is NOT found in statistical parse results'

            print '\n'

    def _generate_likelihood(self, surface, leading_context=None, following_context=None):
        assert leading_context or following_context

        likelihoods = []
        results = self.contextless_parser.parse(surface)

        if not results:
            return None

        if len(results)==1:
            return [(formatter.format_morpheme_container_for_parseset(results[0]), 1.0)]

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

        return likelihoods

    def _create_mock_container(self, word):
        if isinstance(word, UnparsableWordBinding):
            print u'Previous word is unparsable, skipped : {}'.format(word.str)
            return None

        surface_str, surface_syntactic_category = word.str, word.syntactic_category
        stem_str, stem_syntactic_category, stem_secondary_syntactic_category = WordNGramGenerator._get_stem(word)
        lemma_root_str, lemma_root_syntactic_category = word.root.lemma_root, word.root.syntactic_category

        if word.secondary_syntactic_category:
            surface_syntactic_category += u'_' + word.secondary_syntactic_category
        if stem_secondary_syntactic_category:
            stem_syntactic_category += u'_' + stem_secondary_syntactic_category
        if word.root.secondary_syntactic_category:
            lemma_root_syntactic_category += u'_' + word.root.secondary_syntactic_category

        return MockMorphemeContainerBuilder.builder(word.format(), surface_str, surface_syntactic_category).stem(stem_str, stem_syntactic_category).lexeme(lemma_root_str, lemma_root_syntactic_category).build()

    @classmethod
    def create_calculator(cls, parseset_index):
        raise NotImplementedError()


class LikelihoodCalculatorTest(_BaseLikelihoodCalculatorTest):
    @classmethod
    def create_calculator(cls, parseset_index):
        mongodb_connection = pymongo.Connection(host='127.0.0.1')
        collection_map = {
            1: mongodb_connection['trnltk']['wordUnigrams{}'.format(parseset_index)],
            2: mongodb_connection['trnltk']['wordBigrams{}'.format(parseset_index)],
            3: mongodb_connection['trnltk']['wordTrigrams{}'.format(parseset_index)]
        }

        database_index_builder = DatabaseIndexBuilder(collection_map)
        target_form_given_context_counter = TargetFormGivenContextCounter(collection_map)
        ngram_frequency_smoother = CachedSimpleGoodTuringNGramFrequencySmoother()
        sequence_likelihood_calculator = UniformSequenceLikelihoodCalculator()

        generator = ContextParsingLikelihoodCalculator(database_index_builder, target_form_given_context_counter, ngram_frequency_smoother, sequence_likelihood_calculator)

        return generator

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
