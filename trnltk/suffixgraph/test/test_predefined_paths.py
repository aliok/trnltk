# coding=utf-8
import os
import unittest
from hamcrest import *
from hamcrest.core.base_matcher import BaseMatcher
from trnltk.stem.dictionaryitem import  PrimaryPosition, SecondaryPosition
from trnltk.stem.dictionaryloader import DictionaryLoader
from trnltk.stem.stemgenerator import StemGenerator
from trnltk.suffixgraph.predefinedpaths import PredefinedPaths

class ParserTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(ParserTest, cls).setUpClass()
        cls.all_stems = []

        dictionary_items = DictionaryLoader.load_from_file(os.path.join(os.path.dirname(__file__), '../../resources/master_dictionary.txt'))
        for di in dictionary_items:
            if di.primary_position in [
                PrimaryPosition.NOUN, PrimaryPosition.VERB, PrimaryPosition.ADVERB,
                PrimaryPosition.ADJECTIVE, PrimaryPosition.PRONOUN,
                PrimaryPosition.DETERMINER, PrimaryPosition.INTERJECTION, PrimaryPosition.CONJUNCTION,
                PrimaryPosition.NUMERAL, PrimaryPosition.PUNCTUATION]:
                cls.all_stems.extend(StemGenerator.generate(di))

        predefinedPaths = PredefinedPaths(cls.all_stems)
        predefinedPaths.create_predefined_paths()

        cls.predefined_paths = predefinedPaths.token_map

    def test_should_have_paths_for_personal_pronouns(self):
        PRON = PrimaryPosition.PRONOUN
        PERS = SecondaryPosition.PERSONAL

        # last one ends with transition to derivation state
        self.assert_defined_path(u'ben', PRON, PERS,
            u'ben(ben)+Pron+Pers+A1sg+Pnon+Nom',
            u'ben(ben)+Pron+Pers+A1sg+Pnon+Acc(i[i])',
            u'ben(ben)+Pron+Pers+A1sg+Pnon+Loc(de[de])',
            u'ben(ben)+Pron+Pers+A1sg+Pnon+Abl(den[den])',
            u'ben(ben)+Pron+Pers+A1sg+Pnon+Ins(le[le])',
            u'ben(ben)+Pron+Pers+A1sg+Pnon+Ins(imle[imle])',
            u'ben(ben)+Pron+Pers+A1sg+Pnon+Gen(im[im])',
            u'ben(ben)+Pron+Pers+A1sg+Pnon+Nom')

        self.assert_defined_path(u'ban', PRON, PERS,
            u'ban(ben)+Pron+Pers+A1sg+Pnon+Dat(a[a])')

        # last one ends with transition to derivation state
        self.assert_defined_path(u'sen', PRON, PERS,
            u'sen(sen)+Pron+Pers+A2sg+Pnon+Nom',
            u'sen(sen)+Pron+Pers+A2sg+Pnon+Acc(i[i])',
            u'sen(sen)+Pron+Pers+A2sg+Pnon+Loc(de[de])',
            u'sen(sen)+Pron+Pers+A2sg+Pnon+Abl(den[den])',
            u'sen(sen)+Pron+Pers+A2sg+Pnon+Ins(le[le])',
            u'sen(sen)+Pron+Pers+A2sg+Pnon+Ins(inle[inle])',
            u'sen(sen)+Pron+Pers+A2sg+Pnon+Gen(in[in])',
            u'sen(sen)+Pron+Pers+A2sg+Pnon+Nom')

        self.assert_defined_path(u'san', PRON, PERS,
            u'san(sen)+Pron+Pers+A2sg+Pnon+Dat(a[a])')


    def assert_defined_path(self, stem_root, primary_position, secondary_position, *args):
        assert_that(self.predefined_tokens(stem_root, primary_position, secondary_position), IsTokensMatches([a for a in args]))

    def predefined_tokens(self, stem_root, primary_position, secondary_position):
        predefined_tokens = []
        for stem in self.predefined_paths.keys():
            if stem.root==stem_root and stem.dictionary_item.primary_position==primary_position and stem.dictionary_item.secondary_position==secondary_position:
                predefined_tokens.extend(self.predefined_paths[stem])

        return [r.to_pretty_str() for r in predefined_tokens]


class IsTokensMatches(BaseMatcher):
    def __init__(self, expected_results):
        self.expected_results = expected_results

    def _matches(self, item):
        return item == self.expected_results

    def describe_to(self, description):
        description.append_text(u'     ' + str(self.expected_results))

if __name__ == '__main__':
    unittest.main()
