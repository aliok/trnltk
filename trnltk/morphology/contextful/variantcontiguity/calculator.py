# coding=utf-8
import itertools
import logging
import numpy
from trnltk.morphology.contextful.variantcontiguity.hidden.database import DatabaseIndexBuilder
from trnltk.morphology.contextful.variantcontiguity.hidden import query
from trnltk.morphology.contextful.variantcontiguity.hidden.appender import ContextWordAppender, ParseResultSurfaceAppender, ParseResultStemAppender, ParseResultLemmaRootAppender
from trnltk.morphology.model import formatter
from trnltk.morphology.contextful.variantcontiguity.hidden.query import WordNGramQueryContainer, QueryExecutor, CachingQueryExecutor, QueryExecutionContextBuilder, CachingQueryExecutionContext, InMemoryCachingQueryExecutor

numpy.seterr(divide='ignore', invalid='ignore')

logger = logging.getLogger('contextstats')
query_logger = query.logger

_context_word_appender = ContextWordAppender()
_target_surface_syn_cat_appender = ParseResultSurfaceAppender(True, True)
_target_stem_syn_cat_appender = ParseResultStemAppender(True, True)
_target_lemma_root_syn_cat_appender = ParseResultLemmaRootAppender(True, True)

_context_surface_syn_cat_appender = ParseResultSurfaceAppender(True, False)
_context_stem_syn_cat_appender = ParseResultStemAppender(True, False)
_context_lemma_root_syn_cat_appender = ParseResultLemmaRootAppender(True, False)

