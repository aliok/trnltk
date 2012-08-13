# coding=utf-8
import os
import unittest
from xml.dom.minidom import parse
import pymongo
from trnltk.morphology.contextfree.parser.parser import ContextFreeMorphologicalParser
from trnltk.morphology.contextfree.parser.rootfinder import WordRootFinder, NumeralRootFinder, ProperNounFromApostropheRootFinder, ProperNounWithoutApostropheRootFinder
from trnltk.morphology.model import formatter
from trnltk.morphology.morphotactics.extendedsuffixgraph import ExtendedSuffixGraph
from trnltk.morphology.morphotactics.predefinedpaths import PredefinedPaths
from trnltk.statistics.contextstats import BigramContextProbabilityGenerator
from trnltk.morphology.lexicon.lexiconloader import LexiconLoader
from trnltk.morphology.lexicon.rootgenerator import RootGenerator, RootMapGenerator
from trnltk.parseset.xmlbindings import ParseSetBinding

dom = parse(os.path.join(os.path.dirname(__file__), 'morphology_contextfree_statistics_sample_parseset.xml'))
parseset = ParseSetBinding.build(dom.getElementsByTagName("parseset")[0])
parse_set_word_list = []
for sentence in parseset.sentences:
    parse_set_word_list.extend(sentence.words)

class BigramContextProbabilityGeneratorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(BigramContextProbabilityGeneratorTest, cls).setUpClass()
        all_roots = []

        lexemes = LexiconLoader.load_from_file(os.path.join(os.path.dirname(__file__), '../../resources/master_dictionary.txt'))
        for di in lexemes:
            all_roots.extend(RootGenerator.generate(di))

        root_map_generator = RootMapGenerator()
        cls.root_map = root_map_generator.generate(all_roots)

        suffix_graph = ExtendedSuffixGraph()
        predefined_paths = PredefinedPaths(cls.root_map, suffix_graph)
        predefined_paths.create_predefined_paths()

        word_root_finder = WordRootFinder(cls.root_map)
        numeral_root_finder = NumeralRootFinder()
        proper_noun_from_apostrophe_root_finder = ProperNounFromApostropheRootFinder()
        proper_noun_without_apostrophe_root_finder = ProperNounWithoutApostropheRootFinder()

        cls.context_free_parser = ContextFreeMorphologicalParser(suffix_graph, predefined_paths,
            [word_root_finder, numeral_root_finder, proper_noun_from_apostrophe_root_finder, proper_noun_without_apostrophe_root_finder])

        mongodb_connection = pymongo.Connection()
        collection = mongodb_connection['trnltk']['wordBigrams999']

        cls.generator = BigramContextProbabilityGenerator(collection)

    def test_generate_one_word(self):
        context = [u'bir']
        surface = u'erkek'

        context_with_parse_results = [(cw, self.context_free_parser.parse(cw)) for cw in context]
        print [(cw, [formatter.format_morpheme_container_for_parseset(cwr) for cwr in cwrs]) for cw, cwrs in context_with_parse_results]
        print

        results = self.context_free_parser.parse(surface)
        for result in results:
            formatted_parse_result = formatter.format_morpheme_container_for_parseset(result)
            likelihood = self.generator.generate(result, context_with_parse_results)
            print formatted_parse_result, likelihood


if __name__ == '__main__':
    unittest.main()
