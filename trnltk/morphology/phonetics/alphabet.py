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

class TurkishLetter(object):
    def __init__(self, char_value, upper_case_char_value, alphabetic_index, vowel=False, frontal=False, rounded=False, voiceless=False,
                 continuant=False, in_ascii=True, foreign=False, ascii_equivalent_char=None):
        """
        @type char_value: unicode
        @type upper_case_char_value: unicode
        @type alphabetic_index: int
        @type vowel: bool
        @type frontal: bool
        @type rounded: bool
        @type voiceless: bool
        @type in_ascii: bool
        @type foreign: bool
        @type ascii_equivalent_char: unicode
        """
        self.char_value = char_value
        self.upper_case_char_value = upper_case_char_value
        self.alphabetic_index = alphabetic_index
        self.vowel = vowel
        self.frontal = frontal
        self.rounded = rounded
        self.voiceless = voiceless
        self.continuant = continuant
        self.in_ascii = in_ascii
        self.foreign = foreign
        self.ascii_equivalent_char = ascii_equivalent_char if ascii_equivalent_char else char_value

        self._check_consistency()

    def _check_consistency(self):
        if ((self.voiceless or self.continuant) and self.vowel) or (
            not self.vowel and (self.frontal or self.rounded)):
            raise Exception("Letter seems to have both vowel and Consonant attributes")
        elif (not self.in_ascii) and ('a' > self.char_value > 'z'):
            raise Exception("Marked as English alphabet but it is not." + self.char_value)
        elif self.alphabetic_index < 0:
            raise Exception("Alphabetical index must be positive:" + str(self.alphabetic_index))

    def __eq__(self, other):
        if not other:
            return False

        return self.char_value==other.char_value and self.upper_case_char_value==other.upper_case_char_value

    def __hash__(self):
        return hash((self.char_value, self.upper_case_char_value))

