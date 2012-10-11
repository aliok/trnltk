# coding=utf-8
import os
import unittest
from xml.dom.minidom import parse
from hamcrest import *
from trnltk.morphology.contextfree.parser.parser import ContextFreeMorphologicalParser
from trnltk.morphology.contextfree.parser.rootfinder import WordRootFinder
from trnltk.statistics.morphemecontainerstats import MorphemeContainerContextFreeProbabilityGenerator
from trnltk.morphology.lexicon.lexiconloader import LexiconLoader
from trnltk.morphology.lexicon.rootgenerator import RootGenerator, RootMapGenerator
from trnltk.morphology.morphotactics.basicsuffixgraph import BasicSuffixGraph
from trnltk.parseset.xmlbindings import ParseSetBinding
from trnltk.statistics.suffixtransitionstats import SuffixTransitionProbabilityGenerator

dom = parse(os.path.join(os.path.dirname(__file__), 'morphology_contextfree_statistics_sample_parseset.xml'))
parseset = ParseSetBinding.build(dom.getElementsByTagName("parseset")[0])
parse_set_word_list = []
for sentence in parseset.sentences:
    parse_set_word_list.extend(sentence.words)

class MorphemeContainerContextFreeProbabilityGeneratorWithContainersTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(MorphemeContainerContextFreeProbabilityGeneratorWithContainersTest, cls).setUpClass()
        all_roots = []

        lexicon_lines = u'''
            duvar
            tutku
            saç
            oğul [A:LastVowelDrop]
            demek [A:RootChange, Passive_In, Passive_InIl]
            bu [P:Det]
        '''.strip().splitlines()

        lexemes = LexiconLoader.load_from_lines(lexicon_lines)
        for di in lexemes:
            all_roots.extend(RootGenerator.generate(di))

        root_map_generator = RootMapGenerator()
        cls.root_map = root_map_generator.generate(all_roots)

        suffix_graph = BasicSuffixGraph()
        suffix_graph.initialize()

        word_root_finder = WordRootFinder(cls.root_map)

        cls.context_free_parser = ContextFreeMorphologicalParser(suffix_graph, None,
            [word_root_finder])

    def _create_generator_with_words(self, word_indices):
        asked_word_bindings = [word_binding for (index, word_binding) in
                               filter(lambda (index, word): index in word_indices, enumerate(parse_set_word_list))]

        suffix_transition_probability_generator = SuffixTransitionProbabilityGenerator(asked_word_bindings)

        return MorphemeContainerContextFreeProbabilityGenerator(
            suffix_transition_probability_generator.first_suffix_transition_probability_matrix,
            suffix_transition_probability_generator.suffix_transition_probability_matrix
        )

    def test_probabilities_of_words_without_any_other_words_should_be_1(self):
        for i in range(len(parse_set_word_list)):
            generator = self._create_generator_with_words([i])
            parse_results = self.context_free_parser.parse(parse_set_word_list[i].str)
            probabilities = [generator.get_probability(parse_result) for parse_result in parse_results]
            print u'Calculating probability of word {} : {}'.format(parse_set_word_list[i].str, probabilities)
            assert_that(any([probability==1.0 for probability in probabilities]))


if __name__ == '__main__':
    unittest.main()
