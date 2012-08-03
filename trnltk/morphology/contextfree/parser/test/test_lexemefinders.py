# coding=utf-8
import unittest
from hamcrest.core.assert_that import *
from hamcrest.core.core.isequal import equal_to
from hamcrest.library.object.haslength import has_length
from trnltk.morphology.model.lexeme import SecondarySyntacticCategory
from trnltk.morphology.contextfree.parser.lexemefinder import NumeralLexemeFinder, ProperNounFromApostropheLexemeFinder, ProperNounWithoutApostropheLexemeFinder

class NumeralLexemeFinderTest(unittest.TestCase):

    def setUp(self):
        self.lexeme_finder = NumeralLexemeFinder()

    def test_should_recognize_number_roots(self):
        lexemes = self.lexeme_finder.find_lexeme_for_partial_input('3')
        assert_that(lexemes[0].str, equal_to('3'))

        lexemes = self.lexeme_finder.find_lexeme_for_partial_input('0')
        assert_that(lexemes[0].str, equal_to('0'))

        lexemes = self.lexeme_finder.find_lexeme_for_partial_input('-1')
        assert_that(lexemes[0].str, equal_to('-1'))

        lexemes = self.lexeme_finder.find_lexeme_for_partial_input('+3')
        assert_that(lexemes[0].str, equal_to('+3'))

        lexemes = self.lexeme_finder.find_lexeme_for_partial_input('3,5')
        assert_that(lexemes[0].str, equal_to('3,5'))

        lexemes = self.lexeme_finder.find_lexeme_for_partial_input('-999999999999,12345678901')
        assert_that(lexemes[0].str, equal_to('-999999999999,12345678901'))

        lexemes = self.lexeme_finder.find_lexeme_for_partial_input('+2.999.999.999.999,12345678901')
        assert_that(lexemes[0].str, equal_to('+2.999.999.999.999,12345678901'))

class ProperNounFromApostropheLexemeFinderTest(unittest.TestCase):

    def setUp(self):
        self.lexeme_finder = ProperNounFromApostropheLexemeFinder()

    def test_should_recognize_abbreviations(self):
        lexemes = self.lexeme_finder.find_lexeme_for_partial_input(u"TR'")
        assert_that(lexemes[0].str, equal_to(u'TR'))
        assert_that(lexemes[0].lexeme.secondary_syntactic_category, equal_to(SecondarySyntacticCategory.ABBREVIATION))

        lexemes = self.lexeme_finder.find_lexeme_for_partial_input(u"MB'")
        assert_that(lexemes[0].str, equal_to(u'MB'))
        assert_that(lexemes[0].lexeme.secondary_syntactic_category, equal_to(SecondarySyntacticCategory.ABBREVIATION))

        lexemes = self.lexeme_finder.find_lexeme_for_partial_input(u"POL'")
        assert_that(lexemes[0].str, equal_to(u'POL'))
        assert_that(lexemes[0].lexeme.secondary_syntactic_category, equal_to(SecondarySyntacticCategory.ABBREVIATION))

        lexemes = self.lexeme_finder.find_lexeme_for_partial_input(u"KAFA1500'")
        assert_that(lexemes[0].str, equal_to(u'KAFA1500'))
        assert_that(lexemes[0].lexeme.secondary_syntactic_category, equal_to(SecondarySyntacticCategory.ABBREVIATION))

        lexemes = self.lexeme_finder.find_lexeme_for_partial_input(u"1500KAFA'")
        assert_that(lexemes[0].str, equal_to(u'1500KAFA'))
        assert_that(lexemes[0].lexeme.secondary_syntactic_category, equal_to(SecondarySyntacticCategory.ABBREVIATION))

        lexemes = self.lexeme_finder.find_lexeme_for_partial_input(u"İŞÇĞÜÖ'")
        assert_that(lexemes[0].str, equal_to(u'İŞÇĞÜÖ'))
        assert_that(lexemes[0].lexeme.secondary_syntactic_category, equal_to(SecondarySyntacticCategory.ABBREVIATION))

        lexemes = self.lexeme_finder.find_lexeme_for_partial_input(u"123'")
        assert_that(lexemes, has_length(0))


    def test_should_recognize_proper_nouns(self):
        lexemes = self.lexeme_finder.find_lexeme_for_partial_input(u"Ahmet'")
        assert_that(lexemes[0].str, equal_to(u'Ahmet'))
        assert_that(lexemes[0].lexeme.secondary_syntactic_category, equal_to(SecondarySyntacticCategory.PROPER_NOUN))

        lexemes = self.lexeme_finder.find_lexeme_for_partial_input(u"Mehmed'")
        assert_that(lexemes[0].str, equal_to(u'Mehmed'))
        assert_that(lexemes[0].lexeme.secondary_syntactic_category, equal_to(SecondarySyntacticCategory.PROPER_NOUN))

        lexemes = self.lexeme_finder.find_lexeme_for_partial_input(u"A123a'")
        assert_that(lexemes[0].str, equal_to(u'A123a'))
        assert_that(lexemes[0].lexeme.secondary_syntactic_category, equal_to(SecondarySyntacticCategory.PROPER_NOUN))

        lexemes = self.lexeme_finder.find_lexeme_for_partial_input(u"AvA'")
        assert_that(lexemes[0].str, equal_to(u'AvA'))
        assert_that(lexemes[0].lexeme.secondary_syntactic_category, equal_to(SecondarySyntacticCategory.PROPER_NOUN))

        lexemes = self.lexeme_finder.find_lexeme_for_partial_input(u"AAxxAA'")
        assert_that(lexemes[0].str, equal_to(u'AAxxAA'))
        assert_that(lexemes[0].lexeme.secondary_syntactic_category, equal_to(SecondarySyntacticCategory.PROPER_NOUN))

        lexemes = self.lexeme_finder.find_lexeme_for_partial_input(u"İstanbul'")
        assert_that(lexemes[0].str, equal_to(u'İstanbul'))
        assert_that(lexemes[0].lexeme.secondary_syntactic_category, equal_to(SecondarySyntacticCategory.PROPER_NOUN))

        lexemes = self.lexeme_finder.find_lexeme_for_partial_input(u"Çanakkale'")
        assert_that(lexemes[0].str, equal_to(u'Çanakkale'))
        assert_that(lexemes[0].lexeme.secondary_syntactic_category, equal_to(SecondarySyntacticCategory.PROPER_NOUN))

        lexemes = self.lexeme_finder.find_lexeme_for_partial_input(u"Ömer'")
        assert_that(lexemes[0].str, equal_to(u'Ömer'))
        assert_that(lexemes[0].lexeme.secondary_syntactic_category, equal_to(SecondarySyntacticCategory.PROPER_NOUN))

        lexemes = self.lexeme_finder.find_lexeme_for_partial_input(u"Şaban'")
        assert_that(lexemes[0].str, equal_to(u'Şaban'))
        assert_that(lexemes[0].lexeme.secondary_syntactic_category, equal_to(SecondarySyntacticCategory.PROPER_NOUN))

        lexemes = self.lexeme_finder.find_lexeme_for_partial_input(u"Ümmühan'")
        assert_that(lexemes[0].str, equal_to(u'Ümmühan'))
        assert_that(lexemes[0].lexeme.secondary_syntactic_category, equal_to(SecondarySyntacticCategory.PROPER_NOUN))

        lexemes = self.lexeme_finder.find_lexeme_for_partial_input(u"aaa'")
        assert_that(lexemes, has_length(0))

        lexemes = self.lexeme_finder.find_lexeme_for_partial_input(u"aAAAA'")
        assert_that(lexemes, has_length(0))

        lexemes = self.lexeme_finder.find_lexeme_for_partial_input(u"1aa'")
        assert_that(lexemes, has_length(0))

        lexemes = self.lexeme_finder.find_lexeme_for_partial_input(u"a111'")
        assert_that(lexemes, has_length(0))

        lexemes = self.lexeme_finder.find_lexeme_for_partial_input(u"şaa'")
        assert_that(lexemes, has_length(0))

