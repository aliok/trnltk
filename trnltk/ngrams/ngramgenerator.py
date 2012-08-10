from collections import  deque
from trnltk.parseset.xmlbindings import UnparsableWordBinding

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