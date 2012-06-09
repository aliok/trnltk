# coding=utf-8
from trnltk.stem.dictionaryitem import RootAttribute
from trnltk.suffixgraph.suffixconditions import comes_after, followed_by, applies_to_stem, doesnt_come_after, doesnt, followed_by_suffix, that_goes_to, requires_root_attribute, doesnt_come_after_derivation, followed_by_derivation, followed_by_one_from_group
from trnltk.suffixgraph.suffixgraphmodel import *

NOUN_ROOT = State("NOUN_ROOT", 'Noun', State.TRANSFER)
NOUN_WITH_AGREEMENT = State("NOUN_WITH_AGREEMENT", 'Noun', State.TRANSFER)
NOUN_WITH_POSSESSION = State("NOUN_WITH_POSSESSION", 'Noun', State.TRANSFER)
NOUN_WITH_CASE = State("NOUN_WITH_CASE", 'Noun', State.TRANSFER)
NOUN_TERMINAL = State("NOUN_TERMINAL", 'Noun', State.TERMINAL)
NOUN_NOM_DERIV = State("NOUN_NOM_DERIV", 'Noun', State.DERIV)
NOUN_DERIV_WITH_CASE = State("NOUN_DERIV_WITH_CASE", 'Noun', State.DERIV)

VERB_ROOT = State("VERB_ROOT", 'Verb', State.TRANSFER)
VERB_WITH_POLARITY = State("VERB_WITH_POLARITY", 'Verb', State.TRANSFER)
VERB_WITH_TENSE = State("VERB_WITH_TENSE", 'Verb', State.TRANSFER)
VERB_TERMINAL = State("VERB_TERMINAL", 'Verb', State.TERMINAL)
VERB_PLAIN_DERIV = State("VERB_PLAIN_DERIV", 'Verb', State.DERIV)
VERB_POLARITY_DERIV = State("VERB_POLARITY_DERIV", 'Verb', State.DERIV)
VERB_TENSE_DERIV = State("VERB_TENSE_DERIV", 'Verb', State.DERIV)

ADJECTIVE_ROOT = State("ADJECTIVE_ROOT", 'Adj', State.TRANSFER)
ADJECTIVE_PART_WITHOUT_POSSESSION = State("ADJECTIVE_PART_WITHOUT_POSSESSION", 'Adj', State.TRANSFER)
ADJECTIVE_TERMINAL = State("ADJECTIVE_TERMINAL", 'Adj', State.TERMINAL)
ADJECTIVE_DERIV = State("ADJECTIVE_DERIV", 'Adj', State.DERIV)

ADVERB_ROOT = State("ADVERB_ROOT", 'Adv', State.TRANSFER)
ADVERB_TERMINAL = State("ADVERB_TERMINAL", 'Adv', State.TERMINAL)
ADVERB_DERIV = State("ADVERB_DERIV", 'Adv', State.DERIV)

PRONOUN_ROOT = State("PRONOUN_ROOT", 'Pron', State.TRANSFER)
PRONOUN_WITH_AGREEMENT = State("PRONOUN_WITH_AGREEMENT", 'Pron', State.TRANSFER)
PRONOUN_WITH_POSSESSION = State("PRONOUN_WITH_POSSESSION", 'Pron', State.TRANSFER)
PRONOUN_WITH_CASE = State("PRONOUN_WITH_CASE", 'Pron', State.TRANSFER)
PRONOUN_NOM_DERIV = State("PRONOUN_NOM_DERIV", 'Pron', State.DERIV)
PRONOUN_TERMINAL = State("PRONOUN_TERMINAL", 'Pron', State.TERMINAL)

DETERMINER_ROOT_TERMINAL = State("DETERMINER_ROOT_TERMINAL", "Det", State.TERMINAL)

INTERJECTION_ROOT_TERMINAL = State("INTERJECTION_ROOT_TERMINAL", "Interj", State.TERMINAL)

CONJUNCTION_ROOT_TERMINAL = State("CONJUNCTION_ROOT_TERMINAL", "Conj", State.TERMINAL)

NUMERAL_ROOT = State("NUMERAL_ROOT", "Num", State.TRANSFER)
NUMERAL_DERIV = State("NUMERAL_DERIV", "Num", State.DERIV)

PUNC_ROOT_TERMINAL = State("PUNC_ROOT_TERMINAL", 'Punc', State.TERMINAL)

ALL_STATES = {
    NOUN_ROOT, NOUN_WITH_AGREEMENT, NOUN_WITH_POSSESSION, NOUN_WITH_CASE, NOUN_TERMINAL, NOUN_DERIV_WITH_CASE, NOUN_NOM_DERIV,
    VERB_ROOT, VERB_WITH_POLARITY, VERB_WITH_TENSE, VERB_TERMINAL, VERB_PLAIN_DERIV, VERB_POLARITY_DERIV, VERB_TENSE_DERIV,
    ADJECTIVE_ROOT, ADJECTIVE_PART_WITHOUT_POSSESSION, ADJECTIVE_TERMINAL, ADJECTIVE_DERIV,
    ADVERB_ROOT, ADVERB_TERMINAL, ADVERB_DERIV,
    PRONOUN_ROOT, PRONOUN_WITH_AGREEMENT, PRONOUN_WITH_POSSESSION, PRONOUN_WITH_CASE, PRONOUN_TERMINAL, PRONOUN_NOM_DERIV,
    DETERMINER_ROOT_TERMINAL,
    INTERJECTION_ROOT_TERMINAL,
    CONJUNCTION_ROOT_TERMINAL,
    NUMERAL_ROOT, NUMERAL_DERIV,
    PUNC_ROOT_TERMINAL
}

