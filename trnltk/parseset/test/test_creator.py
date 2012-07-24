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
        tokens.append(self._get_word_token_tuple(u'elmadan'))
        tokens.append(self._get_word_token_tuple(u'abcabcabc'))
        tokens.append(self._get_word_token_tuple(u'buyurmam'))
        tokens.append(self._get_word_token_tuple(u'yetiştirdik'))

        sentence = self.parseset_creator.create_sentence_binding_from_tokens(tokens)

        expected = u'''
<sentence>
	<unparsable_word str="blablabla"/>
	<word parse_result="elma(elma)+Noun+A3sg+Pnon+Abl(dAn[dan])" str="elmadan">
		<stem lemma="elma" primary_position="Noun" root="elma" secondary_position=""/>
		<suffixes>
			<inflectionalSuffix application="" form="" id="A3Sg_Noun" name="A3sg"/>
			<inflectionalSuffix application="" form="" id="Pnon_Noun" name="Pnon"/>
			<inflectionalSuffix application="dan" form="dAn" id="Abl_Noun" name="Abl"/>
		</suffixes>
	</word>
	<unparsable_word str="abcabcabc"/>
	<word parse_result="buyur(buyurmak)+Verb+Neg(mA[ma])+Aor+A1sg(+Im[m])" str="buyurmam">
		<stem lemma="buyurmak" primary_position="Verb" root="buyur" secondary_position=""/>
		<suffixes>
			<inflectionalSuffix application="ma" form="mA" id="Neg" name="Neg"/>
			<inflectionalSuffix application="" form="" id="Aor" name="Aor"/>
			<inflectionalSuffix application="m" form="+Im" id="A1Sg_Verb" name="A1sg"/>
		</suffixes>
	</word>
	<word parse_result="yetiş(yetişmek)+Verb+Verb+Caus(dIr[tir])+Pos+Past(dI[di])+A1pl(k[k])" str="yetiştirdik">
		<stem lemma="yetişmek" primary_position="Verb" root="yetiş" secondary_position=""/>
		<suffixes>
			<derivationalSuffix application="tir" form="dIr" id="Caus" name="Caus" to="Verb"/>
			<inflectionalSuffix application="" form="" id="Pos" name="Pos"/>
			<inflectionalSuffix application="di" form="dI" id="Past" name="Past"/>
			<inflectionalSuffix application="k" form="k" id="A1Pl_Verb" name="A1pl"/>
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
