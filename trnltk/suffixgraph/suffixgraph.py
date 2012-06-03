# coding=utf-8
from trnltk.stem.dictionaryitem import RootAttribute
from trnltk.suffixgraph.suffixconditions import comes_after, followed_by, applies_to_stem, doesnt_come_after, doesnt, followed_by_suffix, that_goes_to, requires_root_attribute, doesnt_come_after_derivation
from trnltk.suffixgraph.suffixgraphmodel import *

MAX_RANK = 99999

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
    ADJECTIVE_ROOT, ADJECTIVE_TERMINAL, ADJECTIVE_DERIV,
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
A3Sg_Noun = Suffix("A3Sg_Noun", 10, Noun_Agreements_Group, 'A3sg')
A3Pl_Noun = Suffix("A3Pl_Noun", 8, Noun_Agreements_Group, 'A3pl')

###########  Possessive agreements
Pnon = Suffix("Pnon", 11)
P1Sg = Suffix("P1sg", 11)
P2Sg = Suffix("P2sg", 11)
P3Sg = Suffix("P3sg", 11)
P1Pl = Suffix("P1pl", 11)
P2Pl = Suffix("P2pl", 11)
P3Pl = Suffix("P3pl", 11)

###########  Noun cases
Noun_Case_Group = SuffixGroup('Noun_Case_Group')
Nom = Suffix("Nom", 99, Noun_Case_Group)
Nom_Deriv = Suffix("Nom_Deriv", 99, Noun_Case_Group, "Nom")
Acc = Suffix("Acc", 99, Noun_Case_Group)
Dat = Suffix("Dat", 99, Noun_Case_Group)
Loc = Suffix("Loc", 99, Noun_Case_Group)
Abl = Suffix("Abl", 99, Noun_Case_Group)

############# Noun case-likes
Gen = Suffix("Gen", 99, Noun_Case_Group)
Ins = Suffix("Ins", 99, Noun_Case_Group)

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
A1Sg_Verb = Suffix("A1Sg_Verb", 99, Verb_Agreements_Group, "A1sg")
A2Sg_Verb = Suffix("A2Sg_Verb", 99, Verb_Agreements_Group, "A2sg")
A3Sg_Verb = Suffix("A3Sg_Verb", 99, Verb_Agreements_Group, "A3sg")
A1Pl_Verb = Suffix("A1Pl_Verb", 99, Verb_Agreements_Group, "A1pl")
A2Pl_Verb = Suffix("A2Pl_Verb", 99, Verb_Agreements_Group, "A2pl")
A3Pl_Verb = Suffix("A3Pl_Verb", 99, Verb_Agreements_Group, "A3pl")

############# Verb conditions
Verb_Polarity_Group = SuffixGroup("Verb_Conditions_Group")
Negative = Suffix("Neg", 5, Verb_Polarity_Group)
Positive = Suffix("Pos", 6, Verb_Polarity_Group)

############# Verbal tenses
Aorist = Suffix("Aor", 10)
Progressive = Suffix("Prog", 10)
Future = Suffix("Fut", 10)
Narr = Suffix("Narr", 15)
Past = Suffix("Past", 20)

Cond = Suffix("Cond", 30)
Imp = Suffix("Imp", 10)

############ Modals
Necess = Suffix("Necess", 10)
Opt = Suffix("Opt", 10)

############ Verb to Noun derivations
Inf = Suffix("Inf")
PastPart_Noun = Suffix("PastPart_Noun", pretty_name='PastPart')

############ Verb to Verb derivations
Able = Suffix("Able")
Pass = Suffix("Pass")
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
FutPart = Suffix('FutPart')
Agt_Adj = Suffix('Agt_Adj', pretty_name='Agt')

########### Adjective to Adverb derivations
Ly = Suffix("Ly")

########### Adjective to Noun derivations
Ness = Suffix("Ness")

########### Adjective to Verb derivations
Become = Suffix("Become")

#############  Pronoun Agreements
Pronoun_Agreements_Group = SuffixGroup("Pronoun_Agreements_Group")
A1Sg_Pron = Suffix("A1Sg_Pron", 10, Pronoun_Agreements_Group, 'A1sg')
A2Sg_Pron = Suffix("A2Sg_Pron", 10, Pronoun_Agreements_Group, 'A2sg')
A3Sg_Pron = Suffix("A3Sg_Pron", 10, Pronoun_Agreements_Group, 'A3sg')
A1Pl_Pron = Suffix("A1Pl_Pron", 10, Pronoun_Agreements_Group, 'A1pl')
A2Pl_Pron = Suffix("A2Pl_Pron", 10, Pronoun_Agreements_Group, 'A2pl')
A3Pl_Pron = Suffix("A3Pl_Pron", 10, Pronoun_Agreements_Group, 'A3pl')

