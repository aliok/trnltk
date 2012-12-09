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
import copy
from trnltk.morphology.numbers.digitconverter import DigitsToNumberConverter
from trnltk.morphology.phonetics.alphabet import TurkishAlphabet
from trnltk.morphology.phonetics.phonetics import Phonetics
from trnltk.morphology.model.lexeme import DynamicLexeme, SyntacticCategory, SecondarySyntacticCategory

class Root(object):
    def __init__(self, root, lexeme, phonetic_expectations, phonetic_attributes):
        """
        @type root: unicode
        @type lexeme: Lexeme
        @type phonetic_expectations: set of str or None
        @type phonetic_attributes: set of str or None
        """
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

    def _clone(self, deep=False):
        return Root(
            self.str,
            self.lexeme.clone() if deep else self.lexeme,
            copy.copy(self.phonetic_expectations) if self.phonetic_expectations else None,
            copy.copy(self.phonetic_attributes) if self.phonetic_attributes else None)

class DynamicRoot(Root):
    def __init__(self, root, lexeme, phonetic_expectations, phonetic_attributes):
        """
        @type root: unicode
        @type lexeme: Lexeme
        @type phonetic_expectations: set of str or None
        @type phonetic_attributes: set of str or None
        """
        super(DynamicRoot, self).__init__(root, lexeme, phonetic_expectations, phonetic_attributes)

    def _clone(self, deep=False):
        return DynamicRoot(
            self.str,
            self.lexeme.clone() if deep else self.lexeme,
            copy.copy(self.phonetic_expectations) if self.phonetic_expectations else None,
            copy.copy(self.phonetic_attributes) if self.phonetic_attributes else None)

class NumeralRoot(DynamicRoot):
    def __init__(self, numeral):
        root = numeral
        lexeme = DynamicLexeme(numeral, numeral, SyntacticCategory.NUMERAL, SecondarySyntacticCategory.DIGITS, None)
        phonetic_expectations = None
        phonetic_attributes = Phonetics.calculate_phonetic_attributes_of_plain_sequence(DigitsToNumberConverter.convert_digits_to_words(numeral))
        super(NumeralRoot, self).__init__(root, lexeme, phonetic_expectations, phonetic_attributes)

    def _clone(self, deep=False):
        return NumeralRoot(self.str)

class AbbreviationRoot(DynamicRoot):
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

    def _clone(self, deep=False):
        return AbbreviationRoot(self.str)

class ProperNounRoot(DynamicRoot):
    def __init__(self, noun):
        root = noun
        lexeme = DynamicLexeme(noun, noun, SyntacticCategory.NOUN, SecondarySyntacticCategory.PROPER_NOUN, None)
        phonetic_attributes = Phonetics.calculate_phonetic_attributes_of_plain_sequence(noun)
        phonetic_expectations = None
        super(ProperNounRoot, self).__init__(root, lexeme, phonetic_expectations, phonetic_attributes)

    def _clone(self, deep=False):
        return ProperNounRoot(self.str)
