# coding=utf-8
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

class ContextlessDistributionCalculatorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(ContextlessDistributionCalculatorTest, cls).setUpClass()
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
            1: mongodb_connection['trnltk']['wordUnigrams999']
        }

        database_index_builder = DatabaseIndexBuilder(collection_map)
        target_form_given_context_counter = TargetFormGivenContextCounter(collection_map)

        cls.calculator = ContextlessDistributionCalculator(database_index_builder, target_form_given_context_counter)
        cls.calculator.build_indexes()

    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        query_logger.setLevel(logging.INFO)

    def _test_calculate(self, surface, shouldnt_have_ambiguity=False, expected_likelihood_sum=1.0, expected_likelihood_for_one=None):
        results = self.contextless_parser.parse(surface)

        likelihoods = []

        for result in results:
            formatted_parse_result = formatter.format_morpheme_container_for_parseset(result)
            formatted_parse_result_likelihood = self.calculator.calculate(result)
            likelihoods.append((formatted_parse_result, formatted_parse_result_likelihood))

        pprint.pprint(likelihoods)

        likelihood_sum = sum([t[1] for t in likelihoods])
        assert likelihood_sum == 1 or likelihood_sum == 0
        if not likelihood_sum:
            print "likelihood_sum is 0!"

        if expected_likelihood_sum is not None:
            assert expected_likelihood_sum == likelihood_sum

        non_zero_likelihoods = filter(lambda t: t[1] != 0, likelihoods)

        if shouldnt_have_ambiguity and likelihood_sum != 0:
            assert len(non_zero_likelihoods) == 1

        if expected_likelihood_for_one is not None:
            all([non_zero_likelihood == expected_likelihood_for_one for non_zero_likelihood in non_zero_likelihoods])

        print '\n'

    def test_calculate_without_ambiguity(self):
        self._test_calculate(u'masa', True)
        self._test_calculate(u'kitap', True)
        self._test_calculate(u'deri', True)

    def test_calculate_with_ambiguity(self):
        self._test_calculate(u'onun')
        self._test_calculate(u'erkek')
        self._test_calculate(u'bir')

    def test_calculate_with_unparsable(self):
        self._test_calculate(u'asdasd', expected_likelihood_sum=0.0)

    def test_calculate_with_non_existing(self):
        self._test_calculate(u'gelircesine', expected_likelihood_sum=0.0)


if __name__ == '__main__':
    unittest.main()