#############  Empty transitions
FreeTransitionSuffix("Noun_Free_Transition_1", NOUN_WITH_CASE, NOUN_TERMINAL)
FreeTransitionSuffix("Noun_Free_Transition_2", NOUN_WITH_CASE, NOUN_DERIV_WITH_CASE)
FreeTransitionSuffix("Verb_Free_Transition_1", VERB_ROOT, VERB_PLAIN_DERIV)
FreeTransitionSuffix("Verb_Free_Transition_2", VERB_WITH_POLARITY, VERB_POLARITY_DERIV)
FreeTransitionSuffix("Verb_Free_Transition_3", VERB_WITH_TENSE, VERB_TENSE_DERIV)
FreeTransitionSuffix("Adj_Free_Transition_1", ADJECTIVE_ROOT, ADJECTIVE_TERMINAL)
FreeTransitionSuffix("Adj_Free_Transition_2", ADJECTIVE_ROOT, ADJECTIVE_DERIV)
FreeTransitionSuffix("Adv_Free_Transition", ADVERB_ROOT, ADVERB_TERMINAL)
FreeTransitionSuffix("Pronoun_Free_Transition", PRONOUN_WITH_CASE, PRONOUN_TERMINAL)
FreeTransitionSuffix("Numeral_Free_Transition", NUMERAL_ROOT, NUMERAL_DERIV)
ZeroTransitionSuffix("Numeral_Zero_Transition", NUMERAL_DERIV, ADJECTIVE_ROOT)
#TODO: transition from numeral to adverb for case "birer birer geldiler?" hmm maybe duplication caused an adj->adv transition?

#############  Noun Agreements
Noun_Agreements_Group = SuffixGroup("Noun_Agreements_Group")
A3Sg_Noun = Suffix("A3Sg_Noun", Noun_Agreements_Group, 'A3sg')
A3Pl_Noun = Suffix("A3Pl_Noun", Noun_Agreements_Group, 'A3pl')

###########  Possessive agreements
Noun_Possessions_Group = SuffixGroup("Noun_Possession_Group")
Pnon_Noun = Suffix("Pnon_Noun", Noun_Possessions_Group, "Pnon")
P1Sg_Noun = Suffix("P1sg_Noun", Noun_Possessions_Group, "P1sg")
P2Sg_Noun = Suffix("P2sg_Noun", Noun_Possessions_Group, "P2sg")
P3Sg_Noun = Suffix("P3sg_Noun", Noun_Possessions_Group, "P3sg")
P1Pl_Noun = Suffix("P1pl_Noun", Noun_Possessions_Group, "P1pl")
P2Pl_Noun = Suffix("P2pl_Noun", Noun_Possessions_Group, "P2pl")
P3Pl_Noun = Suffix("P3pl_Noun", Noun_Possessions_Group, "P3pl")

###########  Noun cases
Noun_Cases_Group = SuffixGroup('Noun_Case_Group')
Nom_Noun = Suffix("Nom_Noun", Noun_Cases_Group, "Nom")
Nom_Noun_Deriv = Suffix("Nom_Deriv_Noun", Noun_Cases_Group, "Nom")
Acc_Noun = Suffix("Acc_Noun", Noun_Cases_Group, "Acc")
Dat_Noun = Suffix("Dat_Noun", Noun_Cases_Group, "Dat")
Loc_Noun = Suffix("Loc_Noun", Noun_Cases_Group, "Loc")
Abl_Noun = Suffix("Abl_Noun", Noun_Cases_Group, "Abl")

Gen_Noun = Suffix("Gen_Noun", Noun_Cases_Group, "Gen")
Ins_Noun = Suffix("Ins_Noun", Noun_Cases_Group, "Ins")

############# Noun to Noun derivations
Agt_Noun = Suffix("Agt_Noun", pretty_name='Agt')
Dim = Suffix("Dim")

############# Noun to Verb derivations
Acquire = Suffix("Acquire")

############# Noun to Adjective derivations
With = Suffix("With")
Without = Suffix("Without")
Rel = Suffix("Rel")

############# Verb agreements
Verb_Agreements_Group = SuffixGroup('Verb_Agreements_Group')
A1Sg_Verb = Suffix("A1Sg_Verb", Verb_Agreements_Group, "A1sg")
A2Sg_Verb = Suffix("A2Sg_Verb", Verb_Agreements_Group, "A2sg")
A3Sg_Verb = Suffix("A3Sg_Verb", Verb_Agreements_Group, "A3sg")
A1Pl_Verb = Suffix("A1Pl_Verb", Verb_Agreements_Group, "A1pl")
A2Pl_Verb = Suffix("A2Pl_Verb", Verb_Agreements_Group, "A2pl")
A3Pl_Verb = Suffix("A3Pl_Verb", Verb_Agreements_Group, "A3pl")