########### Pronoun possessions
Pronoun_Possessions_Group = SuffixGroup("Pronoun_Possessions_Group")
Pnon_Pron = Suffix("Pnon_Pron", 10, Pronoun_Possessions_Group, 'Pnon')
P1Sg_Pron = Suffix("P1Sg_Pron", 10, Pronoun_Possessions_Group, 'P1sg')
P2Sg_Pron = Suffix("P1Sg_Pron", 10, Pronoun_Possessions_Group, 'P2sg')
P3Sg_Pron = Suffix("P1Sg_Pron", 10, Pronoun_Possessions_Group, 'P3sg')
P1Pl_Pron = Suffix("P1Sg_Pron", 10, Pronoun_Possessions_Group, 'P1pl')
P2Pl_Pron = Suffix("P1Sg_Pron", 10, Pronoun_Possessions_Group, 'P2pl')
P3Pl_Pron = Suffix("P1Sg_Pron", 10, Pronoun_Possessions_Group, 'P3pl')

###########  Pronoun cases
Pronoun_Case_Group = SuffixGroup('Pronoun_Case_Group')
Nom_Pron = Suffix("Nom", 99, Pronoun_Case_Group)
Nom_Pron_Deriv = Suffix("Nom_Pron_Deriv", 99, Pronoun_Case_Group, pretty_name="Nom")
Acc_Pron = Suffix("Acc", 99, Pronoun_Case_Group)
Dat_Pron = Suffix("Dat", 99, Pronoun_Case_Group)
Loc_Pron = Suffix("Loc", 99, Pronoun_Case_Group)
Abl_Pron = Suffix("Abl", 99, Pronoun_Case_Group)

############# Pronoun case-likes
Gen_Pron = Suffix("Gen", 99, Pronoun_Case_Group)
Ins_Pron = Suffix("Ins", 99, Pronoun_Case_Group)

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
    #TODO: rename these to Pnon_Noun etc
    NOUN_WITH_AGREEMENT.add_out_suffix(Pnon, NOUN_WITH_POSSESSION)
    Pnon.add_suffix_form("")

    NOUN_WITH_AGREEMENT.add_out_suffix(P1Sg, NOUN_WITH_POSSESSION)
    P1Sg.add_suffix_form("+Im")

    NOUN_WITH_AGREEMENT.add_out_suffix(P2Sg, NOUN_WITH_POSSESSION)
    P2Sg.add_suffix_form("+In")

    NOUN_WITH_AGREEMENT.add_out_suffix(P3Sg, NOUN_WITH_POSSESSION)
    P3Sg.add_suffix_form("+sI")

    NOUN_WITH_AGREEMENT.add_out_suffix(P1Pl, NOUN_WITH_POSSESSION)
    P1Pl.add_suffix_form("+ImIz")

    NOUN_WITH_AGREEMENT.add_out_suffix(P2Pl, NOUN_WITH_POSSESSION)
    P2Pl.add_suffix_form("+InIz")

    NOUN_WITH_AGREEMENT.add_out_suffix(P3Pl, NOUN_WITH_POSSESSION)
    P3Pl.add_suffix_form("lArI")
    P3Pl.add_suffix_form("I", comes_after(A3Pl_Noun))

