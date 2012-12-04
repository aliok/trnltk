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
import logging
from pprint import pformat
from trnltk.morphology.contextful.likelihoodmetrics.hidden.ngramtypefrequencyfinder import NgramTypeFrequencyFinder
from trnltk.morphology.contextful.likelihoodmetrics.hidden.simplegoodturing import SimpleGoodTuringSmoother

logger = logging.getLogger('contextlessDistributionSmoother')

class ContextlessDistributionSmoother(object):
    def initialize(self):
        raise NotImplementedError()

    def smooth_parse_result_occurrence_count(self, parse_result_occurrence_count):
        raise NotImplementedError()

    def smooth_word_occurrence_count(self, word_occurrence_count):
        raise NotImplementedError()


class CachedContextlessDistributionSmoother(ContextlessDistributionSmoother):
    """
     Since SimpleGoodTuringContextlessDistributionSmoother takes a lot of time to initialize,
     this class returns the smooth counts which are calculated before.

     The values are calculated using test_simplegoodturingcontextlessdistributionsmoother.py.

     In a production app, these values should be cached in a db collection and updated incrementally
     over the time.
    """

    def __init__(self):
        self._parse_result_smooth_count_map = {
            0: 0.008502447849533839,
            1: 0.21471040149642595,
            2: 1.1129522477195453,
            3: 1.8991528085245906,
            4: 3.488358849588453,
            5: 3.9048094131380293
        }
        self._word_smooth_count_map = {
            0: 0.05562595701990601,
            1: 0.22317104256946213,
            2: 1.0726985250469303,
            3: 1.9161010077475567,
            4: 3.182159988876787,
            5: 4.016279163368528
        }

    def initialize(self):
        # do nothing
        pass

    def smooth_parse_result_occurrence_count(self, parse_result_occurrence_count):
        return self._parse_result_smooth_count_map.get(parse_result_occurrence_count, parse_result_occurrence_count)

    def smooth_word_occurrence_count(self, word_occurrence_count):
        return self._word_smooth_count_map.get(word_occurrence_count, word_occurrence_count)


class SimpleGoodTuringContextlessDistributionSmoother(ContextlessDistributionSmoother):
    AVG_PARSE_RESULTS_FOR_A_WORD = 6    # avg parse result count for a word
    AVG_WORDS_FOR_A_LEXEME = 50         # avg word count for a lexeme
    AVG_WORDS_FOR_A_STEM = 10           # avg word count for a stem

    def __init__(self, smoothing_threshold, unigram_collection):
        self._smoothing_threshold = smoothing_threshold
        self._unigram_collection = unigram_collection

        assert self._smoothing_threshold and self._smoothing_threshold > 1

    def initialize(self):
        logger.debug(
            "Initializing SimpleGoodTuringContextlessDistributionSmoother for K:{}, AVG_PARSE_RESULTS_FOR_A_WORD:{}, AVG_WORDS_FOR_A_LEXEME:{}".format(
                self._smoothing_threshold, self.AVG_PARSE_RESULTS_FOR_A_WORD, self.AVG_WORDS_FOR_A_LEXEME))

        distinct_parse_result_count = NgramTypeFrequencyFinder.find_distinct_parse_result_count(
            self._unigram_collection)
        distinct_word_count = NgramTypeFrequencyFinder.find_distinct_word_count(self._unigram_collection)

        distinct_lexeme_count = NgramTypeFrequencyFinder.find_distinct_count(self._unigram_collection, ['lemma_root'])
        distinct_stem_count = NgramTypeFrequencyFinder.find_distinct_count(self._unigram_collection, ['stem'])
        possible_word_count_estimate_from_lexemes = distinct_lexeme_count * self.AVG_WORDS_FOR_A_LEXEME
        possible_word_count_estimate_from_stems = distinct_stem_count * self.AVG_WORDS_FOR_A_STEM

        possible_word_count_estimate = possible_word_count_estimate_from_stems + possible_word_count_estimate_from_lexemes
        unseen_word_count = possible_word_count_estimate - distinct_word_count

        possible_parse_result_count_estimate = possible_word_count_estimate * self.AVG_PARSE_RESULTS_FOR_A_WORD
        unseen_parse_result_count = possible_parse_result_count_estimate - distinct_parse_result_count

        logger.debug("Found {} distinct parse results".format(distinct_parse_result_count))
        logger.debug("Found {} distinct words".format(distinct_word_count))
        logger.debug("Estimated possible parse result count : {}".format(possible_parse_result_count_estimate))
        logger.debug("Estimated unseen parse result count : {}".format(unseen_parse_result_count))

        logger.debug("Found {} distinct lexemes".format(distinct_lexeme_count))
        logger.debug("Estimated possible word count from lexemes: {}".format(possible_word_count_estimate_from_lexemes))
        logger.debug("Estimated possible word count from stems: {}".format(possible_word_count_estimate_from_stems))
        logger.debug("Estimated possible word count: {}".format(possible_word_count_estimate))
        logger.debug("Estimated unseen word count : {}".format(unseen_word_count))

        frequencies_of_parse_result_frequencies = {1: distinct_parse_result_count}
        frequencies_of_word_frequencies = {1: distinct_word_count}

        for i in range(2, self._smoothing_threshold + 2):
            frequencies_of_parse_result_frequencies[
            i] = NgramTypeFrequencyFinder.find_frequency_of_parse_result_frequency(self._unigram_collection, i)
            frequencies_of_word_frequencies[i] = NgramTypeFrequencyFinder.find_frequency_of_word_frequency(
                self._unigram_collection, i)

        logger.debug("Frequencies of parse result frequencies")
        logger.debug(pformat(frequencies_of_parse_result_frequencies))

        logger.debug("Frequencies of word frequencies")
        logger.debug(pformat(frequencies_of_word_frequencies))

        self._parse_result_count_smoother = SimpleGoodTuringSmoother(self._smoothing_threshold,
            frequencies_of_parse_result_frequencies,
            unseen_parse_result_count)

        self._word_count_smoother = SimpleGoodTuringSmoother(self._smoothing_threshold, frequencies_of_word_frequencies,
            unseen_word_count)

        self._parse_result_count_smoother.initialize()
        self._word_count_smoother.initialize()

    def smooth_parse_result_occurrence_count(self, parse_result_occurrence_count):
        if parse_result_occurrence_count > self._smoothing_threshold:
            return parse_result_occurrence_count

        return self._parse_result_count_smoother.smooth(parse_result_occurrence_count)


    def smooth_word_occurrence_count(self, word_occurrence_count):
        if word_occurrence_count > self._smoothing_threshold:
            return word_occurrence_count

        return self._word_count_smoother.smooth(word_occurrence_count)