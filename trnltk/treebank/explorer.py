# coding=utf-8
# yapacagimi, yapacagimi -> true
from collections import defaultdict
import os
from xml.dom.minidom import parse
from trnltk.parseset.xmlbindings import ParseSetBinding

def concordance_full_word(full_word, syntactic_category=None):
    pass

# kitabimi, kitab -> true
def concordance_stem(stem, syntactic_category=None):
    pass

# kitabimi, kitap -> true
def concordance_dictionary_item(dictionary_item, syntactic_category=None):
    pass

# yapacagimi, yapacak -> true
def concordance_transition_word(transition_word, syntactic_category=None):
    pass

# yapacagimi, yapacag => true
def concordance_transition_full_word(transition_full_word, syntactic_category=None):
    pass


class ConcordanceIndex(object):
    def offsets(self, sth):
        raise NotImplementedError()

class CompleteWordConcordanceIndex(ConcordanceIndex):
    def __init__(self, word_list):
        self._offsets = defaultdict(list)

        for index, word in enumerate(word_list):
            self._offsets[word.str].append(index)

    def offsets(self, word):
        return self._offsets[word]


class StemConcordanceIndex(ConcordanceIndex):
    def __init__(self, word_list):
        self._offsets = defaultdict(list)

        for index, word in enumerate(word_list):
            if hasattr(word, "stem"):
                self._offsets[word.stem.root].append(index)

    def offsets(self, stem):
        return self._offsets[stem]

class DictionaryItemConcordanceIndex(ConcordanceIndex):
    def __init__(self, word_list):
        self._offsets = defaultdict(list)

        for index, word in enumerate(word_list):
            if hasattr(word, "stem"):
                self._offsets[word.stem.lemma_root].append(index)

    def offsets(self, lemma_root):
        return self._offsets[lemma_root]

class TransitionWordConcordanceIndex(ConcordanceIndex):
    def __init__(self, word_list):
        self._offsets = defaultdict(list)

        for index, word in enumerate(word_list):
            if hasattr(word, "suffixes") and word.suffixes:
                for suffix in word.suffixes:
                    self._offsets[suffix.word].append(index)

    def offsets(self, word):
        return self._offsets[word]

class TransitionMatchedWordConcordanceIndex(ConcordanceIndex):
    def __init__(self, word_list):
        self._offsets = defaultdict(list)

        for index, word in enumerate(word_list):
            if hasattr(word, "suffixes") and word.suffixes:
                for suffix in word.suffixes:
                    self._offsets[suffix.matched_word].append(index)

    def offsets(self, word):
        return self._offsets[word]

def print_concordance(word_list, offsets, width=75, lines=25):
    if offsets:
        half_width = (width - len(word_list[offsets[0]].str) - 2) / 2
        context = width/4 # approx number of words of context

        lines = min(lines, len(offsets))
        print "Displaying %s of %s matches:" % (lines, len(offsets))
        for i in offsets:
            if lines <= 0:
                break
            left = (' ' * half_width +
                    ' '.join([word.str for word in word_list[i-context:i]]))
            right = ' '.join([word.str for word in word_list[i+1:i+context]])
            word = word_list[i].str
            left = left[-half_width:]
            right = right[:half_width]
            sum = left + u' ' + word + u' ' + right
            sum = sum[0:width] if len(sum)>=width else sum
            print sum
            lines -= 1
    else:
        print "No matches"


def doit():
    dom = parse(os.path.join(os.path.dirname(__file__), '../testresources/parsesets/parseset005.xml'))
    parseset = ParseSetBinding.build(dom.getElementsByTagName("parseset")[0])
    word_list = []
    for sentence in parseset.sentences:
        word_list.extend(sentence.words)

    to_search = u"git"

    idx = CompleteWordConcordanceIndex(word_list)
    print_concordance(word_list, idx.offsets(to_search))
    print "\n\n"

    idx = StemConcordanceIndex(word_list)
    print_concordance(word_list, idx.offsets(to_search))
    print "\n\n"

    idx = DictionaryItemConcordanceIndex(word_list)
    print_concordance(word_list, idx.offsets(to_search))
    print "\n\n"

    idx = TransitionWordConcordanceIndex(word_list)
    print_concordance(word_list, idx.offsets(to_search))
    print "\n\n"

    idx = TransitionMatchedWordConcordanceIndex(word_list)
    print_concordance(word_list, idx.offsets(to_search))
    print "\n\n"


# similar

if __name__ == '__main__':
    doit()