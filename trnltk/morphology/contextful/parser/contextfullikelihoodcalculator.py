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

    def calculate_likelihood_single(self, target):
        """
        @type target: MorphemeContainer
        """
        return self._WEIGHT_CONTEXTLESS_DISTRIBUTION_METRIC_CALCULATOR * self._contextless_distribution_metric_calculator.calculate(target)

    def calculate_likelihood(self, target, leading_context, following_context):
        """
        @type target: MorphemeContainer
        @param leading_context: list<list<MorphemeContainer>>
        @param following_context: list<list<MorphemeContainer>>
        @rtype: float
        """
        total = 0.0

        total += self._WEIGHT_COLLOCATION_METRIC_CALCULATOR * self._collocation_metric_calculator.calculate_likelihood(target, leading_context, following_context)
        total += self._WEIGHT_CONTEXTLESS_DISTRIBUTION_METRIC_CALCULATOR * self._contextless_distribution_metric_calculator.calculate(target)

        return total

    def calculate_oneway_likelihood(self, target, context, target_comes_after):
        """
        @type target: MorphemeContainer
        @param context: list<list<MorphemeContainer>>
        @rtype: float
        """
        total = 0.0

        total += self._WEIGHT_CONTEXTLESS_DISTRIBUTION_METRIC_CALCULATOR * self._contextless_distribution_metric_calculator.calculate(target)
        total += self._WEIGHT_COLLOCATION_METRIC_CALCULATOR * self._collocation_metric_calculator.calculate_oneway_likelihood(target, context, target_comes_after)

        return total
