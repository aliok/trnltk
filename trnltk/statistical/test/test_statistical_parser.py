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
import os
import unittest
from xml.dom.minidom import parse
from trnltk.morphology.morphotactics.basicsuffixgraph import BasicSuffixGraph
from trnltk.morphology.morphotactics.numeralsuffixgraph import NumeralSuffixGraph
from trnltk.parseset.xmlbindings import ParseSetBinding
from trnltk.statistical.parser import StatisticalParser
from trnltk.morphology.lexicon.lexiconloader import LexiconLoader
from trnltk.morphology.lexicon.rootgenerator import RootGenerator, RootMapGenerator
from trnltk.morphology.morphotactics.copulasuffixgraph import CopulaSuffixGraph
from trnltk.morphology.contextless.parser.parser import ContextlessMorphologicalParser
from trnltk.morphology.contextless.parser.rootfinder import WordRootFinder, DigitNumeralRootFinder, ProperNounFromApostropheRootFinder, ProperNounWithoutApostropheRootFinder, TextNumeralRootFinder
from trnltk.morphology.morphotactics.predefinedpaths import PredefinedPaths
from trnltk.treebank.explorer import CompleteWordConcordanceIndex

class StatisticalParserTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(StatisticalParserTest, cls).setUpClass()
        all_roots = []

        lexemes = LexiconLoader.load_from_file(os.path.join(os.path.dirname(__file__), '../../resources/master_dictionary.txt'))
        for di in lexemes:
            all_roots.extend(RootGenerator.generate(di))


        root_map_generator = RootMapGenerator()
        cls.root_map = root_map_generator.generate(all_roots)

        suffix_graph = CopulaSuffixGraph(NumeralSuffixGraph(BasicSuffixGraph()))
        suffix_graph.initialize()

        predefined_paths = PredefinedPaths(cls.root_map, suffix_graph)
        predefined_paths.create_predefined_paths()

        word_root_finder = WordRootFinder(cls.root_map)
        digit_numeral_root_finder = DigitNumeralRootFinder()
        text_numeral_root_finder = TextNumeralRootFinder(cls.root_map)
        proper_noun_from_apostrophe_root_finder = ProperNounFromApostropheRootFinder()
        proper_noun_without_apostrophe_root_finder = ProperNounWithoutApostropheRootFinder()

        contextless_parser = ContextlessMorphologicalParser(suffix_graph, predefined_paths,
            [word_root_finder, digit_numeral_root_finder, text_numeral_root_finder, proper_noun_from_apostrophe_root_finder, proper_noun_without_apostrophe_root_finder])

        parseset_index = "001"
        dom = parse(os.path.join(os.path.dirname(__file__), '../../testresources/parsesets/parseset{}.xml'.format(parseset_index)))
        parseset = ParseSetBinding.build(dom.getElementsByTagName("parseset")[0])
        parse_set_word_list = []
        for sentence in parseset.sentences:
            parse_set_word_list.extend(sentence.words)

        complete_word_concordance_index = CompleteWordConcordanceIndex(parse_set_word_list)

        cls.parser = StatisticalParser(contextless_parser, complete_word_concordance_index)

    def test_should_parse(self):
        result = self.parser.parse(u'verirsiniz')
        print result.get_parse_results_with_ratio()


if __name__ == '__main__':
    unittest.main()
