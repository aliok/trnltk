class PrimaryPosition:
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
    PUNCTUATION = "Punc"

    ALL = sorted({NOUN, ADJECTIVE, ADVERB, CONJUNCTION, INTERJECTION, VERB, PRONOUN, NUMERAL, DETERMINER, PARTICLE, PUNCTUATION})

class SecondaryPosition:
    DUPLICATOR = "Dup"
    POST_POSITIVE = "Postp"
    QUESTION = "Ques"
    DEMONSTRATIVE = "Demons"
    REFLEXIVE = "Reflex"
    PERSONAL = "Pers"
    TIME = "Time"
    PROPER_NOUN = "Prop"

    CARD = "Card"

    ALL = sorted({DUPLICATOR, POST_POSITIVE, QUESTION, DEMONSTRATIVE, PERSONAL, TIME, PROPER_NOUN, CARD})

#    NONE = "None"

class RootAttribute:
    Voicing = "Voicing"
    VoicingOpt = "VoicingOpt"
    NoVoicing = "NoVoicing"
    InverseHarmony = "InverseHarmony"
    LastVowelDrop = "LastVowelDrop"
    Doubling = "Doubling"
    StemChange = "StemChange"
    NounConsInsert = "NounConsInsert"
    NounConsInsert_n = "NounConsInsert_n"
    NoQuote = "NoQuote"
    Plural = "Plural"
    ProgressiveVowelDrop = "ProgressiveVowelDrop"
    Aorist_I = "Aorist_I"
    Aorist_A = "Aorist_A"
    NonTransitive = "NonTransitive"
    Passive_In = "Passive_In"
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
        Voicing, VoicingOpt, NoVoicing, InverseHarmony, LastVowelDrop, Doubling, StemChange, NounConsInsert, NounConsInsert_n,
        NoQuote, Plural, ProgressiveVowelDrop, Aorist_I, Aorist_A, NonTransitive, Passive_In, CompoundP3sg, Compound,
        Causative_t, Causative_It, Causative_Ir, Causative_Ar, Causative_dIr, Reflexive, Reciprocal, NoSuffix
    })

    CAUSATIVES = sorted({
        Causative_t, Causative_Ir, Causative_It, Causative_Ar, Causative_dIr
    })

class DictionaryItem:
    #TODO: make this and similar classes immutable
    def __init__(self, lemma, root, primary_position, secondary_position, attributes):
        self.lemma = lemma
        self.root = root
        self.primary_position = primary_position
        self.secondary_position = secondary_position
        self.attributes = attributes if attributes else []

    def clone(self):
        return DictionaryItem(self.lemma, self.root, self.primary_position, self.secondary_position, self.attributes[:])

    def __str__(self):
        return u'{}({})+{}+{} R_ATTR:{}'.format(repr(self.lemma), repr(self.root), self.primary_position, self.secondary_position, self.attributes)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not other:
            return False
        return self.lemma == other.lemma and self.root == other.root and self.primary_position == other.primary_position\
               and self.secondary_position == other.secondary_position and self.attributes == other.attributes

    def __hash__(self):
        result = hash((self.lemma,
                       self.root,
                       self.primary_position,
                       self.secondary_position,
                       tuple(sorted(self.attributes))))
        return result