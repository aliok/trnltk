# coding=utf-8
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
import itertools
import logging
import numpy
from trnltk.morphology.contextful.likelihoodmetrics.hidden.querykeyappender import _context_word_appender, _target_surface_syn_cat_appender, _target_stem_syn_cat_appender, _target_lemma_root_syn_cat_appender, _context_surface_syn_cat_appender, _context_stem_syn_cat_appender, _context_lemma_root_syn_cat_appender
from trnltk.morphology.contextful.likelihoodmetrics.hidden import query
from trnltk.morphology.contextful.parser.sequencelikelihoodcalculator import SequenceLikelihoodCalculator
from trnltk.morphology.model import formatter

numpy.seterr(divide='ignore', invalid='ignore')

logger = logging.getLogger('contextParsingCollocationLikelihoodCalculatorLogger')
query_logger = query.logger

class BaseContextParsingLikelihoodCalculator(object):
    WEIGHT_LEADING_CONTEXT = 0.6
    WEIGHT_FOLLOWING_CONTEXT = 0.4

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
        raise NotImplementedError()

    def build_indexes(self):
        raise NotImplementedError()


class ContextParsingLikelihoodCalculator(BaseContextParsingLikelihoodCalculator):
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

    def __init__(self, database_index_builder, target_form_given_context_counter, ngram_frequency_smoother, sequence_likelihood_calculator):
        """
        @type database_index_builder: DatabaseIndexBuilder
        @type target_form_given_context_counter: TargetFormGivenContextCounter
        @type ngram_frequency_smoother: NGramFrequencySmoother
        @type sequence_likelihood_calculator: SequenceLikelihoodCalculator
        """
        self._database_index_builder = database_index_builder
        self._ngram_frequency_smoother = ngram_frequency_smoother
        self._sequence_likelihood_calculator = sequence_likelihood_calculator
        self._target_form_given_context_counter = target_form_given_context_counter

    def build_indexes(self):
        self._database_index_builder.create_indexes([(_context_word_appender,)])
        for appender_matrix_row in self.APPENDER_MATRIX:
            self._database_index_builder.create_indexes(appender_matrix_row)

    def calculate_oneway_likelihood(self, target, context, target_comes_after, calculation_context=None):
        """
        @type target: WordFormContainer
        @type context: list of WordFormContainer
        @type target_comes_after: bool
        @rtype: float
        """
        assert target
        assert context

        target_morpheme_container_str = target.format()

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

        if calculation_context is not None:
            calculation_context['possibilities'] = {}

        target_likelihoods_for_context_parse_results = []
        context_parse_results_likelihoods = []

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
                    target_form_given_count = self._target_form_given_context_counter._count_target_form_given_context(target, context_parse_results, target_comes_after, target_appender,
                        context_appender)
                    target_form_given_context_counts[i][j] = target_form_given_count

            logger.debug("       Target form counts given context forms: \n{}".format(target_form_given_context_counts))

            if calculation_context is not None:
                word_calc_context['target_form_counts'] = target_form_given_context_counts
            logger.debug("       Target form counts: \n{}".format(target_form_given_context_counts))

            smoothed_target_form_given_context_counts = self._smooth_target_context_cooccurrence_counts(target_form_given_context_counts, target,
                context_parse_results, target_comes_after)

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

            target_likelihoods_for_context_parse_results.append(item_likelihood)

            logger.debug("      Calculated oneway likelihood for target given context item is {}".format(item_likelihood))

            # say, target_comes_after=True, context={c1,c2} and target=t
            # until now, we looked at collocation of (c1, c2, t) and (c2,t)
            # now we look collocation of (c1,c2)
            # which makes complete sense while calculating the weight for current cartesian product item
            context_sequence_likelihood_calculation_direction = SequenceLikelihoodCalculator.HIGHEST_WEIGHT_ON_LAST if target_comes_after else SequenceLikelihoodCalculator.HIGHEST_WEIGHT_ON_FIRST
            sequence_likelihood_context = {} if calculation_context is not None else None
            context_likelihood = self._sequence_likelihood_calculator.calculate(context_parse_results, context_sequence_likelihood_calculation_direction, sequence_likelihood_context)

            if calculation_context is not None:
                word_calc_context['context_sequence_likelihood'] = sequence_likelihood_context

            context_parse_results_likelihoods.append(context_likelihood)

            logger.debug("      Context likelihood is {}".format(context_likelihood))

        likelihood = 0.0

        # normalize but don't smooth. weights are already smoothed
        total_context_parse_results_weights = sum(context_parse_results_likelihoods)
        normalized_context_parse_results_weights = []
        if total_context_parse_results_weights:
            normalized_context_parse_results_weights = [context_parse_results_item_weight/total_context_parse_results_weights for context_parse_results_item_weight in context_parse_results_likelihoods]
        else:
            normalized_context_parse_results_weights = [0.0 for context_parse_results_item_weight in context_parse_results_likelihoods]
        logger.debug("     Normalized context parse results weights are {}".format(normalized_context_parse_results_weights))

        for index, context_parse_results in enumerate(cartesian_products_of_context_parse_results):
            target_likelihood_for_context_parse_results_item = target_likelihoods_for_context_parse_results[index]
            context_parse_results_item_likelihood = normalized_context_parse_results_weights[index]
            weighted_parse_result_possibility_likelihood = context_parse_results_item_likelihood * target_likelihood_for_context_parse_results_item
            likelihood += weighted_parse_result_possibility_likelihood
            if calculation_context is not None:
                word_calc_context = calculation_context['possibilities'][index]
                word_calc_context['context_likelihood'] = context_parse_results_item_likelihood
                word_calc_context['weighted_parse_result_possibility_likelihood'] = weighted_parse_result_possibility_likelihood

            logger.debug("      Weighted context parse result likelihood is {} for context : {}".format(weighted_parse_result_possibility_likelihood, context_parse_results))

        if calculation_context is not None:
            calculation_context['sum_likelihood'] = likelihood
        logger.debug("  Calculated oneway likelihood is {}".format(likelihood))

        return likelihood

    def _get_context_form_count_matrix(self, context_parse_results):
        context_form_counts = numpy.zeros(3, dtype=float)

        for i, context_appender in enumerate(self.CONTEXT_APPENDER_VECTOR):
            # target_comes_after doesn't matter, since there is no target
            context_form_count = self._target_form_given_context_counter._count_target_form_given_context(None, context_parse_results, False, None, context_appender)
            context_form_counts[i] = context_form_count

        return context_form_counts

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

                ngram_type = [target_ngram_type_item] + context_len * [context_ngram_type_item] if target_comes_after else context_len * [
                    context_ngram_type_item] + [target_ngram_type_item]

                smoothed_counts[i][j] = self._ngram_frequency_smoother.smooth(target_form_given_context_counts[i][j], ngram_type)

        return smoothed_counts
