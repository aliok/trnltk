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
from trnltk.morphology.contextless.parser.bruteforcenounrootfinders import BruteForceNounRootFinder, BruteForceCompoundNounRootFinder
from trnltk.morphology.model.lexeme import SyntacticCategory, LexemeAttribute

class BruteForceNounRootFinderTest(unittest.TestCase):
    def setUp(self):
        self.root_finder = BruteForceNounRootFinder()

    def test_should_check_invalid_cases(self):
        f = lambda: self.root_finder.find_roots_for_partial_input(None, None)
        self.assertRaises(AssertionError, f)

        f = lambda: self.root_finder.find_roots_for_partial_input("", None)
        self.assertRaises(AssertionError, f)

        f = lambda: self.root_finder.find_roots_for_partial_input(None, "")
        self.assertRaises(AssertionError, f)

        f = lambda: self.root_finder.find_roots_for_partial_input("", "")
        self.assertRaises(AssertionError, f)

        f = lambda: self.root_finder.find_roots_for_partial_input(u"a", None)
        self.assertRaises(AssertionError, f)

        f = lambda: self.root_finder.find_roots_for_partial_input(u"a", u"")
        self.assertRaises(AssertionError, f)

        f = lambda: self.root_finder.find_roots_for_partial_input(u"ab", u"a")
        self.assertRaises(AssertionError, f)

        f = lambda: self.root_finder.find_roots_for_partial_input(u"ab", u"ad")
        self.assertRaises(AssertionError, f)

        f = lambda: self.root_finder.find_roots_for_partial_input(u"ab", u"ada")
        self.assertRaises(AssertionError, f)

    def test_should_create_no_roots(self):
        roots = self.root_finder.find_roots_for_partial_input(u'b', u'be')
        assert_that(roots, has_length(0))

        roots = self.root_finder.find_roots_for_partial_input(u'b', u'ben')
        assert_that(roots, has_length(0))


    def test_should_create_roots_without_orthographic_changes(self):
        roots = self.root_finder.find_roots_for_partial_input(u"a", u"a")
        assert_that(roots, has_length(1))
        assert_that(roots[0].str, equal_to(u'a'))
        assert_that(roots[0].lexeme.root, equal_to(u'a'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'a'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))

        roots = self.root_finder.find_roots_for_partial_input(u"b", u"b")
        assert_that(roots, has_length(1))
        assert_that(roots[0].str, equal_to(u'b'))
        assert_that(roots[0].lexeme.root, equal_to(u'b'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'b'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))

        roots = self.root_finder.find_roots_for_partial_input(u"ab", u"ab")
        assert_that(roots, has_length(1))
        assert_that(roots[0].str, equal_to(u'ab'))
        assert_that(roots[0].lexeme.root, equal_to(u'ab'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'ab'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))

        roots = self.root_finder.find_roots_for_partial_input(u"ba", u"ba")
        assert_that(roots, has_length(1))
        assert_that(roots[0].str, equal_to(u'ba'))
        assert_that(roots[0].lexeme.root, equal_to(u'ba'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'ba'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))

        roots = self.root_finder.find_roots_for_partial_input(u"atağ", u"atağ")
        assert_that(roots, has_length(1))
        assert_that(roots[0].str, equal_to(u'atağ'))
        assert_that(roots[0].lexeme.root, equal_to(u'atağ'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'atağ'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))

        roots = self.root_finder.find_roots_for_partial_input(u"abc", u"abc")
        assert_that(roots, has_length(1))
        assert_that(roots[0].str, equal_to(u'abc'))
        assert_that(roots[0].lexeme.root, equal_to(u'abc'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'abc'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))

        roots = self.root_finder.find_roots_for_partial_input(u"abc", u"abcdef")
        assert_that(roots, has_length(1))
        assert_that(roots[0].str, equal_to(u'abc'))
        assert_that(roots[0].lexeme.root, equal_to(u'abc'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'abc'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))

    def test_should_create_roots_with_voicing(self):
        roots = self.root_finder.find_roots_for_partial_input(u"ab", u"aba")
        assert_that(roots, has_length(2))
        assert_that(roots[0].str, equal_to(u'ab'))
        assert_that(roots[0].lexeme.root, equal_to(u'ab'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'ab'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[1].str, equal_to(u'ab'))
        assert_that(roots[1].lexeme.root, equal_to(u'ap'))
        assert_that(roots[1].lexeme.lemma, equal_to(u'ap'))
        assert_that(roots[1].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))

        roots = self.root_finder.find_roots_for_partial_input(u"ad", u"adımı")
        assert_that(roots, has_length(2))
        assert_that(roots[0].str, equal_to(u'ad'))
        assert_that(roots[0].lexeme.root, equal_to(u'ad'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'ad'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[1].str, equal_to(u'ad'))
        assert_that(roots[1].lexeme.root, equal_to(u'at'))
        assert_that(roots[1].lexeme.lemma, equal_to(u'at'))
        assert_that(roots[1].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))

        # skipped the case where nK voices to nG as in cenk->cengi
        #roots = self.root_finder.find_roots_for_partial_input(u"ang", u"anga")
        #assert_that(roots, has_length(2))
        #assert_that(roots[0].str, equal_to(u'ang'))
        #assert_that(roots[0].lexeme.root, equal_to(u'ang'))
        #assert_that(roots[0].lexeme.lemma, equal_to(u'ang'))
        #assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        #assert_that(roots[1].str, equal_to(u'ank'))
        #assert_that(roots[1].lexeme.root, equal_to(u'ank'))
        #assert_that(roots[1].lexeme.lemma, equal_to(u'ank'))
        #assert_that(roots[1].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))

        roots = self.root_finder.find_roots_for_partial_input(u"ağ", u"ağa")
        assert_that(roots, has_length(3))
        assert_that(roots[0].str, equal_to(u'ağ'))
        assert_that(roots[0].lexeme.root, equal_to(u'ağ'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'ağ'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[1].str, equal_to(u'ağ'))
        assert_that(roots[1].lexeme.root, equal_to(u'ag'))
        assert_that(roots[1].lexeme.lemma, equal_to(u'ag'))
        assert_that(roots[1].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[2].str, equal_to(u'ağ'))
        assert_that(roots[2].lexeme.root, equal_to(u'ak'))
        assert_that(roots[2].lexeme.lemma, equal_to(u'ak'))
        assert_that(roots[2].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))

        roots = self.root_finder.find_roots_for_partial_input(u"ac", u"acımdan")
        assert_that(roots, has_length(2))
        assert_that(roots[0].str, equal_to(u'ac'))
        assert_that(roots[0].lexeme.root, equal_to(u'ac'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'ac'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[1].str, equal_to(u'ac'))
        assert_that(roots[1].lexeme.root, equal_to(u'aç'))
        assert_that(roots[1].lexeme.lemma, equal_to(u'aç'))
        assert_that(roots[1].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))

    def test_should_create_roots_with_explicit_no_voicing(self):
        roots = self.root_finder.find_roots_for_partial_input(u"ap", u"apa")
        assert_that(roots, has_length(1))
        assert_that(roots[0].str, equal_to(u'ap'))
        assert_that(roots[0].lexeme.root, equal_to(u'ap'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'ap'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[0].lexeme.attributes, equal_to({LexemeAttribute.NoVoicing}))

        roots = self.root_finder.find_roots_for_partial_input(u"at", u"atana")
        assert_that(roots, has_length(1))
        assert_that(roots[0].str, equal_to(u'at'))
        assert_that(roots[0].lexeme.root, equal_to(u'at'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'at'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[0].lexeme.attributes, equal_to({LexemeAttribute.NoVoicing}))

        roots = self.root_finder.find_roots_for_partial_input(u"ak", u"aka")
        assert_that(roots, has_length(1))
        assert_that(roots[0].str, equal_to(u'ak'))
        assert_that(roots[0].lexeme.root, equal_to(u'ak'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'ak'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[0].lexeme.attributes, equal_to({LexemeAttribute.NoVoicing}))

        roots = self.root_finder.find_roots_for_partial_input(u"aç", u"açarak")
        assert_that(roots, has_length(1))
        assert_that(roots[0].str, equal_to(u'aç'))
        assert_that(roots[0].lexeme.root, equal_to(u'aç'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'aç'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[0].lexeme.attributes, equal_to({LexemeAttribute.NoVoicing}))

    def test_should_create_roots_with_inverse_harmony_when_vowel_is_next_letter(self):
        roots = self.root_finder.find_roots_for_partial_input(u"ab", u"abe")
        assert_that(roots, has_length(2))
        assert_that(roots[0].str, equal_to(u'ab'))
        assert_that(roots[0].lexeme.root, equal_to(u'ab'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'ab'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[0].lexeme.attributes, equal_to({LexemeAttribute.InverseHarmony}))
        assert_that(roots[1].str, equal_to(u'ab'))
        assert_that(roots[1].lexeme.root, equal_to(u'ap'))
        assert_that(roots[1].lexeme.lemma, equal_to(u'ap'))
        assert_that(roots[1].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[1].lexeme.attributes, equal_to({LexemeAttribute.InverseHarmony}))

        roots = self.root_finder.find_roots_for_partial_input(u"hal", u"halimden")
        assert_that(roots, has_length(1))
        assert_that(roots[0].str, equal_to(u'hal'))
        assert_that(roots[0].lexeme.root, equal_to(u'hal'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'hal'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[0].lexeme.attributes, equal_to({LexemeAttribute.InverseHarmony}))

        roots = self.root_finder.find_roots_for_partial_input(u"oy", u"oyümü")
        assert_that(roots, has_length(1))
        assert_that(roots[0].str, equal_to(u'oy'))
        assert_that(roots[0].lexeme.root, equal_to(u'oy'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'oy'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[0].lexeme.attributes, equal_to({LexemeAttribute.InverseHarmony}))

        roots = self.root_finder.find_roots_for_partial_input(u"yup", u"yupö")
        assert_that(roots, has_length(1))
        assert_that(roots[0].str, equal_to(u'yup'))
        assert_that(roots[0].lexeme.root, equal_to(u'yup'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'yup'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[0].lexeme.attributes, equal_to({LexemeAttribute.InverseHarmony, LexemeAttribute.NoVoicing}))

    def test_should_create_roots_with_inverse_harmony_when_vowel_is_the_letter_after_next_letter(self):
        roots = self.root_finder.find_roots_for_partial_input(u"ab", u"abdeki")
        assert_that(roots, has_length(1))
        assert_that(roots[0].str, equal_to(u'ab'))
        assert_that(roots[0].lexeme.root, equal_to(u'ab'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'ab'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[0].lexeme.attributes, equal_to({LexemeAttribute.InverseHarmony}))

        roots = self.root_finder.find_roots_for_partial_input(u"hal", u"haldik")
        assert_that(roots, has_length(1))
        assert_that(roots[0].str, equal_to(u'hal'))
        assert_that(roots[0].lexeme.root, equal_to(u'hal'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'hal'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[0].lexeme.attributes, equal_to({LexemeAttribute.InverseHarmony}))

        roots = self.root_finder.find_roots_for_partial_input(u"oy", u"oypü")
        assert_that(roots, has_length(1))
        assert_that(roots[0].str, equal_to(u'oy'))
        assert_that(roots[0].lexeme.root, equal_to(u'oy'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'oy'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[0].lexeme.attributes, equal_to({LexemeAttribute.InverseHarmony}))

        roots = self.root_finder.find_roots_for_partial_input(u"yup", u"yupsö")
        assert_that(roots, has_length(1))
        assert_that(roots[0].str, equal_to(u'yup'))
        assert_that(roots[0].lexeme.root, equal_to(u'yup'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'yup'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[0].lexeme.attributes, equal_to({LexemeAttribute.InverseHarmony}))

    def test_should_create_roots_with_inverse_harmony_when_vowel_is_the_letter_two_after_next_letter(self):
        ## the ones below doesn't make sense, since no suffix can have the form
        ## Consonant+Consontant+Vowel applied when the root ends with a vowel.
        ## supported just in case that there is such a form I can't think of

        roots = self.root_finder.find_roots_for_partial_input(u"ab", u"abrzeklm")
        assert_that(roots, has_length(1))
        assert_that(roots[0].str, equal_to(u'ab'))
        assert_that(roots[0].lexeme.root, equal_to(u'ab'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'ab'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[0].lexeme.attributes, equal_to({LexemeAttribute.InverseHarmony}))

        roots = self.root_finder.find_roots_for_partial_input(u"hal", u"haltdi")
        assert_that(roots, has_length(1))
        assert_that(roots[0].str, equal_to(u'hal'))
        assert_that(roots[0].lexeme.root, equal_to(u'hal'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'hal'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[0].lexeme.attributes, equal_to({LexemeAttribute.InverseHarmony}))

        roots = self.root_finder.find_roots_for_partial_input(u"oy", u"oykpüxyz")
        assert_that(roots, has_length(1))
        assert_that(roots[0].str, equal_to(u'oy'))
        assert_that(roots[0].lexeme.root, equal_to(u'oy'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'oy'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[0].lexeme.attributes, equal_to({LexemeAttribute.InverseHarmony}))

        roots = self.root_finder.find_roots_for_partial_input(u"yup", u"yupfsö")
        assert_that(roots, has_length(1))
        assert_that(roots[0].str, equal_to(u'yup'))
        assert_that(roots[0].lexeme.root, equal_to(u'yup'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'yup'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[0].lexeme.attributes, equal_to({LexemeAttribute.InverseHarmony}))

    def test_should_create_roots_with_inverse_harmony_and_explicit_no_voicing(self):
        roots = self.root_finder.find_roots_for_partial_input(u"ap", u"ape")
        assert_that(roots, has_length(1))
        assert_that(roots[0].str, equal_to(u'ap'))
        assert_that(roots[0].lexeme.root, equal_to(u'ap'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'ap'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[0].lexeme.attributes, equal_to({LexemeAttribute.InverseHarmony, LexemeAttribute.NoVoicing}))

        roots = self.root_finder.find_roots_for_partial_input(u"yot", u"yotüne")
        assert_that(roots, has_length(1))
        assert_that(roots[0].str, equal_to(u'yot'))
        assert_that(roots[0].lexeme.root, equal_to(u'yot'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'yot'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[0].lexeme.attributes, equal_to({LexemeAttribute.InverseHarmony, LexemeAttribute.NoVoicing}))

        roots = self.root_finder.find_roots_for_partial_input(u"ak", u"akimi")
        assert_that(roots, has_length(1))
        assert_that(roots[0].str, equal_to(u'ak'))
        assert_that(roots[0].lexeme.root, equal_to(u'ak'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'ak'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[0].lexeme.attributes, equal_to({LexemeAttribute.InverseHarmony, LexemeAttribute.NoVoicing}))

        roots = self.root_finder.find_roots_for_partial_input(u"kuç", u"kuçö")
        assert_that(roots, has_length(1))
        assert_that(roots[0].str, equal_to(u'kuç'))
        assert_that(roots[0].lexeme.root, equal_to(u'kuç'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'kuç'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[0].lexeme.attributes, equal_to({LexemeAttribute.InverseHarmony, LexemeAttribute.NoVoicing}))


    def test_should_create_roots_with_doubling(self):
        # simple doubling
        roots = self.root_finder.find_roots_for_partial_input(u"hiss", u"hissi")
        assert_that(roots, has_length(2))
        assert_that(roots[0].str, equal_to(u'hiss'))
        assert_that(roots[0].lexeme.root, equal_to(u'hiss'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'hiss'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[0].lexeme.attributes, equal_to(set([])))
        assert_that(roots[1].str, equal_to(u'hiss'))
        assert_that(roots[1].lexeme.root, equal_to(u'his'))
        assert_that(roots[1].lexeme.lemma, equal_to(u'his'))
        assert_that(roots[1].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[1].lexeme.attributes, equal_to({LexemeAttribute.Doubling}))

        # doubling with Voicing and NoVoicing
        roots = self.root_finder.find_roots_for_partial_input(u"tıbb", u"tıbbın")
        assert_that(roots, has_length(3))
        assert_that(roots[0].str, equal_to(u'tıbb'))
        assert_that(roots[0].lexeme.root, equal_to(u'tıbb'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'tıbb'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[0].lexeme.attributes, equal_to(set([])))
        assert_that(roots[1].str, equal_to(u'tıbb'))
        assert_that(roots[1].lexeme.root, equal_to(u'tıb'))
        assert_that(roots[1].lexeme.lemma, equal_to(u'tıb'))
        assert_that(roots[1].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[1].lexeme.attributes, equal_to({LexemeAttribute.Doubling}))
        assert_that(roots[2].str, equal_to(u'tıbb'))
        assert_that(roots[2].lexeme.root, equal_to(u'tıp'))
        assert_that(roots[2].lexeme.lemma, equal_to(u'tıp'))
        assert_that(roots[2].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[2].lexeme.attributes, equal_to({LexemeAttribute.Doubling}))

        # doubling with NoVoicing
        roots = self.root_finder.find_roots_for_partial_input(u"hakk", u"hakka")
        assert_that(roots, has_length(2))
        assert_that(roots[0].str, equal_to(u'hakk'))
        assert_that(roots[0].lexeme.root, equal_to(u'hakk'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'hakk'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[0].lexeme.attributes, equal_to({LexemeAttribute.NoVoicing}))
        assert_that(roots[1].str, equal_to(u'hakk'))
        assert_that(roots[1].lexeme.root, equal_to(u'hak'))
        assert_that(roots[1].lexeme.lemma, equal_to(u'hak'))
        assert_that(roots[1].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[1].lexeme.attributes, equal_to({LexemeAttribute.NoVoicing, LexemeAttribute.Doubling}))

        # doubling with no {Voicing and NoVoicing} and InverseHarmony
        roots = self.root_finder.find_roots_for_partial_input(u"hall", u"hallini")
        assert_that(roots, has_length(2))
        assert_that(roots[0].str, equal_to(u'hall'))
        assert_that(roots[0].lexeme.root, equal_to(u'hall'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'hall'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[0].lexeme.attributes, equal_to({LexemeAttribute.InverseHarmony}))
        assert_that(roots[1].str, equal_to(u'hall'))
        assert_that(roots[1].lexeme.root, equal_to(u'hal'))
        assert_that(roots[1].lexeme.lemma, equal_to(u'hal'))
        assert_that(roots[1].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[1].lexeme.attributes, equal_to({LexemeAttribute.Doubling, LexemeAttribute.InverseHarmony}))

        # doubling with {Voicing and NoVoicing} and {InverseHarmony}
        # ignore the case "serhadt"
        roots = self.root_finder.find_roots_for_partial_input(u"serhadd", u"serhaddime")
        assert_that(roots, has_length(3))
        assert_that(roots[0].str, equal_to(u'serhadd'))
        assert_that(roots[0].lexeme.root, equal_to(u'serhadd'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'serhadd'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[0].lexeme.attributes, equal_to({LexemeAttribute.InverseHarmony}))
        assert_that(roots[1].str, equal_to(u'serhadd'))
        assert_that(roots[1].lexeme.root, equal_to(u'serhad'))
        assert_that(roots[1].lexeme.lemma, equal_to(u'serhad'))
        assert_that(roots[1].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[1].lexeme.attributes, equal_to({LexemeAttribute.Doubling, LexemeAttribute.InverseHarmony}))
        assert_that(roots[2].str, equal_to(u'serhadd'))
        assert_that(roots[2].lexeme.root, equal_to(u'serhat'))
        assert_that(roots[2].lexeme.lemma, equal_to(u'serhat'))
        assert_that(roots[2].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[2].lexeme.attributes, equal_to({LexemeAttribute.Doubling, LexemeAttribute.InverseHarmony}))


class BruteForceCompoundNounRootFinderTest(unittest.TestCase):
    def setUp(self):
        self.root_finder = BruteForceCompoundNounRootFinder()

    def test_should_check_invalid_cases(self):
        f = lambda: self.root_finder.find_roots_for_partial_input(None, None)
        self.assertRaises(AssertionError, f)

        f = lambda: self.root_finder.find_roots_for_partial_input("", None)
        self.assertRaises(AssertionError, f)

        f = lambda: self.root_finder.find_roots_for_partial_input(None, "")
        self.assertRaises(AssertionError, f)

        f = lambda: self.root_finder.find_roots_for_partial_input("", "")
        self.assertRaises(AssertionError, f)

        f = lambda: self.root_finder.find_roots_for_partial_input(u"a", None)
        self.assertRaises(AssertionError, f)

        f = lambda: self.root_finder.find_roots_for_partial_input(u"a", u"")
        self.assertRaises(AssertionError, f)

        f = lambda: self.root_finder.find_roots_for_partial_input(u"ab", u"a")
        self.assertRaises(AssertionError, f)

        f = lambda: self.root_finder.find_roots_for_partial_input(u"ab", u"ad")
        self.assertRaises(AssertionError, f)

        f = lambda: self.root_finder.find_roots_for_partial_input(u"ab", u"ada")
        self.assertRaises(AssertionError, f)

    def test_should_find_no_roots(self):
        roots = self.root_finder.find_roots_for_partial_input(u"abc", u"abcdef")
        assert_that(roots, has_length(0))

        roots = self.root_finder.find_roots_for_partial_input(u"a", u"anu")
        assert_that(roots, has_length(0))

        roots = self.root_finder.find_roots_for_partial_input(u"an", u"anu")
        assert_that(roots, has_length(0))

        roots = self.root_finder.find_roots_for_partial_input(u"anu", u"anu")
        assert_that(roots, has_length(0))

        roots = self.root_finder.find_roots_for_partial_input(u"a", u"anun")
        assert_that(roots, has_length(0))

        roots = self.root_finder.find_roots_for_partial_input(u"an", u"anun")
        assert_that(roots, has_length(0))

        roots = self.root_finder.find_roots_for_partial_input(u"anu", u"anun")
        assert_that(roots, has_length(0))

        roots = self.root_finder.find_roots_for_partial_input(u"anun", u"anun")
        assert_that(roots, has_length(0))

        roots = self.root_finder.find_roots_for_partial_input(u"t", u"tatın")
        assert_that(roots, has_length(0))

        roots = self.root_finder.find_roots_for_partial_input(u"ta", u"tatın")
        assert_that(roots, has_length(0))

        roots = self.root_finder.find_roots_for_partial_input(u"tat", u"tatın")
        assert_that(roots, has_length(0))

        roots = self.root_finder.find_roots_for_partial_input(u"tatı", u"tatın")
        assert_that(roots, has_length(0))

        roots = self.root_finder.find_roots_for_partial_input(u"tatın", u"tatın")
        assert_that(roots, has_length(0))

        roots = self.root_finder.find_roots_for_partial_input(u"suborusu", u"suborusun")
        assert_that(roots, has_length(0))

    def test_should_create_roots_without_consontant_insertion_s(self):
        # most of the following words are made up!

        # no orthographic changes, no consontant insertion 's'
        roots = self.root_finder.find_roots_for_partial_input(u"bacakkalemi", u"bacakkalemini")
        assert_that(roots, has_length(1))
        assert_that(roots[0].str, equal_to(u'bacakkalem'))
        assert_that(roots[0].lexeme.root, equal_to(u'bacakkalemi'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'bacakkalemi'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[0].lexeme.attributes, equal_to({LexemeAttribute.CompoundP3sg}))

        # with explicit NoVoicing
        roots = self.root_finder.find_roots_for_partial_input(u"adamotu", u"adamotunu")
        assert_that(roots, has_length(1))
        assert_that(roots[0].str, equal_to(u'adamot'))
        assert_that(roots[0].lexeme.root, equal_to(u'adamotu'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'adamotu'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[0].lexeme.attributes, equal_to({LexemeAttribute.CompoundP3sg, LexemeAttribute.NoVoicing}))

        # with possible voicing
        roots = self.root_finder.find_roots_for_partial_input(u"aslankuyruğu", u"aslankuyruğundan")
        assert_that(roots, has_length(3))
        assert_that(roots[0].str, equal_to(u'aslankuyruğ'))
        assert_that(roots[0].lexeme.root, equal_to(u'aslankuyruğu'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'aslankuyruğu'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[0].lexeme.attributes, equal_to({LexemeAttribute.CompoundP3sg}))
        assert_that(roots[1].str, equal_to(u'aslankuyrug'))
        assert_that(roots[1].lexeme.root, equal_to(u'aslankuyruğu'))
        assert_that(roots[1].lexeme.lemma, equal_to(u'aslankuyruğu'))
        assert_that(roots[1].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[1].lexeme.attributes, equal_to({LexemeAttribute.CompoundP3sg}))
        assert_that(roots[2].str, equal_to(u'aslankuyruk'))
        assert_that(roots[2].lexeme.root, equal_to(u'aslankuyruğu'))
        assert_that(roots[2].lexeme.lemma, equal_to(u'aslankuyruğu'))
        assert_that(roots[2].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[2].lexeme.attributes, equal_to({LexemeAttribute.CompoundP3sg}))

        # with InverseHarmony
        roots = self.root_finder.find_roots_for_partial_input(u"dünyahali", u"dünyahaline")
        assert_that(roots, has_length(1))
        assert_that(roots[0].str, equal_to(u'dünyahal'))
        assert_that(roots[0].lexeme.root, equal_to(u'dünyahali'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'dünyahali'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[0].lexeme.attributes,
            equal_to({LexemeAttribute.CompoundP3sg, LexemeAttribute.InverseHarmony}))

        # with InverseHarmony and possible voicing
        roots = self.root_finder.find_roots_for_partial_input(u"abcvaadi", u"abcvaadini")
        assert_that(roots, has_length(2))
        assert_that(roots[0].str, equal_to(u'abcvaad'))
        assert_that(roots[0].lexeme.root, equal_to(u'abcvaadi'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'abcvaadi'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[0].lexeme.attributes,
            equal_to({LexemeAttribute.CompoundP3sg, LexemeAttribute.InverseHarmony}))
        assert_that(roots[1].str, equal_to(u'abcvaat'))
        assert_that(roots[1].lexeme.root, equal_to(u'abcvaadi'))
        assert_that(roots[1].lexeme.lemma, equal_to(u'abcvaadi'))
        assert_that(roots[1].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[1].lexeme.attributes,
            equal_to({LexemeAttribute.CompoundP3sg, LexemeAttribute.InverseHarmony}))

        # with InverseHarmony and explicit NoVoicing
        roots = self.root_finder.find_roots_for_partial_input(u"anaşefkati", u"anaşefkatini")
        assert_that(roots, has_length(1))
        assert_that(roots[0].str, equal_to(u'anaşefkat'))
        assert_that(roots[0].lexeme.root, equal_to(u'anaşefkati'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'anaşefkati'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[0].lexeme.attributes,
            equal_to({LexemeAttribute.CompoundP3sg, LexemeAttribute.InverseHarmony, LexemeAttribute.NoVoicing}))

        # with doubling
        roots = self.root_finder.find_roots_for_partial_input(u"gönülsırrı", u"gönülsırrına")
        assert_that(roots, has_length(2))
        assert_that(roots[0].str, equal_to(u'gönülsırr'))
        assert_that(roots[0].lexeme.root, equal_to(u'gönülsırrı'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'gönülsırrı'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[0].lexeme.attributes, equal_to({LexemeAttribute.CompoundP3sg}))
        assert_that(roots[1].str, equal_to(u'gönülsır'))
        assert_that(roots[1].lexeme.root, equal_to(u'gönülsırrı'))
        assert_that(roots[1].lexeme.lemma, equal_to(u'gönülsırrı'))
        assert_that(roots[1].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[1].lexeme.attributes, equal_to({LexemeAttribute.CompoundP3sg, LexemeAttribute.Doubling}))

        # with doubling and explicit NoVoicing
        roots = self.root_finder.find_roots_for_partial_input(u"müşterihakkı", u"müşterihakkına")
        assert_that(roots, has_length(2))
        assert_that(roots[0].str, equal_to(u'müşterihakk'))
        assert_that(roots[0].lexeme.root, equal_to(u'müşterihakkı'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'müşterihakkı'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[0].lexeme.attributes, equal_to({LexemeAttribute.CompoundP3sg, LexemeAttribute.NoVoicing}))
        assert_that(roots[1].str, equal_to(u'müşterihak'))
        assert_that(roots[1].lexeme.root, equal_to(u'müşterihakkı'))
        assert_that(roots[1].lexeme.lemma, equal_to(u'müşterihakkı'))
        assert_that(roots[1].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[1].lexeme.attributes,
            equal_to({LexemeAttribute.CompoundP3sg, LexemeAttribute.NoVoicing, LexemeAttribute.Doubling}))

        # with doubling and InverseHarmony
        roots = self.root_finder.find_roots_for_partial_input(u"olaymahalli", u"olaymahalline")
        assert_that(roots, has_length(2))
        assert_that(roots[0].str, equal_to(u'olaymahall'))
        assert_that(roots[0].lexeme.root, equal_to(u'olaymahalli'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'olaymahalli'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[0].lexeme.attributes,
            equal_to({LexemeAttribute.CompoundP3sg, LexemeAttribute.InverseHarmony}))
        assert_that(roots[1].str, equal_to(u'olaymahal'))
        assert_that(roots[1].lexeme.root, equal_to(u'olaymahalli'))
        assert_that(roots[1].lexeme.lemma, equal_to(u'olaymahalli'))
        assert_that(roots[1].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[1].lexeme.attributes,
            equal_to({LexemeAttribute.CompoundP3sg, LexemeAttribute.InverseHarmony, LexemeAttribute.Doubling}))

        # with doubling, possible voicing and inverse harmony
        roots = self.root_finder.find_roots_for_partial_input(u"yaşhaddi", u"yaşhaddinden")
        assert_that(roots, has_length(3))
        assert_that(roots[0].str, equal_to(u'yaşhadd'))
        assert_that(roots[0].lexeme.root, equal_to(u'yaşhaddi'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'yaşhaddi'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[0].lexeme.attributes,
            equal_to({LexemeAttribute.CompoundP3sg, LexemeAttribute.InverseHarmony}))
        assert_that(roots[1].str, equal_to(u'yaşhad'))
        assert_that(roots[1].lexeme.root, equal_to(u'yaşhaddi'))
        assert_that(roots[1].lexeme.lemma, equal_to(u'yaşhaddi'))
        assert_that(roots[1].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[1].lexeme.attributes,
            equal_to({LexemeAttribute.CompoundP3sg, LexemeAttribute.InverseHarmony, LexemeAttribute.Doubling}))
        assert_that(roots[2].str, equal_to(u'yaşhat'))
        assert_that(roots[2].lexeme.root, equal_to(u'yaşhaddi'))
        assert_that(roots[2].lexeme.lemma, equal_to(u'yaşhaddi'))
        assert_that(roots[2].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[2].lexeme.attributes,
            equal_to({LexemeAttribute.CompoundP3sg, LexemeAttribute.InverseHarmony, LexemeAttribute.Doubling}))

    def test_should_create_roots_with_consontant_insertion_s(self):
        # most of the following words are made up!
        roots = self.root_finder.find_roots_for_partial_input(u"suborusu", u"suborusuna")
        assert_that(roots, has_length(2))
        assert_that(roots[0].str, equal_to(u'suborus'))
        assert_that(roots[0].lexeme.root, equal_to(u'suborusu'))
        assert_that(roots[0].lexeme.lemma, equal_to(u'suborusu'))
        assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[0].lexeme.attributes, equal_to({LexemeAttribute.CompoundP3sg}))
        assert_that(roots[1].str, equal_to(u'suboru'))
        assert_that(roots[1].lexeme.root, equal_to(u'suborusu'))
        assert_that(roots[1].lexeme.lemma, equal_to(u'suborusu'))
        assert_that(roots[1].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        assert_that(roots[1].lexeme.attributes, equal_to({LexemeAttribute.CompoundP3sg}))

        # InverseHarmony and consonant 's' doesn't work together.
        # Compound gets the 's' if it ends with a vowel.
        # However, a word ending with a vowel cannot have InverseHarmony.
        # Thus, this is an invalid case!
        #roots = self.root_finder.find_roots_for_partial_input(u"abcdesı", u"abcdesına")
        #assert_that(roots, has_length(2))
        #assert_that(roots[0].str, equal_to(u'abcdes'))
        #assert_that(roots[0].lexeme.root, equal_to(u'abcdesı'))
        #assert_that(roots[0].lexeme.lemma, equal_to(u'abcdesı'))
        #assert_that(roots[0].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        #assert_that(roots[0].lexeme.attributes, equal_to({LexemeAttribute.CompoundP3sg, LexemeAttribute.InverseHarmony}))
        #assert_that(roots[1].str, equal_to(u'abcde'))
        #assert_that(roots[1].lexeme.root, equal_to(u'abcdesı'))
        #assert_that(roots[1].lexeme.lemma, equal_to(u'abcdesı'))
        #assert_that(roots[1].lexeme.syntactic_category, equal_to(SyntacticCategory.NOUN))
        #assert_that(roots[1].lexeme.attributes, equal_to({LexemeAttribute.CompoundP3sg, LexemeAttribute.InverseHarmony}))

if __name__ == '__main__':
    unittest.main()
