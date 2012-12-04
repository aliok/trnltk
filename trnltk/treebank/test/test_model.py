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
import unittest
from hamcrest import *
from trnltk.treebank.model import HierarchicalIndex

class HierarchicalIndexTest(unittest.TestCase):
    def test_index_with_sample_case_for_depth_2(self):
        idx = HierarchicalIndex(2)

        # A
        idx.insert(1, 'A', 'X')
        idx.insert(2, 'A', 'X')
        idx.insert(3, 'A', 'X')

        idx.insert(4, 'A', 'Y')
        idx.insert(5, 'A', 'Y')

        idx.insert(10, 'A', 'Z')
        idx.insert(11, 'A', 'Z')

        #B
        idx.insert(6, 'B', 'X')
        idx.insert(7, 'B', 'X')

        idx.insert(8, 'B', 'Y')

        assert_that(idx.get('A'), equal_to([1, 2, 3, 4, 5, 10, 11]))
        assert_that(idx.get('A', 'Y'), equal_to([4, 5]))
        assert_that(idx.get('B'), equal_to([6, 7, 8]))
        assert_that(idx.get('B', 'X'), equal_to([6, 7]))


    def test_index_with_sample_case_for_depth_3(self):
        idx = HierarchicalIndex(3)

        # A
        idx.insert(1, 'A', 'X', 'i')
        idx.insert(2, 'A', 'X', 'ii')
        idx.insert(3, 'A', 'X', 'ii')

        idx.insert(4, 'A', 'Y', 'i')
        idx.insert(5, 'A', 'Y', 'ii')

        idx.insert(10, 'A', 'Z', 'ii')
        idx.insert(11, 'A', 'Z', 'iii')

        #B
        idx.insert(6, 'B', 'X', 'ii')
        idx.insert(7, 'B', 'X', 'iii')

        idx.insert(8, 'B', 'Y', 'i')

        #same queries with case for depth 2
        assert_that(idx.get('A'), equal_to([1, 2, 3, 4, 5, 10, 11]))
        assert_that(idx.get('A', 'Y'), equal_to([4, 5]))
        assert_that(idx.get('B'), equal_to([6, 7, 8]))
        assert_that(idx.get('B', 'X'), equal_to([6, 7]))

        #new queries
        assert_that(idx.get('B', 'X', 'ii'), equal_to([6]))
        assert_that(idx.get('A', 'X', 'ii'), equal_to([2, 3]))

    def test_index_should_not_init_with_wrong_args(self):
        self.assertRaises(AssertionError, lambda: HierarchicalIndex(depth=1))
        self.assertRaises(AssertionError, lambda: HierarchicalIndex(depth=0))
        self.assertRaises(AssertionError, lambda: HierarchicalIndex(depth='a'))
        self.assertRaises(AssertionError, lambda: HierarchicalIndex(depth=list()))
        self.assertRaises(AssertionError, lambda: HierarchicalIndex(depth=2.3))


    def test_index_should_validate_depth_in_operations(self):
        # depth=2
        idx = HierarchicalIndex(2)

        assert_that(idx.get('A'), has_length(0))
        assert_that(idx.get('A', 'X'), has_length(0))
        self.assertRaises(AssertionError, lambda: idx.get('A', 'X', 'i'))

        self.assertRaises(AssertionError, lambda: idx.insert(1))
        self.assertRaises(AssertionError, lambda: idx.insert(1, 'A'))
        idx.insert(1, 'A', 'X')             # should not raise anything
        self.assertRaises(AssertionError, lambda: idx.insert(1, 'A', 'X', 'i'))

        assert_that(idx.get('A', 'X'), equal_to([1]))

        # depth=3
        idx = HierarchicalIndex(3)

        assert_that(idx.get('A'), has_length(0))
        assert_that(idx.get('A', 'X'), has_length(0))
        assert_that(idx.get('A', 'X', 'i'), has_length(0))
        self.assertRaises(AssertionError, lambda: idx.get('A', 'X', 'i', '1'))

        self.assertRaises(AssertionError, lambda: idx.insert(1))
        self.assertRaises(AssertionError, lambda: idx.insert(1, 'A'))
        self.assertRaises(AssertionError, lambda: idx.insert(1, 'A', 'X'))
        idx.insert(1, 'A', 'X', 'i')        # should not raise anything
        self.assertRaises(AssertionError, lambda: idx.insert(1, 'A', 'X', 'i', 'a'))

        assert_that(idx.get('A', 'X', 'i'), equal_to([1]))

        # depth=N
        N = 100
        idx = HierarchicalIndex(N)
        for i in range(1, N + 1):
            assert_that(idx.get(*range(0, i)), has_length(0))   # try calling idx.get(0,0,0,0.....0) with N items at last iteration
        self.assertRaises(AssertionError, lambda: idx.get(*range(0, N + 1)))

        for i in range(1, N):
            self.assertRaises(AssertionError, lambda: idx.insert(1, *range(0, i)))
        idx.insert(1, *range(0, N))             # should not raise anything

        assert_that(idx.get(*range(0, N)), equal_to([1]))

if __name__ == '__main__':
    unittest.main()
