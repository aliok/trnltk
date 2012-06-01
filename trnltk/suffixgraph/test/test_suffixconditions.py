# coding=utf-8
import unittest
from hamcrest import *
from mock import Mock
from trnltk.suffixgraph.suffixconditions import comes_after
from trnltk.suffixgraph.suffixgraph import Suffix

class SuffixConditionsTest(unittest.TestCase):

    def test_comes_after(self):
        s1 = Suffix("S-1")
        s2 = Suffix("S-2")

        self.assert_suffixes_matches_not(comes_after(s2), None)
        self.assert_suffixes_matches    (comes_after(s2), [s2])
        self.assert_suffixes_matches_not(comes_after(s2), [s1])
        self.assert_suffixes_matches    (comes_after(s2), [s1, s2])

    def test_logical_operators(self):
        s1 = Suffix("S-1")
        s2 = Suffix("S-2")

        self.assert_suffixes_matches_not(comes_after(s1) & comes_after(s2), None)
        self.assert_suffixes_matches_not(comes_after(s1) | comes_after(s1), None)

        self.assert_suffixes_matches_not(~comes_after(s1), [s1])
        self.assert_suffixes_matches    (~comes_after(s1), [s2])
        self.assert_suffixes_matches_not(~comes_after(s1), [s1, s2])

        self.assert_suffixes_matches_not(comes_after(s1) & comes_after(s2), [s1])
        self.assert_suffixes_matches_not(comes_after(s1) & comes_after(s2), [s2])
        self.assert_suffixes_matches    (comes_after(s1) & comes_after(s2), [s1, s2])

        self.assert_suffixes_matches    (comes_after(s1) | comes_after(s2), [s1])
        self.assert_suffixes_matches    (comes_after(s1) | comes_after(s2), [s2])
        self.assert_suffixes_matches    (comes_after(s1) | comes_after(s2), [s1, s2])

        self.assert_suffixes_matches    (comes_after(s1) | ~comes_after(s2), [s1])
        self.assert_suffixes_matches_not(comes_after(s1) | ~comes_after(s2), [s2])
        self.assert_suffixes_matches    (comes_after(s1) | ~comes_after(s2), [s1, s2])

        self.assert_suffixes_matches    (comes_after(s1) & ~comes_after(s2), [s1])
        self.assert_suffixes_matches_not(comes_after(s1) & ~comes_after(s2), [s2])
        self.assert_suffixes_matches_not(comes_after(s1) & ~comes_after(s2), [s1, s2])

        self.assert_suffixes_matches_not(~comes_after(s1) | comes_after(s2), [s1])
        self.assert_suffixes_matches    (~comes_after(s1) | comes_after(s2), [s2])
        self.assert_suffixes_matches    (~comes_after(s1) | comes_after(s2), [s1, s2])

        self.assert_suffixes_matches_not(~comes_after(s1) & comes_after(s2), [s1])
        self.assert_suffixes_matches    (~comes_after(s1) & comes_after(s2), [s2])
        self.assert_suffixes_matches_not(~comes_after(s1) & comes_after(s2), [s1, s2])

        self.assert_suffixes_matches    (~comes_after(s1) | ~comes_after(s2), [s1])
        self.assert_suffixes_matches    (~comes_after(s1) | ~comes_after(s2), [s2])
        self.assert_suffixes_matches_not(~comes_after(s1) | ~comes_after(s2), [s1, s2])

        self.assert_suffixes_matches_not(~comes_after(s1) & ~comes_after(s2), [s1])
        self.assert_suffixes_matches_not(~comes_after(s1) & ~comes_after(s2), [s2])
        self.assert_suffixes_matches_not(~comes_after(s1) & ~comes_after(s2), [s1, s2])

    def assert_suffixes_matches(self, condition, suffixes):
        self.do_assert_suffixes_matches(condition, suffixes, True)

    def assert_suffixes_matches_not(self, condition, suffixes):
        self.do_assert_suffixes_matches(condition, suffixes, False)

    def do_assert_suffixes_matches(self, condition, suffixes, val):
        mock = Mock()
        mock.get_suffixes_since_derivation_suffix.return_value=suffixes

        assert_that(condition.matches(mock), equal_to(val))

if __name__ == '__main__':
    unittest.main()