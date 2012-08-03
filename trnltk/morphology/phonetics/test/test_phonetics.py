# coding=utf-8
import unittest
from trnltk.morphology.stem.dictionaryitem import RootAttribute
from trnltk.morphology.phonetics.phonetics import Phonetics, PhoneticExpectation, PhoneticAttributes

ac = Phonetics.is_suffix_form_applicable
def ap(word, form_str, root_attributes=None):
    phonetic_attributes = Phonetics.calculate_phonetic_attributes(word, root_attributes)
    word, application = Phonetics.apply(word, phonetic_attributes, form_str, root_attributes)
    return word + application

def apnv(word, form_str):
    return ap(word, form_str, [RootAttribute.NoVoicing])

es = Phonetics.expectations_satisfied
V = PhoneticExpectation.VowelStart
C = PhoneticExpectation.ConsonantStart

cpa = Phonetics.calculate_phonetic_attributes_of_plain_sequence

am = Phonetics.application_matches

class PhoneticExpectationsTest(unittest.TestCase):
    def test_should_return_applicable(self):
        self.assertTrue(ac(u'elma', None))
        self.assertTrue(ac(u'elma', u''))
        self.assertTrue(ac(u'elma', u' '))
        self.assertTrue(ac(u'elma', u'lAr'))
        self.assertTrue(ac(u'elma', u'cI'))
        self.assertTrue(ac(u'elma', u'lAş'))
        self.assertTrue(ac(u'elma', u'dIr'))
        self.assertTrue(ac(u'elma', u'nIn'))
        self.assertTrue(ac(u'elma', u'+nIn'))
        self.assertTrue(ac(u'elma', u'+yI'))
        self.assertTrue(ac(u'elma', u'+sI'))
        self.assertTrue(ac(u'elma', u'+dAn'))
        self.assertTrue(ac(u'elma', u'+Im'))
        self.assertTrue(ac(u'elma', u'+ylA'))

        self.assertTrue(ac(u'armut', None))
        self.assertTrue(ac(u'armut', u''))
        self.assertTrue(ac(u'armut', u' '))
        self.assertTrue(ac(u'armut', u'lAr'))
        self.assertTrue(ac(u'armut', u'cI'))
        self.assertTrue(ac(u'armut', u'lAş'))
        self.assertTrue(ac(u'armut', u'dIr'))
        self.assertTrue(ac(u'armut', u'In'))
        self.assertTrue(ac(u'armut', u'+nIn'))
        self.assertTrue(ac(u'armut', u'+yI'))
        self.assertTrue(ac(u'armut', u'+sI'))
        self.assertTrue(ac(u'armut', u'+dAn'))
        self.assertTrue(ac(u'armut', u'+Im'))
        self.assertTrue(ac(u'armut', u'+ylA'))

        self.assertTrue(ac(u'yap', u'+yAcAk'))
        self.assertTrue(ac(u'yap', u'dIk'))
        self.assertTrue(ac(u'yap', u'm'))
        self.assertTrue(ac(u'yap', u'+IyOr'))
        self.assertTrue(ac(u'yap', u'+Ar'))

        self.assertTrue(ac(u'yapacak', u'+Im'))
        self.assertTrue(ac(u'yaptı', u'+Im'))
        self.assertTrue(ac(u'yapıyor', u'+Im'))
        self.assertTrue(ac(u'yapmakta', u'+yIm'))
        self.assertTrue(ac(u'yapmış', u'+Im'))

        self.assertTrue(ac(u'ata', u'+yAcAk'))
        self.assertTrue(ac(u'ata', u'dIk'))
        self.assertTrue(ac(u'ata', u'm'))
        self.assertTrue(ac(u'ata', u'+IyOr'))
        self.assertTrue(ac(u'ata', u'+Ar'))

    def test_should_return_not_applicable(self):
        self.assertFalse(ac(u'elma', u'Ar'))
        self.assertFalse(ac(u'elma', u'In'))
        self.assertFalse(ac(u'elma', u'+II'))

        #        self.assertFalse(a(u'armut', u'nda'))      #there can be no suffix like "nda", but "+nda"

        #        self.assertFalse(a(u'yap', u'ndIk'))       #there can be no suffix "ndik", but "+ndik"

        self.assertFalse(ac(u'ata', u'Ar'))
        self.assertFalse(ac(u'ata', u'In'))
        self.assertFalse(ac(u'ata', u'+II'))

    def test_should_apply_suffixes(self):
        self.assertEqual(ap(u'elma', None), u'elma')
        self.assertEqual(ap(u'elma', u''), u'elma')
        self.assertEqual(ap(u'elma', u' '), u'elma')
        self.assertEqual(ap(u'elma', u'lAr'), u'elmalar')
        self.assertEqual(ap(u'elma', u'cI'), u'elmacı')
        self.assertEqual(ap(u'elma', u'lAş'), u'elmalaş')
        self.assertEqual(ap(u'elma', u'dIr'), u'elmadır')
        self.assertEqual(ap(u'elma', u'nIn'), u'elmanın')
        self.assertEqual(ap(u'elma', u'+nIn'), u'elmanın')
        self.assertEqual(ap(u'elma', u'+yI'), u'elmayı')
        self.assertEqual(ap(u'elma', u'+sI'), u'elması')
        self.assertEqual(ap(u'elma', u'+dAn'), u'elmadan')
        self.assertEqual(ap(u'elma', u'+Im'), u'elmam')
        self.assertEqual(ap(u'elma', u'+ylA'), u'elmayla')

        self.assertEqual(ap(u'armut', None), u'armut')
        self.assertEqual(ap(u'armut', u''), u'armut')
        self.assertEqual(ap(u'armut', u' '), u'armut')
        self.assertEqual(ap(u'armut', u'lAr'), u'armutlar')
        self.assertEqual(ap(u'armut', u'cI'), u'armutçu')
        self.assertEqual(ap(u'armut', u'lAş'), u'armutlaş')
        self.assertEqual(ap(u'armut', u'dIr'), u'armuttur')
        self.assertEqual(ap(u'armut', u'In'), u'armudun')
        self.assertEqual(ap(u'armut', u'+nIn'), u'armudun')
        self.assertEqual(ap(u'armut', u'+yI'), u'armudu')
        self.assertEqual(ap(u'armut', u'+sI'), u'armudu')
        self.assertEqual(ap(u'armut', u'+dAn'), u'armudan')
        self.assertEqual(ap(u'armut', u'+Im'), u'armudum')
        self.assertEqual(ap(u'armut', u'+ylA'), u'armutla')

        self.assertEqual(ap(u'del', u'+yAcAk'), u'delecek')
        self.assertEqual(ap(u'del', u'dIk'), u'deldik')
        self.assertEqual(ap(u'del', u'm'), u'delm')
        self.assertEqual(ap(u'del', u'+Iyor'), u'deliyor')
        self.assertEqual(ap(u'del', u'+Ar'), u'deler')

        self.assertEqual(ap(u'ata', u'+yAcAk'), u'atayacak')
        self.assertEqual(ap(u'ata', u'dIk'), u'atadık')
        self.assertEqual(ap(u'ata', u'm'), u'atam')
        self.assertEqual(ap(u'ata', u'+Ar'), u'atar')
        self.assertEqual(ap(u'at', u'+IyOr', [RootAttribute.NoVoicing]), u'atıyor')

        self.assertEqual(ap(u'bul', u'mAlI'), u'bulmalu')
        self.assertEqual(ap(u'bul', u'mAlI!'), u'bulmalı')

    def test_should_apply_suffixes_with_attributes(self):
        self.assertEqual(apnv(u'yap', u'+yAcAk'), u'yapacak')
        self.assertEqual(apnv(u'yap', u'+Iyor'), u'yapıyor')
        self.assertEqual(apnv(u'yap', u'+Ar'), u'yapar')
        self.assertEqual(apnv(u'yap', u'tI'), u'yaptı')

        self.assertEqual(apnv(u'kek', u'+I'), u'keki')
        self.assertEqual(apnv(u'kek', u'+Im'), u'kekim')
        self.assertEqual(apnv(u'kek', u'+A'), u'keke')
        self.assertEqual(apnv(u'kek', u'dA'), u'kekte')

    def test_should_satisfy_no_expectations(self):
        self.assertTrue(es([], None))
        self.assertTrue(es([], ''))
        self.assertTrue(es([], 'xxxx'))

    def test_should_not_satisfy_expectations_with_no_form(self):
        self.assertFalse(es([C], None))
        self.assertFalse(es([V], ''))
        self.assertFalse(es([C, V], ' '))

    def test_should_satisfy_vowel_starts(self):
        self.assertTrue(es([V], "ir"))
        self.assertTrue(es([V], "Ir"))
        self.assertTrue(es([V], "Aa"))
        self.assertTrue(es([V], "aa"))
        self.assertTrue(es([V], "+Aa"))
        self.assertTrue(es([V], "+ia"))
        self.assertTrue(es([V], "+inda"))
        self.assertTrue(es([V], "+nIn"))
        self.assertTrue(es([V], "+na"))
        self.assertTrue(es([V], "+ya"))


    def test_should_not_satisfy_vowel_starts(self):
        self.assertFalse(es([V], "lir"))
        self.assertFalse(es([V], "lIr"))
        self.assertFalse(es([V], "dA"))
        self.assertFalse(es([V], "da"))
        self.assertFalse(es([V], "+nda"))

    def test_should_satisfy_consonant_starts(self):
        self.assertTrue(es([C], "da"))
        self.assertTrue(es([C], "nda"))
        self.assertTrue(es([C], "+ar"))
        self.assertTrue(es([C], "+Ar"))
        self.assertTrue(es([C], "+ir"))
        self.assertTrue(es([C], "+Ir"))
        self.assertTrue(es([C], "+nda"))
        self.assertTrue(es([C], "+nin"))
        self.assertTrue(es([C], "+nIn"))

    def test_should_not_satisfy_consonant_starts(self):
        self.assertFalse(es([C], "a"))
        self.assertFalse(es([C], "aa"))
        self.assertFalse(es([C], "A"))
        self.assertFalse(es([C], "Aa"))
        self.assertFalse(es([C], "ada"))
        self.assertFalse(es([C], "Ada"))
        self.assertFalse(es([C], "+aa"))
        self.assertFalse(es([C], "+Aa"))
        self.assertFalse(es([C], "+aa"))

    def test_should_calculate_phonetic_attrs(self):
        LLV = PhoneticAttributes.LastLetterVowel
        LLC = PhoneticAttributes.LastLetterConsonant

        LVR = PhoneticAttributes.LastVowelRounded
        LVU = PhoneticAttributes.LastVowelUnrounded
        LVF = PhoneticAttributes.LastVowelFrontal
        LVB = PhoneticAttributes.LastVowelBack

        LLVless =  PhoneticAttributes.LastLetterVoiceless
        LLVlessStop = PhoneticAttributes.LastLetterVoicelessStop
        LLNotVless =  PhoneticAttributes.LastLetterNotVoiceless

        self.assertEqual({LLV, LVU, LVF, LLNotVless}, cpa("e"))
        self.assertEqual({LLC, LVU, LVF, LLNotVless}, cpa("el"))
        self.assertEqual({LLC, LVU, LVF, LLVless, LLVlessStop}, cpa("ek"))
        self.assertEqual({LLC, LVU, LVF, LLVless}, cpa("eh"))
        self.assertEqual({LLC, LVU, LVF, LLNotVless}, cpa("elm"))
        self.assertEqual({LLC, LVU, LVF, LLVless, LLVlessStop}, cpa("elk"))
        self.assertEqual({LLV, LVU, LVB, LLNotVless}, cpa("elma"))
        self.assertEqual({LLV, LVR, LVB, LLNotVless}, cpa("elmo"))

    def test_should_match_application(self):
        self.assertTrue(am(u'elma', u'elma', True))
        self.assertTrue(am(u'elmalar', u'elma', True))
        self.assertTrue(am(u'elmalar', u'elma', True))
        self.assertTrue(am(u'keklerim', u'kekler', True))
        self.assertTrue(am(u'armudunu', u'armut', True))
        self.assertTrue(am(u'armudunu', u'armudu', True))
        self.assertTrue(am(u'armudunu', u'armudunu', True))
        self.assertTrue(am(u'yapacağım', u'yap', True))
        self.assertTrue(am(u'yapacağım', u'yapacak', True))
        self.assertTrue(am(u'yapacağım', u'yapacağım', True))

        self.assertTrue(am(u'yapacağım', u'yap', False))
        self.assertTrue(am(u'armut', u'armut', False))

    def test_should_not_match_application(self):
        self.assertFalse(am(u'elma', None, True))
        self.assertFalse(am(u'elma', u'elmax', True))
        self.assertFalse(am(u'elmalar', u'a', True))
        self.assertFalse(am(u'elmalar', u'ea', True))
        self.assertFalse(am(u'elmalar', u'ela', True))
        self.assertFalse(am(u'elmalar', u'elmx', True))
        self.assertFalse(am(u'elmalar', u'elmax', True))
        self.assertFalse(am(u'elmalar', u'elmalx', True))
        self.assertFalse(am(u'elmalar', u'elmalax', True))
        self.assertFalse(am(u'elmalar', u'elmalarx', True))

        self.assertFalse(am(u'yapacağım', u'yapacak', False))
        self.assertFalse(am(u'armudunu', u'armut', False))

if __name__ == '__main__':
    unittest.main()