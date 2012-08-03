# coding=utf-8
import codecs
import os
import unittest
from trnltk.morphology.contextfree.parser import formatter
from trnltk.morphology.contextfree.parser.parser import ContextFreeMorphologicalParser
from trnltk.parseset import xmlbindings
from trnltk.parseset.creator import ParseSetCreator
from trnltk.morphology.contextfree.parser.lexemefinder import NumeralLexemeFinder, WordLexemeFinder, ProperNounFromApostropheLexemeFinder, ProperNounWithoutApostropheLexemeFinder
from trnltk.parseset.xmlbindings import ParseSetBinding
from trnltk.morphology.model.lexiconloader import LexiconLoader
from trnltk.morphology.model.rootgenerator import RootGenerator, RootMapGenerator
from trnltk.morphology.suffixgraph.predefinedpaths import PredefinedPaths
from trnltk.morphology.suffixgraph.suffixgraph import SuffixGraph

END_OF_SENTENCE_MARKER = '#END#OF#SENTENCE#'

class ParseSetCreatorWithSimpleParsesetsTest(unittest.TestCase):

    def setUp(self):
        self.parseset_creator = ParseSetCreator()

        all_stems = []

        dictionary_items = LexiconLoader.load_from_file(os.path.join(os.path.dirname(__file__), '../../resources/master_dictionary.txt'))
        for di in dictionary_items:
            all_stems.extend(RootGenerator.generate(di))

        stem_root_map = (RootMapGenerator()).generate(all_stems)

        suffix_graph = SuffixGraph()
        predefined_paths = PredefinedPaths(stem_root_map, suffix_graph)
        predefined_paths.create_predefined_paths()

        word_stem_finder = WordLexemeFinder(stem_root_map)
        numeral_stem_finder = NumeralLexemeFinder()
        proper_noun_from_apostrophe_stem_finder = ProperNounFromApostropheLexemeFinder()
        proper_noun_without_apostrophe_stem_finder = ProperNounWithoutApostropheLexemeFinder()

        self.parser = ContextFreeMorphologicalParser(suffix_graph, predefined_paths,
            [word_stem_finder, numeral_stem_finder, proper_noun_from_apostrophe_stem_finder, proper_noun_without_apostrophe_stem_finder])

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
                    sentence_binding = self.parseset_creator.create_sentence_binding_from_tokens(entries_for_sentence)
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
            if parse_result_part== formatter.format_parse_token_for_simple_parseset(parse_result):
                return parse_result

        return None

if __name__ == '__main__':
    unittest.main()