def _register_noun_cases():
    comes_after_P3 = comes_after(P3Sg) | comes_after(P3Pl)
    doesnt_come_after_P3 = ~comes_after_P3
    
    #TODO rename these to Nom_Noun etc
    NOUN_WITH_POSSESSION.add_out_suffix(Nom, NOUN_WITH_CASE)
    Nom.add_suffix_form("")

    NOUN_WITH_POSSESSION.add_out_suffix(Nom_Deriv, NOUN_NOM_DERIV)
    Nom_Deriv.add_suffix_form("", comes_after(Pnon))

    NOUN_WITH_POSSESSION.add_out_suffix(Acc, NOUN_WITH_CASE)
    Acc.add_suffix_form(u"+yI", doesnt_come_after_P3)
    Acc.add_suffix_form(u"nI", comes_after_P3)

    NOUN_WITH_POSSESSION.add_out_suffix(Dat, NOUN_WITH_CASE)
    Dat.add_suffix_form(u"+yA", doesnt_come_after_P3)
    Dat.add_suffix_form(u"nA", comes_after_P3)

    NOUN_WITH_POSSESSION.add_out_suffix(Loc, NOUN_WITH_CASE)
    Loc.add_suffix_form(u"dA", doesnt_come_after_P3 & doesnt_come_after_derivation(Inf, "mAk"))
    Loc.add_suffix_form(u"ndA")

    NOUN_WITH_POSSESSION.add_out_suffix(Abl, NOUN_WITH_CASE)
    Abl.add_suffix_form(u"dAn", doesnt_come_after_P3)
    Abl.add_suffix_form(u"ndAn")

    NOUN_WITH_POSSESSION.add_out_suffix(Gen, NOUN_WITH_CASE)
    Gen.add_suffix_form(u"+nIn")

    NOUN_WITH_POSSESSION.add_out_suffix(Ins, NOUN_WITH_CASE)
    Ins.add_suffix_form(u"+ylA")

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

    VERB_WITH_TENSE.add_out_suffix(Cond, VERB_WITH_TENSE)
    VERB_WITH_TENSE.add_out_suffix(Narr, VERB_WITH_TENSE)
    VERB_WITH_TENSE.add_out_suffix(Past, VERB_WITH_TENSE)

def _register_verb_agreements():
    comes_after_imperative = comes_after(Imp)
    doesnt_come_after_imperative = doesnt(comes_after_imperative)

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
    A1Pl_Verb.add_suffix_form("+Iz")
    A1Pl_Verb.add_suffix_form("k")     # only for "gel-di-k"
    A1Pl_Verb.add_suffix_form("yIz")   # "yap-makta-yız" OR "gel-me-yiz"

    VERB_WITH_TENSE.add_out_suffix(A2Pl_Verb, VERB_TERMINAL)
    A2Pl_Verb.add_suffix_form("sInIz", doesnt_come_after_imperative)
    A2Pl_Verb.add_suffix_form("nIz", doesnt_come_after_imperative)
    A2Pl_Verb.add_suffix_form("+yIn", comes_after_imperative)
    A2Pl_Verb.add_suffix_form("+yInIz", comes_after_imperative)

    VERB_WITH_TENSE.add_out_suffix(A3Pl_Verb, VERB_TERMINAL)
    A3Pl_Verb.add_suffix_form("lAr", doesnt_come_after_imperative)
    A3Pl_Verb.add_suffix_form("sInlAr", comes_after_imperative)

def _register_modal_verbs():
    followed_by_modal_followers = followed_by(Past) | followed_by(Narr) | followed_by(A1Sg_Verb) | followed_by(A2Sg_Verb) | followed_by(A3Sg_Verb) # TODO: add the group!

    VERB_WITH_POLARITY.add_out_suffix(Necess, VERB_WITH_TENSE)
    Necess.add_suffix_form(u"mAlI")
    
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
    VERB_POLARITY_DERIV.add_out_suffix(PastPart_Noun, ADJECTIVE_ROOT)
    PastPart_Noun.add_suffix_form(u"dIk")

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
    
    VERB_POLARITY_DERIV.add_out_suffix(FutPart, ADJECTIVE_ROOT)
    FutPart.add_suffix_form(u'+yAcak')

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

def _register_pronoun_agreements():
    applies_to_ben = applies_to_stem('ben') | applies_to_stem('ban')
    applies_to_sen = applies_to_stem('sen') | applies_to_stem('san')
    applies_to_bu_su_o = applies_to_stem('o') | applies_to_stem('bu') | applies_to_stem(u'şu')
    applies_to_biz = applies_to_stem('biz')
    applies_to_siz = applies_to_stem('siz')
    applies_to_biz_siz = applies_to_biz | applies_to_siz

    PRONOUN_ROOT.add_out_suffix(A1Sg_Pron, PRONOUN_WITH_AGREEMENT)
    A1Sg_Pron.add_suffix_form("", applies_to_ben)
    
    PRONOUN_ROOT.add_out_suffix(A2Sg_Pron, PRONOUN_WITH_AGREEMENT)
    A2Sg_Pron.add_suffix_form("", applies_to_sen)
    
    PRONOUN_ROOT.add_out_suffix(A3Sg_Pron, PRONOUN_WITH_AGREEMENT)
    A3Sg_Pron.add_suffix_form("", doesnt(applies_to_ben) & doesnt(applies_to_sen) & doesnt(applies_to_biz_siz))
    
    PRONOUN_ROOT.add_out_suffix(A1Pl_Pron, PRONOUN_WITH_AGREEMENT)
    A1Pl_Pron.add_suffix_form("", applies_to_biz)
    
    PRONOUN_ROOT.add_out_suffix(A2Pl_Pron, PRONOUN_WITH_AGREEMENT)
    A2Pl_Pron.add_suffix_form("", applies_to_siz)
    
    PRONOUN_ROOT.add_out_suffix(A3Pl_Pron, PRONOUN_WITH_AGREEMENT)
    A3Pl_Pron.add_suffix_form("nlar", applies_to_bu_su_o)
    A3Pl_Pron.add_suffix_form("lAr", doesnt(applies_to_ben) & doesnt(applies_to_sen) & doesnt(applies_to_biz) & doesnt(applies_to_siz))

