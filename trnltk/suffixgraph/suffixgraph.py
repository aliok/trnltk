# coding=utf-8
from trnltk.suffixgraph.suffixconditions import comes_after, followed_by

MAX_RANK = 99999

class State:
    TERMINAL = "TERMINAL"
    TRANSFER = "TRANSFER"
    DERIV = "DERIVATIONAL"

    def __init__(self, name, pretty_name, type):
        self.name = name
        self.pretty_name = pretty_name
        self.outputs = [] #(suffix, out_state) tuples
        self.type = type

    def add_out_suffix(self, suffix, to_state):
        self.outputs.append((suffix, to_state))

    def __str__(self):
        return self.name

    def __repr__(self):
        return repr(self.name)

class SuffixGroup:
    def __init__(self, name):
        self.name = name
        self.suffixes = []

    def __str__(self):
        return self.name

    def __repr__(self):
        return repr(self.name)

class Suffix:
    def __init__(self, name, rank=0, group=None, pretty_name=None):
        self.name = name
        self.suffix_forms = []
        self.rank = rank
        self.group = None
        self.pretty_name = pretty_name or name

        if group:
            self.group = group
            group.suffixes.append(self)

    def add_suffix_form(self, suffix_form, precondition=None, postcondition=None):
        form = None
        if type(suffix_form) is str or type(suffix_form) is unicode:
            form = SuffixForm(suffix_form, precondition, postcondition)
        elif type(suffix_form) is SuffixForm:
            assert precondition is None and  postcondition is None
        else:
            raise Exception("Unknown type for suffixForm" + repr(suffix_form))

        form.suffix=self
        self.suffix_forms.append(form)

    def __str__(self):
        return "{}({})".format(self.name, self.rank)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.name==other.name

class FreeTransitionSuffix(Suffix):
    def __init__(self, name, from_state, to_state):
        Suffix.__init__(self, name, 0 if from_state.type==State.DERIV else 999, None)
        self.add_suffix_form("")
        from_state.add_out_suffix(self, to_state)


class SuffixForm:
    def __init__(self, form, precondition=None, postcondition=None):
        self.form = form
        self.suffix = None
        self.precondition = precondition
        self.postcondition = postcondition

    def __str__(self):
        return self.form

    def __repr__(self):
        return repr(self.form)


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

ADJECTIVE_ROOT = State("ADJECTIVE_ROOT", 'Adj', State.TRANSFER)
ADJECTIVE_TERMINAL = State("ADJECTIVE_ROOT", 'Adj', State.TERMINAL)
ADJECTIVE_DERIV = State("ADJECTIVE_DERIV", 'Adj', State.DERIV)

ADVERB_ROOT = State("ADVERB_ROOT", 'Adv', State.TRANSFER)
ADVERB_TERMINAL = State("ADVERB_ROOT", 'Adv', State.TERMINAL)
ADVERB_DERIV = State("ADVERB_DERIV", 'Adv', State.DERIV)

ALL_STATES = {
    NOUN_ROOT, NOUN_WITH_AGREEMENT, NOUN_WITH_POSSESSION, NOUN_WITH_CASE, NOUN_TERMINAL, NOUN_DERIV_WITH_CASE, NOUN_NOM_DERIV,
    VERB_ROOT, VERB_WITH_POLARITY, VERB_WITH_TENSE, VERB_TERMINAL, VERB_PLAIN_DERIV, VERB_POLARITY_DERIV,
    ADJECTIVE_ROOT, ADJECTIVE_TERMINAL, ADJECTIVE_DERIV,
    ADVERB_ROOT, ADVERB_TERMINAL, ADVERB_DERIV
}

