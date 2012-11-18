from __future__ import division
from bson.code import Code
from collections import defaultdict
import json
import logging
from numpy.linalg import linalg
import operator
import numpy
import pprint

logger = logging.getLogger('ngramfrequencysmoother')

PLOTTING_MODE = False

class NGramFrequencySmoother(object):
    """
    "Simple Good-Turing" smoothing: For N_p's where p>smoothing_upper_count, c is not smoothed.

    Uses loglinregression if Nc=0, while calculating Nc+1.

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

        self._ngram_item_types = ['surface', 'stem', 'lemma_root']

    def initialize(self):
        self._vocabulary_sizes_for_ngram_item_types = self._find_vocabulary_sizes(self._ngram_item_types)
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("Found vocabulary sizes for ngram types : " + str(self._vocabulary_sizes_for_ngram_item_types))

        self._calculate_frequencies_of_ngram_frequencies()
        if logger.isEnabledFor(logging.DEBUG):
            # convert default dict to normal dict and then pprint it
            logger.debug("Found frequencies of ngram frequencies : " + pprint.pformat(json.loads(json.dumps(self._frequencies_of_ngram_frequencies))))

        self._calculate_loglinregression_coefficients()
        if logger.isEnabledFor(logging.DEBUG):
            # convert default dict to normal dict and then pprint it
            logger.debug("Loglin regression coefficients a : " + pprint.pformat(json.loads(json.dumps(self._loglinregression_m))))
            logger.debug("Loglin regression coefficients b : " + pprint.pformat(json.loads(json.dumps(self._loglinregression_c))))

    def _calculate_frequencies_of_ngram_frequencies(self):
        self._frequencies_of_ngram_frequencies = defaultdict(lambda: defaultdict(int))

        for frequency in range(0, self._smoothing_upper_count + 2):
            if self._ngram_length == 1:
                for target_type in self._ngram_item_types:
                    ngram_type, type_key = self._get_ngram_type_and_key(True, [], target_type)
                    frequency_of_frequency = self._find_frequency_of_frequency(ngram_type, frequency)
                    self._frequencies_of_ngram_frequencies[type_key][frequency] = frequency_of_frequency
            else:
                for context_type in self._ngram_item_types:
                    for context_is_leading in (True, False):
                        for target_type in self._ngram_item_types:
                            ngram_type, type_key = self._get_ngram_type_and_key(context_is_leading, context_type, target_type)
                            frequency_of_frequency = self._find_frequency_of_frequency(ngram_type, frequency)
                            self._frequencies_of_ngram_frequencies[type_key][frequency] = frequency_of_frequency

    def _find_frequency_of_frequency(self, ngram_type, frequency):
        logger.debug(" Finding freq of freq for freq={}, ngram_type={}".format(frequency, ngram_type))
        if frequency == 0:      # special treatment for frequency 0, estimate missing mass
            distinct_ngram_count_for_ngram_type = self._find_frequency_from_database(self._collection, ngram_type, None)
            possible_ngram_count_for_ngram_type = reduce(operator.mul,
                [self._vocabulary_sizes_for_ngram_item_types[ngram_type_item] for ngram_type_item in ngram_type])
            frequency_of_frequency_0 = possible_ngram_count_for_ngram_type - distinct_ngram_count_for_ngram_type
            logger.debug("  Distinct ngram count for ngram type = " + str(distinct_ngram_count_for_ngram_type))
            logger.debug("  Possible ngram count for ngram type = " + str(possible_ngram_count_for_ngram_type))
            logger.debug("  Frequency of frequency = " + str(frequency_of_frequency_0))
            return frequency_of_frequency_0
        else:
            frequency_from_database = self._find_frequency_from_database(self._collection, ngram_type, frequency)
            logger.debug("  Frequency of frequency = " + str(frequency_from_database))
            return frequency_from_database

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

    def _calculate_loglinregression_coefficients(self):
        self._loglinregression_m = {}
        self._loglinregression_c = {}

        if self._ngram_length == 1:
            for target_type in self._ngram_item_types:
                ngram_type, type_key = self._get_ngram_type_and_key(True, [], target_type)
                self._calculate_loglinregression_coefficients_for_ngram_type(type_key)
        else:
            for context_type in self._ngram_item_types:
                for context_is_leading in (True, False):
                    for target_type in self._ngram_item_types:
                        ngram_type, type_key = self._get_ngram_type_and_key(context_is_leading, context_type, target_type)
                        self._calculate_loglinregression_coefficients_for_ngram_type(type_key)


    def _calculate_loglinregression_coefficients_for_ngram_type(self, type_key):
        cs = self._frequencies_of_ngram_frequencies[type_key].keys()[1:]    # skip c=0
        Ns = self._frequencies_of_ngram_frequencies[type_key].values()[1:]  # skip c=0
        if not PLOTTING_MODE:
            m, c = self._loglinregression(cs, Ns)
            self._loglinregression_m[type_key] = m
            self._loglinregression_c[type_key] = c
        else:
            m0, c0 = self._linregression(cs, Ns)
            m1, c1 = self._loglinregression(cs, Ns)

            x0 = numpy.array(cs)
            y0 = numpy.array(Ns)

            x1 = numpy.log(numpy.array(cs))
            y1 = numpy.log(numpy.array(Ns))

            import matplotlib.pyplot as plt

            plt.plot(x0, y0, 'o', label='Original data', markersize=10)
            plt.plot(x0, m0 * x0 + c0, 'r', label='Lin fitted line, m={}, c={}'.format(m0, c0))
            plt.legend()
            plt.show()

            plt.plot(x1, y1, 'o', label='Log original data', markersize=10)
            plt.plot(x1, m1 * x1 + c1, 'r', label='Loglin fitted line, m={}, c={}'.format(m1, c1))
            plt.legend()
            plt.show()

            self._loglinregression_m[type_key] = m1
            self._loglinregression_c[type_key] = c1

    def _loglinregression(self, x, y):
        log_x = numpy.log(x)
        log_y = numpy.log(y)
        log_y[numpy.isinf(log_y)] = 0.0

        m, c = self._linregression(log_x, log_y)
        # if slope (m) is bigger than -1, then it is not log linear. but do nothing about it
        return m, c

    def _linregression(self, x, y):
        m, c = linalg.lstsq(numpy.vstack([x, numpy.ones(len(x))]).T, y)[0]
        return m, c

    def smooth(self, count, ngram_type):
        K = self._smoothing_upper_count
        type_key = '_'.join(ngram_type)       # something like "surface_surface_stem"

        logger.debug("Smoothing c value for c={}, ngram_type={}".format(count, str(ngram_type)))

        smoothed_count = 0

        if count == 0:
            # total probability of unseen (from definition) : N1 / N
            # total count of unseen : (N1 / N) * N = N1
            # since we're not calculating the probability, but the estimated count:
            # count of _one_ unseen : N1 / N0
            smoothed_count = (self._frequencies_of_ngram_frequencies[type_key][1] / self._frequencies_of_ngram_frequencies[type_key][0])
        elif count <= K:        # apply smoothing up to K. for bigger, the result is reliable enough
            N_c = self._frequencies_of_ngram_frequencies[type_key][count]
            N_c_1 = self._frequencies_of_ngram_frequencies[type_key][count + 1]
            N_k_1 = self._frequencies_of_ngram_frequencies[type_key][K + 1]
            N_1 = self._frequencies_of_ngram_frequencies[type_key][1]

            if logger.isEnabledFor(logging.DEBUG):
                Nc_values = {
                    'N_{}'.format(count): N_c,
                    'N_{}_1'.format(count): N_c_1,
                    'N_k_1': N_k_1,
                    'N_1': N_1,
                    }
                logger.debug("  Nc values without loglin mapping " + pprint.pformat(Nc_values))

            N_c = self._map_c_to_Nc(type_key, count) if N_c == 0 else N_c
            N_c_1 = self._map_c_to_Nc(type_key, count + 1) if N_c_1 == 0 else N_c_1
            N_k_1 = self._map_c_to_Nc(type_key, K + 1) if N_k_1 == 0 else N_k_1
            N_1 = self._map_c_to_Nc(type_key, 1) if N_1 == 0 else N_1

            if logger.isEnabledFor(logging.DEBUG):
                Nc_values = {
                    'N_{}'.format(count): N_c,
                    'N_{}_1'.format(count): N_c_1,
                    'N_k_1': N_k_1,
                    'N_1': N_1,
                    }
                logger.debug("  Nc values with loglin mapping      " + pprint.pformat(Nc_values))

            a = (N_c_1 / N_c)
            b = (K + 1) * N_k_1 / N_1

            smoothed_count = ((count + 1) * a - count * b) / (1 - b)
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug("  a={}, b={}, smoothed_count={}".format(a, b, smoothed_count))

        else:
            smoothed_count = count

        logger.debug(" Smoothed_count={}".format(smoothed_count))

        return smoothed_count

    def _map_c_to_Nc(self, ngram_type_key, count):
        m = self._loglinregression_m[ngram_type_key]
        c = self._loglinregression_c[ngram_type_key]
        val = (c + m * numpy.log(count)) if count != 0 else c
        Nc = numpy.exp([val])[0]

        return Nc

    def _get_ngram_type_and_key(self, context_is_leading, context_type, target_type):
        context_ngram_type = (self._ngram_length - 1) * [context_type]
        ngram_type = (context_ngram_type + [target_type]) if context_is_leading else ([target_type] + context_ngram_type)
        type_key = '_'.join(ngram_type)
        return ngram_type, type_key