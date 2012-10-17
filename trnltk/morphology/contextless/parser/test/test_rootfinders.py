# coding=utf-8
import unittest
from hamcrest import *
from mock import Mock
from trnltk.morphology.model.lexeme import SecondarySyntacticCategory, SyntacticCategory
from trnltk.morphology.contextless.parser.rootfinder import DigitNumeralRootFinder, ProperNounFromApostropheRootFinder, ProperNounWithoutApostropheRootFinder, WordRootFinder, TextNumeralRootFinder

class WordRootFinderTest(unittest.TestCase):

    def setUp(self):
        mock_lexeme1_1 = Mock()
        mock_lexeme1_2 = Mock()
        mock_lexeme2_1 = Mock()
        mock_lexeme2_2 = Mock()

        mock_lexeme1_1.syntactic_category = SyntacticCategory.NOUN
        mock_lexeme1_2.syntactic_category = SyntacticCategory.NOUN
        mock_lexeme2_1.syntactic_category = SyntacticCategory.NOUN
        mock_lexeme2_2.syntactic_category = SyntacticCategory.NUMERAL

        self.mock_root1_1 = Mock()
        self.mock_root1_2 = Mock()
        self.mock_root2_1 = Mock()
        self.mock_root2_2 = Mock()

        self.mock_root1_1.lexeme = mock_lexeme1_1
        self.mock_root1_2.lexeme = mock_lexeme1_2
        self.mock_root2_1.lexeme = mock_lexeme2_1
        self.mock_root2_2.lexeme = mock_lexeme2_2

        lexeme_map = {u'root1' : [self.mock_root1_1, self.mock_root1_2], u'root2': [self.mock_root2_1, self.mock_root2_2]}

        self.root_finder = WordRootFinder(lexeme_map)

    def test_should_find_roots(self):
        roots = self.root_finder.find_roots_for_partial_input(u"root1")
        assert_that(roots, has_length(2))
        assert_that(roots, has_items(self.mock_root1_1, self.mock_root1_2))

        roots = self.root_finder.find_roots_for_partial_input(u"root2")
        assert_that(roots, has_length(1))
        assert_that(roots, has_items(self.mock_root2_1))

        roots = self.root_finder.find_roots_for_partial_input(u"UNDEFINED")
        assert_that(roots, has_length(0))

class TextNumeralRootFinderTest(unittest.TestCase):

    def setUp(self):
        mock_lexeme1_1 = Mock()
        mock_lexeme1_2 = Mock()
        mock_lexeme2_1 = Mock()
        mock_lexeme2_2 = Mock()

        mock_lexeme1_1.syntactic_category = SyntacticCategory.NUMERAL
        mock_lexeme1_2.syntactic_category = SyntacticCategory.NUMERAL
        mock_lexeme2_1.syntactic_category = SyntacticCategory.NUMERAL
        mock_lexeme2_2.syntactic_category = SyntacticCategory.NOUN

        self.mock_root1_1 = Mock()
        self.mock_root1_2 = Mock()
        self.mock_root2_1 = Mock()
        self.mock_root2_2 = Mock()

        self.mock_root1_1.lexeme = mock_lexeme1_1
        self.mock_root1_2.lexeme = mock_lexeme1_2
        self.mock_root2_1.lexeme = mock_lexeme2_1
        self.mock_root2_2.lexeme = mock_lexeme2_2

        lexeme_map = {u'root1' : [self.mock_root1_1, self.mock_root1_2], u'root2': [self.mock_root2_1, self.mock_root2_2]}

        self.root_finder = TextNumeralRootFinder(lexeme_map)

    def test_should_find_roots(self):
        roots = self.root_finder.find_roots_for_partial_input(u"root1")
        assert_that(roots, has_length(2))
        assert_that(roots, has_items(self.mock_root1_1, self.mock_root1_2))

        roots = self.root_finder.find_roots_for_partial_input(u"root2")
        assert_that(roots, has_length(1))
        assert_that(roots, has_items(self.mock_root2_1))

        roots = self.root_finder.find_roots_for_partial_input(u"UNDEFINED")
        assert_that(roots, has_length(0))

