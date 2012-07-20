# coding=utf-8
import unittest
from hamcrest.core.assert_that import *
from hamcrest.core.core.isequal import equal_to
from hamcrest.library.object.haslength import has_length
from trnltk.stem.dictionaryitem import SecondaryPosition
from trnltk.parser.stemfinder import NumeralStemFinder, ProperNounFromApostropheStemFinder, ProperNounWithoutApostropheStemFinder

class NumeralStemFinderTest(unittest.TestCase):

    def setUp(self):
        self.stem_finder = NumeralStemFinder()

    def test_should_recognize_number_stems(self):
        stems = self.stem_finder.find_stem_for_partial_input('3')
        assert_that(stems[0].root, equal_to('3'))

        stems = self.stem_finder.find_stem_for_partial_input('0')
        assert_that(stems[0].root, equal_to('0'))

        stems = self.stem_finder.find_stem_for_partial_input('-1')
        assert_that(stems[0].root, equal_to('-1'))

        stems = self.stem_finder.find_stem_for_partial_input('+3')
        assert_that(stems[0].root, equal_to('+3'))

        stems = self.stem_finder.find_stem_for_partial_input('3,5')
        assert_that(stems[0].root, equal_to('3,5'))

        stems = self.stem_finder.find_stem_for_partial_input('-999999999999,12345678901')
        assert_that(stems[0].root, equal_to('-999999999999,12345678901'))

        stems = self.stem_finder.find_stem_for_partial_input('+2.999.999.999.999,12345678901')
        assert_that(stems[0].root, equal_to('+2.999.999.999.999,12345678901'))

class ProperNounFromApostropheStemFinderTest(unittest.TestCase):

    def setUp(self):
        self.stem_finder = ProperNounFromApostropheStemFinder()

    def test_should_recognize_abbreviations(self):
        stems = self.stem_finder.find_stem_for_partial_input(u"TR'")
        assert_that(stems[0].root, equal_to(u'TR'))
        assert_that(stems[0].dictionary_item.secondary_position, equal_to(SecondaryPosition.ABBREVIATION))

        stems = self.stem_finder.find_stem_for_partial_input(u"MB'")
        assert_that(stems[0].root, equal_to(u'MB'))
        assert_that(stems[0].dictionary_item.secondary_position, equal_to(SecondaryPosition.ABBREVIATION))

        stems = self.stem_finder.find_stem_for_partial_input(u"POL'")
        assert_that(stems[0].root, equal_to(u'POL'))
        assert_that(stems[0].dictionary_item.secondary_position, equal_to(SecondaryPosition.ABBREVIATION))

        stems = self.stem_finder.find_stem_for_partial_input(u"KAFA1500'")
        assert_that(stems[0].root, equal_to(u'KAFA1500'))
        assert_that(stems[0].dictionary_item.secondary_position, equal_to(SecondaryPosition.ABBREVIATION))

        stems = self.stem_finder.find_stem_for_partial_input(u"1500KAFA'")
        assert_that(stems[0].root, equal_to(u'1500KAFA'))
        assert_that(stems[0].dictionary_item.secondary_position, equal_to(SecondaryPosition.ABBREVIATION))

        stems = self.stem_finder.find_stem_for_partial_input(u"İŞÇĞÜÖ'")
        assert_that(stems[0].root, equal_to(u'İŞÇĞÜÖ'))
        assert_that(stems[0].dictionary_item.secondary_position, equal_to(SecondaryPosition.ABBREVIATION))

        stems = self.stem_finder.find_stem_for_partial_input(u"123'")
        assert_that(stems, has_length(0))


    def test_should_recognize_proper_nouns(self):
        stems = self.stem_finder.find_stem_for_partial_input(u"Ahmet'")
        assert_that(stems[0].root, equal_to(u'Ahmet'))
        assert_that(stems[0].dictionary_item.secondary_position, equal_to(SecondaryPosition.PROPER_NOUN))

        stems = self.stem_finder.find_stem_for_partial_input(u"Mehmed'")
        assert_that(stems[0].root, equal_to(u'Mehmed'))
        assert_that(stems[0].dictionary_item.secondary_position, equal_to(SecondaryPosition.PROPER_NOUN))

        stems = self.stem_finder.find_stem_for_partial_input(u"A123a'")
        assert_that(stems[0].root, equal_to(u'A123a'))
        assert_that(stems[0].dictionary_item.secondary_position, equal_to(SecondaryPosition.PROPER_NOUN))

        stems = self.stem_finder.find_stem_for_partial_input(u"AvA'")
        assert_that(stems[0].root, equal_to(u'AvA'))
        assert_that(stems[0].dictionary_item.secondary_position, equal_to(SecondaryPosition.PROPER_NOUN))

        stems = self.stem_finder.find_stem_for_partial_input(u"AAxxAA'")
        assert_that(stems[0].root, equal_to(u'AAxxAA'))
        assert_that(stems[0].dictionary_item.secondary_position, equal_to(SecondaryPosition.PROPER_NOUN))

        stems = self.stem_finder.find_stem_for_partial_input(u"İstanbul'")
        assert_that(stems[0].root, equal_to(u'İstanbul'))
        assert_that(stems[0].dictionary_item.secondary_position, equal_to(SecondaryPosition.PROPER_NOUN))

        stems = self.stem_finder.find_stem_for_partial_input(u"Çanakkale'")
        assert_that(stems[0].root, equal_to(u'Çanakkale'))
        assert_that(stems[0].dictionary_item.secondary_position, equal_to(SecondaryPosition.PROPER_NOUN))

        stems = self.stem_finder.find_stem_for_partial_input(u"Ömer'")
        assert_that(stems[0].root, equal_to(u'Ömer'))
        assert_that(stems[0].dictionary_item.secondary_position, equal_to(SecondaryPosition.PROPER_NOUN))

        stems = self.stem_finder.find_stem_for_partial_input(u"Şaban'")
        assert_that(stems[0].root, equal_to(u'Şaban'))
        assert_that(stems[0].dictionary_item.secondary_position, equal_to(SecondaryPosition.PROPER_NOUN))

        stems = self.stem_finder.find_stem_for_partial_input(u"Ümmühan'")
        assert_that(stems[0].root, equal_to(u'Ümmühan'))
        assert_that(stems[0].dictionary_item.secondary_position, equal_to(SecondaryPosition.PROPER_NOUN))

        stems = self.stem_finder.find_stem_for_partial_input(u"aaa'")
        assert_that(stems, has_length(0))

        stems = self.stem_finder.find_stem_for_partial_input(u"aAAAA'")
        assert_that(stems, has_length(0))

        stems = self.stem_finder.find_stem_for_partial_input(u"1aa'")
        assert_that(stems, has_length(0))

        stems = self.stem_finder.find_stem_for_partial_input(u"a111'")
        assert_that(stems, has_length(0))

        stems = self.stem_finder.find_stem_for_partial_input(u"şaa'")
        assert_that(stems, has_length(0))

