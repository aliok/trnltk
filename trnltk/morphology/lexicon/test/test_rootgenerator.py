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
from trnltk.morphology.phonetics.phonetics import PhoneticAttributes, PhoneticExpectation
from trnltk.morphology.model.lexeme import Lexeme, SyntacticCategory, LexemeAttribute
from trnltk.morphology.lexicon.rootgenerator import RootGenerator, Root, CircumflexConvertingRootGenerator

LLV = PhoneticAttributes.LastLetterVowel
LLC = PhoneticAttributes.LastLetterConsonant

LVR = PhoneticAttributes.LastVowelRounded
LVU = PhoneticAttributes.LastVowelUnrounded
LVF = PhoneticAttributes.LastVowelFrontal
LVB = PhoneticAttributes.LastVowelBack

LLCont =  PhoneticAttributes.LastLetterContinuant
LLNotCont =  PhoneticAttributes.LastLetterNotContinuant

LLVless =  PhoneticAttributes.LastLetterVoiceless
LLVStop = PhoneticAttributes.LastLetterVoicedStop
LLVlessStop = PhoneticAttributes.LastLetterVoicelessStop
LLNotVless =  PhoneticAttributes.LastLetterNotVoiceless

class RootGeneratorTest(unittest.TestCase):
    def test_should_generate_with_no_modifiers(self):
        lexeme = Lexeme(u"elma", u"elma", SyntacticCategory.NOUN, None, None)
        generated_roots = RootGenerator.generate(lexeme)
        assert_that(generated_roots, has_length(1))
        assert_that(generated_roots, has_item(Root(u'elma', lexeme, None, {LLNotCont, LLV, LVB, LLNotVless, LVU})))

        lexeme = Lexeme(u"kek", u"kek", SyntacticCategory.NOUN, None, {LexemeAttribute.NoVoicing})
        generated_roots = RootGenerator.generate(lexeme)
        assert_that(generated_roots, has_length(1))
        assert_that(generated_roots, has_item(Root(u'kek', lexeme, None, {LLNotCont, LVF, LLC, LLVless, LLVlessStop, LVU})))

    def test_should_generate_with_voicing(self):
        lexeme = Lexeme(u"armut", u"armut", SyntacticCategory.NOUN, None, {LexemeAttribute.Voicing})
        generated_roots = RootGenerator.generate(lexeme)
        assert_that(generated_roots, has_length(2))
        assert_that(generated_roots, has_item(Root(u'armut', lexeme, {PhoneticExpectation.ConsonantStart}, {LLNotCont, LVB, LLC, LLVless, LLVlessStop, LVR})))
        assert_that(generated_roots, has_item(Root(u'armud', lexeme, {PhoneticExpectation.VowelStart}, {LLNotCont, LVB, LLC, LLVless, LVR})))

        lexeme = Lexeme(u"kapak", u"kapak", SyntacticCategory.NOUN, None, {LexemeAttribute.Voicing})
        generated_roots = RootGenerator.generate(lexeme)
        assert_that(generated_roots, has_length(2))
        assert_that(generated_roots, has_item(Root(u'kapak', lexeme, {PhoneticExpectation.ConsonantStart}, {LLNotCont, LVB, LLC, LLVless, LLVlessStop, LVU})))
        assert_that(generated_roots, has_item(Root(u'kapağ', lexeme, {PhoneticExpectation.VowelStart}, {LLCont, LVB, LLC, LLVless, LVU})))

        lexeme = Lexeme(u"cenk", u"cenk", SyntacticCategory.NOUN, None, {LexemeAttribute.Voicing})
        generated_roots = RootGenerator.generate(lexeme)
        assert_that(generated_roots, has_length(2))
        assert_that(generated_roots, has_item(Root(u'cenk', lexeme, {PhoneticExpectation.ConsonantStart}, {LLNotCont, LVF, LLC, LLVless, LLVlessStop, LVU})))
        assert_that(generated_roots, has_item(Root(u'ceng', lexeme, {PhoneticExpectation.VowelStart}, {LLNotCont, LVF, LLC, LLVless, LVU})))

        lexeme = Lexeme(u"kap", u"kap", SyntacticCategory.NOUN, None, {LexemeAttribute.Voicing})
        generated_roots = RootGenerator.generate(lexeme)
        assert_that(generated_roots, has_length(2))
        assert_that(generated_roots, has_item(Root(u'kap', lexeme, {PhoneticExpectation.ConsonantStart}, {LLNotCont, LVB, LLC, LLVless, LLVlessStop, LVU})))
        assert_that(generated_roots, has_item(Root(u'kab', lexeme, {PhoneticExpectation.VowelStart}, {LLNotCont, LVB, LLC, LLVless, LVU})))

    def test_should_generate_with_last_vowel_drop(self):
        lexeme = Lexeme(u"ağız", u"ağız", SyntacticCategory.NOUN, None, {LexemeAttribute.LastVowelDrop})
        generated_roots = RootGenerator.generate(lexeme)
        assert_that(generated_roots, has_length(2))
        assert_that(generated_roots, has_item(Root(u"ağız", lexeme, {PhoneticExpectation.ConsonantStart}, {LLCont, LVB, LLC, LLNotVless, LVU})))
        assert_that(generated_roots, has_item(Root(u"ağz", lexeme, {PhoneticExpectation.VowelStart}, {LLCont, LVB, LLC, LLNotVless, LVU})))

        lexeme = Lexeme(u"ahit", u"ahit", SyntacticCategory.NOUN, None, {LexemeAttribute.LastVowelDrop, LexemeAttribute.Voicing})
        generated_roots = RootGenerator.generate(lexeme)
        assert_that(generated_roots, has_length(2))
        assert_that(generated_roots, has_item(Root(u"ahit", lexeme, {PhoneticExpectation.ConsonantStart}, {LLNotCont, LVF, LLC, LLVless, LLVlessStop, LVU})))
        assert_that(generated_roots, has_item(Root(u"ahd", lexeme, {PhoneticExpectation.VowelStart}, {LLNotCont, LVF, LLVless, LLC, LVU})))

    def test_should_generate_with_doubling(self):
        lexeme = Lexeme(u"hac", u"hac", SyntacticCategory.NOUN, None, {LexemeAttribute.Doubling})
        generated_roots = RootGenerator.generate(lexeme)
        assert_that(generated_roots, has_length(2))
        assert_that(generated_roots, has_item(Root(u"hac", lexeme, {PhoneticExpectation.ConsonantStart}, {LLNotCont, LLVStop, LVB, LLC, LLNotVless, LVU})))
        assert_that(generated_roots, has_item(Root(u"hacc", lexeme, {PhoneticExpectation.VowelStart}, {LLNotCont, LLVStop, LVB, LLC, LLNotVless, LVU})))

        lexeme = Lexeme(u"ret", u"ret", SyntacticCategory.NOUN, None, {LexemeAttribute.Voicing, LexemeAttribute.Doubling})
        generated_roots = RootGenerator.generate(lexeme)
        assert_that(generated_roots, has_length(2))
        assert_that(generated_roots, has_item(Root(u"ret", lexeme, {PhoneticExpectation.ConsonantStart}, {LLNotCont, LVF, LLC, LLVless, LLVlessStop, LVU})))
        assert_that(generated_roots, has_item(Root(u"redd", lexeme, {PhoneticExpectation.VowelStart}, {LLNotCont, LVF, LLC, LLVless, LVU})))

    def test_should_generate_with_progressive_vowel_drop(self):
        lexeme = Lexeme(u"atamak", u"ata", SyntacticCategory.VERB, None, {LexemeAttribute.ProgressiveVowelDrop})
        generated_roots = RootGenerator.generate(lexeme)
        assert_that(generated_roots, has_length(2))
        assert_that(generated_roots, has_item(Root(u"ata", lexeme, None, {LLNotCont, LVB, LLV, LLNotVless, LVU})))
        assert_that(generated_roots, has_item(Root(u"at", lexeme, {PhoneticExpectation.VowelStart}, {LLNotCont, LVB, LLC, LLVless, LLVlessStop, LVU})))

    def test_should_generate_with_inverse_harmony(self):
        lexeme = Lexeme(u"kemal", u"kemal", SyntacticCategory.NOUN, None, {LexemeAttribute.InverseHarmony})
        generated_roots = RootGenerator.generate(lexeme)
        assert_that(generated_roots, has_length(1))
        assert_that(generated_roots, has_item(Root(u"kemal", lexeme, None, {LLCont, LVF, LLC, LLNotVless, LVU})))

        lexeme = Lexeme(u"kanaat", u"kanaat", SyntacticCategory.NOUN, None, {LexemeAttribute.NoVoicing, LexemeAttribute.InverseHarmony})
        generated_roots = RootGenerator.generate(lexeme)
        assert_that(generated_roots, has_length(1))
        assert_that(generated_roots, has_item(Root(u"kanaat", lexeme, None, {LLNotCont, LVF, LLC, LLVless, LLVlessStop, LVU})))

    def test_should_generate_converting_circumflexes(self):
        lexeme = Lexeme(u"rüzgâr", u"rüzgâr", SyntacticCategory.NOUN, None, None)
        generated_roots = CircumflexConvertingRootGenerator.generate(lexeme)
        assert_that(generated_roots, has_length(2))
        assert_that(generated_roots, has_item(Root(u"rüzgar", lexeme, None, {LLCont, LVB, LLC, LLNotVless, LVU})))
        assert_that(generated_roots, has_item(Root(u"rüzgâr", lexeme, None, {LLCont,LVB, LLC, LLNotVless, LVU})))

        lexeme = Lexeme(u"alenî", u"alenî", SyntacticCategory.ADJECTIVE, None, None)
        generated_roots = CircumflexConvertingRootGenerator.generate(lexeme)
        assert_that(generated_roots, has_length(2))
        assert_that(generated_roots, has_item(Root(u"aleni", lexeme, None, {LLNotCont,LVF, LLV, LLNotVless, LVU})))
        assert_that(generated_roots, has_item(Root(u"alenî", lexeme, None, {LLNotCont,LVF, LLV, LLNotVless, LVU})))

        lexeme = Lexeme(u"cülûs", u"cülûs", SyntacticCategory.NOUN, None, None)
        generated_roots = CircumflexConvertingRootGenerator.generate(lexeme)
        assert_that(generated_roots, has_length(2))
        assert_that(generated_roots, has_item(Root(u"cülus", lexeme, None, {LLCont,LVB, LLC, LLVless, LVR})))
        assert_that(generated_roots, has_item(Root(u"cülûs", lexeme, None, {LLCont,LVB, LLC, LLVless, LVR})))

        lexeme = Lexeme(u"Âdem", u"Âdem", SyntacticCategory.NOUN, None, None)
        generated_roots = CircumflexConvertingRootGenerator.generate(lexeme)
        assert_that(generated_roots, has_length(2))
        assert_that(generated_roots, has_item(Root(u"Adem", lexeme, None, {LLCont,LVF, LLC, LLNotVless, LVU})))
        assert_that(generated_roots, has_item(Root(u"Âdem", lexeme, None, {LLCont,LVF, LLC, LLNotVless, LVU})))

    def test_should_generate_verbs_with_voicing_and_novoicing(self):
        lexeme = Lexeme(u"gitmek", u"git", SyntacticCategory.VERB, None, {LexemeAttribute.Voicing})
        generated_roots = RootGenerator.generate(lexeme)
        assert_that(generated_roots, has_length(2))
        assert_that(generated_roots, has_item(Root(u'git', lexeme, {PhoneticExpectation.ConsonantStart}, {LLNotCont, LVF, LLC, LLVless, LLVlessStop, LVU})))
        assert_that(generated_roots, has_item(Root(u'gid', lexeme, {PhoneticExpectation.VowelStart}, {LLNotCont, LVF, LLC, LLVless, LVU})))

        lexeme = Lexeme(u"sürtmek", u"sürt", SyntacticCategory.VERB, None, None)
        generated_roots = RootGenerator.generate(lexeme)
        assert_that(generated_roots, has_length(1))
        assert_that(generated_roots, has_item(Root(u'sürt', lexeme, None, {LLNotCont, LVF, LLC, LLVless, LLVlessStop, LVR})))


if __name__ == '__main__':
    unittest.main()