class DigitNumeralRootFinderTest(unittest.TestCase):

    def setUp(self):
        self.root_finder = DigitNumeralRootFinder()

    def test_should_recognize_number_roots(self):
        roots = self.root_finder.find_roots_for_partial_input('3')
        assert_that(roots[0].str, equal_to('3'))

        roots = self.root_finder.find_roots_for_partial_input('0')
        assert_that(roots[0].str, equal_to('0'))

        roots = self.root_finder.find_roots_for_partial_input('-1')
        assert_that(roots[0].str, equal_to('-1'))

        roots = self.root_finder.find_roots_for_partial_input('+3')
        assert_that(roots[0].str, equal_to('+3'))

        roots = self.root_finder.find_roots_for_partial_input('3,5')
        assert_that(roots[0].str, equal_to('3,5'))

        roots = self.root_finder.find_roots_for_partial_input('-999999999999,12345678901')
        assert_that(roots[0].str, equal_to('-999999999999,12345678901'))

        roots = self.root_finder.find_roots_for_partial_input('+2.999.999.999.999,12345678901')
        assert_that(roots[0].str, equal_to('+2.999.999.999.999,12345678901'))

class ProperNounFromApostropheRootFinderTest(unittest.TestCase):

    def setUp(self):
        self.root_finder = ProperNounFromApostropheRootFinder()

    def test_should_recognize_abbreviations(self):
        roots = self.root_finder.find_roots_for_partial_input(u"TR'")
        assert_that(roots[0].str, equal_to(u'TR'))
        assert_that(roots[0].lexeme.secondary_syntactic_category, equal_to(SecondarySyntacticCategory.ABBREVIATION))

        roots = self.root_finder.find_roots_for_partial_input(u"MB'")
        assert_that(roots[0].str, equal_to(u'MB'))
        assert_that(roots[0].lexeme.secondary_syntactic_category, equal_to(SecondarySyntacticCategory.ABBREVIATION))

        roots = self.root_finder.find_roots_for_partial_input(u"POL'")
        assert_that(roots[0].str, equal_to(u'POL'))
        assert_that(roots[0].lexeme.secondary_syntactic_category, equal_to(SecondarySyntacticCategory.ABBREVIATION))

        roots = self.root_finder.find_roots_for_partial_input(u"KAFA1500'")
        assert_that(roots[0].str, equal_to(u'KAFA1500'))
        assert_that(roots[0].lexeme.secondary_syntactic_category, equal_to(SecondarySyntacticCategory.ABBREVIATION))

        roots = self.root_finder.find_roots_for_partial_input(u"1500KAFA'")
        assert_that(roots[0].str, equal_to(u'1500KAFA'))
        assert_that(roots[0].lexeme.secondary_syntactic_category, equal_to(SecondarySyntacticCategory.ABBREVIATION))

        roots = self.root_finder.find_roots_for_partial_input(u"İŞÇĞÜÖ'")
        assert_that(roots[0].str, equal_to(u'İŞÇĞÜÖ'))
        assert_that(roots[0].lexeme.secondary_syntactic_category, equal_to(SecondarySyntacticCategory.ABBREVIATION))

        roots = self.root_finder.find_roots_for_partial_input(u"123'")
        assert_that(roots, has_length(0))


    def test_should_recognize_proper_nouns(self):
        roots = self.root_finder.find_roots_for_partial_input(u"Ahmet'")
        assert_that(roots[0].str, equal_to(u'Ahmet'))
        assert_that(roots[0].lexeme.secondary_syntactic_category, equal_to(SecondarySyntacticCategory.PROPER_NOUN))

        roots = self.root_finder.find_roots_for_partial_input(u"Mehmed'")
        assert_that(roots[0].str, equal_to(u'Mehmed'))
        assert_that(roots[0].lexeme.secondary_syntactic_category, equal_to(SecondarySyntacticCategory.PROPER_NOUN))

        roots = self.root_finder.find_roots_for_partial_input(u"A123a'")
        assert_that(roots[0].str, equal_to(u'A123a'))
        assert_that(roots[0].lexeme.secondary_syntactic_category, equal_to(SecondarySyntacticCategory.PROPER_NOUN))

        roots = self.root_finder.find_roots_for_partial_input(u"AvA'")
        assert_that(roots[0].str, equal_to(u'AvA'))
        assert_that(roots[0].lexeme.secondary_syntactic_category, equal_to(SecondarySyntacticCategory.PROPER_NOUN))

        roots = self.root_finder.find_roots_for_partial_input(u"AAxxAA'")
        assert_that(roots[0].str, equal_to(u'AAxxAA'))
        assert_that(roots[0].lexeme.secondary_syntactic_category, equal_to(SecondarySyntacticCategory.PROPER_NOUN))

        roots = self.root_finder.find_roots_for_partial_input(u"İstanbul'")
        assert_that(roots[0].str, equal_to(u'İstanbul'))
        assert_that(roots[0].lexeme.secondary_syntactic_category, equal_to(SecondarySyntacticCategory.PROPER_NOUN))

        roots = self.root_finder.find_roots_for_partial_input(u"Çanakkale'")
        assert_that(roots[0].str, equal_to(u'Çanakkale'))
        assert_that(roots[0].lexeme.secondary_syntactic_category, equal_to(SecondarySyntacticCategory.PROPER_NOUN))

        roots = self.root_finder.find_roots_for_partial_input(u"Ömer'")
        assert_that(roots[0].str, equal_to(u'Ömer'))
        assert_that(roots[0].lexeme.secondary_syntactic_category, equal_to(SecondarySyntacticCategory.PROPER_NOUN))

        roots = self.root_finder.find_roots_for_partial_input(u"Şaban'")
        assert_that(roots[0].str, equal_to(u'Şaban'))
        assert_that(roots[0].lexeme.secondary_syntactic_category, equal_to(SecondarySyntacticCategory.PROPER_NOUN))

        roots = self.root_finder.find_roots_for_partial_input(u"Ümmühan'")
        assert_that(roots[0].str, equal_to(u'Ümmühan'))
        assert_that(roots[0].lexeme.secondary_syntactic_category, equal_to(SecondarySyntacticCategory.PROPER_NOUN))

        roots = self.root_finder.find_roots_for_partial_input(u"aaa'")
        assert_that(roots, has_length(0))

        roots = self.root_finder.find_roots_for_partial_input(u"aAAAA'")
        assert_that(roots, has_length(0))

        roots = self.root_finder.find_roots_for_partial_input(u"1aa'")
        assert_that(roots, has_length(0))

        roots = self.root_finder.find_roots_for_partial_input(u"a111'")
        assert_that(roots, has_length(0))

        roots = self.root_finder.find_roots_for_partial_input(u"şaa'")
        assert_that(roots, has_length(0))

