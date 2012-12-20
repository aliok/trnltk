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
import os
import unittest
from hamcrest import *
from trnltk.morphology.model.lexeme import Lexeme, SyntacticCategory, LexemeAttribute, SecondarySyntacticCategory
from trnltk.morphology.lexicon.lexiconloader import LexiconLoader

class LexiconLoaderTest(unittest.TestCase):
    def test_should_create_lexeme_from_line(self):
        
        item = LexiconLoader._crate_lexeme_from_line(u'a [P:Interj]')
        assert_that(item, equal_to(Lexeme(u"a", u"a", SyntacticCategory.INTERJECTION, None, None)))
        
        item = LexiconLoader._crate_lexeme_from_line(u'aba [P:Adj]')
        assert_that(item, equal_to(Lexeme(u"aba", u"aba", SyntacticCategory.ADJECTIVE, None, None)))

        item = LexiconLoader._crate_lexeme_from_line(u'abadî')
        assert_that(item, equal_to(Lexeme(u"abadî", u"abadî", None, None, None)))

        item = LexiconLoader._crate_lexeme_from_line(u'abat [P:Adj; A:NoVoicing]')
        assert_that(item, equal_to(Lexeme(u"abat", u"abat", SyntacticCategory.ADJECTIVE, None, {LexemeAttribute.NoVoicing})))

        item = LexiconLoader._crate_lexeme_from_line(u'Abdal')
        assert_that(item, equal_to(Lexeme(u"Abdal", u"Abdal", None, None, None)))

        item = LexiconLoader._crate_lexeme_from_line(u'abdest [A:NoVoicing]')
        assert_that(item, equal_to(Lexeme(u"abdest", u"abdest", None, None, {LexemeAttribute.NoVoicing})))

        item = LexiconLoader._crate_lexeme_from_line(u'abes [P:Adv]')
        assert_that(item, equal_to(Lexeme(u"abes", u"abes", SyntacticCategory.ADVERB, None, None)))

        item = LexiconLoader._crate_lexeme_from_line(u'ablak [P:Adj; A:NoVoicing]')
        assert_that(item, equal_to(Lexeme(u"ablak", u"ablak", SyntacticCategory.ADJECTIVE, None, {LexemeAttribute.NoVoicing})))

        item = LexiconLoader._crate_lexeme_from_line(u'abuk [P:Adj, Dup;A:NoVoicing, NoSuffix]')
        assert_that(item, equal_to(Lexeme(u"abuk", u"abuk", SyntacticCategory.ADJECTIVE, SecondarySyntacticCategory.DUPLICATOR, {LexemeAttribute.NoVoicing, LexemeAttribute.NoSuffix})))

        item = LexiconLoader._crate_lexeme_from_line(u'acemborusu [A:CompoundP3sg; R:acemboru]')
        assert_that(item, equal_to(Lexeme(u"acemborusu", u"acemboru", None, None, {LexemeAttribute.CompoundP3sg})))

        item = LexiconLoader._crate_lexeme_from_line(u'acembuselik')
        assert_that(item, equal_to(Lexeme(u"acembuselik", u"acembuselik", None, None, None)))

        item = LexiconLoader._crate_lexeme_from_line(u'aciz [A: LastVowelDrop]')
        assert_that(item, equal_to(Lexeme(u"aciz", u"aciz", None, None, {LexemeAttribute.LastVowelDrop})))

        item = LexiconLoader._crate_lexeme_from_line(u'âciz [P:Adj]')
        assert_that(item, equal_to(Lexeme(u"âciz", u"âciz", SyntacticCategory.ADJECTIVE, None, None)))

        item = LexiconLoader._crate_lexeme_from_line(u'açık [P:Adj]')
        assert_that(item, equal_to(Lexeme(u"açık", u"açık", SyntacticCategory.ADJECTIVE, None, None)))

        item = LexiconLoader._crate_lexeme_from_line(u'ad')
        assert_that(item, equal_to(Lexeme(u"ad", u"ad", None, None, None)))

        item = LexiconLoader._crate_lexeme_from_line(u'ad [P:Noun; A:Doubling, InverseHarmony]')
        assert_that(item, equal_to(Lexeme(u"ad", u"ad", SyntacticCategory.NOUN, None, {LexemeAttribute.Doubling, LexemeAttribute.InverseHarmony})))

        item = LexiconLoader._crate_lexeme_from_line(u'addetmek [A:Voicing, Aorist_A]')
        assert_that(item, equal_to(Lexeme(u"addetmek", u"addetmek", None, None, {LexemeAttribute.Voicing, LexemeAttribute.Aorist_A})))

        item = LexiconLoader._crate_lexeme_from_line(u'addolmak')
        assert_that(item, equal_to(Lexeme(u"addolmak", u"addolmak", None, None, None)))

        item = LexiconLoader._crate_lexeme_from_line(u'ahlat [A:NoVoicing, Plural]')
        assert_that(item, equal_to(Lexeme(u"ahlat", u"ahlat", None, None, {LexemeAttribute.NoVoicing, LexemeAttribute.Plural})))

        item = LexiconLoader._crate_lexeme_from_line(u'akşam [P:Noun, Time]')
        assert_that(item, equal_to(Lexeme(u"akşam", u"akşam", SyntacticCategory.NOUN, SecondarySyntacticCategory.TIME, None)))

        item = LexiconLoader._crate_lexeme_from_line(u'yemek [P:Noun]')
        assert_that(item, equal_to(Lexeme(u"yemek", u"yemek", SyntacticCategory.NOUN, None, None)))

        item = LexiconLoader._crate_lexeme_from_line(u'yemek')
        assert_that(item, equal_to(Lexeme(u"yemek", u"yemek", None, None, None)))

        item = LexiconLoader._crate_lexeme_from_line(u'sürtmek')
        assert_that(item, equal_to(Lexeme(u"sürtmek", u"sürtmek", None, None, None)))

        item = LexiconLoader._crate_lexeme_from_line(u'ürkmek [A:Causative_It]')
        assert_that(item, equal_to(Lexeme(u"ürkmek", u"ürkmek", None, None, {LexemeAttribute.Causative_It})))

        item = LexiconLoader._crate_lexeme_from_line(u'akşamsefası [A:CompoundP3sg; R:akşamsefa]')
        assert_that(item, equal_to(Lexeme(u"akşamsefası", u"akşamsefa", None, None, {LexemeAttribute.CompoundP3sg})))

        item = LexiconLoader._crate_lexeme_from_line(u'akşamüstü [P:Noun, Time; A:CompoundP3sg; R:akşamüst]')
        assert_that(item, equal_to(Lexeme(u"akşamüstü", u"akşamüst", SyntacticCategory.NOUN, SecondarySyntacticCategory.TIME, {LexemeAttribute.CompoundP3sg})))

        item = LexiconLoader._crate_lexeme_from_line(u'mi [P:Ques]')
        assert_that(item, equal_to(Lexeme(u"mi", u"mi", SyntacticCategory.QUESTION, None, None)))

    def test_should_not_set_category_and_lemma_if_category_is_set_already(self):
        item_org = Lexeme(u'elma', u'elma', SyntacticCategory.NOUN, None, None)
        item_clone = item_org.clone()
        LexiconLoader._set_category_and_lemma(item_clone)
        assert_that(item_org, equal_to(item_clone))

        item_org = Lexeme(u'mavi', u'mavi', SyntacticCategory.ADJECTIVE, None, None)
        item_clone = item_org.clone()
        LexiconLoader._set_category_and_lemma(item_clone)
        assert_that(item_org, equal_to(item_clone))

        item_org = Lexeme(u'aha', u'aha', SyntacticCategory.INTERJECTION, None, None)
        item_clone = item_org.clone()
        LexiconLoader._set_category_and_lemma(item_clone)
        assert_that(item_org, equal_to(item_clone))

        item_org = Lexeme(u'yemek', u'yemek', SyntacticCategory.NOUN, None, None)
        item_clone = item_org.clone()
        LexiconLoader._set_category_and_lemma(item_clone)
        assert_that(item_org, equal_to(item_clone))

        item_org = Lexeme(u'tokmak', u'tokmak', SyntacticCategory.NOUN, None, None)
        item_clone = item_org.clone()
        LexiconLoader._set_category_and_lemma(item_clone)
        assert_that(item_org, equal_to(item_clone))

    def test_should_set_category_and_lemma_for_nonverbs(self):
        item = Lexeme(u'elma', u'elma', None, None, None)
        LexiconLoader._set_category_and_lemma(item)
        assert_that(item, equal_to(Lexeme(u'elma', u'elma', SyntacticCategory.NOUN, None, None)))

    def test_should_set_category_and_lemma_for_verbs(self):
        item = Lexeme(u'yemek', u'yemek', None, None, None)
        LexiconLoader._set_category_and_lemma(item)
        assert_that(item, equal_to(Lexeme(u'yemek', u'ye', SyntacticCategory.VERB, None, None)))

        item = Lexeme(u'elemek', u'elemek', None, None, None)
        LexiconLoader._set_category_and_lemma(item)
        assert_that(item, equal_to(Lexeme(u'elemek', u'ele', SyntacticCategory.VERB, None, None)))

    def test_should_infer_morphemic_attrs_for_verbs(self):
        PVD = LexemeAttribute.ProgressiveVowelDrop
        PI = LexemeAttribute.Passive_In
        AA = LexemeAttribute.Aorist_A
        AI = LexemeAttribute.Aorist_I
        VO = LexemeAttribute.Voicing
        NVO = LexemeAttribute.NoVoicing

        C_T = LexemeAttribute.Causative_t
        C_IR = LexemeAttribute.Causative_Ir
        C_IT = LexemeAttribute.Causative_It
        C_AR = LexemeAttribute.Causative_Ar
        C_DIR = LexemeAttribute.Causative_dIr

        item = Lexeme(u'gitmek', u'git', SyntacticCategory.VERB, None, {VO, C_DIR})
        LexiconLoader._infer_morphemic_attributes(item)
        assert_that(item, equal_to(Lexeme(u'gitmek', u'git', SyntacticCategory.VERB, None, {VO, C_DIR, AA})))

        item = Lexeme(u'gelmek', u'gel', SyntacticCategory.VERB, None, {AI, C_DIR})
        LexiconLoader._infer_morphemic_attributes(item)
        assert_that(item, equal_to(Lexeme(u'gelmek', u'gel', SyntacticCategory.VERB, None, {AI, C_DIR, PI, NVO})))

        item = Lexeme(u'atmak', u'at', SyntacticCategory.VERB, None, {NVO, C_DIR})
        LexiconLoader._infer_morphemic_attributes(item)
        assert_that(item, equal_to(Lexeme(u'atmak', u'at', SyntacticCategory.VERB, None, {NVO, C_DIR, AA})))

        item = Lexeme(u'atamak', u'ata', SyntacticCategory.VERB, None, None)
        LexiconLoader._infer_morphemic_attributes(item)
        assert_that(item, equal_to(Lexeme(u'atamak', u'ata', SyntacticCategory.VERB, None, {PVD, PI, AI, C_T, NVO})))

        item = Lexeme(u'dolamak', u'dola', SyntacticCategory.VERB, None, None)
        LexiconLoader._infer_morphemic_attributes(item)
        assert_that(item, equal_to(Lexeme(u'dolamak', u'dola', SyntacticCategory.VERB, None, {PVD, PI, AI, C_T, NVO})))

        item = Lexeme(u'tanımak', u'tanı', SyntacticCategory.VERB, None, {AI})
        LexiconLoader._infer_morphemic_attributes(item)
        assert_that(item, equal_to(Lexeme(u'tanımak', u'tanı', SyntacticCategory.VERB, None, {AI, PVD, PI, AI, C_T, NVO})))

        item = Lexeme(u'getirmek', u'getir', SyntacticCategory.VERB, None, {AI})
        LexiconLoader._infer_morphemic_attributes(item)
        assert_that(item, equal_to(Lexeme(u'getirmek', u'getir', SyntacticCategory.VERB, None, {AI, AI, C_T, NVO})))

        item = Lexeme(u'ürkmek', u'ürk', SyntacticCategory.VERB, None, {C_IT})
        LexiconLoader._infer_morphemic_attributes(item)
        assert_that(item, equal_to(Lexeme(u'ürkmek', u'ürk', SyntacticCategory.VERB, None, {C_IT, AA, NVO})))

        item = Lexeme(u'ağlamak', u'ağla', SyntacticCategory.VERB, None, None)
        LexiconLoader._infer_morphemic_attributes(item)
        assert_that(item, equal_to(Lexeme(u'ağlamak', u'ağla', SyntacticCategory.VERB, None, {PVD, PI, AI, C_T, NVO})))

    def test_should_load_lexicon_from_str(self):
        dictionary_content = u'''
            a [P:Interj]
            aba [P:Adj]
            abadî
            abat [P:Adj; A:NoVoicing]
            Abdal
            abdest [A:NoVoicing]
            abes [P:Adj]
            abes [P:Adv]
            ablak [P:Adj; A:NoVoicing]
            abuk [P:Adj, Dup;A:NoVoicing, NoSuffix]
            acemborusu [A:CompoundP3sg; R:acemboru]
            acembuselik
            aciz [A:LastVowelDrop]
            âciz [P:Adj]
            açık [P:Adj]
            ad
            ad [P:Noun; A:Doubling, InverseHarmony]
            addetmek [A:Voicing, Aorist_A]
            addolmak [A:Causative_dIr]
            ahlat [A:NoVoicing, Plural]
            akşam [P:Noun, Time]
            atamak [A:Causative_It]
            sürtmek
            yemek [P:Noun]
            yemek [A:Causative_dIr]
            ürkmek [A:Causative_It]
        '''
        dictionary_lines = dictionary_content.split('\n')
        dictionary_lines = [l.strip() for l in dictionary_lines]
        dictionary_lines = filter(lambda line: line, dictionary_lines)

        lexemes = LexiconLoader.load_from_lines(dictionary_lines)

        assert_that(lexemes, has_length(len(dictionary_lines)), str(len(lexemes)-len(dictionary_lines)))

        assert_that(lexemes, has_item(Lexeme(u'a', u'a', SyntacticCategory.INTERJECTION, None, None)))
        assert_that(lexemes, has_item(Lexeme(u'aba', u'aba', SyntacticCategory.ADJECTIVE, None, {LexemeAttribute.NoVoicing})))
        assert_that(lexemes, has_item(Lexeme(u'abadî', u'abadî', SyntacticCategory.NOUN, None, {LexemeAttribute.NoVoicing})))
        assert_that(lexemes, has_item(Lexeme(u'abat', u'abat', SyntacticCategory.ADJECTIVE, None, {LexemeAttribute.NoVoicing})))
        assert_that(lexemes, has_item(Lexeme(u'Abdal', u'Abdal', SyntacticCategory.NOUN, SecondarySyntacticCategory.PROPER_NOUN, {LexemeAttribute.NoVoicing})))
        assert_that(lexemes, has_item(Lexeme(u'abdest', u'abdest', SyntacticCategory.NOUN, None, {LexemeAttribute.NoVoicing})))
        assert_that(lexemes, has_item(Lexeme(u'abes', u'abes', SyntacticCategory.ADJECTIVE, None, {LexemeAttribute.NoVoicing})))
        assert_that(lexemes, has_item(Lexeme(u'abes', u'abes', SyntacticCategory.ADVERB, None, None)))
        assert_that(lexemes, has_item(Lexeme(u'ablak', u'ablak', SyntacticCategory.ADJECTIVE, None, {LexemeAttribute.NoVoicing})))
        assert_that(lexemes, has_item(Lexeme(u'abuk', u'abuk', SyntacticCategory.ADJECTIVE, SecondarySyntacticCategory.DUPLICATOR, {LexemeAttribute.NoSuffix, LexemeAttribute.NoVoicing})))
        assert_that(lexemes, has_item(Lexeme(u'acemborusu', u'acemboru', SyntacticCategory.NOUN, None, {LexemeAttribute.CompoundP3sg, LexemeAttribute.NoVoicing})))
        assert_that(lexemes, has_item(Lexeme(u'acembuselik', u'acembuselik', SyntacticCategory.NOUN, None, {LexemeAttribute.Voicing})))
        assert_that(lexemes, has_item(Lexeme(u'aciz', u'aciz', SyntacticCategory.NOUN, None, {LexemeAttribute.LastVowelDrop, LexemeAttribute.NoVoicing})))
        assert_that(lexemes, has_item(Lexeme(u'âciz', u'âciz', SyntacticCategory.ADJECTIVE, None, {LexemeAttribute.NoVoicing})))
        assert_that(lexemes, has_item(Lexeme(u'açık', u'açık', SyntacticCategory.ADJECTIVE, None, {LexemeAttribute.Voicing})))
        assert_that(lexemes, has_item(Lexeme(u'ad', u'ad', SyntacticCategory.NOUN, None, {LexemeAttribute.NoVoicing})))
        assert_that(lexemes, has_item(Lexeme(u'ad', u'ad', SyntacticCategory.NOUN, None, {LexemeAttribute.Doubling, LexemeAttribute.InverseHarmony, LexemeAttribute.NoVoicing})))
        assert_that(lexemes, has_item(Lexeme(u'addetmek', u'addet', SyntacticCategory.VERB, None, {LexemeAttribute.Aorist_A, LexemeAttribute.Causative_dIr, LexemeAttribute.Voicing})))
        assert_that(lexemes, has_item(Lexeme(u'addolmak', u'addol', SyntacticCategory.VERB, None, {LexemeAttribute.Aorist_I, LexemeAttribute.Causative_dIr, LexemeAttribute.NoVoicing, LexemeAttribute.Passive_In})))
        assert_that(lexemes, has_item(Lexeme(u'ahlat', u'ahlat', SyntacticCategory.NOUN, None, {LexemeAttribute.NoVoicing, LexemeAttribute.Plural})))
        assert_that(lexemes, has_item(Lexeme(u'akşam', u'akşam', SyntacticCategory.NOUN, SecondarySyntacticCategory.TIME, {LexemeAttribute.NoVoicing})))
        assert_that(lexemes, has_item(Lexeme(u'atamak', u'ata', SyntacticCategory.VERB, None, {LexemeAttribute.Aorist_I, LexemeAttribute.Causative_It, LexemeAttribute.NoVoicing, LexemeAttribute.Passive_In, LexemeAttribute.ProgressiveVowelDrop})))
        assert_that(lexemes, has_item(Lexeme(u'sürtmek', u'sürt', SyntacticCategory.VERB, None, {LexemeAttribute.Aorist_A, LexemeAttribute.Causative_Ir, LexemeAttribute.NoVoicing})))
        assert_that(lexemes, has_item(Lexeme(u'yemek', u'yemek', SyntacticCategory.NOUN, None, {LexemeAttribute.Voicing})))
        assert_that(lexemes, has_item(Lexeme(u'yemek', u'ye', SyntacticCategory.VERB, None, {LexemeAttribute.Aorist_A, LexemeAttribute.Causative_dIr, LexemeAttribute.NoVoicing, LexemeAttribute.Passive_In, LexemeAttribute.ProgressiveVowelDrop})))
        assert_that(lexemes, has_item(Lexeme(u'ürkmek', u'ürk', SyntacticCategory.VERB, None, {LexemeAttribute.Aorist_A, LexemeAttribute.Causative_It, LexemeAttribute.NoVoicing})))


    def test_should_validate_master_dict(self):
        path = os.path.join(os.path.dirname(__file__), '../../../resources/master_dictionary.txt')

        items = LexiconLoader.load_from_file(path)
        assert_that(len(items)>0, equal_to(True))
        for item in items:
            assert_that(item.lemma, not_none(), str(item))
            assert_that(item.root, not_none(), str(item))
            assert_that(item.syntactic_category, not_none(), str(item))
            assert_that(SyntacticCategory.ALL, has_item(item.syntactic_category), str(item))

            if item.secondary_syntactic_category:
                assert_that(SecondarySyntacticCategory.ALL, has_item(item.secondary_syntactic_category), str(item))

            if item.attributes:
                for attr in item.attributes:
                    assert_that(LexemeAttribute.ALL, has_item(attr), str(item))

if __name__ == '__main__':
    unittest.main()