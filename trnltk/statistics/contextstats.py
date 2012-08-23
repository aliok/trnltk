# coding=utf-8
import itertools
import logging
import numpy
from trnltk.morphology.model import formatter
from trnltk.statistics.query import WordNGramQueryContainer, QueryBuilder, QueryExecutor

numpy.seterr(divide='ignore', invalid='ignore')

logger = logging.getLogger('contextstats')

class QueryFormAppender(object):
    def append(self, container, query, params):
        raise NotImplementedError()

class ContextWordAppender(QueryFormAppender):
    def append(self, context_item, query, params):
        query.given_surface(False)
        params.append(context_item)

class ParseResultFormAppender(QueryFormAppender):
    def __init__(self, add_syntactic_category, is_target):
        self.add_syntactic_category = add_syntactic_category
        self.is_target = is_target

    def append(self, target, query, params):
        raise NotImplementedError()

class ParseResultSurfaceAppender(ParseResultFormAppender):
    def append(self, morpheme_container, query, params):
        if self.is_target:
            if self.add_syntactic_category:
                query.target_surface(True)
            else:
                query.target_surface(False)
        else:
            if self.add_syntactic_category:
                query.given_surface(True)
            else:
                query.given_surface(False)

        if self.add_syntactic_category:
            params.append(morpheme_container.get_surface())
            params.append(morpheme_container.get_surface_syntactic_category())
        else:
            params.append(morpheme_container.get_surface())

class ParseResultStemAppender(ParseResultFormAppender):
    def append(self, morpheme_container, query, params):
        if self.is_target:
            if self.add_syntactic_category:
                query.target_stem(True)
            else:
                query.target_stem(False)
        else:
            if self.add_syntactic_category:
                query.given_stem(True)
            else:
                query.given_stem(False)

        if self.add_syntactic_category:
            params.append(morpheme_container.get_stem())
            params.append(morpheme_container.get_stem_syntactic_category())
        else:
            params.append(morpheme_container.get_stem())

class ParseResultLemmaRootAppender(ParseResultFormAppender):
    def append(self, morpheme_container, query, params):
        if self.is_target:
            if self.add_syntactic_category:
                query.target_lemma_root(True)
            else:
                query.target_lemma_root(False)
        else:
            if self.add_syntactic_category:
                query.given_lemma_root(True)
            else:
                query.given_lemma_root(False)

        if self.add_syntactic_category:
            params.append(morpheme_container.get_lemma_root())
            params.append(morpheme_container.get_lemma_root_syntactic_category())
        else:
            params.append(morpheme_container.get_lemma_root())

context_word_appender = ContextWordAppender()
target_surface_syn_cat_appender = ParseResultSurfaceAppender(True, True)
target_stem_syn_cat_appender = ParseResultStemAppender(True, True)
target_lemma_root_syn_cat_appender = ParseResultLemmaRootAppender(True, True)

context_surface_syn_cat_appender = ParseResultSurfaceAppender(True, False)
context_stem_syn_cat_appender = ParseResultStemAppender(True, False)
context_lemma_root_syn_cat_appender = ParseResultLemmaRootAppender(True, False)

class NonContextParsingLikelihoodCalculator(object):
    COEFFICIENT_SURFACE_GIVEN_CONTEXT = 0.55
    COEFFICIENT_STEM_GIVEN_CONTEXT = 0.3
    COEFFICIENT_LEXEME_GIVEN_CONTEXT = 0.15

    WEIGHT_LEADING_CONTEXT = 0.6
    WEIGHT_FOLLOWING_CONTEXT = 0.4

    def __init__(self, collection_map):
        self._collection_map = collection_map

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

        count_given_context = self._count_target_form_given_context(target, context, False, None, context_word_appender)

        if not count_given_context:
            return 0

        count_target_surface_given_context = self._count_target_form_given_context(target, context, target_comes_after, target_surface_syn_cat_appender, context_word_appender)
        count_target_stem_given_context = self._count_target_form_given_context(target, context, target_comes_after, target_stem_syn_cat_appender, context_word_appender)
        count_target_lexeme_given_context = self._count_target_form_given_context(target, context, target_comes_after, target_lemma_root_syn_cat_appender, context_word_appender)

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
        query_execution_context = QueryBuilder(self._collection_map).build_query(query_container, target_comes_after)
        return QueryExecutor().query_execution_context(query_execution_context).params(*params).count()



