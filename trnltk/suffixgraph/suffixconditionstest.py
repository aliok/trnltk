# coding=utf-8
import unittest
from hamcrest import *
from trnltk.suffixgraph.suffixconditions import comes_after
from trnltk.suffixgraph.suffixgraph import Suffix

def assert_matches(condition, suffixes):
    assert_that(condition.matches(suffixes), equal_to(True))

def assert_matches_not(condition, suffixes):
    assert_that(condition.matches(suffixes), equal_to(False))

class SuffixConditionsTest(unittest.TestCase):
    def test_comes_after(self):
        s1 = Suffix("S-1")
        s2 = Suffix("S-2")

        assert_matches_not(comes_after(s2), None)
        assert_matches    (comes_after(s2), [s2])
        assert_matches_not(comes_after(s2), [s1])
        assert_matches    (comes_after(s2), [s1, s2])

    def test_logical_operators(self):
        s1 = Suffix("S-1")
        s2 = Suffix("S-2")

        assert_matches_not(comes_after(s1) & comes_after(s2), None)
        assert_matches_not(comes_after(s1) | comes_after(s1), None)

        assert_matches_not(~comes_after(s1), [s1])
        assert_matches    (~comes_after(s1), [s2])
        assert_matches_not(~comes_after(s1), [s1, s2])

        assert_matches_not(comes_after(s1) & comes_after(s2), [s1])
        assert_matches_not(comes_after(s1) & comes_after(s2), [s2])
        assert_matches    (comes_after(s1) & comes_after(s2), [s1, s2])

        assert_matches    (comes_after(s1) | comes_after(s2), [s1])
        assert_matches    (comes_after(s1) | comes_after(s2), [s2])
        assert_matches    (comes_after(s1) | comes_after(s2), [s1, s2])

        assert_matches    (comes_after(s1) | ~comes_after(s2), [s1])
        assert_matches_not(comes_after(s1) | ~comes_after(s2), [s2])
        assert_matches    (comes_after(s1) | ~comes_after(s2), [s1, s2])

        assert_matches    (comes_after(s1) & ~comes_after(s2), [s1])
        assert_matches_not(comes_after(s1) & ~comes_after(s2), [s2])
        assert_matches_not(comes_after(s1) & ~comes_after(s2), [s1, s2])

        assert_matches_not(~comes_after(s1) | comes_after(s2), [s1])
        assert_matches    (~comes_after(s1) | comes_after(s2), [s2])
        assert_matches    (~comes_after(s1) | comes_after(s2), [s1, s2])

        assert_matches_not(~comes_after(s1) & comes_after(s2), [s1])
        assert_matches    (~comes_after(s1) & comes_after(s2), [s2])
        assert_matches_not(~comes_after(s1) & comes_after(s2), [s1, s2])

        assert_matches    (~comes_after(s1) | ~comes_after(s2), [s1])
        assert_matches    (~comes_after(s1) | ~comes_after(s2), [s2])
        assert_matches_not(~comes_after(s1) | ~comes_after(s2), [s1, s2])

        assert_matches_not(~comes_after(s1) & ~comes_after(s2), [s1])
        assert_matches_not(~comes_after(s1) & ~comes_after(s2), [s2])
        assert_matches_not(~comes_after(s1) & ~comes_after(s2), [s1, s2])

if __name__ == '__main__':
    unittest.main()