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
import codecs
import os
import unittest
from trnltk.morphology.contextless.parser.parser import  UpperCaseSupportingContextlessMorphologicalParser
from trnltk.morphology.model import formatter
from trnltk.morphology.morphotactics.copulasuffixgraph import CopulaSuffixGraph
from trnltk.morphology.morphotactics.numeralsuffixgraph import NumeralSuffixGraph
from trnltk.morphology.morphotactics.propernounsuffixgraph import ProperNounSuffixGraph
from trnltk.parseset import xmlbindings
from trnltk.parseset.creator import ParseSetCreator
from trnltk.morphology.contextless.parser.rootfinder import DigitNumeralRootFinder, WordRootFinder, ProperNounFromApostropheRootFinder, ProperNounWithoutApostropheRootFinder, TextNumeralRootFinder
from trnltk.parseset.xmlbindings import ParseSetBinding
from trnltk.morphology.lexicon.lexiconloader import LexiconLoader
from trnltk.morphology.lexicon.rootgenerator import RootGenerator, RootMapGenerator
from trnltk.morphology.morphotactics.predefinedpaths import PredefinedPaths
from trnltk.morphology.morphotactics.basicsuffixgraph import BasicSuffixGraph

END_OF_SENTENCE_MARKER = '#END#OF#SENTENCE#'
PARSESET_HEADER = """
<!--
<?xml version="1.0"?>
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
-->
""".strip()

def modify_treebank_parse_result_strs_to_look_like_trnltk(parse_result_str):
    #TODO
    parse_result_str = parse_result_str.replace('Prog1', 'Prog')
    parse_result_str = parse_result_str.replace('Prog2', 'Prog')
    parse_result_str = parse_result_str.replace('Inf1', 'Inf')
    parse_result_str = parse_result_str.replace('Inf2', 'Inf')
    parse_result_str = parse_result_str.replace('Inf3', 'Inf')
    parse_result_str = parse_result_str.replace('WithoutHavingDoneSo1', 'WithoutHavingDoneSo')
    parse_result_str = parse_result_str.replace('WithoutHavingDoneSo2', 'WithoutHavingDoneSo')


    #TODO
    parse_result_str = parse_result_str.replace('Hastily', 'Hastily+Pos')

    parse_result_str = parse_result_str.replace('Postp+PCNom', 'Part')
    parse_result_str = parse_result_str.replace('Postp+PCDat', 'Postp')
    parse_result_str = parse_result_str.replace('Postp+PCAcc', 'Postp')
    parse_result_str = parse_result_str.replace('Postp+PCLoc', 'Postp')
    parse_result_str = parse_result_str.replace('Postp+PCAbl', 'Postp')
    parse_result_str = parse_result_str.replace('Postp+PCIns', 'Postp')
    parse_result_str = parse_result_str.replace('Postp+PCGen', 'Postp')

    return parse_result_str

class ParseSetCreatorWithSimpleParsesetsTest(unittest.TestCase):

    def setUp(self):
        self.parseset_creator = ParseSetCreator()

        all_roots = []

        lexemes = LexiconLoader.load_from_file(os.path.join(os.path.dirname(__file__), '../../resources/master_dictionary.txt'))
        for di in lexemes:
            all_roots.extend(RootGenerator.generate(di))

        root_map = (RootMapGenerator()).generate(all_roots)

        suffix_graph = CopulaSuffixGraph(NumeralSuffixGraph(ProperNounSuffixGraph(BasicSuffixGraph())))
        suffix_graph.initialize()

        predefined_paths = PredefinedPaths(root_map, suffix_graph)
        predefined_paths.create_predefined_paths()

        word_root_finder = WordRootFinder(root_map)
        digit_numeral_root_finder = DigitNumeralRootFinder()
        text_numeral_root_finder = TextNumeralRootFinder(root_map)
        proper_noun_from_apostrophe_root_finder = ProperNounFromApostropheRootFinder()
        proper_noun_without_apostrophe_root_finder = ProperNounWithoutApostropheRootFinder()

        self.parser = UpperCaseSupportingContextlessMorphologicalParser(suffix_graph, predefined_paths,
            [word_root_finder, digit_numeral_root_finder, text_numeral_root_finder, proper_noun_from_apostrophe_root_finder, proper_noun_without_apostrophe_root_finder])

    def test_should_create_parseset_001(self):
        self._create_parseset_n("001")

    def test_should_create_parseset_002(self):
        self._create_parseset_n("002")

    def test_should_create_parseset_003(self):
        self._create_parseset_n("003")

    def test_should_create_parseset_004(self):
        self._create_parseset_n("004")

    def test_should_create_parseset_005(self):
        self._create_parseset_n("005")

    def test_should_create_parseset_999(self):
        self._create_parseset_n("999")

    def _create_parseset_n(self, set_number):
        source_file_path = os.path.join(os.path.dirname(__file__), '../../testresources/simpleparsesets/simpleparseset{}.txt'.format(set_number))
        destination_file_path = os.path.join(os.path.dirname(__file__), '../../testresources/parsesets/parseset{}.xml'.format(set_number))

        line_index = 0
        sentences = []
        with codecs.open(source_file_path, mode='r', encoding='utf-8') as src:
            entries_for_sentence = []
            for line in src:
                print u'Processing line {}'.format(line_index)
                line_index +=1
                if not line:
                    continue
                elif line.startswith(END_OF_SENTENCE_MARKER):
                    sentence_binding = self.parseset_creator.create_sentence_binding_from_morpheme_containers(entries_for_sentence)
                    sentences.append(sentence_binding)
                    entries_for_sentence = []
                elif line.startswith("#"):
                    continue
                else:
                    word_part = line[:line.find('=')].strip()
                    parse_result_part = line[line.find('=')+1:].strip()

                    parse_result_matching_simple_parseset = self._find_parse_result_matching_simple_parseset(word_part, parse_result_part)

                    entries_for_sentence.append((word_part, parse_result_matching_simple_parseset))

        parseset_binding = ParseSetBinding()
        parseset_binding.sentences = sentences
        parseset_dom = parseset_binding.to_dom()
        parseset_dom.setAttribute("xmlns", xmlbindings.NAMESPACE)
        with codecs.open(destination_file_path, mode='w', encoding='utf-8') as output:
            output.write(PARSESET_HEADER)
            output.write('\n')
            output.write(parseset_dom.toprettyxml())


    def _find_parse_result_matching_simple_parseset(self, word_part, parse_result_part):
        parse_results = self.parser.parse(word_part)

        for parse_result in parse_results:
            parse_result_str = formatter.format_morpheme_container_for_simple_parseset(parse_result)
            if parse_result_part==parse_result_str:
                return parse_result
            elif parse_result_str==modify_treebank_parse_result_strs_to_look_like_trnltk(parse_result_part):
                return parse_result

        return None

if __name__ == '__main__':
    unittest.main()
