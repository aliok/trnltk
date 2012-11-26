from __future__ import division
from trnltk.morphology.contextful.likelihoodmetrics.hidden.querykeyappender import _word_parse_result_appender, _word_surface_appender

class ContextlessDistributionCalculator(object):
    def __init__(self, database_index_builder, target_form_given_context_counter):
        self._database_index_builder = database_index_builder
        self._target_form_given_context_counter = target_form_given_context_counter

    def build_indexes(self):
        self._database_index_builder.create_indexes([(_word_parse_result_appender,)])
        self._database_index_builder.create_indexes([(_word_surface_appender,)])

    def calculate(self, target, calculation_context=None):
        """
        Without considering context and wordforms, calculates (how many times given parse result occurs) /
        (how many times given parse result's surface occurs).

        @type target: WordFormContainer
        @rtype calculation_context: dict
        @rtype: float
        """

        surface_occurrence_count = self._target_form_given_context_counter._count_target_form_given_context(None, [target.get_surface()], False, None,
            _word_surface_appender)

        if calculation_context is not None:
            calculation_context['surface_occurrence_count'] = surface_occurrence_count

            if not surface_occurrence_count:
                calculation_context['parse_result_occurrence_count'] = 0

        if not surface_occurrence_count:
            return 0.0
        else:
            parse_result_occurrence_count = self._target_form_given_context_counter._count_target_form_given_context(None, [target], False, None,
                _word_parse_result_appender)

            likelihood = parse_result_occurrence_count / surface_occurrence_count

            if calculation_context is not None:
                calculation_context['parse_result_occurrence_count'] = parse_result_occurrence_count
                calculation_context['likelihood'] = likelihood

            return likelihood
