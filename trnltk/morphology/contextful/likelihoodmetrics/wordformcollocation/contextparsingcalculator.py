# coding=utf-8
import itertools
import logging
import numpy
from trnltk.morphology.contextful.likelihoodmetrics.wordformcollocation.hidden.database import DatabaseIndexBuilder
from trnltk.morphology.contextful.likelihoodmetrics.wordformcollocation.hidden import query
from trnltk.morphology.contextful.likelihoodmetrics.wordformcollocation.hidden.appender import _context_word_appender, _target_surface_syn_cat_appender, _target_stem_syn_cat_appender, _target_lemma_root_syn_cat_appender, _context_surface_syn_cat_appender, _context_stem_syn_cat_appender, _context_lemma_root_syn_cat_appender
from trnltk.morphology.model import formatter
from trnltk.morphology.contextful.likelihoodmetrics.wordformcollocation.hidden.query import WordNGramQueryContainer, QueryExecutor, CachingQueryExecutor, QueryExecutionContextBuilder, CachingQueryExecutionContext, InMemoryCachingQueryExecutor

numpy.seterr(divide='ignore', invalid='ignore')

logger = logging.getLogger('contextstats')
query_logger = query.logger


class ContextParsingLikelihoodCalculator(object):
    WEIGHT_LEADING_CONTEXT = 0.6
    WEIGHT_FOLLOWING_CONTEXT = 0.4

    COEFFICIENTS_TARGET_GIVEN_CONTEXT_FORM = numpy.array([0.55, 0.30, 0.15]).reshape(1, 3)
    COEFFICIENTS_TARGET_FORM_GIVEN_CONTEXT = numpy.array([0.60, 0.30, 0.10]).reshape(1, 3)

    APPENDER_MATRIX = [
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

    CONTEXT_APPENDER_VECTOR = [
        _context_surface_syn_cat_appender,
        _context_stem_syn_cat_appender,
        _context_lemma_root_syn_cat_appender
    ]

    def __init__(self, collection_map, ngram_frequency_smoother):
        self._collection_map = collection_map
        self._ngram_frequency_smoother = ngram_frequency_smoother

    def build_indexes(self):
        index_builder = DatabaseIndexBuilder(self._collection_map)

        index_builder.create_indexes([(_context_word_appender,)])
        for appender_matrix_row in self.APPENDER_MATRIX:
            index_builder.create_indexes(appender_matrix_row)

    def calculate_likelihood(self, target, leading_context, following_context, calculation_context=None):
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(u"  Calculating twoway likelihood of \n\t{0}\n\t{1}\n\t{2}".format(
                [t[0].get_surface() if t else "<Unparsable>" for t in leading_context],
                formatter.format_morpheme_container_for_simple_parseset(target),
                [t[0].get_surface() if t else "<Unparsable>" for t in following_context]))

        assert leading_context or following_context

        calculation_context_leading = {} if calculation_context is not None else None
        calculation_context_following = {} if calculation_context is not None else None

        if calculation_context is not None:
            calculation_context['leading_context_length'] = len(leading_context)
            calculation_context['following_context_length'] = len(following_context)

        likelihood = None
        if leading_context and following_context:
            likelihood = self.calculate_oneway_likelihood(target, leading_context, True, calculation_context_leading) * self.WEIGHT_LEADING_CONTEXT +\
                         self.calculate_oneway_likelihood(target, following_context, False, calculation_context_following) * self.WEIGHT_FOLLOWING_CONTEXT
        elif leading_context:
            likelihood = self.calculate_oneway_likelihood(target, leading_context, True, calculation_context_leading) * self.WEIGHT_LEADING_CONTEXT
        elif following_context:
            likelihood = self.calculate_oneway_likelihood(target, following_context, False, calculation_context_following) * self.WEIGHT_FOLLOWING_CONTEXT

        if calculation_context is not None:
            calculation_context['leading'] = calculation_context_leading
            calculation_context['following'] = calculation_context_following
            calculation_context['weight_leading_context'] = self.WEIGHT_LEADING_CONTEXT
            calculation_context['weight_following_context'] = self.WEIGHT_FOLLOWING_CONTEXT

        if calculation_context is not None:
            calculation_context['sum_likelihood'] = likelihood

        logger.debug("  Calculated likelihood is {}".format(likelihood))

        return likelihood

    def calculate_oneway_likelihood(self, target, context, target_comes_after, calculation_context=None):
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
                logger.debug(u"  Calculating oneway likelihood of {1}, {0}".format(formatter.format_morpheme_container_for_simple_parseset(target),
                    [t[0].get_surface() if t else "<Unparsable>" for t in context]))
            else:
                logger.debug(u"  Calculating oneway likelihood of {0}, {1}".format(formatter.format_morpheme_container_for_simple_parseset(target),
                    [t[0].get_surface() if t else "<Unparsable>" for t in context]))

        cartesian_products_of_context_parse_results = self._get_cartesian_products_of_context_parse_results(context)
        logger.debug("  Going to check the usages with the following cartesian product of parse results: \n{}".format(
            [[formatter.format_morpheme_container_for_simple_parseset_without_suffixes(mc) for mc in product_item] for product_item in
                                                                                                                   cartesian_products_of_context_parse_results]))

        if not cartesian_products_of_context_parse_results or not any(cartesian_products_of_context_parse_results):
            return 0.0

        likelihood = 0.0

        if calculation_context is not None:
            calculation_context['possibilities'] = {}

        for index, context_parse_results in enumerate(cartesian_products_of_context_parse_results):
            word_calc_context = None
            if calculation_context is not None:
                word_calc_context = calculation_context['possibilities'][index] = {}

            if logger.isEnabledFor(logging.DEBUG):
                context_parse_result_str_list = [formatter.format_morpheme_container_for_simple_parseset_without_suffixes(t) for t in context_parse_results]
                if target_comes_after:
                    logger.debug(u"   Calculating oneway likelihood of {1}, {0}".format(target_morpheme_container_str, context_parse_result_str_list))
                else:
                    logger.debug(u"   Calculating oneway likelihood of {0}, {1}".format(target_morpheme_container_str, context_parse_result_str_list))

            context_counts = self._get_context_form_count_matrix(context_parse_results)
            logger.debug("       Context form counts: \n{}".format(context_counts))

            smoothed_context_counts = self._smooth_context_cooccurrence_counts(context_counts, context_parse_results)
            if calculation_context is not None:
                word_calc_context['smoothed_context_counts'] = smoothed_context_counts
            logger.debug("       Smoothed context form counts: \n{}".format(smoothed_context_counts))

            if calculation_context is not None:
                word_calc_context['context_words'] = {}
                for i, context_item in enumerate(context_parse_results):
                    word_calc_context['context_words'][i] = {
                        'surface': context_item.get_surface_with_syntactic_categories(),
                        'stem': context_item.get_stem_with_syntactic_categories(),
                        'lexeme': context_item.get_lemma_root_with_syntactic_categories()
                    }

            target_form_given_context_counts = numpy.zeros((3, 3), dtype=float)

            for i, appender_matrix_row in enumerate(self.APPENDER_MATRIX):
                for j, (target_appender, context_appender) in enumerate(appender_matrix_row):
                    target_form_given_count = self._count_target_form_given_context(target, context_parse_results, target_comes_after, target_appender, context_appender)
                    target_form_given_context_counts[i][j] = target_form_given_count

            logger.debug("       Target form counts given context forms: \n{}".format(target_form_given_context_counts))

            if calculation_context is not None:
                word_calc_context['target_form_counts'] = target_form_given_context_counts
            logger.debug("       Target form counts: \n{}".format(target_form_given_context_counts))

            smoothed_target_form_given_context_counts = self._smooth_target_context_cooccurrence_counts(target_form_given_context_counts, target, context_parse_results, target_comes_after)

            if calculation_context is not None:
                word_calc_context['smoothed_target_form_counts'] = smoothed_target_form_given_context_counts
            logger.debug("       Smoothed target form counts: \n{}".format(smoothed_target_form_given_context_counts))

            target_form_probabilities = smoothed_target_form_given_context_counts / smoothed_context_counts
            target_form_probabilities[numpy.isinf(target_form_probabilities)] = 0.0
            target_form_probabilities[numpy.isnan(target_form_probabilities)] = 0.0

            if calculation_context is not None:
                word_calc_context['target_form_probabilities'] = target_form_probabilities
            logger.debug("       Target form probabilities: \n{}".format(target_form_probabilities))

            target_form_probabilities = target_form_probabilities * self.COEFFICIENTS_TARGET_GIVEN_CONTEXT_FORM
            if calculation_context is not None:
                word_calc_context['coefficients_target_given_context_form'] = self.COEFFICIENTS_TARGET_GIVEN_CONTEXT_FORM
                word_calc_context['target_form_probabilities_with_context_form_weights'] = target_form_probabilities
            logger.debug("       Target form probabilities with context form weights: \n{}".format(target_form_probabilities))

            target_form_probabilities = numpy.dot(target_form_probabilities, numpy.ones((3, 1), dtype=float))
            if calculation_context is not None:
                word_calc_context['summed_target_form_probabilities'] = target_form_probabilities
            logger.debug("       Summed target form probabilities: \n{}".format(target_form_probabilities))

            weight_summed_target_probability = numpy.dot(self.COEFFICIENTS_TARGET_FORM_GIVEN_CONTEXT, target_form_probabilities)
            assert numpy.shape(weight_summed_target_probability) == (1, 1)
            if calculation_context is not None:
                word_calc_context['coefficients_target_form_given_context'] = self.COEFFICIENTS_TARGET_FORM_GIVEN_CONTEXT
                word_calc_context['weight_summed_target_probability'] = weight_summed_target_probability
            logger.debug("       Weight-summed target probability: \n{}".format(weight_summed_target_probability))

            item_likelihood = weight_summed_target_probability[0][0]

            logger.debug("      Calculated oneway likelihood for target given context item is {}".format(item_likelihood))

            likelihood += item_likelihood

        if calculation_context is not None:
            calculation_context['sum_likelihood'] = likelihood
        logger.debug("  Calculated oneway likelihood is {}".format(likelihood))

        return likelihood

    def _get_context_form_count_matrix(self, context_parse_results):
        context_form_counts = numpy.zeros(3, dtype=float)

        for i, context_appender in enumerate(self.CONTEXT_APPENDER_VECTOR):
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
                cartesian_products_of_context_parse_results = [(x[0] if isinstance(x[0], list) else [x[0]]) + [x[1]] for x in
                                                               cartesian_products_of_context_parse_results]

        # cartesian product results in tuples, but if there is nothing to product we must return something iterable
        cartesian_product_list = list(cartesian_products_of_context_parse_results)
        if numpy.shape(cartesian_product_list) == (len(cartesian_product_list),):
            return [[context_parse_result] for context_parse_result in cartesian_product_list]

        return cartesian_product_list

    def _smooth_context_cooccurrence_counts(self, context_counts, context_parse_results):
        smoothed_counts = numpy.zeros(3, dtype=float)

        for i, count in enumerate(context_counts):
            context_appender = self.CONTEXT_APPENDER_VECTOR[i]
            context_ngram_type_item = context_appender.get_ngram_type_item()

            context_len = len(context_parse_results)

            ngram_type = context_len * [context_ngram_type_item]

            smoothed_counts[i] = self._ngram_frequency_smoother.smooth(context_counts[i], ngram_type)

        return smoothed_counts

    def _smooth_target_context_cooccurrence_counts(self, target_form_given_context_counts, target, context_parse_results, target_comes_after):
        smoothed_counts = numpy.zeros((3, 3), dtype=float)

        for i, row in enumerate(target_form_given_context_counts):
            for j, count in enumerate(row):
                target_appender, context_appender = self.APPENDER_MATRIX[i][j]
                target_ngram_type_item = target_appender.get_ngram_type_item()
                context_ngram_type_item = context_appender.get_ngram_type_item()

                context_len = len(context_parse_results)

                ngram_type = [target_ngram_type_item] + context_len * [context_ngram_type_item] if target_comes_after else context_len * [context_ngram_type_item] + [target_ngram_type_item]

                smoothed_counts[i][j] = self._ngram_frequency_smoother.smooth(target_form_given_context_counts[i][j], ngram_type)

        return smoothed_counts


class CachingContextParsingLikelihoodCalculator(ContextParsingLikelihoodCalculator):
    def __init__(self, collection_map, query_cache_collection, ngram_frequency_smoother):
        super(CachingContextParsingLikelihoodCalculator, self).__init__(collection_map, ngram_frequency_smoother)
        self._query_cache_collection = query_cache_collection

    def _find_count_for_query(self, params, query_container, target_comes_after):
        query_execution_context = QueryExecutionContextBuilder(self._collection_map).create_context(query_container, target_comes_after)
        caching_query_execution_context = CachingQueryExecutionContext(query_execution_context.keys, query_execution_context.collection,
            self._query_cache_collection)
        return CachingQueryExecutor().query_execution_context(caching_query_execution_context).params(*params).count()


class InMemoryCachingContextParsingLikelihoodCalculator(ContextParsingLikelihoodCalculator):
    def __init__(self, collection_map, ngram_frequency_smoother):
        super(InMemoryCachingContextParsingLikelihoodCalculator, self).__init__(collection_map, ngram_frequency_smoother)

    def _find_count_for_query(self, params, query_container, target_comes_after):
        query_execution_context = QueryExecutionContextBuilder(self._collection_map).create_context(query_container, target_comes_after)
        return InMemoryCachingQueryExecutor().query_execution_context(query_execution_context).params(*params).count()