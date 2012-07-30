# coding=utf-8
from difflib import context_diff
import os
import unittest
from hamcrest.core.assert_that import assert_that
from hamcrest.core.core.isequal import equal_to
from trnltk.parser.parser import Parser
from trnltk.parseset.creator import ParseSetCreator
from trnltk.parser.stemfinder import NumeralStemFinder, WordStemFinder
from trnltk.stem.dictionaryloader import DictionaryLoader
from trnltk.stem.stemgenerator import StemGenerator, StemRootMapGenerator
from trnltk.suffixgraph.predefinedpaths import PredefinedPaths
from trnltk.suffixgraph.suffixgraph import SuffixGraph

class ParseSetCreatorTest(unittest.TestCase):

    def setUp(self):
        self.parseset_creator = ParseSetCreator()

        all_stems = []

        dictionary_items = DictionaryLoader.load_from_file(os.path.join(os.path.dirname(__file__), '../../resources/master_dictionary.txt'))
        for di in dictionary_items:
            all_stems.extend(StemGenerator.generate(di))

        stem_root_map = (StemRootMapGenerator()).generate(all_stems)

        suffix_graph = SuffixGraph()
        predefined_paths = PredefinedPaths(stem_root_map, suffix_graph)
        predefined_paths.create_predefined_paths()

        word_stem_finder = WordStemFinder(stem_root_map)
        numeral_stem_finder = NumeralStemFinder()

        self.parser = Parser(suffix_graph, predefined_paths, [word_stem_finder, numeral_stem_finder])

    def test_should_create_sentence_binding_from_tokens(self):
        tokens = []
        tokens.append(self._get_word_token_tuple(u'blablabla'))
        tokens.append(self._get_word_token_tuple(u'kitaba'))
        tokens.append(self._get_word_token_tuple(u'abcabcabc'))
        tokens.append(self._get_word_token_tuple(u'buyurmam'))
        tokens.append(self._get_word_token_tuple(u'yetiştirdik'))
        tokens.append(self._get_word_token_tuple(u'kıvrandığın'))
        tokens.append(self._get_word_token_tuple(u'sabahçı'))
        tokens.append(self._get_word_token_tuple(u'sabah'))

        sentence = self.parseset_creator.create_sentence_binding_from_tokens(tokens)

        expected = u'''
<sentence>
	<unparsable_word str="blablabla"/>
	<word parse_result="kitap+Noun+A3sg+Pnon+Dat" str="kitaba" syntactic_category="Noun">
		<stem lemma="kitap" lemma_root="kitap" root="kitab" syntactic_category="Noun"/>
		<suffixes>
			<inflectionalSuffix actual="" application="" form="" id="A3Sg_Noun" matched_word="kitab" name="A3sg" to_syntactic_category="Noun" word="kitap"/>
			<inflectionalSuffix actual="" application="" form="" id="Pnon_Noun" matched_word="kitab" name="Pnon" to_syntactic_category="Noun" word="kitap"/>
			<inflectionalSuffix actual="a" application="a" form="+yA" id="Dat_Noun" matched_word="kitaba" name="Dat" to_syntactic_category="Noun" word="kitaba"/>
		</suffixes>
	</word>
	<unparsable_word str="abcabcabc"/>
	<word parse_result="buyur+Verb+Neg+Aor+A1sg" str="buyurmam" syntactic_category="Verb">
		<stem lemma="buyurmak" lemma_root="buyur" root="buyur" syntactic_category="Verb"/>
		<suffixes>
			<inflectionalSuffix actual="ma" application="ma" form="mA" id="Neg" matched_word="buyurma" name="Neg" to_syntactic_category="Verb" word="buyurma"/>
			<inflectionalSuffix actual="" application="" form="" id="Aor" matched_word="buyurma" name="Aor" to_syntactic_category="Verb" word="buyurma"/>
			<inflectionalSuffix actual="m" application="m" form="+Im" id="A1Sg_Verb" matched_word="buyurmam" name="A1sg" to_syntactic_category="Verb" word="buyurmam"/>
		</suffixes>
	</word>
	<word parse_result="yetiş+Verb+Verb+Caus+Pos+Past+A1pl" str="yetiştirdik" syntactic_category="Verb">
		<stem lemma="yetişmek" lemma_root="yetiş" root="yetiş" syntactic_category="Verb"/>
		<suffixes>
			<derivationalSuffix actual="tir" application="tir" form="dIr" id="Caus" matched_word="yetiştir" name="Caus" to_syntactic_category="Verb" word="yetiştir"/>
			<inflectionalSuffix actual="" application="" form="" id="Pos" matched_word="yetiştir" name="Pos" to_syntactic_category="Verb" word="yetiştir"/>
			<inflectionalSuffix actual="di" application="di" form="dI" id="Past" matched_word="yetiştirdi" name="Past" to_syntactic_category="Verb" word="yetiştirdi"/>
			<inflectionalSuffix actual="k" application="k" form="k" id="A1Pl_Verb" matched_word="yetiştirdik" name="A1pl" to_syntactic_category="Verb" word="yetiştirdik"/>
		</suffixes>
	</word>
	<word parse_result="kıvran+Verb+Pos+Adj+PastPart+P2sg" str="kıvrandığın" syntactic_category="Adj">
		<stem lemma="kıvranmak" lemma_root="kıvran" root="kıvran" syntactic_category="Verb"/>
		<suffixes>
			<inflectionalSuffix actual="" application="" form="" id="Pos" matched_word="kıvran" name="Pos" to_syntactic_category="Verb" word="kıvran"/>
			<derivationalSuffix actual="dığ" application="dık" form="dIk" id="PastPart_Adj" matched_word="kıvrandığ" name="PastPart" to_syntactic_category="Adj" word="kıvrandık"/>
			<inflectionalSuffix actual="ın" application="ın" form="+In" id="P2Sg_Adj" matched_word="kıvrandığın" name="P2sg" to_syntactic_category="Adj" word="kıvrandığın"/>
		</suffixes>
	</word>
	<word parse_result="sabah+Noun+Time+A3sg+Pnon+Nom+Noun+Agt+A3sg+Pnon+Nom" str="sabahçı" syntactic_category="Noun">
		<stem lemma="sabah" lemma_root="sabah" root="sabah" secondary_syntactic_category="Time" syntactic_category="Noun"/>
		<suffixes>
			<inflectionalSuffix actual="" application="" form="" id="A3Sg_Noun" matched_word="sabah" name="A3sg" to_syntactic_category="Noun" word="sabah"/>
			<inflectionalSuffix actual="" application="" form="" id="Pnon_Noun" matched_word="sabah" name="Pnon" to_syntactic_category="Noun" word="sabah"/>
			<inflectionalSuffix actual="" application="" form="" id="Nom_Deriv_Noun" matched_word="sabah" name="Nom" to_syntactic_category="Noun" word="sabah"/>
			<derivationalSuffix actual="çı" application="çı" form="cI" id="Agt_Noun" matched_word="sabahçı" name="Agt" to_syntactic_category="Noun" word="sabahçı"/>
			<inflectionalSuffix actual="" application="" form="" id="A3Sg_Noun" matched_word="sabahçı" name="A3sg" to_syntactic_category="Noun" word="sabahçı"/>
			<inflectionalSuffix actual="" application="" form="" id="Pnon_Noun" matched_word="sabahçı" name="Pnon" to_syntactic_category="Noun" word="sabahçı"/>
			<inflectionalSuffix actual="" application="" form="" id="Nom_Noun" matched_word="sabahçı" name="Nom" to_syntactic_category="Noun" word="sabahçı"/>
		</suffixes>
	</word>
	<word parse_result="sabah+Noun+Time+A3sg+Pnon+Nom" secondary_syntactic_category="Time" str="sabah" syntactic_category="Noun">
		<stem lemma="sabah" lemma_root="sabah" root="sabah" secondary_syntactic_category="Time" syntactic_category="Noun"/>
		<suffixes>
			<inflectionalSuffix actual="" application="" form="" id="A3Sg_Noun" matched_word="sabah" name="A3sg" to_syntactic_category="Noun" word="sabah"/>
			<inflectionalSuffix actual="" application="" form="" id="Pnon_Noun" matched_word="sabah" name="Pnon" to_syntactic_category="Noun" word="sabah"/>
			<inflectionalSuffix actual="" application="" form="" id="Nom_Noun" matched_word="sabah" name="Nom" to_syntactic_category="Noun" word="sabah"/>
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

    def _get_word_token_tuple(self, seq):
        res = self.parser.parse(seq)
        if res:
            return (seq, res[0])
        else:
            return (seq, None)

if __name__ == '__main__':
    unittest.main()
