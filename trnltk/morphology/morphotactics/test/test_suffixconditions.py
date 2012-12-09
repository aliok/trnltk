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
from mock import Mock
from trnltk.morphology.model.lexeme import LexemeAttribute
from trnltk.morphology.contextless.parser.parser import SuffixFormApplication
from trnltk.morphology.morphotactics.suffixconditions import comes_after, has_lexeme_attributes
from trnltk.morphology.morphotactics.basicsuffixgraph import Suffix
from trnltk.morphology.model.morpheme import SuffixForm, Transition

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

    def test_comes_after_with_forms(self):
        s1 = Suffix("S-1")
        s2 = Suffix("S-2")
        f11 = 'a'
        f12 = 'b'
        f21 = 'c'

        self.assert_suffixes_matches    ( comes_after(s1, f11), [(s1, f11)])
        self.assert_suffixes_matches    ( comes_after(s1     ), [(s1, f11)])
        self.assert_suffixes_matches_not(~comes_after(s1, f11), [(s1, f11)])
        self.assert_suffixes_matches_not(~comes_after(s1     ), [(s1, f11)])

        self.assert_suffixes_matches    ( comes_after(s1, f11), [(s1, f11), (s1, f12)])
        self.assert_suffixes_matches    (~comes_after(s2, f21), [(s1, f11), (s1, f12)])

    def test_requires_lexeme_attributes(self):
        C_T = LexemeAttribute.Causative_t
        C_AR = LexemeAttribute.Causative_Ar

        self.assert_lexeme_attr_matches_not(has_lexeme_attributes([C_T]), None)
        self.assert_lexeme_attr_matches_not(has_lexeme_attributes([C_T]), [])
        self.assert_lexeme_attr_matches_not(has_lexeme_attributes([C_T]), [C_AR])
        self.assert_lexeme_attr_matches    (has_lexeme_attributes([C_T]), [C_T])
        self.assert_lexeme_attr_matches    (has_lexeme_attributes([C_T]), [C_T, C_AR])

        self.assert_lexeme_attr_matches_not(has_lexeme_attributes([C_T, C_AR]), None)
        self.assert_lexeme_attr_matches_not(has_lexeme_attributes([C_T, C_AR]), [])
        self.assert_lexeme_attr_matches_not(has_lexeme_attributes([C_T, C_AR]), [C_AR])
        self.assert_lexeme_attr_matches_not(has_lexeme_attributes([C_T, C_AR]), [C_T])
        self.assert_lexeme_attr_matches    (has_lexeme_attributes([C_T, C_AR]), [C_T, C_AR])

        self.assert_lexeme_attr_matches    (~has_lexeme_attributes([C_T, C_AR]), [C_T])
        self.assert_lexeme_attr_matches_not(~has_lexeme_attributes([C_T, C_AR]), [C_T, C_AR])


    def assert_suffixes_matches(self, condition, suffix_form_tuples):
        self.do_assert_suffixes_matches(condition, suffix_form_tuples, True)

    def assert_suffixes_matches_not(self, condition, suffix_form_tuples):
        self.do_assert_suffixes_matches(condition, suffix_form_tuples, False)

    def do_assert_suffixes_matches(self, condition, suffix_form_tuples, val):
        suffixes = []
        transitions = []

        suffix_form_tuples = [] if not suffix_form_tuples else suffix_form_tuples

        for suffix_form_tuple in suffix_form_tuples:
            if type(suffix_form_tuple) is tuple:
                suffix =  suffix_form_tuple[0]
                suffix_form_str =  suffix_form_tuple[1] if len(suffix_form_tuple)==2 else None
                suffix_form = SuffixForm(suffix_form_str)
                suffix_form.suffix = suffix
                transitions.append(Transition(None, SuffixFormApplication(suffix_form, None, None), None))

                suffixes.append(suffix)
            else:
                suffixes.append(suffix_form_tuple)

        mock = Mock()
        mock.get_transitions_since_derivation_suffix.return_value=transitions
        mock.get_suffixes_since_derivation_suffix.return_value=suffixes

        assert_that(condition.is_satisfied_by(mock), equal_to(val))


    def assert_lexeme_attr_matches(self, condition, attrs):
        self.do_assert_lexeme_attr_matches(condition, attrs, True)

    def assert_lexeme_attr_matches_not(self, condition, attrs):
        self.do_assert_lexeme_attr_matches(condition, attrs, False)

    def do_assert_lexeme_attr_matches(self, condition, attrs, val):
        morpheme_container = Mock()
        root = Mock()
        lexeme = Mock()

        morpheme_container.get_root.return_value = root
        morpheme_container.get_transitions.return_value = []
        root.lexeme = lexeme
        lexeme.attributes = attrs

        morpheme_container.get_suffixes_since_derivation_suffix.return_value=[]

        assert_that(condition.is_satisfied_by(morpheme_container), equal_to(val))

if __name__ == '__main__':
    unittest.main()