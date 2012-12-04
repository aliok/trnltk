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
from __future__ import division
import json
import logging
import operator
import pprint
from trnltk.morphology.contextful.likelihoodmetrics.hidden.ngramtypefrequencyfinder import NgramTypeFrequencyFinder
from trnltk.morphology.contextful.likelihoodmetrics.hidden.simplegoodturing import SimpleGoodTuringSmoother

logger = logging.getLogger('ngramfrequencysmoother')

PLOTTING_MODE = False

class NGramFrequencySmoother(object):
    def initialize(self):
        raise NotImplementedError()

    def smooth(self, count, ngram_type):
        raise NotImplementedError()


class CachedSimpleGoodTuringNGramFrequencySmoother(NGramFrequencySmoother):
    """
    Since SimpleGoodTuringNGramFrequencySmoother cannot be used in real-time (too slow) and smoothed values
    don't change over time if knowledge is not changing too, smoothed values can be cached.

    Uses generated values from test_simplegoodturingngramfrequencysmoother.py

    In a production environment, a similar logic should be used. However, values must be hold in a db and
    smoothing should be done incrementally (update values considering new ngrams).
    """

    def __init__(self):
        super(CachedSimpleGoodTuringNGramFrequencySmoother, self).__init__()

        self._bigram_smoothed_frequencies = {
            'surface_surface_0': 0.000123425512116,
            'surface_surface_1': 0.108999917508,
            'surface_surface_2': 0.7211039089,
            'surface_surface_3': 1.80180333319,
            'surface_surface_4': 2.90503258449,
            'surface_surface_5': 3.43060225833,

            'surface_stem_0': 0.00022860945759,
            'surface_stem_1': 0.133121743817,
            'surface_stem_2': 0.821048687544,
            'surface_stem_3': 1.72898136936,
            'surface_stem_4': 2.80142813265,
            'surface_stem_5': 3.40034048232,

            'surface_lemma_root_0': 0.000398378900614,
            'surface_lemma_root_1': 0.145298329356,
            'surface_lemma_root_2': 0.898302276993,
            'surface_lemma_root_3': 1.6804091374,
            'surface_lemma_root_4': 2.72640794743,
            'surface_lemma_root_5': 4.18204717541,

            'stem_surface_0': 0.000225091760951,
            'stem_surface_1': 0.131174483367,
            'stem_surface_2': 0.776106338802,
            'stem_surface_3': 1.83209725514,
            'stem_surface_4': 2.87394819337,
            'stem_surface_5': 3.48336420633,

            'stem_stem_0': 0.000407209734465,
            'stem_stem_1': 0.169074407696,
            'stem_stem_2': 0.856675152649,
            'stem_stem_3': 1.75574822879,
            'stem_stem_4': 2.90701020882,
            'stem_stem_5': 3.25804752031,

            'stem_lemma_root_0': 0.000693373280741,
            'stem_lemma_root_1': 0.190889854104,
            'stem_lemma_root_2': 0.942544322168,
            'stem_lemma_root_3': 1.6487501381,
            'stem_lemma_root_4': 2.94332419882,
            'stem_lemma_root_5': 3.90563370524,

            'lemma_root_surface_0': 0.00039035813432,
            'lemma_root_surface_1': 0.142654089676,
            'lemma_root_surface_2': 0.790363818635,
            'lemma_root_surface_3': 2.01468100259,
            'lemma_root_surface_4': 2.99365181917,
            'lemma_root_surface_5': 3.03071229674,

            'lemma_root_stem_0': 0.000695132297003,
            'lemma_root_stem_1': 0.188806572288,
            'lemma_root_stem_2': 0.889023922574,
            'lemma_root_stem_3': 1.85882338782,
            'lemma_root_stem_4': 2.97753621167,
            'lemma_root_stem_5': 2.84911840754,

            'lemma_root_lemma_root_0': 0.00117028598239,
            'lemma_root_lemma_root_1': 0.216058157008,
            'lemma_root_lemma_root_2': 0.967023392214,
            'lemma_root_lemma_root_3': 1.78431415531,
            'lemma_root_lemma_root_4': 2.90467308233,
            'lemma_root_lemma_root_5': 3.53232742842,
            }

        self._trigram_smoothed_frequencies = {
            'surface_surface_surface_0': 9.22687755635e-09,
            'surface_surface_surface_1': 0.0286890410384,
            'surface_surface_surface_2': 0.46959983179,
            'surface_surface_surface_3': 1.34420357649,
            'surface_surface_surface_4': 2.29600991759,
            'surface_surface_surface_5': 2.115467769,

            'surface_surface_stem_0': 1.83710091123e-08,
            'surface_surface_stem_1': 0.0342590629637,
            'surface_surface_stem_2': 0.454439768923,
            'surface_surface_stem_3': 1.24755140979,
            'surface_surface_stem_4': 2.8734259063,
            'surface_surface_stem_5': 2.86658432497,

            'surface_surface_lemma_root_0': 3.35868516445e-08,
            'surface_surface_lemma_root_1': 0.0375710847479,
            'surface_surface_lemma_root_2': 0.45842390544,
            'surface_surface_lemma_root_3': 1.04665449463,
            'surface_surface_lemma_root_4': 3.78345221326,
            'surface_surface_lemma_root_5': 2.56770432396,

            'stem_stem_surface_0': 3.64377596779e-08,
            'stem_stem_surface_1': 0.0405367686527,
            'stem_stem_surface_2': 0.530384698807,
            'stem_stem_surface_3': 1.35378088733,
            'stem_stem_surface_4': 1.94598215017,
            'stem_stem_surface_5': 3.12754463348,

            'stem_stem_stem_0': 7.21961950054e-08,
            'stem_stem_stem_1': 0.0483937710988,
            'stem_stem_stem_2': 0.533755125978,
            'stem_stem_stem_3': 1.45812077501,
            'stem_stem_stem_4': 2.16698963187,
            'stem_stem_stem_5': 3.08666805263,

            'stem_stem_lemma_root_0': 1.31694702881e-07,
            'stem_stem_lemma_root_1': 0.0529987276796,
            'stem_stem_lemma_root_2': 0.537959555351,
            'stem_stem_lemma_root_3': 1.21802890146,
            'stem_stem_lemma_root_4': 2.92575101378,
            'stem_stem_lemma_root_5': 2.92137188033,

            'lemma_root_lemma_root_surface_0': 1.21279094728e-07,
            'lemma_root_lemma_root_surface_1': 0.0491118077325,
            'lemma_root_lemma_root_surface_2': 0.53776683087,
            'lemma_root_lemma_root_surface_3': 1.16598647503,
            'lemma_root_lemma_root_surface_4': 2.57767890248,
            'lemma_root_lemma_root_surface_5': 2.99582027168,

            'lemma_root_lemma_root_stem_0': 2.39776948949e-07,
            'lemma_root_lemma_root_stem_1': 0.0579459938026,
            'lemma_root_lemma_root_stem_2': 0.55871041893,
            'lemma_root_lemma_root_stem_3': 1.26626723082,
            'lemma_root_lemma_root_stem_4': 2.55677128883,
            'lemma_root_lemma_root_stem_5': 3.13743122747,

            'lemma_root_lemma_root_lemma_root_0': 4.36996140548e-07,
            'lemma_root_lemma_root_lemma_root_1': 0.0631832582214,
            'lemma_root_lemma_root_lemma_root_2': 0.56597215725,
            'lemma_root_lemma_root_lemma_root_3': 1.11055698449,
            'lemma_root_lemma_root_lemma_root_4': 3.09837845226,
            'lemma_root_lemma_root_lemma_root_5': 2.9321533977,

            'surface_stem_stem_0': 3.64963450539e-08,
            'surface_stem_stem_1': 0.0394099232386,
            'surface_stem_stem_2': 0.518668707403,
            'surface_stem_stem_3': 1.14636801272,
            'surface_stem_stem_4': 2.60165262233,
            'surface_stem_stem_5': 3.35704618551,

            'surface_lemma_root_lemma_root_0': 1.21769143243e-07,
            'surface_lemma_root_lemma_root_1': 0.0462806332683,
            'surface_lemma_root_lemma_root_2': 0.550582741383,
            'surface_lemma_root_lemma_root_3': 0.903313123313,
            'surface_lemma_root_lemma_root_4': 3.29622779939,
            'surface_lemma_root_lemma_root_5': 3.48031985225,

            'stem_surface_surface_0': 1.83733426303e-08,
            'stem_surface_surface_1': 0.0341145060813,
            'stem_surface_surface_2': 0.512360626489,
            'stem_surface_surface_3': 1.26584365284,
            'stem_surface_surface_4': 2.10918996294,
            'stem_surface_surface_5': 2.52379985859,

            'stem_lemma_root_lemma_root_0': 2.40131492071e-07,
            'stem_lemma_root_lemma_root_1': 0.0567626710285,
            'stem_lemma_root_lemma_root_2': 0.574378576896,
            'stem_lemma_root_lemma_root_3': 1.14378042296,
            'stem_lemma_root_lemma_root_4': 2.86320962549,
            'stem_lemma_root_lemma_root_5': 3.20384010593,

            'lemma_root_surface_surface_0': 3.3573280622e-08,
            'lemma_root_surface_surface_1': 0.0378749147921,
            'lemma_root_surface_surface_2': 0.497538057059,
            'lemma_root_surface_surface_3': 1.09560828421,
            'lemma_root_surface_surface_4': 2.85568215016,
            'lemma_root_surface_surface_5': 2.49680470348,

            'lemma_root_stem_stem_0': 1.3152470358e-07,
            'lemma_root_stem_stem_1': 0.0542902949509,
            'lemma_root_stem_stem_2': 0.522993420085,
            'lemma_root_stem_stem_3': 1.29971843048,
            'lemma_root_stem_stem_4': 2.63171795211,
            'lemma_root_stem_stem_5': 2.91787697511,
            }

    def initialize(self):
        # do nothing
        pass

    def smooth(self, count, ngram_type):
        assert int(count) == count        # should be integer (could be int, stored in float)
        assert count >= 0

        if count > 5:
            return count

        if len(ngram_type) == 1:
            # We cannot determine the vocabulary size and thus N_0. So, smoothing cannot be applied for unigrams.
            return count

        key = '_'.join(ngram_type) + '_' + str(int(count))
        if len(ngram_type) == 2:
            return self._bigram_smoothed_frequencies[key]
        elif len(ngram_type) == 3:
            return self._trigram_smoothed_frequencies[key]
        else:
            raise Exception("{}-grams are not supported".format(len(ngram_type)))