############# Verb conditions
Verb_Polarity_Group = SuffixGroup("Verb_Conditions_Group")
Negative = Suffix("Neg", Verb_Polarity_Group)
Positive = Suffix("Pos", Verb_Polarity_Group)

############# Verbal tenses
Aorist = Suffix("Aor")
Progressive = Suffix("Prog")
Future = Suffix("Fut")
Narr = Suffix("Narr")
Past = Suffix("Past")

Cond = Suffix("Cond")
Imp = Suffix("Imp")

############ Modals
Neces = Suffix("Neces")
Opt = Suffix("Opt")

############ Verb to Noun derivations
Inf = Suffix("Inf")
PastPart_Noun = Suffix("PastPart_Noun", pretty_name='PastPart')
FutPart_Noun = Suffix('FutPart_Noun', pretty_name='FutPart')

############ Verb to Verb derivations
Able = Suffix("Able")
Pass = Suffix("Pass")
Recip = Suffix("Recip")
Caus = Suffix("Caus", allow_repetition=True)
Hastily = Suffix("Hastily")

########### Verb to Adverb derivations
AfterDoingSo = Suffix("AfterDoingSo")
AsLongAs = Suffix("AsLongAs")
ByDoingSo = Suffix("ByDoingSo")
While = Suffix("While")
AsIf = Suffix("AsIf")

########### Verb to Adjective derivations
PresPart = Suffix("PresPart")
PastPart_Adj = Suffix("PastPart_Adj", pretty_name='PastPart')
FutPart_Adj = Suffix('FutPart_Adj', pretty_name='FutPart')
Agt_Adj = Suffix('Agt_Adj', pretty_name='Agt')

########### Adjective to Adverb derivations
Ly = Suffix("Ly")

########### Adjective to Noun derivations
Ness = Suffix("Ness")

########### Adjective to Verb derivations
Become = Suffix("Become")

########### Adjective possessions
Adjective_Possessions_Group = SuffixGroup("Adjective_Possessions_Group")
Pnon_Adj = Suffix("Pnon_Adj", Adjective_Possessions_Group, 'Pnon')
P1Sg_Adj = Suffix("P1Sg_Adj", Adjective_Possessions_Group, 'P1sg')
P2Sg_Adj = Suffix("P2Sg_Adj", Adjective_Possessions_Group, 'P2sg')
P3Sg_Adj = Suffix("P3Sg_Adj", Adjective_Possessions_Group, 'P3sg')
P1Pl_Adj = Suffix("P1Pl_Adj", Adjective_Possessions_Group, 'P1pl')
P2Pl_Adj = Suffix("P2Pl_Adj", Adjective_Possessions_Group, 'P2pl')
P3Pl_Adj = Suffix("P3Pl_Adj", Adjective_Possessions_Group, 'P3pl')

#############  Pronoun Agreements
Pronoun_Agreements_Group = SuffixGroup("Pronoun_Agreements_Group")
A1Sg_Pron = Suffix("A1Sg_Pron", Pronoun_Agreements_Group, 'A1sg')
A2Sg_Pron = Suffix("A2Sg_Pron", Pronoun_Agreements_Group, 'A2sg')
A3Sg_Pron = Suffix("A3Sg_Pron", Pronoun_Agreements_Group, 'A3sg')
A1Pl_Pron = Suffix("A1Pl_Pron", Pronoun_Agreements_Group, 'A1pl')
A2Pl_Pron = Suffix("A2Pl_Pron", Pronoun_Agreements_Group, 'A2pl')
A3Pl_Pron = Suffix("A3Pl_Pron", Pronoun_Agreements_Group, 'A3pl')

########### Pronoun possessions
Pronoun_Possessions_Group = SuffixGroup("Pronoun_Possessions_Group")
Pnon_Pron = Suffix("Pnon_Pron", Pronoun_Possessions_Group, 'Pnon')
P1Sg_Pron = Suffix("P1Sg_Pron", Pronoun_Possessions_Group, 'P1sg')
P2Sg_Pron = Suffix("P2Sg_Pron", Pronoun_Possessions_Group, 'P2sg')
P3Sg_Pron = Suffix("P3Sg_Pron", Pronoun_Possessions_Group, 'P3sg')
P1Pl_Pron = Suffix("P1Pl_Pron", Pronoun_Possessions_Group, 'P1pl')
P2Pl_Pron = Suffix("P2Pl_Pron", Pronoun_Possessions_Group, 'P2pl')
P3Pl_Pron = Suffix("P3Pl_Pron", Pronoun_Possessions_Group, 'P3pl')

###########  Pronoun cases
Pronoun_Case_Group = SuffixGroup('Pronoun_Case_Group')
Nom_Pron = Suffix("Nom", Pronoun_Case_Group)
Nom_Pron_Deriv = Suffix("Nom_Pron_Deriv", Pronoun_Case_Group, pretty_name="Nom")
Acc_Pron = Suffix("Acc", Pronoun_Case_Group)
Dat_Pron = Suffix("Dat", Pronoun_Case_Group)
Loc_Pron = Suffix("Loc", Pronoun_Case_Group)
Abl_Pron = Suffix("Abl", Pronoun_Case_Group)

############# Pronoun case-likes
Gen_Pron = Suffix("Gen", Pronoun_Case_Group)
Ins_Pron = Suffix("Ins", Pronoun_Case_Group)

