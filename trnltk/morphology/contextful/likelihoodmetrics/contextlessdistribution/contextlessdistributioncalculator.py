from trnltk.morphology.contextful.likelihoodmetrics.hidden.querykeyappender import _word_parse_result_appender, _word_surface_appender


class ContextlessDistributionCalculator(object):
    def __init__(self, database_index_builder, target_form_given_context_counter):
        self._database_index_builder = database_index_builder
        self._target_form_given_context_counter = target_form_given_context_counter

    def build_indexes(self):
        self._database_index_builder.create_indexes([(_word_parse_result_appender,)])
        self._database_index_builder.create_indexes([(_word_surface_appender,)])

    def calculate(self, target):
        """
        Without considering context and wordforms, calculates (how many times given parse result occurs) /
        (how many times given parse result's surface occurs).

        @type target: WordFormContainer
        """
        surface_occurrence_count = self._target_form_given_context_counter._count_target_form_given_context(None, [target.get_surface()], False, None,
            _word_surface_appender)
        if not surface_occurrence_count:
            return 0.0
        else:
            parse_result_occurrence_count = self._target_form_given_context_counter._count_target_form_given_context(None, [target], False, None,
                _word_parse_result_appender)
            return parse_result_occurrence_count / surface_occurrence_count
