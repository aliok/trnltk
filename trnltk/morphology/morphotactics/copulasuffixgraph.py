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
from trnltk.morphology.model.lexeme import SyntacticCategory
from trnltk.morphology.morphotactics.suffixconditions import comes_after, doesnt_come_after
from trnltk.morphology.model.morpheme import *
from trnltk.morphology.morphotactics.suffixgraph import SuffixGraphDecorator

class CopulaSuffixGraph(SuffixGraphDecorator):

    def __init__(self, decorated):
        super(CopulaSuffixGraph, self).__init__(decorated)


    def register_states(self):
        self.NOUN_COPULA = self._register_state("NOUN_COPULA", State.DERIVATIONAL, SyntacticCategory.NOUN)
        self.ADJECTIVE_COPULA = self._register_state("ADJECTIVE_COPULA", State.DERIVATIONAL, SyntacticCategory.ADJECTIVE)
        self.ADVERB_COPULA = self._register_state("ADVERB_COPULA", State.DERIVATIONAL, SyntacticCategory.ADVERB)
        self.PRONOUN_COPULA = self._register_state("PRONOUN_COPULA", State.DERIVATIONAL, SyntacticCategory.PRONOUN)
        self.VERB_DEGIL_ROOT = self._register_state("VERB_DEGIL_ROOT", State.TRANSFER, SyntacticCategory.VERB)

        self.VERB_COPULA_WITHOUT_TENSE = self._register_state("VERB_COPULA_WITHOUT_TENSE", State.TRANSFER, SyntacticCategory.VERB)
        self.VERB_COPULA_WITHOUT_TENSE_DERIV = self._register_state("VERB_COPULA_WITHOUT_TENSE_DERIV", State.DERIVATIONAL, SyntacticCategory.VERB)
        self.VERB_COPULA_WITH_TENSE = self._register_state("VERB_COPULA_WITH_TENSE", State.TRANSFER, SyntacticCategory.VERB)#

        # from decorated
        self.DECORATED_ADJECTIVE_DERIV = self.get_state('ADJECTIVE_DERIV')
        self.DECORATED_ADVERB_ROOT = self.get_state('ADVERB_ROOT')

        self.DECORATED_NOUN_TERMINAL_TRANSFER       = self.get_state('NOUN_TERMINAL_TRANSFER')
        self.DECORATED_ADJECTIVE_TERMINAL_TRANSFER  = self.get_state('ADJECTIVE_TERMINAL_TRANSFER')
        self.DECORATED_ADVERB_TERMINAL_TRANSFER     = self.get_state('ADVERB_TERMINAL_TRANSFER')
        self.DECORATED_PRONOUN_TERMINAL_TRANSFER    = self.get_state('PRONOUN_TERMINAL_TRANSFER')
        self.DECORATED_VERB_TERMINAL_TRANSFER       = self.get_state('VERB_TERMINAL_TRANSFER')

        self.DECORATED_QUESTION_WITH_AGREEMENT      = self.get_state('QUESTION_WITH_AGREEMENT')

    def _find_default_root_state(self, root):
        if root.lexeme.syntactic_category==SyntacticCategory.VERB and root.str==u'değil':
            return self.VERB_DEGIL_ROOT

        return self._decorated._find_default_root_state(root)


    def register_suffixes(self):
        self.DECORATED_NOUN_TERMINAL_TRANSFER      .add_out_suffix(self._register_free_transition_suffix("Noun_Cop_Free_Transition"     ), self.NOUN_COPULA)
        self.DECORATED_ADJECTIVE_TERMINAL_TRANSFER .add_out_suffix(self._register_free_transition_suffix("Adjective_Cop_Free_Transition"), self.ADJECTIVE_COPULA)
        self.DECORATED_ADVERB_TERMINAL_TRANSFER    .add_out_suffix(self._register_free_transition_suffix("Adverb_Cop_Free_Transition"   ), self.ADVERB_COPULA)
        self.DECORATED_PRONOUN_TERMINAL_TRANSFER   .add_out_suffix(self._register_free_transition_suffix("Pronoun_Cop_Free_Transition"  ), self.PRONOUN_COPULA)
        self.VERB_DEGIL_ROOT                       .add_out_suffix(self._register_free_transition_suffix("Verb_Degil_Free_Transition"   ), self.VERB_COPULA_WITHOUT_TENSE)
        self.VERB_COPULA_WITHOUT_TENSE             .add_out_suffix(self._register_free_transition_suffix("Copula_Deriv_Free_Transition" ), self.VERB_COPULA_WITHOUT_TENSE_DERIV)

        self.NOUN_COPULA              .add_out_suffix(self._register_zero_transition_suffix("Noun_Copula_Zero_Transition"     ),   self.VERB_COPULA_WITHOUT_TENSE)
        self.ADJECTIVE_COPULA         .add_out_suffix(self._register_zero_transition_suffix("Adjective_Copula_Zero_Transition"),   self.VERB_COPULA_WITHOUT_TENSE)
        self.ADVERB_COPULA            .add_out_suffix(self._register_zero_transition_suffix("Adverb_Copula_Zero_Transition"   ),   self.VERB_COPULA_WITHOUT_TENSE)
        self.PRONOUN_COPULA           .add_out_suffix(self._register_zero_transition_suffix("Pronoun_Copula_Zero_Transition"  ),   self.VERB_COPULA_WITHOUT_TENSE)

        self.DECORATED_ADJECTIVE_DERIV.add_out_suffix(self._register_zero_transition_suffix("Adjective_Adverb_Zero_Transition"), self.DECORATED_ADVERB_ROOT)

        ############# Copula tenses
        self.Pres_Cop           = self._register_suffix("Pres_Cop", pretty_name="Pres")
        self.Narr_Cop           = self._register_suffix("Narr_Cop", pretty_name="Narr")
        self.Past_Cop           = self._register_suffix("Past_Cop", pretty_name="Past")
        self.Cond_Cop           = self._register_suffix("Cond_Cop", pretty_name="Cond")
        self.Cond_Cop_Secondary = self._register_suffix("Cond_Cop_Secondary", pretty_name="Cond")

        ############# Copula agreements
        self.Copula_Agreements_Group = SuffixGroup('Copula_Agreements_Group')
        self.A1Sg_Cop = self._register_suffix("A1Sg_Cop", self.Copula_Agreements_Group, "A1sg")
        self.A2Sg_Cop = self._register_suffix("A2Sg_Cop", self.Copula_Agreements_Group, "A2sg")
        self.A3Sg_Cop = self._register_suffix("A3Sg_Cop", self.Copula_Agreements_Group, "A3sg")
        self.A1Pl_Cop = self._register_suffix("A1Pl_Cop", self.Copula_Agreements_Group, "A1pl")
        self.A2Pl_Cop = self._register_suffix("A2Pl_Cop", self.Copula_Agreements_Group, "A2pl")
        self.A3Pl_Cop = self._register_suffix("A3Pl_Cop", self.Copula_Agreements_Group, "A3pl")

        ############ Copula tenses to Adverb
        self.While_Cop = self._register_suffix("While_Cop", pretty_name="While")

        ############ Explicit Copula
        self.Cop_Verb = self._register_suffix("Cop_Verb", pretty_name="Cop")
        self.Cop_Ques = self._register_suffix("Cop_Ques", pretty_name="Cop")


        # from decorated
        self.Decorated_Aorist = self.get_suffix(u'Aor')
        self.Decorated_Past   = self.get_suffix(u'Past')
        self.Decorated_Cond = self.get_suffix(u'Cond')
        self.Decorated_Narr_Ques = self.get_suffix(u'Narr_Ques')
        self.Decorated_Pres_Ques = self.get_suffix(u'Pres_Ques')
        self.Decorated_Past_Ques = self.get_suffix(u'Past_Ques')
        self.Decorated_Imp = self.get_suffix(u'Imp')
        self.Decorated_Opt = self.get_suffix(u'Opt')

    def create_suffix_edges(self):
        self._register_copula_tenses()
        self._register_copula_agreements()
        self._register_copula_tenses_to_other_categories()
        self._register_verb_explicit_copula()
        self._register_ques_explicit_copula()

    def _register_copula_tenses(self):
        self.VERB_COPULA_WITHOUT_TENSE.add_out_suffix(self.Pres_Cop, self.VERB_COPULA_WITH_TENSE)
        self.Pres_Cop.add_suffix_form(u"")

        self.VERB_COPULA_WITHOUT_TENSE.add_out_suffix(self.Narr_Cop, self.VERB_COPULA_WITH_TENSE)
        self.Narr_Cop.add_suffix_form(u"+ymIş")

        self.VERB_COPULA_WITHOUT_TENSE.add_out_suffix(self.Past_Cop, self.VERB_COPULA_WITH_TENSE)
        self.Past_Cop.add_suffix_form(u"+ydI")

        self.VERB_COPULA_WITHOUT_TENSE.add_out_suffix(self.Cond_Cop, self.VERB_COPULA_WITH_TENSE)
        self.Cond_Cop.add_suffix_form(u"+ysA")

        self.VERB_COPULA_WITH_TENSE.add_out_suffix(self.Cond_Cop_Secondary, self.VERB_COPULA_WITH_TENSE)
        self.Cond_Cop_Secondary.add_suffix_form(u"+ysA", doesnt_come_after(self.Pres_Cop))

    def _register_copula_agreements(self):
        comes_after_cond_or_past = comes_after(self.Cond_Cop) | comes_after(self.Cond_Cop_Secondary) | comes_after(self.Past_Cop)

        self.VERB_COPULA_WITH_TENSE.add_out_suffix(self.A1Sg_Cop, self.DECORATED_VERB_TERMINAL_TRANSFER)
        self.A1Sg_Cop.add_suffix_form("+yIm")                          # (ben) elma-yim, (ben) armud-um, elma-ymis-im
        self.A1Sg_Cop.add_suffix_form("m", comes_after_cond_or_past)   # elma-ydi-m, elma-ysa-m

        self.VERB_COPULA_WITH_TENSE.add_out_suffix(self.A2Sg_Cop, self.DECORATED_VERB_TERMINAL_TRANSFER)
        self.A2Sg_Cop.add_suffix_form("sIn")                           # (sen) elma-sin, (sen) armutsun, elma-ymis-sin
        self.A2Sg_Cop.add_suffix_form("n", comes_after_cond_or_past)   # elma-ydi-n, elma-ysa-n

        self.VERB_COPULA_WITH_TENSE.add_out_suffix(self.A3Sg_Cop, self.DECORATED_VERB_TERMINAL_TRANSFER)
        self.A3Sg_Cop.add_suffix_form("")                              # (o) elma(dir), (o) armut(tur), elma-ymis, elma-ysa, elma-ydi

        self.VERB_COPULA_WITH_TENSE.add_out_suffix(self.A1Pl_Cop, self.DECORATED_VERB_TERMINAL_TRANSFER)
        self.A1Pl_Cop.add_suffix_form("+yIz")                          # (biz) elma-yiz, (biz) armud-uz, elma-ymis-iz
        self.A1Pl_Cop.add_suffix_form("k", comes_after_cond_or_past)   # elma-ydi-k, elma-ysa-k

        self.VERB_COPULA_WITH_TENSE.add_out_suffix(self.A2Pl_Cop, self.DECORATED_VERB_TERMINAL_TRANSFER)
        self.A2Pl_Cop.add_suffix_form("sInIz")                         # (siz) elma-siniz, (siz) armut-sunuz, elma-ymis-siniz
        self.A2Pl_Cop.add_suffix_form("nIz", comes_after_cond_or_past) # elma-ydi-niz, elma-ysa-niz

        self.VERB_COPULA_WITH_TENSE.add_out_suffix(self.A3Pl_Cop, self.DECORATED_VERB_TERMINAL_TRANSFER)
        self.A3Pl_Cop.add_suffix_form("lAr")    # (onlar) elma-lar(dir), (onlar) armut-lar(dir), elma-ymis-lar, elma-ydi-lar, elma-ysa-lar

    def _register_copula_tenses_to_other_categories(self):
        self.VERB_COPULA_WITHOUT_TENSE_DERIV.add_out_suffix(self.While_Cop, self.DECORATED_ADVERB_ROOT)
        self.While_Cop.add_suffix_form("+yken")

    def _register_verb_explicit_copula(self):

        explicit_verb_copula_precondition = doesnt_come_after(self.Decorated_Aorist) & doesnt_come_after(self.Decorated_Past) \
                                            & doesnt_come_after(self.Decorated_Cond) & doesnt_come_after(self.Decorated_Imp) \
                                            & doesnt_come_after(self.Decorated_Opt)

        explicit_verb_copula_precondition &= doesnt_come_after(self.Cond_Cop) & doesnt_come_after(self.Cond_Cop_Secondary) & doesnt_come_after(self.Past_Cop) & doesnt_come_after(self.Narr_Cop)
        explicit_verb_copula_precondition &= doesnt_come_after(self.Decorated_Narr_Ques) & doesnt_come_after(self.Decorated_Past_Ques)

        self.DECORATED_VERB_TERMINAL_TRANSFER.add_out_suffix(self.Cop_Verb, self.DECORATED_VERB_TERMINAL_TRANSFER)
        self.Cop_Verb.add_suffix_form("dIr", precondition=explicit_verb_copula_precondition)

    def _register_ques_explicit_copula(self):

        explicit_ques_copula_precondition = comes_after(self.Decorated_Pres_Ques)

        self.DECORATED_QUESTION_WITH_AGREEMENT.add_out_suffix(self.Cop_Verb, self.DECORATED_QUESTION_WITH_AGREEMENT)
        self.Cop_Ques.add_suffix_form("dIr", precondition=explicit_ques_copula_precondition)