############# Pronoun to Adjective derivations
Without_Pron = Suffix("Without_Pron", pretty_name="Without")

###########################################################################
############################## Forms ######################################
###########################################################################

def _register_noun_suffixes():
    _register_noun_agreements()
    _register_possessive_agreements()
    _register_noun_cases()
    _register_noun_to_noun_derivations()
    _register_noun_to_verb_derivations()
    _register_noun_to_adjective_derivations()

def _register_verb_suffixes():
    _register_verb_agreements()
    _register_verb_polarisations()
    _register_verb_tenses()
    _register_modal_verbs()
    _register_verb_to_verb_derivations()
    _register_verb_to_noun_derivations()
    _register_verb_to_adverb_derivations()
    _register_verb_to_adjective_derivations()

def _register_adjective_suffixes():
    _register_adjective_to_adverb_derivations()
    _register_adjective_to_noun_derivations()
    _register_adjective_to_verb_derivations()
    _register_adjective_possessions()

def _register_pronoun_suffixes():
    _register_pronoun_agreements()
    _register_pronoun_possessions()
    _register_pronoun_cases()
    _register_pronoun_to_adjective_suffixes()


def _register_noun_agreements():
    NOUN_ROOT.add_out_suffix(A3Sg_Noun, NOUN_WITH_AGREEMENT)
    A3Sg_Noun.add_suffix_form("")

    NOUN_ROOT.add_out_suffix(A3Pl_Noun, NOUN_WITH_AGREEMENT)
    A3Pl_Noun.add_suffix_form("lAr")

def _register_possessive_agreements():
    NOUN_WITH_AGREEMENT.add_out_suffix(Pnon_Noun, NOUN_WITH_POSSESSION)
    Pnon_Noun.add_suffix_form("")

    NOUN_WITH_AGREEMENT.add_out_suffix(P1Sg_Noun, NOUN_WITH_POSSESSION)
    P1Sg_Noun.add_suffix_form("+Im")

    NOUN_WITH_AGREEMENT.add_out_suffix(P2Sg_Noun, NOUN_WITH_POSSESSION)
    P2Sg_Noun.add_suffix_form("+In")

    NOUN_WITH_AGREEMENT.add_out_suffix(P3Sg_Noun, NOUN_WITH_POSSESSION)
    P3Sg_Noun.add_suffix_form("+sI")

    NOUN_WITH_AGREEMENT.add_out_suffix(P1Pl_Noun, NOUN_WITH_POSSESSION)
    P1Pl_Noun.add_suffix_form("+ImIz")

    NOUN_WITH_AGREEMENT.add_out_suffix(P2Pl_Noun, NOUN_WITH_POSSESSION)
    P2Pl_Noun.add_suffix_form("+InIz")

    NOUN_WITH_AGREEMENT.add_out_suffix(P3Pl_Noun, NOUN_WITH_POSSESSION)
    P3Pl_Noun.add_suffix_form("lArI")
    P3Pl_Noun.add_suffix_form("I", comes_after(A3Pl_Noun))

def _register_noun_cases():
    comes_after_P3 = comes_after(P3Sg_Noun) | comes_after(P3Pl_Noun)
    doesnt_come_after_P3 = ~comes_after_P3
    
    NOUN_WITH_POSSESSION.add_out_suffix(Nom_Noun, NOUN_WITH_CASE)
    Nom_Noun.add_suffix_form("")

    NOUN_WITH_POSSESSION.add_out_suffix(Nom_Noun_Deriv, NOUN_NOM_DERIV)
    Nom_Noun_Deriv.add_suffix_form("", comes_after(Pnon_Noun))

    NOUN_WITH_POSSESSION.add_out_suffix(Acc_Noun, NOUN_WITH_CASE)
    Acc_Noun.add_suffix_form(u"+yI", doesnt_come_after_P3)
    Acc_Noun.add_suffix_form(u"nI", comes_after_P3)

    NOUN_WITH_POSSESSION.add_out_suffix(Dat_Noun, NOUN_WITH_CASE)
    Dat_Noun.add_suffix_form(u"+yA", doesnt_come_after_P3)
    Dat_Noun.add_suffix_form(u"nA", comes_after_P3)

    NOUN_WITH_POSSESSION.add_out_suffix(Loc_Noun, NOUN_WITH_CASE)
    Loc_Noun.add_suffix_form(u"dA", doesnt_come_after_P3 & doesnt_come_after_derivation(Inf, "mAk"))
    Loc_Noun.add_suffix_form(u"ndA")

    NOUN_WITH_POSSESSION.add_out_suffix(Abl_Noun, NOUN_WITH_CASE)
    Abl_Noun.add_suffix_form(u"dAn", doesnt_come_after_P3)
    Abl_Noun.add_suffix_form(u"ndAn")

    NOUN_WITH_POSSESSION.add_out_suffix(Gen_Noun, NOUN_WITH_CASE)
    Gen_Noun.add_suffix_form(u"+nIn")

    NOUN_WITH_POSSESSION.add_out_suffix(Ins_Noun, NOUN_WITH_CASE)
    Ins_Noun.add_suffix_form(u"+ylA")

