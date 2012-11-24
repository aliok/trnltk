from trnltk.morphology.contextful.likelihoodmetrics.hidden.database import DatabaseIndexBuilder
from trnltk.morphology.contextful.likelihoodmetrics.hidden.querykeyappender import _word_parse_result_appender, _word_surface_appender


class ContextlessDistributionCalculator(object):
    def __init__(self, unigram_collection):
        self._unigram_collection = unigram_collection

    def build_indexes(self):
        index_builder = DatabaseIndexBuilder({1: self._unigram_collection})

        index_builder.create_indexes([(_word_parse_result_appender,)])
        index_builder.create_indexes([(_word_surface_appender,)])

    def calculate(self, target):
        """
        Without considering context and wordforms, calculates (how many times given parse result occurs) /
        (how many times given parse result's surface occurs).

        @type target: WordFormContainer
        """
        pass
