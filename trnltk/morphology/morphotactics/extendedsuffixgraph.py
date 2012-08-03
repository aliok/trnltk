# coding=utf-8
from trnltk.morphology.lexiconmodel.lexeme import SyntacticCategory
from trnltk.morphology.morphotactics.suffixconditions import comes_after, doesnt_come_after
from trnltk.morphology.morphotactics.suffixgraph import SuffixGraph
from trnltk.morphology.morphotactics.suffixgraphmodel import *

class ExtendedSuffixGraph(SuffixGraph):

    def __init__(self):
        SuffixGraph.__init__(self)

        self._add_states()
        self._add_suffixes()
        self._register_suffixes()

    def _add_states(self):
        SuffixGraph._add_states(self)

        self.NOUN_COPULA = State("NOUN_COPULA", State.DERIV, SyntacticCategory.NOUN)
        self.ADJECTIVE_COPULA = State("ADJECTIVE_COPULA", State.DERIV, SyntacticCategory.ADJECTIVE)
        self.ADVERB_COPULA = State("ADVERB_COPULA", State.DERIV, SyntacticCategory.ADVERB)
        self.PRONOUN_COPULA = State("PRONOUN_COPULA", State.DERIV, SyntacticCategory.PRONOUN)
        self.VERB_DEGIL_ROOT = State("VERB_DEGIL_ROOT", State.TRANSFER, SyntacticCategory.VERB)

        self.VERB_COPULA_WITHOUT_TENSE = State("VERB_COPULA_WITHOUT_TENSE", State.TRANSFER, SyntacticCategory.VERB)
        self.VERB_COPULA_WITHOUT_TENSE_DERIV = State("VERB_COPULA_WITHOUT_TENSE_DERIV", State.DERIV, SyntacticCategory.VERB)
        self.VERB_COPULA_WITH_TENSE = State("VERB_COPULA_WITH_TENSE", State.TRANSFER, SyntacticCategory.VERB)

        self.ALL_STATES |= {
            self.NOUN_COPULA, self.ADJECTIVE_COPULA, self.ADVERB_COPULA, self.PRONOUN_COPULA, self.VERB_DEGIL_ROOT,
            self.VERB_COPULA_WITHOUT_TENSE, self.VERB_COPULA_WITHOUT_TENSE_DERIV, self.VERB_COPULA_WITH_TENSE
        }

    def get_default_stem_state(self, stem):
        if stem.dictionary_item.syntactic_category==SyntacticCategory.VERB and stem.root==u'değil':
            return self.VERB_DEGIL_ROOT
        else:
            return SuffixGraph.get_default_stem_state(self, stem)


    def _add_suffixes(self):
        SuffixGraph._add_suffixes(self)

        FreeTransitionSuffix("Noun_Cop_Free_Transition",         self.NOUN_TERMINAL_TRANSFER,      self.NOUN_COPULA)
        FreeTransitionSuffix("Adjective_Cop_Free_Transition",    self.ADJECTIVE_TERMINAL_TRANSFER, self.ADJECTIVE_COPULA)
        FreeTransitionSuffix("Adverb_Cop_Free_Transition",       self.ADVERB_TERMINAL_TRANSFER,    self.ADVERB_COPULA)
        FreeTransitionSuffix("Pronoun_Cop_Free_Transition",      self.PRONOUN_TERMINAL_TRANSFER,   self.PRONOUN_COPULA)
        FreeTransitionSuffix("Verb_Degil_Free_Transition",       self.VERB_DEGIL_ROOT,             self.VERB_COPULA_WITHOUT_TENSE)
        FreeTransitionSuffix("Copula_Deriv_Free_Transition",     self.VERB_COPULA_WITHOUT_TENSE,   self.VERB_COPULA_WITHOUT_TENSE_DERIV)

        ZeroTransitionSuffix("Noun_Copula_Zero_Transition",      self.NOUN_COPULA,        self.VERB_COPULA_WITHOUT_TENSE)
        ZeroTransitionSuffix("Adjective_Copula_Zero_Transition", self.ADJECTIVE_COPULA,   self.VERB_COPULA_WITHOUT_TENSE)
        ZeroTransitionSuffix("Adverb_Copula_Zero_Transition",    self.ADVERB_COPULA,      self.VERB_COPULA_WITHOUT_TENSE)
        ZeroTransitionSuffix("Pronoun_Copula_Zero_Transition",   self.PRONOUN_COPULA,     self.VERB_COPULA_WITHOUT_TENSE)

        ############# Copula tenses
        self.Pres_Cop = Suffix("Pres_Cop", pretty_name="Pres")
        self.Narr_Cop = Suffix("Narr_Cop", pretty_name="Narr")
        self.Past_Cop = Suffix("Past_Cop", pretty_name="Past")
        self.Cond_Cop = Suffix("Cond_Cop", pretty_name="Cond")

        ############# Copula agreements
        self.Copula_Agreements_Group = SuffixGroup('Copula_Agreements_Group')
        self.A1Sg_Cop = Suffix("A1Sg_Cop", self.Copula_Agreements_Group, "A1sg")
        self.A2Sg_Cop = Suffix("A2Sg_Cop", self.Copula_Agreements_Group, "A2sg")
        self.A3Sg_Cop = Suffix("A3Sg_Cop", self.Copula_Agreements_Group, "A3sg")
        self.A1Pl_Cop = Suffix("A1Pl_Cop", self.Copula_Agreements_Group, "A1pl")
        self.A2Pl_Cop = Suffix("A2Pl_Cop", self.Copula_Agreements_Group, "A2pl")
        self.A3Pl_Cop = Suffix("A3Pl_Cop", self.Copula_Agreements_Group, "A3pl")

        ############ Copula tenses to Adverb
        self.While_Cop = Suffix("While_Cop", pretty_name="While")

        ############ Explicit Copula
        self.Cop_Verb = Suffix("Cop_Verb", pretty_name="Cop")

    def _register_suffixes(self):
        SuffixGraph._register_suffixes(self)

        self._register_copula_tenses()
        self._register_copula_agreements()
        self._register_copula_tenses_to_other_categories()
        self._register_verb_explicit_copula()

    def _register_copula_tenses(self):
        self.VERB_COPULA_WITHOUT_TENSE.add_out_suffix(self.Pres_Cop, self.VERB_COPULA_WITH_TENSE)
        self.Pres_Cop.add_suffix_form(u"")

        self.VERB_COPULA_WITHOUT_TENSE.add_out_suffix(self.Narr_Cop, self.VERB_COPULA_WITH_TENSE)
        self.Narr_Cop.add_suffix_form(u"+ymIş")

        self.VERB_COPULA_WITHOUT_TENSE.add_out_suffix(self.Past_Cop, self.VERB_COPULA_WITH_TENSE)
        self.Past_Cop.add_suffix_form(u"+ydI")

        self.VERB_COPULA_WITHOUT_TENSE.add_out_suffix(self.Cond_Cop, self.VERB_COPULA_WITH_TENSE)
        self.Cond_Cop.add_suffix_form(u"+ysA")

    def _register_copula_agreements(self):
        comes_after_cond_or_past = comes_after(self.Cond_Cop) | comes_after(self.Past_Cop)

        self.VERB_COPULA_WITH_TENSE.add_out_suffix(self.A1Sg_Cop, self.VERB_TERMINAL_TRANSFER)
        self.A1Sg_Cop.add_suffix_form("+yIm")                          # (ben) elma-yim, (ben) armud-um, elma-ymis-im
        self.A1Sg_Cop.add_suffix_form("m", comes_after_cond_or_past)   # elma-ydi-m, elma-ysa-m

        self.VERB_COPULA_WITH_TENSE.add_out_suffix(self.A2Sg_Cop, self.VERB_TERMINAL_TRANSFER)
        self.A2Sg_Cop.add_suffix_form("sIn")                           # (sen) elma-sin, (sen) armutsun, elma-ymis-sin
        self.A2Sg_Cop.add_suffix_form("n", comes_after_cond_or_past)   # elma-ydi-n, elma-ysa-n

        self.VERB_COPULA_WITH_TENSE.add_out_suffix(self.A3Sg_Cop, self.VERB_TERMINAL_TRANSFER)
        self.A3Sg_Cop.add_suffix_form("")                              # (o) elma(dir), (o) armut(tur), elma-ymis, elma-ysa, elma-ydi

        self.VERB_COPULA_WITH_TENSE.add_out_suffix(self.A1Pl_Cop, self.VERB_TERMINAL_TRANSFER)
        self.A1Pl_Cop.add_suffix_form("+yIz")                          # (biz) elma-yiz, (biz) armud-uz, elma-ymis-iz
        self.A1Pl_Cop.add_suffix_form("k", comes_after_cond_or_past)   # elma-ydi-k, elma-ysa-k

        self.VERB_COPULA_WITH_TENSE.add_out_suffix(self.A2Pl_Cop, self.VERB_TERMINAL_TRANSFER)
        self.A2Pl_Cop.add_suffix_form("sInIz")                         # (siz) elma-siniz, (siz) armut-sunuz, elma-ymis-siniz
        self.A2Pl_Cop.add_suffix_form("nIz", comes_after_cond_or_past) # elma-ydi-niz, elma-ysa-niz

        self.VERB_COPULA_WITH_TENSE.add_out_suffix(self.A3Pl_Cop, self.VERB_TERMINAL_TRANSFER)
        self.A3Pl_Cop.add_suffix_form("lAr")    # (onlar) elma-lar(dir), (onlar) armut-lar(dir), elma-ymis-lar, elma-ydi-lar, elma-ysa-lar

    def _register_copula_tenses_to_other_categories(self):
        self.VERB_COPULA_WITHOUT_TENSE_DERIV.add_out_suffix(self.While_Cop, self.ADVERB_ROOT)
        self.While_Cop.add_suffix_form("+yken")

    def _register_verb_explicit_copula(self):

        explicit_verb_copula_precondition = doesnt_come_after(self.Aorist) & doesnt_come_after(self.Past) \
                                            & doesnt_come_after(self.Cond) & doesnt_come_after(self.Imp) \
                                            & doesnt_come_after(self.Opt)

        explicit_verb_copula_precondition &= doesnt_come_after(self.Cond_Cop) & doesnt_come_after(self.Past_Cop) & doesnt_come_after(self.Narr_Cop)
        explicit_verb_copula_precondition &= doesnt_come_after(self.Narr_Ques) & doesnt_come_after(self.Past_Ques)


        self.VERB_TERMINAL_TRANSFER.add_out_suffix(self.Cop_Verb, self.VERB_TERMINAL_TRANSFER)
        self.Cop_Verb.add_suffix_form("dIr", precondition=explicit_verb_copula_precondition)