def _register_noun_to_noun_derivations():
    NOUN_NOM_DERIV.add_out_suffix(Agt_Noun, NOUN_ROOT)
    Agt_Noun.add_suffix_form(u"cI")

    NOUN_NOM_DERIV.add_out_suffix(Dim, NOUN_ROOT)
    Dim.add_suffix_form(u"cIk")

def _register_noun_to_verb_derivations():
    NOUN_NOM_DERIV.add_out_suffix(Acquire, VERB_ROOT)
    Acquire.add_suffix_form(u"lAn")

def _register_noun_to_adjective_derivations():
    NOUN_NOM_DERIV.add_out_suffix(With, ADJECTIVE_ROOT)
    With.add_suffix_form(u"lI")

    NOUN_NOM_DERIV.add_out_suffix(Without, ADJECTIVE_ROOT)
    Without.add_suffix_form(u"sIz")

    NOUN_DERIV_WITH_CASE.add_out_suffix(Rel, ADJECTIVE_ROOT)
    Rel.add_suffix_form(u"ki")

def _register_verb_polarisations():
    VERB_ROOT.add_out_suffix(Negative, VERB_WITH_POLARITY)
    Negative.add_suffix_form(u"m", postcondition=doesnt(followed_by_suffix(that_goes_to(State.DERIV))))
    Negative.add_suffix_form(u"mA")

    VERB_ROOT.add_out_suffix(Positive, VERB_WITH_POLARITY)
    Positive.add_suffix_form("")

def _register_verb_tenses():
    VERB_WITH_POLARITY.add_out_suffix(Aorist, VERB_WITH_TENSE)
    Aorist.add_suffix_form(u"+Ir", requires_root_attribute(RootAttribute.Aorist_I))
    Aorist.add_suffix_form(u"+Ar")
    Aorist.add_suffix_form(u"z", comes_after(Negative))    # gel-me-z or gel-me-z-sin
    Aorist.add_suffix_form(u"", comes_after(Negative), followed_by(A1Sg_Verb) or followed_by(A1Pl_Verb))     # gel-me-m or gel-me-yiz

    VERB_WITH_POLARITY.add_out_suffix(Progressive, VERB_WITH_TENSE)
    Progressive.add_suffix_form(u"Iyor")
    Progressive.add_suffix_form(u"mAktA")

    VERB_WITH_POLARITY.add_out_suffix(Future, VERB_WITH_TENSE)
    Future.add_suffix_form(u"+yAcAk")

    VERB_WITH_POLARITY.add_out_suffix(Narr, VERB_WITH_TENSE)
    Narr.add_suffix_form(u"mIş")
    Narr.add_suffix_form(u"ymIş")

    VERB_WITH_POLARITY.add_out_suffix(Past, VERB_WITH_TENSE)
    Past.add_suffix_form(u"dI")
    Past.add_suffix_form(u"ydI")

    VERB_WITH_POLARITY.add_out_suffix(Cond, VERB_WITH_TENSE)
    Cond.add_suffix_form(u"sA")

    VERB_WITH_POLARITY.add_out_suffix(Imp, VERB_WITH_TENSE)
    Imp.add_suffix_form(u"", postcondition=followed_by(A2Sg_Verb) | followed_by(A3Sg_Verb) | followed_by(A2Pl_Verb) | followed_by(A3Pl_Verb))
    Imp.add_suffix_form(u"sAnA", postcondition=followed_by(A2Sg_Verb))
    Imp.add_suffix_form(u"sAnIzA", postcondition=followed_by(A2Pl_Verb))

    VERB_WITH_TENSE.add_out_suffix(Cond, VERB_WITH_TENSE)
    VERB_WITH_TENSE.add_out_suffix(Narr, VERB_WITH_TENSE)
    VERB_WITH_TENSE.add_out_suffix(Past, VERB_WITH_TENSE)

def _register_verb_agreements():
    comes_after_imperative = comes_after(Imp)
    doesnt_come_after_imperative = doesnt(comes_after_imperative)
    comes_after_empty_imperative = comes_after(Imp, u"")
    doesnt_come_after_empty_imperative = doesnt(comes_after_empty_imperative)

    VERB_WITH_TENSE.add_out_suffix(A1Sg_Verb, VERB_TERMINAL)
    A1Sg_Verb.add_suffix_form("+Im")
    A1Sg_Verb.add_suffix_form("yIm")   #"yap-makta-yım", gel-meli-yim

    VERB_WITH_TENSE.add_out_suffix(A2Sg_Verb, VERB_TERMINAL)
    A2Sg_Verb.add_suffix_form("n", doesnt_come_after_imperative)
    A2Sg_Verb.add_suffix_form("sIn", doesnt_come_after_imperative)
    A2Sg_Verb.add_suffix_form("", comes_after_imperative)

    VERB_WITH_TENSE.add_out_suffix(A3Sg_Verb, VERB_TERMINAL)
    A3Sg_Verb.add_suffix_form("", doesnt_come_after_imperative)
    A3Sg_Verb.add_suffix_form("sIn", comes_after_imperative)

    VERB_WITH_TENSE.add_out_suffix(A1Pl_Verb, VERB_TERMINAL)
    A1Pl_Verb.add_suffix_form("+Iz", doesnt_come_after(Opt))
    A1Pl_Verb.add_suffix_form("k", doesnt_come_after(Opt))     # only for "gel-di-k"
    A1Pl_Verb.add_suffix_form("yIz", doesnt_come_after(Opt))   # "yap-makta-yız" OR "gel-me-yiz"
    A1Pl_Verb.add_suffix_form("lIm", comes_after(Opt))     # only for "gel-e-lim"

    VERB_WITH_TENSE.add_out_suffix(A2Pl_Verb, VERB_TERMINAL)
    A2Pl_Verb.add_suffix_form("", comes_after_imperative & doesnt_come_after_empty_imperative)
    A2Pl_Verb.add_suffix_form("sInIz", doesnt_come_after_imperative)
    A2Pl_Verb.add_suffix_form("nIz", doesnt_come_after_imperative)
    A2Pl_Verb.add_suffix_form("+yIn", comes_after_empty_imperative)
    A2Pl_Verb.add_suffix_form("+yInIz", comes_after_empty_imperative)

    VERB_WITH_TENSE.add_out_suffix(A3Pl_Verb, VERB_TERMINAL)
    A3Pl_Verb.add_suffix_form("lAr", doesnt_come_after_imperative)
    A3Pl_Verb.add_suffix_form("sInlAr", comes_after_imperative)

