# coding=utf-8
import os
import unittest
from hamcrest import *
from hamcrest.core.base_matcher import BaseMatcher
from trnltk.stem.dictionaryitem import  PrimaryPosition
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
        predefinedPaths.define_predefined_paths()

        cls.predefined_paths = predefinedPaths.token_map

    def test_should_have_paths_for_personal_pronouns(self):
        self.assert_defined_path(u'ben', u'ben(ben)+Pron+Pers+A1sg+Pnon+Nom', u'ben(ben)+Pron+Pers+A1sg+Pnon+Nom') # second one ends derivation state
        self.assert_defined_path(u'bana', u'ban(ben)+Pron+Pers+A1sg+Pnon+Dat(a[a])')
        self.assert_defined_path(u'beni', u'ben(ben)+Pron+Pers+A1sg+Pnon+Acc(i[i])')


    def assert_defined_path(self, word_to_parse, *args):
        assert_that(self.predefined_tokens(word_to_parse), IsParseResultMatches([a for a in args]))

    def predefined_tokens(self, word):
        return [r.to_pretty_str() for r in self.predefined_paths[word]]


class IsParseResultMatches(BaseMatcher):
    def __init__(self, expected_results):
        self.expected_results = expected_results

    def _matches(self, item):
        return item == self.expected_results

    def describe_to(self, description):
        description.append_text(u'     ' + str(self.expected_results))

if __name__ == '__main__':
    unittest.main()
