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
class SyntacticCategory(object):
    NOUN = "Noun"
    ADJECTIVE = "Adj"
    ADVERB = "Adv"
    CONJUNCTION = "Conj"
    INTERJECTION = "Interj"
    VERB = "Verb"
    PRONOUN = "Pron"
    NUMERAL = "Num"
    DETERMINER = "Det"
    PARTICLE = "Part"
    QUESTION = "Ques"
    PUNCTUATION = "Punc"

    ALL = sorted({NOUN, ADJECTIVE, ADVERB, CONJUNCTION, INTERJECTION, VERB, PRONOUN, NUMERAL, DETERMINER, PARTICLE, QUESTION, PUNCTUATION})

class SecondarySyntacticCategory(object):
    DUPLICATOR = "Dup"
    POST_POSITIVE = "Postp"
    QUESTION = "Ques"
    DEMONSTRATIVE = "Demons"
    REFLEXIVE = "Reflex"
    PERSONAL = "Pers"
    TIME = "Time"
    PROPER_NOUN = "Prop"
    ABBREVIATION = "Abbr"

    CARD = "Card"
    ORD = "Ord"
    DIGITS = "Digits"

    ALL = sorted({DUPLICATOR, POST_POSITIVE, QUESTION, DEMONSTRATIVE, REFLEXIVE, PERSONAL, TIME, PROPER_NOUN, ABBREVIATION, CARD, ORD})

#    NONE = "None"

class RootAttribute(object):
    Voicing = "Voicing"
    VoicingOpt = "VoicingOpt"
    NoVoicing = "NoVoicing"
    InverseHarmony = "InverseHarmony"
    LastVowelDrop = "LastVowelDrop"
    Doubling = "Doubling"
    RootChange = "RootChange"
    NounConsInsert = "NounConsInsert"
    NounConsInsert_n = "NounConsInsert_n"
    NoQuote = "NoQuote"
    Plural = "Plural"
    ProgressiveVowelDrop = "ProgressiveVowelDrop"
    Aorist_I = "Aorist_I"
    Aorist_A = "Aorist_A"
    NonTransitive = "NonTransitive"
    Passive_In = "Passive_In"
    Passive_InIl = "Passive_InIl"
    Passive_NotApplicable = "Passive_NotApplicable"
    CompoundP3sg = "CompoundP3sg"
    Compound = "Compound"
    Reflexive = "Reflexive"
    Reciprocal = "Reciprocal"
    NoSuffix = "NoSuffix"

    Causative_t = "Causative_t"
    Causative_Ir = "Causative_Ir"
    Causative_It = "Causative_It"
    Causative_Ar = "Causative_Ar"
    Causative_dIr = "Causative_dIr"

    ALL = sorted({
        Voicing, VoicingOpt, NoVoicing, InverseHarmony, LastVowelDrop, Doubling, RootChange, NounConsInsert, NounConsInsert_n,
        NoQuote, Plural, ProgressiveVowelDrop, Aorist_I, Aorist_A, NonTransitive, Passive_In, Passive_InIl, Passive_NotApplicable,
        CompoundP3sg, Compound, Causative_t, Causative_It, Causative_Ir, Causative_Ar, Causative_dIr, Reflexive, Reciprocal, NoSuffix
    })

    CAUSATIVES = sorted({
        Causative_t, Causative_Ir, Causative_It, Causative_Ar, Causative_dIr
    })

class Lexeme(object):
    #TODO: make this and similar classes immutable
    def __init__(self, lemma, root, syntactic_category, secondary_syntactic_category, attributes):
        self.lemma = lemma
        self.root = root
        self.syntactic_category = syntactic_category
        self.secondary_syntactic_category = secondary_syntactic_category
        self.attributes = attributes if attributes else []

    def clone(self):
        return Lexeme(self.lemma, self.root, self.syntactic_category, self.secondary_syntactic_category, self.attributes[:])

    def __str__(self):
        return u'{}({})+{}+{} R_ATTR:{}'.format(repr(self.lemma), repr(self.root), self.syntactic_category, self.secondary_syntactic_category, self.attributes)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not other:
            return False
        return self.lemma == other.lemma and self.root == other.root and self.syntactic_category == other.syntactic_category\
               and self.secondary_syntactic_category == other.secondary_syntactic_category and self.attributes == other.attributes

    def __hash__(self):
        result = hash((self.lemma,
                       self.root,
                       self.syntactic_category,
                       self.secondary_syntactic_category,
                       tuple(sorted(self.attributes))))
        return result

class DynamicLexeme(Lexeme):
    def __init__(self, lemma, root, syntactic_category, secondary_syntactic_category, attributes):
        Lexeme.__init__(self, lemma, root, syntactic_category, secondary_syntactic_category, attributes)