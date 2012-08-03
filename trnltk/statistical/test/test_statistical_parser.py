# coding=utf-8
import os
import unittest
from xml.dom.minidom import parse
from trnltk.parseset.xmlbindings import ParseSetBinding
from trnltk.statistical.parser import StatisticalParser
from trnltk.morphology.lexicon.lexiconloader import LexiconLoader
from trnltk.morphology.lexicon.rootgenerator import RootGenerator, RootMapGenerator
from trnltk.morphology.morphotactics.extendedsuffixgraph import ExtendedSuffixGraph
from trnltk.morphology.contextfree.parser.parser import ContextFreeMorphologicalParser
from trnltk.morphology.contextfree.parser.lexemefinder import WordLexemeFinder, NumeralLexemeFinder, ProperNounFromApostropheLexemeFinder, ProperNounWithoutApostropheLexemeFinder
from trnltk.morphology.morphotactics.predefinedpaths import PredefinedPaths
from trnltk.treebank.explorer import CompleteWordConcordanceIndex

class StatisticalParserTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(StatisticalParserTest, cls).setUpClass()
        all_roots = []

        dictionary_items = LexiconLoader.load_from_file(os.path.join(os.path.dirname(__file__), '../../resources/master_dictionary.txt'))
        for di in dictionary_items:
            all_roots.extend(RootGenerator.generate(di))


        root_map_generator = RootMapGenerator()
        cls.root_map = root_map_generator.generate(all_roots)

        suffix_graph = ExtendedSuffixGraph()
        predefined_paths = PredefinedPaths(cls.root_map, suffix_graph)
        predefined_paths.create_predefined_paths()

        word_lexeme_finder = WordLexemeFinder(cls.root_map)
        numeral_lexeme_finder = NumeralLexemeFinder()
        proper_noun_from_apostrophe_lexeme_finder = ProperNounFromApostropheLexemeFinder()
        proper_noun_without_apostrophe_lexeme_finder = ProperNounWithoutApostropheLexemeFinder()

        context_free_parser = ContextFreeMorphologicalParser(suffix_graph, predefined_paths,
            [word_lexeme_finder, numeral_lexeme_finder, proper_noun_from_apostrophe_lexeme_finder, proper_noun_without_apostrophe_lexeme_finder])

        parseset_index = "001"
        dom = parse(os.path.join(os.path.dirname(__file__), '../../testresources/parsesets/parseset{}.xml'.format(parseset_index)))
        parseset = ParseSetBinding.build(dom.getElementsByTagName("parseset")[0])
        parse_set_word_list = []
        for sentence in parseset.sentences:
            parse_set_word_list.extend(sentence.words)

        complete_word_concordance_index = CompleteWordConcordanceIndex(parse_set_word_list)

        cls.parser = StatisticalParser(context_free_parser, complete_word_concordance_index)

    def test_should_parse(self):
        result = self.parser.parse(u'verirsiniz')
        print result.get_parse_results_with_ratio()


if __name__ == '__main__':
    unittest.main()