class ProperNounWithoutApostropheLexemeFinderTest(unittest.TestCase):

    def setUp(self):
        self.lexeme_finder = ProperNounWithoutApostropheLexemeFinder()

    def test_should_recognize_proper_nouns(self):
        lexemes = self.lexeme_finder.find_lexeme_for_partial_input(u"A")
        assert_that(lexemes[0].str, equal_to(u'A'))
        assert_that(lexemes[0].lexeme.secondary_syntactic_category, equal_to(SecondarySyntacticCategory.PROPER_NOUN))

        lexemes = self.lexeme_finder.find_lexeme_for_partial_input(u"Al")
        assert_that(lexemes[0].str, equal_to(u'Al'))
        assert_that(lexemes[0].lexeme.secondary_syntactic_category, equal_to(SecondarySyntacticCategory.PROPER_NOUN))

        lexemes = self.lexeme_finder.find_lexeme_for_partial_input(u"Ali")
        assert_that(lexemes[0].str, equal_to(u'Ali'))
        assert_that(lexemes[0].lexeme.secondary_syntactic_category, equal_to(SecondarySyntacticCategory.PROPER_NOUN))

        lexemes = self.lexeme_finder.find_lexeme_for_partial_input(u"Ali8")
        assert_that(lexemes[0].str, equal_to(u'Ali8'))
        assert_that(lexemes[0].lexeme.secondary_syntactic_category, equal_to(SecondarySyntacticCategory.PROPER_NOUN))

        lexemes = self.lexeme_finder.find_lexeme_for_partial_input(u"a")
        assert_that(lexemes, has_length(0))

        lexemes = self.lexeme_finder.find_lexeme_for_partial_input(u"Ali'nin")
        assert_that(lexemes, has_length(0))

        lexemes = self.lexeme_finder.find_lexeme_for_partial_input(u"123A")
        assert_that(lexemes, has_length(0))

if __name__ == '__main__':
    unittest.main()
