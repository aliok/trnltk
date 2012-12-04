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

    def build_indexes(self):
        self._wrapped_calculator.build_indexes()

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
            calculation_context['interpolation'] = {'context_length': context_len, 'likelihood': {}, 'weight': {}, 'item': {}, 'part_weight': {}}

        interpolation_weights = self._calculate_interpolation_weights(context_len)

        total_likelihood = 0

        for i in range(0, len(context)):
            calculation_context_item = {} if calculation_context else None

            context_part = context[context_len - i - 1:] if target_comes_after else context[0: i + 1]
            part_likelihood = self._wrapped_calculator.calculate_oneway_likelihood(target, context_part, target_comes_after, calculation_context_item)
            part_weight = part_likelihood * interpolation_weights[i]
            total_likelihood += part_weight

            if calculation_context is not None:
                calculation_context['interpolation']['item'][i] = calculation_context_item
                calculation_context['interpolation']['likelihood'][i] = part_likelihood
                calculation_context['interpolation']['weight'][i] = interpolation_weights[i]
                calculation_context['interpolation']['part_weight'][i] = part_weight

        if calculation_context is not None:
            calculation_context['sum_likelihood'] = total_likelihood

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
