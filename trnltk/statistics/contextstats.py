# coding=utf-8
import itertools
from trnltk.statistics.query import WordNGramQueryContainer, QueryBuilder, QueryExecutor

class NonContextParsingLikelihoodCalculator(object):
    COEFFICIENT_SURFACE_GIVEN_CONTEXT = 0.55
    COEFFICIENT_STEM_GIVEN_CONTEXT = 0.3
    COEFFICIENT_LEXEME_GIVEN_CONTEXT = 0.15

    WEIGHT_LEADING_CONTEXT = 0.6
    WEIGHT_FOLLOWING_CONTEXT = 0.4

    def __init__(self, collection_map):
        self._collection_map = collection_map

    def calculate_likelihood(self, target, leading_context, following_context):
        return self.calculate_oneway_likelihood(target, leading_context  , True ) * self.WEIGHT_LEADING_CONTEXT   + \
               self.calculate_oneway_likelihood(target, following_context, False) * self.WEIGHT_FOLLOWING_CONTEXT


    def calculate_oneway_likelihood(self, target, context, target_comes_after):
        """
        @type target: WordFormContainer
        @type context: list of WordFormContainer
        @type target_comes_after: bool
        @rtype: float
        """
        assert target
        assert context

        count_given_context = self._count_given_context(context)

        if not count_given_context:
            return 0

        count_target_surface_given_context = self._count_target_surface_given_context(target, context, target_comes_after)
        count_target_stem_given_context = self._count_target_stem_given_context(target, context, target_comes_after)
        count_target_lexeme_given_context = self._count_target_lexeme_given_context(target, context, target_comes_after)

        likelihood = (
                         count_target_surface_given_context * self.COEFFICIENT_SURFACE_GIVEN_CONTEXT +
                         count_target_stem_given_context * self.COEFFICIENT_STEM_GIVEN_CONTEXT+
                         count_target_lexeme_given_context * self.COEFFICIENT_LEXEME_GIVEN_CONTEXT
                     ) / count_given_context

        return likelihood

    def _count_given_context(self, context):
        query_container = WordNGramQueryContainer(len(context))
        params = []
        for context_item in context:
            query_container = query_container.given_surface(False)
            params.append(context_item[0])

        # target_comes_after doesn't matter, since there is no target
        return self._find_count_for_query(params, query_container, False)

    def _count_target_surface_given_context(self, target, context, target_comes_after):
        query_container = WordNGramQueryContainer(len(context) + 1)
        params = []

        query_container = query_container.target_surface(True)
        params.append(target.get_surface())
        params.append(target.get_surface_syntactic_category())

        for context_item in context:
            query_container = query_container.given_surface(False)
            params.append(context_item[0])

        return self._find_count_for_query(params, query_container, target_comes_after)

    def _count_target_stem_given_context(self, target, context, target_comes_after):
        query_container = WordNGramQueryContainer(len(context) + 1)
        params = []

        query_container = query_container.target_stem(True)
        params.append(target.get_stem())
        params.append(target.get_stem_syntactic_category())

        for context_item in context:
            query_container = query_container.given_surface(False)
            params.append(context_item[0])

        return self._find_count_for_query(params, query_container, target_comes_after)

    def _count_target_lexeme_given_context(self, target, context, target_comes_after):
        query_container = WordNGramQueryContainer(len(context) + 1)
        params = []

        query_container = query_container.target_lemma_root(True)
        params.append(target.get_lemma_root())
        params.append(target.get_lemma_root_syntactic_category())

        for context_item in context:
            query_container = query_container.given_surface(False)
            params.append(context_item[0])

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
        return self.calculate_oneway_likelihood(target, leading_context  , True ) * self.WEIGHT_LEADING_CONTEXT   +\
               self.calculate_oneway_likelihood(target, following_context, False) * self.WEIGHT_FOLLOWING_CONTEXT


    def calculate_oneway_likelihood(self, target, context, target_comes_after):
        """
        @type target: WordFormContainer
        @type context: list of WordFormContainer
        @type target_comes_after: bool
        @rtype: float
        """
        assert target
        assert context

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
            p_target_surface_given_context = self._calculate_probability_target_surface_given_context(target, context_parse_results, target_comes_after)
            p_target_stem_given_context = self._calculate_probability_target_stem_given_context(target, context_parse_results, target_comes_after)
            p_target_lexeme_given_context = self._calculate_probability_target_lexeme_given_context(target, context_parse_results, target_comes_after)


            likelihood +=  p_target_surface_given_context * self.COEFFICIENT_SURFACE_GIVEN_CONTEXT +\
                           p_target_stem_given_context    * self.COEFFICIENT_STEM_GIVEN_CONTEXT    +\
                           p_target_lexeme_given_context  * self.COEFFICIENT_LEXEME_GIVEN_CONTEXT

        return likelihood

    def _count_given_context(self, context):
        query_container = WordNGramQueryContainer(len(context))
        params = []
        for context_item in context:
            query_container = query_container.given_surface(False)
            params.append(context_item[0])

        # target_comes_after doesn't matter, since there is no target
        return self._find_count_for_query(params, query_container, False)

    ################## context form counts
    def _count_given_context_surfaces(self, context_parse_results):
        query_container = WordNGramQueryContainer(len(context_parse_results))
        params = []
        for context_item_parse_result in context_parse_results:
            query_container = query_container.given_surface(True)
            params.append(context_item_parse_result.get_surface())
            params.append(context_item_parse_result.get_surface_syntactic_category())

        # target_comes_after doesn't matter, since there is no target
        return self._find_count_for_query(params, query_container, False)

    def _count_given_context_stems(self, context_parse_results):
        query_container = WordNGramQueryContainer(len(context_parse_results))
        params = []
        for context_item_parse_result in context_parse_results:
            query_container = query_container.given_stem(True)
            params.append(context_item_parse_result.get_stem())
            params.append(context_item_parse_result.get_stem_syntactic_category())

        # target_comes_after doesn't matter, since there is no target
        return self._find_count_for_query(params, query_container, False)

    def _count_given_context_lexemes(self, context_parse_results):
        query_container = WordNGramQueryContainer(len(context_parse_results))
        params = []
        for context_item_parse_result in context_parse_results:
            query_container = query_container.given_lemma_root(True)
            params.append(context_item_parse_result.get_lemma_root())
            params.append(context_item_parse_result.get_lemma_root_syntactic_category())

        # target_comes_after doesn't matter, since there is no target
        return self._find_count_for_query(params, query_container, False)


    ################## 1. target surface given context
    def _calculate_probability_target_surface_given_context(self, target, context_parse_results, target_comes_after):
        probability_target_surface_given_context_surfaces = self._calculate_probability_target_surface_given_context_surfaces(target, context_parse_results, target_comes_after)
        probability_target_surface_given_context_stems = self._calculate_probability_target_surface_given_context_stems(target, context_parse_results, target_comes_after)
        probability_target_surface_given_context_lexemes = self._calculate_probability_target_surface_given_context_lexemes(target, context_parse_results, target_comes_after)

        likelihood = (
                          probability_target_surface_given_context_surfaces * self.COEFFICIENT_SURFACE_GIVEN_CONTEXT +
                          probability_target_surface_given_context_stems * self.COEFFICIENT_STEM_GIVEN_CONTEXT+
                          probability_target_surface_given_context_lexemes * self.COEFFICIENT_LEXEME_GIVEN_CONTEXT
                      )

        return likelihood

    def _calculate_probability_target_surface_given_context_surfaces(self, target, context_parse_results, target_comes_after):
        count_given_context_surfaces = self._count_given_context_surfaces(context_parse_results)

        if not count_given_context_surfaces:
            return 0.0

        count_target_surface_given_context_surfaces = self._count_target_surface_given_context_surfaces(target, context_parse_results, target_comes_after)

        return count_target_surface_given_context_surfaces / count_given_context_surfaces

    ################## 1.a target surface given context surfaces
    def _count_target_surface_given_context_surfaces(self, target, context_parse_results, target_comes_after):
        query_container = WordNGramQueryContainer(len(context_parse_results) + 1)
        params = []

        query_container = query_container.target_surface(True)
        params.append(target.get_surface())
        params.append(target.get_surface_syntactic_category())

        for context_item_parse_result in context_parse_results:
            query_container = query_container.given_surface(True)
            params.append(context_item_parse_result.get_surface())
            params.append(context_item_parse_result.get_surface_syntactic_category())

        return self._find_count_for_query(params, query_container, target_comes_after)

    ################## 1.b target surface given context stems
    def _calculate_probability_target_surface_given_context_stems(self, target, context_parse_results, target_comes_after):
        count_given_context_stems = self._count_given_context_stems(context_parse_results)

        if not count_given_context_stems:
            return 0.0

        count_target_surface_given_context_stems = self._count_target_surface_given_context_stems(target, context_parse_results, target_comes_after)

        return count_target_surface_given_context_stems / count_given_context_stems

    def _count_target_surface_given_context_stems(self, target, context_parse_results, target_comes_after):
        query_container = WordNGramQueryContainer(len(context_parse_results) + 1)
        params = []

        query_container = query_container.target_surface(True)
        params.append(target.get_surface())
        params.append(target.get_surface_syntactic_category())

        for context_item_parse_result in context_parse_results:
            query_container = query_container.given_stem(True)
            params.append(context_item_parse_result.get_stem())
            params.append(context_item_parse_result.get_stem_syntactic_category())

        return self._find_count_for_query(params, query_container, target_comes_after)

    ################## 1.c target surface given context lexemes
    def _calculate_probability_target_surface_given_context_lexemes(self, target, context_parse_results, target_comes_after):
        count_given_context_lexemes = self._count_given_context_lexemes(context_parse_results)

        if not count_given_context_lexemes:
            return 0.0

        count_target_surface_given_context_lexemes = self._count_target_surface_given_context_lexemes(target, context_parse_results, target_comes_after)

        return count_target_surface_given_context_lexemes / count_given_context_lexemes

    def _count_target_surface_given_context_lexemes(self, target, context_parse_results, target_comes_after):
        query_container = WordNGramQueryContainer(len(context_parse_results) + 1)
        params = []

        query_container = query_container.target_surface(True)
        params.append(target.get_surface())
        params.append(target.get_surface_syntactic_category())

        for context_item_parse_result in context_parse_results:
            query_container = query_container.given_lemma_root(True)
            params.append(context_item_parse_result.get_lemma_root())
            params.append(context_item_parse_result.get_lemma_root_syntactic_category())

        return self._find_count_for_query(params, query_container, target_comes_after)


    ################## 2. target stem given context
    def _calculate_probability_target_stem_given_context(self, target, context_parse_results, target_comes_after):
        probability_target_stem_given_context_surfaces = self._calculate_probability_target_stem_given_context_surfaces(target, context_parse_results, target_comes_after)
        probability_target_stem_given_context_stems = self._calculate_probability_target_stem_given_context_stems(target, context_parse_results, target_comes_after)
        probability_target_stem_given_context_lexemes = self._calculate_probability_target_stem_given_context_lexemes(target, context_parse_results, target_comes_after)

        likelihood = (
            probability_target_stem_given_context_surfaces * self.COEFFICIENT_SURFACE_GIVEN_CONTEXT +
            probability_target_stem_given_context_stems * self.COEFFICIENT_STEM_GIVEN_CONTEXT+
            probability_target_stem_given_context_lexemes * self.COEFFICIENT_LEXEME_GIVEN_CONTEXT
            )

        return likelihood

    ################## 2.a target stem given context surfaces
    def _calculate_probability_target_stem_given_context_surfaces(self, target, context_parse_results, target_comes_after):
        count_given_context_surfaces = self._count_given_context_surfaces(context_parse_results)

        if not count_given_context_surfaces:
            return 0.0

        count_target_stem_given_context_surfaces = self._count_target_stem_given_context_surfaces(target, context_parse_results, target_comes_after)

        return count_target_stem_given_context_surfaces / count_given_context_surfaces

    def _count_target_stem_given_context_surfaces(self, target, context_parse_results, target_comes_after):
        query_container = WordNGramQueryContainer(len(context_parse_results) + 1)
        params = []

        query_container = query_container.target_stem(True)
        params.append(target.get_stem())
        params.append(target.get_stem_syntactic_category())

        for context_item_parse_result in context_parse_results:
            query_container = query_container.given_surface(True)
            params.append(context_item_parse_result.get_surface())
            params.append(context_item_parse_result.get_surface_syntactic_category())

        return self._find_count_for_query(params, query_container, target_comes_after)

    ############## 2,b target stem given context stems
    def _calculate_probability_target_stem_given_context_stems(self, target, context_parse_results, target_comes_after):
        count_given_context_stems = self._count_given_context_stems(context_parse_results)

        if not count_given_context_stems:
            return 0.0

        count_target_stem_given_context_stems = self._count_target_stem_given_context_stems(target, context_parse_results, target_comes_after)

        return count_target_stem_given_context_stems / count_given_context_stems

    def _count_target_stem_given_context_stems(self, target, context_parse_results, target_comes_after):
        query_container = WordNGramQueryContainer(len(context_parse_results) + 1)
        params = []

        query_container = query_container.target_stem(True)
        params.append(target.get_stem())
        params.append(target.get_stem_syntactic_category())

        for context_item_parse_result in context_parse_results:
            query_container = query_container.given_stem(True)
            params.append(context_item_parse_result.get_stem())
            params.append(context_item_parse_result.get_stem_syntactic_category())

        return self._find_count_for_query(params, query_container, target_comes_after)

    ############## 2,c target stem given context lexemes
    def _calculate_probability_target_stem_given_context_lexemes(self, target, context_parse_results, target_comes_after):
        count_given_context_lexemes = self._count_given_context_lexemes(context_parse_results)

        if not count_given_context_lexemes:
            return 0.0

        count_target_stem_given_context_lexemes = self._count_target_stem_given_context_lexemes(target, context_parse_results, target_comes_after)

        return count_target_stem_given_context_lexemes / count_given_context_lexemes

    def _count_target_stem_given_context_lexemes(self, target, context_parse_results, target_comes_after):
        query_container = WordNGramQueryContainer(len(context_parse_results) + 1)
        params = []

        query_container = query_container.target_stem(True)
        params.append(target.get_stem())
        params.append(target.get_stem_syntactic_category())

        for context_item_parse_result in context_parse_results:
            query_container = query_container.given_lemma_root(True)
            params.append(context_item_parse_result.get_lemma_root())
            params.append(context_item_parse_result.get_lemma_root_syntactic_category())

        return self._find_count_for_query(params, query_container, target_comes_after)


    ################## 3. target lexeme given context
    def _calculate_probability_target_lexeme_given_context(self, target, context_parse_results, target_comes_after):
        probability_target_lexeme_given_context_surfaces = self._calculate_probability_target_lexeme_given_context_surfaces(target, context_parse_results, target_comes_after)
        probability_target_lexeme_given_context_stems = self._calculate_probability_target_lexeme_given_context_stems(target, context_parse_results, target_comes_after)
        probability_target_lexeme_given_context_lexemes = self._calculate_probability_target_lexeme_given_context_lexemes(target, context_parse_results, target_comes_after)

        likelihood = (
            probability_target_lexeme_given_context_surfaces * self.COEFFICIENT_SURFACE_GIVEN_CONTEXT +
            probability_target_lexeme_given_context_stems * self.COEFFICIENT_STEM_GIVEN_CONTEXT+
            probability_target_lexeme_given_context_lexemes * self.COEFFICIENT_LEXEME_GIVEN_CONTEXT
            )

        return likelihood


    ################## 3.a target lexeme given context surfaces
    def _calculate_probability_target_lexeme_given_context_surfaces(self, target, context_parse_results, target_comes_after):
        count_given_context_surfaces = self._count_given_context_surfaces(context_parse_results)

        if not count_given_context_surfaces:
            return 0.0

        count_target_lexeme_given_context_surfaces = self._count_target_lexeme_given_context_surfaces(target, context_parse_results, target_comes_after)

        return count_target_lexeme_given_context_surfaces / count_given_context_surfaces

    def _count_target_lexeme_given_context_surfaces(self, target, context_parse_results, target_comes_after):
        query_container = WordNGramQueryContainer(len(context_parse_results) + 1)
        params = []

        query_container = query_container.target_lemma_root(True)
        params.append(target.get_lemma_root())
        params.append(target.get_lemma_root_syntactic_category())

        for context_item_parse_result in context_parse_results:
            query_container = query_container.given_surface(True)
            params.append(context_item_parse_result.get_surface())
            params.append(context_item_parse_result.get_surface_syntactic_category())

        return self._find_count_for_query(params, query_container, target_comes_after)

    ################## 3.b target lexeme given context stems
    def _calculate_probability_target_lexeme_given_context_stems(self, target, context_parse_results, target_comes_after):
        count_given_context_stems = self._count_given_context_stems(context_parse_results)

        if not count_given_context_stems:
            return 0.0

        count_target_lexeme_given_context_stems = self._count_target_lexeme_given_context_stems(target, context_parse_results, target_comes_after)

        return count_target_lexeme_given_context_stems / count_given_context_stems

    def _count_target_lexeme_given_context_stems(self, target, context_parse_results, target_comes_after):
        query_container = WordNGramQueryContainer(len(context_parse_results) + 1)
        params = []

        query_container = query_container.target_lemma_root(True)
        params.append(target.get_lemma_root())
        params.append(target.get_lemma_root_syntactic_category())

        for context_item_parse_result in context_parse_results:
            query_container = query_container.given_stem(True)
            params.append(context_item_parse_result.get_stem())
            params.append(context_item_parse_result.get_stem_syntactic_category())

        return self._find_count_for_query(params, query_container, target_comes_after)

    ################## 3.c target lexeme given context lexemes
    def _calculate_probability_target_lexeme_given_context_lexemes(self, target, context_parse_results, target_comes_after):
        count_given_context_lexemes = self._count_given_context_lexemes(context_parse_results)

        if not count_given_context_lexemes:
            return 0.0

        count_target_lexeme_given_context_lexemes = self._count_target_lexeme_given_context_lexemes(target, context_parse_results, target_comes_after)

        return count_target_lexeme_given_context_lexemes / count_given_context_lexemes

    def _count_target_lexeme_given_context_lexemes(self, target, context_parse_results, target_comes_after):
        query_container = WordNGramQueryContainer(len(context_parse_results) + 1)
        params = []

        query_container = query_container.target_lemma_root(True)
        params.append(target.get_lemma_root())
        params.append(target.get_lemma_root_syntactic_category())

        for context_item_parse_result in context_parse_results:
            query_container = query_container.given_lemma_root(True)
            params.append(context_item_parse_result.get_lemma_root())
            params.append(context_item_parse_result.get_lemma_root_syntactic_category())

        return self._find_count_for_query(params, query_container, target_comes_after)

    #########
    def _find_count_for_query(self, params, query_container, target_comes_after):
        query_execution_context = QueryBuilder(self._collection_map).build_query(query_container, target_comes_after)
        return QueryExecutor().query_execution_context(query_execution_context).params(*params).count()