#############  Empty transitions
FreeTransitionSuffix("Noun_Free_Transition_1", NOUN_WITH_CASE, NOUN_TERMINAL)
FreeTransitionSuffix("Noun_Free_Transition_2", NOUN_WITH_CASE, NOUN_DERIV_WITH_CASE)
FreeTransitionSuffix("Verb_Free_Transition_1", VERB_ROOT, VERB_PLAIN_DERIV)
FreeTransitionSuffix("Verb_Free_Transition_2", VERB_WITH_POLARITY, VERB_POLARITY_DERIV)
FreeTransitionSuffix("Adj_Free_Transition_1", ADJECTIVE_ROOT, ADJECTIVE_TERMINAL)
FreeTransitionSuffix("Adj_Free_Transition_2", ADJECTIVE_ROOT, ADJECTIVE_DERIV)
FreeTransitionSuffix("Adv_Free_Transition", ADVERB_ROOT, ADVERB_TERMINAL)

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
Inst = Suffix("Inst", 99, Noun_Case_Group)

############# Noun to Noun derivations
Agt = Suffix("Agt")
Dim = Suffix("Dim")

############# Noun to Verb derivations
Acquire = Suffix("Acquire", 99)

############# Noun to Adjective derivations
With = Suffix("With")
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

############ Modals
Abil = Suffix("Abil", 10)
Necess = Suffix("Necess", 10)
Opt = Suffix("Opt", 10)

############ Verb to Verb derivations
Pass = Suffix("Pass")

########### Verb to Adverb derivations
AfterDoingSo = Suffix("AfterDoingSo")

########### Adjective to Adverb derivations
Ly = Suffix("Ly")



###########################################################################
############################## Forms ######################################
###########################################################################

#############  Noun Agreements
NOUN_ROOT.add_out_suffix(A3Sg_Noun, NOUN_WITH_AGREEMENT)
A3Sg_Noun.add_suffix_form("")

NOUN_ROOT.add_out_suffix(A3Pl_Noun, NOUN_WITH_AGREEMENT)
A3Pl_Noun.add_suffix_form("lAr")

###########  Possessive agreements
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

###########  Noun cases
NOUN_WITH_POSSESSION.add_out_suffix(Nom, NOUN_WITH_CASE)
Nom.add_suffix_form("")

NOUN_WITH_POSSESSION.add_out_suffix(Nom_Deriv, NOUN_NOM_DERIV)
Nom_Deriv.add_suffix_form("", comes_after(Pnon))

NOUN_WITH_POSSESSION.add_out_suffix(Acc, NOUN_WITH_CASE)
Acc.add_suffix_form(u"+yI", ~comes_after(P3Sg))
Acc.add_suffix_form(u"nI", comes_after(P3Sg))

NOUN_WITH_POSSESSION.add_out_suffix(Dat, NOUN_WITH_CASE)
Dat.add_suffix_form(u"+yA", ~comes_after(P3Sg))
Dat.add_suffix_form(u"nA", comes_after(P3Sg))

NOUN_WITH_POSSESSION.add_out_suffix(Loc, NOUN_WITH_CASE)
Loc.add_suffix_form(u"dA", ~comes_after(P3Sg))
Loc.add_suffix_form(u"ndA")

NOUN_WITH_POSSESSION.add_out_suffix(Abl, NOUN_WITH_CASE)
Abl.add_suffix_form(u"dAn", ~comes_after(P3Sg))
Abl.add_suffix_form(u"ndAn")

############# Noun case-likes
NOUN_WITH_POSSESSION.add_out_suffix(Gen, NOUN_WITH_CASE)
Gen.add_suffix_form(u"+nIn")

NOUN_WITH_POSSESSION.add_out_suffix(Inst, NOUN_WITH_CASE)
Inst.add_suffix_form(u"+ylA")

############# Noun to Noun derivations
NOUN_NOM_DERIV.add_out_suffix(Agt, NOUN_ROOT)
Agt.add_suffix_form(u"cI")

NOUN_NOM_DERIV.add_out_suffix(Dim, NOUN_ROOT)
Dim.add_suffix_form(u"cIk")

############# Noun to Verb derivations
NOUN_NOM_DERIV.add_out_suffix(Acquire, VERB_ROOT)
Acquire.add_suffix_form(u"lAn")

############# Noun to Adjective derivations
NOUN_NOM_DERIV.add_out_suffix(With, ADJECTIVE_ROOT)
With.add_suffix_form(u"lI")

NOUN_DERIV_WITH_CASE.add_out_suffix(Rel, ADJECTIVE_ROOT)
Rel.add_suffix_form(u"ki")

