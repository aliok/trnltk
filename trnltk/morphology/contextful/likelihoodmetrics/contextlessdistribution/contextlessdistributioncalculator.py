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
from trnltk.morphology.contextful.likelihoodmetrics.hidden.querykeyappender import _word_parse_result_appender, _word_surface_appender

class ContextlessDistributionCalculator(object):
    def __init__(self, database_index_builder, target_form_given_context_counter, smoother):
        """
        @type database_index_builder: DatabaseIndexBuilder
        @type target_form_given_context_counter: TargetFormGivenContextCounter
        @type smoother: ContextlessDistributionSmoother
        """
        self._database_index_builder = database_index_builder
        self._target_form_given_context_counter = target_form_given_context_counter
        self._smoother = smoother

    def build_indexes(self):
        self._database_index_builder.create_indexes([(_word_parse_result_appender,)])
        self._database_index_builder.create_indexes([(_word_surface_appender,)])

    def calculate(self, target, calculation_context=None):
        """
        Without considering context and wordforms, calculates (how many times given parse result occurs) /
        (how many times given parse result's surface occurs).

        Values are smoothed, so that we have an estimation for the parse results and
        surfaces that doesn't exist in the database

        @type target: WordFormContainer
        @rtype calculation_context: dict
        @rtype: float
        """

        # since we ignore the syntactic category, it is better to call "surface without syn cat" "word"
        word_occurrence_count = self._target_form_given_context_counter._count_target_form_given_context(None, [target.get_surface()], False, None,
            _word_surface_appender)
        parse_result_occurrence_count = None

        if not word_occurrence_count:
            parse_result_occurrence_count = 0
        else:
            parse_result_occurrence_count = self._target_form_given_context_counter._count_target_form_given_context(None, [target], False, None,
                _word_parse_result_appender)

        if calculation_context is not None:
            calculation_context['word_occurrence_count'] = word_occurrence_count
            calculation_context['parse_result_occurrence_count'] = parse_result_occurrence_count

        smooth_parse_result_occurrence_count = self._smoother.smooth_parse_result_occurrence_count(parse_result_occurrence_count)
        smooth_word_occurrence_count = self._smoother.smooth_word_occurrence_count(word_occurrence_count)

        smooth_likelihood = smooth_parse_result_occurrence_count / smooth_word_occurrence_count

        if calculation_context is not None:
            calculation_context['smooth_word_occurrence_count'] = smooth_word_occurrence_count
            calculation_context['smooth_parse_result_occurrence_count'] = smooth_parse_result_occurrence_count
            calculation_context['smooth_likelihood'] = smooth_likelihood

        return smooth_likelihood
