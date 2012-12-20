# coding=utf-8
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
from trnltk.morphology.phonetics.alphabet import TurkishAlphabet
from trnltk.morphology.model.lexeme import LexemeAttribute

class PhoneticExpectation(object):
    VowelStart = 'VowelStart'
    ConsonantStart = 'ConsonantStart'


class PhoneticAttributes(object):
    LastLetterVowel = "LastLetterVowel"
    LastLetterConsonant = "LastLetterConsonant"

    LastVowelFrontal = "LastVowelFrontal"
    LastVowelBack = "LastVowelBack"
    LastVowelRounded = "LastVowelRounded"
    LastVowelUnrounded = "LastVowelUnrounded"

    LastLetterVoiceless = "LastLetterVoiceless"
    LastLetterNotVoiceless = "LastLetterNotVoiceless"
    LastLetterContinuant = "LastLetterContinuant"
    LastLetterNotContinuant = "LastLetterNotContinuant"

    LastLetterVoicedStop = "LastLetterVoicedStop"
    LastLetterVoicelessStop = "LastLetterVoicelessStop"

    FirstLetterVowel = "FirstLetterVowel"
    FirstLetterConsonant = "FirstLetterConsonant"

    HasNoVowel = "HasNoVowel"


class Phonetics(object):
    @classmethod
    def is_suffix_form_applicable(cls, word, form_str):
        """
        Calculates the phonetics of the word and a suffix for and determines if the suffix form is applicable.
        @type word: unicode or None
        @type form_str: unicode or None
        @rtype: bool
        """
        if not form_str or not form_str.strip():
            return True

        if not word or not word.strip():
            return False

        word = word.strip()
        form_str = form_str.strip()

        phonetic_attributes = cls.calculate_phonetic_attributes_of_plain_sequence(word)

        # ci, dik, +yacak, +iyor, +ar, +yi, +im, +yla

        first_form_letter = TurkishAlphabet.get_letter_for_char(form_str[0])
        if first_form_letter.char_value == '+':
            # +yacak, +iyor, +ar, +yi, +im, +yla

            optional_letter = TurkishAlphabet.get_letter_for_char(form_str[1])
            if optional_letter.vowel:
                #+iyor, +ar, +im
                if PhoneticAttributes.LastLetterVowel in phonetic_attributes:
                    # ata, dana
                    return cls.is_suffix_form_applicable(word, form_str[2:])
                else:
                    # yap, kitap
                    return True

            else:
                # +yacak, +yi, +yla
                if PhoneticAttributes.LastLetterVowel in phonetic_attributes:
                    #ata, dana
                    return True
                else:
                    # yap, kitap
                    return cls.is_suffix_form_applicable(word, form_str[2:])

        else:
            if first_form_letter.vowel:
                return PhoneticAttributes.LastLetterVowel not in phonetic_attributes
            else:
                return True

    @classmethod
    def apply(cls, word, phonetic_attributes, form_str, lexeme_attributes=None):
        """
        Applies a suffix form to a word, considering the phonetics and root attributes given.
        @param word: Surface
        @type word: unicode
        @param phonetic_attributes: Provided phonetics of the surface
        @type phonetic_attributes: set of unicode
        @param form_str: Suffix form
        @type form_str: unicode
        @param lexeme_attributes: Provided lexeme attributes of the root of surface
        @type lexeme_attributes: set of unicode
        @return: Tuple (word, applied suffix form)
        @rtype: tuple
        """
        if not form_str or not form_str.strip():
            return word, u''

        if not word or not word.strip():
            return None, None

        # ci, dik, +yacak, +iyor, +ar, +yi, +im, +yla

        first_form_letter = TurkishAlphabet.get_letter_for_char(form_str[0])
        if first_form_letter.char_value == '+':
            # +yacak, +iyor, +ar, +yi, +im, +yla

            optional_letter = TurkishAlphabet.get_letter_for_char(form_str[1])
            if optional_letter.vowel:
                #+iyor, +ar, +im
                if PhoneticAttributes.LastLetterVowel in phonetic_attributes:
                    # ata, dana
                    return cls.apply(word, phonetic_attributes, form_str[2:], lexeme_attributes)
                else:
                    # yap, kitap
                    return cls._handle_phonetics(word, phonetic_attributes, form_str[1:], lexeme_attributes)

            else:
                # +yacak, +yi, +yla
                if PhoneticAttributes.LastLetterVowel in phonetic_attributes:
                    #ata, dana
                    return cls._handle_phonetics(word, phonetic_attributes, form_str[1:], lexeme_attributes)
                else:
                    # yap, kitap
                    return cls.apply(word, phonetic_attributes, form_str[2:], lexeme_attributes)

        else:
            return cls._handle_phonetics(word, phonetic_attributes, form_str, lexeme_attributes)

    @classmethod
    def _handle_phonetics(cls, word, phonetic_attributes, form_str, lexeme_attributes=None):
        lexeme_attributes = lexeme_attributes or []
        phonetic_attributes = phonetic_attributes or []

        first_letter_of_form = TurkishAlphabet.get_letter_for_char(form_str[0])

        # first apply voicing if possible
        if LexemeAttribute.NoVoicing not in lexeme_attributes and PhoneticAttributes.LastLetterVoicelessStop in phonetic_attributes and first_letter_of_form.vowel:
            voiced_letter = TurkishAlphabet.voice(TurkishAlphabet.get_letter_for_char(word[-1]))
            if voiced_letter:
                word = word[:-1] + voiced_letter.char_value

        # then try devoicing
        if PhoneticAttributes.LastLetterVoiceless in phonetic_attributes and TurkishAlphabet.devoice(first_letter_of_form):
            form_str = TurkishAlphabet.devoice(first_letter_of_form).char_value + form_str[1:]

        applied = u''

        for i in range(len(form_str)):
            c = form_str[i]
            next_c = form_str[i + 1] if i + 1 < len(form_str) else None

            if c == '!':
                continue

            letter = TurkishAlphabet.get_letter_for_char(c)
            if letter.vowel and letter.upper_case_char_value == c:
                if c == u'A':
                    if PhoneticAttributes.LastVowelBack in phonetic_attributes:
                        applied += u'a'
                    else:
                        applied += u'e'
                elif c == u'I':
                    if PhoneticAttributes.LastVowelBack in phonetic_attributes:
                        if PhoneticAttributes.LastVowelUnrounded in phonetic_attributes or next_c == '!':
                            applied += u'ı'
                        else:
                            applied += u'u'
                    else:
                        if PhoneticAttributes.LastVowelUnrounded in phonetic_attributes or next_c == '!':
                            applied += u'i'
                        else:
                            applied += u'ü'
                elif c == u'O':
                    if PhoneticAttributes.LastVowelBack in phonetic_attributes:
                        applied += u'o'
                    else:
                        applied += u'ö'

            else:
                applied = applied + c

        return word, applied

    @classmethod
    def expectations_satisfied(cls, phonetic_expectations, form_str):
        """
        Checks if a list of phonetic expectations are satisfied with the given suffix form string.
        @type phonetic_expectations: list
        @type form_str: unicode
        @rtype: bool
        """
        if not phonetic_expectations:
            return True

        if not form_str or not form_str.strip():
            return False

        form_str = form_str.strip()

        expectation_satisfaction_map = dict()

        for phonetic_expectation in phonetic_expectations:
            expectation_satisfaction_map[phonetic_expectation] = cls._expectation_satisfied(phonetic_expectation,
                form_str)

        return all(expectation_satisfaction_map.values())


    @classmethod
    def _expectation_satisfied(cls, phonetic_expectation, form_str):
        if phonetic_expectation == PhoneticExpectation.VowelStart:
            first_char = form_str[0]
            if first_char == '+':
                return cls._expectation_satisfied(phonetic_expectation, form_str[1:]) or cls._expectation_satisfied(
                    phonetic_expectation, form_str[2:])
            else:
                return TurkishAlphabet.get_letter_for_char(first_char).vowel

        elif phonetic_expectation == PhoneticExpectation.ConsonantStart:
            first_char = form_str[0]
            if first_char == '+':
                return cls._expectation_satisfied(phonetic_expectation, form_str[1:]) or cls._expectation_satisfied(
                    phonetic_expectation, form_str[2:])
            else:
                return not TurkishAlphabet.get_letter_for_char(first_char).vowel

        else:
            raise Exception('Unknown phonetic_expectation', phonetic_expectation)

    @classmethod
    def calculate_phonetic_attributes(cls, word, lexeme_attributes):
        """
        Calculates the phonetic attributes of a word, considering the root attributes of it.
        @type word: unicode
        @type lexeme_attributes: set of unicode
        @rtype: set
        """

        phonetic_attributes = cls.calculate_phonetic_attributes_of_plain_sequence(word)
        if lexeme_attributes and LexemeAttribute.InverseHarmony in lexeme_attributes:
            if PhoneticAttributes.LastVowelBack in phonetic_attributes:
                phonetic_attributes.remove(PhoneticAttributes.LastVowelBack)
                phonetic_attributes.add(PhoneticAttributes.LastVowelFrontal)

            elif PhoneticAttributes.LastVowelFrontal in phonetic_attributes:
                phonetic_attributes.remove(PhoneticAttributes.LastVowelFrontal)
                phonetic_attributes.add(PhoneticAttributes.LastVowelBack)

        return phonetic_attributes

    @classmethod
    def calculate_phonetic_attributes_of_plain_sequence(cls, seq):
        """
        Calculates the phonetic attributes of a word, without the root attributes of it.
        @type seq: unicode
        @rtype: set
        """
        attrs = []

        last_vowel = cls.get_last_vowel(seq)
        last_letter = TurkishAlphabet.get_letter_for_char(seq[-1])
        if last_vowel:
            if last_vowel.rounded:
                attrs.append(PhoneticAttributes.LastVowelRounded)
            else:
                attrs.append(PhoneticAttributes.LastVowelUnrounded)

            if last_vowel.frontal:
                attrs.append(PhoneticAttributes.LastVowelFrontal)
            else:
                attrs.append(PhoneticAttributes.LastVowelBack)

        if last_letter.vowel:
            attrs.append(PhoneticAttributes.LastLetterVowel)
        else:
            attrs.append(PhoneticAttributes.LastLetterConsonant)

        if last_letter.voiceless:
            attrs.append(PhoneticAttributes.LastLetterVoiceless)
            if not last_letter.continuant:
                attrs.append(PhoneticAttributes.LastLetterVoicelessStop)
        else:
            attrs.append(PhoneticAttributes.LastLetterNotVoiceless)
            if not last_letter.continuant and not last_letter.vowel:
                attrs.append(PhoneticAttributes.LastLetterVoicedStop)

        if last_letter.continuant:
            attrs.append(PhoneticAttributes.LastLetterContinuant)
        else:
            attrs.append(PhoneticAttributes.LastLetterNotContinuant)

        return set(attrs)

    @classmethod
    def get_last_vowel(cls, seq):
        for s in reversed(seq):
            turkish_letter = TurkishAlphabet.get_letter_for_char(s)
            if turkish_letter.vowel:
                return turkish_letter

    @classmethod
    def application_matches(cls, word, applied_str, voicing_allowed):
        """
        Checks if a suffix applied word is matched by a surface.

            >>> Phonetics.application_matches(u'armudunu', u'armut', True)
            True
            >>> Phonetics.application_matches(u'armudunu', u'armut', False)
            False
            >>> Phonetics.application_matches(u'armudunu', u'armudu', True)
            True
            >>> Phonetics.application_matches(u'armudunu', u'armudu', False)
            True

        @param word: The full word (surface)
        @param applied_str: Suffix applied part of the word
        @param voicing_allowed: If voicing should be considered or ignored
        @type word: unicode
        @type applied_str: unicode
        @type voicing_allowed: bool
        @rtype: L{bool}
        """
        if not applied_str or len(applied_str) > len(word):
            return False

        elif word == applied_str or word.startswith(applied_str):
            return True

        if  voicing_allowed and word.startswith(applied_str[:-1]):
            last_letter_of_application = TurkishAlphabet.get_letter_for_char(applied_str[-1])
            last_letter_of_word_part = TurkishAlphabet.get_letter_for_char(word[len(applied_str) - 1])
            return TurkishAlphabet.voice(last_letter_of_application) == last_letter_of_word_part

        else:
            return False