class SimpleGoodTuringNGramFrequencySmoother(NGramFrequencySmoother):
    """
    "Simple Good-Turing" smoothing with threshold. For N_p's where p>smoothing_threshold, c is not smoothed.

    Uses loglinregression if Nc=0, while calculating Nc+1.

    Doesn't work with unigrams, since the unseen count cannot be estimated.

    What is different:

     -- surface, stem, lemma_root difference in vocabulary size, while calculating the c* value for N0

     -- ngram types : calculations for e.g. NGrams with types <stem,stem,surface> and <lexeme,lexeme,surface> are different
    """
    #TODO: how about the smoothing logic used in contextless distribution for unigram smoothing?
    def __init__(self, ngram_length, smoothing_threshold, collection, unigram_collection):
        super(SimpleGoodTuringNGramFrequencySmoother, self).__init__()

        self._ngram_length = ngram_length
        self._smoothing_threshold = smoothing_threshold
        self._collection = collection
        self._unigram_collection = unigram_collection
        self._ngram_type_frequency_finder = NgramTypeFrequencyFinder()

        assert ngram_length >= 2
        assert smoothing_threshold > 1

        self._ngram_item_types = ['surface', 'stem', 'lemma_root']

        self._smoothers_for_ngram_types = {}

    def initialize(self):
        self._vocabulary_sizes_for_ngram_item_types = self._find_vocabulary_sizes(self._ngram_item_types)
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("Found vocabulary sizes for ngram types : " + str(self._vocabulary_sizes_for_ngram_item_types))

        for context_type in self._ngram_item_types:
            for context_is_leading in (True, False):
                for target_type in self._ngram_item_types:
                    ngram_type, type_key = self._get_ngram_type_and_key(context_is_leading, context_type, target_type)

                    if type_key in self._smoothers_for_ngram_types:
                        # stuff already calculated, smoother already created!
                        continue

                    distinct_ngram_count_for_ngram_type = NgramTypeFrequencyFinder.find_distinct_count(self._collection, ngram_type)
                    possible_ngram_count_for_ngram_type = reduce(operator.mul,
                        [self._vocabulary_sizes_for_ngram_item_types[ngram_type_item] for ngram_type_item in ngram_type])
                    frequency_of_frequency_0 = possible_ngram_count_for_ngram_type - distinct_ngram_count_for_ngram_type
                    logger.debug("  Distinct ngram count for ngram type = " + str(distinct_ngram_count_for_ngram_type))
                    logger.debug("  Possible ngram count for ngram type = " + str(possible_ngram_count_for_ngram_type))
                    logger.debug("  Frequency of frequency 0 (unseen) = " + str(frequency_of_frequency_0))

                    frequencies_of_frequencies_for_ngram_type = {}
                    for i in range(1, self._smoothing_threshold + 2):
                        frequencies_of_frequencies_for_ngram_type[i] = self._find_frequency_of_frequency(ngram_type, i)

                    smoother = SimpleGoodTuringSmoother(self._smoothing_threshold, frequencies_of_frequencies_for_ngram_type, frequency_of_frequency_0)
                    self._smoothers_for_ngram_types[type_key] = smoother

        for ngram_type_key, smoother in self._smoothers_for_ngram_types.iteritems():
            smoother.initialize(PLOTTING_MODE)

        if logger.isEnabledFor(logging.DEBUG):
            for ngram_type_key, smoother in self._smoothers_for_ngram_types.iteritems():
                # convert default dict to normal dict and then pprint it
                logger.debug("Found frequencies of ngram frequencies for {}: " + pprint.pformat(json.loads(json.dumps(smoother._frequencies_of_frequencies))))
                logger.debug("Found unseen for {}: {}".format(smoother._unseen_count))

        if logger.isEnabledFor(logging.DEBUG):
            for ngram_type_key, smoother in self._smoothers_for_ngram_types.iteritems():
                # convert default dict to normal dict and then pprint it
                logger.debug("Loglin regression coefficient m for {}: ".format(ngram_type_key, smoother._loglinregression_m))
                logger.debug("Loglin regression coefficient c for {}: ".format(ngram_type_key, smoother._loglinregression_c))

    def _find_frequency_of_frequency(self, ngram_type, frequency):
        assert frequency > 0 and ngram_type
        logger.debug(" Finding freq of freq for freq={}, ngram_type={}".format(frequency, ngram_type))
        frequency_from_database = NgramTypeFrequencyFinder.find_frequency_of_frequency(self._collection, ngram_type, frequency)
        logger.debug("  Frequency of frequency = " + str(frequency_from_database))
        return frequency_from_database

    def _find_vocabulary_sizes(self, ngram_item_types):
        """
        @return: Vocabulary sizes, which is number of distinct unigrams for surfaces, stems and lexemes
        @rtype: list
        """
        vocabulary_sizes_for_types = {}
        for ngram_item_type in ngram_item_types:
            vocabulary_size_for_type = NgramTypeFrequencyFinder.find_distinct_count(self._unigram_collection, [ngram_item_type])
            vocabulary_sizes_for_types[ngram_item_type] = vocabulary_size_for_type

        return vocabulary_sizes_for_types

    def smooth(self, count, ngram_type):
        logger.debug("Smoothing c value for c={}, ngram_type={}".format(count, str(ngram_type)))

        if len(ngram_type) == 1:
            # We cannot determine the vocabulary size and thus N_0. So, smoothing cannot be applied for unigrams.
            logger.debug("Smoothing cannot be applied for unigrams, returning the count")
            return count

        type_key = '_'.join(ngram_type)       # something like "surface_surface_stem"
        return self._smoothers_for_ngram_types[type_key].smooth(count)

    def _get_ngram_type_and_key(self, context_is_leading, context_type, target_type):
        context_ngram_type = (self._ngram_length - 1) * [context_type]
        ngram_type = (context_ngram_type + [target_type]) if context_is_leading else ([target_type] + context_ngram_type)
        type_key = '_'.join(ngram_type)
        return ngram_type, type_key