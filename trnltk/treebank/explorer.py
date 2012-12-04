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
from trnltk.parseset.xmlbindings import  UnparsableWordBinding, DerivationalSuffixBinding
from trnltk.treebank.model import HierarchicalIndex

class ConcordanceIndex(object):
    def offsets(self, sth, syntactic_category, secondary_syntactic_category):
        raise NotImplementedError()

class CompleteWordConcordanceIndex(ConcordanceIndex):
    def __init__(self, word_list):
        self._offsets = HierarchicalIndex(3)

        for index, word in enumerate(word_list):
            if isinstance(word, UnparsableWordBinding):
                continue

            self._offsets.insert(index, word.str, word.syntactic_category, word.secondary_syntactic_category)

    def offsets(self, word_str, syntactic_category=None, secondary_syntactic_category=None):
        assert word_str is not None
        if secondary_syntactic_category:
            assert syntactic_category is not None

        args = [word_str, syntactic_category, secondary_syntactic_category]
        args = filter(lambda x : x is not None, args)

        return self._offsets.get(*args)

class RootConcordanceIndex(ConcordanceIndex):
    def __init__(self, word_list):
        self._offsets = HierarchicalIndex(3)

        for index, word in enumerate(word_list):
            if isinstance(word, UnparsableWordBinding):
                continue

            self._offsets.insert(index, word.root.str, word.root.syntactic_category, word.root.secondary_syntactic_category)


    def offsets(self, word_str, syntactic_category=None, secondary_syntactic_category=None):
        assert word_str is not None
        if secondary_syntactic_category:
            assert syntactic_category is not None

        args = [word_str, syntactic_category, secondary_syntactic_category]
        args = filter(lambda x : x is not None, args)

        return self._offsets.get(*args)

class DictionaryItemConcordanceIndex(ConcordanceIndex):
    def __init__(self, word_list):
        self._offsets = HierarchicalIndex(3)

        for index, word in enumerate(word_list):
            if isinstance(word, UnparsableWordBinding):
                continue

            self._offsets.insert(index, word.root.lemma_root, word.root.syntactic_category, word.root.secondary_syntactic_category)

    def offsets(self, word_str, syntactic_category=None, secondary_syntactic_category=None):
        assert word_str is not None
        if secondary_syntactic_category:
            assert syntactic_category is not None

        args = [word_str, syntactic_category, secondary_syntactic_category]
        args = filter(lambda x : x is not None, args)

        return self._offsets.get(*args)

class TransitionWordConcordanceIndex(ConcordanceIndex):
    def __init__(self, word_list):
        self._offsets = HierarchicalIndex(3)

        for index, word in enumerate(word_list):
            if isinstance(word, UnparsableWordBinding):
                continue

            secondary_syntactic_category = word.root.secondary_syntactic_category
            for suffix in word.suffixes:
                syntactic_category = suffix.to_syntactic_category
                if isinstance(suffix, DerivationalSuffixBinding):
                    secondary_syntactic_category = None

                self._offsets.insert(index, suffix.word, syntactic_category, secondary_syntactic_category)

    def offsets(self, word_str, syntactic_category=None, secondary_syntactic_category=None):
        assert word_str is not None
        if secondary_syntactic_category:
            assert syntactic_category is not None

        args = [word_str, syntactic_category, secondary_syntactic_category]
        args = filter(lambda x : x is not None, args)

        return self._offsets.get(*args)

class TransitionMatchedWordConcordanceIndex(ConcordanceIndex):
    def __init__(self, word_list):
        self._offsets = HierarchicalIndex(3)

        for index, word in enumerate(word_list):
            if isinstance(word, UnparsableWordBinding):
                continue

            syntactic_category = word.root.syntactic_category
            secondary_syntactic_category = word.root.secondary_syntactic_category
            for suffix in word.suffixes:
                syntactic_category = suffix.to_syntactic_category
                if isinstance(suffix, DerivationalSuffixBinding):
                    secondary_syntactic_category = None

                self._offsets.insert(index, suffix.matched_word, syntactic_category, secondary_syntactic_category)

    def offsets(self, word_str, syntactic_category=None, secondary_syntactic_category=None):
        assert word_str is not None
        if secondary_syntactic_category:
            assert syntactic_category is not None

        args = [word_str, syntactic_category, secondary_syntactic_category]
        args = filter(lambda x : x is not None, args)

        return self._offsets.get(*args)
