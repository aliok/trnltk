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
"""
There is no verification -yet- in test of this class.
The tests are there for making sure there is no run time exceptions
"""
import logging
import unittest
from trnltk.morphology.contextful.likelihoodmetrics.hidden.simplegoodturing import logger, SimpleGoodTuringSmoother

K = 5

class SimpleGoodTuringSmootherTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(SimpleGoodTuringSmootherTest, cls).setUpClass()

    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        logger.setLevel(logging.DEBUG)


    def test_smoother_assertions(self):
        self.assertRaises(AssertionError, lambda : SimpleGoodTuringSmoother(0, {1:2}, 3))
        self.assertRaises(AssertionError, lambda : SimpleGoodTuringSmoother(2, {}, 2))
        self.assertRaises(AssertionError, lambda : SimpleGoodTuringSmoother(2, {1:2}, 0))

        self.assertRaises(AssertionError, lambda : SimpleGoodTuringSmoother(1, {0:1}, 3))
        self.assertRaises(AssertionError, lambda : SimpleGoodTuringSmoother(1, {1:2}, 1))
        self.assertRaises(AssertionError, lambda : SimpleGoodTuringSmoother(1, {1:2}, 2))
        self.assertRaises(AssertionError, lambda : SimpleGoodTuringSmoother(2, {1:2, 2:3}, 2))
        self.assertRaises(AssertionError, lambda : SimpleGoodTuringSmoother(2, {1:2, 2:3}, 3))


    def test_with_small_values(self):
        smoother = SimpleGoodTuringSmoother(K, {1: 10, 2: 5, 3: 3, 4: 2, 5: 1, 6: 0}, 100)
        smoother.initialize()

        for i in range(0, K + 5):
            logger.info("c_{} : {}, \t c*_{} : {}".format(i, i, i, smoother.smooth(i)))

    def test_with_larger_values(self):
        smoother = SimpleGoodTuringSmoother(K, {1: 268, 2: 112, 3: 70, 4: 41, 5: 24, 6: 14, 7: 15, 400: 1, 1918: 1}, 1000)
        smoother.initialize()

        for i in range(0, K + 5):
            logger.info("c_{} : {}, \t c*_{} : {}".format(i, i, i, smoother.smooth(i)))

    def test_with_larger_values_sc_2(self):
        smoother = SimpleGoodTuringSmoother(K, {1: 16181, 2: 2213, 3: 870, 4: 431, 5: 304, 6: 202}, 2111251811)
        smoother.initialize()

        for i in range(0, K + 5):
            logger.info("c_{} : {}, \t c*_{} : {}".format(i, i, i, smoother.smooth(i)))

    def test_with_zero_frequencies_in_between(self):
        smoother = SimpleGoodTuringSmoother(K, {1: 268, 2: 0, 3: 70, 4: 0, 5: 24, 6: 14, 7: 15, 400: 1, 1918: 1}, 1000)
        smoother.initialize()

        for i in range(0, K + 5):
            logger.info("c_{} : {}, \t c*_{} : {}".format(i, i, i, smoother.smooth(i)))


if __name__ == '__main__':
    unittest.main()
