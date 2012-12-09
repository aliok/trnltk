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
from trnltk.morphology.contextful.likelihoodmetrics.contextlessdistribution.contextlessdistributionsmoother import SimpleGoodTuringContextlessDistributionSmoother, CachedContextlessDistributionSmoother

"""
There is no verification -yet- in test of this class.
The tests are there for making sure there is no run time exceptions
"""
import logging
import os
import pprint
import unittest
import pymongo
from trnltk.morphology.contextful.likelihoodmetrics.contextlessdistribution.contextlessdistributioncalculator import ContextlessDistributionCalculator
from trnltk.morphology.contextful.likelihoodmetrics.hidden.database import DatabaseIndexBuilder
from trnltk.morphology.contextful.likelihoodmetrics.hidden.targetformgivencontextcounter import TargetFormGivenContextCounter
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
from trnltk.morphology.contextful.likelihoodmetrics.wordformcollocation.contextparsingcalculator import query_logger

class BaseContextlessDistributionCalculatorTest(object):
    @classmethod
    def setUpClass(cls):
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

        mongodb_connection = pymongo.Connection(host='127.0.0.1')
        collection_map = {
            1: mongodb_connection['trnltk']['wordUnigrams{}'.format(cls.parseset_index)]
        }

        database_index_builder = DatabaseIndexBuilder(collection_map)
        target_form_given_context_counter = TargetFormGivenContextCounter(collection_map)
        smoother = CachedContextlessDistributionSmoother()
        smoother.initialize()

        cls.calculator = ContextlessDistributionCalculator(database_index_builder, target_form_given_context_counter, smoother)
        cls.calculator.build_indexes()

    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        query_logger.setLevel(logging.INFO)

    def _test_calculate(self, surface):
        results = self.contextless_parser.parse(surface)

        likelihoods = []

        for result in results:
            formatted_parse_result = formatter.format_morpheme_container_for_parseset(result)
            formatted_parse_result_likelihood = self.calculator.calculate(result)
            likelihoods.append((formatted_parse_result, formatted_parse_result_likelihood))

        pprint.pprint(likelihoods)

    def test_calculate_without_ambiguity(self):
        self._test_calculate(u'masa')
        self._test_calculate(u'kitap')
        self._test_calculate(u'deri')

    def test_calculate_with_ambiguity(self):
        self._test_calculate(u'onun')
        self._test_calculate(u'erkek')
        self._test_calculate(u'bir')

    def test_calculate_with_unparsable(self):
        self._test_calculate(u'asdasd')

    def test_calculate_with_non_existing(self):
        self._test_calculate(u'gelircesine')

class ContextlessDistributionCalculatorTestForParseSet001(unittest.TestCase, BaseContextlessDistributionCalculatorTest):
    @classmethod
    def setUpClass(cls):
        BaseContextlessDistributionCalculatorTest.parseset_index = "001"
        BaseContextlessDistributionCalculatorTest.setUpClass()

    def test_calculate_with_unparsable(self):
        super(ContextlessDistributionCalculatorTestForParseSet001, self).test_calculate_with_unparsable()

    def test_calculate_with_ambiguity(self):
        super(ContextlessDistributionCalculatorTestForParseSet001, self).test_calculate_with_ambiguity()

    def test_calculate_without_ambiguity(self):
        super(ContextlessDistributionCalculatorTestForParseSet001, self).test_calculate_without_ambiguity()

    def test_calculate_with_non_existing(self):
        super(ContextlessDistributionCalculatorTestForParseSet001, self).test_calculate_with_non_existing()


class ContextlessDistributionCalculatorTestForParseSet999(unittest.TestCase, BaseContextlessDistributionCalculatorTest):
    @classmethod
    def setUpClass(cls):
        BaseContextlessDistributionCalculatorTest.parseset_index = "999"
        BaseContextlessDistributionCalculatorTest.setUpClass()


if __name__ == '__main__':
    unittest.main()