def _register_modal_verbs():
    followed_by_modal_followers = followed_by(Past) | followed_by(Narr) | followed_by_one_from_group(Verb_Agreements_Group)

    VERB_WITH_POLARITY.add_out_suffix(Neces, VERB_WITH_TENSE)
    Neces.add_suffix_form(u"mAlI!")
    
    VERB_WITH_POLARITY.add_out_suffix(Opt, VERB_WITH_TENSE)
    Opt.add_suffix_form(u"Ay")
    Opt.add_suffix_form(u"A", doesnt_come_after(Negative), followed_by_modal_followers)
    Opt.add_suffix_form(u"yAy")
    Opt.add_suffix_form(u"yA", postcondition=followed_by_modal_followers)

def _register_verb_to_verb_derivations():
    VERB_PLAIN_DERIV.add_out_suffix(Able, VERB_ROOT)
    Able.add_suffix_form(u"+yAbil", postcondition=doesnt(followed_by(Negative)))
    Able.add_suffix_form(u"+yA", postcondition=followed_by(Negative))
    
    VERB_POLARITY_DERIV.add_out_suffix(Hastily, VERB_ROOT)
    Hastily.add_suffix_form(u"+yIver")
    
    VERB_PLAIN_DERIV.add_out_suffix(Pass, VERB_ROOT)
    Pass.add_suffix_form(u"+In")
    Pass.add_suffix_form(u"+nIl")
    Pass.add_suffix_form(u"+InIl")

    VERB_PLAIN_DERIV.add_out_suffix(Recip, VERB_ROOT)
    Recip.add_suffix_form(u"+Iş", post_derivation_condition=doesnt(followed_by_derivation(Caus)))
    
    VERB_PLAIN_DERIV.add_out_suffix(Caus, VERB_ROOT)
    Caus.add_suffix_form(u"t", requires_root_attribute(RootAttribute.Causative_t) & doesnt_come_after_derivation(Caus, "t") & doesnt_come_after_derivation(Caus, "It"))
    Caus.add_suffix_form(u"Ir", requires_root_attribute(RootAttribute.Causative_Ir) & doesnt_come_after_derivation(Able))
    Caus.add_suffix_form(u"It", requires_root_attribute(RootAttribute.Causative_It) & doesnt_come_after_derivation(Able))
    Caus.add_suffix_form(u"Ar", requires_root_attribute(RootAttribute.Causative_Ar) & doesnt_come_after_derivation(Able))
    Caus.add_suffix_form(u"dIr", requires_root_attribute(RootAttribute.Causative_dIr))

def _register_verb_to_noun_derivations():
    VERB_POLARITY_DERIV.add_out_suffix(Inf, NOUN_ROOT)
    Inf.add_suffix_form(u"mAk")
    Inf.add_suffix_form(u"mA")
    Inf.add_suffix_form(u"+yIş")
    
    VERB_POLARITY_DERIV.add_out_suffix(PastPart_Noun, NOUN_ROOT)
    PastPart_Noun.add_suffix_form(u"dIk")

    VERB_POLARITY_DERIV.add_out_suffix(FutPart_Noun, NOUN_ROOT)
    FutPart_Noun.add_suffix_form(u'+yAcAk')

def _register_verb_to_adverb_derivations():
    VERB_POLARITY_DERIV.add_out_suffix(AfterDoingSo, ADVERB_ROOT)
    AfterDoingSo.add_suffix_form(u"+yIp")
    
    VERB_POLARITY_DERIV.add_out_suffix(AsLongAs, ADVERB_ROOT)
    AsLongAs.add_suffix_form(u"dIkçA")
    
    VERB_POLARITY_DERIV.add_out_suffix(ByDoingSo, ADVERB_ROOT)
    ByDoingSo.add_suffix_form(u"+yArAk")
    
    VERB_TENSE_DERIV.add_out_suffix(While, ADVERB_ROOT)
    While.add_suffix_form(u"ken")
    
    VERB_TENSE_DERIV.add_out_suffix(AsIf, ADVERB_ROOT)
    AsIf.add_suffix_form(u"cAsInA")

