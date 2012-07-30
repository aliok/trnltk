# coding=utf-8
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

class StemConcordanceIndex(ConcordanceIndex):
    def __init__(self, word_list):
        self._offsets = HierarchicalIndex(3)

        for index, word in enumerate(word_list):
            if isinstance(word, UnparsableWordBinding):
                continue

            self._offsets.insert(index, word.stem.root, word.stem.syntactic_category, word.stem.secondary_syntactic_category)


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

            self._offsets.insert(index, word.stem.lemma_root, word.stem.syntactic_category, word.stem.secondary_syntactic_category)

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

            syntactic_category = word.stem.syntactic_category
            secondary_syntactic_category = word.stem.secondary_syntactic_category
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

            syntactic_category = word.stem.syntactic_category
            secondary_syntactic_category = word.stem.secondary_syntactic_category
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
