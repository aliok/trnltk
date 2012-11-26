class ContextfulLikelihoodCalculator(object):
    _WEIGHT_CONTEXTLESS_DISTRIBUTION_METRIC_CALCULATOR = 0.05
    _WEIGHT_COLLOCATION_METRIC_CALCULATOR = 0.95

    def __init__(self, collocation_metric_calculator, contextless_distribution_metric_calculator):
        """
        @type collocation_metric_calculator: BaseContextParsingLikelihoodCalculator
        @type contextless_distribution_metric_calculator: ContextlessDistributionCalculator
        """
        self._collocation_metric_calculator = collocation_metric_calculator
        self._contextless_distribution_metric_calculator = contextless_distribution_metric_calculator

    def calculate_likelihood_single(self, target, calculation_context=None):
        """
        @type target: MorphemeContainer
        @type calculation_context: dict
        @rtype: float
        """

        contextless_distribution_calculation_context = None if calculation_context is None else {}

        contextless_distribution_likelihood = self._contextless_distribution_metric_calculator.calculate(target, contextless_distribution_calculation_context)

        return self._WEIGHT_CONTEXTLESS_DISTRIBUTION_METRIC_CALCULATOR * contextless_distribution_likelihood

    def calculate_likelihood(self, target, leading_context, following_context, calculation_context=None):
        """
        @type target: MorphemeContainer
        @type leading_context: list<list<MorphemeContainer>>
        @type following_context: list<list<MorphemeContainer>>
        @type calculation_context: dict or None
        @rtype: float
        """
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
        @type calculation_context: dict
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
