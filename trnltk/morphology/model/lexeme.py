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
    NOUN = u"Noun"
    ADJECTIVE = u"Adj"
    ADVERB = u"Adv"
    CONJUNCTION = u"Conj"
    INTERJECTION = u"Interj"
    VERB = u"Verb"
    PRONOUN = u"Pron"
    NUMERAL = u"Num"
    DETERMINER = u"Det"
    PARTICLE = u"Part"
    QUESTION = u"Ques"
    PUNCTUATION = u"Punc"

    ALL = sorted(
        {NOUN, ADJECTIVE, ADVERB, CONJUNCTION, INTERJECTION, VERB, PRONOUN, NUMERAL, DETERMINER, PARTICLE, QUESTION,
         PUNCTUATION})


class SecondarySyntacticCategory(object):
    DUPLICATOR = u"Dup"
    POST_POSITIVE = u"Postp"
    QUESTION = u"Ques"
    DEMONSTRATIVE = u"Demons"
    REFLEXIVE = u"Reflex"
    PERSONAL = u"Pers"
    TIME = u"Time"
    PROPER_NOUN = u"Prop"
    ABBREVIATION = u"Abbr"

    CARD = u"Card"
    ORD = u"Ord"
    DIGITS = u"Digits"

    ALL = sorted(
        {DUPLICATOR, POST_POSITIVE, QUESTION, DEMONSTRATIVE, REFLEXIVE, PERSONAL, TIME, PROPER_NOUN, ABBREVIATION, CARD,
         ORD})


class LexemeAttribute(object):
    # attributes applicable to all
    Voicing = u"Voicing"
    VoicingOpt = u"VoicingOpt"
    NoVoicing = u"NoVoicing"
    InverseHarmony = u"InverseHarmony"
    LastVowelDrop = u"LastVowelDrop"
    Doubling = u"Doubling"
    RootChange = u"RootChange"
    Plural = u"Plural"
    NoSuffix = u"NoSuffix"

    # noun attributes
    CompoundP3sg = u"CompoundP3sg"

    # verb attributes
    ProgressiveVowelDrop = u"ProgressiveVowelDrop"
    Aorist_I = u"Aorist_I"
    Aorist_A = u"Aorist_A"
    Causative_t = u"Causative_t"
    Causative_Ir = u"Causative_Ir"
    Causative_It = u"Causative_It"
    Causative_Ar = u"Causative_Ar"
    Causative_dIr = u"Causative_dIr"
    Passive_Il = u"Passive_Il"
    Passive_In = u"Passive_In"
    Passive_InIl = u"Passive_InIl"

    ALL = sorted({
        Voicing, VoicingOpt, NoVoicing, InverseHarmony, LastVowelDrop, Doubling, RootChange,
        Plural, ProgressiveVowelDrop, Aorist_I, Aorist_A, Passive_Il, Passive_In, Passive_InIl,
        CompoundP3sg, Causative_t, Causative_It, Causative_Ir, Causative_Ar, Causative_dIr, NoSuffix
    })

    CAUSATIVES = sorted({
        Causative_t, Causative_Ir, Causative_It, Causative_Ar, Causative_dIr
    })


class Lexeme(object):
    #TODO: make this and similar classes immutable
    def __init__(self, lemma, root, syntactic_category, secondary_syntactic_category, attributes):
        """
        @type lemma: unicode
        @type root: unicode
        @type syntactic_category: unicode
        @type secondary_syntactic_category: unicode or None
        @type attributes: set of unicode or None
        """
        self.lemma = lemma
        self.root = root
        self.syntactic_category = syntactic_category
        self.secondary_syntactic_category = secondary_syntactic_category
        self.attributes = attributes if attributes else set()

    def clone(self):
        return Lexeme(self.lemma, self.root, self.syntactic_category, self.secondary_syntactic_category,
            set(self.attributes))

    def __str__(self):
        return u'{}({})+{}+{} R_ATTR:{}'.format(repr(self.lemma), repr(self.root), self.syntactic_category,
            self.secondary_syntactic_category, self.attributes)

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