# coding=utf-8
import logging
import os
import unittest
from hamcrest import *
from hamcrest.core.base_matcher import BaseMatcher
from trnltk.morphology.contextfree.parser import formatter
from trnltk.morphology.lexiconmodel.lexiconloader import LexiconLoader
from trnltk.morphology.lexiconmodel.rootgenerator import RootGenerator, RootMapGenerator
from trnltk.morphology.morphotactics.extendedsuffixgraph import ExtendedSuffixGraph
from trnltk.morphology.contextfree.parser.parser import ContextFreeMorphologicalParser, logger as parser_logger
from trnltk.morphology.contextfree.parser.lexemefinder import WordLexemeFinder, NumeralLexemeFinder, ProperNounFromApostropheLexemeFinder, ProperNounWithoutApostropheLexemeFinder
from trnltk.morphology.contextfree.parser.suffixapplier import logger as suffix_applier_logger
from trnltk.morphology.morphotactics.predefinedpaths import PredefinedPaths

class ParserTestWithProperNouns(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(ParserTestWithProperNouns, cls).setUpClass()
        all_stems = []

        dictionary_items = LexiconLoader.load_from_file(os.path.join(os.path.dirname(__file__), '../../resources/master_dictionary.txt'))
        for di in dictionary_items:
            all_stems.extend(RootGenerator.generate(di))


        stem_root_map_generator = RootMapGenerator()
        cls.stem_root_map = stem_root_map_generator.generate(all_stems)

        suffix_graph = ExtendedSuffixGraph()
        predefined_paths = PredefinedPaths(cls.stem_root_map, suffix_graph)
        predefined_paths.create_predefined_paths()

        word_stem_finder = WordLexemeFinder(cls.stem_root_map)
        numeral_stem_finder = NumeralLexemeFinder()
        proper_noun_from_apostrophe_stem_finder = ProperNounFromApostropheLexemeFinder()
        proper_noun_without_apostrophe_stem_finder = ProperNounWithoutApostropheLexemeFinder()

        cls.parser = ContextFreeMorphologicalParser(suffix_graph, predefined_paths,
            [word_stem_finder, numeral_stem_finder, proper_noun_from_apostrophe_stem_finder, proper_noun_without_apostrophe_stem_finder])

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

        self.assert_parse_correct(u"AB",            u"AB(AB)+Noun+Prop+A3sg+Pnon+Nom")
        self.assert_parse_correct(u"AB'ye",            u"AB(AB)+Noun+Prop+A3sg+Pnon+Acc")       ## TODO: not supported yet!

    def assert_parse_correct_for_verb(self, word_to_parse, *args):
        assert_that(self.parse_result(word_to_parse), IsParseResultMatches([a for a in args]))

    def assert_parse_correct(self, word_to_parse, *args):
        assert_that(self.parse_result(word_to_parse), IsParseResultMatchesIgnoreVerbPresA3Sg([a for a in args]))

    def parse_result(self, word):
        return [formatter.format_parse_token_for_tests(r) for r in (self.parser.parse(word))]

class IsParseResultMatches(BaseMatcher):
    def __init__(self, expected_results):
        self.expected_results = expected_results

    def _matches(self, items):
        return all(er in items for er in self.expected_results) and all(item in self.expected_results for item in items)

    def describe_to(self, description):
        description.append_text(u'     ' + str(self.expected_results))

class IsParseResultMatchesIgnoreVerbPresA3Sg(BaseMatcher):
    def __init__(self, expected_results):
        self.expected_results = expected_results

    def _matches(self, items):
        items = filter(lambda item : u'+Zero+Pres+' not in item, items)
        return all(er in items for er in self.expected_results) and all(item in self.expected_results for item in items)

    def describe_to(self, description):
        description.append_text(u'     ' + str(self.expected_results))

if __name__ == '__main__':
    unittest.main()