class ProperNounWithoutApostropheStemFinderTest(unittest.TestCase):

    def setUp(self):
        self.stem_finder = ProperNounWithoutApostropheStemFinder()

    def test_should_recognize_proper_nouns(self):
        stems = self.stem_finder.find_stem_for_partial_input(u"A")
        assert_that(stems[0].root, equal_to(u'A'))
        assert_that(stems[0].dictionary_item.secondary_position, equal_to(SecondaryPosition.PROPER_NOUN))

        stems = self.stem_finder.find_stem_for_partial_input(u"Al")
        assert_that(stems[0].root, equal_to(u'Al'))
        assert_that(stems[0].dictionary_item.secondary_position, equal_to(SecondaryPosition.PROPER_NOUN))

        stems = self.stem_finder.find_stem_for_partial_input(u"Ali")
        assert_that(stems[0].root, equal_to(u'Ali'))
        assert_that(stems[0].dictionary_item.secondary_position, equal_to(SecondaryPosition.PROPER_NOUN))

        stems = self.stem_finder.find_stem_for_partial_input(u"Ali8")
        assert_that(stems[0].root, equal_to(u'Ali8'))
        assert_that(stems[0].dictionary_item.secondary_position, equal_to(SecondaryPosition.PROPER_NOUN))

        stems = self.stem_finder.find_stem_for_partial_input(u"a")
        assert_that(stems, has_length(0))

        stems = self.stem_finder.find_stem_for_partial_input(u"Ali'nin")
        assert_that(stems, has_length(0))

        stems = self.stem_finder.find_stem_for_partial_input(u"123A")
        assert_that(stems, has_length(0))

if __name__ == '__main__':
    unittest.main()
