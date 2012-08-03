# coding=utf-8
import unittest
from hamcrest import *
from trnltk.morphology.phonetics.phonetics import PhoneticAttributes, PhoneticExpectation
from trnltk.morphology.stem.dictionaryitem import DictionaryItem, SyntacticCategory, RootAttribute
from trnltk.morphology.stem.stemgenerator import StemGenerator, Stem, CircumflexConvertingStemGenerator

LLV = PhoneticAttributes.LastLetterVowel
LLC = PhoneticAttributes.LastLetterConsonant

LVR = PhoneticAttributes.LastVowelRounded
LVU = PhoneticAttributes.LastVowelUnrounded
LVF = PhoneticAttributes.LastVowelFrontal
LVB = PhoneticAttributes.LastVowelBack

LLVless =  PhoneticAttributes.LastLetterVoiceless
LLVlessStop = PhoneticAttributes.LastLetterVoicelessStop
LLNotVless =  PhoneticAttributes.LastLetterNotVoiceless

class StemGeneratorTest(unittest.TestCase):
    def test_should_generate_with_no_modifiers(self):
        dictionary_item = DictionaryItem("elma", "elma", SyntacticCategory.NOUN, None, None)
        generated_stems = StemGenerator.generate(dictionary_item)
        assert_that(generated_stems, has_length(1))
        assert_that(generated_stems, has_item(Stem('elma', dictionary_item, None, {LVB, LLV, LLNotVless, LVU})))

        dictionary_item = DictionaryItem("kek", "kek", SyntacticCategory.NOUN, None, [RootAttribute.NoVoicing])
        generated_stems = StemGenerator.generate(dictionary_item)
        assert_that(generated_stems, has_length(1))
        assert_that(generated_stems, has_item(Stem('kek', dictionary_item, None, {LVF, LLC, LLVless, LLVlessStop, LVU})))

    def test_should_generate_with_voicing(self):
        dictionary_item = DictionaryItem("armut", "armut", SyntacticCategory.NOUN, None, [RootAttribute.Voicing])
        generated_stems = StemGenerator.generate(dictionary_item)
        assert_that(generated_stems, has_length(2))
        assert_that(generated_stems, has_item(Stem('armut', dictionary_item, {PhoneticExpectation.ConsonantStart}, {LVB, LLC, LLVless, LLVlessStop, LVR})))
        assert_that(generated_stems, has_item(Stem('armud', dictionary_item, {PhoneticExpectation.VowelStart}, {LVB, LLC, LLVless, LVR})))

        dictionary_item = DictionaryItem("kapak", "kapak", SyntacticCategory.NOUN, None, [RootAttribute.Voicing])
        generated_stems = StemGenerator.generate(dictionary_item)
        assert_that(generated_stems, has_length(2))
        assert_that(generated_stems, has_item(Stem('kapak', dictionary_item, {PhoneticExpectation.ConsonantStart}, {LVB, LLC, LLVless, LLVlessStop, LVU})))
        assert_that(generated_stems, has_item(Stem(u'kapağ', dictionary_item, {PhoneticExpectation.VowelStart}, {LVB, LLC, LLVless, LVU})))

        dictionary_item = DictionaryItem("cenk", "cenk", SyntacticCategory.NOUN, None, [RootAttribute.Voicing])
        generated_stems = StemGenerator.generate(dictionary_item)
        assert_that(generated_stems, has_length(2))
        assert_that(generated_stems, has_item(Stem('cenk', dictionary_item, {PhoneticExpectation.ConsonantStart}, {LVF, LLC, LLVless, LLVlessStop, LVU})))
        assert_that(generated_stems, has_item(Stem('ceng', dictionary_item, {PhoneticExpectation.VowelStart}, {LVF, LLC, LLVless, LVU})))

        dictionary_item = DictionaryItem("kap", "kap", SyntacticCategory.NOUN, None, [RootAttribute.Voicing])
        generated_stems = StemGenerator.generate(dictionary_item)
        assert_that(generated_stems, has_length(2))
        assert_that(generated_stems, has_item(Stem('kap', dictionary_item, {PhoneticExpectation.ConsonantStart}, {LVB, LLC, LLVless, LLVlessStop, LVU})))
        assert_that(generated_stems, has_item(Stem('kab', dictionary_item, {PhoneticExpectation.VowelStart}, {LVB, LLC, LLVless, LVU})))

    def test_should_generate_with_last_vowel_drop(self):
        dictionary_item = DictionaryItem(u"ağız", u"ağız", SyntacticCategory.NOUN, None, [RootAttribute.LastVowelDrop])
        generated_stems = StemGenerator.generate(dictionary_item)
        assert_that(generated_stems, has_length(2))
        assert_that(generated_stems, has_item(Stem(u"ağız", dictionary_item, {PhoneticExpectation.ConsonantStart}, {LVB, LLC, LLNotVless, LVU})))
        assert_that(generated_stems, has_item(Stem(u"ağz", dictionary_item, {PhoneticExpectation.VowelStart}, {LVB, LLC, LLNotVless, LVU})))

        dictionary_item = DictionaryItem(u"ahit", u"ahit", SyntacticCategory.NOUN, None, [RootAttribute.LastVowelDrop, RootAttribute.Voicing])
        generated_stems = StemGenerator.generate(dictionary_item)
        assert_that(generated_stems, has_length(2))
        assert_that(generated_stems, has_item(Stem(u"ahit", dictionary_item, {PhoneticExpectation.ConsonantStart}, {LVF, LLC, LLVless, LLVlessStop, LVU})))
        assert_that(generated_stems, has_item(Stem(u"ahd", dictionary_item, {PhoneticExpectation.VowelStart}, {LVF, LLVless, LLC, LVU})))

    def test_should_generate_with_doubling(self):
        dictionary_item = DictionaryItem(u"hac", u"hac", SyntacticCategory.NOUN, None, [RootAttribute.Doubling])
        generated_stems = StemGenerator.generate(dictionary_item)
        assert_that(generated_stems, has_length(2))
        assert_that(generated_stems, has_item(Stem(u"hac", dictionary_item, {PhoneticExpectation.ConsonantStart}, {LVB, LLC, LLNotVless, LVU})))
        assert_that(generated_stems, has_item(Stem(u"hacc", dictionary_item, {PhoneticExpectation.VowelStart}, {LVB, LLC, LLNotVless, LVU})))

        dictionary_item = DictionaryItem(u"ret", u"ret", SyntacticCategory.NOUN, None, [RootAttribute.Voicing, RootAttribute.Doubling])
        generated_stems = StemGenerator.generate(dictionary_item)
        assert_that(generated_stems, has_length(2))
        assert_that(generated_stems, has_item(Stem(u"ret", dictionary_item, {PhoneticExpectation.ConsonantStart}, {LVF, LLC, LLVless, LLVlessStop, LVU})))
        assert_that(generated_stems, has_item(Stem(u"redd", dictionary_item, {PhoneticExpectation.VowelStart}, {LVF, LLC, LLVless, LVU})))

    def test_should_generate_with_progressive_vowel_drop(self):
        dictionary_item = DictionaryItem(u"atamak", u"ata", SyntacticCategory.VERB, None, [RootAttribute.ProgressiveVowelDrop])
        generated_stems = StemGenerator.generate(dictionary_item)
        assert_that(generated_stems, has_length(2))
        assert_that(generated_stems, has_item(Stem(u"ata", dictionary_item, None, {LVB, LLV, LLNotVless, LVU})))
        assert_that(generated_stems, has_item(Stem(u"at", dictionary_item, {PhoneticExpectation.VowelStart}, {LVB, LLC, LLVless, LLVlessStop, LVU})))

    def test_should_generate_with_inverse_harmony(self):
        dictionary_item = DictionaryItem(u"kemal", u"kemal", SyntacticCategory.NOUN, None, [RootAttribute.InverseHarmony])
        generated_stems = StemGenerator.generate(dictionary_item)
        assert_that(generated_stems, has_length(1))
        assert_that(generated_stems, has_item(Stem(u"kemal", dictionary_item, None, {LVF, LLC, LLNotVless, LVU})))

        dictionary_item = DictionaryItem(u"kanaat", u"kanaat", SyntacticCategory.NOUN, None, [RootAttribute.NoVoicing, RootAttribute.InverseHarmony])
        generated_stems = StemGenerator.generate(dictionary_item)
        assert_that(generated_stems, has_length(1))
        assert_that(generated_stems, has_item(Stem(u"kanaat", dictionary_item, None, {LVF, LLC, LLVless, LLVlessStop, LVU})))

    def test_should_generate_converting_circumflexes(self):
        dictionary_item = DictionaryItem(u"rüzgâr", u"rüzgâr", SyntacticCategory.NOUN, None, None)
        generated_stems = CircumflexConvertingStemGenerator.generate(dictionary_item)
        assert_that(generated_stems, has_length(2))
        assert_that(generated_stems, has_item(Stem(u"rüzgar", dictionary_item, None, {LVB, LLC, LLNotVless, LVU})))
        assert_that(generated_stems, has_item(Stem(u"rüzgâr", dictionary_item, None, {LVB, LLC, LLNotVless, LVU})))

        dictionary_item = DictionaryItem(u"alenî", u"alenî", SyntacticCategory.ADJECTIVE, None, None)
        generated_stems = CircumflexConvertingStemGenerator.generate(dictionary_item)
        assert_that(generated_stems, has_length(2))
        assert_that(generated_stems, has_item(Stem(u"aleni", dictionary_item, None, {LVF, LLV, LLNotVless, LVU})))
        assert_that(generated_stems, has_item(Stem(u"alenî", dictionary_item, None, {LVF, LLV, LLNotVless, LVU})))

        dictionary_item = DictionaryItem(u"cülûs", u"cülûs", SyntacticCategory.NOUN, None, None)
        generated_stems = CircumflexConvertingStemGenerator.generate(dictionary_item)
        assert_that(generated_stems, has_length(2))
        assert_that(generated_stems, has_item(Stem(u"cülus", dictionary_item, None, {LVB, LLC, LLVless, LVR})))
        assert_that(generated_stems, has_item(Stem(u"cülûs", dictionary_item, None, {LVB, LLC, LLVless, LVR})))

        dictionary_item = DictionaryItem(u"Âdem", u"Âdem", SyntacticCategory.NOUN, None, None)
        generated_stems = CircumflexConvertingStemGenerator.generate(dictionary_item)
        assert_that(generated_stems, has_length(2))
        assert_that(generated_stems, has_item(Stem(u"Adem", dictionary_item, None, {LVF, LLC, LLNotVless, LVU})))
        assert_that(generated_stems, has_item(Stem(u"Âdem", dictionary_item, None, {LVF, LLC, LLNotVless, LVU})))


if __name__ == '__main__':
    unittest.main()