class TurkishAlphabet(object):
    L_a =  TurkishLetter(u'a', u'A', 1, vowel=True)
    L_b =  TurkishLetter(u'b', u'B', 2, continuant=False)
    L_c =  TurkishLetter(u'c', u'C', 3, continuant=False)
    L_cc = TurkishLetter(u'ç', u'Ç', 4, continuant=False, voiceless=True, in_ascii=False, ascii_equivalent_char=u'c')
    L_d =  TurkishLetter(u'd', u'D', 5, continuant=False)
    L_e =  TurkishLetter(u'e', u'E', 6, vowel=True, frontal=True)
    L_f =  TurkishLetter(u'f', u'F', 7, continuant=True, voiceless=True)
    L_g =  TurkishLetter(u'g', u'G', 8, continuant=False)
    L_gg = TurkishLetter(u'ğ', u'Ğ', 9, continuant=True, in_ascii=False, ascii_equivalent_char=u'g')
    L_h =  TurkishLetter(u'h', u'H', 10, continuant=True, voiceless=True)
    L_ii = TurkishLetter(u'ı', u'I', 11, vowel=True, in_ascii=False, ascii_equivalent_char=u'i')
    L_i =  TurkishLetter(u'i', u'İ', 12, vowel=True, frontal=True)
    L_j =  TurkishLetter(u'j', u'J', 13, continuant=True)
    L_k =  TurkishLetter(u'k', u'K', 14, continuant=False, voiceless=True)
    L_l =  TurkishLetter(u'l', u'L', 15, continuant=True)
    L_m =  TurkishLetter(u'm', u'M', 16, continuant=True)
    L_n =  TurkishLetter(u'n', u'N', 17, continuant=True)
    L_o =  TurkishLetter(u'o', u'O', 18, vowel=True, rounded=True)
    L_oo = TurkishLetter(u'ö', u'Ö', 19, vowel=True, frontal=True, rounded=True, in_ascii=False, ascii_equivalent_char=u'o')
    L_p =  TurkishLetter(u'p', u'P', 20, continuant=False, voiceless=True)
    L_r =  TurkishLetter(u'r', u'R', 21, continuant=True)
    L_s =  TurkishLetter(u's', u'S', 22, continuant=True, voiceless=True)
    L_ss = TurkishLetter(u'ş', u'Ş', 23, continuant=True, voiceless=True, in_ascii=False, ascii_equivalent_char=u's')
    L_t =  TurkishLetter(u't', u'T', 24, continuant=False, voiceless=True)
    L_u =  TurkishLetter(u'u', u'U', 25, vowel=True, rounded=True)
    L_uu = TurkishLetter(u'ü', u'Ü', 26, vowel=True, rounded=True, frontal=True, in_ascii=False, ascii_equivalent_char=u'u')
    L_v =  TurkishLetter(u'v', u'V', 27, continuant=True)
    L_y =  TurkishLetter(u'y', u'Y', 28, continuant=True)
    L_z =  TurkishLetter(u'z', u'Z', 29, continuant=True)

    L_q =  TurkishLetter(u'q', u'Q', 30, foreign=True)
    L_w =  TurkishLetter(u'w', u'W', 31, foreign=True)
    L_x =  TurkishLetter(u'x', u'X', 32, foreign=True)

    L_ac = TurkishLetter(u'â', u'Â', 33, vowel=True, in_ascii=False, ascii_equivalent_char=u'a')
    L_ic = TurkishLetter(u'î', u'Î', 34, vowel=True, frontal=True, in_ascii=False, ascii_equivalent_char=u'i')
    L_uc = TurkishLetter(u'û', u'Û', 35, vowel=True, rounded=True, in_ascii=False, ascii_equivalent_char=u'u')

    Turkish_Letters = {L_a, L_b, L_c, L_cc, L_d, L_e, L_f, L_g,
                       L_gg, L_h, L_ii, L_i, L_j, L_k, L_l, L_m,
                       L_n, L_o, L_oo, L_p, L_r, L_s, L_ss, L_t,
                       L_u, L_uu, L_v, L_y, L_z, L_q, L_w, L_x,
                       L_ac, L_ic, L_uc}

    Consonants = set([l for l in Turkish_Letters if not l.vowel])
    Vowels = set([l for l in Turkish_Letters if l.vowel])

    Devoicing_Map = {L_b: L_p, L_c: L_cc, L_d: L_t, L_g: L_k}
    Voicing_Map =   {L_p: L_b, L_cc: L_c, L_t: L_d, L_g: L_gg, L_k: L_gg}

    Inverse_Voicing_Map = {L_b: {L_p}, L_c: {L_cc}, L_d: {L_t}, L_g: {L_k}, L_gg : {L_g, L_k}}

    Lower_Case_Letter_Map = None
    Upper_Case_Letter_Map = None

    @classmethod
    def get_letter_for_char(cls, char):
        """
        @type char: str or unicode
        @rtype: TurkishLetter
        """

        assert char and len(char)==1

        if TurkishAlphabet.Lower_Case_Letter_Map.has_key(char):
            return TurkishAlphabet.Lower_Case_Letter_Map[char]

        elif TurkishAlphabet.Upper_Case_Letter_Map.has_key(char):
            return TurkishAlphabet.Upper_Case_Letter_Map[char]

        return TurkishLetter(char, char.upper(), 99)

    @classmethod
    def get_letter_for_upper_case_char(cls, char):
        if TurkishAlphabet.Upper_Case_Letter_Map.has_key(char):
            return TurkishAlphabet.Upper_Case_Letter_Map[char]
        return None

    @classmethod
    def voice(cls, letter):
        """
        @type letter: TurkishLetter
        @rtype: TurkishLetter
        """
        if TurkishAlphabet.Voicing_Map.has_key(letter):
            return TurkishAlphabet.Voicing_Map[letter]
        else:
            return None

    @classmethod
    def devoice(cls, letter):
        """
        @type letter: TurkishLetter
        @rtype: TurkishLetter
        """
        if TurkishAlphabet.Devoicing_Map.has_key(letter):
            return TurkishAlphabet.Devoicing_Map[letter]
        else:
            return None

    @classmethod
    def lower(cls, word):
        if not word:
            return word
        lower_word = u''
        for c in word:
            if c.isupper():
                letter_for_upper_char = cls.get_letter_for_upper_case_char(c)
                if letter_for_upper_char:
                    lower_word += letter_for_upper_char.char_value
                else:
                    lower_word += letter_for_upper_char.lower()
            else:
                lower_word += c.lower()

        return lower_word

    @classmethod
    def _initialize(cls):
        if not TurkishAlphabet.Lower_Case_Letter_Map or not TurkishAlphabet.Upper_Case_Letter_Map:
            TurkishAlphabet.Lower_Case_Letter_Map = {}
            TurkishAlphabet.Upper_Case_Letter_Map = {}

            for letter in TurkishAlphabet.Turkish_Letters:
                TurkishAlphabet.Lower_Case_Letter_Map[letter.char_value] = letter
                TurkishAlphabet.Upper_Case_Letter_Map[letter.upper_case_char_value] = letter


TurkishAlphabet._initialize()