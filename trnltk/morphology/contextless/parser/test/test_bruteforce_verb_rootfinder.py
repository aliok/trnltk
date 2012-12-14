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
from hamcrest import *
from trnltk.morphology.contextless.parser.bruteforceverbrootfinder import BruteForceVerbRootFinder
from trnltk.morphology.model.lexeme import SyntacticCategory, LexemeAttribute

class BruteForceVerbRootFinderTest(unittest.TestCase):

    def setUp(self):
        self.root_finder = BruteForceVerbRootFinder()

    def test_should_check_invalid_cases(self):
        f = lambda : self.root_finder.find_roots_for_partial_input(None, None)
        self.assertRaises(AssertionError, f)

        f = lambda : self.root_finder.find_roots_for_partial_input("", None)
        self.assertRaises(AssertionError, f)

        f = lambda : self.root_finder.find_roots_for_partial_input(None, "")
        self.assertRaises(AssertionError, f)

        f = lambda : self.root_finder.find_roots_for_partial_input("", "")
        self.assertRaises(AssertionError, f)

        f = lambda : self.root_finder.find_roots_for_partial_input(u"a", None)
        self.assertRaises(AssertionError, f)

        f = lambda : self.root_finder.find_roots_for_partial_input(u"a", u"")
        self.assertRaises(AssertionError, f)

        f = lambda : self.root_finder.find_roots_for_partial_input(u"ab", u"a")
        self.assertRaises(AssertionError, f)



    def test_should_create_roots_without_orthographic_changes_and_no_lexeme_attributes(self):
    #TODO