class NonContextParsingLikelihoodCalculator(object):
    COEFFICIENT_SURFACE_GIVEN_CONTEXT = 0.55
    COEFFICIENT_STEM_GIVEN_CONTEXT = 0.3
    COEFFICIENT_LEXEME_GIVEN_CONTEXT = 0.15

    WEIGHT_LEADING_CONTEXT = 0.6
    WEIGHT_FOLLOWING_CONTEXT = 0.4

    def __init__(self, collection_map):
        self._collection_map = collection_map

    def build_indexes(self):
        index_builder = DatabaseIndexBuilder(self._collection_map)

        non_context_parsing_appender_matrix = [
            (_target_surface_syn_cat_appender, _context_word_appender),
            (_target_stem_syn_cat_appender, _context_word_appender),
            (_target_lemma_root_syn_cat_appender, _context_word_appender)
        ]

        index_builder.create_indexes([(_context_word_appender,)])
        index_builder.create_indexes(non_context_parsing_appender_matrix)

    def calculate_likelihood(self, target, leading_context, following_context):
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("Calculating likelihood of {1}, {0}, {2}".format(formatter.format_morpheme_container_for_simple_parseset(target), leading_context, following_context))

        likelihood =  self.calculate_oneway_likelihood(target, leading_context  , True ) * self.WEIGHT_LEADING_CONTEXT   + \
                      self.calculate_oneway_likelihood(target, following_context, False) * self.WEIGHT_FOLLOWING_CONTEXT

        logger.debug(" Calculated likelihood is {}".format(likelihood))

        return likelihood

    def calculate_oneway_likelihood(self, target, context, target_comes_after):
        """
        @type target: WordFormContainer
        @type context: list of WordFormContainer
        @type target_comes_after: bool
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
            return 0

        count_target_surface_given_context = self._count_target_form_given_context(target, context, target_comes_after, _target_surface_syn_cat_appender, _context_word_appender)
        count_target_stem_given_context = self._count_target_form_given_context(target, context, target_comes_after, _target_stem_syn_cat_appender, _context_word_appender)
        count_target_lexeme_given_context = self._count_target_form_given_context(target, context, target_comes_after, _target_lemma_root_syn_cat_appender, _context_word_appender)

        logger.debug("    Found {} context occurrences".format(count_given_context))
        logger.debug("    Found {} target surface with context occurrences".format(count_target_surface_given_context))
        logger.debug("    Found {} target stem with context occurrences".format(count_target_stem_given_context))
        logger.debug("    Found {} target lexeme with context occurrences".format(count_target_lexeme_given_context))

        likelihood = (
                         count_target_surface_given_context * self.COEFFICIENT_SURFACE_GIVEN_CONTEXT +
                         count_target_stem_given_context * self.COEFFICIENT_STEM_GIVEN_CONTEXT+
                         count_target_lexeme_given_context * self.COEFFICIENT_LEXEME_GIVEN_CONTEXT
                     ) / count_given_context

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
    def __init__(self, collection_map, query_cache_collection):
        super(CachingNonContextParsingLikelihoodCalculator, self).__init__(collection_map)
        self._query_cache_collection = query_cache_collection

    def _find_count_for_query(self, params, query_container, target_comes_after):
        query_execution_context = QueryExecutionContextBuilder(self._collection_map).create_context(query_container, target_comes_after)
        caching_query_execution_context = CachingQueryExecutionContext(query_execution_context.keys, query_execution_context.collection, self._query_cache_collection)
        return CachingQueryExecutor().query_execution_context(caching_query_execution_context).params(*params).count()


class ContextParsingLikelihoodCalculator(object):
    WEIGHT_LEADING_CONTEXT = 0.6
    WEIGHT_FOLLOWING_CONTEXT = 0.4

    COEFFICIENTS_TARGET_GIVEN_CONTEXT_FORM = numpy.array([0.55, 0.30, 0.15]).reshape(1,3)
    COEFFICIENTS_TARGET_FORM_GIVEN_CONTEXT = numpy.array([0.55, 0.30, 0.15]).reshape(1,3)

    def __init__(self, collection_map):
        self._collection_map = collection_map

    def build_indexes(self):
        index_builder = DatabaseIndexBuilder(self._collection_map)

        non_context_parsing_appender_matrix_row_0 = [
            (_target_surface_syn_cat_appender, _context_surface_syn_cat_appender),
            (_target_surface_syn_cat_appender, _context_stem_syn_cat_appender),
            (_target_surface_syn_cat_appender, _context_lemma_root_syn_cat_appender)
        ]

        non_context_parsing_appender_matrix_row_1 = [
            (_target_stem_syn_cat_appender, _context_surface_syn_cat_appender),
            (_target_stem_syn_cat_appender, _context_stem_syn_cat_appender),
            (_target_stem_syn_cat_appender, _context_lemma_root_syn_cat_appender)
        ]

        non_context_parsing_appender_matrix_row_2 = [
            (_target_lemma_root_syn_cat_appender, _context_surface_syn_cat_appender),
            (_target_lemma_root_syn_cat_appender, _context_stem_syn_cat_appender),
            (_target_lemma_root_syn_cat_appender, _context_lemma_root_syn_cat_appender)
        ]

        index_builder.create_indexes([(_context_word_appender,)])
        index_builder.create_indexes(non_context_parsing_appender_matrix_row_0)
        index_builder.create_indexes(non_context_parsing_appender_matrix_row_1)
        index_builder.create_indexes(non_context_parsing_appender_matrix_row_2)

    def calculate_likelihood(self, target, leading_context, following_context):
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(u"  Calculating twoway likelihood of \n\t{0}\n\t{1}\n\t{2}".format(
                [t[0].get_surface() if t else "<Unparsable>" for t in leading_context],
                formatter.format_morpheme_container_for_simple_parseset(target),
                [t[0].get_surface() if t else "<Unparsable>" for t in following_context]))

        likelihood = self.calculate_oneway_likelihood(target, leading_context  , True ) * self.WEIGHT_LEADING_CONTEXT   +\
                     self.calculate_oneway_likelihood(target, following_context, False) * self.WEIGHT_FOLLOWING_CONTEXT

        logger.debug("  Calculated likelihood is {}".format(likelihood))

        return likelihood

    def calculate_oneway_likelihood(self, target, context, target_comes_after):
        """
        @type target: WordFormContainer
        @type context: list of WordFormContainer
        @type target_comes_after: bool
        @rtype: float
        """
        assert target
        assert context

        target_morpheme_container_str = formatter.format_morpheme_container_for_simple_parseset(target)

        if logger.isEnabledFor(logging.DEBUG):
            if target_comes_after:
                logger.debug(u"  Calculating oneway likelihood of {1}, {0}".format(formatter.format_morpheme_container_for_simple_parseset(target), [t[0].get_surface() if t else "<Unparsable>" for t in context]))
            else:
                logger.debug(u"  Calculating oneway likelihood of {0}, {1}".format(formatter.format_morpheme_container_for_simple_parseset(target), [t[0].get_surface() if t else "<Unparsable>" for t in context]))

        cartesian_products_of_context_parse_results = self._get_cartesian_products_of_context_parse_results(context)
        logger.debug("  Going to check the usages with the following cartesian product of parse results: \n{}".format(
            [[formatter.format_morpheme_container_for_simple_parseset_without_suffixes(mc) for mc in product_item] for product_item in cartesian_products_of_context_parse_results]))

        if not cartesian_products_of_context_parse_results or not any(cartesian_products_of_context_parse_results):
            return 0.0

        likelihood = 0.0

        for context_parse_results in cartesian_products_of_context_parse_results:
            if logger.isEnabledFor(logging.DEBUG):
                context_parse_result_str_list = [formatter.format_morpheme_container_for_simple_parseset_without_suffixes(t) for t in context_parse_results]
                if target_comes_after:
                    logger.debug(u"   Calculating oneway likelihood of {1}, {0}".format(target_morpheme_container_str, context_parse_result_str_list))
                else:
                    logger.debug(u"   Calculating oneway likelihood of {0}, {1}".format(target_morpheme_container_str, context_parse_result_str_list))

            context_counts = self._get_context_form_count_matrix(context_parse_results)
            logger.debug("       Context form counts: \n{}".format(context_counts))

            appender_matrix = [
                [
                    (_target_surface_syn_cat_appender, _context_surface_syn_cat_appender),
                    (_target_surface_syn_cat_appender, _context_stem_syn_cat_appender),
                    (_target_surface_syn_cat_appender, _context_lemma_root_syn_cat_appender)
                ]
                ,
                [
                    (_target_stem_syn_cat_appender, _context_surface_syn_cat_appender),
                    (_target_stem_syn_cat_appender, _context_stem_syn_cat_appender),
                    (_target_stem_syn_cat_appender, _context_lemma_root_syn_cat_appender)
                ]
                ,
                [
                    (_target_lemma_root_syn_cat_appender, _context_surface_syn_cat_appender),
                    (_target_lemma_root_syn_cat_appender, _context_stem_syn_cat_appender),
                    (_target_lemma_root_syn_cat_appender, _context_lemma_root_syn_cat_appender)
                ]
            ]

            target_form_given_context_counts = numpy.zeros((3,3), dtype=float)

            for i, appender_matrix_row in enumerate(appender_matrix):
                for j, (target_appender, context_appender) in enumerate(appender_matrix_row):
                    target_form_given_count = self._count_target_form_given_context(target, context_parse_results, target_comes_after, target_appender, context_appender)
                    target_form_given_context_counts[i][j] = target_form_given_count

            logger.debug("       Target form counts given context forms: \n{}".format(target_form_given_context_counts))

            target_form_probabilities = target_form_given_context_counts / context_counts
            target_form_probabilities[numpy.isinf(target_form_probabilities)]=0.0
            target_form_probabilities[numpy.isnan(target_form_probabilities)]=0.0
            logger.debug("       Target form probabilities: \n{}".format(target_form_probabilities))

            target_form_probabilities = target_form_probabilities * self.COEFFICIENTS_TARGET_GIVEN_CONTEXT_FORM
            logger.debug("       Target form probabilities with context form weights: \n{}".format(target_form_probabilities))

            target_form_probabilities = numpy.dot(target_form_probabilities, numpy.ones((3,1), dtype=float))
            logger.debug("       Summed target form probabilities: \n{}".format(target_form_probabilities))

            weigh_summed_target_probability = numpy.dot(self.COEFFICIENTS_TARGET_FORM_GIVEN_CONTEXT, target_form_probabilities)
            assert numpy.shape(weigh_summed_target_probability) == (1,1)
            logger.debug("       Weigh-summed target probability: \n{}".format(weigh_summed_target_probability))

            item_likelihood = weigh_summed_target_probability[0][0]
            logger.debug("      Calculated oneway likelihood for target given context item is {}".format(item_likelihood))

            likelihood += item_likelihood

        logger.debug("  Calculated oneway likelihood is {}".format(likelihood))

        return likelihood

    def _get_context_form_count_matrix(self, context_parse_results):
        appender_matrix = [
            _context_surface_syn_cat_appender,
            _context_stem_syn_cat_appender,
            _context_lemma_root_syn_cat_appender
        ]

        context_form_counts = numpy.zeros(3, dtype=float)

        for i, context_appender in enumerate(appender_matrix):
            # target_comes_after doesn't matter, since there is no target
            context_form_count = self._count_target_form_given_context(None, context_parse_results, False, None, context_appender)
            context_form_counts[i] = context_form_count

        return context_form_counts

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

    def _get_cartesian_products_of_context_parse_results(self, context):
        # context is in form:
        # [ [parse_result_0_for_word_0, parse_result_1_for_word_0]
        #   [parse_result_0_for_word_1, parse_result_1_for_word_1] ]

        # if context is empty, or its items are empty lists
        if not context or not any(context):
            return []

        cartesian_products_of_context_parse_results = []

        for context_item_morpheme_containers in context:
            if not context_item_morpheme_containers:
                continue      #TODO: logging! one of the context words is unparsable. we'll just ignore it and use the remaining context information

            if not cartesian_products_of_context_parse_results:
                cartesian_products_of_context_parse_results = context_item_morpheme_containers[:]
            else:
                cartesian_products_of_context_parse_results = itertools.product(cartesian_products_of_context_parse_results, context_item_morpheme_containers)
                cartesian_products_of_context_parse_results = list(cartesian_products_of_context_parse_results)
                cartesian_products_of_context_parse_results = [(x[0] if isinstance(x[0], list) else [x[0]]) + [x[1]] for x in cartesian_products_of_context_parse_results]

        # cartesian product results in tuples, but if there is nothing to product we must return something iterable
        cartesian_product_list = list(cartesian_products_of_context_parse_results)
        if numpy.shape(cartesian_product_list) == (len(cartesian_product_list),):
            return [[context_parse_result] for context_parse_result in cartesian_product_list]

        return cartesian_product_list


class CachingContextParsingLikelihoodCalculator(ContextParsingLikelihoodCalculator):
    def __init__(self, collection_map, query_cache_collection):
        super(CachingContextParsingLikelihoodCalculator, self).__init__(collection_map)
        self._query_cache_collection = query_cache_collection

    def _find_count_for_query(self, params, query_container, target_comes_after):
        query_execution_context = QueryExecutionContextBuilder(self._collection_map).create_context(query_container, target_comes_after)
        caching_query_execution_context = CachingQueryExecutionContext(query_execution_context.keys, query_execution_context.collection, self._query_cache_collection)
        return CachingQueryExecutor().query_execution_context(caching_query_execution_context).params(*params).count()

class InMemoryCachingContextParsingLikelihoodCalculator(ContextParsingLikelihoodCalculator):
    def __init__(self, collection_map):
        super(InMemoryCachingContextParsingLikelihoodCalculator, self).__init__(collection_map)

    def _find_count_for_query(self, params, query_container, target_comes_after):
        query_execution_context = QueryExecutionContextBuilder(self._collection_map).create_context(query_container, target_comes_after)
        return InMemoryCachingQueryExecutor().query_execution_context(query_execution_context).params(*params).count()