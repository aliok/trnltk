# coding=utf-8
import codecs
import os
import unittest
from trnltk.morphology.contextfree.parser.parser import ContextFreeMorphologicalParser
from trnltk.morphology.model import formatter
from trnltk.morphology.morphotactics.copulasuffixgraph import CopulaSuffixGraph
from trnltk.morphology.morphotactics.numeralsuffixgraph import NumeralSuffixGraph
from trnltk.parseset import xmlbindings
from trnltk.parseset.creator import ParseSetCreator
from trnltk.morphology.contextfree.parser.rootfinder import DigitNumeralRootFinder, WordRootFinder, ProperNounFromApostropheRootFinder, ProperNounWithoutApostropheRootFinder, TextNumeralRootFinder
from trnltk.parseset.xmlbindings import ParseSetBinding
from trnltk.morphology.lexicon.lexiconloader import LexiconLoader
from trnltk.morphology.lexicon.rootgenerator import RootGenerator, RootMapGenerator
from trnltk.morphology.morphotactics.predefinedpaths import PredefinedPaths
from trnltk.morphology.morphotactics.basicsuffixgraph import BasicSuffixGraph

END_OF_SENTENCE_MARKER = '#END#OF#SENTENCE#'

class ParseSetCreatorWithSimpleParsesetsTest(unittest.TestCase):

    def setUp(self):
        self.parseset_creator = ParseSetCreator()

        all_roots = []

        lexemes = LexiconLoader.load_from_file(os.path.join(os.path.dirname(__file__), '../../resources/master_dictionary.txt'))
        for di in lexemes:
            all_roots.extend(RootGenerator.generate(di))

        root_map = (RootMapGenerator()).generate(all_roots)

        suffix_graph = CopulaSuffixGraph(NumeralSuffixGraph(BasicSuffixGraph()))
        suffix_graph.initialize()

        predefined_paths = PredefinedPaths(root_map, suffix_graph)
        predefined_paths.create_predefined_paths()

        word_root_finder = WordRootFinder(root_map)
        digit_numeral_root_finder = DigitNumeralRootFinder()
        text_numeral_root_finder = TextNumeralRootFinder(root_map)
        proper_noun_from_apostrophe_root_finder = ProperNounFromApostropheRootFinder()
        proper_noun_without_apostrophe_root_finder = ProperNounWithoutApostropheRootFinder()

        self.parser = ContextFreeMorphologicalParser(suffix_graph, predefined_paths,
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

#    def test_should_create_parseset_999(self):
#        self._create_parseset_n("999")

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
            output.write('<?xml version="1.0"?>\n')
            output.write(parseset_dom.toprettyxml())


    def _find_parse_result_matching_simple_parseset(self, word_part, parse_result_part):
        parse_results = self.parser.parse(word_part)
        for parse_result in parse_results:
            if parse_result_part== formatter.format_morpheme_container_for_simple_parseset(parse_result):
                return parse_result

        return None

if __name__ == '__main__':
    unittest.main()