#        roots = self.root_finder.find_roots_for_partial_input(u"s", u"saldı")
#        assert_that(roots, has_length(1))
#        assert_that(roots[0].str, equal_to(u'sal'))
#        assert_that(roots[0].lexeme.root, equal_to(u'sal'))
#        assert_that(roots[0].lexeme.lemma, equal_to(u'salmak'))
#        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
#        assert_that(roots[0].lexeme.attributes, equal_to(set()))

        roots = self.root_finder.find_roots_for_partial_input(u"al", u"al")
        assert_that(roots, has_length(1))
        assert_that(roots[0].str, equal_to(u'al'))
        assert_that(roots[0].lexeme.root, equal_to(u'al'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'almak'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[0].lexeme.attributes, equal_to(set()))

        roots = self.root_finder.find_roots_for_partial_input(u"sal", u"sal")
        assert_that(roots, has_length(1))
        assert_that(roots[0].str, equal_to(u'sal'))
        assert_that(roots[0].lexeme.root, equal_to(u'sal'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'salmak'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[0].lexeme.attributes, equal_to(set()))

        roots = self.root_finder.find_roots_for_partial_input(u"al", u"aldı")
        assert_that(roots, has_length(1))
        assert_that(roots[0].str, equal_to(u'al'))
        assert_that(roots[0].lexeme.root, equal_to(u'al'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'almak'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[0].lexeme.attributes, equal_to(set()))

        roots = self.root_finder.find_roots_for_partial_input(u"sal", u"saldı")
        assert_that(roots, has_length(1))
        assert_that(roots[0].str, equal_to(u'sal'))
        assert_that(roots[0].lexeme.root, equal_to(u'sal'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'salmak'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[0].lexeme.attributes, equal_to(set()))

    def test_should_create_roots_with_progressive_vowel_drop(self):
        roots = self.root_finder.find_roots_for_partial_input(u"başl", u"başlıyor")
        assert_that(roots, has_length(1))
        assert_that(roots[0].str, equal_to(u'başl'))
        assert_that(roots[0].lexeme.root, equal_to(u'başla'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'başlamak'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[0].lexeme.attributes, equal_to({LexemeAttribute.ProgressiveVowelDrop}))

        roots = self.root_finder.find_roots_for_partial_input(u"ell", u"elliyorduk")
        assert_that(roots, has_length(1))
        assert_that(roots[0].str, equal_to(u'ell'))
        assert_that(roots[0].lexeme.root, equal_to(u'elle'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'ellemek'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[0].lexeme.attributes, equal_to({LexemeAttribute.ProgressiveVowelDrop}))

        roots = self.root_finder.find_roots_for_partial_input(u"oyn", u"oynuyorlar")
        assert_that(roots, has_length(1))
        assert_that(roots[0].str, equal_to(u'oyn'))
        assert_that(roots[0].lexeme.root, equal_to(u'oyna'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'oynamak'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[0].lexeme.attributes, equal_to({LexemeAttribute.ProgressiveVowelDrop}))

        roots = self.root_finder.find_roots_for_partial_input(u"söyl", u"söylüyorsun")
        assert_that(roots, has_length(1))
        assert_that(roots[0].str, equal_to(u'söyl'))
        assert_that(roots[0].lexeme.root, equal_to(u'söyle'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'söylemek'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[0].lexeme.attributes, equal_to({LexemeAttribute.ProgressiveVowelDrop}))

    def test_should_create_roots_with_aorist_A_and_causative_Ar(self):
        # each Aorist_A case is also a Causative_Ar case
        roots = self.root_finder.find_roots_for_partial_input(u"çık", u"çıkarmış")
        roots = sorted(roots, key=lambda r : r.lexeme.attributes)
        assert_that(roots, has_length(3))
        assert_that(roots[0].str, equal_to(u'çık'))
        assert_that(roots[0].lexeme.root, equal_to(u'çık'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'çıkmak'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[0].lexeme.attributes, equal_to(set()))
        assert_that(roots[1].str, equal_to(u'çık'))
        assert_that(roots[1].lexeme.root, equal_to(u'çık'))
        assert_that(roots[1].lexeme.lemma, equal_to(u'çıkmak'))
        assert_that(roots[1].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[1].lexeme.attributes, equal_to({LexemeAttribute.Aorist_A}))
        assert_that(roots[2].str, equal_to(u'çık'))
        assert_that(roots[2].lexeme.root, equal_to(u'çık'))
        assert_that(roots[2].lexeme.lemma, equal_to(u'çıkmak'))
        assert_that(roots[2].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[2].lexeme.attributes, equal_to({LexemeAttribute.Causative_Ar}))

        roots = self.root_finder.find_roots_for_partial_input(u"öt", u"ötermiş")
        roots = sorted(roots, key=lambda r : r.lexeme.attributes)
        assert_that(roots, has_length(3))
        assert_that(roots[0].str, equal_to(u'öt'))
        assert_that(roots[0].lexeme.root, equal_to(u'öt'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'ötmek'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[0].lexeme.attributes, equal_to(set()))
        assert_that(roots[1].str, equal_to(u'öt'))
        assert_that(roots[1].lexeme.root, equal_to(u'öt'))
        assert_that(roots[1].lexeme.lemma, equal_to(u'ötmek'))
        assert_that(roots[1].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[1].lexeme.attributes, equal_to({LexemeAttribute.Causative_Ar}))
        assert_that(roots[2].str, equal_to(u'öt'))
        assert_that(roots[2].lexeme.root, equal_to(u'öt'))
        assert_that(roots[2].lexeme.lemma, equal_to(u'ötmek'))
        assert_that(roots[2].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[2].lexeme.attributes, equal_to({LexemeAttribute.Aorist_A}))

    def test_should_create_roots_with_aorist_I(self):
        # each Aorist_I case is also a Causative_Ir case
        # this actually doesn't make sense since yat+Aor->yatar but yat+Caus->yatir
        # however, there is no way to distinguish
        roots = self.root_finder.find_roots_for_partial_input(u"yat", u"yatır")
        roots = sorted(roots, key=lambda r : r.lexeme.attributes)
        assert_that(roots, has_length(3))
        assert_that(roots[0].str, equal_to(u'yat'))
        assert_that(roots[0].lexeme.root, equal_to(u'yat'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'yatmak'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[0].lexeme.attributes, equal_to(set()))
        assert_that(roots[1].str, equal_to(u'yat'))
        assert_that(roots[1].lexeme.root, equal_to(u'yat'))
        assert_that(roots[1].lexeme.lemma, equal_to(u'yatmak'))
        assert_that(roots[1].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[1].lexeme.attributes, equal_to({LexemeAttribute.Aorist_I}))
        assert_that(roots[2].str, equal_to(u'yat'))
        assert_that(roots[2].lexeme.root, equal_to(u'yat'))
        assert_that(roots[2].lexeme.lemma, equal_to(u'yatmak'))
        assert_that(roots[2].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[2].lexeme.attributes, equal_to({LexemeAttribute.Causative_Ir}))

        roots = self.root_finder.find_roots_for_partial_input(u"gel", u"gelir")
        roots = sorted(roots, key=lambda r : r.lexeme.attributes)
        assert_that(roots, has_length(3))
        assert_that(roots[0].str, equal_to(u'gel'))
        assert_that(roots[0].lexeme.root, equal_to(u'gel'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'gelmek'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[0].lexeme.attributes, equal_to(set()))
        assert_that(roots[1].str, equal_to(u'gel'))
        assert_that(roots[1].lexeme.root, equal_to(u'gel'))
        assert_that(roots[1].lexeme.lemma, equal_to(u'gelmek'))
        assert_that(roots[1].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[1].lexeme.attributes, equal_to({LexemeAttribute.Aorist_I}))
        assert_that(roots[2].str, equal_to(u'gel'))
        assert_that(roots[2].lexeme.root, equal_to(u'gel'))
        assert_that(roots[2].lexeme.lemma, equal_to(u'gelmek'))
        assert_that(roots[2].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[2].lexeme.attributes, equal_to({LexemeAttribute.Causative_Ir}))

    def test_should_create_roots_with_causative_t(self):
        roots = self.root_finder.find_roots_for_partial_input(u"kapa", u"kapattım")
        roots = sorted(roots, key=lambda r : r.lexeme.attributes)
        assert_that(roots, has_length(2))
        assert_that(roots[0].str, equal_to(u'kapa'))
        assert_that(roots[0].lexeme.root, equal_to(u'kapa'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'kapamak'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[0].lexeme.attributes, equal_to(set()))
        assert_that(roots[1].str, equal_to(u'kapa'))
        assert_that(roots[1].lexeme.root, equal_to(u'kapa'))
        assert_that(roots[1].lexeme.lemma, equal_to(u'kapamak'))
        assert_that(roots[1].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[1].lexeme.attributes, equal_to({LexemeAttribute.Causative_t}))

        roots = self.root_finder.find_roots_for_partial_input(u"yürü", u"yürütecekmiş")
        roots = sorted(roots, key=lambda r : r.lexeme.attributes)
        assert_that(roots, has_length(2))
        assert_that(roots[0].str, equal_to(u'yürü'))
        assert_that(roots[0].lexeme.root, equal_to(u'yürü'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'yürümek'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[0].lexeme.attributes, equal_to(set()))
        assert_that(roots[1].str, equal_to(u'yürü'))
        assert_that(roots[1].lexeme.root, equal_to(u'yürü'))
        assert_that(roots[1].lexeme.lemma, equal_to(u'yürümek'))
        assert_that(roots[1].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[1].lexeme.attributes, equal_to({LexemeAttribute.Causative_t}))

    def test_should_create_roots_with_causative_It(self):
        roots = self.root_finder.find_roots_for_partial_input(u"ak", u"akıtmışlar")
        roots = sorted(roots, key=lambda r : r.lexeme.attributes)
        assert_that(roots, has_length(2))
        assert_that(roots[0].str, equal_to(u'ak'))
        assert_that(roots[0].lexeme.root, equal_to(u'ak'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'akmak'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[0].lexeme.attributes, equal_to(set()))
        assert_that(roots[1].str, equal_to(u'ak'))
        assert_that(roots[1].lexeme.root, equal_to(u'ak'))
        assert_that(roots[1].lexeme.lemma, equal_to(u'akmak'))
        assert_that(roots[1].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[1].lexeme.attributes, equal_to({LexemeAttribute.Causative_It}))

        roots = self.root_finder.find_roots_for_partial_input(u"kork", u"korkutacaklar")
        roots = sorted(roots, key=lambda r : r.lexeme.attributes)
        assert_that(roots, has_length(2))
        assert_that(roots[0].str, equal_to(u'kork'))
        assert_that(roots[0].lexeme.root, equal_to(u'kork'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'korkmak'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[0].lexeme.attributes, equal_to(set()))
        assert_that(roots[1].str, equal_to(u'kork'))
        assert_that(roots[1].lexeme.root, equal_to(u'kork'))
        assert_that(roots[1].lexeme.lemma, equal_to(u'korkmak'))
        assert_that(roots[1].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[1].lexeme.attributes, equal_to({LexemeAttribute.Causative_It}))

    def test_should_create_roots_with_causative_It(self):
        roots = self.root_finder.find_roots_for_partial_input(u"al", u"aldırmışlar")
        roots = sorted(roots, key=lambda r : r.lexeme.attributes)
        assert_that(roots, has_length(2))
        assert_that(roots[0].str, equal_to(u'al'))
        assert_that(roots[0].lexeme.root, equal_to(u'al'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'almak'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[0].lexeme.attributes, equal_to(set()))
        assert_that(roots[1].str, equal_to(u'al'))
        assert_that(roots[1].lexeme.root, equal_to(u'al'))
        assert_that(roots[1].lexeme.lemma, equal_to(u'almak'))
        assert_that(roots[1].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[1].lexeme.attributes, equal_to({LexemeAttribute.Causative_dIr}))

        roots = self.root_finder.find_roots_for_partial_input(u"öl", u"öldürmüşcesine")
        roots = sorted(roots, key=lambda r : r.lexeme.attributes)
        assert_that(roots, has_length(2))
        assert_that(roots[0].str, equal_to(u'öl'))
        assert_that(roots[0].lexeme.root, equal_to(u'öl'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'ölmek'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[0].lexeme.attributes, equal_to(set()))
        assert_that(roots[1].str, equal_to(u'öl'))
        assert_that(roots[1].lexeme.root, equal_to(u'öl'))
        assert_that(roots[1].lexeme.lemma, equal_to(u'ölmek'))
        assert_that(roots[1].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[1].lexeme.attributes, equal_to({LexemeAttribute.Causative_dIr}))

        roots = self.root_finder.find_roots_for_partial_input(u"öt", u"öttürüyorum")
        roots = sorted(roots, key=lambda r : r.lexeme.attributes)
        assert_that(roots, has_length(3))
        assert_that(roots[0].str, equal_to(u'öt'))
        assert_that(roots[0].lexeme.root, equal_to(u'öt'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'ötmek'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[0].lexeme.attributes, equal_to(set()))
        assert_that(roots[1].str, equal_to(u'öt'))
        assert_that(roots[1].lexeme.root, equal_to(u'öt'))
        assert_that(roots[1].lexeme.lemma, equal_to(u'ötmek'))
        assert_that(roots[1].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[1].lexeme.attributes, equal_to({LexemeAttribute.Causative_dIr}))
        assert_that(roots[2].str, equal_to(u'öt'))
        assert_that(roots[2].lexeme.root, equal_to(u'öt'))
        assert_that(roots[2].lexeme.lemma, equal_to(u'ötmek'))
        assert_that(roots[2].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[2].lexeme.attributes, equal_to({LexemeAttribute.Causative_t}))    # doesn't make sense, but ok


    def test_should_create_roots_with_passive_Il(self):
        roots = self.root_finder.find_roots_for_partial_input(u"sat", u"satılmış")
        roots = sorted(roots, key=lambda r : r.lexeme.attributes)
        assert_that(roots, has_length(2))
        assert_that(roots[0].str, equal_to(u'sat'))
        assert_that(roots[0].lexeme.root, equal_to(u'sat'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'satmak'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[0].lexeme.attributes, equal_to(set()))
        assert_that(roots[1].str, equal_to(u'sat'))
        assert_that(roots[1].lexeme.root, equal_to(u'sat'))
        assert_that(roots[1].lexeme.lemma, equal_to(u'satmak'))
        assert_that(roots[1].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[1].lexeme.attributes, equal_to({LexemeAttribute.Passive_Il}))

        roots = self.root_finder.find_roots_for_partial_input(u"döv", u"dövülen")
        roots = sorted(roots, key=lambda r : r.lexeme.attributes)
        assert_that(roots, has_length(2))
        assert_that(roots[0].str, equal_to(u'döv'))
        assert_that(roots[0].lexeme.root, equal_to(u'döv'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'dövmek'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[0].lexeme.attributes, equal_to(set()))
        assert_that(roots[1].str, equal_to(u'döv'))
        assert_that(roots[1].lexeme.root, equal_to(u'döv'))
        assert_that(roots[1].lexeme.lemma, equal_to(u'dövmek'))
        assert_that(roots[1].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[1].lexeme.attributes, equal_to({LexemeAttribute.Passive_Il}))

    def test_should_create_roots_with_passive_In(self):
        roots = self.root_finder.find_roots_for_partial_input(u"al", u"alındı")
        roots = sorted(roots, key=lambda r : r.lexeme.attributes)
        assert_that(roots, has_length(2))
        assert_that(roots[0].str, equal_to(u'al'))
        assert_that(roots[0].lexeme.root, equal_to(u'al'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'almak'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[0].lexeme.attributes, equal_to(set()))
        assert_that(roots[1].str, equal_to(u'al'))
        assert_that(roots[1].lexeme.root, equal_to(u'al'))
        assert_that(roots[1].lexeme.lemma, equal_to(u'almak'))
        assert_that(roots[1].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[1].lexeme.attributes, equal_to({LexemeAttribute.Passive_In}))

        roots = self.root_finder.find_roots_for_partial_input(u"tekmele", u"tekmelendim")
        roots = sorted(roots, key=lambda r : r.lexeme.attributes)
        assert_that(roots, has_length(2))
        assert_that(roots[0].str, equal_to(u'tekmele'))
        assert_that(roots[0].lexeme.root, equal_to(u'tekmele'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'tekmelemek'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[0].lexeme.attributes, equal_to(set()))
        assert_that(roots[1].str, equal_to(u'tekmele'))
        assert_that(roots[1].lexeme.root, equal_to(u'tekmele'))
        assert_that(roots[1].lexeme.lemma, equal_to(u'tekmelemek'))
        assert_that(roots[1].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[1].lexeme.attributes, equal_to({LexemeAttribute.Passive_In}))

    def test_should_create_roots_with_passive_InIl(self):
        roots = self.root_finder.find_roots_for_partial_input(u"de", u"denildi")
        roots = sorted(roots, key=lambda r : r.lexeme.attributes)
        assert_that(roots, has_length(3))
        assert_that(roots[0].str, equal_to(u'de'))
        assert_that(roots[0].lexeme.root, equal_to(u'de'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'demek'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[0].lexeme.attributes, equal_to(set()))
        assert_that(roots[1].str, equal_to(u'de'))
        assert_that(roots[1].lexeme.root, equal_to(u'de'))
        assert_that(roots[1].lexeme.lemma, equal_to(u'demek'))
        assert_that(roots[1].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[1].lexeme.attributes, equal_to({LexemeAttribute.Passive_In}))
        assert_that(roots[2].str, equal_to(u'de'))
        assert_that(roots[2].lexeme.root, equal_to(u'de'))
        assert_that(roots[2].lexeme.lemma, equal_to(u'demek'))
        assert_that(roots[2].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[2].lexeme.attributes, equal_to({LexemeAttribute.Passive_InIl}))


    def test_should_create_roots_with_voicing(self):
        # nothing but voicing
        roots = self.root_finder.find_roots_for_partial_input(u"gid", u"gidip")
        roots = sorted(roots, key=lambda r : r.lexeme.attributes)
        assert_that(roots, has_length(2))
        assert_that(roots[0].str, equal_to(u'gid'))
        assert_that(roots[0].lexeme.root, equal_to(u'gid'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'gidmek'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[0].lexeme.attributes, equal_to(set()))
        assert_that(roots[1].str, equal_to(u'gid'))
        assert_that(roots[1].lexeme.root, equal_to(u'git'))
        assert_that(roots[1].lexeme.lemma, equal_to(u'gitmek'))
        assert_that(roots[1].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[1].lexeme.attributes, equal_to({LexemeAttribute.Voicing}))

        # skip progressive vowel drop and voicing

        # voicing and aorist_A and causative_Ar (ok, gidermek is not really git+Caus)
        roots = self.root_finder.find_roots_for_partial_input(u"gid", u"giderdi")
        roots = sorted(roots, key=lambda r : r.lexeme.attributes)
        assert_that(roots, has_length(6))
        assert_that(roots[0].str, equal_to(u'gid'))
        assert_that(roots[0].lexeme.root, equal_to(u'gid'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'gidmek'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[0].lexeme.attributes, equal_to(set()))
        assert_that(roots[1].str, equal_to(u'gid'))
        assert_that(roots[1].lexeme.root, equal_to(u'git'))
        assert_that(roots[1].lexeme.lemma, equal_to(u'gitmek'))
        assert_that(roots[1].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[1].lexeme.attributes, equal_to({LexemeAttribute.Voicing, LexemeAttribute.Aorist_A}))
        assert_that(roots[2].str, equal_to(u'gid'))
        assert_that(roots[2].lexeme.root, equal_to(u'gid'))
        assert_that(roots[2].lexeme.lemma, equal_to(u'gidmek'))
        assert_that(roots[2].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[2].lexeme.attributes, equal_to({LexemeAttribute.Causative_Ar}))
        assert_that(roots[3].str, equal_to(u'gid'))
        assert_that(roots[3].lexeme.root, equal_to(u'gid'))
        assert_that(roots[3].lexeme.lemma, equal_to(u'gidmek'))
        assert_that(roots[3].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[3].lexeme.attributes, equal_to({LexemeAttribute.Aorist_A}))
        assert_that(roots[4].str, equal_to(u'gid'))
        assert_that(roots[4].lexeme.root, equal_to(u'git'))
        assert_that(roots[4].lexeme.lemma, equal_to(u'gitmek'))
        assert_that(roots[4].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[4].lexeme.attributes, equal_to({LexemeAttribute.Voicing}))
        assert_that(roots[5].str, equal_to(u'gid'))
        assert_that(roots[5].lexeme.root, equal_to(u'git'))
        assert_that(roots[5].lexeme.lemma, equal_to(u'gitmek'))
        assert_that(roots[5].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[5].lexeme.attributes, equal_to({LexemeAttribute.Voicing, LexemeAttribute.Causative_Ar}))

        # voicing and aorist_I and causative_Ir
        # couldn't find an example, but lets support it until we find out that it is impossible
        roots = self.root_finder.find_roots_for_partial_input(u"abd", u"abdırmış") ##TODO
        roots = sorted(roots, key=lambda r : r.lexeme.attributes)
        assert_that(roots, has_length(4))
        assert_that(roots[0].str, equal_to(u'abd'))
        assert_that(roots[0].lexeme.root, equal_to(u'abd'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'abdmak'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[0].lexeme.attributes, equal_to({LexemeAttribute.Aorist_I}))
        assert_that(roots[1].str, equal_to(u'abd'))
        assert_that(roots[1].lexeme.root, equal_to(u'abt'))
        assert_that(roots[1].lexeme.lemma, equal_to(u'abtmak'))
        assert_that(roots[1].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[1].lexeme.attributes, equal_to({LexemeAttribute.Voicing, LexemeAttribute.Aorist_I}))
        assert_that(roots[2].str, equal_to(u'abd'))
        assert_that(roots[2].lexeme.root, equal_to(u'abd'))
        assert_that(roots[2].lexeme.lemma, equal_to(u'abdmak'))
        assert_that(roots[2].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[2].lexeme.attributes, equal_to({LexemeAttribute.Causative_Ir}))
        assert_that(roots[3].str, equal_to(u'abd'))
        assert_that(roots[3].lexeme.root, equal_to(u'abt'))
        assert_that(roots[3].lexeme.lemma, equal_to(u'abtmak'))
        assert_that(roots[3].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[3].lexeme.attributes, equal_to({LexemeAttribute.Voicing, LexemeAttribute.Causative_Ir}))

        # skip {Causative_t, Causative_It, Causative_dIr} and voicing

        # voicing and passive_Il
        # tadılan, güdülen, didilen, gidilen, hapsedilen ...
        roots = self.root_finder.find_roots_for_partial_input(u"ed", u"edilen")
        roots = sorted(roots, key=lambda r : r.lexeme.attributes)
        assert_that(roots, has_length(4))
        assert_that(roots[0].str, equal_to(u'ed'))
        assert_that(roots[0].lexeme.root, equal_to(u'ed'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'edmek'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[0].lexeme.attributes, equal_to(set()))
        assert_that(roots[1].str, equal_to(u'ed'))
        assert_that(roots[1].lexeme.root, equal_to(u'ed'))
        assert_that(roots[1].lexeme.lemma, equal_to(u'edmek'))
        assert_that(roots[1].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[1].lexeme.attributes, equal_to({LexemeAttribute.Passive_Il}))
        assert_that(roots[2].str, equal_to(u'ed'))
        assert_that(roots[2].lexeme.root, equal_to(u'et'))
        assert_that(roots[2].lexeme.lemma, equal_to(u'etmek'))
        assert_that(roots[2].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[2].lexeme.attributes, equal_to({LexemeAttribute.Voicing}))
        assert_that(roots[3].str, equal_to(u'ed'))
        assert_that(roots[3].lexeme.root, equal_to(u'et'))
        assert_that(roots[3].lexeme.lemma, equal_to(u'etmek'))
        assert_that(roots[3].lexeme.syntactic_category, equal_to(SyntacticCategory.VERB))
        assert_that(roots[3].lexeme.attributes, equal_to({LexemeAttribute.Passive_Il, LexemeAttribute.Voicing}))

        # skip voicing and {passive_InIl, passive_In}

    def test_should_create_roots_with_inverse_harmony(self):
        roots = self.root_finder.find_roots_for_partial_input(u"yol", u"yole")

        for r in roots:
            print r

    def test_should_create_roots_with_voicing_and_inverse_harmony(self):
        roots = self.root_finder.find_roots_for_partial_input(u"sad", u"sadip")

        for r in roots:
            print r

if __name__ == '__main__':
    unittest.main()