############# Verb agreements
VERB_WITH_TENSE.add_out_suffix(A1Sg_Verb, VERB_TERMINAL)
A1Sg_Verb.add_suffix_form("+Im")
A1Sg_Verb.add_suffix_form("yIm")   #"yap-makta-yım", gel-meli-yim

VERB_WITH_TENSE.add_out_suffix(A2Sg_Verb, VERB_TERMINAL)
A2Sg_Verb.add_suffix_form("n")
A2Sg_Verb.add_suffix_form("sIn")

VERB_WITH_TENSE.add_out_suffix(A3Sg_Verb, VERB_TERMINAL)
A3Sg_Verb.add_suffix_form("")

VERB_WITH_TENSE.add_out_suffix(A1Pl_Verb, VERB_TERMINAL)
A1Pl_Verb.add_suffix_form("+Iz", ~comes_after(Aorist))
A1Pl_Verb.add_suffix_form("k")     # only for "gel-di-k"
A1Pl_Verb.add_suffix_form("yIz")   # "yap-makta-yız" OR "gel-me-yiz"

VERB_WITH_TENSE.add_out_suffix(A2Pl_Verb, VERB_TERMINAL)
A2Pl_Verb.add_suffix_form("sInIz")
A2Pl_Verb.add_suffix_form("nIz")

VERB_WITH_TENSE.add_out_suffix(A3Pl_Verb, VERB_TERMINAL)
A3Pl_Verb.add_suffix_form("lAr")

############# Verb conditions
VERB_ROOT.add_out_suffix(Negative, VERB_WITH_POLARITY)
Negative.add_suffix_form(u"m")
Negative.add_suffix_form(u"mA")
Negative.add_suffix_form(u"", postcondition=followed_by(Abil))

VERB_ROOT.add_out_suffix(Positive, VERB_WITH_POLARITY)
Positive.add_suffix_form("")

############# Verbal tenses
VERB_WITH_POLARITY.add_out_suffix(Aorist, VERB_WITH_TENSE)
Aorist.add_suffix_form(u"+Ir")
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

VERB_WITH_TENSE.add_out_suffix(Cond, VERB_WITH_TENSE)
VERB_WITH_TENSE.add_out_suffix(Narr, VERB_WITH_TENSE)
VERB_WITH_TENSE.add_out_suffix(Past, VERB_WITH_TENSE)

############ Modals
VERB_WITH_POLARITY.add_out_suffix(Abil, VERB_WITH_POLARITY)
Abil.add_suffix_form(u"+yAbil", ~comes_after(Negative))
Abil.add_suffix_form(u"+yAmA", comes_after(Negative))

VERB_WITH_POLARITY.add_out_suffix(Necess, VERB_WITH_TENSE)
Necess.add_suffix_form(u"mAlI")

VERB_WITH_POLARITY.add_out_suffix(Opt, VERB_WITH_TENSE)
Opt.add_suffix_form(u"Ay")
Opt.add_suffix_form(u"A", ~comes_after(Negative), followed_by(Past) | followed_by(Narr) | followed_by(A1Sg_Verb) | followed_by(A2Sg_Verb) | followed_by(A3Sg_Verb) ) # TODO: add the group!
Opt.add_suffix_form(u"yAy")
Opt.add_suffix_form(u"yA", None, followed_by(Past) | followed_by(Narr) | followed_by(A1Sg_Verb) | followed_by(A2Sg_Verb) | followed_by(A3Sg_Verb) ) # TODO: add the group!

############ Verb to Verb derivations
VERB_PLAIN_DERIV.add_out_suffix(Pass, VERB_ROOT)
Pass.add_suffix_form(u"+In")
Pass.add_suffix_form(u"+nIl")
Pass.add_suffix_form(u"+InIl")

########### Verb to Adverb derivations:
VERB_POLARITY_DERIV.add_out_suffix(AfterDoingSo, ADVERB_ROOT)
AfterDoingSo.add_suffix_form("+yIp")

########### Adjective to Adverb derivations
ADJECTIVE_DERIV.add_out_suffix(Ly, ADVERB_ROOT)
Ly.add_suffix_form("cA")