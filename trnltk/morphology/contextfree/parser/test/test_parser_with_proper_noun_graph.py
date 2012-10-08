# coding=utf-8
import logging
import os
import unittest
from hamcrest import *
from hamcrest.core.base_matcher import BaseMatcher
from trnltk.morphology.contextfree.parser.test.parser_test import ParserTest
from trnltk.morphology.lexicon.lexiconloader import LexiconLoader
from trnltk.morphology.lexicon.rootgenerator import RootGenerator, RootMapGenerator
from trnltk.morphology.model import formatter
from trnltk.morphology.morphotactics.basicsuffixgraph import BasicSuffixGraph
from trnltk.morphology.morphotactics.copulasuffixgraph import CopulaSuffixGraph
from trnltk.morphology.contextfree.parser.parser import ContextFreeMorphologicalParser, logger as parser_logger
from trnltk.morphology.contextfree.parser.rootfinder import WordRootFinder, DigitNumeralRootFinder, ProperNounFromApostropheRootFinder, ProperNounWithoutApostropheRootFinder
from trnltk.morphology.contextfree.parser.suffixapplier import logger as suffix_applier_logger
from trnltk.morphology.morphotactics.predefinedpaths import PredefinedPaths
from trnltk.morphology.morphotactics.suffixgraph import EmptySuffixGraph

class ParserTestWithProperNouns(ParserTest):

    @classmethod
    def setUpClass(cls):
        super(ParserTestWithProperNouns, cls).setUpClass()
        all_roots = []

        lexemes = LexiconLoader.load_from_file(os.path.join(os.path.dirname(__file__), '../../../../resources/master_dictionary.txt'))
        for di in lexemes:
            all_roots.extend(RootGenerator.generate(di))


        root_map_generator = RootMapGenerator()
        cls.root_map = root_map_generator.generate(all_roots)

        suffix_graph = CopulaSuffixGraph(BasicSuffixGraph())
        suffix_graph.initialize()

        predefined_paths = PredefinedPaths(cls.root_map, suffix_graph)
        predefined_paths.create_predefined_paths()

        word_root_finder = WordRootFinder(cls.root_map)
        numeral_root_finder = DigitNumeralRootFinder()
        proper_noun_from_apostrophe_root_finder = ProperNounFromApostropheRootFinder()
        proper_noun_without_apostrophe_root_finder = ProperNounWithoutApostropheRootFinder()

        cls.parser = ContextFreeMorphologicalParser(suffix_graph, predefined_paths,
            [word_root_finder, numeral_root_finder, proper_noun_from_apostrophe_root_finder, proper_noun_without_apostrophe_root_finder])

    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        parser_logger.setLevel(logging.INFO)
        suffix_applier_logger.setLevel(logging.INFO)

    def test_should_parse_proper_nouns(self):
        parser_logger.setLevel(logging.DEBUG)
        suffix_applier_logger.setLevel(logging.DEBUG)

        self.assert_parse_correct(u"Ali",            u"Ali(Ali)+Noun+Prop+A3sg+Pnon+Nom")
        self.assert_parse_correct(u"ABD",            u"ABD(ABD)+Noun+Prop+A3sg+Pnon+Nom")
        self.assert_parse_correct(u"Ahmet",          u"Ahmet(Ahmet)+Noun+Prop+A3sg+Pnon+Nom")
        self.assert_parse_correct(u"Ali'ye",         u"Ali(Ali)+Noun+Prop+A3sg+Pnon+Acc")       ## TODO: not supported yet.

    def test_should_parse_abbreviations(self):
        parser_logger.setLevel(logging.DEBUG)
        suffix_applier_logger.setLevel(logging.DEBUG)

        self.assert_parse_correct(u"AB",            u"AB(AB)+Noun+Abbr+A3sg+Pnon+Nom")
        self.assert_parse_correct(u"AB'ye",         u"AB(AB)+Noun+Abbr+A3sg+Pnon+Acc")       ## TODO: not supported yet!


if __name__ == '__main__':
    unittest.main()
