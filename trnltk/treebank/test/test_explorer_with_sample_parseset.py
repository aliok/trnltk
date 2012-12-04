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
from xml.dom.minidom import parse
from hamcrest import *
from trnltk.parseset.xmlbindings import ParseSetBinding
from trnltk.morphology.model.lexeme import SyntacticCategory, SecondarySyntacticCategory
from trnltk.treebank.explorer import CompleteWordConcordanceIndex, RootConcordanceIndex, DictionaryItemConcordanceIndex, TransitionWordConcordanceIndex, TransitionMatchedWordConcordanceIndex

class ExplorerTestWithSampleParseSet(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        dom = parse(os.path.join(os.path.dirname(__file__), 'concordance_sample_parseset.xml'))
        parseset = ParseSetBinding.build(dom.getElementsByTagName("parseset")[0])
        word_list = []
        for sentence in parseset.sentences:
            word_list.extend(sentence.words)

        cls.word_list = word_list

    def test_should_find_complete_word_concordance(self):
        idx = CompleteWordConcordanceIndex(self.word_list)

        assert_that(idx.offsets(u'something'), equal_to([]))

        assert_that(idx.offsets(u"o"), equal_to([0, 1, 2]))
        assert_that(idx.offsets(u"o", SyntacticCategory.PRONOUN), equal_to([0, 1]))
        assert_that(idx.offsets(u"o", SyntacticCategory.DETERMINER), equal_to([2]))
        assert_that(idx.offsets(u"o", SyntacticCategory.PRONOUN, SecondarySyntacticCategory.PERSONAL), equal_to([0]))
        assert_that(idx.offsets(u"o", SyntacticCategory.PRONOUN, SecondarySyntacticCategory.DEMONSTRATIVE), equal_to([1]))

        assert_that(idx.offsets(u"onu", SyntacticCategory.PRONOUN, SecondarySyntacticCategory.PERSONAL), equal_to([3]))
        assert_that(idx.offsets(u"onu", SyntacticCategory.PRONOUN, SecondarySyntacticCategory.DEMONSTRATIVE), equal_to([4]))

        assert_that(idx.offsets(u"gittim"), equal_to([6]))
        assert_that(idx.offsets(u"gittim", SyntacticCategory.VERB), equal_to([6]))

        assert_that(idx.offsets(u"giderim"), equal_to([7]))
        assert_that(idx.offsets(u"giderim", SyntacticCategory.VERB), equal_to([7]))

        assert_that(idx.offsets(u"gidecekler"), equal_to([8, 10]))
        assert_that(idx.offsets(u"gidecekler", SyntacticCategory.VERB), equal_to([8]))
        assert_that(idx.offsets(u"gidecekler", SyntacticCategory.NOUN), equal_to([10]))

        assert_that(idx.offsets(u"gideceğim"), equal_to([9, 11]))
        assert_that(idx.offsets(u"gideceğim", SyntacticCategory.VERB), equal_to([9]))
        assert_that(idx.offsets(u"gideceğim", SyntacticCategory.NOUN), equal_to([11]))


    def test_should_find_root_concordance(self):
        idx = RootConcordanceIndex(self.word_list)

        assert_that(idx.offsets(u'something'), equal_to([]))

        assert_that(idx.offsets(u"o"), equal_to([0, 1, 2, 3, 4]))
        assert_that(idx.offsets(u"o", SyntacticCategory.PRONOUN), equal_to([0, 1, 3, 4]))
        assert_that(idx.offsets(u"o", SyntacticCategory.DETERMINER), equal_to([2]))
        assert_that(idx.offsets(u"o", SyntacticCategory.PRONOUN, SecondarySyntacticCategory.PERSONAL), equal_to([0, 3]))
        assert_that(idx.offsets(u"o", SyntacticCategory.PRONOUN, SecondarySyntacticCategory.DEMONSTRATIVE), equal_to([1, 4]))

        assert_that(idx.offsets(u"git"), equal_to([6]))
        assert_that(idx.offsets(u"gid"), equal_to([7, 8, 9, 10, 11]))
        assert_that(idx.offsets(u"gid", SyntacticCategory.VERB), equal_to([7, 8, 9, 10, 11]))

    def test_should_find_lemma_concordance(self):
        idx = DictionaryItemConcordanceIndex(self.word_list)

        assert_that(idx.offsets(u'something'), equal_to([]))

        assert_that(idx.offsets(u"o"), equal_to([0, 1, 2, 3, 4]))
        assert_that(idx.offsets(u"o", SyntacticCategory.PRONOUN), equal_to([0, 1, 3, 4]))
        assert_that(idx.offsets(u"o", SyntacticCategory.DETERMINER), equal_to([2]))
        assert_that(idx.offsets(u"o", SyntacticCategory.PRONOUN, SecondarySyntacticCategory.PERSONAL), equal_to([0, 3]))
        assert_that(idx.offsets(u"o", SyntacticCategory.PRONOUN, SecondarySyntacticCategory.DEMONSTRATIVE), equal_to([1, 4]))

        assert_that(idx.offsets(u"git"), equal_to([6, 7, 8, 9, 10, 11]))
        assert_that(idx.offsets(u"gid"), equal_to([]))
        assert_that(idx.offsets(u"git", SyntacticCategory.VERB), equal_to([6, 7, 8, 9, 10, 11]))

    def test_should_find_transition_word_concordance(self):
        idx = TransitionWordConcordanceIndex(self.word_list)

        assert_that(idx.offsets(u'something'), equal_to([]))

        assert_that(idx.offsets(u"o"), equal_to([0, 1, 3, 4]))
        assert_that(idx.offsets(u"o", SyntacticCategory.PRONOUN), equal_to([0, 1, 3, 4]))
        assert_that(idx.offsets(u"o", SyntacticCategory.DETERMINER), equal_to([]))
        assert_that(idx.offsets(u"o", SyntacticCategory.PRONOUN, SecondarySyntacticCategory.PERSONAL), equal_to([0, 3]))
        assert_that(idx.offsets(u"o", SyntacticCategory.PRONOUN, SecondarySyntacticCategory.DEMONSTRATIVE), equal_to([1, 4]))

        assert_that(idx.offsets(u"git"), equal_to([6, 7, 8, 9, 10, 11]))
        assert_that(idx.offsets(u"gid"), equal_to([]))
        assert_that(idx.offsets(u"git", SyntacticCategory.VERB), equal_to([6, 7, 8, 9, 10, 11]))

        assert_that(idx.offsets(u"gidecek"), equal_to([8, 9, 10, 11]))
        assert_that(idx.offsets(u"gidecek", SyntacticCategory.NOUN), equal_to([10, 11]))
        assert_that(idx.offsets(u"gidecek", SyntacticCategory.VERB), equal_to([8, 9]))

        assert_that(idx.offsets(u"gideceğ"), equal_to([]))

    def test_should_find_transition_matched_word_concordance(self):
        idx = TransitionMatchedWordConcordanceIndex(self.word_list)

        assert_that(idx.offsets(u'something'), equal_to([]))

        assert_that(idx.offsets(u"o"), equal_to([0, 1, 3, 4]))
        assert_that(idx.offsets(u"o", SyntacticCategory.PRONOUN), equal_to([0, 1, 3, 4]))
        assert_that(idx.offsets(u"o", SyntacticCategory.DETERMINER), equal_to([]))
        assert_that(idx.offsets(u"o", SyntacticCategory.PRONOUN, SecondarySyntacticCategory.PERSONAL), equal_to([0, 3]))
        assert_that(idx.offsets(u"o", SyntacticCategory.PRONOUN, SecondarySyntacticCategory.DEMONSTRATIVE), equal_to([1, 4]))

        assert_that(idx.offsets(u"git"), equal_to([6, 7, 8, 9, 10, 11]))
        assert_that(idx.offsets(u"gid"), equal_to([]))
        assert_that(idx.offsets(u"git", SyntacticCategory.VERB), equal_to([6, 7, 8, 9, 10, 11]))

        assert_that(idx.offsets(u"gidecek"), equal_to([8, 10]))
        assert_that(idx.offsets(u"gidecek", SyntacticCategory.NOUN), equal_to([10]))
        assert_that(idx.offsets(u"gidecek", SyntacticCategory.VERB), equal_to([8]))

        assert_that(idx.offsets(u"gideceğ"), equal_to([9, 11]))
        assert_that(idx.offsets(u"gideceğ", SyntacticCategory.NOUN), equal_to([11]))
        assert_that(idx.offsets(u"gideceğ", SyntacticCategory.VERB), equal_to([9]))

if __name__ == '__main__':
    unittest.main()
