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
from __future__ import division

class SequenceLikelihoodCalculator(object):
    # this means, context is like [A,B] and likelihood is P(A)*x + P(AB)*y, where y>x
    HIGHEST_WEIGHT_ON_LAST = "HIGHEST_WEIGHT_ON_LAST"

    # this means, context is like [A,B] and likelihood is P(AB)*x + p(B)*y, where x>y
    HIGHEST_WEIGHT_ON_FIRST = "HIGHEST_WEIGHT_ON_FIRST"

    _ALPHA = 10 # use same alpha with InterpolatingLikelihoodCalculator
    _WEIGHT_FOR_1 = 1 / (_ALPHA + 1)
    _WEIGHT_FOR_2 = _ALPHA / (_ALPHA + 1)

    def __init__(self, contextful_likelihood_calculator):
        """
        @type contextful_likelihood_calculator: ContextfulLikelihoodCalculator
        """
        self._contextful_likelihood_calculator = contextful_likelihood_calculator

    def calculate(self, context, direction=None, calculation_context=None):
        """
        Finds the likelihood for a parse result sequence.

        Simplified formula: P(AB,HIGHEST_WEIGHT_ON_LAST) = x*(P(A) * P(B) * P(B|A)) + y*(P(B))

        Doesn't apply smoothing to P(A), P(B) and P(B|A); since those values are already smoothed.

        @param direction: Cannot be None if len(context)>1
        @type context: list
        @type direction: str
        @rtype: float
        """
        if not context:
            return 0.0

        context_len = len(context)

        if calculation_context is not None:
            calculation_context['sequence_length'] = context_len

        if context_len == 1:
            return self._contextful_likelihood_calculator.calculate_likelihood_single(context[0], calculation_context)
        elif context_len == 2:
            assert direction in [self.HIGHEST_WEIGHT_ON_FIRST, self.HIGHEST_WEIGHT_ON_LAST]

            if calculation_context is not None:
                calculation_context['direction'] = direction
                calculation_context['A'] = {}
                calculation_context['B'] = {}
                calculation_context['A_GIVEN_B'] = {}
                calculation_context['B_GIVEN_A'] = {}

            calc_context_A = calculation_context['A'] if calculation_context is not None else None
            calc_context_B = calculation_context['B'] if calculation_context is not None else None
            calc_context_B_GIVEN_A = calculation_context['B_GIVEN_A'] if calculation_context is not None else None
            calc_context_A_GIVEN_B = calculation_context['A_GIVEN_B'] if calculation_context is not None else None


            if direction == self.HIGHEST_WEIGHT_ON_LAST:
                # P(A)*x + P(AB)*y, y>x
                A = context[0]
                B = context[1]
                target_comes_after = True

                P_A = self.calculate([A], calc_context_A)    # P(A)
                P_B = self.calculate([B], calc_context_B)    # P(B)
                P_B_GIVEN_A = self._contextful_likelihood_calculator.calculate_oneway_likelihood(B, [[A]], target_comes_after, calc_context_B_GIVEN_A)
                P_AB = P_A * P_B * P_B_GIVEN_A      # P(AB) = P(A) * P(B) * P(B|A)

                weighted_likelihood = P_A * self._WEIGHT_FOR_1 + P_AB * self._WEIGHT_FOR_2

                if calculation_context is not None:
                    calculation_context['P_A'] = P_A
                    calculation_context['P_B'] = P_B
                    calculation_context['P_B_GIVEN_A'] = P_B_GIVEN_A
                    calculation_context['P_AB'] = P_AB
                    calculation_context['weight_A'] = self._WEIGHT_FOR_1
                    calculation_context['weight_AB'] = self._WEIGHT_FOR_2
                    calculation_context['weighted_likelihood'] = weighted_likelihood

                return weighted_likelihood
            else:
                # P(AB)*x + P(B)*y, x>y
                A = context[0]
                B = context[1]
                target_comes_after = False

                P_A = self.calculate([A], calc_context_A)    # P(A)
                P_B = self.calculate([B], calc_context_B)    # P(B)
                P_A_GIVEN_B = self._contextful_likelihood_calculator.calculate_oneway_likelihood(A, [[B]], target_comes_after, calc_context_A_GIVEN_B)
                P_AB = P_A * P_B * P_A_GIVEN_B      # P(AB) = P(A) * P(B) * P(A|B). we use P(A|B) here and that is not a mistake

                weighted_likelihood = P_B * self._WEIGHT_FOR_1 + P_AB * self._WEIGHT_FOR_2

                if calculation_context is not None:
                    calculation_context['P_A'] = P_A
                    calculation_context['P_B'] = P_B
                    calculation_context['P_A_GIVEN_B'] = P_A_GIVEN_B
                    calculation_context['P_AB'] = P_AB
                    calculation_context['weight_B'] = self._WEIGHT_FOR_1
                    calculation_context['weight_AB'] = self._WEIGHT_FOR_2
                    calculation_context['weighted_likelihood'] = weighted_likelihood

                return weighted_likelihood

        else:
            # impractical to use for now.
            # takes time to convert the code to work with arbitrary lengths
            raise NotImplementedError("Context length > 3 is not supported yet!")

class UniformSequenceLikelihoodCalculator(SequenceLikelihoodCalculator):
    def __init__(self):
        super(UniformSequenceLikelihoodCalculator, self).__init__(None)

    def calculate(self, context, direction=None, calculation_context=None):
        return 1.0      # this will be normalized by the caller