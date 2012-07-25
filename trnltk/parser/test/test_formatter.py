# coding=utf-8
import logging
import unittest
from hamcrest import *
from trnltk.parser import formatter
from trnltk.stem.dictionaryloader import DictionaryLoader
from trnltk.stem.stemgenerator import StemGenerator, StemRootMapGenerator
from trnltk.parser.parser import Parser, logger as parser_logger
from trnltk.parser.stemfinder import  WordStemFinder
from trnltk.parser.suffixapplier import logger as suffix_applier_logger
from trnltk.suffixgraph.suffixgraph import SuffixGraph

class FormatterTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(FormatterTest, cls).setUpClass()
        all_stems = []

        dictionary_content = ["kitap", "yapmak"]
        dictionary_items = DictionaryLoader.load_from_lines(dictionary_content)
        for di in dictionary_items:
            all_stems.extend(StemGenerator.generate(di))

        cls.stem_root_map = (StemRootMapGenerator()).generate(all_stems)


    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        parser_logger.setLevel(logging.INFO)
        suffix_applier_logger.setLevel(logging.INFO)

        suffix_graph = SuffixGraph()

        word_stem_finder = WordStemFinder(self.stem_root_map)

        self.parser = Parser(suffix_graph, None, [word_stem_finder])

    def test_should_format_for_simple_parseset(self):
        parse_result = self.parser.parse(u'kitaba')[0]
        assert_that(formatter.format_parse_token_for_simple_parseset(parse_result), equal_to(u'(1,"kitap+Noun+A3sg+Pnon+Dat")'))

        parse_result = self.parser.parse(u'yaptırtmayı')[0]
        assert_that(formatter.format_parse_token_for_simple_parseset(parse_result), equal_to(u'(1,"yap+Verb")(2,"Verb+Caus")(3,"Verb+Caus+Pos")(4,"Noun+Inf+A3sg+Pnon+Acc")'))

    def test_should_format_for_tests(self):
        parse_result = self.parser.parse(u'kitaba')[0]
        assert_that(formatter.format_parse_token_for_tests(parse_result), equal_to(u'kitab(kitap)+Noun+A3sg+Pnon+Dat(+yA[a])'))

        parse_result = self.parser.parse(u'yaptırtmayı')[0]
        assert_that(formatter.format_parse_token_for_tests(parse_result), equal_to(u'yap(yapmak)+Verb+Verb+Caus(dIr[tır])+Verb+Caus(t[t])+Pos+Noun+Inf(mA[ma])+A3sg+Pnon+Acc(+yI[yı])'))

    def test_should_format_for_parseset(self):
        parse_result = self.parser.parse(u'kitaba')[0]
        assert_that(formatter.format_parse_token_for_parseset(parse_result), equal_to(u'kitap+Noun+A3sg+Pnon+Dat'))

        parse_result = self.parser.parse(u'yaptırtmayı')[0]
        assert_that(formatter.format_parse_token_for_parseset(parse_result), equal_to(u'yap+Verb+Verb+Caus+Verb+Caus+Pos+Noun+Inf+A3sg+Pnon+Acc'))

if __name__ == '__main__':
    unittest.main()
