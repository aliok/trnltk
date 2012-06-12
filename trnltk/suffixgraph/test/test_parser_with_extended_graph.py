# coding=utf-8
import logging
import os
import unittest
from hamcrest import *
from hamcrest.core.base_matcher import BaseMatcher
from trnltk.stem.dictionaryloader import DictionaryLoader
from trnltk.stem.stemgenerator import StemGenerator
from trnltk.suffixgraph.extendedsuffixgraph import ExtendedSuffixGraph
from trnltk.suffixgraph.parser import Parser, logger as parser_logger
from trnltk.suffixgraph.suffixapplier import logger as suffix_applier_logger
from trnltk.suffixgraph.predefinedpaths import PredefinedPaths

class ParserTestWithExtendedGraph(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(ParserTestWithExtendedGraph, cls).setUpClass()
        cls.all_stems = []

        dictionary_items = DictionaryLoader.load_from_file(os.path.join(os.path.dirname(__file__), '../../resources/master_dictionary.txt'))
        for di in dictionary_items:
            cls.all_stems.extend(StemGenerator.generate(di))

        predefined_paths = PredefinedPaths(cls.all_stems)
        predefined_paths.create_predefined_paths()

        cls.parser = Parser(cls.all_stems, ExtendedSuffixGraph(), predefined_paths)

    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        parser_logger.setLevel(logging.INFO)
        suffix_applier_logger.setLevel(logging.INFO)

    def test_should_parse_other_positions_to_verbs_zero_transition(self):
        parser_logger.setLevel(logging.DEBUG)
        suffix_applier_logger.setLevel(logging.DEBUG)

        #remove stem 'elmas' for tests!
        self.parser.stem_map.pop('elmas')


        self.assert_parse_correct_for_verb(u'elmayım',            u'elma(elma)+Noun+A3sg+Pnon+Nom+Verb+Zero+Pres+A1sg(+yIm[yım])')
        self.assert_parse_correct_for_verb(u'elmasın',            u'elma(elma)+Noun+A3sg+Pnon+Nom+Verb+Zero+Pres+A2sg(sIn[sın])')
        self.assert_parse_correct_for_verb(u'elma',               u'elma(elma)+Noun+A3sg+Pnon+Nom', u'elma(elma)+Noun+A3sg+Pnon+Nom+Verb+Zero+Pres+A3sg')
        self.assert_parse_correct_for_verb(u'elmayız',            u'elma(elma)+Noun+A3sg+Pnon+Nom+Verb+Zero+Pres+A1pl(+yIz[yız])')
        self.assert_parse_correct_for_verb(u'elmasınız',          u'elma(elma)+Noun+A3sg+Pnon+Nom+Verb+Zero+Pres+A2pl(sInIz[sınız])')
        self.assert_parse_correct_for_verb(u'elmalar',            u'elma(elma)+Noun+A3sg+Pnon+Nom+Verb+Zero+Pres+A3pl(lAr[lar])', u'elma(elma)+Noun+A3pl(lAr[lar])+Pnon+Nom', u'elma(elma)+Noun+A3pl(lAr[lar])+Pnon+Nom+Verb+Zero+Pres+A3sg')

        self.assert_parse_correct_for_verb(u'elmaymışım',         u'elma(elma)+Noun+A3sg+Pnon+Nom+Verb+Zero+Narr(ymIş[ymış])+A1sg(+yIm[ım])')
        self.assert_parse_correct_for_verb(u'elmaymışsın',        u'elma(elma)+Noun+A3sg+Pnon+Nom+Verb+Zero+Narr(ymIş[ymış])+A2sg(sIn[sın])')
        self.assert_parse_correct_for_verb(u'elmaymış',           u'elma(elma)+Noun+A3sg+Pnon+Nom+Verb+Zero+Narr(ymIş[ymış])+A3sg')
        self.assert_parse_correct_for_verb(u'elmaymışız',         u'elma(elma)+Noun+A3sg+Pnon+Nom+Verb+Zero+Narr(ymIş[ymış])+A1pl(+yIz[ız])')
        self.assert_parse_correct_for_verb(u'elmaymışsınız',      u'elma(elma)+Noun+A3sg+Pnon+Nom+Verb+Zero+Narr(ymIş[ymış])+A2pl(sInIz[sınız])')
        self.assert_parse_correct_for_verb(u'elmaymışlar',        u'elma(elma)+Noun+A3sg+Pnon+Nom+Verb+Zero+Narr(ymIş[ymış])+A3pl(lAr[lar])')

        self.assert_parse_correct_for_verb(u'elmaydım',           u'elma(elma)+Noun+A3sg+Pnon+Nom+Verb+Zero+Past(ydI[ydı])+A1sg(m[m])')
        self.assert_parse_correct_for_verb(u'elmaydın',           u'elma(elma)+Noun+A3sg+Pnon+Nom+Verb+Zero+Past(ydI[ydı])+A2sg(n[n])')
        self.assert_parse_correct_for_verb(u'elmaydı',            u'elma(elma)+Noun+A3sg+Pnon+Nom+Verb+Zero+Past(ydI[ydı])+A3sg')
        self.assert_parse_correct_for_verb(u'elmaydık',           u'elma(elma)+Noun+A3sg+Pnon+Nom+Verb+Zero+Past(ydI[ydı])+A1pl(k[k])')
        self.assert_parse_correct_for_verb(u'elmaydınız',         u'elma(elma)+Noun+A3sg+Pnon+Nom+Verb+Zero+Past(ydI[ydı])+A2pl(nIz[nız])')
        self.assert_parse_correct_for_verb(u'elmaydılar',         u'elma(elma)+Noun+A3sg+Pnon+Nom+Verb+Zero+Past(ydI[ydı])+A3pl(lAr[lar])')

        self.assert_parse_correct_for_verb(u'elmaysam',           u'elma(elma)+Noun+A3sg+Pnon+Nom+Verb+Zero+Cond(+ysA[ysa])+A1sg(m[m])')
        self.assert_parse_correct_for_verb(u'elmaysan',           u'elma(elma)+Noun+A3sg+Pnon+Nom+Verb+Zero+Cond(+ysA[ysa])+A2sg(n[n])')
        self.assert_parse_correct_for_verb(u'elmaysa',            u'elma(elma)+Noun+A3sg+Pnon+Nom+Verb+Zero+Cond(+ysA[ysa])+A3sg')
        self.assert_parse_correct_for_verb(u'elmaysak',           u'elma(elma)+Noun+A3sg+Pnon+Nom+Verb+Zero+Cond(+ysA[ysa])+A1pl(k[k])')
        self.assert_parse_correct_for_verb(u'elmaysanız',         u'elma(elma)+Noun+A3sg+Pnon+Nom+Verb+Zero+Cond(+ysA[ysa])+A2pl(nIz[nız])')
        self.assert_parse_correct_for_verb(u'elmaysalar',         u'elma(elma)+Noun+A3sg+Pnon+Nom+Verb+Zero+Cond(+ysA[ysa])+A3pl(lAr[lar])')

        self.assert_parse_correct_for_verb(u'elmansam',           u'x')
        self.assert_parse_correct_for_verb(u'elmamsa',            u'x')
        self.assert_parse_correct_for_verb(u'elmamdın',           u'x')
        self.assert_parse_correct_for_verb(u'elmanızdık',         u'x')
        self.assert_parse_correct_for_verb(u'elmamızmışsınız',    u'x')
        self.assert_parse_correct_for_verb(u'elmalarınızsalar',   u'x')

        self.assert_parse_correct_for_verb(u'iyiyim',             u'x')
        self.assert_parse_correct_for_verb(u'küçüğümüzdeyseler',  u'x')
        self.assert_parse_correct_for_verb(u'küçüklerimizindiler',u'x')
        self.assert_parse_correct_for_verb(u'bendim',             u'x')
        self.assert_parse_correct_for_verb(u'benim',             u'x')
        self.assert_parse_correct_for_verb(u'sensin',             u'x')
        self.assert_parse_correct_for_verb(u'oydu',               u'x')
        self.assert_parse_correct_for_verb(u'hızlıcaymışlar',     u'x')

    def assert_parse_correct_for_verb(self, word_to_parse, *args):
        assert_that(self.parse_result(word_to_parse), IsParseResultMatches([a for a in args]))

    def assert_parse_correct(self, word_to_parse, *args):
        assert_that(self.parse_result(word_to_parse), IsParseResultMatchesIgnoreVerbPresA3Sg([a for a in args]))

    def parse_result(self, word):
        return [r.to_pretty_str() for r in (self.parser.parse(word))]

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
