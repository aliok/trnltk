# coding=utf-8
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

        sentence = self.parseset_creator.create_sentence_binding_from_tokens(tokens)

        expected = '''
<sentence>
	<unparsable_word str="blablabla"/>
	<word parse_result="elma(elma)+Noun+A3sg+Pnon+Abl(dAn[dan])" str="elmadan">
		<stem lemma="elma" primary_position="Noun" root="elma" secondary_position=""/>
		<suffixes>
			<suffix application="" form="" name="A3Sg_Noun"/>
			<suffix application="" form="" name="Pnon_Noun"/>
			<suffix application="dan" form="dAn" name="Abl_Noun"/>
			<suffix application="" form="" name="Noun_Free_Transition_1"/>
			<suffix application="" form="" name="Noun_Free_Transition_2"/>
		</suffixes>
	</word>
	<unparsable_word str="abcabcabc"/>
	<word parse_result="buyur(buyurmak)+Verb+Neg(mA[ma])+Aor+A1sg(+Im[m])" str="buyurmam">
		<stem lemma="buyurmak" primary_position="Verb" root="buyur" secondary_position=""/>
		<suffixes>
			<suffix application="ma" form="mA" name="Neg"/>
			<suffix application="" form="" name="Aor"/>
			<suffix application="m" form="+Im" name="A1Sg_Verb"/>
			<suffix application="" form="" name="Verb_Free_Transition_4"/>
		</suffixes>
	</word>
</sentence>
'''
        expected = expected.strip()

        assert_that(expected, equal_to(sentence.to_dom().toprettyxml().strip()))

    def _get_word_token_tuple(self, seq):
        res = self.parser.parse(seq)
        if res:
            return (seq, res[0])
        else:
            return (seq, None)

if __name__ == '__main__':
    unittest.main()
