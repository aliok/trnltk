# coding=utf-8
__author__ = 'ali'

class TurkishLetter:
    def __init__(self, char_value, upper_case_char_value, alphabetic_index, vowel=False, frontal=False, rounded=False, voiceless=False,
                 stop_consonant=False, in_ascii=True, foreign=False, english_equivalent_char=None):
        self.char_value = char_value
        self.upper_case_char_value = upper_case_char_value
        self.alphabetic_index = alphabetic_index
        self.vowel = vowel
        self.frontal = frontal
        self.rounded = rounded
        self.voiceless = voiceless
        self.stop_consonant = stop_consonant
        self.in_ascii = in_ascii
        self.foreign = foreign
        self.english_equivalent_char = english_equivalent_char if english_equivalent_char else char_value

        self.check_consistency()

    def check_consistency(self):
        if ((self.voiceless or self.stop_consonant) and self.vowel) or (
            not self.vowel and (self.frontal or self.rounded)):
            raise Exception("Letter seems to have both vowel and Consonant attributes")
        elif (not self.in_ascii) and ('a' > self.char_value > 'z'):
            raise Exception("Marked as english alphabet but it is not." + self.char_value)
        elif self.alphabetic_index < 0:
            raise Exception("Alphabetical index must be positive:" + str(self.alphabetic_index))


class TurkishAlphabet:
    L_a = TurkishLetter(u'a', u'A', 1, vowel=True)
    L_b = TurkishLetter(u'b', u'B', 2)
    L_c = TurkishLetter(u'c', u'C', 3)
    L_cc = TurkishLetter(u'ç', u'Ç', 4, in_ascii=False, voiceless=True, stop_consonant=True, english_equivalent_char=u'c')
    L_d = TurkishLetter(u'd', u'D', 5)
    L_e = TurkishLetter(u'e', u'E', 6, vowel=True, frontal=True)
    L_f = TurkishLetter(u'f', u'F', 7, voiceless=True)
    L_g = TurkishLetter(u'g', u'G', 8)
    L_gg = TurkishLetter(u'ğ', u'Ğ', 9, in_ascii=False, english_equivalent_char=u'g')
    L_h = TurkishLetter(u'h', u'H', 10, voiceless=True)
    L_ii = TurkishLetter(u'ı', u'I', 11, vowel=True, in_ascii=False, english_equivalent_char=u'i')
    L_i = TurkishLetter(u'i', u'İ', 12, vowel=True, frontal=True)
    L_j = TurkishLetter(u'j', u'J', 13)
    L_k = TurkishLetter(u'k', u'K', 14, voiceless=True, stop_consonant=True)
    L_l = TurkishLetter(u'l', u'L', 15)
    L_m = TurkishLetter(u'm', u'M', 16)
    L_n = TurkishLetter(u'n', u'N', 17)
    L_o = TurkishLetter(u'o', u'O', 18, vowel=True, rounded=True)
    L_oo = TurkishLetter(u'ö', u'Ö', 19, vowel=True, frontal=True, rounded=True, in_ascii=False, english_equivalent_char=u'o')
    L_p = TurkishLetter(u'p', u'P', 20, voiceless=True, stop_consonant=True)
    L_r = TurkishLetter(u'r', u'R', 21)
    L_s = TurkishLetter(u's', u'S', 22, voiceless=True)
    L_ss = TurkishLetter(u'ş', u'Ş', 23, in_ascii=False, voiceless=True, english_equivalent_char=u's')
    L_t = TurkishLetter(u't', u'T', 24, voiceless=True, stop_consonant=True)
    L_u = TurkishLetter(u'u', u'U', 25, vowel=True, rounded=True)
    L_uu = TurkishLetter(u'ü', u'Ü', 26, vowel=True, rounded=True, frontal=True, in_ascii=False, english_equivalent_char=u'u')
    L_v = TurkishLetter(u'v', u'V', 27)
    L_y = TurkishLetter(u'y', u'Y', 28)
    L_z = TurkishLetter(u'z', u'Z', 29)

    L_q = TurkishLetter(u'q', u'Q', 30, foreign=True)
    L_w = TurkishLetter(u'w', u'W', 31, foreign=True)
    L_x = TurkishLetter(u'x', u'X', 32, foreign=True)

    L_ac = TurkishLetter(u'â', u'Â', 33, vowel=True, in_ascii=False, english_equivalent_char=u'a')
    L_ic = TurkishLetter(u'î', u'Î', 34, vowel=True, frontal=True, in_ascii=False, english_equivalent_char=u'i')
    L_uc = TurkishLetter(u'û', u'Û', 35, vowel=True, rounded=True, in_ascii=False, english_equivalent_char=u'u')

    Turkish_Letters = {L_a, L_b, L_c, L_cc, L_d, L_e, L_f, L_g,
                       L_gg, L_h, L_ii, L_i, L_j, L_k, L_l, L_m,
                       L_n, L_o, L_oo, L_p, L_r, L_s, L_ss, L_t,
                       L_u, L_uu, L_v, L_y, L_z, L_q, L_w, L_x,
                       L_ac, L_ic, L_uc}

    Devoicing_Map = {L_b: L_p, L_c: L_cc, L_d: L_t, L_g: L_k, L_gg: L_k}
    Voicing_Map =   {L_p: L_b, L_cc: L_c, L_t: L_d, L_g: L_gg, L_k: L_gg}

    @classmethod
    def get_letter_for_char(cls, char):
        #TODO: map!
        for letter in TurkishAlphabet.Turkish_Letters:
            if letter.char_value == char or letter.upper_case_char_value==char:
                return letter

        return TurkishLetter(char, char.upper(), 99)

    @classmethod
    def voice(cls, letter):
        if TurkishAlphabet.Voicing_Map.has_key(letter):
            return TurkishAlphabet.Voicing_Map[letter]
        else:
            return None

    @classmethod
    def devoice(cls, letter):
        if TurkishAlphabet.Devoicing_Map.has_key(letter):
            return TurkishAlphabet.Devoicing_Map[letter]
        else:
            return None