def _register_pronoun_possessions():
    doesnt_apply_to_persp = ~applies_to_stem('ben') & ~applies_to_stem('sen') & ~applies_to_stem('ban') & ~applies_to_stem('san') & ~applies_to_stem('biz') & ~applies_to_stem('siz')
    doesnt_apply_to_demonsp = ~applies_to_stem('o') & ~applies_to_stem('bu') & ~applies_to_stem(u'şu')
    doesnt_apply_to_persp_and_demonsp = doesnt_apply_to_demonsp & doesnt_apply_to_persp

    PRONOUN_WITH_AGREEMENT.add_out_suffix(Pnon_Pron, PRONOUN_WITH_POSSESSION)
    Pnon_Pron.add_suffix_form("")
    
    PRONOUN_WITH_AGREEMENT.add_out_suffix(P1Sg_Pron, PRONOUN_WITH_POSSESSION)
    P1Sg_Pron.add_suffix_form("+Im", doesnt_apply_to_persp_and_demonsp)
    
    PRONOUN_WITH_AGREEMENT.add_out_suffix(P2Sg_Pron, PRONOUN_WITH_POSSESSION)
    P2Sg_Pron.add_suffix_form("+In", doesnt_apply_to_persp_and_demonsp)
    
    PRONOUN_WITH_AGREEMENT.add_out_suffix(P3Sg_Pron, PRONOUN_WITH_POSSESSION)
    P3Sg_Pron.add_suffix_form("+sI", doesnt_apply_to_persp_and_demonsp)
    
    PRONOUN_WITH_AGREEMENT.add_out_suffix(P1Pl_Pron, PRONOUN_WITH_POSSESSION)
    P1Pl_Pron.add_suffix_form("+ImIz", doesnt_apply_to_persp_and_demonsp)
    
    PRONOUN_WITH_AGREEMENT.add_out_suffix(P2Pl_Pron, PRONOUN_WITH_POSSESSION)
    P2Pl_Pron.add_suffix_form("+InIz", doesnt_apply_to_persp_and_demonsp)
    
    PRONOUN_WITH_AGREEMENT.add_out_suffix(P3Pl_Pron, PRONOUN_WITH_POSSESSION)
    P3Pl_Pron.add_suffix_form("lArI", doesnt_apply_to_persp_and_demonsp)
    P3Pl_Pron.add_suffix_form("I", comes_after(A3Pl_Pron) & doesnt_apply_to_persp_and_demonsp)

