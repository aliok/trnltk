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
class ContextfulLikelihoodCalculator(object):
    _WEIGHT_CONTEXTLESS_DISTRIBUTION_METRIC_CALCULATOR = 0.01
    _WEIGHT_COLLOCATION_METRIC_CALCULATOR = 0.99

    def __init__(self, collocation_metric_calculator, contextless_distribution_metric_calculator):
        """
        @type collocation_metric_calculator: BaseContextParsingLikelihoodCalculator
        @type contextless_distribution_metric_calculator: ContextlessDistributionCalculator
        """
        self._collocation_metric_calculator = collocation_metric_calculator
        self._contextless_distribution_metric_calculator = contextless_distribution_metric_calculator

    def build_indexes(self):
        self._collocation_metric_calculator.build_indexes()
        self._contextless_distribution_metric_calculator.build_indexes()

    def calculate_likelihood_single(self, target, calculation_context=None):
        """
        @type target: MorphemeContainer
        @type calculation_context: dict or None
        @rtype: float
        """

        contextless_distribution_calculation_context = {} if calculation_context is not None else None

        contextless_distribution_likelihood = self._contextless_distribution_metric_calculator.calculate(target, contextless_distribution_calculation_context)

        total = self._WEIGHT_CONTEXTLESS_DISTRIBUTION_METRIC_CALCULATOR * contextless_distribution_likelihood

        if calculation_context is not None:
            calculation_context['contextless_distribution'] = contextless_distribution_calculation_context

            calculation_context['contextless_distribution_metric_weight'] = self._WEIGHT_CONTEXTLESS_DISTRIBUTION_METRIC_CALCULATOR

            calculation_context['total_likelihood'] = total

        return total

    def calculate_likelihood(self, target, leading_context, following_context, calculation_context=None):
        """
        @type target: MorphemeContainer
        @type leading_context: list<list<MorphemeContainer>>
        @type following_context: list<list<MorphemeContainer>>
        @type calculation_context: dict or None
        @rtype: float
        """

        assert target

        if not leading_context and not following_context:
            return self.calculate_likelihood_single(target, calculation_context)

        total = 0.0

        collocation_calculation_context = None if calculation_context is None else {}
        contextless_distribution_calculation_context = None if calculation_context is None else {}

        collocation_likelihood = self._collocation_metric_calculator.calculate_likelihood(target, leading_context, following_context,
            collocation_calculation_context)
        contextless_distribution_likelihood = self._contextless_distribution_metric_calculator.calculate(target, contextless_distribution_calculation_context)

        total += self._WEIGHT_COLLOCATION_METRIC_CALCULATOR * collocation_likelihood
        total += self._WEIGHT_CONTEXTLESS_DISTRIBUTION_METRIC_CALCULATOR * contextless_distribution_likelihood

        if calculation_context is not None:
            calculation_context['collocation'] = collocation_calculation_context
            calculation_context['contextless_distribution'] = contextless_distribution_calculation_context

            calculation_context['collocation_metric_weight'] = self._WEIGHT_COLLOCATION_METRIC_CALCULATOR
            calculation_context['contextless_distribution_metric_weight'] = self._WEIGHT_CONTEXTLESS_DISTRIBUTION_METRIC_CALCULATOR

            calculation_context['total_likelihood'] = total

        return total

    def calculate_oneway_likelihood(self, target, context, target_comes_after, calculation_context=None):
        """
        @type target: MorphemeContainer
        @type context: list<list<MorphemeContainer>>
        @type calculation_context: dict or None
        @rtype: float
        """
        total = 0.0

        collocation_calculation_context = None if calculation_context is None else {}
        contextless_distribution_calculation_context = None if calculation_context is None else {}

        collocation_likelihood = self._collocation_metric_calculator.calculate_oneway_likelihood(target, context, target_comes_after,
            collocation_calculation_context)
        contextless_distribution_likelihood = self._contextless_distribution_metric_calculator.calculate(target, contextless_distribution_calculation_context)

        total += self._WEIGHT_COLLOCATION_METRIC_CALCULATOR * collocation_likelihood
        total += self._WEIGHT_CONTEXTLESS_DISTRIBUTION_METRIC_CALCULATOR * contextless_distribution_likelihood

        if calculation_context is not None:
            calculation_context['collocation'] = collocation_calculation_context
            calculation_context['contextless_distribution'] = contextless_distribution_calculation_context

        return total