def _register_verb_to_adjective_derivations():
    VERB_POLARITY_DERIV.add_out_suffix(PresPart, ADJECTIVE_ROOT)
    PresPart.add_suffix_form(u'An')

    VERB_POLARITY_DERIV.add_out_suffix(PastPart_Adj, ADJECTIVE_PART_WITHOUT_POSSESSION)
    PastPart_Adj.add_suffix_form(u'dIk')

    VERB_POLARITY_DERIV.add_out_suffix(FutPart_Adj, ADJECTIVE_PART_WITHOUT_POSSESSION)
    FutPart_Adj.add_suffix_form(u'+yAcAk')

    VERB_POLARITY_DERIV.add_out_suffix(Agt_Adj, ADJECTIVE_ROOT)
    Agt_Adj.add_suffix_form(u"+yIcI")

def _register_adjective_to_adverb_derivations():
    ADJECTIVE_DERIV.add_out_suffix(Ly, ADVERB_ROOT)
    Ly.add_suffix_form(u"cA")

def _register_adjective_to_noun_derivations():
    ADJECTIVE_DERIV.add_out_suffix(Ness, NOUN_ROOT)
    Ness.add_suffix_form(u"lIk")

def _register_adjective_to_verb_derivations():
    ADJECTIVE_DERIV.add_out_suffix(Become, VERB_ROOT)
    Become.add_suffix_form(u"lAş")

def _register_adjective_possessions():
    ADJECTIVE_PART_WITHOUT_POSSESSION.add_out_suffix(Pnon_Adj, ADJECTIVE_TERMINAL)
    Pnon_Adj.add_suffix_form("")

    ADJECTIVE_PART_WITHOUT_POSSESSION.add_out_suffix(P1Sg_Adj, ADJECTIVE_TERMINAL)
    P1Sg_Adj.add_suffix_form("+Im")

    ADJECTIVE_PART_WITHOUT_POSSESSION.add_out_suffix(P2Sg_Adj, ADJECTIVE_TERMINAL)
    P2Sg_Adj.add_suffix_form("+In")

    ADJECTIVE_PART_WITHOUT_POSSESSION.add_out_suffix(P3Sg_Adj, ADJECTIVE_TERMINAL)
    P3Sg_Adj.add_suffix_form("+sI")

    ADJECTIVE_PART_WITHOUT_POSSESSION.add_out_suffix(P1Pl_Adj, ADJECTIVE_TERMINAL)
    P1Pl_Adj.add_suffix_form("+ImIz")

    ADJECTIVE_PART_WITHOUT_POSSESSION.add_out_suffix(P2Pl_Adj, ADJECTIVE_TERMINAL)
    P2Pl_Adj.add_suffix_form("+InIz")

    ADJECTIVE_PART_WITHOUT_POSSESSION.add_out_suffix(P3Pl_Adj, ADJECTIVE_TERMINAL)
    P3Pl_Adj.add_suffix_form("lArI")

def _register_pronoun_agreements():
    PRONOUN_ROOT.add_out_suffix(A1Sg_Pron, PRONOUN_WITH_AGREEMENT)
    #A1Sg_Pron forms are predefined, 'ben' and 'kendi'
    
    PRONOUN_ROOT.add_out_suffix(A2Sg_Pron, PRONOUN_WITH_AGREEMENT)
    #A2Sg_Pron forms are predefined, 'sen' and 'kendi'

    PRONOUN_ROOT.add_out_suffix(A3Sg_Pron, PRONOUN_WITH_AGREEMENT)
    A3Sg_Pron.add_suffix_form("")
    #A3Sg_Pron forms for 'o', 'bu', 'su', 'kendi' are predefined

    PRONOUN_ROOT.add_out_suffix(A1Pl_Pron, PRONOUN_WITH_AGREEMENT)
    #A1Pl_Pron forms are predefined, 'biz' and 'kendi'

    PRONOUN_ROOT.add_out_suffix(A2Pl_Pron, PRONOUN_WITH_AGREEMENT)
    #A2Pl_Pron forms are predefined, 'siz' and 'kendi'

    PRONOUN_ROOT.add_out_suffix(A3Pl_Pron, PRONOUN_WITH_AGREEMENT)
    A3Pl_Pron.add_suffix_form("lAr")
    #A3Pl_Pron forms for 'onlar', 'bunlar', 'sunlar', 'kendileri' are predefined


