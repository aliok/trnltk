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
	<word parse_result="kitap+Noun+A3sg+Pnon+Dat" syntactic_category="Noun" str="kitaba">
		<stem lemma="kitap" lemma_root="kitap" syntactic_category="Noun" root="kitab"/>
		<suffixes>
			<inflectionalSuffix actual="" application="" form="" id="A3Sg_Noun" matched_word="kitab" name="A3sg" word="kitap"/>
			<inflectionalSuffix actual="" application="" form="" id="Pnon_Noun" matched_word="kitab" name="Pnon" word="kitap"/>
			<inflectionalSuffix actual="a" application="a" form="+yA" id="Dat_Noun" matched_word="kitaba" name="Dat" word="kitaba"/>
		</suffixes>
	</word>
	<unparsable_word str="abcabcabc"/>
	<word parse_result="buyur+Verb+Neg+Aor+A1sg" syntactic_category="Verb" str="buyurmam">
		<stem lemma="buyurmak" lemma_root="buyur" syntactic_category="Verb" root="buyur"/>
		<suffixes>
			<inflectionalSuffix actual="ma" application="ma" form="mA" id="Neg" matched_word="buyurma" name="Neg" word="buyurma"/>
			<inflectionalSuffix actual="" application="" form="" id="Aor" matched_word="buyurma" name="Aor" word="buyurma"/>
			<inflectionalSuffix actual="m" application="m" form="+Im" id="A1Sg_Verb" matched_word="buyurmam" name="A1sg" word="buyurmam"/>
		</suffixes>
	</word>
	<word parse_result="yetiş+Verb+Verb+Caus+Pos+Past+A1pl" syntactic_category="Verb" str="yetiştirdik">
		<stem lemma="yetişmek" lemma_root="yetiş" syntactic_category="Verb" root="yetiş"/>
		<suffixes>
			<derivationalSuffix actual="tir" application="tir" form="dIr" id="Caus" matched_word="yetiştir" name="Caus" to="Verb" word="yetiştir"/>
			<inflectionalSuffix actual="" application="" form="" id="Pos" matched_word="yetiştir" name="Pos" word="yetiştir"/>
			<inflectionalSuffix actual="di" application="di" form="dI" id="Past" matched_word="yetiştirdi" name="Past" word="yetiştirdi"/>
			<inflectionalSuffix actual="k" application="k" form="k" id="A1Pl_Verb" matched_word="yetiştirdik" name="A1pl" word="yetiştirdik"/>
		</suffixes>
	</word>
	<word parse_result="kıvran+Verb+Pos+Adj+PastPart+P2sg" syntactic_category="Adj" str="kıvrandığın">
		<stem lemma="kıvranmak" lemma_root="kıvran" syntactic_category="Verb" root="kıvran"/>
		<suffixes>
			<inflectionalSuffix actual="" application="" form="" id="Pos" matched_word="kıvran" name="Pos" word="kıvran"/>
			<derivationalSuffix actual="dığ" application="dık" form="dIk" id="PastPart_Adj" matched_word="kıvrandığ" name="PastPart" to="Adj" word="kıvrandık"/>
			<inflectionalSuffix actual="ın" application="ın" form="+In" id="P2Sg_Adj" matched_word="kıvrandığın" name="P2sg" word="kıvrandığın"/>
		</suffixes>
	</word>
	<word parse_result="sabah+Noun+Time+A3sg+Pnon+Nom+Noun+Agt+A3sg+Pnon+Nom" syntactic_category="Noun" str="sabahçı">
		<stem lemma="sabah" lemma_root="sabah" syntactic_category="Noun" root="sabah" secondary_syntactic_category="Time"/>
		<suffixes>
			<inflectionalSuffix actual="" application="" form="" id="A3Sg_Noun" matched_word="sabah" name="A3sg" word="sabah"/>
			<inflectionalSuffix actual="" application="" form="" id="Pnon_Noun" matched_word="sabah" name="Pnon" word="sabah"/>
			<inflectionalSuffix actual="" application="" form="" id="Nom_Deriv_Noun" matched_word="sabah" name="Nom" word="sabah"/>
			<derivationalSuffix actual="çı" application="çı" form="cI" id="Agt_Noun" matched_word="sabahçı" name="Agt" to="Noun" word="sabahçı"/>
			<inflectionalSuffix actual="" application="" form="" id="A3Sg_Noun" matched_word="sabahçı" name="A3sg" word="sabahçı"/>
			<inflectionalSuffix actual="" application="" form="" id="Pnon_Noun" matched_word="sabahçı" name="Pnon" word="sabahçı"/>
			<inflectionalSuffix actual="" application="" form="" id="Nom_Noun" matched_word="sabahçı" name="Nom" word="sabahçı"/>
		</suffixes>
	</word>
	<word parse_result="sabah+Noun+Time+A3sg+Pnon+Nom" syntactic_category="Noun" secondary_syntactic_category="Time" str="sabah">
		<stem lemma="sabah" lemma_root="sabah" syntactic_category="Noun" root="sabah" secondary_syntactic_category="Time"/>
		<suffixes>
			<inflectionalSuffix actual="" application="" form="" id="A3Sg_Noun" matched_word="sabah" name="A3sg" word="sabah"/>
			<inflectionalSuffix actual="" application="" form="" id="Pnon_Noun" matched_word="sabah" name="Pnon" word="sabah"/>
			<inflectionalSuffix actual="" application="" form="" id="Nom_Noun" matched_word="sabah" name="Nom" word="sabah"/>
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
