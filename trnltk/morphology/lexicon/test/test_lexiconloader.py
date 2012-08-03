# coding=utf-8
import os
import unittest
from hamcrest import *
from trnltk.morphology.model.lexeme import Lexeme, SyntacticCategory, RootAttribute, SecondarySyntacticCategory
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
        assert_that(item, equal_to(Lexeme(u"abat", u"abat", SyntacticCategory.ADJECTIVE, None, [RootAttribute.NoVoicing])))

        item = LexiconLoader._crate_lexeme_from_line(u'Abdal')
        assert_that(item, equal_to(Lexeme(u"Abdal", u"Abdal", None, None, None)))

        item = LexiconLoader._crate_lexeme_from_line(u'abdest [A:NoVoicing]')
        assert_that(item, equal_to(Lexeme(u"abdest", u"abdest", None, None, [RootAttribute.NoVoicing])))

        item = LexiconLoader._crate_lexeme_from_line(u'abes [P:Adv]')
        assert_that(item, equal_to(Lexeme(u"abes", u"abes", SyntacticCategory.ADVERB, None, None)))

        item = LexiconLoader._crate_lexeme_from_line(u'ablak [P:Adj; A:NoVoicing]')
        assert_that(item, equal_to(Lexeme(u"ablak", u"ablak", SyntacticCategory.ADJECTIVE, None, [RootAttribute.NoVoicing])))

        item = LexiconLoader._crate_lexeme_from_line(u'abuk [P:Adj, Dup;A:NoVoicing, NoSuffix]')
        assert_that(item, equal_to(Lexeme(u"abuk", u"abuk", SyntacticCategory.ADJECTIVE, SecondarySyntacticCategory.DUPLICATOR, [RootAttribute.NoVoicing, RootAttribute.NoSuffix])))

        item = LexiconLoader._crate_lexeme_from_line(u'acemborusu [A:CompoundP3sg; R:acemboru]')
        assert_that(item, equal_to(Lexeme(u"acemborusu", u"acemboru", None, None, [RootAttribute.CompoundP3sg])))

        item = LexiconLoader._crate_lexeme_from_line(u'acembuselik')
        assert_that(item, equal_to(Lexeme(u"acembuselik", u"acembuselik", None, None, None)))

        item = LexiconLoader._crate_lexeme_from_line(u'aciz [A: LastVowelDrop]')
        assert_that(item, equal_to(Lexeme(u"aciz", u"aciz", None, None, [RootAttribute.LastVowelDrop])))

        item = LexiconLoader._crate_lexeme_from_line(u'âciz [P:Adj]')
        assert_that(item, equal_to(Lexeme(u"âciz", u"âciz", SyntacticCategory.ADJECTIVE, None, None)))

        item = LexiconLoader._crate_lexeme_from_line(u'açık [P:Adj]')
        assert_that(item, equal_to(Lexeme(u"açık", u"açık", SyntacticCategory.ADJECTIVE, None, None)))

        item = LexiconLoader._crate_lexeme_from_line(u'ad')
        assert_that(item, equal_to(Lexeme(u"ad", u"ad", None, None, None)))

        item = LexiconLoader._crate_lexeme_from_line(u'ad [P:Noun; A:Doubling, InverseHarmony]')
        assert_that(item, equal_to(Lexeme(u"ad", u"ad", SyntacticCategory.NOUN, None, [RootAttribute.Doubling, RootAttribute.InverseHarmony])))

        item = LexiconLoader._crate_lexeme_from_line(u'addetmek [A:Voicing, Aorist_A]')
        assert_that(item, equal_to(Lexeme(u"addetmek", u"addetmek", None, None, [RootAttribute.Voicing, RootAttribute.Aorist_A])))

        item = LexiconLoader._crate_lexeme_from_line(u'addolmak')
        assert_that(item, equal_to(Lexeme(u"addolmak", u"addolmak", None, None, None)))

        item = LexiconLoader._crate_lexeme_from_line(u'ahlat [A:NoVoicing, Plural]')
        assert_that(item, equal_to(Lexeme(u"ahlat", u"ahlat", None, None, [RootAttribute.NoVoicing, RootAttribute.Plural])))

        item = LexiconLoader._crate_lexeme_from_line(u'akşam [P:Noun, Time; S:+Rel_ki]')
        assert_that(item, equal_to(Lexeme(u"akşam", u"akşam", SyntacticCategory.NOUN, SecondarySyntacticCategory.TIME, None)))

        item = LexiconLoader._crate_lexeme_from_line(u'yemek [P:Noun]')
        assert_that(item, equal_to(Lexeme(u"yemek", u"yemek", SyntacticCategory.NOUN, None, None)))

        item = LexiconLoader._crate_lexeme_from_line(u'yemek')
        assert_that(item, equal_to(Lexeme(u"yemek", u"yemek", None, None, None)))

        item = LexiconLoader._crate_lexeme_from_line(u'ürkmek [A:Causative_It]')
        assert_that(item, equal_to(Lexeme(u"ürkmek", u"ürkmek", None, None, [RootAttribute.Causative_It])))

        item = LexiconLoader._crate_lexeme_from_line(u'akşamsefası [A:CompoundP3sg; R:akşamsefa]')
        assert_that(item, equal_to(Lexeme(u"akşamsefası", u"akşamsefa", None, None, [RootAttribute.CompoundP3sg])))

        item = LexiconLoader._crate_lexeme_from_line(u'akşamüstü [P:Noun, Time; A:CompoundP3sg; R:akşamüst]')
        assert_that(item, equal_to(Lexeme(u"akşamüstü", u"akşamüst", SyntacticCategory.NOUN, SecondarySyntacticCategory.TIME, [RootAttribute.CompoundP3sg])))

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
        PVD = RootAttribute.ProgressiveVowelDrop
        PI = RootAttribute.Passive_In
        AA = RootAttribute.Aorist_A
        AI = RootAttribute.Aorist_I
        VO = RootAttribute.Voicing
        NVO = RootAttribute.NoVoicing

        C_T = RootAttribute.Causative_t
        C_IR = RootAttribute.Causative_Ir
        C_IT = RootAttribute.Causative_It
        C_AR = RootAttribute.Causative_Ar
        C_DIR = RootAttribute.Causative_dIr

        item = Lexeme(u'gitmek', u'git', SyntacticCategory.VERB, None, [VO, C_DIR])
        LexiconLoader._infer_morphemic_attributes(item)
        assert_that(item, equal_to(Lexeme(u'gitmek', u'git', SyntacticCategory.VERB, None, [VO, C_DIR, AA])))

        item = Lexeme(u'gelmek', u'gel', SyntacticCategory.VERB, None, [AI, C_DIR])
        LexiconLoader._infer_morphemic_attributes(item)
        assert_that(item, equal_to(Lexeme(u'gelmek', u'gel', SyntacticCategory.VERB, None, [AI, C_DIR, PI, NVO])))

        item = Lexeme(u'atmak', u'at', SyntacticCategory.VERB, None, [NVO, C_DIR])
        LexiconLoader._infer_morphemic_attributes(item)
        assert_that(item, equal_to(Lexeme(u'atmak', u'at', SyntacticCategory.VERB, None, [NVO, C_DIR, AA])))

        item = Lexeme(u'atamak', u'ata', SyntacticCategory.VERB, None, None)
        LexiconLoader._infer_morphemic_attributes(item)
        assert_that(item, equal_to(Lexeme(u'atamak', u'ata', SyntacticCategory.VERB, None, [PVD, PI, AI, C_T, NVO])))

        item = Lexeme(u'dolamak', u'dola', SyntacticCategory.VERB, None, None)
        LexiconLoader._infer_morphemic_attributes(item)
        assert_that(item, equal_to(Lexeme(u'dolamak', u'dola', SyntacticCategory.VERB, None, [PVD, PI, AI, C_T, NVO])))

        item = Lexeme(u'tanımak', u'tanı', SyntacticCategory.VERB, None, [AI])
        LexiconLoader._infer_morphemic_attributes(item)
        assert_that(item, equal_to(Lexeme(u'tanımak', u'tanı', SyntacticCategory.VERB, None, [AI, PVD, PI, AI, C_T, NVO])))

        item = Lexeme(u'getirmek', u'getir', SyntacticCategory.VERB, None, [AI])
        LexiconLoader._infer_morphemic_attributes(item)
        assert_that(item, equal_to(Lexeme(u'getirmek', u'getir', SyntacticCategory.VERB, None, [AI, AI, C_T, NVO])))

        item = Lexeme(u'ürkmek', u'ürk', SyntacticCategory.VERB, None, [C_IT])
        LexiconLoader._infer_morphemic_attributes(item)
        assert_that(item, equal_to(Lexeme(u'ürkmek', u'ürk', SyntacticCategory.VERB, None, [C_IT, AA, NVO])))

        item = Lexeme(u'ağlamak', u'ağla', SyntacticCategory.VERB, None, None)
        LexiconLoader._infer_morphemic_attributes(item)
        assert_that(item, equal_to(Lexeme(u'ağlamak', u'ağla', SyntacticCategory.VERB, None, [PVD, PI, AI, C_T, NVO])))

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
            akşam [P:Noun, Time; S:+Rel_ki]
            atamak [A:Causative_It]
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
        assert_that(lexemes, has_item(Lexeme(u'aba', u'aba', SyntacticCategory.ADJECTIVE, None, [RootAttribute.NoVoicing])))
        assert_that(lexemes, has_item(Lexeme(u'abadî', u'abadî', SyntacticCategory.NOUN, None, [RootAttribute.NoVoicing])))
        assert_that(lexemes, has_item(Lexeme(u'abat', u'abat', SyntacticCategory.ADJECTIVE, None, [RootAttribute.NoVoicing])))
        assert_that(lexemes, has_item(Lexeme(u'Abdal', u'Abdal', SyntacticCategory.NOUN, SecondarySyntacticCategory.PROPER_NOUN, [RootAttribute.NoVoicing])))
        assert_that(lexemes, has_item(Lexeme(u'abdest', u'abdest', SyntacticCategory.NOUN, None, [RootAttribute.NoVoicing])))
        assert_that(lexemes, has_item(Lexeme(u'abes', u'abes', SyntacticCategory.ADJECTIVE, None, [RootAttribute.NoVoicing])))
        assert_that(lexemes, has_item(Lexeme(u'abes', u'abes', SyntacticCategory.ADVERB, None, None)))
        assert_that(lexemes, has_item(Lexeme(u'ablak', u'ablak', SyntacticCategory.ADJECTIVE, None, [RootAttribute.NoVoicing])))
        assert_that(lexemes, has_item(Lexeme(u'abuk', u'abuk', SyntacticCategory.ADJECTIVE, SecondarySyntacticCategory.DUPLICATOR, [RootAttribute.NoSuffix, RootAttribute.NoVoicing])))
        assert_that(lexemes, has_item(Lexeme(u'acemborusu', u'acemboru', SyntacticCategory.NOUN, None, [RootAttribute.CompoundP3sg, RootAttribute.NoVoicing])))
        assert_that(lexemes, has_item(Lexeme(u'acembuselik', u'acembuselik', SyntacticCategory.NOUN, None, [RootAttribute.Voicing])))
        assert_that(lexemes, has_item(Lexeme(u'aciz', u'aciz', SyntacticCategory.NOUN, None, [RootAttribute.LastVowelDrop, RootAttribute.NoVoicing])))
        assert_that(lexemes, has_item(Lexeme(u'âciz', u'âciz', SyntacticCategory.ADJECTIVE, None, [RootAttribute.NoVoicing])))
        assert_that(lexemes, has_item(Lexeme(u'açık', u'açık', SyntacticCategory.ADJECTIVE, None, [RootAttribute.Voicing])))
        assert_that(lexemes, has_item(Lexeme(u'ad', u'ad', SyntacticCategory.NOUN, None, [RootAttribute.NoVoicing])))
        assert_that(lexemes, has_item(Lexeme(u'ad', u'ad', SyntacticCategory.NOUN, None, [RootAttribute.Doubling, RootAttribute.InverseHarmony, RootAttribute.NoVoicing])))
        assert_that(lexemes, has_item(Lexeme(u'addetmek', u'addet', SyntacticCategory.VERB, None, [RootAttribute.Aorist_A, RootAttribute.Causative_dIr, RootAttribute.Voicing])))
        assert_that(lexemes, has_item(Lexeme(u'addolmak', u'addol', SyntacticCategory.VERB, None, [RootAttribute.Aorist_I, RootAttribute.Causative_dIr, RootAttribute.NoVoicing, RootAttribute.Passive_In])))
        assert_that(lexemes, has_item(Lexeme(u'ahlat', u'ahlat', SyntacticCategory.NOUN, None, [RootAttribute.NoVoicing, RootAttribute.Plural])))
        assert_that(lexemes, has_item(Lexeme(u'akşam', u'akşam', SyntacticCategory.NOUN, SecondarySyntacticCategory.TIME, [RootAttribute.NoVoicing])))
        assert_that(lexemes, has_item(Lexeme(u'atamak', u'ata', SyntacticCategory.VERB, None, [RootAttribute.Aorist_I, RootAttribute.Causative_It, RootAttribute.NoVoicing, RootAttribute.Passive_In, RootAttribute.ProgressiveVowelDrop])))
        assert_that(lexemes, has_item(Lexeme(u'yemek', u'yemek', SyntacticCategory.NOUN, None, [RootAttribute.Voicing])))
        assert_that(lexemes, has_item(Lexeme(u'yemek', u'ye', SyntacticCategory.VERB, None, [RootAttribute.Aorist_A, RootAttribute.Causative_dIr, RootAttribute.NoVoicing, RootAttribute.Passive_In, RootAttribute.ProgressiveVowelDrop])))
        assert_that(lexemes, has_item(Lexeme(u'ürkmek', u'ürk', SyntacticCategory.VERB, None, [RootAttribute.Aorist_A, RootAttribute.Causative_It, RootAttribute.NoVoicing])))


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
                    assert_that(RootAttribute.ALL, has_item(attr), str(item))

if __name__ == '__main__':
    unittest.main()