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
from trnltk.morphology.model.lexeme import Lexeme, SyntacticCategory, RootAttribute
from trnltk.morphology.lexicon.rootgenerator import RootGenerator, Root, CircumflexConvertingRootGenerator

LLV = PhoneticAttributes.LastLetterVowel
LLC = PhoneticAttributes.LastLetterConsonant

LVR = PhoneticAttributes.LastVowelRounded
LVU = PhoneticAttributes.LastVowelUnrounded
LVF = PhoneticAttributes.LastVowelFrontal
LVB = PhoneticAttributes.LastVowelBack

LLVless =  PhoneticAttributes.LastLetterVoiceless
LLVlessStop = PhoneticAttributes.LastLetterVoicelessStop
LLNotVless =  PhoneticAttributes.LastLetterNotVoiceless

class RootGeneratorTest(unittest.TestCase):
    def test_should_generate_with_no_modifiers(self):
        lexeme = Lexeme("elma", "elma", SyntacticCategory.NOUN, None, None)
        generated_roots = RootGenerator.generate(lexeme)
        assert_that(generated_roots, has_length(1))
        assert_that(generated_roots, has_item(Root('elma', lexeme, None, {LVB, LLV, LLNotVless, LVU})))

        lexeme = Lexeme("kek", "kek", SyntacticCategory.NOUN, None, [RootAttribute.NoVoicing])
        generated_roots = RootGenerator.generate(lexeme)
        assert_that(generated_roots, has_length(1))
        assert_that(generated_roots, has_item(Root('kek', lexeme, None, {LVF, LLC, LLVless, LLVlessStop, LVU})))

    def test_should_generate_with_voicing(self):
        lexeme = Lexeme("armut", "armut", SyntacticCategory.NOUN, None, [RootAttribute.Voicing])
        generated_roots = RootGenerator.generate(lexeme)
        assert_that(generated_roots, has_length(2))
        assert_that(generated_roots, has_item(Root('armut', lexeme, {PhoneticExpectation.ConsonantStart}, {LVB, LLC, LLVless, LLVlessStop, LVR})))
        assert_that(generated_roots, has_item(Root('armud', lexeme, {PhoneticExpectation.VowelStart}, {LVB, LLC, LLVless, LVR})))

        lexeme = Lexeme("kapak", "kapak", SyntacticCategory.NOUN, None, [RootAttribute.Voicing])
        generated_roots = RootGenerator.generate(lexeme)
        assert_that(generated_roots, has_length(2))
        assert_that(generated_roots, has_item(Root('kapak', lexeme, {PhoneticExpectation.ConsonantStart}, {LVB, LLC, LLVless, LLVlessStop, LVU})))
        assert_that(generated_roots, has_item(Root(u'kapağ', lexeme, {PhoneticExpectation.VowelStart}, {LVB, LLC, LLVless, LVU})))

        lexeme = Lexeme("cenk", "cenk", SyntacticCategory.NOUN, None, [RootAttribute.Voicing])
        generated_roots = RootGenerator.generate(lexeme)
        assert_that(generated_roots, has_length(2))
        assert_that(generated_roots, has_item(Root('cenk', lexeme, {PhoneticExpectation.ConsonantStart}, {LVF, LLC, LLVless, LLVlessStop, LVU})))
        assert_that(generated_roots, has_item(Root('ceng', lexeme, {PhoneticExpectation.VowelStart}, {LVF, LLC, LLVless, LVU})))

        lexeme = Lexeme("kap", "kap", SyntacticCategory.NOUN, None, [RootAttribute.Voicing])
        generated_roots = RootGenerator.generate(lexeme)
        assert_that(generated_roots, has_length(2))
        assert_that(generated_roots, has_item(Root('kap', lexeme, {PhoneticExpectation.ConsonantStart}, {LVB, LLC, LLVless, LLVlessStop, LVU})))
        assert_that(generated_roots, has_item(Root('kab', lexeme, {PhoneticExpectation.VowelStart}, {LVB, LLC, LLVless, LVU})))

    def test_should_generate_with_last_vowel_drop(self):
        lexeme = Lexeme(u"ağız", u"ağız", SyntacticCategory.NOUN, None, [RootAttribute.LastVowelDrop])
        generated_roots = RootGenerator.generate(lexeme)
        assert_that(generated_roots, has_length(2))
        assert_that(generated_roots, has_item(Root(u"ağız", lexeme, {PhoneticExpectation.ConsonantStart}, {LVB, LLC, LLNotVless, LVU})))
        assert_that(generated_roots, has_item(Root(u"ağz", lexeme, {PhoneticExpectation.VowelStart}, {LVB, LLC, LLNotVless, LVU})))

        lexeme = Lexeme(u"ahit", u"ahit", SyntacticCategory.NOUN, None, [RootAttribute.LastVowelDrop, RootAttribute.Voicing])
        generated_roots = RootGenerator.generate(lexeme)
        assert_that(generated_roots, has_length(2))
        assert_that(generated_roots, has_item(Root(u"ahit", lexeme, {PhoneticExpectation.ConsonantStart}, {LVF, LLC, LLVless, LLVlessStop, LVU})))
        assert_that(generated_roots, has_item(Root(u"ahd", lexeme, {PhoneticExpectation.VowelStart}, {LVF, LLVless, LLC, LVU})))

    def test_should_generate_with_doubling(self):
        lexeme = Lexeme(u"hac", u"hac", SyntacticCategory.NOUN, None, [RootAttribute.Doubling])
        generated_roots = RootGenerator.generate(lexeme)
        assert_that(generated_roots, has_length(2))
        assert_that(generated_roots, has_item(Root(u"hac", lexeme, {PhoneticExpectation.ConsonantStart}, {LVB, LLC, LLNotVless, LVU})))
        assert_that(generated_roots, has_item(Root(u"hacc", lexeme, {PhoneticExpectation.VowelStart}, {LVB, LLC, LLNotVless, LVU})))

        lexeme = Lexeme(u"ret", u"ret", SyntacticCategory.NOUN, None, [RootAttribute.Voicing, RootAttribute.Doubling])
        generated_roots = RootGenerator.generate(lexeme)
        assert_that(generated_roots, has_length(2))
        assert_that(generated_roots, has_item(Root(u"ret", lexeme, {PhoneticExpectation.ConsonantStart}, {LVF, LLC, LLVless, LLVlessStop, LVU})))
        assert_that(generated_roots, has_item(Root(u"redd", lexeme, {PhoneticExpectation.VowelStart}, {LVF, LLC, LLVless, LVU})))

    def test_should_generate_with_progressive_vowel_drop(self):
        lexeme = Lexeme(u"atamak", u"ata", SyntacticCategory.VERB, None, [RootAttribute.ProgressiveVowelDrop])
        generated_roots = RootGenerator.generate(lexeme)
        assert_that(generated_roots, has_length(2))
        assert_that(generated_roots, has_item(Root(u"ata", lexeme, None, {LVB, LLV, LLNotVless, LVU})))
        assert_that(generated_roots, has_item(Root(u"at", lexeme, {PhoneticExpectation.VowelStart}, {LVB, LLC, LLVless, LLVlessStop, LVU})))

    def test_should_generate_with_inverse_harmony(self):
        lexeme = Lexeme(u"kemal", u"kemal", SyntacticCategory.NOUN, None, [RootAttribute.InverseHarmony])
        generated_roots = RootGenerator.generate(lexeme)
        assert_that(generated_roots, has_length(1))
        assert_that(generated_roots, has_item(Root(u"kemal", lexeme, None, {LVF, LLC, LLNotVless, LVU})))

        lexeme = Lexeme(u"kanaat", u"kanaat", SyntacticCategory.NOUN, None, [RootAttribute.NoVoicing, RootAttribute.InverseHarmony])
        generated_roots = RootGenerator.generate(lexeme)
        assert_that(generated_roots, has_length(1))
        assert_that(generated_roots, has_item(Root(u"kanaat", lexeme, None, {LVF, LLC, LLVless, LLVlessStop, LVU})))

    def test_should_generate_converting_circumflexes(self):
        lexeme = Lexeme(u"rüzgâr", u"rüzgâr", SyntacticCategory.NOUN, None, None)
        generated_roots = CircumflexConvertingRootGenerator.generate(lexeme)
        assert_that(generated_roots, has_length(2))
        assert_that(generated_roots, has_item(Root(u"rüzgar", lexeme, None, {LVB, LLC, LLNotVless, LVU})))
        assert_that(generated_roots, has_item(Root(u"rüzgâr", lexeme, None, {LVB, LLC, LLNotVless, LVU})))

        lexeme = Lexeme(u"alenî", u"alenî", SyntacticCategory.ADJECTIVE, None, None)
        generated_roots = CircumflexConvertingRootGenerator.generate(lexeme)
        assert_that(generated_roots, has_length(2))
        assert_that(generated_roots, has_item(Root(u"aleni", lexeme, None, {LVF, LLV, LLNotVless, LVU})))
        assert_that(generated_roots, has_item(Root(u"alenî", lexeme, None, {LVF, LLV, LLNotVless, LVU})))

        lexeme = Lexeme(u"cülûs", u"cülûs", SyntacticCategory.NOUN, None, None)
        generated_roots = CircumflexConvertingRootGenerator.generate(lexeme)
        assert_that(generated_roots, has_length(2))
        assert_that(generated_roots, has_item(Root(u"cülus", lexeme, None, {LVB, LLC, LLVless, LVR})))
        assert_that(generated_roots, has_item(Root(u"cülûs", lexeme, None, {LVB, LLC, LLVless, LVR})))

        lexeme = Lexeme(u"Âdem", u"Âdem", SyntacticCategory.NOUN, None, None)
        generated_roots = CircumflexConvertingRootGenerator.generate(lexeme)
        assert_that(generated_roots, has_length(2))
        assert_that(generated_roots, has_item(Root(u"Adem", lexeme, None, {LVF, LLC, LLNotVless, LVU})))
        assert_that(generated_roots, has_item(Root(u"Âdem", lexeme, None, {LVF, LLC, LLNotVless, LVU})))


if __name__ == '__main__':
    unittest.main()