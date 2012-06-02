# coding=utf-8
import unittest
from hamcrest import *
from mock import Mock
from trnltk.stem.dictionaryitem import RootAttribute
from trnltk.suffixgraph.suffixconditions import comes_after, requires_root_attributes
from trnltk.suffixgraph.suffixgraph import Suffix

class SuffixConditionsTest(unittest.TestCase):

    def test_comes_after(self):
        s1 = Suffix("S-1")
        s2 = Suffix("S-2")

        self.assert_suffixes_matches_not(comes_after(s2), None)
        self.assert_suffixes_matches    (comes_after(s2), [s2])
        self.assert_suffixes_matches_not(comes_after(s2), [s1])
        self.assert_suffixes_matches    (comes_after(s2), [s1, s2])

    def test_comes_after_with_logical_operators(self):
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

    def test_requires_root_attributes(self):
        C_T = RootAttribute.Causative_t
        C_AR = RootAttribute.Causative_Ar

        self.assert_root_attr_matches_not(requires_root_attributes([C_T]), None)
        self.assert_root_attr_matches_not(requires_root_attributes([C_T]), [])
        self.assert_root_attr_matches_not(requires_root_attributes([C_T]), [C_AR])
        self.assert_root_attr_matches    (requires_root_attributes([C_T]), [C_T])
        self.assert_root_attr_matches    (requires_root_attributes([C_T]), [C_T, C_AR])

        self.assert_root_attr_matches_not(requires_root_attributes([C_T, C_AR]), None)
        self.assert_root_attr_matches_not(requires_root_attributes([C_T, C_AR]), [])
        self.assert_root_attr_matches_not(requires_root_attributes([C_T, C_AR]), [C_AR])
        self.assert_root_attr_matches_not(requires_root_attributes([C_T, C_AR]), [C_T])
        self.assert_root_attr_matches    (requires_root_attributes([C_T, C_AR]), [C_T, C_AR])

        self.assert_root_attr_matches    (~requires_root_attributes([C_T, C_AR]), [C_T])
        self.assert_root_attr_matches_not(~requires_root_attributes([C_T, C_AR]), [C_T, C_AR])


    def assert_suffixes_matches(self, condition, suffixes):
        self.do_assert_suffixes_matches(condition, suffixes, True)

    def assert_suffixes_matches_not(self, condition, suffixes):
        self.do_assert_suffixes_matches(condition, suffixes, False)

    def do_assert_suffixes_matches(self, condition, suffixes, val):
        mock = Mock()
        mock.get_suffixes_since_derivation_suffix.return_value=suffixes

        assert_that(condition.matches(mock), equal_to(val))


    def assert_root_attr_matches(self, condition, attrs):
        self.do_assert_root_attr_matches(condition, attrs, True)

    def assert_root_attr_matches_not(self, condition, attrs):
        self.do_assert_root_attr_matches(condition, attrs, False)

    def do_assert_root_attr_matches(self, condition, attrs, val):
        parse_token = Mock()
        stem = Mock()
        dictionary_item = Mock()

        parse_token.stem = stem
        stem.dictionary_item = dictionary_item
        dictionary_item.attributes = attrs

        assert_that(condition.matches(parse_token), equal_to(val))

if __name__ == '__main__':
    unittest.main()