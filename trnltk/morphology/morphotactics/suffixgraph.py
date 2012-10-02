# coding=utf-8
from trnltk.morphology.model.graphmodel import State
from trnltk.morphology.model.lexeme import RootAttribute, SyntacticCategory, SecondarySyntacticCategory
from trnltk.morphology.morphotactics.suffixconditions import comes_after, followed_by, applies_to_root, doesnt_come_after, doesnt, followed_by_suffix_goes_to, has_root_attribute, doesnt_come_after_derivation, followed_by_derivation, followed_by_one_from_group, doesnt_have_root_attribute, root_has_secondary_syntactic_category, comes_after_derivation, comes_after_last_non_blank_derivation
from trnltk.morphology.model.morpheme import *

class SuffixGraph(object):

    def __init__(self):
        self._add_states()
        self._add_suffixes()
        self._register_suffixes()

    def _add_states(self):
        self.NOUN_ROOT = State("NOUN_ROOT", State.TRANSFER, SyntacticCategory.NOUN)
        self.NOUN_WITH_AGREEMENT = State("NOUN_WITH_AGREEMENT", State.TRANSFER, SyntacticCategory.NOUN)
        self.NOUN_WITH_POSSESSION = State("NOUN_WITH_POSSESSION", State.TRANSFER, SyntacticCategory.NOUN)
        self.NOUN_WITH_CASE = State("NOUN_WITH_CASE", State.TRANSFER, SyntacticCategory.NOUN)
        self.NOUN_TERMINAL_TRANSFER = State("NOUN_TERMINAL_TRANSFER", State.TRANSFER, SyntacticCategory.NOUN)
        self.NOUN_TERMINAL = State("NOUN_TERMINAL", State.TERMINAL, SyntacticCategory.NOUN)
        self.NOUN_NOM_DERIV = State("NOUN_NOM_DERIV", State.DERIVATIONAL, SyntacticCategory.NOUN)
        self.NOUN_POSSESSIVE_NOM_DERIV = State("NOUN_POSSESSIVE_NOM_DERIV", State.DERIVATIONAL, SyntacticCategory.NOUN)
        self.NOUN_DERIV_WITH_CASE = State("NOUN_DERIV_WITH_CASE", State.DERIVATIONAL, SyntacticCategory.NOUN)

        self.NOUN_COMPOUND_ROOT = State("NOUN_COMPOUND_ROOT", State.TRANSFER, SyntacticCategory.NOUN)
        self.NOUN_COMPOUND_WITH_AGREEMENT = State("NOUN_COMPOUND_WITH_AGREEMENT", State.TRANSFER, SyntacticCategory.NOUN)
        self.NOUN_COMPOUND_WITH_POSSESSION = State("NOUN_COMPOUND_WITH_POSSESSION", State.TRANSFER, SyntacticCategory.NOUN)

        self.VERB_ROOT = State("VERB_ROOT", State.TRANSFER, SyntacticCategory.VERB)
        self.VERB_WITH_POLARITY = State("VERB_WITH_POLARITY", State.TRANSFER, SyntacticCategory.VERB)
        self.VERB_WITH_TENSE = State("VERB_WITH_TENSE", State.TRANSFER, SyntacticCategory.VERB)
        self.VERB_TERMINAL = State("VERB_TERMINAL", State.TERMINAL, SyntacticCategory.VERB)
        self.VERB_TERMINAL_TRANSFER = State("VERB_TERMINAL_TRANSFER", State.TRANSFER, SyntacticCategory.VERB)
        self.VERB_PLAIN_DERIV = State("VERB_PLAIN_DERIV", State.DERIVATIONAL, SyntacticCategory.VERB)
        self.VERB_POLARITY_DERIV = State("VERB_POLARITY_DERIV", State.DERIVATIONAL, SyntacticCategory.VERB)
        self.VERB_TENSE_DERIV = State("VERB_TENSE_DERIV", State.DERIVATIONAL, SyntacticCategory.VERB)
        self.VERB_TENSE_ADJ_DERIV = State("VERB_TENSE_ADJ_DERIV", State.DERIVATIONAL, SyntacticCategory.VERB)

        self.ADJECTIVE_ROOT = State("ADJECTIVE_ROOT", State.TRANSFER, SyntacticCategory.ADJECTIVE)
        self.ADJECTIVE_PART_WITHOUT_POSSESSION = State("ADJECTIVE_PART_WITHOUT_POSSESSION", State.TRANSFER, SyntacticCategory.ADJECTIVE)
        self.ADJECTIVE_TERMINAL = State("ADJECTIVE_TERMINAL", State.TERMINAL, SyntacticCategory.ADJECTIVE)
        self.ADJECTIVE_TERMINAL_TRANSFER = State("ADJECTIVE_TERMINAL_TRANSFER", State.TRANSFER, SyntacticCategory.ADJECTIVE)
        self.ADJECTIVE_DERIV = State("ADJECTIVE_DERIV", State.DERIVATIONAL, SyntacticCategory.ADJECTIVE)

        self.ADVERB_ROOT = State("ADVERB_ROOT", State.TRANSFER, SyntacticCategory.ADVERB)
        self.ADVERB_TERMINAL = State("ADVERB_TERMINAL", State.TERMINAL, SyntacticCategory.ADVERB)
        self.ADVERB_TERMINAL_TRANSFER = State("ADVERB_TERMINAL_TRANSFER", State.TRANSFER, SyntacticCategory.ADVERB)
        self.ADVERB_DERIV = State("ADVERB_DERIV", State.DERIVATIONAL, SyntacticCategory.ADVERB)

        self.PRONOUN_ROOT = State("PRONOUN_ROOT", State.TRANSFER, SyntacticCategory.PRONOUN)
        self.PRONOUN_WITH_AGREEMENT = State("PRONOUN_WITH_AGREEMENT", State.TRANSFER, SyntacticCategory.PRONOUN)
        self.PRONOUN_WITH_POSSESSION = State("PRONOUN_WITH_POSSESSION", State.TRANSFER, SyntacticCategory.PRONOUN)
        self.PRONOUN_WITH_CASE = State("PRONOUN_WITH_CASE", State.TRANSFER, SyntacticCategory.PRONOUN)
        self.PRONOUN_NOM_DERIV = State("PRONOUN_NOM_DERIV", State.DERIVATIONAL, SyntacticCategory.PRONOUN)
        self.PRONOUN_TERMINAL = State("PRONOUN_TERMINAL", State.TERMINAL, SyntacticCategory.PRONOUN)
        self.PRONOUN_TERMINAL_TRANSFER = State("PRONOUN_TERMINAL_TRANSFER", State.TRANSFER, SyntacticCategory.PRONOUN)
        self.PRONOUN_DERIV_WITH_CASE = State("PRONOUN_DERIV_WITH_CASE", State.DERIVATIONAL, SyntacticCategory.PRONOUN)

        self.DETERMINER_ROOT_TERMINAL = State("DETERMINER_ROOT_TERMINAL", State.TERMINAL, SyntacticCategory.DETERMINER)

        self.INTERJECTION_ROOT_TERMINAL = State("INTERJECTION_ROOT_TERMINAL", State.TERMINAL, SyntacticCategory.INTERJECTION)

        self.CONJUNCTION_ROOT_TERMINAL = State("CONJUNCTION_ROOT_TERMINAL", State.TERMINAL, SyntacticCategory.CONJUNCTION)

        self.NUMERAL_CARDINAL_ROOT = State("NUMERAL_CARDINAL_ROOT", State.TRANSFER, SyntacticCategory.NUMERAL)
        self.NUMERAL_CARDINAL_DERIV = State("NUMERAL_CARDINAL_DERIV", State.DERIVATIONAL, SyntacticCategory.NUMERAL)

        self.NUMERAL_DIGIT_CARDINAL_ROOT = State("NUMERAL_DIGIT_CARDINAL_ROOT", State.TRANSFER, SyntacticCategory.NUMERAL)

        self.NUMERAL_ORDINAL_ROOT = State("NUMERAL_ORDINAL_ROOT", State.TRANSFER, SyntacticCategory.NUMERAL)
        self.NUMERAL_ORDINAL_DERIV = State("NUMERAL_ORDINAL_DERIV", State.DERIVATIONAL, SyntacticCategory.NUMERAL)

        self.QUESTION_ROOT = State("QUESTION_ROOT", State.TRANSFER, SyntacticCategory.QUESTION)
        self.QUESTION_WITH_TENSE = State("QUESTION_WITH_TENSE", State.TRANSFER, SyntacticCategory.QUESTION)
        self.QUESTION_WITH_AGREEMENT = State("QUESTION_WITH_AGREEMENT", State.TRANSFER, SyntacticCategory.QUESTION)
        self.QUESTION_TERMINAL = State("QUESTION_TERMINAL", State.TERMINAL, SyntacticCategory.QUESTION)

        self.PUNC_ROOT_TERMINAL = State("PUNC_ROOT_TERMINAL", State.TERMINAL, SyntacticCategory.PUNCTUATION)

        self.PART_ROOT_TERMINAL = State("PART_ROOT_TERMINAL", State.TERMINAL, SyntacticCategory.PARTICLE)

        self.ALL_STATES = {
            self.NOUN_ROOT, self.NOUN_WITH_AGREEMENT, self.NOUN_WITH_POSSESSION, self.NOUN_WITH_CASE, self.NOUN_TERMINAL,
            self.NOUN_TERMINAL_TRANSFER, self.NOUN_DERIV_WITH_CASE, self.NOUN_NOM_DERIV, self.NOUN_POSSESSIVE_NOM_DERIV,

            self.NOUN_COMPOUND_ROOT, self.NOUN_COMPOUND_WITH_AGREEMENT, self.NOUN_COMPOUND_WITH_POSSESSION,

            self.VERB_ROOT, self.VERB_WITH_POLARITY, self.VERB_WITH_TENSE, self.VERB_TERMINAL, self.VERB_TERMINAL_TRANSFER,
            self.VERB_PLAIN_DERIV, self.VERB_POLARITY_DERIV, self.VERB_TENSE_DERIV, self.VERB_TENSE_ADJ_DERIV,

            self.ADJECTIVE_ROOT, self.ADJECTIVE_PART_WITHOUT_POSSESSION, self.ADJECTIVE_TERMINAL,
            self.ADJECTIVE_TERMINAL_TRANSFER, self.ADJECTIVE_DERIV,

            self.ADVERB_ROOT, self.ADVERB_TERMINAL, self.ADVERB_TERMINAL_TRANSFER, self.ADVERB_DERIV,

            self.PRONOUN_ROOT, self.PRONOUN_WITH_AGREEMENT, self.PRONOUN_WITH_POSSESSION, self.PRONOUN_WITH_CASE,
            self.PRONOUN_TERMINAL, self.PRONOUN_TERMINAL_TRANSFER, self.PRONOUN_DERIV_WITH_CASE, self.PRONOUN_NOM_DERIV,

            self.DETERMINER_ROOT_TERMINAL,

            self.INTERJECTION_ROOT_TERMINAL,

            self.CONJUNCTION_ROOT_TERMINAL,

            self.NUMERAL_CARDINAL_ROOT, self.NUMERAL_CARDINAL_DERIV,
            self.NUMERAL_DIGIT_CARDINAL_ROOT,
            self.NUMERAL_ORDINAL_ROOT, self.NUMERAL_ORDINAL_DERIV,

            self.QUESTION_ROOT, self.QUESTION_WITH_TENSE, self.QUESTION_WITH_AGREEMENT, self.QUESTION_TERMINAL,

            self.PUNC_ROOT_TERMINAL,

            self.PART_ROOT_TERMINAL
        }

    def get_default_root_state(self, root):
        """
        Return the initial state for root based on primary and secondary syntactic category of it.
        @type root: Root
        @rtype: State
        """
        if not root.lexeme.syntactic_category or root.lexeme.syntactic_category==SyntacticCategory.NOUN:
            if RootAttribute.CompoundP3sg in root.lexeme.attributes:
                return self.NOUN_COMPOUND_ROOT
            else:
                return self.NOUN_ROOT
        elif root.lexeme.syntactic_category==SyntacticCategory.VERB:
            return self.VERB_ROOT
        elif root.lexeme.syntactic_category==SyntacticCategory.ADVERB:
            return self.ADVERB_ROOT
        elif root.lexeme.syntactic_category==SyntacticCategory.ADJECTIVE:
            return self.ADJECTIVE_ROOT
        elif root.lexeme.syntactic_category==SyntacticCategory.PRONOUN:
            return self.PRONOUN_ROOT
        elif root.lexeme.syntactic_category==SyntacticCategory.DETERMINER:
            return self.DETERMINER_ROOT_TERMINAL
        elif root.lexeme.syntactic_category==SyntacticCategory.INTERJECTION:
            return self.INTERJECTION_ROOT_TERMINAL
        elif root.lexeme.syntactic_category==SyntacticCategory.CONJUNCTION:
            return self.CONJUNCTION_ROOT_TERMINAL
        elif root.lexeme.syntactic_category==SyntacticCategory.NUMERAL and root.lexeme.secondary_syntactic_category==SecondarySyntacticCategory.DIGITS:
            return self.NUMERAL_DIGIT_CARDINAL_ROOT
        elif root.lexeme.syntactic_category==SyntacticCategory.NUMERAL and root.lexeme.secondary_syntactic_category==SecondarySyntacticCategory.CARD:
            return self.NUMERAL_CARDINAL_ROOT
        elif root.lexeme.syntactic_category==SyntacticCategory.NUMERAL and root.lexeme.secondary_syntactic_category==SecondarySyntacticCategory.ORD:
            return self.NUMERAL_ORDINAL_ROOT
        elif root.lexeme.syntactic_category==SyntacticCategory.PUNCTUATION:
            return self.PUNC_ROOT_TERMINAL
        elif root.lexeme.syntactic_category==SyntacticCategory.PARTICLE:
            return self.PART_ROOT_TERMINAL
        elif root.lexeme.syntactic_category==SyntacticCategory.QUESTION:
            return self.QUESTION_ROOT
        else:
            raise Exception("No _root state found for root {} !".format(root))

    def _add_suffixes(self):

        #############  Empty _transitions
        self.NOUN_WITH_CASE               .add_out_suffix(FreeTransitionSuffix("Noun_Free_Transition_1"     ), self.NOUN_TERMINAL_TRANSFER)
        self.NOUN_TERMINAL_TRANSFER       .add_out_suffix(FreeTransitionSuffix("Noun_Free_Transition_2"     ), self.NOUN_TERMINAL)
        self.NOUN_WITH_CASE               .add_out_suffix(FreeTransitionSuffix("Noun_Free_Transition_3"     ), self.NOUN_DERIV_WITH_CASE)

        self.VERB_ROOT                    .add_out_suffix(FreeTransitionSuffix("Verb_Free_Transition_1"     ), self.VERB_PLAIN_DERIV)
        self.VERB_WITH_POLARITY           .add_out_suffix(FreeTransitionSuffix("Verb_Free_Transition_2"     ), self.VERB_POLARITY_DERIV)
        self.VERB_WITH_TENSE              .add_out_suffix(FreeTransitionSuffix("Verb_Free_Transition_3"     ), self.VERB_TENSE_DERIV)
        self.VERB_TERMINAL_TRANSFER       .add_out_suffix(FreeTransitionSuffix("Verb_Free_Transition_4"     ), self.VERB_TERMINAL)

        self.ADJECTIVE_ROOT               .add_out_suffix(FreeTransitionSuffix("Adj_Free_Transition_1"      ), self.ADJECTIVE_TERMINAL_TRANSFER)
        self.ADJECTIVE_TERMINAL_TRANSFER  .add_out_suffix(FreeTransitionSuffix("Adj_Free_Transition_2"      ), self.ADJECTIVE_TERMINAL)
        self.ADJECTIVE_ROOT               .add_out_suffix(FreeTransitionSuffix("Adj_Free_Transition_3"      ), self.ADJECTIVE_DERIV)

        self.ADVERB_ROOT                  .add_out_suffix(FreeTransitionSuffix("Adv_Free_Transition_1"      ), self.ADVERB_TERMINAL_TRANSFER)
        self.ADVERB_TERMINAL_TRANSFER     .add_out_suffix(FreeTransitionSuffix("Adv_Free_Transition_2"      ), self.ADVERB_TERMINAL)
        self.ADVERB_ROOT                  .add_out_suffix(FreeTransitionSuffix("Adv_Free_Transition_3"      ), self.ADVERB_DERIV)

        self.PRONOUN_WITH_CASE            .add_out_suffix(FreeTransitionSuffix("Pronoun_Free_Transition_1"  ), self.PRONOUN_TERMINAL_TRANSFER)
        self.PRONOUN_TERMINAL_TRANSFER    .add_out_suffix(FreeTransitionSuffix("Pronoun_Free_Transition_2"  ), self.PRONOUN_TERMINAL)
        self.PRONOUN_WITH_CASE            .add_out_suffix(FreeTransitionSuffix("Pronoun_Free_Transition_3"  ), self.PRONOUN_DERIV_WITH_CASE)

        self.NUMERAL_CARDINAL_ROOT        .add_out_suffix(FreeTransitionSuffix("Numeral_Free_Transition_1"  ), self.NUMERAL_CARDINAL_DERIV)
        self.NUMERAL_ORDINAL_ROOT         .add_out_suffix(FreeTransitionSuffix("Numeral_Free_Transition_2"  ), self.NUMERAL_ORDINAL_DERIV)

        self.QUESTION_WITH_AGREEMENT      .add_out_suffix(FreeTransitionSuffix("Question_Free_Transition_1" ), self.QUESTION_TERMINAL)

        self.NUMERAL_DIGIT_CARDINAL_ROOT  .add_out_suffix(FreeTransitionSuffix("Digits_Free_Transition_1"   ), self.NUMERAL_CARDINAL_DERIV)

        self.NUMERAL_CARDINAL_DERIV       .add_out_suffix(ZeroTransitionSuffix("Numeral_Zero_Transition_1"  ), self.ADJECTIVE_ROOT)
        self.NUMERAL_ORDINAL_DERIV        .add_out_suffix(ZeroTransitionSuffix("Numeral_Zero_Transition_2"  ), self.ADJECTIVE_ROOT)
        self.ADJECTIVE_DERIV              .add_out_suffix(ZeroTransitionSuffix("Adj_to_Noun_Zero_Transition"), self.NOUN_ROOT)
        self.VERB_TENSE_ADJ_DERIV         .add_out_suffix(ZeroTransitionSuffix("Verb_to_Adj_Zero_Transition"), self.ADJECTIVE_ROOT)

        #TODO: transition from numeral to adverb for case "birer birer geldiler?" hmm maybe duplication caused an adj->adv transition?

        #############  Noun Agreements
        self.Noun_Agreements_Group = SuffixGroup("Noun_Agreements_Group")
        self.A3Sg_Noun = Suffix("A3Sg_Noun", self.Noun_Agreements_Group, 'A3sg')
        self.A3Pl_Noun = Suffix("A3Pl_Noun", self.Noun_Agreements_Group, 'A3pl')

        ###########  Possessive agreements
        self.Noun_Possessions_Group = SuffixGroup("Noun_Possession_Group")
        self.Pnon_Noun = Suffix("Pnon_Noun", self.Noun_Possessions_Group, "Pnon")
        self.P1Sg_Noun = Suffix("P1sg_Noun", self.Noun_Possessions_Group, "P1sg")
        self.P2Sg_Noun = Suffix("P2sg_Noun", self.Noun_Possessions_Group, "P2sg")
        self.P3Sg_Noun = Suffix("P3sg_Noun", self.Noun_Possessions_Group, "P3sg")
        self.P1Pl_Noun = Suffix("P1pl_Noun", self.Noun_Possessions_Group, "P1pl")
        self.P2Pl_Noun = Suffix("P2pl_Noun", self.Noun_Possessions_Group, "P2pl")
        self.P3Pl_Noun = Suffix("P3pl_Noun", self.Noun_Possessions_Group, "P3pl")

        ###########  Noun cases
        self.Noun_Cases_Group = SuffixGroup('Noun_Case_Group')
        self.Nom_Noun = Suffix("Nom_Noun", self.Noun_Cases_Group, "Nom")
        self.Nom_Noun_Deriv = Suffix("Nom_Deriv_Noun", self.Noun_Cases_Group, "Nom")
        self.Nom_Noun_Possessive_Deriv = Suffix("Nom_Deriv_Possessive_Noun", self.Noun_Cases_Group, "Nom")
        self.Acc_Noun = Suffix("Acc_Noun", self.Noun_Cases_Group, "Acc")
        self.Dat_Noun = Suffix("Dat_Noun", self.Noun_Cases_Group, "Dat")
        self.Loc_Noun = Suffix("Loc_Noun", self.Noun_Cases_Group, "Loc")
        self.Abl_Noun = Suffix("Abl_Noun", self.Noun_Cases_Group, "Abl")

        self.Gen_Noun = Suffix("Gen_Noun", self.Noun_Cases_Group, "Gen")
        self.Ins_Noun = Suffix("Ins_Noun", self.Noun_Cases_Group, "Ins")

        ############# Noun to Noun derivations
        self.Agt_Noun = Suffix("Agt_Noun", pretty_name='Agt')
        self.Dim = Suffix("Dim")
        self.Prof = Suffix("Prof")
        self.FitFor = Suffix("FitFor")
        self.Title = Suffix("Title")

        ############# Noun to Verb derivations
        self.Acquire = Suffix("Acquire")

        ############# Noun to Adjective derivations
        self.With = Suffix("With")
        self.Without = Suffix("Without")
        self.PointQual_Noun = Suffix("PointQual_Noun", pretty_name="PointQual")     #was marked as relative pronoun in other projects, but that is "Alininki"
        self.JustLike_Noun = Suffix("JustLike_Noun", pretty_name='JustLike')
        self.Equ_Noun = Suffix("Equ_Noun", pretty_name='Equ')
        self.Y = Suffix("Y")
        self.For = Suffix("For")
        self.DurationOf = Suffix("DurationOf")
        self.OfUnit_Noun = Suffix("OfUnit_Noun", pretty_name='OfUnit')

        ############ Noun to Adverb derivations
        self.InTermsOf = Suffix("InTermsOf")
        self.By_Pnon = Suffix("By_Pnon", pretty_name='By')
        self.By_Possessive = Suffix("By_Possessive", pretty_name='By')
        self.ManyOf = Suffix("ManyOf")
        self.ForALotOfTime = Suffix("ForALotOfTime")

        ############ Noun to Pronoun derivations
        self.Relative_Noun_Pronoun_Group = SuffixGroup("Relative_Noun_Pronoun_Group")
        self.RelPron_A3Sg_Noun = Suffix("RelPron_A3Sg_Noun", self.Relative_Noun_Pronoun_Group, "A3sg")
        self.RelPron_A3Pl_Noun = Suffix("RelPron_A3Pl_Noun", self.Relative_Noun_Pronoun_Group, "A3pl")

        ############# Noun Compound suffixes
        self.A3Sg_Noun_Compound = Suffix("A3Sg_Noun_Compound", pretty_name="A3sg")
        self.PNon_Noun_Compound = Suffix("Pnon_Noun_Compound", pretty_name="Pnon")
        self.P3Sg_Noun_Compound = Suffix("P3Sg_Noun_Compound", pretty_name="P3sg")
        self.P3Pl_Noun_Compound = Suffix("P3Pl_Noun_Compound", pretty_name="P3pl")
        self.Nom_Noun_Compound_Deriv = Suffix("Nom_Noun_Compound_Deriv", pretty_name="Nom")

        ############# Verb agreements
        self.Verb_Agreements_Group = SuffixGroup('Verb_Agreements_Group')
        self.A1Sg_Verb = Suffix("A1Sg_Verb", self.Verb_Agreements_Group, "A1sg")
        self.A2Sg_Verb = Suffix("A2Sg_Verb", self.Verb_Agreements_Group, "A2sg")
        self.A3Sg_Verb = Suffix("A3Sg_Verb", self.Verb_Agreements_Group, "A3sg")
        self.A1Pl_Verb = Suffix("A1Pl_Verb", self.Verb_Agreements_Group, "A1pl")
        self.A2Pl_Verb = Suffix("A2Pl_Verb", self.Verb_Agreements_Group, "A2pl")
        self.A3Pl_Verb = Suffix("A3Pl_Verb", self.Verb_Agreements_Group, "A3pl")

        ############# Verb conditions
        self.Verb_Polarity_Group = SuffixGroup("Verb_Conditions_Group")
        self.Negative = Suffix("Neg", self.Verb_Polarity_Group)
        self.Positive = Suffix("Pos", self.Verb_Polarity_Group)

        ############# Verbal tenses
        self.Aorist = Suffix("Aor")
        self.Progressive = Suffix("Prog")
        self.Future = Suffix("Fut")
        self.Narr = Suffix("Narr")
        self.Past = Suffix("Past")
        self.Pres = Suffix("Pres")

        self.Cond = Suffix("Cond")
        self.Imp = Suffix("Imp")

        ############ Modals
        self.Neces = Suffix("Neces")
        self.Opt = Suffix("Opt")
        self.Desr = Suffix("Desr")

        ############ Verb to Noun derivations
        self.Inf = Suffix("Inf")
        self.PastPart_Noun = Suffix("PastPart_Noun", pretty_name='PastPart')
        self.FutPart_Noun = Suffix('FutPart_Noun', pretty_name='FutPart')

        ############ Verb to Verb derivations
        self.Able = Suffix("Able")
        self.Pass = Suffix("Pass")
        self.Recip = Suffix("Recip")
        self.Caus = Suffix("Caus", allow_repetition=True)
        self.Hastily = Suffix("Hastily")

        ########### Verb to Adverb derivations
        self.AfterDoingSo = Suffix("AfterDoingSo")
        self.WithoutHavingDoneSo = Suffix("WithoutHavingDoneSo")
        self.AsLongAs = Suffix("AsLongAs")
        self.ByDoingSo = Suffix("ByDoingSo")
        self.While = Suffix("While")
        self.When = Suffix("When")
        self.SinceDoingSo = Suffix('SinceDoingSo')
        self.AsIf = Suffix("AsIf")

        ########### Verb to Adjective derivations
        self.PresPart = Suffix("PresPart")
        self.PastPart_Adj = Suffix("PastPart_Adj", pretty_name='PastPart')
        self.FutPart_Adj = Suffix('FutPart_Adj', pretty_name='FutPart')
        self.Agt_Adj = Suffix('Agt_Adj', pretty_name='Agt')

        self.Aorist_to_Adj = Suffix("Aorist_to_Adj", pretty_name="Aor")
        self.Future_to_Adj = Suffix("Future_to_Adj", pretty_name="Fut")
        self.Narr_to_Adj = Suffix("Narr_to_Adj", pretty_name="Narr")

        ########### Adjective to Adjective derivations
        self.JustLike_Adj = Suffix("JustLike_Adj", pretty_name='JustLike')
        self.Equ_Adj = Suffix("Equ_Adj", pretty_name='Equ')
        self.Quite = Suffix("Quite")

        ########### Adjective to Adverb derivations
        self.Ly = Suffix("Ly")

        ########### Adjective to Noun derivations
        self.Ness = Suffix("Ness")

        ########### Adjective to Verb derivations
        self.Become = Suffix("Become")

        ########### Adjective possessions
        self.Adjective_Possessions_Group = SuffixGroup("Adjective_Possessions_Group")
        self.Pnon_Adj = Suffix("Pnon_Adj", self.Adjective_Possessions_Group, 'Pnon')
        self.P1Sg_Adj = Suffix("P1Sg_Adj", self.Adjective_Possessions_Group, 'P1sg')
        self.P2Sg_Adj = Suffix("P2Sg_Adj", self.Adjective_Possessions_Group, 'P2sg')
        self.P3Sg_Adj = Suffix("P3Sg_Adj", self.Adjective_Possessions_Group, 'P3sg')
        self.P1Pl_Adj = Suffix("P1Pl_Adj", self.Adjective_Possessions_Group, 'P1pl')
        self.P2Pl_Adj = Suffix("P2Pl_Adj", self.Adjective_Possessions_Group, 'P2pl')
        self.P3Pl_Adj = Suffix("P3Pl_Adj", self.Adjective_Possessions_Group, 'P3pl')

        #############  Pronoun Agreements
        self.Pronoun_Agreements_Group = SuffixGroup("Pronoun_Agreements_Group")
        self.A1Sg_Pron = Suffix("A1Sg_Pron", self.Pronoun_Agreements_Group, 'A1sg')
        self.A2Sg_Pron = Suffix("A2Sg_Pron", self.Pronoun_Agreements_Group, 'A2sg')
        self.A3Sg_Pron = Suffix("A3Sg_Pron", self.Pronoun_Agreements_Group, 'A3sg')
        self.A1Pl_Pron = Suffix("A1Pl_Pron", self.Pronoun_Agreements_Group, 'A1pl')
        self.A2Pl_Pron = Suffix("A2Pl_Pron", self.Pronoun_Agreements_Group, 'A2pl')
        self.A3Pl_Pron = Suffix("A3Pl_Pron", self.Pronoun_Agreements_Group, 'A3pl')

        ########### Pronoun possessions
        self.Pronoun_Possessions_Group = SuffixGroup("Pronoun_Possessions_Group")
        self.Pnon_Pron = Suffix("Pnon_Pron", self.Pronoun_Possessions_Group, 'Pnon')
        self.P1Sg_Pron = Suffix("P1Sg_Pron", self.Pronoun_Possessions_Group, 'P1sg')
        self.P2Sg_Pron = Suffix("P2Sg_Pron", self.Pronoun_Possessions_Group, 'P2sg')
        self.P3Sg_Pron = Suffix("P3Sg_Pron", self.Pronoun_Possessions_Group, 'P3sg')
        self.P1Pl_Pron = Suffix("P1Pl_Pron", self.Pronoun_Possessions_Group, 'P1pl')
        self.P2Pl_Pron = Suffix("P2Pl_Pron", self.Pronoun_Possessions_Group, 'P2pl')
        self.P3Pl_Pron = Suffix("P3Pl_Pron", self.Pronoun_Possessions_Group, 'P3pl')

        ###########  Pronoun cases
        self.Pronoun_Case_Group = SuffixGroup('Pronoun_Case_Group')
        self.Nom_Pron = Suffix("Nom_Pron", self.Pronoun_Case_Group, pretty_name="Nom")
        self.Nom_Pron_Deriv = Suffix("Nom_Pron_Deriv", self.Pronoun_Case_Group, pretty_name="Nom")
        self.Acc_Pron = Suffix("Acc_Pron", self.Pronoun_Case_Group, pretty_name='Acc')
        self.Dat_Pron = Suffix("Dat_Pron", self.Pronoun_Case_Group, pretty_name='Dat')
        self.Loc_Pron = Suffix("Loc_Pron", self.Pronoun_Case_Group, pretty_name='Loc')
        self.Abl_Pron = Suffix("Abl_Pron", self.Pronoun_Case_Group, pretty_name='Abl')

        ############# Pronoun case-likes
        self.Gen_Pron = Suffix("Gen_Pron", self.Pronoun_Case_Group, pretty_name='Gen')
        self.Ins_Pron = Suffix("Ins_Pron", self.Pronoun_Case_Group, pretty_name='Ins')
        self.AccordingTo = Suffix("AccordingTo", self.Pronoun_Case_Group)

        ############# Pronoun to Adjective derivations
        self.Without_Pron = Suffix("Without_Pron", pretty_name="Without")
        self.PointQual_Pron = Suffix("PointQual_Pron", pretty_name="PointQual")

        ############# Pronoun to Pronoun derivations
        self.Relative_Pron_Pronoun_Group = SuffixGroup("Relative_Pron_Pronoun_Group")
        self.RelPron_A3Sg_Pron = Suffix("RelPron_A3Sg_Pron", self.Relative_Pron_Pronoun_Group, "A3sg")
        self.RelPron_A3Pl_Pron = Suffix("RelPron_A3Pl_Pron", self.Relative_Pron_Pronoun_Group, "A3pl")

        ############# Adverb to Adjective derivations
        self.PointQual_Adv = Suffix("PointQual_Adv", pretty_name="PointQual")

        ############ Question Tenses
        self.Question_Tense_Group = SuffixGroup('Question_Tense_Group')
        self.Pres_Ques = Suffix("Pres_Ques", self.Question_Tense_Group, "Pres")
        self.Past_Ques = Suffix("Past_Ques", self.Question_Tense_Group, "Past")
        self.Narr_Ques = Suffix("Narr_Ques", self.Question_Tense_Group, "Narr")

        ############ Question Agreements
        self.Question_Agreements_Group = SuffixGroup("Question_Agreements_Group")
        self.A1Sg_Ques = Suffix("A1Sg_Ques", self.Question_Agreements_Group, 'A1sg')
        self.A2Sg_Ques = Suffix("A2Sg_Ques", self.Question_Agreements_Group, 'A2sg')
        self.A3Sg_Ques = Suffix("A3Sg_Ques", self.Question_Agreements_Group, 'A3sg')
        self.A1Pl_Ques = Suffix("A1Pl_Ques", self.Question_Agreements_Group, 'A1pl')
        self.A2Pl_Ques = Suffix("A2Pl_Ques", self.Question_Agreements_Group, 'A2pl')
        self.A3Pl_Ques = Suffix("A3Pl_Ques", self.Question_Agreements_Group, 'A3pl')

        ########### Cardinal numbers to Adjective derivations
        self.NumbersOf = Suffix("NumbersOf")
        self.OfUnit_Number = Suffix("OfUnit_Number", pretty_name='OfUnit')

        ########### Cardinal digits suffixes
        self.Apos_Digit = Suffix("Apos")

    def _register_suffixes(self):
        self._register_noun_suffixes()
        self._register_verb_suffixes()
        self._register_adjective_suffixes()
        self._register_pronoun_suffixes()
        self._register_adverb_suffixes()
        self._register_question_suffixes()
        self._register_numeral_suffixes()

    def _register_noun_suffixes(self):
        self._register_noun_agreements()
        self._register_possessive_agreements()
        self._register_noun_cases()
        self._register_noun_to_noun_derivations()
        self._register_noun_to_verb_derivations()
        self._register_noun_to_adjective_derivations()
        self._register_noun_to_adverb_derivations()
        self._register_noun_to_pronoun_derivations()
        self._register_noun_compound_suffixes()

    def _register_verb_suffixes(self):
        self._register_verb_agreements()
        self._register_verb_polarisations()
        self._register_verb_tenses()
        self._register_modal_verbs()
        self._register_verb_to_verb_derivations()
        self._register_verb_to_noun_derivations()
        self._register_verb_to_adverb_derivations()
        self._register_verb_to_adjective_derivations()

    def _register_adjective_suffixes(self):
        self._register_adjective_to_adjective_derivations()
        self._register_adjective_to_adverb_derivations()
        self._register_adjective_to_noun_derivations()
        self._register_adjective_to_verb_derivations()
        self._register_adjective_possessions()

    def _register_pronoun_suffixes(self):
        self._register_pronoun_agreements()
        self._register_pronoun_possessions()
        self._register_pronoun_cases()
        self._register_pronoun_to_adjective_suffixes()
        self._register_pronoun_to_pronoun_derivations()

    def _register_adverb_suffixes(self):
        self._register_adverb_to_adjective_derivations()

    def _register_question_suffixes(self):
        self._register_question_tenses()
        self._register_question_agreements()

    def _register_numeral_suffixes(self):
        self._register_cardinal_to_adjective_suffixes()
        self._register_digits_suffixes()

    def _register_noun_agreements(self):
        self.NOUN_ROOT.add_out_suffix(self.A3Sg_Noun, self.NOUN_WITH_AGREEMENT)
        self.A3Sg_Noun.add_suffix_form("")

        self.NOUN_ROOT.add_out_suffix(self.A3Pl_Noun, self.NOUN_WITH_AGREEMENT)
        self.A3Pl_Noun.add_suffix_form("lAr")

    def _register_possessive_agreements(self):
        doesnt_come_after_PointerQual = doesnt(comes_after_last_non_blank_derivation(self.PointQual_Adv))  & \
                                        doesnt(comes_after_last_non_blank_derivation(self.PointQual_Noun)) & \
                                        doesnt(comes_after_last_non_blank_derivation(self.PointQual_Pron))

        self.NOUN_WITH_AGREEMENT.add_out_suffix(self.Pnon_Noun, self.NOUN_WITH_POSSESSION)
        self.Pnon_Noun.add_suffix_form("")

        self.NOUN_WITH_AGREEMENT.add_out_suffix(self.P1Sg_Noun, self.NOUN_WITH_POSSESSION)
        self.P1Sg_Noun.add_suffix_form("+Im", doesnt_come_after_PointerQual)

        self.NOUN_WITH_AGREEMENT.add_out_suffix(self.P2Sg_Noun, self.NOUN_WITH_POSSESSION)
        self.P2Sg_Noun.add_suffix_form("+In", doesnt_come_after_PointerQual)

        self.NOUN_WITH_AGREEMENT.add_out_suffix(self.P3Sg_Noun, self.NOUN_WITH_POSSESSION)
        self.P3Sg_Noun.add_suffix_form("+sI", doesnt_come_after_PointerQual)

        self.NOUN_WITH_AGREEMENT.add_out_suffix(self.P1Pl_Noun, self.NOUN_WITH_POSSESSION)
        self.P1Pl_Noun.add_suffix_form("+ImIz", doesnt_come_after_PointerQual)

        self.NOUN_WITH_AGREEMENT.add_out_suffix(self.P2Pl_Noun, self.NOUN_WITH_POSSESSION)
        self.P2Pl_Noun.add_suffix_form("+InIz", doesnt_come_after_PointerQual)

        self.NOUN_WITH_AGREEMENT.add_out_suffix(self.P3Pl_Noun, self.NOUN_WITH_POSSESSION)
        self.P3Pl_Noun.add_suffix_form("lArI!", doesnt_come_after_PointerQual)
        self.P3Pl_Noun.add_suffix_form("I!", comes_after(self.A3Pl_Noun) & doesnt_come_after_PointerQual)

    def _register_noun_cases(self):
        comes_after_P3 = comes_after(self.P3Sg_Noun) | comes_after(self.P3Pl_Noun) | comes_after(self.P3Sg_Noun_Compound) | comes_after(self.P3Pl_Noun_Compound)
        doesnt_come_after_P3 = ~comes_after_P3

        comes_after_PointQual  = comes_after_last_non_blank_derivation(self.PointQual_Adv) | comes_after_last_non_blank_derivation(self.PointQual_Noun) | comes_after_last_non_blank_derivation(self.PointQual_Pron)
        doesnt_come_after_PointQual = ~comes_after_PointQual

        comes_after_PointQual_Followed_By_A3Sg = comes_after_PointQual & (comes_after(self.A3Sg_Noun) | comes_after(self.A3Sg_Noun_Compound))
        comes_after_PointQual_Followed_By_A3Pl = comes_after_PointQual & comes_after(self.A3Pl_Noun)

        self.NOUN_WITH_POSSESSION.add_out_suffix(self.Nom_Noun, self.NOUN_WITH_CASE)
        self.Nom_Noun.add_suffix_form("")

        self.NOUN_WITH_POSSESSION.add_out_suffix(self.Nom_Noun_Deriv, self.NOUN_NOM_DERIV)
        self.Nom_Noun_Deriv.add_suffix_form("", comes_after(self.Pnon_Noun))

        self.NOUN_WITH_POSSESSION.add_out_suffix(self.Nom_Noun_Possessive_Deriv, self.NOUN_POSSESSIVE_NOM_DERIV)
        self.Nom_Noun_Possessive_Deriv.add_suffix_form("", doesnt_come_after(self.Pnon_Noun))

        self.NOUN_WITH_POSSESSION.add_out_suffix(self.Acc_Noun, self.NOUN_WITH_CASE)
        self.Acc_Noun.add_suffix_form(u"+yI", (doesnt_come_after_P3 & doesnt(comes_after_PointQual_Followed_By_A3Sg)) | comes_after_PointQual_Followed_By_A3Pl)
        self.Acc_Noun.add_suffix_form(u"nI", comes_after_P3 | comes_after_PointQual_Followed_By_A3Sg)

        self.NOUN_WITH_POSSESSION.add_out_suffix(self.Dat_Noun, self.NOUN_WITH_CASE)
        self.Dat_Noun.add_suffix_form(u"+yA", (doesnt_come_after_P3 & doesnt(comes_after_PointQual_Followed_By_A3Sg)) | comes_after_PointQual_Followed_By_A3Pl)
        self.Dat_Noun.add_suffix_form(u"nA", comes_after_P3 | comes_after_PointQual_Followed_By_A3Sg)

        self.NOUN_WITH_POSSESSION.add_out_suffix(self.Loc_Noun, self.NOUN_WITH_CASE)
        self.Loc_Noun.add_suffix_form(u"dA", ((doesnt_come_after_P3 & doesnt(comes_after_PointQual_Followed_By_A3Sg)) | comes_after_PointQual_Followed_By_A3Pl) & doesnt_come_after_derivation(self.Inf, "mAk"))
        self.Loc_Noun.add_suffix_form(u"ndA", comes_after_P3 | comes_after_PointQual_Followed_By_A3Sg)

        self.NOUN_WITH_POSSESSION.add_out_suffix(self.Abl_Noun, self.NOUN_WITH_CASE)
        self.Abl_Noun.add_suffix_form(u"dAn", (doesnt_come_after_P3 & doesnt(comes_after_PointQual_Followed_By_A3Sg)) | comes_after_PointQual_Followed_By_A3Pl)
        self.Abl_Noun.add_suffix_form(u"ndAn", comes_after_P3 | comes_after_PointQual_Followed_By_A3Sg)

        self.NOUN_WITH_POSSESSION.add_out_suffix(self.Gen_Noun, self.NOUN_WITH_CASE)
        self.Gen_Noun.add_suffix_form(u"+nIn")

        self.NOUN_WITH_POSSESSION.add_out_suffix(self.Ins_Noun, self.NOUN_WITH_CASE)
        self.Ins_Noun.add_suffix_form(u"+ylA")

    def _register_noun_to_noun_derivations(self):
        self.NOUN_NOM_DERIV.add_out_suffix(self.Agt_Noun, self.NOUN_ROOT)
        self.Agt_Noun.add_suffix_form(u"cI")

        self.NOUN_NOM_DERIV.add_out_suffix(self.Dim, self.NOUN_ROOT)
        self.Dim.add_suffix_form(u"cIk")

        self.NOUN_NOM_DERIV.add_out_suffix(self.Prof, self.NOUN_ROOT)
        self.Prof.add_suffix_form(u"lIk")

        self.NOUN_NOM_DERIV.add_out_suffix(self.FitFor, self.NOUN_ROOT)
        self.FitFor.add_suffix_form(u"lIk")

        self.NOUN_NOM_DERIV.add_out_suffix(self.Title, self.NOUN_ROOT)
        self.Title.add_suffix_form(u"lIk")

    def _register_noun_to_verb_derivations(self):
        self.NOUN_NOM_DERIV.add_out_suffix(self.Acquire, self.VERB_ROOT)
        self.Acquire.add_suffix_form(u"lAn")

    def _register_noun_to_adjective_derivations(self):
        self.NOUN_NOM_DERIV.add_out_suffix(self.With, self.ADJECTIVE_ROOT)
        self.With.add_suffix_form(u"lI")

        self.NOUN_NOM_DERIV.add_out_suffix(self.Without, self.ADJECTIVE_ROOT)
        self.Without.add_suffix_form(u"sIz")

        self.NOUN_NOM_DERIV.add_out_suffix(self.JustLike_Noun, self.ADJECTIVE_ROOT)
        self.JustLike_Noun.add_suffix_form(u"+ImsI")

        self.NOUN_NOM_DERIV.add_out_suffix(self.Equ_Noun, self.ADJECTIVE_ROOT)
        self.Equ_Noun.add_suffix_form(u"cA")

        self.NOUN_NOM_DERIV.add_out_suffix(self.Y, self.ADJECTIVE_ROOT)
        self.Y.add_suffix_form(u"lIk")

        self.NOUN_NOM_DERIV.add_out_suffix(self.For, self.ADJECTIVE_ROOT)
        self.For.add_suffix_form(u"lIk")

        self.NOUN_NOM_DERIV.add_out_suffix(self.DurationOf, self.ADJECTIVE_ROOT)
        self.DurationOf.add_suffix_form(u"lIk")

        self.NOUN_NOM_DERIV.add_out_suffix(self.OfUnit_Noun, self.ADJECTIVE_ROOT)
        self.OfUnit_Noun.add_suffix_form(u"lIk")

        self.NOUN_DERIV_WITH_CASE.add_out_suffix(self.PointQual_Noun, self.ADJECTIVE_ROOT)
        self.PointQual_Noun.add_suffix_form(u"ki", comes_after(self.Loc_Noun))

    def _register_noun_to_adverb_derivations(self):
        self.NOUN_NOM_DERIV.add_out_suffix(self.InTermsOf, self.ADVERB_ROOT)
        self.InTermsOf.add_suffix_form(u"cA")

        self.NOUN_NOM_DERIV.add_out_suffix(self.By_Pnon, self.ADVERB_ROOT)
        self.By_Pnon.add_suffix_form(u"cA")

        self.NOUN_POSSESSIVE_NOM_DERIV.add_out_suffix(self.By_Possessive, self.ADVERB_ROOT)
        self.By_Possessive.add_suffix_form(u"ncA")

        self.NOUN_NOM_DERIV.add_out_suffix(self.ManyOf, self.ADVERB_ROOT)
        self.ManyOf.add_suffix_form(u"lArcA")

        self.NOUN_NOM_DERIV.add_out_suffix(self.ForALotOfTime, self.ADVERB_ROOT)
        self.ForALotOfTime.add_suffix_form(u"lArcA", precondition=root_has_secondary_syntactic_category(SecondarySyntacticCategory.TIME))

    def _register_noun_to_pronoun_derivations(self):
        comes_after_Gen_Noun = comes_after(self.Gen_Noun)   # since it only works for nouns after Gen : "masaninki", "kardesiminkiler"
        followed_by_Pnon_Pron = followed_by(self.Pnon_Pron) # since sth like this doesn't work: "masanınkim"

        self.NOUN_DERIV_WITH_CASE.add_out_suffix(self.RelPron_A3Sg_Noun, self.PRONOUN_WITH_AGREEMENT)
        self.RelPron_A3Sg_Noun.add_suffix_form(u"ki", comes_after_Gen_Noun, followed_by_Pnon_Pron)

        self.NOUN_DERIV_WITH_CASE.add_out_suffix(self.RelPron_A3Pl_Noun, self.PRONOUN_WITH_AGREEMENT)
        self.RelPron_A3Pl_Noun.add_suffix_form(u"kiler", comes_after_Gen_Noun, followed_by_Pnon_Pron)

    def _register_noun_compound_suffixes(self):
        self.NOUN_COMPOUND_ROOT.add_out_suffix(self.A3Sg_Noun_Compound, self.NOUN_COMPOUND_WITH_AGREEMENT)
        self.A3Sg_Noun_Compound.add_suffix_form(u"")

        self.NOUN_COMPOUND_WITH_AGREEMENT.add_out_suffix(self.P3Sg_Noun_Compound, self.NOUN_WITH_POSSESSION)
        self.P3Sg_Noun_Compound.add_suffix_form(u"+sI")

        self.NOUN_COMPOUND_WITH_AGREEMENT.add_out_suffix(self.P3Pl_Noun_Compound, self.NOUN_WITH_POSSESSION)
        self.P3Pl_Noun_Compound.add_suffix_form(u"lArI!")

        self.NOUN_COMPOUND_WITH_AGREEMENT.add_out_suffix(self.PNon_Noun_Compound, self.NOUN_COMPOUND_WITH_POSSESSION)
        self.PNon_Noun_Compound.add_suffix_form(u"")

        self.NOUN_COMPOUND_WITH_POSSESSION.add_out_suffix(self.Nom_Noun_Compound_Deriv, self.NOUN_NOM_DERIV)
        self.Nom_Noun_Compound_Deriv.add_suffix_form(u"")

    def _register_verb_polarisations(self):
        self.VERB_ROOT.add_out_suffix(self.Negative, self.VERB_WITH_POLARITY)
        self.Negative.add_suffix_form(u"m", postcondition=doesnt(followed_by_suffix_goes_to(State.DERIVATIONAL)))
        self.Negative.add_suffix_form(u"mA")

        self.VERB_ROOT.add_out_suffix(self.Positive, self.VERB_WITH_POLARITY)
        self.Positive.add_suffix_form("")

    def _register_verb_tenses(self):
        followed_by_A1Sg_A1Pl = followed_by(self.A1Sg_Verb, u'+Im') | followed_by(self.A1Pl_Verb, u'yIz')

        self.Aorist.add_suffix_form(u"+Ir", has_root_attribute(RootAttribute.Aorist_I) & doesnt_come_after(self.Negative))
        self.Aorist.add_suffix_form(u"+Ar", doesnt_come_after(self.Negative))
        self.Aorist.add_suffix_form(u"z", comes_after(self.Negative), doesnt(followed_by_A1Sg_A1Pl))    # gel-me-z or gel-me-z-sin
        self.Aorist.add_suffix_form(u"", comes_after(self.Negative), followed_by_A1Sg_A1Pl)     # gel-me-m or gel-me-yiz

        self.Progressive.add_suffix_form(u"Iyor")
        self.Progressive.add_suffix_form(u"mAktA")

        self.Future.add_suffix_form(u"+yAcAk")

        self.Narr.add_suffix_form(u"mIş")
        self.Narr.add_suffix_form(u"ymIş")

        self.Past.add_suffix_form(u"dI")
        self.Past.add_suffix_form(u"ydI")

        self.Cond.add_suffix_form(u"+ysA")

        self.Imp.add_suffix_form(u"", postcondition=followed_by(self.A2Sg_Verb) | followed_by(self.A3Sg_Verb) | followed_by(self.A2Pl_Verb) | followed_by(self.A3Pl_Verb))
        self.Imp.add_suffix_form(u"sAnA", postcondition=followed_by(self.A2Sg_Verb))
        self.Imp.add_suffix_form(u"sAnIzA", postcondition=followed_by(self.A2Pl_Verb))

        self.Pres.add_suffix_form(u"")

        self.VERB_WITH_POLARITY.add_out_suffix(self.Aorist, self.VERB_WITH_TENSE)
        self.VERB_WITH_POLARITY.add_out_suffix(self.Progressive, self.VERB_WITH_TENSE)
        self.VERB_WITH_POLARITY.add_out_suffix(self.Future, self.VERB_WITH_TENSE)
        self.VERB_WITH_POLARITY.add_out_suffix(self.Narr, self.VERB_WITH_TENSE)
        self.VERB_WITH_POLARITY.add_out_suffix(self.Past, self.VERB_WITH_TENSE)
        self.VERB_WITH_POLARITY.add_out_suffix(self.Cond, self.VERB_WITH_TENSE)
        self.VERB_WITH_POLARITY.add_out_suffix(self.Imp, self.VERB_WITH_TENSE)

        self.VERB_WITH_TENSE.add_out_suffix(self.Cond, self.VERB_WITH_TENSE)
        self.VERB_WITH_TENSE.add_out_suffix(self.Narr, self.VERB_WITH_TENSE)
        self.VERB_WITH_TENSE.add_out_suffix(self.Past, self.VERB_WITH_TENSE)

    def _register_verb_agreements(self):
        comes_after_imperative = comes_after(self.Imp)
        doesnt_come_after_imperative = doesnt(comes_after_imperative)
        comes_after_empty_imperative = comes_after(self.Imp, u"")
        doesnt_come_after_empty_imperative = doesnt(comes_after_empty_imperative)

        self.VERB_WITH_TENSE.add_out_suffix(self.A1Sg_Verb, self.VERB_TERMINAL_TRANSFER)
        self.A1Sg_Verb.add_suffix_form("+Im")
        self.A1Sg_Verb.add_suffix_form("yIm")   #"yap-makta-yım", gel-meli-yim

        self.VERB_WITH_TENSE.add_out_suffix(self.A2Sg_Verb, self.VERB_TERMINAL_TRANSFER)
        self.A2Sg_Verb.add_suffix_form("n", doesnt_come_after_imperative & doesnt_come_after(self.Opt))
        self.A2Sg_Verb.add_suffix_form("sIn", doesnt_come_after_imperative)
        self.A2Sg_Verb.add_suffix_form("", comes_after_imperative)

        self.VERB_WITH_TENSE.add_out_suffix(self.A3Sg_Verb, self.VERB_TERMINAL_TRANSFER)
        self.A3Sg_Verb.add_suffix_form("", doesnt_come_after_imperative)
        self.A3Sg_Verb.add_suffix_form("sIn", comes_after_imperative)

        self.VERB_WITH_TENSE.add_out_suffix(self.A1Pl_Verb, self.VERB_TERMINAL_TRANSFER)
        self.A1Pl_Verb.add_suffix_form("+Iz", doesnt_come_after(self.Opt))
        self.A1Pl_Verb.add_suffix_form("k",   doesnt_come_after(self.Opt))   # only for "gel-di-k"
        self.A1Pl_Verb.add_suffix_form("yIz", doesnt_come_after(self.Opt))   # "yap-makta-yız" OR "gel-me-yiz"
        self.A1Pl_Verb.add_suffix_form("lIm", comes_after(self.Opt))         # only for "gel-e-lim"

        self.VERB_WITH_TENSE.add_out_suffix(self.A2Pl_Verb, self.VERB_TERMINAL_TRANSFER)
        self.A2Pl_Verb.add_suffix_form("", comes_after_imperative & doesnt_come_after_empty_imperative)
        self.A2Pl_Verb.add_suffix_form("sInIz", doesnt_come_after_imperative)
        self.A2Pl_Verb.add_suffix_form("nIz", doesnt_come_after_imperative)
        self.A2Pl_Verb.add_suffix_form("+yIn", comes_after_empty_imperative)
        self.A2Pl_Verb.add_suffix_form("+yInIz", comes_after_empty_imperative)

        self.VERB_WITH_TENSE.add_out_suffix(self.A3Pl_Verb, self.VERB_TERMINAL_TRANSFER)
        self.A3Pl_Verb.add_suffix_form("lAr", doesnt_come_after_imperative)
        self.A3Pl_Verb.add_suffix_form("sInlAr", comes_after_imperative)

    def _register_modal_verbs(self):
        followed_by_modal_followers = followed_by(self.Past) | followed_by(self.Narr) | followed_by_one_from_group(self.Verb_Agreements_Group)

        self.VERB_WITH_POLARITY.add_out_suffix(self.Neces, self.VERB_WITH_TENSE)
        self.Neces.add_suffix_form(u"mAlI!")

        self.VERB_WITH_POLARITY.add_out_suffix(self.Opt, self.VERB_WITH_TENSE)
        self.Opt.add_suffix_form(u"Ay")
        self.Opt.add_suffix_form(u"A", doesnt_come_after(self.Negative), followed_by_modal_followers)
        self.Opt.add_suffix_form(u"yAy")
        self.Opt.add_suffix_form(u"yA", postcondition=followed_by_modal_followers)

        self.VERB_WITH_POLARITY.add_out_suffix(self.Desr, self.VERB_WITH_TENSE)
        self.Desr.add_suffix_form(u"sA")

    def _register_verb_to_verb_derivations(self):
        self.VERB_PLAIN_DERIV.add_out_suffix(self.Able, self.VERB_ROOT)
        self.Able.add_suffix_form(u"+yAbil", postcondition=doesnt(followed_by(self.Negative)))
        self.Able.add_suffix_form(u"+yA", postcondition=followed_by(self.Negative))

        self.VERB_POLARITY_DERIV.add_out_suffix(self.Hastily, self.VERB_ROOT)
        self.Hastily.add_suffix_form(u"+yIver")

        root_can_have_passive = doesnt_have_root_attribute(RootAttribute.Passive_NotApplicable)
        passive_Il = doesnt_have_root_attribute(RootAttribute.Passive_In) & doesnt_have_root_attribute(RootAttribute.Passive_InIl)
        self.VERB_PLAIN_DERIV.add_out_suffix(self.Pass, self.VERB_ROOT)
        self.Pass.add_suffix_form(u"+In", root_can_have_passive & has_root_attribute(RootAttribute.Passive_In))
        self.Pass.add_suffix_form(u"+nIl", root_can_have_passive & passive_Il)
        self.Pass.add_suffix_form(u"+InIl", root_can_have_passive & has_root_attribute(RootAttribute.Passive_InIl))

        self.VERB_PLAIN_DERIV.add_out_suffix(self.Recip, self.VERB_ROOT)
        self.Recip.add_suffix_form(u"+Iş", post_derivation_condition=doesnt(followed_by_derivation(self.Caus)))

        self.VERB_PLAIN_DERIV.add_out_suffix(self.Caus, self.VERB_ROOT)
        self.Caus.add_suffix_form(u"t",  has_root_attribute(RootAttribute.Causative_t) & doesnt_come_after_derivation(self.Caus, "t") & doesnt_come_after_derivation(self.Caus, "It"))
        self.Caus.add_suffix_form(u"Ir", has_root_attribute(RootAttribute.Causative_Ir) & doesnt_come_after_derivation(self.Able))
        self.Caus.add_suffix_form(u"It", has_root_attribute(RootAttribute.Causative_It) & doesnt_come_after_derivation(self.Able))
        self.Caus.add_suffix_form(u"Ar", has_root_attribute(RootAttribute.Causative_Ar) & doesnt_come_after_derivation(self.Able))
        self.Caus.add_suffix_form(u"dIr", has_root_attribute(RootAttribute.Causative_dIr))

    def _register_verb_to_noun_derivations(self):
        self.VERB_POLARITY_DERIV.add_out_suffix(self.Inf, self.NOUN_ROOT)
        self.Inf.add_suffix_form(u"mAk")
        self.Inf.add_suffix_form(u"mA")
        self.Inf.add_suffix_form(u"+yIş")

        self.VERB_POLARITY_DERIV.add_out_suffix(self.PastPart_Noun, self.NOUN_ROOT)
        self.PastPart_Noun.add_suffix_form(u"dIk")

        self.VERB_POLARITY_DERIV.add_out_suffix(self.FutPart_Noun, self.NOUN_ROOT)
        self.FutPart_Noun.add_suffix_form(u'+yAcAk')

    def _register_verb_to_adverb_derivations(self):
        self.VERB_POLARITY_DERIV.add_out_suffix(self.AfterDoingSo, self.ADVERB_ROOT)
        self.AfterDoingSo.add_suffix_form(u"+yIp")

        self.VERB_POLARITY_DERIV.add_out_suffix(self.WithoutHavingDoneSo, self.ADVERB_ROOT)
        self.WithoutHavingDoneSo.add_suffix_form(u"mAdAn")
        self.WithoutHavingDoneSo.add_suffix_form(u"mAksIzIn")

        self.VERB_POLARITY_DERIV.add_out_suffix(self.AsLongAs, self.ADVERB_ROOT)
        self.AsLongAs.add_suffix_form(u"dIkçA")

        self.VERB_POLARITY_DERIV.add_out_suffix(self.ByDoingSo, self.ADVERB_ROOT)
        self.ByDoingSo.add_suffix_form(u"+yArAk")

        self.VERB_POLARITY_DERIV.add_out_suffix(self.When, self.ADVERB_ROOT)
        self.When.add_suffix_form(u"+yIncA")

        self.VERB_POLARITY_DERIV.add_out_suffix(self.SinceDoingSo, self.ADVERB_ROOT)
        self.SinceDoingSo.add_suffix_form(u"+yAlI!")

        self.VERB_TENSE_DERIV.add_out_suffix(self.While, self.ADVERB_ROOT)
        self.While.add_suffix_form(u"ken")

        self.VERB_TENSE_DERIV.add_out_suffix(self.AsIf, self.ADVERB_ROOT)
        self.AsIf.add_suffix_form(u"cAsInA", comes_after(self.Aorist) | comes_after(self.Progressive) | comes_after(self.Future) | comes_after(self.Narr))

    def _register_verb_to_adjective_derivations(self):
        self.VERB_POLARITY_DERIV.add_out_suffix(self.PresPart, self.ADJECTIVE_ROOT)
        self.PresPart.add_suffix_form(u'+yAn')

        self.VERB_POLARITY_DERIV.add_out_suffix(self.PastPart_Adj, self.ADJECTIVE_PART_WITHOUT_POSSESSION)
        self.PastPart_Adj.add_suffix_form(u'dIk')

        self.VERB_POLARITY_DERIV.add_out_suffix(self.FutPart_Adj, self.ADJECTIVE_PART_WITHOUT_POSSESSION)
        self.FutPart_Adj.add_suffix_form(u'+yAcAk')

        self.VERB_POLARITY_DERIV.add_out_suffix(self.Agt_Adj, self.ADJECTIVE_ROOT)
        self.Agt_Adj.add_suffix_form(u"+yIcI")


        self.VERB_WITH_POLARITY.add_out_suffix(self.Aorist_to_Adj, self.VERB_TENSE_ADJ_DERIV)
        self.Aorist_to_Adj.add_suffix_form(u"+Ir", has_root_attribute(RootAttribute.Aorist_I))
        self.Aorist_to_Adj.add_suffix_form(u"+Ar")
        self.Aorist_to_Adj.add_suffix_form(u"z", comes_after(self.Negative))    # gel-me-z

        self.VERB_WITH_POLARITY.add_out_suffix(self.Narr_to_Adj, self.VERB_TENSE_ADJ_DERIV)
        self.Narr_to_Adj.add_suffix_form(u"mIş")
        self.Narr_to_Adj.add_suffix_form(u"ymIş")

    def _register_adjective_to_adjective_derivations(self):
        self.ADJECTIVE_DERIV.add_out_suffix(self.JustLike_Adj, self.ADJECTIVE_ROOT)
        self.JustLike_Adj.add_suffix_form(u"+ImsI")

        self.ADJECTIVE_DERIV.add_out_suffix(self.Equ_Adj, self.ADJECTIVE_ROOT)
        self.Equ_Adj.add_suffix_form(u"cA")

        self.ADJECTIVE_DERIV.add_out_suffix(self.Quite, self.ADJECTIVE_ROOT)
        self.Quite.add_suffix_form(u"cA")

    def _register_adjective_to_adverb_derivations(self):
        self.ADJECTIVE_DERIV.add_out_suffix(self.Ly, self.ADVERB_ROOT)
        self.Ly.add_suffix_form(u"cA")

    def _register_adjective_to_noun_derivations(self):
        self.ADJECTIVE_DERIV.add_out_suffix(self.Ness, self.NOUN_ROOT)
        self.Ness.add_suffix_form(u"lIk")

    def _register_adjective_to_verb_derivations(self):
        self.ADJECTIVE_DERIV.add_out_suffix(self.Become, self.VERB_ROOT)
        self.Become.add_suffix_form(u"lAş")

    def _register_adjective_possessions(self):
        self.ADJECTIVE_PART_WITHOUT_POSSESSION.add_out_suffix(self.Pnon_Adj, self.ADJECTIVE_TERMINAL_TRANSFER)
        self.Pnon_Adj.add_suffix_form("")

        self.ADJECTIVE_PART_WITHOUT_POSSESSION.add_out_suffix(self.P1Sg_Adj, self.ADJECTIVE_TERMINAL_TRANSFER)
        self.P1Sg_Adj.add_suffix_form("+Im")

        self.ADJECTIVE_PART_WITHOUT_POSSESSION.add_out_suffix(self.P2Sg_Adj, self.ADJECTIVE_TERMINAL_TRANSFER)
        self.P2Sg_Adj.add_suffix_form("+In")

        self.ADJECTIVE_PART_WITHOUT_POSSESSION.add_out_suffix(self.P3Sg_Adj, self.ADJECTIVE_TERMINAL_TRANSFER)
        self.P3Sg_Adj.add_suffix_form("+sI")

        self.ADJECTIVE_PART_WITHOUT_POSSESSION.add_out_suffix(self.P1Pl_Adj, self.ADJECTIVE_TERMINAL_TRANSFER)
        self.P1Pl_Adj.add_suffix_form("+ImIz")

        self.ADJECTIVE_PART_WITHOUT_POSSESSION.add_out_suffix(self.P2Pl_Adj, self.ADJECTIVE_TERMINAL_TRANSFER)
        self.P2Pl_Adj.add_suffix_form("+InIz")

        self.ADJECTIVE_PART_WITHOUT_POSSESSION.add_out_suffix(self.P3Pl_Adj, self.ADJECTIVE_TERMINAL_TRANSFER)
        self.P3Pl_Adj.add_suffix_form("lArI!")

    def _register_pronoun_agreements(self):
        self.PRONOUN_ROOT.add_out_suffix(self.A1Sg_Pron, self.PRONOUN_WITH_AGREEMENT)
        #A1Sg_Pron forms are predefined, 'ben' and 'kendi'

        self.PRONOUN_ROOT.add_out_suffix(self.A2Sg_Pron, self.PRONOUN_WITH_AGREEMENT)
        #A2Sg_Pron forms are predefined, 'sen' and 'kendi'

        self.PRONOUN_ROOT.add_out_suffix(self.A3Sg_Pron, self.PRONOUN_WITH_AGREEMENT)
        self.A3Sg_Pron.add_suffix_form("")
        #A3Sg_Pron forms for 'o', 'bu', 'su', 'kendi' are predefined

        self.PRONOUN_ROOT.add_out_suffix(self.A1Pl_Pron, self.PRONOUN_WITH_AGREEMENT)
        #A1Pl_Pron forms are predefined, 'biz' and 'kendi'

        self.PRONOUN_ROOT.add_out_suffix(self.A2Pl_Pron, self.PRONOUN_WITH_AGREEMENT)
        #A2Pl_Pron forms are predefined, 'siz' and 'kendi'

        self.PRONOUN_ROOT.add_out_suffix(self.A3Pl_Pron, self.PRONOUN_WITH_AGREEMENT)
        self.A3Pl_Pron.add_suffix_form("lAr")
        #A3Pl_Pron forms for 'onlar', 'bunlar', 'sunlar', 'kendileri' are predefined


    def _register_pronoun_possessions(self):
        self.PRONOUN_WITH_AGREEMENT.add_out_suffix(self.Pnon_Pron, self.PRONOUN_WITH_POSSESSION)
        self.Pnon_Pron.add_suffix_form("")
        #Pnon_Pron forms for 'ben', 'sen', 'o', 'biz', 'siz', 'onlar', 'bu', 'su', 'kendi' are predefined

        self.PRONOUN_WITH_AGREEMENT.add_out_suffix(self.P1Sg_Pron, self.PRONOUN_WITH_POSSESSION)
        self.P1Sg_Pron.add_suffix_form("+Im")
        #P1Sg_Pron forms for 'ben', 'sen', 'o', 'biz', 'siz', 'onlar', 'bu', 'su', 'kendi' are predefined

        self.PRONOUN_WITH_AGREEMENT.add_out_suffix(self.P2Sg_Pron, self.PRONOUN_WITH_POSSESSION)
        self.P2Sg_Pron.add_suffix_form("+In")
        #P2Sg_Pron forms for 'ben', 'sen', 'o', 'biz', 'siz', 'onlar', 'bu', 'su', 'kendi' are predefined

        self.PRONOUN_WITH_AGREEMENT.add_out_suffix(self.P3Sg_Pron, self.PRONOUN_WITH_POSSESSION)
        self.P3Sg_Pron.add_suffix_form("+sI")
        #P3Sg_Pron forms for 'ben', 'sen', 'o', 'biz', 'siz', 'onlar', 'bu', 'su', 'kendi' are predefined

        self.PRONOUN_WITH_AGREEMENT.add_out_suffix(self.P1Pl_Pron, self.PRONOUN_WITH_POSSESSION)
        self.P1Pl_Pron.add_suffix_form("+ImIz")
        #P1Pl_Pron forms for 'ben', 'sen', 'o', 'biz', 'siz', 'onlar', 'bu', 'su', 'kendi' are predefined

        self.PRONOUN_WITH_AGREEMENT.add_out_suffix(self.P2Pl_Pron, self.PRONOUN_WITH_POSSESSION)
        self.P2Pl_Pron.add_suffix_form("+InIz")
        #P2Pl_Pron forms for 'ben', 'sen', 'o', 'biz', 'siz', 'onlar', 'bu', 'su', 'kendi' are predefined

        self.PRONOUN_WITH_AGREEMENT.add_out_suffix(self.P3Pl_Pron, self.PRONOUN_WITH_POSSESSION)
        self.P3Pl_Pron.add_suffix_form("lArI!")
        self.P3Pl_Pron.add_suffix_form("I!", comes_after(self.A3Pl_Pron))
        #P3Pl_Pron forms for "'ben', 'sen', 'o', 'biz', 'siz', 'onlar', 'bu', 'su', 'kendi' are predefined

    def _register_pronoun_cases(self):
        comes_after_P3 = comes_after(self.P3Sg_Pron) | comes_after(self.P3Pl_Pron) | \
                         comes_after_derivation(self.RelPron_A3Sg_Noun) | comes_after_derivation(self.RelPron_A3Sg_Pron)
        doesnt_come_after_P3 = ~comes_after_P3

        self.PRONOUN_WITH_POSSESSION.add_out_suffix(self.Nom_Pron, self.PRONOUN_WITH_CASE)
        self.Nom_Pron.add_suffix_form("")

        self.PRONOUN_WITH_POSSESSION.add_out_suffix(self.Nom_Pron_Deriv, self.PRONOUN_NOM_DERIV)
        self.Nom_Pron_Deriv.add_suffix_form("", comes_after(self.Pnon_Pron))

        self.PRONOUN_WITH_POSSESSION.add_out_suffix(self.Acc_Pron, self.PRONOUN_WITH_CASE)
        self.Acc_Pron.add_suffix_form(u"+yI", doesnt_come_after_P3)
        self.Acc_Pron.add_suffix_form(u"nI", comes_after_P3)
        #Acc_Pron forms for 'ben', 'sen', 'o', 'biz', 'siz', 'onlar', 'bu', 'su', 'kendi' are predefined

        self.PRONOUN_WITH_POSSESSION.add_out_suffix(self.Dat_Pron, self.PRONOUN_WITH_CASE)
        self.Dat_Pron.add_suffix_form(u"+yA", doesnt_come_after_P3)
        self.Dat_Pron.add_suffix_form(u"nA", comes_after_P3)
        #Dat_Pron forms for 'ben', 'sen', 'o', 'biz', 'siz', 'onlar', 'bu', 'su', 'kendi' are predefined

        self.PRONOUN_WITH_POSSESSION.add_out_suffix(self.Loc_Pron, self.PRONOUN_WITH_CASE)
        self.Loc_Pron.add_suffix_form(u"dA", doesnt_come_after_P3)
        self.Loc_Pron.add_suffix_form(u"ndA", comes_after_P3)
        #Loc_Pron forms for 'ben', 'sen', 'o', 'biz', 'siz', 'onlar', 'bu', 'su', 'kendi' are predefined

        self.PRONOUN_WITH_POSSESSION.add_out_suffix(self.Abl_Pron, self.PRONOUN_WITH_CASE)
        self.Abl_Pron.add_suffix_form(u"dAn", doesnt_come_after_P3)
        self.Abl_Pron.add_suffix_form(u"ndAn", comes_after_P3)
        #Abl_Pron forms for 'ben', 'sen', 'o', 'biz', 'siz', 'onlar', 'bu', 'su', 'kendi' are predefined

        self.PRONOUN_WITH_POSSESSION.add_out_suffix(self.Gen_Pron, self.PRONOUN_WITH_CASE)
        self.Gen_Pron.add_suffix_form(u"+nIn")
        #Gen_Pron forms for 'ben', 'sen', 'o', 'biz', 'siz', 'onlar', 'bu', 'su', 'kendi' are predefined

        self.PRONOUN_WITH_POSSESSION.add_out_suffix(self.Ins_Pron, self.PRONOUN_WITH_CASE)
        self.Ins_Pron.add_suffix_form(u"+ylA")
        #Ins_Pron forms for 'ben', 'sen', 'o', 'biz', 'siz', 'onlar', 'bu', 'su', 'kendi' are predefined

        self.PRONOUN_WITH_POSSESSION.add_out_suffix(self.AccordingTo, self.PRONOUN_WITH_CASE)
        self.AccordingTo.add_suffix_form(u"cA")
        #AccordingTo forms for 'ben', 'sen', 'o', 'biz', 'siz', 'onlar', 'bu', 'su', 'hepsi' are predefined

    def _register_pronoun_to_adjective_suffixes(self):
        applies_to_bu_su_o = applies_to_root('o') | applies_to_root('bu') | applies_to_root(u'şu')

        comes_after_A3Sg_pnon = comes_after(self.A3Sg_Pron) & comes_after(self.Pnon_Pron)

        comes_after_bu_su_o_pnon = comes_after_A3Sg_pnon & applies_to_bu_su_o

        self.PRONOUN_NOM_DERIV.add_out_suffix(self.Without_Pron, self.ADJECTIVE_ROOT)
        self.Without_Pron.add_suffix_form(u"sIz", doesnt(comes_after_bu_su_o_pnon))  # ben-siz, onlar-siz
        self.Without_Pron.add_suffix_form(u"nsuz", comes_after_bu_su_o_pnon)         # o-nsuz, bu-nsuz, su-nsuz

        self.PRONOUN_DERIV_WITH_CASE.add_out_suffix(self.PointQual_Pron, self.ADJECTIVE_ROOT)
        self.PointQual_Pron.add_suffix_form(u"ki", comes_after(self.Loc_Pron))

    def _register_pronoun_to_pronoun_derivations(self):
        comes_after_Gen_Pron = comes_after(self.Gen_Pron)   # since it only works for pronouns after Gen : "oraninki", "senin oraninki", "benimki"
        followed_by_Pnon_Pron = followed_by(self.Pnon_Pron) # since sth like this doesn't work: "oraninkim", "benimkin"

        self.PRONOUN_DERIV_WITH_CASE.add_out_suffix(self.RelPron_A3Sg_Noun, self.PRONOUN_WITH_AGREEMENT)
        self.RelPron_A3Sg_Noun.add_suffix_form(u"ki", comes_after_Gen_Pron, followed_by_Pnon_Pron)

        self.PRONOUN_DERIV_WITH_CASE.add_out_suffix(self.RelPron_A3Pl_Noun, self.PRONOUN_WITH_AGREEMENT)
        self.RelPron_A3Pl_Noun.add_suffix_form(u"kiler", comes_after_Gen_Pron, followed_by_Pnon_Pron)

    def _register_adverb_to_adjective_derivations(self):
        PointQual_form_ku_applicable = applies_to_root(u'bugün') | applies_to_root(u'dün') | applies_to_root(u'gün') | applies_to_root(u'öbür')
        #TODO: only applies to time adverbs

        self.ADVERB_DERIV.add_out_suffix(self.PointQual_Adv, self.ADJECTIVE_ROOT)
        self.PointQual_Adv.add_suffix_form(u"ki", doesnt(PointQual_form_ku_applicable))
        self.PointQual_Adv.add_suffix_form(u"kü", PointQual_form_ku_applicable)

    def _register_question_tenses(self):
        # Question tenses are all predefined
        self.QUESTION_ROOT.add_out_suffix(self.Pres_Ques, self.QUESTION_WITH_AGREEMENT)
        self.QUESTION_ROOT.add_out_suffix(self.Narr_Ques, self.QUESTION_WITH_AGREEMENT)
        self.QUESTION_ROOT.add_out_suffix(self.Past_Ques, self.QUESTION_WITH_AGREEMENT)

    def _register_question_agreements(self):
        # Question agreements are all predefined
        self.QUESTION_WITH_AGREEMENT.add_out_suffix(self.A1Sg_Ques, self.VERB_TERMINAL_TRANSFER)
        self.QUESTION_WITH_AGREEMENT.add_out_suffix(self.A2Sg_Ques, self.VERB_TERMINAL_TRANSFER)
        self.QUESTION_WITH_AGREEMENT.add_out_suffix(self.A3Sg_Ques, self.VERB_TERMINAL_TRANSFER)
        self.QUESTION_WITH_AGREEMENT.add_out_suffix(self.A1Pl_Ques, self.VERB_TERMINAL_TRANSFER)
        self.QUESTION_WITH_AGREEMENT.add_out_suffix(self.A2Pl_Ques, self.VERB_TERMINAL_TRANSFER)
        self.QUESTION_WITH_AGREEMENT.add_out_suffix(self.A3Pl_Ques, self.VERB_TERMINAL_TRANSFER)

    def _register_cardinal_to_adjective_suffixes(self):
        self.NUMERAL_CARDINAL_DERIV.add_out_suffix(self.NumbersOf, self.ADJECTIVE_ROOT)
        self.NumbersOf.add_suffix_form(u"lArcA")

        self.NUMERAL_CARDINAL_DERIV.add_out_suffix(self.OfUnit_Number, self.ADJECTIVE_ROOT)
        self.OfUnit_Number.add_suffix_form(u"lIk")

    def _register_digits_suffixes(self):
        self.NUMERAL_DIGIT_CARDINAL_ROOT.add_out_suffix(self.Apos_Digit, self.NUMERAL_CARDINAL_DERIV)
        self.Apos_Digit.add_suffix_form(u"'")