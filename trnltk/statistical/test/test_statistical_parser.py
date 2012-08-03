# coding=utf-8
import os
import unittest
from xml.dom.minidom import parse
from trnltk.parseset.xmlbindings import ParseSetBinding
from trnltk.statistical.parser import StatisticalParser
from trnltk.morphology.stem.dictionaryloader import DictionaryLoader
from trnltk.morphology.stem.stemgenerator import StemGenerator, StemRootMapGenerator
from trnltk.morphology.suffixgraph.extendedsuffixgraph import ExtendedSuffixGraph
from trnltk.morphology.parser.parser import Parser
from trnltk.morphology.parser.stemfinder import WordStemFinder, NumeralStemFinder, ProperNounFromApostropheStemFinder, ProperNounWithoutApostropheStemFinder
from trnltk.morphology.suffixgraph.predefinedpaths import PredefinedPaths
from trnltk.treebank.explorer import CompleteWordConcordanceIndex

class StatisticalParserTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(StatisticalParserTest, cls).setUpClass()
        all_stems = []

        dictionary_items = DictionaryLoader.load_from_file(os.path.join(os.path.dirname(__file__), '../../resources/master_dictionary.txt'))
        for di in dictionary_items:
            all_stems.extend(StemGenerator.generate(di))


        stem_root_map_generator = StemRootMapGenerator()
        cls.stem_root_map = stem_root_map_generator.generate(all_stems)

        suffix_graph = ExtendedSuffixGraph()
        predefined_paths = PredefinedPaths(cls.stem_root_map, suffix_graph)
        predefined_paths.create_predefined_paths()

        word_stem_finder = WordStemFinder(cls.stem_root_map)
        numeral_stem_finder = NumeralStemFinder()
        proper_noun_from_apostrophe_stem_finder = ProperNounFromApostropheStemFinder()
        proper_noun_without_apostrophe_stem_finder = ProperNounWithoutApostropheStemFinder()

        context_free_parser = Parser(suffix_graph, predefined_paths,
            [word_stem_finder, numeral_stem_finder, proper_noun_from_apostrophe_stem_finder, proper_noun_without_apostrophe_stem_finder])

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