def _register_pronoun_possessions():
    PRONOUN_WITH_AGREEMENT.add_out_suffix(Pnon_Pron, PRONOUN_WITH_POSSESSION)
    Pnon_Pron.add_suffix_form("")
    #Pnon_Pron forms for 'ben', 'sen', 'o', 'biz', 'siz', 'onlar', 'bu', 'su', 'kendi' are predefined
    
    PRONOUN_WITH_AGREEMENT.add_out_suffix(P1Sg_Pron, PRONOUN_WITH_POSSESSION)
    P1Sg_Pron.add_suffix_form("+Im")
    #P1Sg_Pron forms for 'ben', 'sen', 'o', 'biz', 'siz', 'onlar', 'bu', 'su', 'kendi' are predefined
    
    PRONOUN_WITH_AGREEMENT.add_out_suffix(P2Sg_Pron, PRONOUN_WITH_POSSESSION)
    P2Sg_Pron.add_suffix_form("+In")
    #P2Sg_Pron forms for 'ben', 'sen', 'o', 'biz', 'siz', 'onlar', 'bu', 'su', 'kendi' are predefined
    
    PRONOUN_WITH_AGREEMENT.add_out_suffix(P3Sg_Pron, PRONOUN_WITH_POSSESSION)
    P3Sg_Pron.add_suffix_form("+sI")
    #P3Sg_Pron forms for 'ben', 'sen', 'o', 'biz', 'siz', 'onlar', 'bu', 'su', 'kendi' are predefined

    PRONOUN_WITH_AGREEMENT.add_out_suffix(P1Pl_Pron, PRONOUN_WITH_POSSESSION)
    P1Pl_Pron.add_suffix_form("+ImIz")
    #P1Pl_Pron forms for 'ben', 'sen', 'o', 'biz', 'siz', 'onlar', 'bu', 'su', 'kendi' are predefined

    PRONOUN_WITH_AGREEMENT.add_out_suffix(P2Pl_Pron, PRONOUN_WITH_POSSESSION)
    P2Pl_Pron.add_suffix_form("+InIz")
    #P2Pl_Pron forms for 'ben', 'sen', 'o', 'biz', 'siz', 'onlar', 'bu', 'su', 'kendi' are predefined

    PRONOUN_WITH_AGREEMENT.add_out_suffix(P3Pl_Pron, PRONOUN_WITH_POSSESSION)
    P3Pl_Pron.add_suffix_form("lArI")
    P3Pl_Pron.add_suffix_form("I", comes_after(A3Pl_Pron))
    #P3Pl_Pron forms for 'ben', 'sen', 'o', 'biz', 'siz', 'onlar', 'bu', 'su', 'kendi' are predefined

def _register_pronoun_cases():
    PRONOUN_WITH_POSSESSION.add_out_suffix(Nom_Pron, PRONOUN_WITH_CASE)
    Nom_Pron.add_suffix_form("")

    PRONOUN_WITH_POSSESSION.add_out_suffix(Nom_Pron_Deriv, PRONOUN_NOM_DERIV)
    Nom_Pron_Deriv.add_suffix_form("", comes_after(Pnon_Pron))
    
    PRONOUN_WITH_POSSESSION.add_out_suffix(Acc_Pron, PRONOUN_WITH_CASE)
    Acc_Pron.add_suffix_form(u"+yI")
    #Acc_Pron forms for 'ben', 'sen', 'o', 'biz', 'siz', 'onlar', 'bu', 'su', 'kendi' are predefined

    PRONOUN_WITH_POSSESSION.add_out_suffix(Dat_Pron, PRONOUN_WITH_CASE)
    Dat_Pron.add_suffix_form(u"+yA")
    #Dat_Pron forms for 'ben', 'sen', 'o', 'biz', 'siz', 'onlar', 'bu', 'su', 'kendi' are predefined

    PRONOUN_WITH_POSSESSION.add_out_suffix(Loc_Pron, PRONOUN_WITH_CASE)
    Loc_Pron.add_suffix_form(u"dA")
    #Loc_Pron forms for 'ben', 'sen', 'o', 'biz', 'siz', 'onlar', 'bu', 'su', 'kendi' are predefined

    PRONOUN_WITH_POSSESSION.add_out_suffix(Abl_Pron, PRONOUN_WITH_CASE)
    Abl_Pron.add_suffix_form(u"dAn")
    #Abl_Pron forms for 'ben', 'sen', 'o', 'biz', 'siz', 'onlar', 'bu', 'su', 'kendi' are predefined

    PRONOUN_WITH_POSSESSION.add_out_suffix(Gen_Pron, PRONOUN_WITH_CASE)
    Gen_Pron.add_suffix_form(u"+nIn")
    #Gen_Pron forms for 'ben', 'sen', 'o', 'biz', 'siz', 'onlar', 'bu', 'su', 'kendi' are predefined

    PRONOUN_WITH_POSSESSION.add_out_suffix(Ins_Pron, PRONOUN_WITH_CASE)
    Ins_Pron.add_suffix_form(u"+ylA")
    #Ins_Pron forms for 'ben', 'sen', 'o', 'biz', 'siz', 'onlar', 'bu', 'su', 'kendi' are predefined

def _register_pronoun_to_adjective_suffixes():
    applies_to_bu_su_o = applies_to_stem('o') | applies_to_stem('bu') | applies_to_stem(u'şu')

    comes_after_A3Sg_pnon = comes_after(A3Sg_Pron) & comes_after(Pnon_Pron)

    comes_after_bu_su_o_pnon = comes_after_A3Sg_pnon & applies_to_bu_su_o

    PRONOUN_NOM_DERIV.add_out_suffix(Without_Pron, ADJECTIVE_ROOT)
    Without_Pron.add_suffix_form(u"sIz", doesnt(comes_after_bu_su_o_pnon))  # ben-siz, onlar-siz
    Without_Pron.add_suffix_form(u"nsuz", comes_after_bu_su_o_pnon)         # o-nsuz, bu-nsuz, su-nsuz

def _register_suffixes():
    _register_noun_suffixes()
    _register_verb_suffixes()
    _register_adjective_suffixes()
    _register_pronoun_suffixes()


_register_suffixes()
