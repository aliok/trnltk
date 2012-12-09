# coding=utf-8
"""
Copyright  2012  Ali Ok (aliokATapacheDOTorg)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import unittest
from trnltk.morphology.model.lexeme import LexemeAttribute
from trnltk.morphology.phonetics.phonetics import Phonetics, PhoneticExpectation, PhoneticAttributes

ac = Phonetics.is_suffix_form_applicable
def ap(word, form_str, lexeme_attributes=None):
    phonetic_attributes = Phonetics.calculate_phonetic_attributes(word, lexeme_attributes)
    word, application = Phonetics.apply(word, phonetic_attributes, form_str, lexeme_attributes)
    return word + application

def apnv(word, form_str):
    return ap(word, form_str, [LexemeAttribute.NoVoicing])

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
        self.assertEqual(ap(u'at', u'+IyOr', [LexemeAttribute.NoVoicing]), u'atıyor')

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
        self.assertTrue(es([], u''))
        self.assertTrue(es([], u'xxxx'))

    def test_should_not_satisfy_expectations_with_no_form(self):
        self.assertFalse(es([C], None))
        self.assertFalse(es([V], u''))
        self.assertFalse(es([C, V], u' '))

    def test_should_satisfy_vowel_starts(self):
        self.assertTrue(es([V], u"ir"))
        self.assertTrue(es([V], u"Ir"))
        self.assertTrue(es([V], u"Aa"))
        self.assertTrue(es([V], u"aa"))
        self.assertTrue(es([V], u"+Aa"))
        self.assertTrue(es([V], u"+ia"))
        self.assertTrue(es([V], u"+inda"))
        self.assertTrue(es([V], u"+nIn"))
        self.assertTrue(es([V], u"+na"))
        self.assertTrue(es([V], u"+ya"))


    def test_should_not_satisfy_vowel_starts(self):
        self.assertFalse(es([V], u"lir"))
        self.assertFalse(es([V], u"lIr"))
        self.assertFalse(es([V], u"dA"))
        self.assertFalse(es([V], u"da"))
        self.assertFalse(es([V], u"+nda"))

    def test_should_satisfy_consonant_starts(self):
        self.assertTrue(es([C], u"da"))
        self.assertTrue(es([C], u"nda"))
        self.assertTrue(es([C], u"+ar"))
        self.assertTrue(es([C], u"+Ar"))
        self.assertTrue(es([C], u"+ir"))
        self.assertTrue(es([C], u"+Ir"))
        self.assertTrue(es([C], u"+nda"))
        self.assertTrue(es([C], u"+nin"))
        self.assertTrue(es([C], u"+nIn"))

    def test_should_not_satisfy_consonant_starts(self):
        self.assertFalse(es([C], u"a"))
        self.assertFalse(es([C], u"aa"))
        self.assertFalse(es([C], u"A"))
        self.assertFalse(es([C], u"Aa"))
        self.assertFalse(es([C], u"ada"))
        self.assertFalse(es([C], u"Ada"))
        self.assertFalse(es([C], u"+aa"))
        self.assertFalse(es([C], u"+Aa"))
        self.assertFalse(es([C], u"+aa"))

    def test_should_calculate_phonetic_attrs(self):
        LLV = PhoneticAttributes.LastLetterVowel
        LLC = PhoneticAttributes.LastLetterConsonant

        LVR = PhoneticAttributes.LastVowelRounded
        LVU = PhoneticAttributes.LastVowelUnrounded
        LVF = PhoneticAttributes.LastVowelFrontal
        LVB = PhoneticAttributes.LastVowelBack

        LLCont =  PhoneticAttributes.LastLetterContinuant
        LLNotCont =  PhoneticAttributes.LastLetterNotContinuant

        LLVless =  PhoneticAttributes.LastLetterVoiceless
        LLVlessStop = PhoneticAttributes.LastLetterVoicelessStop
        LLNotVless =  PhoneticAttributes.LastLetterNotVoiceless

        self.assertEqual({LLNotCont, LLV, LVU, LVF, LLNotVless}, cpa(u"e"))
        self.assertEqual({LLCont, LLC, LVU, LVF, LLNotVless}, cpa(u"el"))
        self.assertEqual({LLNotCont, LLC, LVU, LVF, LLVless, LLVlessStop}, cpa(u"ek"))
        self.assertEqual({LLCont, LLC, LVU, LVF, LLVless}, cpa(u"eh"))
        self.assertEqual({LLCont, LLC, LVU, LVF, LLNotVless}, cpa(u"elm"))
        self.assertEqual({LLNotCont, LLC, LVU, LVF, LLVless, LLVlessStop}, cpa(u"elk"))
        self.assertEqual({LLNotCont, LLV, LVU, LVB, LLNotVless}, cpa(u"elma"))
        self.assertEqual({LLNotCont, LLV, LVR, LVB, LLNotVless}, cpa(u"elmo"))

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