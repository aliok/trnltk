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
import logging
import unittest
from hamcrest import *
from trnltk.morphology.lexicon.lexiconloader import LexiconLoader
from trnltk.morphology.lexicon.rootgenerator import RootGenerator, RootMapGenerator
from trnltk.morphology.contextless.parser.parser import ContextlessMorphologicalParser, logger as parser_logger
from trnltk.morphology.contextless.parser.rootfinder import  WordRootFinder
from trnltk.morphology.contextless.parser.suffixapplier import logger as suffix_applier_logger
from trnltk.morphology.model import formatter
from trnltk.morphology.morphotactics.basicsuffixgraph import BasicSuffixGraph

class FormatterTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(FormatterTest, cls).setUpClass()
        all_roots = []

        dictionary_content = ["kitap", "yapmak"]
        lexemes = LexiconLoader.load_from_lines(dictionary_content)
        for di in lexemes:
            all_roots.extend(RootGenerator.generate(di))

        cls.root_map = RootMapGenerator().generate(all_roots)


    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        parser_logger.setLevel(logging.INFO)
        suffix_applier_logger.setLevel(logging.INFO)

        suffix_graph = BasicSuffixGraph()
        suffix_graph.initialize()

        word_root_finder = WordRootFinder(self.root_map)

        self.parser = ContextlessMorphologicalParser(suffix_graph, None, [word_root_finder])

    def test_should_format_for_simple_parseset(self):
        parse_result = self.parser.parse(u'kitaba')[0]
        assert_that(formatter.format_morpheme_container_for_simple_parseset(parse_result), equal_to(u'(1,"kitap+Noun+A3sg+Pnon+Dat")'))

        parse_result = self.parser.parse(u'yaptırtmayı')[0]
        assert_that(formatter.format_morpheme_container_for_simple_parseset(parse_result), equal_to(u'(1,"yap+Verb")(2,"Verb+Caus")(3,"Verb+Caus+Pos")(4,"Noun+Inf+A3sg+Pnon+Acc")'))

    def test_should_format_for_tests(self):
        parse_result = self.parser.parse(u'kitaba')[0]
        assert_that(formatter.format_morpheme_container_for_tests(parse_result), equal_to(u'kitab(kitap)+Noun+A3sg+Pnon+Dat(+yA[a])'))

        parse_result = self.parser.parse(u'yaptırtmayı')[0]
        assert_that(formatter.format_morpheme_container_for_tests(parse_result), equal_to(u'yap(yapmak)+Verb+Verb+Caus(dIr[tır])+Verb+Caus(t[t])+Pos+Noun+Inf(mA[ma])+A3sg+Pnon+Acc(+yI[yı])'))

    def test_should_format_for_parseset(self):
        parse_result = self.parser.parse(u'kitaba')[0]
        assert_that(formatter.format_morpheme_container_for_parseset(parse_result), equal_to(u'kitap+Noun+A3sg+Pnon+Dat'))

        parse_result = self.parser.parse(u'yaptırtmayı')[0]
        assert_that(formatter.format_morpheme_container_for_parseset(parse_result), equal_to(u'yap+Verb+Verb+Caus+Verb+Caus+Pos+Noun+Inf+A3sg+Pnon+Acc'))

if __name__ == '__main__':
    unittest.main()
