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
import numpy
from trnltk.morphology.contextful.likelihoodmetrics.hidden.querykeyappender import _target_surface_syn_cat_appender, _context_word_appender, _target_stem_syn_cat_appender, _target_lemma_root_syn_cat_appender
from trnltk.morphology.contextful.likelihoodmetrics.hidden.database import DatabaseIndexBuilder
from trnltk.morphology.contextful.likelihoodmetrics.hidden.query import WordNGramQueryContainer, QueryExecutionContextBuilder, QueryExecutor, CachingQueryExecutionContext, CachingQueryExecutor
from trnltk.morphology.contextful.likelihoodmetrics.hidden import query
from trnltk.morphology.model import formatter

numpy.seterr(divide='ignore', invalid='ignore')

logger = logging.getLogger('noncontextParsingCollocationLikelihoodCalculatorLogger')
query_logger = query.logger

class NonContextParsingLikelihoodCalculator(object):
    """
    @deprecated Not really used -yet- and not really maintained
    """

    COEFFICIENTS_TARGET_GIVEN_CONTEXT_FORM = numpy.array([0.55, 0.30, 0.15]).reshape(1, 3)
    COEFFICIENTS_TARGET_FORM_GIVEN_CONTEXT = numpy.array([0.60, 0.30, 0.10]).reshape(1, 3)

    WEIGHT_LEADING_CONTEXT = 0.6
    WEIGHT_FOLLOWING_CONTEXT = 0.4

    APPENDER_MATRIX = [
        (_target_surface_syn_cat_appender, _context_word_appender),
        (_target_stem_syn_cat_appender, _context_word_appender),
        (_target_lemma_root_syn_cat_appender, _context_word_appender)
    ]

    def __init__(self, collection_map):
        self._collection_map = collection_map

    def build_indexes(self):
        index_builder = DatabaseIndexBuilder(self._collection_map)

        index_builder.create_indexes([(_context_word_appender,)])
        index_builder.create_indexes(self.APPENDER_MATRIX)

    def calculate_likelihood(self, target, leading_context, following_context, calculation_context=None):
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("Calculating likelihood of {1}, {0}, {2}".format(formatter.format_morpheme_container_for_simple_parseset(target), leading_context,
                following_context))

        calculation_context_leading = {} if calculation_context is not None else None
        calculation_context_following = {} if calculation_context is not None else None

        likelihood = self.calculate_oneway_likelihood(target, leading_context, True, calculation_context_leading) * self.WEIGHT_LEADING_CONTEXT +\
                     self.calculate_oneway_likelihood(target, following_context, False, calculation_context_following) * self.WEIGHT_FOLLOWING_CONTEXT

        if calculation_context is not None:
            calculation_context['leading'] = calculation_context_leading
            calculation_context['following'] = calculation_context_following
            calculation_context['weight_leading_context'] = self.WEIGHT_LEADING_CONTEXT
            calculation_context['weight_following_context'] = self.WEIGHT_FOLLOWING_CONTEXT

        logger.debug(" Calculated likelihood is {}".format(likelihood))

        return likelihood

    def calculate_oneway_likelihood(self, target, context, target_comes_after, calculation_context=None):
        """
        @type target: WordFormContainer
        @type context: list of WordFormContainer
        @type target_comes_after: bool
        @type calculation_context : dict or None
        @rtype: float
        """
        assert target
        assert context

        if logger.isEnabledFor(logging.DEBUG):
            if target_comes_after:
                logger.debug("  Calculating oneway likelihood of {1}, {0}".format(formatter.format_morpheme_container_for_simple_parseset(target), context))
            else:
                logger.debug("  Calculating oneway likelihood of {0}, {1}".format(formatter.format_morpheme_container_for_simple_parseset(target), context))

        count_given_context = self._count_target_form_given_context(target, context, False, None, _context_word_appender)

        if not count_given_context:
            return 0.0

        if calculation_context is not None:
            for i, context_item in enumerate(context):
                calculation_context[i] = {
                    'surface': context_item
                }

        target_form_given_context_counts = numpy.zeros((3, 1), dtype=float)

        for i, appender_matrix_row in enumerate(self.APPENDER_MATRIX):
            target_appender, context_appender = appender_matrix_row
            target_form_given_count = self._count_target_form_given_context(target, context, target_comes_after, target_appender, context_appender)
            target_form_given_context_counts[i] = target_form_given_count

        logger.debug("    Target form counts given context forms: \n{}".format(target_form_given_context_counts))
        logger.debug("    Found {} context occurrences".format(count_given_context))

        target_form_probabilities = target_form_given_context_counts / count_given_context
        target_form_probabilities[numpy.isinf(target_form_probabilities)] = 0.0
        target_form_probabilities[numpy.isnan(target_form_probabilities)] = 0.0

        if calculation_context is not None:
            calculation_context['target_form_probabilities'] = target_form_probabilities
        logger.debug("    Target form probabilities: \n{}".format(target_form_probabilities))

        target_form_probabilities = target_form_probabilities * self.COEFFICIENTS_TARGET_GIVEN_CONTEXT_FORM
        if calculation_context is not None:
            calculation_context['coefficients_target_given_context_form'] = self.COEFFICIENTS_TARGET_GIVEN_CONTEXT_FORM
            calculation_context['target_form_probabilities_with_context_form_weights'] = target_form_probabilities
        logger.debug("    Target form probabilities with context form weights: \n{}".format(target_form_probabilities))

        target_form_probabilities = numpy.dot(target_form_probabilities, numpy.ones((3, 1), dtype=float))
        if calculation_context is not None:
            calculation_context['summed_target_form_probabilities'] = target_form_probabilities
        logger.debug("    Summed target form probabilities: \n{}".format(target_form_probabilities))

        weight_summed_target_probability = numpy.dot(self.COEFFICIENTS_TARGET_FORM_GIVEN_CONTEXT, target_form_probabilities)
        assert numpy.shape(weight_summed_target_probability) == (1, 1)
        if calculation_context is not None:
            calculation_context['coefficients_target_form_given_context'] = self.COEFFICIENTS_TARGET_FORM_GIVEN_CONTEXT
            calculation_context['weight_summed_target_probability'] = weight_summed_target_probability
        logger.debug("    Weight-summed target probability: \n{}".format(weight_summed_target_probability))

        likelihood = weight_summed_target_probability[0][0]

        logger.debug("  Calculated oneway likelihood is {}".format(likelihood))

        return likelihood

    def _count_target_form_given_context(self, target, context, target_comes_after, target_appender, context_appender):
        query_container = WordNGramQueryContainer(len(context) + 1) if target_appender else WordNGramQueryContainer(len(context))
        params = []

        if target_appender:
            target_appender.append(target, query_container, params)
        for context_item in context:
            context_appender.append(context_item, query_container, params)

        return self._find_count_for_query(params, query_container, target_comes_after)

    def _find_count_for_query(self, params, query_container, target_comes_after):
        query_execution_context = QueryExecutionContextBuilder(self._collection_map).create_context(query_container, target_comes_after)
        return QueryExecutor().query_execution_context(query_execution_context).params(*params).count()


class CachingNonContextParsingLikelihoodCalculator(NonContextParsingLikelihoodCalculator):
    """
    @deprecated Not really used -yet- and not really maintained
    """

    def __init__(self, collection_map, query_cache_collection):
        super(CachingNonContextParsingLikelihoodCalculator, self).__init__(collection_map)
        self._query_cache_collection = query_cache_collection

    def _find_count_for_query(self, params, query_container, target_comes_after):
        query_execution_context = QueryExecutionContextBuilder(self._collection_map).create_context(query_container, target_comes_after)
        caching_query_execution_context = CachingQueryExecutionContext(query_execution_context.keys, query_execution_context.collection,
            self._query_cache_collection)
        return CachingQueryExecutor().query_execution_context(caching_query_execution_context).params(*params).count()