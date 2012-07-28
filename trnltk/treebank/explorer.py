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


# similar

def print_concordance(full_words, offsets, width=75, lines=25):
    if offsets:
        half_width = (width - len(full_words[offsets[0]]) - 2) / 2
        context = width/4 # approx number of words of context

        lines = min(lines, len(offsets))
        print "Displaying %s of %s matches:" % (lines, len(offsets))
        for i in offsets:
            if lines <= 0:
                break
            left = (' ' * half_width +
                    ' '.join(full_words[i-context:i]))
            right = ' '.join(full_words[i+1:i+context])
            word = full_words[i]
            left = left[-half_width:]
            right = right[:half_width]
            sum = left + u' ' + word + u' ' + right
            sum = sum[0:width] if len(sum)>=width else sum
            print sum
            lines -= 1
    else:
        print "No matches"


class FullWordConcordanceIndex(object):
    def __init__(self, full_words):
        self._full_words = full_words
        self._offsets = defaultdict(list)

        for index, full_word in enumerate(full_words):
            self._offsets[full_word].append(index)

    def offsets(self, word):
        return self._offsets[word]


class StemConcordanceIndex(object):
    def __init__(self, word_stem_tuples):
        self._full_words = [full_word for (full_word, stem) in word_stem_tuples]
        self._offsets = defaultdict(list)

        for index, (full_word, stem) in enumerate(word_stem_tuples):
            if stem:
                self._offsets[stem].append(index)

    def offsets(self, word):
        return self._offsets[word]


class DictionaryItemConcordanceIndex(object):
    def __init__(self, word_lemma_root_tuples):
        self._full_words = [full_word for (full_word, lemma_root) in word_lemma_root_tuples]
        self._offsets = defaultdict(list)

        for index, (full_word, lemma_root) in enumerate(word_lemma_root_tuples):
            if lemma_root:
                self._offsets[lemma_root].append(index)

    def offsets(self, word):
        return self._offsets[word]

class TransitionWordConcordanceIndex(object):
    def __init__(self, word_transition_list_tuples):
        self._full_words = [full_word for (full_word, transition_list) in word_transition_list_tuples]
        self._offsets = defaultdict(list)

        for index, (full_word, transition_list) in enumerate(word_transition_list_tuples):
            if transition_list:
                for transition in transition_list:
                    self._offsets[transition].append(index)

    def offsets(self, word):
        return self._offsets[word]

class TransitionMatchedWordConcordanceIndex(object):
    def __init__(self, word_transition_list_tuples):
        self._full_words = [full_word for (full_word, transition_list) in word_transition_list_tuples]
        self._offsets = defaultdict(list)

        for index, (full_word, transition_list) in enumerate(word_transition_list_tuples):
            if transition_list:
                for transition in transition_list:
                    self._offsets[transition].append(index)

    def offsets(self, word):
        return self._offsets[word]


def doit():
    dom = parse(os.path.join(os.path.dirname(__file__), '../testresources/parsesets/parseset005.xml'))
    parseset = ParseSetBinding.build(dom.getElementsByTagName("parseset")[0])
    full_words = []
    for sentence in parseset.sentences:
        for word in sentence.words:
            full_words.append(word.str)

    word_stem_tuples = []
    for sentence in parseset.sentences:
        for word in sentence.words:
            word_stem_tuples.append((word.str, word.stem.root if hasattr(word, "stem") else None))

    word_lemma_root_tuples = []
    for sentence in parseset.sentences:
        for word in sentence.words:
            word_lemma_root_tuples.append((word.str, word.stem.lemma_root if hasattr(word, "stem") else None))

    word_transition_list_tuples = []
    for sentence in parseset.sentences:
        for word in sentence.words:
            transitions_for_word = set()
            if hasattr(word, "suffixes"):
                for suffix in word.suffixes:
                    transitions_for_word.add(suffix.word)
            word_transition_list_tuples.append((word, sorted(list(transitions_for_word))))

    word_matched_transition_list_tuples = []
    for sentence in parseset.sentences:
        for word in sentence.words:
            transitions_for_word = set()
            if hasattr(word, "suffixes"):
                for suffix in word.suffixes:
                    transitions_for_word.add(suffix.matched_word)
            word_matched_transition_list_tuples.append((word, sorted(list(transitions_for_word))))

    to_search = u"yap"

    print len(full_words)
    idx = FullWordConcordanceIndex(full_words)
    print_concordance(full_words, idx.offsets(to_search))
    print "\n\n"

    idx = StemConcordanceIndex(word_stem_tuples)
    print_concordance(full_words, idx.offsets(to_search))
    print "\n\n"

    idx = DictionaryItemConcordanceIndex(word_lemma_root_tuples)
    print_concordance(full_words, idx.offsets(to_search))
    print "\n\n"

    idx = TransitionWordConcordanceIndex(word_transition_list_tuples)
    print_concordance(full_words, idx.offsets(to_search))
    print "\n\n"

    idx = TransitionMatchedWordConcordanceIndex(word_matched_transition_list_tuples)
    print_concordance(full_words, idx.offsets(to_search))
    print "\n\n"


if __name__ == '__main__':
    doit()