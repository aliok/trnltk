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
from hamcrest import *
from trnltk.parseset.xmlbindings import ParseSetBinding
from trnltk.statistics.suffixtransitionstats import SuffixTransitionProbabilityGenerator

dom = parse(os.path.join(os.path.dirname(__file__), '../../morphology/contextful/likelihoodmetrics/wordformcollocation/test/morphology_contextless_statistics_sample_parseset.xml'))
parseset = ParseSetBinding.build(dom.getElementsByTagName("parseset")[0])
parse_set_word_list = []
for sentence in parseset.sentences:
    parse_set_word_list.extend(sentence.words)

class SuffixTransitionProbabilityGeneratorTest(unittest.TestCase):
    def _create_generator_with_words(self, word_indices):
        asked_word_bindings = [word_binding for (index, word_binding) in
                               filter(lambda (index, word): index in word_indices, enumerate(parse_set_word_list))]
        return SuffixTransitionProbabilityGenerator(asked_word_bindings)

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

        assert_that(generator.suffix_transition_probability_matrix['A3Pl_Noun']['P3Sg_Noun'], equal_to(1.0))
        assert_that(generator.suffix_transition_probability_matrix['P3Sg_Noun']['Nom_Noun'], equal_to(1.0))

    def test_should_check_words_1_2_and_3(self):
        generator = self._create_generator_with_words([1, 2, 3])

        assert_that(generator.first_suffix_transition_probability_matrix['Noun']['A3Sg_Noun'], equal_to(2.0 / 3.0))
        assert_that(generator.first_suffix_transition_probability_matrix['Noun']['A3Pl_Noun'], equal_to(1.0 / 3.0))

        assert_that(generator.suffix_transition_probability_matrix['A3Sg_Noun']['Pnon_Noun'], equal_to(0.5))
        assert_that(generator.suffix_transition_probability_matrix['A3Sg_Noun']['P1Sg_Noun'], equal_to(0.5))

        assert_that(generator.suffix_transition_probability_matrix['A3Pl_Noun']['P3Sg_Noun'], equal_to(1.0))

        assert_that(generator.suffix_transition_probability_matrix['Pnon_Noun']['Acc_Noun'], equal_to(1.0))
        assert_that(generator.suffix_transition_probability_matrix['P3Sg_Noun']['Nom_Noun'], equal_to(1.0))
        assert_that(generator.suffix_transition_probability_matrix['P1Sg_Noun']['Nom_Noun'], equal_to(1.0))

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

if __name__ == '__main__':
    unittest.main()
