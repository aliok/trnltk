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
import logging
import pprint
import numpy
from numpy.linalg import linalg

logger = logging.getLogger('simplegoodturingsmoother')

class SimpleGoodTuringSmoother(object):
    """
    "Simple Good-Turing" smoothing with threshold. For N_p's where p>smoothing_threshold, c is not smoothed.

    Uses loglinregression if Nc=0, while calculating Nc+1.
    """
    def __init__(self, smoothing_threshold, frequencies_of_frequencies, unseen_count):
        self._smoothing_threshold = smoothing_threshold
        self._frequencies_of_frequencies = frequencies_of_frequencies
        self._unseen_count = unseen_count

        assert self._smoothing_threshold
        assert self._frequencies_of_frequencies
        assert self._unseen_count
        assert all([i in self._frequencies_of_frequencies.keys() for i in range(1, self._smoothing_threshold + 2)]),\
        'You should provide frequencies for frequencies in range(1, K+1)'
        assert 0 not in self._frequencies_of_frequencies, 'Frequency of frequency 0 is same as unseen_count'

    def initialize(self, plot=False):
        self._calculate_loglinregression_coefficients(plot)

    def _calculate_loglinregression_coefficients(self, plot=False):
        self._loglinregression_m = None
        self._loglinregression_c = None

        cs = sorted(self._frequencies_of_frequencies.keys())    # skip c=0
        Ns = self._frequencies_of_frequencies.values()  # skip c=0
        if not plot:
            m, c = self._loglinregression(cs, Ns)
            self._loglinregression_m = m
            self._loglinregression_c = c
        else:
            m0, c0 = self._linregression(cs, Ns)
            m1, c1 = self._loglinregression(cs, Ns)

            x0 = numpy.array(cs)
            y0 = numpy.array(Ns)

            x1 = numpy.log(numpy.array(cs))
            y1 = numpy.log(numpy.array(Ns))

            import matplotlib.pyplot as plt

            plt.plot(x0, y0, 'o', label='Original data', markersize=10)
            plt.plot(x0, m0 * x0 + c0, 'r', label='Lin fitted line, m={}, c={}'.format(m0, c0))
            plt.legend()
            plt.show()

            plt.plot(x1, y1, 'o', label='Log original data', markersize=10)
            plt.plot(x1, m1 * x1 + c1, 'r', label='Loglin fitted line, m={}, c={}'.format(m1, c1))
            plt.legend()
            plt.show()

            self._loglinregression_m = m1
            self._loglinregression_c = c1


    def _loglinregression(self, x, y):
        log_x = numpy.log(x)
        log_y = numpy.log(y)
        log_y[numpy.isinf(log_y)] = 0.0

        m, c = self._linregression(log_x, log_y)
        # if slope (m) is bigger than -1, then it is not log linear. but do nothing about it
        return m, c

    def _linregression(self, x, y):
        m, c = linalg.lstsq(numpy.vstack([x, numpy.ones(len(x))]).T, y)[0]
        return m, c

    def smooth(self, count):
        K = self._smoothing_threshold
        smoothed_count = 0

        if count == 0:
            # total probability of unseen (from definition) : N1 / N
            # total count of unseen : (N1 / N) * N = N1
            # since we're not calculating the probability, but the estimated count:
            # count of _one_ unseen : N1 / N0
            smoothed_count = (self._frequencies_of_frequencies[1] / self._unseen_count)
        elif count <= K:        # apply smoothing up to K. for bigger, the result is reliable enough
            N_c = self._frequencies_of_frequencies[count]
            N_c_1 = self._frequencies_of_frequencies[count + 1]
            N_k_1 = self._frequencies_of_frequencies[K + 1]
            N_1 = self._frequencies_of_frequencies[1]

            if logger.isEnabledFor(logging.DEBUG):
                Nc_values = {
                    'N_{}'.format(count): N_c,
                    'N_{}_1'.format(count): N_c_1,
                    'N_k_1': N_k_1,
                    'N_1': N_1,
                    }
                logger.debug("  Nc values without loglin mapping " + pprint.pformat(Nc_values))

            N_c = self._map_c_to_Nc(count) if N_c == 0 else N_c
            N_c_1 = self._map_c_to_Nc(count + 1) if N_c_1 == 0 else N_c_1
            N_k_1 = self._map_c_to_Nc(K + 1) if N_k_1 == 0 else N_k_1
            N_1 = self._map_c_to_Nc(1) if N_1 == 0 else N_1

            if logger.isEnabledFor(logging.DEBUG):
                Nc_values = {
                    'N_{}'.format(count): N_c,
                    'N_{}'.format(count + 1): N_c_1,
                    'N_k_1': N_k_1,
                    'N_1': N_1,
                    }
                logger.debug("  Nc values with loglin mapping      " + pprint.pformat(Nc_values))

            a = (N_c_1 / N_c)
            b = (K + 1) * N_k_1 / N_1

            smoothed_count = ((count + 1) * a - count * b) / (1 - b)
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug("  a={}, b={}, smoothed_count={}".format(a, b, smoothed_count))

        else:
            smoothed_count = count
            #        below is normal Good Turing.
        #        else:
        #            N_c = self._frequencies_of_frequencies[count]
        #            N_c_1 = self._frequencies_of_frequencies[count + 1]
        #
        #            N_c = self._map_c_to_Nc(count) if N_c == 0 else N_c
        #            N_c_1 = self._map_c_to_Nc(count + 1) if N_c_1 == 0 else N_c_1
        #
        #            smoothed_count = (count + 1) * N_c_1 / N_c
        #
        #        logger.debug(" Smoothed_count={}".format(smoothed_count))

        return smoothed_count

    def _map_c_to_Nc(self, count):
        m = self._loglinregression_m
        c = self._loglinregression_c
        val = (c + m * numpy.log(count)) if count != 0 else c
        Nc = numpy.exp([val])[0]

        return Nc