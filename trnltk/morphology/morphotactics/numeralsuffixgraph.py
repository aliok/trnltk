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
from trnltk.morphology.model.graphmodel import State
from trnltk.morphology.model.lexeme import  SyntacticCategory, SecondarySyntacticCategory
from trnltk.morphology.morphotactics.suffixgraph import  SuffixGraphDecorator

class NumeralSuffixGraph(SuffixGraphDecorator):

    def __init__(self, decorated):
        super(NumeralSuffixGraph, self).__init__(decorated)

    def register_states(self):
        self.NUMERAL_CARDINAL_ROOT = self._register_state("NUMERAL_CARDINAL_ROOT", State.TRANSFER, SyntacticCategory.NUMERAL)
        self.NUMERAL_CARDINAL_DERIV = self._register_state("NUMERAL_CARDINAL_DERIV", State.DERIVATIONAL, SyntacticCategory.NUMERAL)

        self.NUMERAL_DIGIT_CARDINAL_ROOT = self._register_state("NUMERAL_DIGIT_CARDINAL_ROOT", State.TRANSFER, SyntacticCategory.NUMERAL)

        self.NUMERAL_ORDINAL_ROOT = self._register_state("NUMERAL_ORDINAL_ROOT", State.TRANSFER, SyntacticCategory.NUMERAL)
        self.NUMERAL_ORDINAL_DERIV = self._register_state("NUMERAL_ORDINAL_DERIV", State.DERIVATIONAL, SyntacticCategory.NUMERAL)

        self.DECORATED_ADJECTIVE_ROOT = self.get_state(u'ADJECTIVE_ROOT')

    def _find_default_root_state(self, root):
        """
        Return the initial state for root based on primary and secondary syntactic category of it.
        @type root: Root
        @rtype: State
        """
        if root.lexeme.syntactic_category==SyntacticCategory.NUMERAL and root.lexeme.secondary_syntactic_category==SecondarySyntacticCategory.DIGITS:
            return self.NUMERAL_DIGIT_CARDINAL_ROOT
        elif root.lexeme.syntactic_category==SyntacticCategory.NUMERAL and root.lexeme.secondary_syntactic_category==SecondarySyntacticCategory.CARD:
            return self.NUMERAL_CARDINAL_ROOT
        elif root.lexeme.syntactic_category==SyntacticCategory.NUMERAL and root.lexeme.secondary_syntactic_category==SecondarySyntacticCategory.ORD:
            return self.NUMERAL_ORDINAL_ROOT

        return self._decorated._find_default_root_state(root)

    def register_suffixes(self):

        #############  Free _transitions
        self.NUMERAL_CARDINAL_ROOT        .add_out_suffix(self._register_free_transition_suffix("Numeral_Free_Transition_1"  ), self.NUMERAL_CARDINAL_DERIV)
        self.NUMERAL_ORDINAL_ROOT         .add_out_suffix(self._register_free_transition_suffix("Numeral_Free_Transition_2"  ), self.NUMERAL_ORDINAL_DERIV)

        self.NUMERAL_DIGIT_CARDINAL_ROOT  .add_out_suffix(self._register_free_transition_suffix("Digits_Free_Transition_1"   ), self.NUMERAL_CARDINAL_DERIV)

        self.NUMERAL_CARDINAL_DERIV       .add_out_suffix(self._register_zero_transition_suffix("Numeral_Zero_Transition_1"  ), self.DECORATED_ADJECTIVE_ROOT)
        self.NUMERAL_ORDINAL_DERIV        .add_out_suffix(self._register_zero_transition_suffix("Numeral_Zero_Transition_2"  ), self.DECORATED_ADJECTIVE_ROOT)

        ########### Cardinal numbers to Adjective derivations
        self.NumbersOf = self._register_suffix("NumbersOf")
        self.OfUnit_Number = self._register_suffix("OfUnit_Number", pretty_name='OfUnit')

        ########### Cardinal digits suffixes
        self.Apos_Digit = self._register_suffix("Apos_Digit", pretty_name="Apos")

    def create_suffix_edges(self):
        self._register_numeral_suffixes()

    def _register_numeral_suffixes(self):
        self._register_cardinal_to_adjective_suffixes()
        self._register_digits_suffixes()

    def _register_cardinal_to_adjective_suffixes(self):
        self.NUMERAL_CARDINAL_DERIV.add_out_suffix(self.NumbersOf, self.DECORATED_ADJECTIVE_ROOT)
        self.NumbersOf.add_suffix_form(u"lArcA")

        self.NUMERAL_CARDINAL_DERIV.add_out_suffix(self.OfUnit_Number, self.DECORATED_ADJECTIVE_ROOT)
        self.OfUnit_Number.add_suffix_form(u"lIk")

    def _register_digits_suffixes(self):
        self.NUMERAL_DIGIT_CARDINAL_ROOT.add_out_suffix(self.Apos_Digit, self.NUMERAL_CARDINAL_DERIV)
        self.Apos_Digit.add_suffix_form(u"'")
