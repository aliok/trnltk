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
from trnltk.morphology.model.lexeme import SyntacticCategory, SecondarySyntacticCategory
from trnltk.morphology.morphotactics.suffixgraph import SuffixGraphDecorator

class ProperNounSuffixGraph(SuffixGraphDecorator):

    def __init__(self, decorated):
        super(ProperNounSuffixGraph, self).__init__(decorated)


    def register_states(self):
        self.PROPER_NOUN_ROOT            = self._register_state("PROPER_NOUN_ROOT",            State.TRANSFER, SyntacticCategory.NOUN)
        self.PROPER_NOUN_WITH_AGREEMENT  = self._register_state("PROPER_NOUN_WITH_AGREEMENT",  State.TRANSFER, SyntacticCategory.NOUN)
        self.PROPER_NOUN_WITH_POSSESSION = self._register_state("PROPER_NOUN_WITH_POSSESSION", State.TRANSFER, SyntacticCategory.NOUN)
        self.PROPER_NOUN_WITH_CASE       = self._register_state("PROPER_NOUN_WITH_CASE",       State.TRANSFER, SyntacticCategory.NOUN)
        self.PROPER_NOUN_TERMINAL        = self._register_state("PROPER_NOUN_TERMINAL",        State.TERMINAL, SyntacticCategory.NOUN)


        # from decorated
        self.DECORATED_NOUN_ROOT = self.get_state('NOUN_ROOT')

    def _find_default_root_state(self, root):
        if root.lexeme.syntactic_category==SyntacticCategory.NOUN and root.lexeme.secondary_syntactic_category==SecondarySyntacticCategory.PROPER_NOUN:
            return self.PROPER_NOUN_ROOT
        elif root.lexeme.syntactic_category==SyntacticCategory.NOUN and root.lexeme.secondary_syntactic_category==SecondarySyntacticCategory.ABBREVIATION:
            return self.PROPER_NOUN_ROOT

        return self._decorated._find_default_root_state(root)


    def register_suffixes(self):
        # free transitions
        self.PROPER_NOUN_WITH_CASE       .add_out_suffix(self._register_free_transition_suffix("Proper_Noun_Free_Transition_1"),  self.PROPER_NOUN_TERMINAL)

        # free transitions, but named
        self.A3Sg_Proper_Noun = self._register_suffix("A3Sg_Proper_Noun", pretty_name="A3sg")
        self.Pnon_Proper_Noun = self._register_suffix("Pnon_Proper_Noun", pretty_name="Pnon")
        self.Nom_Proper_Noun  = self._register_suffix("Nom_Proper_Noun", pretty_name="Nom")


        self.Apos_Proper_Noun = self._register_suffix("Apos_Proper_Noun", pretty_name="Apos")

    def create_suffix_edges(self):
        self.PROPER_NOUN_ROOT            .add_out_suffix(self.A3Sg_Proper_Noun, self.PROPER_NOUN_WITH_AGREEMENT)
        self.A3Sg_Proper_Noun.add_suffix_form(u"")

        self.PROPER_NOUN_WITH_AGREEMENT  .add_out_suffix(self.Pnon_Proper_Noun, self.PROPER_NOUN_WITH_POSSESSION)
        self.Pnon_Proper_Noun.add_suffix_form(u"")

        self.PROPER_NOUN_WITH_POSSESSION .add_out_suffix(self.Nom_Proper_Noun,  self.PROPER_NOUN_WITH_CASE)
        self.Nom_Proper_Noun.add_suffix_form(u"")

        self.PROPER_NOUN_ROOT.add_out_suffix(self.Apos_Proper_Noun, self.DECORATED_NOUN_ROOT)
        self.Apos_Proper_Noun.add_suffix_form(u"'")