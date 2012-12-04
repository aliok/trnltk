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
from difflib import context_diff
import os
import unittest
from hamcrest.core.assert_that import assert_that
from hamcrest.core.core.isequal import equal_to
from trnltk.morphology.contextless.parser.parser import  UpperCaseSupportingContextlessMorphologicalParser
from trnltk.morphology.model import formatter
from trnltk.morphology.morphotactics.copulasuffixgraph import CopulaSuffixGraph
from trnltk.morphology.morphotactics.numeralsuffixgraph import NumeralSuffixGraph
from trnltk.morphology.morphotactics.propernounsuffixgraph import ProperNounSuffixGraph
from trnltk.parseset.creator import ParseSetCreator
from trnltk.morphology.contextless.parser.rootfinder import DigitNumeralRootFinder, WordRootFinder, TextNumeralRootFinder, ProperNounFromApostropheRootFinder, ProperNounWithoutApostropheRootFinder
from trnltk.morphology.lexicon.lexiconloader import LexiconLoader
from trnltk.morphology.lexicon.rootgenerator import RootGenerator, RootMapGenerator
from trnltk.morphology.morphotactics.predefinedpaths import PredefinedPaths
from trnltk.morphology.morphotactics.basicsuffixgraph import BasicSuffixGraph

class ParseSetCreatorTest(unittest.TestCase):

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

    def test_should_create_sentence_binding_from_morpheme_containers(self):
        morpheme_containers = []
        morpheme_containers.append(self._get_word_morpheme_container_tuple(u'blablabla'))
        morpheme_containers.append(self._get_word_morpheme_container_tuple(u'Kitaba', u'kitap+Noun+A3sg+Pnon+Dat'))
        morpheme_containers.append(self._get_word_morpheme_container_tuple(u'abcabcabc'))
        morpheme_containers.append(self._get_word_morpheme_container_tuple(u'buyurmam'))
        morpheme_containers.append(self._get_word_morpheme_container_tuple(u'yetiştirdik'))
        morpheme_containers.append(self._get_word_morpheme_container_tuple(u'Kıvrandığın', u'kıvran+Verb+Pos+Adj+PastPart+P2sg'))
        morpheme_containers.append(self._get_word_morpheme_container_tuple(u'sabahçı'))
        morpheme_containers.append(self._get_word_morpheme_container_tuple(u'sabah'))
        morpheme_containers.append(self._get_word_morpheme_container_tuple(u"Ali'nin"))

        sentence = self.parseset_creator.create_sentence_binding_from_morpheme_containers(morpheme_containers)

        expected = u'''
<sentence>
	<unparsable_word str="blablabla"/>
	<word parse_result="kitap+Noun+A3sg+Pnon+Dat" str="Kitaba" syntactic_category="Noun">
		<root lemma="kitap" lemma_root="kitap" str="kitab" syntactic_category="Noun"/>
		<suffixes>
			<inflectionalSuffix actual="" application="" form="" id="A3Sg_Noun" matched_word="kitab" name="A3sg" to_syntactic_category="Noun" word="kitap"/>
			<inflectionalSuffix actual="" application="" form="" id="Pnon_Noun" matched_word="kitab" name="Pnon" to_syntactic_category="Noun" word="kitap"/>
			<inflectionalSuffix actual="a" application="a" form="+yA" id="Dat_Noun" matched_word="kitaba" name="Dat" to_syntactic_category="Noun" word="kitaba"/>
		</suffixes>
	</word>
	<unparsable_word str="abcabcabc"/>
	<word parse_result="buyur+Verb+Neg+Aor+A1sg" str="buyurmam" syntactic_category="Verb">
		<root lemma="buyurmak" lemma_root="buyur" str="buyur" syntactic_category="Verb"/>
		<suffixes>
			<inflectionalSuffix actual="ma" application="ma" form="mA" id="Neg" matched_word="buyurma" name="Neg" to_syntactic_category="Verb" word="buyurma"/>
			<inflectionalSuffix actual="" application="" form="" id="Aor" matched_word="buyurma" name="Aor" to_syntactic_category="Verb" word="buyurma"/>
			<inflectionalSuffix actual="m" application="m" form="+Im" id="A1Sg_Verb" matched_word="buyurmam" name="A1sg" to_syntactic_category="Verb" word="buyurmam"/>
		</suffixes>
	</word>
	<word parse_result="yetiş+Verb+Verb+Caus+Pos+Past+A1pl" str="yetiştirdik" syntactic_category="Verb">
		<root lemma="yetişmek" lemma_root="yetiş" str="yetiş" syntactic_category="Verb"/>
		<suffixes>
			<derivationalSuffix actual="tir" application="tir" form="dIr" id="Caus" matched_word="yetiştir" name="Caus" to_syntactic_category="Verb" word="yetiştir"/>
			<inflectionalSuffix actual="" application="" form="" id="Pos" matched_word="yetiştir" name="Pos" to_syntactic_category="Verb" word="yetiştir"/>
			<inflectionalSuffix actual="di" application="di" form="dI" id="Past" matched_word="yetiştirdi" name="Past" to_syntactic_category="Verb" word="yetiştirdi"/>
			<inflectionalSuffix actual="k" application="k" form="k" id="A1Pl_Verb" matched_word="yetiştirdik" name="A1pl" to_syntactic_category="Verb" word="yetiştirdik"/>
		</suffixes>
	</word>
	<word parse_result="kıvran+Verb+Pos+Adj+PastPart+P2sg" str="Kıvrandığın" syntactic_category="Adj">
		<root lemma="kıvranmak" lemma_root="kıvran" str="kıvran" syntactic_category="Verb"/>
		<suffixes>
			<inflectionalSuffix actual="" application="" form="" id="Pos" matched_word="kıvran" name="Pos" to_syntactic_category="Verb" word="kıvran"/>
			<derivationalSuffix actual="dığ" application="dık" form="dIk" id="PastPart_Adj" matched_word="kıvrandığ" name="PastPart" to_syntactic_category="Adj" word="kıvrandık"/>
			<inflectionalSuffix actual="ın" application="ın" form="+In" id="P2Sg_Adj" matched_word="kıvrandığın" name="P2sg" to_syntactic_category="Adj" word="kıvrandığın"/>
		</suffixes>
	</word>
	<word parse_result="sabah+Noun+Time+A3sg+Pnon+Nom+Adj+Agt" str="sabahçı" syntactic_category="Adj">
		<root lemma="sabah" lemma_root="sabah" secondary_syntactic_category="Time" str="sabah" syntactic_category="Noun"/>
		<suffixes>
			<inflectionalSuffix actual="" application="" form="" id="A3Sg_Noun" matched_word="sabah" name="A3sg" to_syntactic_category="Noun" word="sabah"/>
			<inflectionalSuffix actual="" application="" form="" id="Pnon_Noun" matched_word="sabah" name="Pnon" to_syntactic_category="Noun" word="sabah"/>
			<inflectionalSuffix actual="" application="" form="" id="Nom_Deriv_Noun" matched_word="sabah" name="Nom" to_syntactic_category="Noun" word="sabah"/>
			<derivationalSuffix actual="çı" application="çı" form="cI" id="Agt_Noun_to_Adj" matched_word="sabahçı" name="Agt" to_syntactic_category="Adj" word="sabahçı"/>
		</suffixes>
	</word>
	<word parse_result="sabah+Adv+Time" secondary_syntactic_category="Time" str="sabah" syntactic_category="Adv">
		<root lemma="sabah" lemma_root="sabah" secondary_syntactic_category="Time" str="sabah" syntactic_category="Adv"/>
	</word>
	<word parse_result="Ali+Noun+Prop+Apos+A3sg+Pnon+Gen" secondary_syntactic_category="Prop" str="Ali'nin" syntactic_category="Noun">
		<root lemma="Ali" lemma_root="Ali" secondary_syntactic_category="Prop" str="Ali" syntactic_category="Noun"/>
		<suffixes>
			<inflectionalSuffix actual="'" application="'" form="'" id="Apos_Proper_Noun" matched_word="Ali'" name="Apos" to_syntactic_category="Noun" word="Ali'"/>
			<inflectionalSuffix actual="" application="" form="" id="A3Sg_Noun" matched_word="Ali'" name="A3sg" to_syntactic_category="Noun" word="Ali'"/>
			<inflectionalSuffix actual="" application="" form="" id="Pnon_Noun" matched_word="Ali'" name="Pnon" to_syntactic_category="Noun" word="Ali'"/>
			<inflectionalSuffix actual="nin" application="nin" form="+nIn" id="Gen_Noun" matched_word="Ali'nin" name="Gen" to_syntactic_category="Noun" word="Ali'nin"/>
		</suffixes>
	</word>
</sentence>
'''
        expected = expected.strip()
        actual = sentence.to_dom().toprettyxml().strip()

        if expected!=actual:
            for line in context_diff(expected.split('\n'), actual.split('\n'), "expected", "actual"):
                print line

        assert_that(expected, equal_to(sentence.to_dom().toprettyxml().strip()))

    def _get_word_morpheme_container_tuple(self, seq, expected_result=None):
        res = self.parser.parse(seq)

        if res:
            if expected_result:
                matching_containers = filter(lambda parse_result : formatter.format_morpheme_container_for_parseset(parse_result)==expected_result, res)
                if matching_containers:
                    return seq, matching_containers[0]
                else:
                    return seq, None
            else:
                return seq, res[0]
        else:
            return seq, None

if __name__ == '__main__':
    unittest.main()
