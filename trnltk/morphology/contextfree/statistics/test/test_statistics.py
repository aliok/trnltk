# coding=utf-8
import os
import unittest
from xml.dom.minidom import parse
from hamcrest import *
from trnltk.morphology.contextfree.parser.parser import ContextFreeMorphologicalParser
from trnltk.morphology.contextfree.parser.rootfinder import WordRootFinder
from trnltk.morphology.contextfree.statistics.statistics import MorphemeContainerContextFreeProbabilityGenerator
from trnltk.morphology.lexicon.lexiconloader import LexiconLoader
from trnltk.morphology.lexicon.rootgenerator import RootGenerator, RootMapGenerator
from trnltk.morphology.morphotactics.suffixgraph import SuffixGraph
from trnltk.parseset.xmlbindings import ParseSetBinding

dom = parse(os.path.join(os.path.dirname(__file__), 'morphology_contextfree_statistics_sample_parseset.xml'))
parseset = ParseSetBinding.build(dom.getElementsByTagName("parseset")[0])
parse_set_word_list = []
for sentence in parseset.sentences:
    parse_set_word_list.extend(sentence.words)

class MorphemeContainerContextFreeProbabilityGeneratorTest(unittest.TestCase):
    def _create_generator_with_words(self, word_indices):
        asked_word_bindings = [word_binding for (index, word_binding) in
                               filter(lambda (index, word): index in word_indices, enumerate(parse_set_word_list))]
        return MorphemeContainerContextFreeProbabilityGenerator(asked_word_bindings)

    def test_should_check_words_0_and_1(self):
        generator = self._create_generator_with_words([0, 1])

        assert_that(generator.first_suffix_transition_probability_matrix['Noun']['A3Sg_Noun'], equal_to(1.0))

        assert_that(generator.suffix_transition_probability_matrix['A3Sg_Noun']['Pnon_Noun'], equal_to(1.0))
        assert_that(generator.suffix_transition_probability_matrix['Pnon_Noun']['Dat_Noun'], equal_to(0.5))
        assert_that(generator.suffix_transition_probability_matrix['Pnon_Noun']['Acc_Noun'], equal_to(0.5))

    def test_should_check_words_1_and_2(self):
        generator = self._create_generator_with_words([1, 2])

        assert_that(generator.first_suffix_transition_probability_matrix['Noun']['A3Sg_Noun'], equal_to(0.5))
        assert_that(generator.first_suffix_transition_probability_matrix['Noun']['A3Pl_Noun'], equal_to(0.5))

        assert_that(generator.suffix_transition_probability_matrix['A3Sg_Noun']['Pnon_Noun'], equal_to(1.0))
        assert_that(generator.suffix_transition_probability_matrix['Pnon_Noun']['Acc_Noun'], equal_to(1.0))

        assert_that(generator.suffix_transition_probability_matrix['A3Pl_Noun']['P3sg_Noun'], equal_to(1.0))
        assert_that(generator.suffix_transition_probability_matrix['P3sg_Noun']['Nom_Noun'], equal_to(1.0))

    def test_should_check_words_1_2_and_3(self):
        generator = self._create_generator_with_words([1, 2, 3])

        assert_that(generator.first_suffix_transition_probability_matrix['Noun']['A3Sg_Noun'], equal_to(2.0 / 3.0))
        assert_that(generator.first_suffix_transition_probability_matrix['Noun']['A3Pl_Noun'], equal_to(1.0 / 3.0))

        assert_that(generator.suffix_transition_probability_matrix['A3Sg_Noun']['Pnon_Noun'], equal_to(0.5))
        assert_that(generator.suffix_transition_probability_matrix['A3Sg_Noun']['P1sg_Noun'], equal_to(0.5))

        assert_that(generator.suffix_transition_probability_matrix['A3Pl_Noun']['P3sg_Noun'], equal_to(1.0))

        assert_that(generator.suffix_transition_probability_matrix['Pnon_Noun']['Acc_Noun'], equal_to(1.0))
        assert_that(generator.suffix_transition_probability_matrix['P3sg_Noun']['Nom_Noun'], equal_to(1.0))
        assert_that(generator.suffix_transition_probability_matrix['P1sg_Noun']['Nom_Noun'], equal_to(1.0))

    def test_should_check_words_1_and_4(self):
        generator = self._create_generator_with_words([1, 4])

        assert_that(generator.first_suffix_transition_probability_matrix['Noun']['A3Sg_Noun'], equal_to(1.0))
        assert_that(generator.first_suffix_transition_probability_matrix['Verb']['Pos'], equal_to(1.0))

        assert_that(generator.suffix_transition_probability_matrix['A3Sg_Noun']['Pnon_Noun'], equal_to(1.0))
        assert_that(generator.suffix_transition_probability_matrix['Pnon_Noun']['Acc_Noun'], equal_to(1.0))

        assert_that(generator.suffix_transition_probability_matrix['Pos']['Past'], equal_to(1.0))
        assert_that(generator.suffix_transition_probability_matrix['Past']['A3Sg_Verb'], equal_to(1.0))

    def test_should_check_word_5(self):
        generator = self._create_generator_with_words([5])

        assert_that(generator.first_suffix_transition_probability_matrix, has_length(0))
        assert_that(generator.suffix_transition_probability_matrix, has_length(0))

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

        suffix_graph = SuffixGraph()

        word_root_finder = WordRootFinder(cls.root_map)

        cls.context_free_parser = ContextFreeMorphologicalParser(suffix_graph, None,
            [word_root_finder])

    def _create_generator_with_words(self, word_indices):
        asked_word_bindings = [word_binding for (index, word_binding) in
                               filter(lambda (index, word): index in word_indices, enumerate(parse_set_word_list))]
        return MorphemeContainerContextFreeProbabilityGenerator(asked_word_bindings)

    def test_probabilities_of_words_without_any_other_words_should_be_1(self):
        for i in range(len(parse_set_word_list)):
            generator = self._create_generator_with_words([i])
            parse_results = self.context_free_parser.parse(parse_set_word_list[i].str)
            assert_that(any([generator.get_probability(parse_result)==1.0 for parse_result in parse_results]))


if __name__ == '__main__':
    unittest.main()
