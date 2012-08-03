import copy
from trnltk.morphology.numbers.digitconverter import DigitsToNumberConverter
from trnltk.morphology.phonetics.alphabet import TurkishAlphabet
from trnltk.morphology.phonetics.phonetics import Phonetics
from trnltk.morphology.lexiconmodel.lexeme import DynamicLexeme, SyntacticCategory, SecondarySyntacticCategory

class Root(object):
    def __init__(self, root, lexeme, phonetic_expectations, phonetic_attributes):
        self.str = root
        self.lexeme = lexeme
        self.phonetic_expectations = phonetic_expectations if phonetic_attributes else []
        self.phonetic_attributes = phonetic_attributes if phonetic_attributes else []

    def __eq__(self, other):
        return self.str==other.str and self.lexeme==other.lexeme\
               and self.phonetic_expectations==other.phonetic_expectations\
        and self.phonetic_attributes==other.phonetic_attributes

    def __hash__(self):
        return hash((self.str,
                     tuple(sorted(self.phonetic_expectations or [])),
                     tuple(sorted(self.phonetic_attributes or []))
            ))

    def __str__(self):
        return u'{}({}) PH_ATTR:{} PH_EXPC:{}'.format(repr(self.str), self.lexeme, self.phonetic_attributes, self.phonetic_expectations)

    def __repr__(self):
        return self.__str__()

    def _clone(self):
        return Root(
            self.str,
            self.lexeme,
            copy.copy(self.phonetic_expectations) if self.phonetic_expectations else None,
            copy.copy(self.phonetic_attributes) if self.phonetic_attributes else None)

class NumeralRoot(Root):
    def __init__(self, numeral):
        root = numeral
        lexeme = DynamicLexeme(numeral, numeral, SyntacticCategory.NUMERAL, SecondarySyntacticCategory.DIGITS, None)
        phonetic_expectations = None
        phonetic_attributes = Phonetics.calculate_phonetic_attributes_of_plain_sequence(DigitsToNumberConverter.convert_digits_to_words(numeral))
        super(NumeralRoot, self).__init__(root, lexeme, phonetic_expectations, phonetic_attributes)

class AbbreviationRoot(Root):
    def __init__(self, abbr):
        root = abbr
        lexeme = DynamicLexeme(abbr, abbr, SyntacticCategory.NOUN, SecondarySyntacticCategory.ABBREVIATION, None)
        phonetic_attributes = None

        last_letter = TurkishAlphabet.get_letter_for_char(abbr[-1])
        if last_letter.vowel:
            phonetic_attributes = Phonetics.calculate_phonetic_attributes_of_plain_sequence(abbr)
        else:
            phonetic_attributes = Phonetics.calculate_phonetic_attributes_of_plain_sequence(abbr + u'E')

        phonetic_expectations = None
        super(AbbreviationRoot, self).__init__(root, lexeme, phonetic_expectations, phonetic_attributes)

class ProperNounRoot(Root):
    def __init__(self, noun):
        root = noun
        lexeme = DynamicLexeme(noun, noun, SyntacticCategory.NOUN, SecondarySyntacticCategory.PROPER_NOUN, None)
        phonetic_attributes = Phonetics.calculate_phonetic_attributes_of_plain_sequence(noun)
        phonetic_expectations = None
        super(ProperNounRoot, self).__init__(root, lexeme, phonetic_expectations, phonetic_attributes)
