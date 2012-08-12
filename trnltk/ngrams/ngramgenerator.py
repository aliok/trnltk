from collections import  deque
from trnltk.parseset.xmlbindings import UnparsableWordBinding, DerivationalSuffixBinding

class NGramGenerator(object):
    def __init__(self, n, extractor, start_of_sentence, end_of_sentence):
        self._n = n
        self.extractor = extractor
        self.start_of_sentence = start_of_sentence
        self.end_of_sentence = end_of_sentence

    def get_ngrams(self, sentence_bindings):
        return [t for t in self.iter_ngrams(sentence_bindings)]

    def iter_ngrams(self, sentence_bindings):
        for sentence_binding in sentence_bindings:
            queue = NGramQueue(self._n, self.start_of_sentence, self.end_of_sentence)
            for word_binding in sentence_binding.words:
                if isinstance(word_binding, UnparsableWordBinding):
                    continue

                yield queue.put(self.extractor(word_binding))

            end_n_grams = queue.end()
            for end_n_gram in end_n_grams:
                yield end_n_gram


class NGramQueue(object):
    def __init__(self, size, start_of_sentence, end_of_sentence):
        self.size = size
        self.start_of_sentence = start_of_sentence
        self.end_of_sentence = end_of_sentence

        self.items = deque(maxlen=self.size)

        for i in range(0, size):
            self.items.append(self.start_of_sentence)


    def put(self, token):
        self.items.append(token)
        return tuple(self.items)

    def end(self):
        for i in range(0, self.size - 1):
            yield self.put(self.end_of_sentence)


class WordNGramGenerator(NGramGenerator):

    START_WORD = {
        'word' : {
            'surface' : {'value': '<s>', 'syntactic_category' : '<s>'},
            'stem' : {'value': '<s>', 'syntactic_category' : '<s>'},
            'lemma_root' : {'value': '<s>', 'syntactic_category' : '<s>'}
        }
    }
    END_WORD = {
        'word' : {
            'surface' : {'value': '</s>', 'syntactic_category' : '</s>'},
            'stem' : {'value': '</s>', 'syntactic_category' : '</s>'},
            'lemma_root' : {'value': '</s>', 'syntactic_category' : '</s>'}
        }
    }

    def __init__(self, n):
        super(WordNGramGenerator, self).__init__(n, self._extract_trigram_item, self.START_WORD, self.END_WORD)


    @classmethod
    def _extract_trigram_item(cls, word_binding):
        """
        @type word_binding: WordBinding
        @return:
        """

        surface_str, surface_syntactic_category = word_binding.str, word_binding.syntactic_category
        stem_str, stem_syntactic_category = cls._get_stem(word_binding)
        lemma_root_str, lemma_root_syntactic_category = word_binding.root.lemma_root, word_binding.root.syntactic_category


        return {
            'word' : {
                'surface' : {'value': surface_str, 'syntactic_category' : surface_syntactic_category},
                'stem' : {'value': stem_str, 'syntactic_category' : stem_syntactic_category},
                'lemma_root' : {'value': lemma_root_str, 'syntactic_category' : lemma_root_syntactic_category}
            }
        }

    @classmethod
    def _get_stem(cls, word_binding):
        """
        Returns the stem of the surface. For example, stem of "kitapcilar" is "kitapci".
        So, the finding process is basically removing the inflections at the end, until there is a derivation.
        @type word_binding: WordBinding
        """

        if not word_binding.suffixes:
            return word_binding.str, word_binding.syntactic_category


        indexes_of_derivational_suffixes = [i for i in range(len(word_binding.suffixes)) if isinstance(word_binding.suffixes[i], DerivationalSuffixBinding)]
        if indexes_of_derivational_suffixes:
            index_of_last_derivational_suffix = indexes_of_derivational_suffixes[-1]
            return word_binding.suffixes[index_of_last_derivational_suffix].word, word_binding.suffixes[index_of_last_derivational_suffix].to_syntactic_category
        else:
            return word_binding.root.lemma_root, word_binding.root.syntactic_category