def _register_pronoun_cases():
    applies_to_bu_su_o = applies_to_stem('o') | applies_to_stem('bu') | applies_to_stem(u'şu')
    doesnt_apply_to_bu_su_o = ~applies_to_bu_su_o

    comes_after_biz_siz_pnon = (comes_after(A1Pl_Pron) & comes_after(Pnon_Pron)) | (comes_after(A2Pl_Pron) & comes_after(Pnon_Pron))
    comes_after_A3Sg_pnon = comes_after(A3Sg_Pron) & comes_after(Pnon_Pron)

    comes_after_bu_su_o_pnon = comes_after_A3Sg_pnon & applies_to_bu_su_o

    PRONOUN_WITH_POSSESSION.add_out_suffix(Nom_Pron, PRONOUN_WITH_CASE)
    Nom_Pron.add_suffix_form("")

    PRONOUN_WITH_POSSESSION.add_out_suffix(Nom_Pron_Deriv, PRONOUN_NOM_DERIV)
    Nom_Pron_Deriv.add_suffix_form("", comes_after(Pnon_Pron))
    
    PRONOUN_WITH_POSSESSION.add_out_suffix(Acc_Pron, PRONOUN_WITH_CASE)
    Acc_Pron.add_suffix_form(u"nu", comes_after_bu_su_o_pnon)   #bu-nu, su-nu, o-nu
    Acc_Pron.add_suffix_form(u"+yI", doesnt(comes_after_bu_su_o_pnon))   #ben-i, sen-i, biz-i, siz-i, onlar-i, nere-yi, kim-i
    Acc_Pron.add_suffix_form(u"leri", comes_after_biz_siz_pnon)     # biz-leri, siz-leri
    
    PRONOUN_WITH_POSSESSION.add_out_suffix(Dat_Pron, PRONOUN_WITH_CASE)
    Dat_Pron.add_suffix_form(u"+yA", comes_after(A3Pl_Pron) & comes_after(Pnon_Pron))
    Dat_Pron.add_suffix_form(u"+yA", doesnt_apply_to_bu_su_o)
    Dat_Pron.add_suffix_form(u"nA", comes_after_bu_su_o_pnon)
    Dat_Pron.add_suffix_form(u"lere", comes_after_biz_siz_pnon)
    
    PRONOUN_WITH_POSSESSION.add_out_suffix(Loc_Pron, PRONOUN_WITH_CASE)
    Loc_Pron.add_suffix_form(u"dA", comes_after(A3Pl_Pron) & comes_after(Pnon_Pron))
    Loc_Pron.add_suffix_form(u"dA", doesnt_apply_to_bu_su_o)
    Loc_Pron.add_suffix_form(u"ndA", comes_after_bu_su_o_pnon)
    Loc_Pron.add_suffix_form(u"lerde", comes_after_biz_siz_pnon)
    
    PRONOUN_WITH_POSSESSION.add_out_suffix(Abl_Pron, PRONOUN_WITH_CASE)
    Abl_Pron.add_suffix_form(u"dAn", comes_after(A3Pl_Pron) & comes_after(Pnon_Pron))
    Abl_Pron.add_suffix_form(u"dAn", doesnt_apply_to_bu_su_o)
    Abl_Pron.add_suffix_form(u"ndAn", comes_after_bu_su_o_pnon)
    Abl_Pron.add_suffix_form(u"lerden", comes_after_biz_siz_pnon)
    
    PRONOUN_WITH_POSSESSION.add_out_suffix(Gen_Pron, PRONOUN_WITH_CASE)
    Gen_Pron.add_suffix_form(u"im", (comes_after(A1Sg_Pron) & comes_after(Pnon_Pron)) | (comes_after(A1Pl_Pron) & comes_after(Pnon_Pron)))    # ben-im, biz-im
    Gen_Pron.add_suffix_form(u"in", (comes_after(A2Sg_Pron) & comes_after(Pnon_Pron)) | (comes_after(A2Pl_Pron) & comes_after(Pnon_Pron)))    # sen-in, siz-in
    Gen_Pron.add_suffix_form(u"nun", comes_after_bu_su_o_pnon)      # bu-nun, su-nun, o-nun
    Gen_Pron.add_suffix_form(u"lerin", comes_after_biz_siz_pnon)    # biz-lerin, siz-lerin
    Gen_Pron.add_suffix_form(u"+nIn", doesnt(comes_after_bu_su_o_pnon) & (comes_after(A3Pl_Pron) | comes_after(A3Sg_Pron)))     #onlar-in, kim-in, nere-nin, kimi-miz-in

    PRONOUN_WITH_POSSESSION.add_out_suffix(Ins_Pron, PRONOUN_WITH_CASE)
    Ins_Pron.add_suffix_form(u"imle", (comes_after(A1Sg_Pron) & comes_after(Pnon_Pron)) | (comes_after(A1Pl_Pron) & comes_after(Pnon_Pron)))  # ben-imle, biz-imle
    Ins_Pron.add_suffix_form(u"inle", (comes_after(A2Sg_Pron) & comes_after(Pnon_Pron)) | (comes_after(A2Pl_Pron) & comes_after(Pnon_Pron)))  # sen-inle, siz-inle
    Ins_Pron.add_suffix_form(u"nunla", comes_after_bu_su_o_pnon)   # o-nunla, bu-nunla, su-nunla
    Ins_Pron.add_suffix_form(u"nla", comes_after_bu_su_o_pnon)     # o-nla, bu-nla, su-nla
    Ins_Pron.add_suffix_form(u"lerle", comes_after_biz_siz_pnon)   # biz-lerle, siz-lerle
    Ins_Pron.add_suffix_form(u"+ylA")    # onlar-la, nere-yle, kim-le

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
