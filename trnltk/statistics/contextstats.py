# coding=utf-8
import itertools
import logging
from trnltk.morphology.model import formatter
from trnltk.statistics.query import WordNGramQueryContainer, QueryBuilder, QueryExecutor

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
    COEFFICIENT_SURFACE_GIVEN_CONTEXT = 0.55
    COEFFICIENT_STEM_GIVEN_CONTEXT = 0.3
    COEFFICIENT_LEXEME_GIVEN_CONTEXT = 0.15

    WEIGHT_LEADING_CONTEXT = 0.6
    WEIGHT_FOLLOWING_CONTEXT = 0.4

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
                if target_comes_after:
                    logger.debug("   Calculating oneway likelihood of {1}, {0}".format(formatter.format_morpheme_container_for_simple_parseset(target), [formatter.format_morpheme_container_for_simple_parseset(t) for t in context_parse_results]))
                else:
                    logger.debug("   Calculating oneway likelihood of {0}, {1}".format(formatter.format_morpheme_container_for_simple_parseset(target), [formatter.format_morpheme_container_for_simple_parseset(t) for t in context_parse_results]))

            count_context_surfaces = self._count_given_context_surfaces(context_parse_results)
            count_context_stems = self._count_given_context_stems(context_parse_results)
            count_context_lexemes = self._count_given_context_lexemes(context_parse_results)

            p_target_surface_given_context = self._calculate_probability_target_surface_given_context(target, context_parse_results, target_comes_after, count_context_surfaces, count_context_stems, count_context_lexemes)
            p_target_stem_given_context = self._calculate_probability_target_stem_given_context(target, context_parse_results, target_comes_after, count_context_surfaces, count_context_stems, count_context_lexemes)
            p_target_lexeme_given_context = self._calculate_probability_target_lexeme_given_context(target, context_parse_results, target_comes_after, count_context_surfaces, count_context_stems, count_context_lexemes)

            logger.debug("      Found surface probability {}".format(p_target_surface_given_context))
            logger.debug("      Found stem probability {}".format(p_target_stem_given_context))
            logger.debug("      Found lexeme probability {}".format(p_target_lexeme_given_context))

            item_likelihood  =  p_target_surface_given_context * self.COEFFICIENT_SURFACE_GIVEN_CONTEXT +\
                                p_target_stem_given_context    * self.COEFFICIENT_STEM_GIVEN_CONTEXT    +\
                                p_target_lexeme_given_context  * self.COEFFICIENT_LEXEME_GIVEN_CONTEXT

            logger.debug("      Calculated oneway likelihood is {}".format(item_likelihood))

            likelihood += item_likelihood

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

    def _calculate_probability_of_case(self, target, context_parse_results, target_comes_after, target_appender, context_appender, given_context_count):
        if not given_context_count:
            return 0.0

        count_target_given_context = self._count_target_form_given_context(target, context_parse_results, target_comes_after, target_appender, context_appender)

        return count_target_given_context / given_context_count

    ################## context form counts
    def _count_given_context_surfaces(self, context_parse_results):
        # target_comes_after doesn't matter, since there is no target
        return self._count_target_form_given_context(None, context_parse_results, False, None, context_surface_syn_cat_appender)

    def _count_given_context_stems(self, context_parse_results):
        # target_comes_after doesn't matter, since there is no target
        return self._count_target_form_given_context(None, context_parse_results, False, None, context_stem_syn_cat_appender)

    def _count_given_context_lexemes(self, context_parse_results):
        # target_comes_after doesn't matter, since there is no target
        return self._count_target_form_given_context(None, context_parse_results, False, None, context_lemma_root_syn_cat_appender)

    ################## 1. target surface given context
    def _calculate_probability_target_surface_given_context(self, target, context_parse_results, target_comes_after, count_given_context_surfaces, count_given_context_stems, count_given_context_lexemes):
        probability_target_surface_given_context_surfaces = self._calculate_probability_target_surface_given_context_surfaces(target, context_parse_results, target_comes_after, count_given_context_surfaces)
        probability_target_surface_given_context_stems = self._calculate_probability_target_surface_given_context_stems(target, context_parse_results, target_comes_after, count_given_context_stems)
        probability_target_surface_given_context_lexemes = self._calculate_probability_target_surface_given_context_lexemes(target, context_parse_results, target_comes_after, count_given_context_lexemes)

        logger.debug("       Found surface probability {} for context surfaces".format(probability_target_surface_given_context_surfaces))
        logger.debug("       Found surface probability {} for context stems".format(probability_target_surface_given_context_stems))
        logger.debug("       Found surface probability {} for context lexemes".format(probability_target_surface_given_context_lexemes))

        likelihood = (
            probability_target_surface_given_context_surfaces * self.COEFFICIENT_SURFACE_GIVEN_CONTEXT +
            probability_target_surface_given_context_stems * self.COEFFICIENT_STEM_GIVEN_CONTEXT+
            probability_target_surface_given_context_lexemes * self.COEFFICIENT_LEXEME_GIVEN_CONTEXT
            )

        return likelihood

    ################## 1.a target surface given context surfaces
    def _calculate_probability_target_surface_given_context_surfaces(self, target, context_parse_results, target_comes_after, count_given_context_surfaces):
        return self._calculate_probability_of_case(target, context_parse_results, target_comes_after, target_surface_syn_cat_appender, context_surface_syn_cat_appender, count_given_context_surfaces)

    ################## 1.b target surface given context stems
    def _calculate_probability_target_surface_given_context_stems(self, target, context_parse_results, target_comes_after, count_given_context_stems):
        return self._calculate_probability_of_case(target, context_parse_results, target_comes_after, target_surface_syn_cat_appender, context_stem_syn_cat_appender, count_given_context_stems)

    ################## 1.c target surface given context lexemes
    def _calculate_probability_target_surface_given_context_lexemes(self, target, context_parse_results, target_comes_after, count_given_context_lexemes):
        return self._calculate_probability_of_case(target, context_parse_results, target_comes_after, target_surface_syn_cat_appender, context_lemma_root_syn_cat_appender, count_given_context_lexemes)

    ################## 2. target stem given context
    def _calculate_probability_target_stem_given_context(self, target, context_parse_results, target_comes_after, count_given_context_surfaces, count_given_context_stems, count_given_context_lexemes):
        probability_target_stem_given_context_surfaces = self._calculate_probability_target_stem_given_context_surfaces(target, context_parse_results, target_comes_after, count_given_context_surfaces)
        probability_target_stem_given_context_stems = self._calculate_probability_target_stem_given_context_stems(target, context_parse_results, target_comes_after, count_given_context_stems)
        probability_target_stem_given_context_lexemes = self._calculate_probability_target_stem_given_context_lexemes(target, context_parse_results, target_comes_after, count_given_context_lexemes)

        logger.debug("       Found stem probability {} for context surfaces".format(probability_target_stem_given_context_surfaces))
        logger.debug("       Found stem probability {} for context stems".format(probability_target_stem_given_context_stems))
        logger.debug("       Found stem probability {} for context lexemes".format(probability_target_stem_given_context_lexemes))

        likelihood = (
            probability_target_stem_given_context_surfaces * self.COEFFICIENT_SURFACE_GIVEN_CONTEXT +
            probability_target_stem_given_context_stems * self.COEFFICIENT_STEM_GIVEN_CONTEXT+
            probability_target_stem_given_context_lexemes * self.COEFFICIENT_LEXEME_GIVEN_CONTEXT
            )

        return likelihood

    ################## 2.a target stem given context surfaces
    def _calculate_probability_target_stem_given_context_surfaces(self, target, context_parse_results, target_comes_after, count_given_context_surfaces):
        return self._calculate_probability_of_case(target, context_parse_results, target_comes_after, target_stem_syn_cat_appender, context_surface_syn_cat_appender, count_given_context_surfaces)

    ############## 2,b target stem given context stems
    def _calculate_probability_target_stem_given_context_stems(self, target, context_parse_results, target_comes_after, count_given_context_stems):
        return self._calculate_probability_of_case(target, context_parse_results, target_comes_after, target_stem_syn_cat_appender, context_stem_syn_cat_appender, count_given_context_stems)

    ############## 2.c target stem given context lexemes
    def _calculate_probability_target_stem_given_context_lexemes(self, target, context_parse_results, target_comes_after, count_given_context_lexemes):
        return self._calculate_probability_of_case(target, context_parse_results, target_comes_after, target_stem_syn_cat_appender, context_lemma_root_syn_cat_appender, count_given_context_lexemes)

    ################## 3. target lexeme given context
    def _calculate_probability_target_lexeme_given_context(self, target, context_parse_results, target_comes_after, count_given_context_surfaces, count_given_context_stems, count_given_context_lexemes):
        probability_target_lexeme_given_context_surfaces = self._calculate_probability_target_lexeme_given_context_surfaces(target, context_parse_results, target_comes_after, count_given_context_surfaces)
        probability_target_lexeme_given_context_stems = self._calculate_probability_target_lexeme_given_context_stems(target, context_parse_results, target_comes_after, count_given_context_stems)
        probability_target_lexeme_given_context_lexemes = self._calculate_probability_target_lexeme_given_context_lexemes(target, context_parse_results, target_comes_after, count_given_context_lexemes)

        logger.debug("       Found lexeme probability {} for context surfaces".format(probability_target_lexeme_given_context_surfaces))
        logger.debug("       Found lexeme probability {} for context stems".format(probability_target_lexeme_given_context_stems))
        logger.debug("       Found lexeme probability {} for context lexemes".format(probability_target_lexeme_given_context_lexemes))

        likelihood = (
            probability_target_lexeme_given_context_surfaces * self.COEFFICIENT_SURFACE_GIVEN_CONTEXT +
            probability_target_lexeme_given_context_stems * self.COEFFICIENT_STEM_GIVEN_CONTEXT+
            probability_target_lexeme_given_context_lexemes * self.COEFFICIENT_LEXEME_GIVEN_CONTEXT
            )

        return likelihood


    ################## 3.a target lexeme given context surfaces
    def _calculate_probability_target_lexeme_given_context_surfaces(self, target, context_parse_results, target_comes_after, count_given_context_surfaces):
        return self._calculate_probability_of_case(target, context_parse_results, target_comes_after, target_lemma_root_syn_cat_appender, context_surface_syn_cat_appender, count_given_context_surfaces)

    ################## 3.b target lexeme given context stems
    def _calculate_probability_target_lexeme_given_context_stems(self, target, context_parse_results, target_comes_after, count_given_context_stems):
        return self._calculate_probability_of_case(target, context_parse_results, target_comes_after, target_lemma_root_syn_cat_appender, context_stem_syn_cat_appender, count_given_context_stems)

    ################## 3.c target lexeme given context lexemes
    def _calculate_probability_target_lexeme_given_context_lexemes(self, target, context_parse_results, target_comes_after, count_given_context_lexemes):
        return self._calculate_probability_of_case(target, context_parse_results, target_comes_after, target_lemma_root_syn_cat_appender, context_lemma_root_syn_cat_appender, count_given_context_lexemes)

    #########
    def _find_count_for_query(self, params, query_container, target_comes_after):
        query_execution_context = QueryBuilder(self._collection_map).build_query(query_container, target_comes_after)
        return QueryExecutor().query_execution_context(query_execution_context).params(*params).count()