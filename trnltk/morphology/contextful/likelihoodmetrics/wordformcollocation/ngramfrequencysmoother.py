from bson.code import Code
from collections import defaultdict
import operator

class NGramFrequencySmoother(object):
    """
    "Simple Good-Turing" smoothing: For N_p's where p>smoothing_upper_count, c is not smoothed.

    What is different:

     -- surface, stem, lemma_root difference in vocabulary size, while calculating the c* value for N0

     -- ngram types : calculations for e.g. NGrams with types <stem,stem,surface> and <lexeme,lexeme,surface> are different
    """

    def __init__(self, ngram_length, smoothing_upper_count, collection, unigram_collection):
        self._ngram_length = ngram_length
        self._smoothing_upper_count = smoothing_upper_count
        self._collection = collection
        self._unigram_collection = unigram_collection

        assert ngram_length >= 1
        assert smoothing_upper_count > 1

    def calculate_frequencies_of_ngram_frequencies(self):
        ngram_item_types = ['surface', 'stem', 'lemma_root']

        self._frequencies_of_ngram_frequencies = defaultdict(lambda: defaultdict(int))

        vocabulary_sizes_for_ngram_item_types = self._find_vocabulary_sizes(ngram_item_types)

        for frequency in range(0, self._smoothing_upper_count + 2):
            if self._ngram_length == 1:
                for target_type in ngram_item_types:
                    ngram_type = [target_type]
                    type_key = '_'.join(ngram_type)
                    frequency_of_frequency = self._find_frequency_of_frequency(ngram_type, frequency, vocabulary_sizes_for_ngram_item_types)
                    self._frequencies_of_ngram_frequencies[type_key][frequency] = frequency_of_frequency
            else:
                for context_type in ngram_item_types:
                    for context_is_leading in (True, False):
                        for target_type in ngram_item_types:
                            context_ngram_type = (self._ngram_length - 1) * [context_type]
                            ngram_type = (context_ngram_type + [target_type]) if context_is_leading else ([target_type] + context_ngram_type)

                            type_key = '_'.join(ngram_type)
                            frequency_of_frequency = self._find_frequency_of_frequency(ngram_type, frequency, vocabulary_sizes_for_ngram_item_types)
                            self._frequencies_of_ngram_frequencies[type_key][frequency] = frequency_of_frequency

    def _find_frequency_of_frequency(self, ngram_type, frequency, vocabulary_sizes):
        if frequency == 0:      # special treatment for frequency 0
            distinct_ngram_count_for_ngram_type = self._find_frequency_from_database(self._collection, ngram_type, None)
            possible_ngram_count_for_ngram_type = reduce(operator.mul, [vocabulary_sizes[ngram_type_item] for ngram_type_item in ngram_type])
            frequency_of_frequency_0 = possible_ngram_count_for_ngram_type - distinct_ngram_count_for_ngram_type
            return frequency_of_frequency_0
        else:
            return self._find_frequency_from_database(self._collection, ngram_type, frequency)

    def _find_vocabulary_sizes(self, ngram_item_types):
        """
        @return: Vocabulary sizes, which is number of distinct unigrams for surfaces, stems and lexemes
        @rtype: list
        """
        vocabulary_sizes_for_types = {}
        for ngram_item_type in ngram_item_types:
            vocabulary_size_for_type = self._find_frequency_from_database(self._unigram_collection, [ngram_item_type], None)
            vocabulary_sizes_for_types[ngram_item_type] = vocabulary_size_for_type

        return vocabulary_sizes_for_types

    @classmethod
    def _find_frequency_from_database(cls, collection, ngram_type, frequency=None):
        """
        Finds the frequency of given frequency, if frequency is provided.
        If frequency is None, then frequency control is ignored; thus count of distinct items for ngram_type is returned.
        For frequency 0, this method should not be used!
        @type ngram_type: list
        @type frequency: None or int
        @rtype: int
        """
        assert frequency is None or frequency > 0

        emission_keys = ''
        for i, ngram_type_item in enumerate(ngram_type):
            emission_keys += "emission_key_val{}:this.item_{}.word.{}.value, ".format(i, i, ngram_type_item)
            emission_keys += "emission_key_cat{}:this.item_{}.word.{}.syntactic_category, ".format(i, i, ngram_type_item)

            # will be something like
            #emission_key_val0:this.item_0.word.surface.value, emission_key_cat0:this.item_0.word.surface.syntactic_category
            #emission_key_val1:this.item_1.word.surface.value, emission_key_cat1:this.item_1.word.surface.syntactic_category
            #emission_key_val2:this.item_2.word.stem.value,    emission_key_cat2:this.item_2.word.stem.syntactic_category

        filter_criteria = {"value.count": frequency} if frequency is not None else None
        mapper = Code("""
                    function(){
                        emit({
                            """ + emission_keys + """
                        }, {count: 1});
                    }
                """)
        reducer = Code("""
                    function(key,values){
                        var total = 0;
                        for (var i = 0; i < values.length; i++) {
                            total += values[i].count
                        }

                        return {count:total};
                    }
                """)

        result = collection.map_reduce(mapper, reducer, "_temporary")

        if filter_criteria:
            result = result.find(filter_criteria)

        return result.count()

    def smooth(self, count, ngram_type):
        K = self._smoothing_upper_count
        type_key = '_'.join(ngram_type)       # something like "surface_surface_stem"

        smoothed_count = 0

        if count == 0:
            smoothed_count = (count + 1) * (self._frequencies_of_ngram_frequencies[type_key][1] / self._frequencies_of_ngram_frequencies[type_key][0])
            #TODO: divide by unseen vocabulary count?
        elif count <= K:
            a = (count + 1) * (self._frequencies_of_ngram_frequencies[type_key][1] / self._frequencies_of_ngram_frequencies[type_key][0])
            b = (count * (K + 1) * self._frequencies_of_ngram_frequencies[type_key][K + 1]) / self._frequencies_of_ngram_frequencies[type_key][1]

            smoothed_count = (a - b) / (1 - b)
        else:
            smoothed_count = count

        return smoothed_count
