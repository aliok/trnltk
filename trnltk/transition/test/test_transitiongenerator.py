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
import logging
import os
import unittest
from hamcrest import *
from trnltk.morphology.lexicon.lexiconloader import LexiconLoader
from trnltk.morphology.lexicon.rootgenerator import RootGenerator, RootMapGenerator
from trnltk.morphology.model import formatter
from trnltk.morphology.morphotactics.basicsuffixgraph import BasicSuffixGraph
from trnltk.morphology.morphotactics.copulasuffixgraph import CopulaSuffixGraph
from trnltk.morphology.contextless.parser.parser import ContextlessMorphologicalParser, logger as parser_logger
from trnltk.morphology.contextless.parser.rootfinder import WordRootFinder, DigitNumeralRootFinder, ProperNounFromApostropheRootFinder, ProperNounWithoutApostropheRootFinder, TextNumeralRootFinder
from trnltk.morphology.contextless.parser.suffixapplier import logger as suffix_applier_logger
from trnltk.morphology.morphotactics.numeralsuffixgraph import NumeralSuffixGraph
from trnltk.morphology.morphotactics.predefinedpaths import PredefinedPaths
from trnltk.morphology.morphotactics.propernounsuffixgraph import ProperNounSuffixGraph
from trnltk.transition.transitiongenerator import TransitionGenerator

class TransitionGeneratorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(TransitionGeneratorTest, cls).setUpClass()
        all_roots = []

        lexemes = LexiconLoader.load_from_file(os.path.join(os.path.dirname(__file__), '../../resources/master_dictionary.txt'))
        for di in lexemes:
            all_roots.extend(RootGenerator.generate(di))

        root_map_generator = RootMapGenerator()
        cls.root_map = root_map_generator.generate(all_roots)

        suffix_graph = CopulaSuffixGraph(NumeralSuffixGraph(ProperNounSuffixGraph(BasicSuffixGraph())))
        suffix_graph.initialize()

        predefined_paths = PredefinedPaths(cls.root_map, suffix_graph)
        predefined_paths.create_predefined_paths()

        word_root_finder = WordRootFinder(cls.root_map)
        digit_numeral_root_finder = DigitNumeralRootFinder()
        text_numeral_root_finder = TextNumeralRootFinder(cls.root_map)
        proper_noun_from_apostrophe_root_finder = ProperNounFromApostropheRootFinder()
        proper_noun_without_apostrophe_root_finder = ProperNounWithoutApostropheRootFinder()

        cls.parser = ContextlessMorphologicalParser(suffix_graph, predefined_paths,
            [word_root_finder, digit_numeral_root_finder, text_numeral_root_finder,
             proper_noun_from_apostrophe_root_finder, proper_noun_without_apostrophe_root_finder])

        cls.transition_generator = TransitionGenerator(cls.parser)

    def test_should_generate_transitions(self):
        parser_logger.setLevel(logging.DEBUG)
        suffix_applier_logger.setLevel(logging.DEBUG)

        self.assert_transitions_generated(
            u'elmaya', u'elma(elma)+Noun+A3sg+Pnon+Dat(+yA[ya])',
            [
                (u'elma',  u'elma(elma)+Noun'),
                (u'elma',  u'elma(elma)+Noun+A3sg'),
                (u'elma',  u'elma(elma)+Noun+A3sg+Pnon'),
                (u'elmaya', u'elma(elma)+Noun+A3sg+Pnon+Dat(+yA[ya])'),
            ]
        )

        self.assert_transitions_generated(
            u'armudu', u'armud(armut)+Noun+A3sg+Pnon+Acc(+yI[u])',
            [
                (u'armud',  u'armud(armut)+Noun'),
                (u'armud',  u'armud(armut)+Noun+A3sg'),
                (u'armud',  u'armud(armut)+Noun+A3sg+Pnon'),
                (u'armudu', u'armud(armut)+Noun+A3sg+Pnon+Acc(+yI[u])'),
            ]
        )

        self.assert_transitions_generated(
            u'yapabildiklerimizden', u'yap(yapmak)+Verb+Verb+Able(+yAbil[abil])+Pos+Noun+PastPart(dIk[dik])+A3pl(lAr[ler])+P1pl(+ImIz[imiz])+Abl(dAn[den])',
            [
                (u'yap',                  u'yap(yapmak)+Verb'),
                (u'yapabil',              u'yap(yapmak)+Verb+Verb+Able(+yAbil[abil])'),
                (u'yapabil',              u'yap(yapmak)+Verb+Verb+Able(+yAbil[abil])+Pos'),
                (u'yapabildik',           u'yap(yapmak)+Verb+Verb+Able(+yAbil[abil])+Pos+Noun+PastPart(dIk[dik])'),
                (u'yapabildikler',        u'yap(yapmak)+Verb+Verb+Able(+yAbil[abil])+Pos+Noun+PastPart(dIk[dik])+A3pl(lAr[ler])'),
                (u'yapabildiklerimiz',    u'yap(yapmak)+Verb+Verb+Able(+yAbil[abil])+Pos+Noun+PastPart(dIk[dik])+A3pl(lAr[ler])+P1pl(+ImIz[imiz])'),
                (u'yapabildiklerimizden', u'yap(yapmak)+Verb+Verb+Able(+yAbil[abil])+Pos+Noun+PastPart(dIk[dik])+A3pl(lAr[ler])+P1pl(+ImIz[imiz])+Abl(dAn[den])')
            ]
        )

        self.assert_transitions_generated(
            u'yaptırttıramazmışız',       u'yap(yapmak)+Verb+Verb+Caus(dIr[tır])+Verb+Caus(t[t])+Verb+Caus(dIr[tır])+Verb+Able(+yA[a])+Neg(mA[ma])+Aor(z[z])+Narr(mIş[mış])+A1pl(+Iz[ız])',
            [
                (u'yap',                  u'yap(yapmak)+Verb'),
                (u'yaptır',               u'yap(yapmak)+Verb+Verb+Caus(dIr[tır])'),
                (u'yaptırt',              u'yap(yapmak)+Verb+Verb+Caus(dIr[tır])+Verb+Caus(t[t])'),
                (u'yaptırttır',           u'yap(yapmak)+Verb+Verb+Caus(dIr[tır])+Verb+Caus(t[t])+Verb+Caus(dIr[tır])'),
                (u'yaptırttıra',          u'yap(yapmak)+Verb+Verb+Caus(dIr[tır])+Verb+Caus(t[t])+Verb+Caus(dIr[tır])+Verb+Able(+yA[a])'),
                (u'yaptırttırama',        u'yap(yapmak)+Verb+Verb+Caus(dIr[tır])+Verb+Caus(t[t])+Verb+Caus(dIr[tır])+Verb+Able(+yA[a])+Neg(mA[ma])'),
                (u'yaptırttıramaz',       u'yap(yapmak)+Verb+Verb+Caus(dIr[tır])+Verb+Caus(t[t])+Verb+Caus(dIr[tır])+Verb+Able(+yA[a])+Neg(mA[ma])+Aor(z[z])'),
                (u'yaptırttıramazmış',    u'yap(yapmak)+Verb+Verb+Caus(dIr[tır])+Verb+Caus(t[t])+Verb+Caus(dIr[tır])+Verb+Able(+yA[a])+Neg(mA[ma])+Aor(z[z])+Narr(mIş[mış])'),
                (u'yaptırttıramazmışız',  u'yap(yapmak)+Verb+Verb+Caus(dIr[tır])+Verb+Caus(t[t])+Verb+Caus(dIr[tır])+Verb+Able(+yA[a])+Neg(mA[ma])+Aor(z[z])+Narr(mIş[mış])+A1pl(+Iz[ız])')
            ]
        )

    def assert_transitions_generated(self, word_to_parse, parse_result_to_pick, expected_transitions):
        picked_morpheme_container = None

        resolutions = self.parser.parse(word_to_parse)
        for resolution in resolutions:
            if formatter.format_morpheme_container_for_tests(resolution) == parse_result_to_pick:
                picked_morpheme_container = resolution
                break

        assert_that(picked_morpheme_container, not_none(),
            u'Parse result to pick {} does not exist in parse resolutions : {}'.format(parse_result_to_pick, [formatter.format_morpheme_container_for_tests(r) for r in resolutions]))

        generated_transitions = self.transition_generator.generate_transitions(word_to_parse, picked_morpheme_container)
        generated_transitions_strs = [(generated_transition.get_surface_so_far(), formatter.format_morpheme_container_for_tests(generated_transition)) for generated_transition in
                                                                                                                              generated_transitions]
        generated_transitions_strs = list(set(generated_transitions_strs))
        generated_transitions_strs = sorted(generated_transitions_strs, cmp=lambda x, y: cmp(len(x[1]), len(y[1])))

        assert_that(len(generated_transitions_strs), equal_to(len(expected_transitions)))

        for i in range(len(expected_transitions)):
            (expected_word, expected_parse_result) = expected_transitions[i]
            (generated_word, generated_parse_result_str) = generated_transitions_strs[i]

            assert_that(expected_word, equal_to(generated_word))
            assert_that(expected_parse_result, equal_to(generated_parse_result_str))

if __name__ == '__main__':
    unittest.main()
