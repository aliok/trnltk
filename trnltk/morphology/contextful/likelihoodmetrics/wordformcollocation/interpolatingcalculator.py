import logging
import math
from trnltk.morphology.contextful.likelihoodmetrics.wordformcollocation.contextparsingcalculator import  BaseContextParsingLikelihoodCalculator
from trnltk.morphology.model import formatter

logger = logging.getLogger('interpolatingCollocationLikelihoodCalculator')

class InterpolatingLikelihoodCalculator(BaseContextParsingLikelihoodCalculator):
    ALPHA = 10

    def __init__(self, wrapped_calculator):
        """
        @type wrapped_calculator: BaseContextParsingLikelihoodCalculator
        """
        self._wrapped_calculator = wrapped_calculator

    def calculate_oneway_likelihood(self, target, context, target_comes_after, calculation_context=None):
        if logger.isEnabledFor(logging.DEBUG):
            if target_comes_after:
                logger.debug(u"  Calculating oneway likelihood of {1}, {0}".format(formatter.format_morpheme_container_for_simple_parseset(target),
                    [t[0].get_surface() if t else "<Unparsable>" for t in context]))
            else:
                logger.debug(u"  Calculating oneway likelihood of {0}, {1}".format(formatter.format_morpheme_container_for_simple_parseset(target),
                    [t[0].get_surface() if t else "<Unparsable>" for t in context]))

        context_len = len(context)

        if calculation_context is not None:
            calculation_context['interpolation'] = {'context_length': context_len, 'likelihood': {}, 'weight': {}, 'item': {}}

        interpolation_weights = self._calculate_interpolation_weights(context_len)

        total_likelihood = 0

        for i in range(0, len(context)):
            calculation_context_item = {} if calculation_context else None

            context_part = context[context_len - i - 1:] if target_comes_after else context[0: i + 1]
            part_likelihood = self._wrapped_calculator.calculate_oneway_likelihood(target, context_part, target_comes_after, calculation_context_item)
            total_likelihood += part_likelihood * interpolation_weights[i]

            if calculation_context is not None:
                calculation_context['interpolation']['item'][i] = calculation_context_item
                calculation_context['interpolation']['likelihood'][i] = part_likelihood
                calculation_context['interpolation']['weight'][i] = interpolation_weights[i]

        return total_likelihood

    def _calculate_interpolation_weights(self, context_len):
        denominator = 0

        for i in range(0, context_len):
            denominator += math.pow(self.ALPHA, i)

        weights = []
        for i in range(0, context_len):
            nominator = math.pow(self.ALPHA, i)
            weights.append(nominator / denominator)

        return weights
