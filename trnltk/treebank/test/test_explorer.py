# coding=utf-8
import os
import unittest
from xml.dom.minidom import parse
from hamcrest import *
from trnltk.parseset.xmlbindings import ParseSetBinding
from trnltk.treebank.explorer import CompleteWordConcordanceIndex, StemConcordanceIndex, DictionaryItemConcordanceIndex, TransitionWordConcordanceIndex, TransitionMatchedWordConcordanceIndex

class ExplorerTest(unittest.TestCase):

    def test_should_validate_concordances_for_parseset_001(self):
        self._validate_concordances_for_parse_set_n("001")

    def test_should_validate_concordances_for_parseset_002(self):
        self._validate_concordances_for_parse_set_n("002")

    def test_should_validate_concordances_for_parseset_003(self):
        self._validate_concordances_for_parse_set_n("003")

    def test_should_validate_concordances_for_parseset_004(self):
        self._validate_concordances_for_parse_set_n("004")

    def test_should_validate_concordances_for_parseset_005(self):
        self._validate_concordances_for_parse_set_n("005")

#    def test_should_validate_concordances_for_parseset_005(self):
#        self._validate_concordances_for_parse_set_n("005")


    def _validate_concordances_for_parse_set_n(self, parseset_index):
        dom = parse(os.path.join(os.path.dirname(__file__), '../../testresources/parsesets/parseset{}.xml'.format(parseset_index)))
        parseset = ParseSetBinding.build(dom.getElementsByTagName("parseset")[0])
        word_list = []
        for sentence in parseset.sentences:
            word_list.extend(sentence.words)

        self._validate_complete_word_concordance_indexes(word_list)
        self._validate_stem_concordance_indexes(word_list)
        self._validate_dictionary_item_concordance_indexes(word_list)
        self._validate_transition_word_concordance_indexes(word_list)
        self._validate_transition_matched_word_concordance_indexes(word_list)

    def _validate_complete_word_concordance_indexes(self, word_list):
        idx = CompleteWordConcordanceIndex(word_list)

        for complete_word in idx._offsets._indices.iterkeys():
            offsets = idx.offsets(complete_word)
            words = [word_list[offset] for offset in offsets]
            assert_that(all([word.str==complete_word for word in words]))

        for complete_word in idx._offsets._indices.iterkeys():
            for syntactic_category in idx._offsets._indices[complete_word].iterkeys():

                offsets = idx.offsets(complete_word, syntactic_category)
                words = [word_list[offset] for offset in offsets]
                assert_that(all([word.str==complete_word and word.syntactic_category==syntactic_category for word in words]))

        for complete_word in idx._offsets._indices.iterkeys():
            for syntactic_category in idx._offsets._indices[complete_word].iterkeys():
                for secondary_syntactic_category in idx._offsets._indices[complete_word][syntactic_category].iterkeys():

                    offsets = idx.offsets(complete_word, syntactic_category, secondary_syntactic_category)
                    words = [word_list[offset] for offset in offsets]
                    assert_that(all([word.str==complete_word and word.syntactic_category==syntactic_category
                                     and word.secondary_syntactic_category==secondary_syntactic_category
                                     for word in words]))

    def _validate_stem_concordance_indexes(self, word_list):
        idx = StemConcordanceIndex(word_list)

        for stem in idx._offsets._indices.iterkeys():
            offsets = idx.offsets(stem)
            words = [word_list[offset] for offset in offsets]
            assert_that(all([word.stem.root==stem for word in words]))

        for stem in idx._offsets._indices.iterkeys():
            for syntactic_category in idx._offsets._indices[stem].iterkeys():

                offsets = idx.offsets(stem, syntactic_category)
                words = [word_list[offset] for offset in offsets]
                assert_that(all([word.stem.root==stem and word.stem.syntactic_category==syntactic_category for word in words]))

        for stem in idx._offsets._indices.iterkeys():
            for syntactic_category in idx._offsets._indices[stem].iterkeys():
                for secondary_syntactic_category in idx._offsets._indices[stem][syntactic_category].iterkeys():

                    offsets = idx.offsets(stem, syntactic_category, secondary_syntactic_category)
                    words = [word_list[offset] for offset in offsets]
                    assert_that(all([word.stem.root==stem and word.stem.syntactic_category==syntactic_category
                                     and word.stem.secondary_syntactic_category==secondary_syntactic_category
                                     for word in words]))

    def _validate_dictionary_item_concordance_indexes(self, word_list):
        idx = DictionaryItemConcordanceIndex(word_list)

        for lemma_root in idx._offsets._indices.iterkeys():
            offsets = idx.offsets(lemma_root)
            words = [word_list[offset] for offset in offsets]
            assert_that(all([word.stem.lemma_root==lemma_root for word in words]))

        for lemma_root in idx._offsets._indices.iterkeys():
            for syntactic_category in idx._offsets._indices[lemma_root].iterkeys():

                offsets = idx.offsets(lemma_root, syntactic_category)
                words = [word_list[offset] for offset in offsets]
                assert_that(all([word.stem.lemma_root==lemma_root and word.stem.syntactic_category==syntactic_category for word in words]))

        for lemma_root in idx._offsets._indices.iterkeys():
            for syntactic_category in idx._offsets._indices[lemma_root].iterkeys():
                for secondary_syntactic_category in idx._offsets._indices[lemma_root][syntactic_category].iterkeys():

                    offsets = idx.offsets(lemma_root, syntactic_category, secondary_syntactic_category)
                    words = [word_list[offset] for offset in offsets]
                    assert_that(all([word.stem.lemma_root==lemma_root and word.stem.syntactic_category==syntactic_category
                                     and word.stem.secondary_syntactic_category==secondary_syntactic_category
                                     for word in words]))

    def _validate_transition_word_concordance_indexes(self, word_list):
        idx = TransitionWordConcordanceIndex(word_list)

        for transition_word in idx._offsets._indices.iterkeys():
            offsets = idx.offsets(transition_word)
            words = [word_list[offset] for offset in offsets]
            assert_that(any([suffix.word==transition_word for word in words for suffix in word.suffixes]),
                u'Transition word {} not found'.format(transition_word))

        for transition_word in idx._offsets._indices.iterkeys():
            for syntactic_category in idx._offsets._indices[transition_word].iterkeys():

                offsets = idx.offsets(transition_word, syntactic_category)
                words = [word_list[offset] for offset in offsets]
                assert_that(any([suffix.word==transition_word and suffix.to_syntactic_category==syntactic_category for word in words for suffix in word.suffixes]),
                    u'Transition word {}+{} not found'.format(transition_word, syntactic_category))

    def _validate_transition_matched_word_concordance_indexes(self, word_list):
        idx = TransitionMatchedWordConcordanceIndex(word_list)

        for transition_word in idx._offsets._indices.iterkeys():
            offsets = idx.offsets(transition_word)
            words = [word_list[offset] for offset in offsets]
            assert_that(any([suffix.matched_word==transition_word for word in words for suffix in word.suffixes]),
                u'Transition word {} not found'.format(transition_word))

        for transition_word in idx._offsets._indices.iterkeys():
            for syntactic_category in idx._offsets._indices[transition_word].iterkeys():

                offsets = idx.offsets(transition_word, syntactic_category)
                words = [word_list[offset] for offset in offsets]
                assert_that(any([suffix.matched_word==transition_word and suffix.to_syntactic_category==syntactic_category for word in words for suffix in word.suffixes]),
                    u'Transition word {}+{} not found'.format(transition_word, syntactic_category))

if __name__ == '__main__':
    unittest.main()