class ContextParsingLikelihoodCalculator(object):
    WEIGHT_LEADING_CONTEXT = 0.6
    WEIGHT_FOLLOWING_CONTEXT = 0.4

    COEFFICIENTS_TARGET_GIVEN_CONTEXT_FORM = numpy.array([0.55, 0.30, 0.15]).reshape(1,3)
    COEFFICIENTS_TARGET_FORM_GIVEN_CONTEXT = numpy.array([0.55, 0.30, 0.15]).reshape(1,3)

    def __init__(self, collection_map):
        self._collection_map = collection_map

    def calculate_likelihood(self, target, leading_context, following_context):
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
                logger.debug("  Calculating oneway likelihood of {1}, {0}".format(formatter.format_morpheme_container_for_simple_parseset(target), [t[0] for t in context]))
            else:
                logger.debug("  Calculating oneway likelihood of {0}, {1}".format(formatter.format_morpheme_container_for_simple_parseset(target), [t[0] for t in context]))

        cartesian_products_of_context_parse_results = []
        if len(context)==1:
            if context[0] is None:
                return 0.0
            else:
                cartesian_products_of_context_parse_results = [[context_parse_result] for context_parse_result in context[0][1]]
        else:
            for context_word in context:
                context_item_morpheme_containers = context_word[1]
                if not context_item_morpheme_containers:
                    break      # TODO: logging! one of the context words is unparsable

                if not cartesian_products_of_context_parse_results:
                    cartesian_products_of_context_parse_results = context_item_morpheme_containers[:]
                else:
                    cartesian_products_of_context_parse_results = itertools.product(cartesian_products_of_context_parse_results, context_item_morpheme_containers)


        likelihood = 0.0

        for context_parse_results in cartesian_products_of_context_parse_results:
            if logger.isEnabledFor(logging.DEBUG):
                context_parse_result_str_list = [formatter.format_morpheme_container_for_simple_parseset(t) for t in context_parse_results]
                if target_comes_after:
                    logger.debug("   Calculating oneway likelihood of {1}, {0}".format(target_morpheme_container_str, context_parse_result_str_list))
                else:
                    logger.debug("   Calculating oneway likelihood of {0}, {1}".format(target_morpheme_container_str, context_parse_result_str_list))

            context_counts = self._get_context_form_count_matrix(context_parse_results)
            logger.debug("       Context form counts: \n{}".format(context_counts))

            appender_matrix = [
                [
                    (target_surface_syn_cat_appender, context_surface_syn_cat_appender),
                    (target_surface_syn_cat_appender, context_stem_syn_cat_appender),
                    (target_surface_syn_cat_appender, context_lemma_root_syn_cat_appender)
                ]
                ,
                [
                    (target_stem_syn_cat_appender, context_surface_syn_cat_appender),
                    (target_stem_syn_cat_appender, context_stem_syn_cat_appender),
                    (target_stem_syn_cat_appender, context_lemma_root_syn_cat_appender)
                ]
                ,
                [
                    (target_lemma_root_syn_cat_appender, context_surface_syn_cat_appender),
                    (target_lemma_root_syn_cat_appender, context_stem_syn_cat_appender),
                    (target_lemma_root_syn_cat_appender, context_lemma_root_syn_cat_appender)
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
            context_surface_syn_cat_appender,
            context_stem_syn_cat_appender,
            context_lemma_root_syn_cat_appender
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
        query_execution_context = QueryBuilder(self._collection_map).build_query(query_container, target_comes_after)
        return QueryExecutor().query_execution_context(query_execution_context).params(*params).count()