class ProperNounWithoutApostropheRootFinderTest(unittest.TestCase):

    def setUp(self):
        self.root_finder = ProperNounWithoutApostropheRootFinder()

    def test_should_recognize_proper_nouns(self):
        roots = self.root_finder.find_roots_for_partial_input(u"A", u"Ali")
        assert_that(roots[0].str, equal_to(u'A'))
        assert_that(roots[0].lexeme.secondary_syntactic_category, equal_to(SecondarySyntacticCategory.PROPER_NOUN))

        roots = self.root_finder.find_roots_for_partial_input(u"Al", u"Ali")
        assert_that(roots[0].str, equal_to(u'Al'))
        assert_that(roots[0].lexeme.secondary_syntactic_category, equal_to(SecondarySyntacticCategory.PROPER_NOUN))

        roots = self.root_finder.find_roots_for_partial_input(u"Ali", u"Ali")
        assert_that(roots[0].str, equal_to(u'Ali'))
        assert_that(roots[0].lexeme.secondary_syntactic_category, equal_to(SecondarySyntacticCategory.PROPER_NOUN))

        roots = self.root_finder.find_roots_for_partial_input(u"Ali8", u"Ali8912")
        assert_that(roots[0].str, equal_to(u'Ali8'))
        assert_that(roots[0].lexeme.secondary_syntactic_category, equal_to(SecondarySyntacticCategory.PROPER_NOUN))

    def test_should_not_recognize_proper_nouns_when_the_input_is_not(self):
        roots = self.root_finder.find_roots_for_partial_input(u"A", u"Ali'nin")
        assert_that(roots, has_length(0))

        roots = self.root_finder.find_roots_for_partial_input(u"Al", u"Ali'nin")
        assert_that(roots, has_length(0))

        roots = self.root_finder.find_roots_for_partial_input(u"Ali", u"Ali'nin")
        assert_that(roots, has_length(0))

        roots = self.root_finder.find_roots_for_partial_input(u"Ali8", u"Ali8912'nin")
        assert_that(roots, has_length(0))

        roots = self.root_finder.find_roots_for_partial_input(u"a", u"aa")
        assert_that(roots, has_length(0))

        roots = self.root_finder.find_roots_for_partial_input(u"Ali'nin", u"Ali'nin")
        assert_that(roots, has_length(0))

        roots = self.root_finder.find_roots_for_partial_input(u"123A", u"123A")
        assert_that(roots, has_length(0))



if __name__ == '__main__':
    unittest.main()
