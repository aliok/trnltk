# coding=utf-8
"""
There is no verification -yet- in test of this class.
The tests are there for making sure there is no run time exceptions
"""
import json
from pprint import pprint
import unittest
import pymongo
from trnltk.morphology.contextful.likelihoodmetrics.wordformcollocation.ngramfrequencysmoother import NGramFrequencySmoother

class NGramFrequencySmootherTestWithSampleData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(NGramFrequencySmootherTestWithSampleData, cls).setUpClass()

        cls._N = 2
        cls._K = 5

        mongodb_connection = pymongo.Connection(host='127.0.0.1')

        unigram_collection = mongodb_connection['trnltk']['ngramFrequencySmootherTest_unigram']
        bigram_collection = mongodb_connection['trnltk']['ngramFrequencySmootherTest_bigram']

        unigram_collection.drop()
        bigram_collection.drop()

        cls._create_sample_data(unigram_collection, bigram_collection)

        cls.smoother = NGramFrequencySmoother(cls._N, cls._K, bigram_collection, unigram_collection)
        cls.smoother.initialize()

    @classmethod
    def _create_sample_data(cls, unigram_collection, bigram_collection):
        item01 = {
            'word': {
                'surface': {
                    'value': 'A', 'syntactic_category': 'p'
                },
                'stem': {
                    'value': 'B', 'syntactic_category': 'q'
                },
                'lemma_root': {
                    'value': 'C', 'syntactic_category': 'r'
                }
            }
        }
        item02 = {
            'word': {
                'surface': {
                    'value': 'D', 'syntactic_category': 's'
                },
                'stem': {
                    'value': 'E', 'syntactic_category': 't'
                },
                'lemma_root': {
                    'value': 'F', 'syntactic_category': 'u'
                }
            }
        }
        item03 = {
            'word': {
                'surface': {
                    'value': 'A', 'syntactic_category': 'p'
                },
                'stem': {
                    'value': 'E', 'syntactic_category': 'q'
                },
                'lemma_root': {
                    'value': 'I', 'syntactic_category': 'r'
                }
            }
        }
        item04 = {
            'word': {
                'surface': {
                    'value': 'J', 'syntactic_category': 's'
                },
                'stem': {
                    'value': 'B', 'syntactic_category': 't'
                },
                'lemma_root': {
                    'value': 'F', 'syntactic_category': 'u'
                }
            }
        }
        item05 = {
            'word': {
                'surface': {
                    'value': 'D', 'syntactic_category': 'p'
                },
                'stem': {
                    'value': 'N', 'syntactic_category': 'q'
                },
                'lemma_root': {
                    'value': 'C', 'syntactic_category': 'r'
                }
            }
        }

        unigram_collection.insert({'item_0': item01})
        unigram_collection.insert({'item_0': item02})
        unigram_collection.insert({'item_0': item03})
        unigram_collection.insert({'item_0': item04})
        unigram_collection.insert({'item_0': item05})

        unigram_collection.insert({'item_0': item01})
        unigram_collection.insert({'item_0': item02})

        bigram_collection.insert({
            'item_0': item01,
            'item_1': item02
        })

        bigram_collection.insert({
            'item_0': item02,
            'item_1': item03
        })

        bigram_collection.insert({
            'item_0': item03,
            'item_1': item04
        })

        bigram_collection.insert({
            'item_0': item04,
            'item_1': item05
        })

        bigram_collection.insert({
            'item_0': item01,
            'item_1': item02
        })

    def test_smooth(self):
        pprint(json.loads(json.dumps(self.smoother._frequencies_of_ngram_frequencies)))
        pprint(json.loads(json.dumps(self.smoother._vocabulary_sizes_for_ngram_item_types)))

        print

        types = ['surface', 'stem', 'lemma_root']
        up = self._K + 4

        for i, ngram_item_type_0 in enumerate(types):
            for j, ngram_item_type_1 in enumerate(types):
                for c in range(0, up + 1):
                    smooth_c = self.smoother.smooth(c, [ngram_item_type_0, ngram_item_type_1])
                    print "c={}, type<{},{}> ==> c*={}".format(c, ngram_item_type_0, ngram_item_type_1, smooth_c)

                print '\n'


class NGramFrequencySmootherTestWithDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(NGramFrequencySmootherTestWithDatabase, cls).setUpClass()

        cls.mongodb_connection = pymongo.Connection(host='127.0.0.1')


    def test_smooth_with_bigrams(self):
        N = 2
        K = 5
        parseset_index = "001"

        self._test_smooth_with_ngrams(N, K, parseset_index)

    def _test_smooth_with_ngrams(self, N, K, parseset_index):
        unigram_collection = self.mongodb_connection['trnltk']['wordUnigrams{}'.format(parseset_index)]
        bigram_collection = self.mongodb_connection['trnltk']['wordBigrams{}'.format(parseset_index)]
        trigram_collection = self.mongodb_connection['trnltk']['wordTrigrams{}'.format(parseset_index)]

        collection = None

        if N==1:
            collection = unigram_collection
        elif N==2:
            collection = bigram_collection
        elif N==3:
            collection = trigram_collection
        else:
            raise Exception("N>3 is not supported in tests!")

        smoother = NGramFrequencySmoother(N, K, collection, unigram_collection)

        smoother.initialize()

        pprint(json.loads(json.dumps(smoother._frequencies_of_ngram_frequencies)))
        pprint(json.loads(json.dumps(smoother._vocabulary_sizes_for_ngram_item_types)))

        print

        types = ['surface', 'stem', 'lemma_root']
        up = K + 4

        for i, ngram_item_type_0 in enumerate(types):
            for j, ngram_item_type_1 in enumerate(types):
                for leading in [True, False]:
                    for c in range(0, up + 1):
                        ngram_type = (([ngram_item_type_0] * (N - 1)) + [ngram_item_type_1]) if leading else ([ngram_item_type_1] + ([ngram_item_type_0] * (N - 1)))
                        smooth_c = smoother.smooth(c, ngram_type)
                        print "c={}, type={} ==> c*={}".format(c, ngram_type, smooth_c)
                    print '\n'


if __name__ == '__main__':
    unittest.main()
