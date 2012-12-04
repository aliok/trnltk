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
import re

class DigitsToNumberConverter(object):
    COMMA_NAME = u'virgül'
    MINUS_NAME = u'eksi'

    NEGATIVE_SIGN = u'-'
    POSITIVE_SIGN = u'+'

    FRACTION_SEPARATOR = ','
    GROUPING_SEPARATOR = '.'

    TURKISH_NUMBER_PATTERN = u'^[-+]?\d+(,\d)?\d*$'
    TURKISH_NUMBER_REGEX = re.compile(TURKISH_NUMBER_PATTERN)
    MAX_GROUP_BASE = 63
    MAX_NATURAL_NUMBER_SUPPORTED = pow(10, 66) - 1

    ZERO_NAME = u'sıfır'

    NUMERAL_SYMBOL_NAMES = {
        0: u'sıfır',
        1: u'bir',
        2: u'iki',
        3: u'üç',
        4: u'dört',
        5: u'beş',
        6: u'altı',
        7: u'yedi',
        8: u'sekiz',
        9: u'dokuz',
        }

    TENS_MULTIPLES_NAMES = {
        1: u'on',
        2: u'yirmi',
        3: u'otuz',
        4: u'kırk',
        5: u'elli',
        6: u'altmış',
        7: u'yetmiş',
        8: u'seksen',
        9: u'doksan',
        }

    HUNDRED_NAME = u'yüz'
    THOUSAND_NAME = u'bin'

    THOUSAND_POWER_NAMES = {
        0: "",
        1: u'bin',
        2: u'milyon',
        3: u'milyar',
        4: u'trilyon',
        5: u'katrilyon',
        6: u'kentilyon',
        7: u'seksilyon',
        8: u'septilyon',
        9: u'oktilyon',
        10: u'nonilyon',
        11: u'desilyon',
        12: u'undesilyon',
        13: u'dodesilyon',
        14: u'tredesilyon',
        15: u'katordesilyon',
        16: u'kendesilyon',
        17: u'seksdesilyon',
        18: u'septendesilyon',
        19: u'oktodesilyon',
        20: u'novemdesilyon',
        21: u'vigintilyon'
    }

    @classmethod
    def _add_text_for_leading_zeros(cls, integer_str, word):
        number_of_leading_zeros = cls._get_number_of_leading_zeros(integer_str)
        for i in range(0, number_of_leading_zeros):
            word = cls.ZERO_NAME + u' ' + word
        return word

    @classmethod
    def convert_digits_to_words(cls, digits):
        """
        Converts a number in digits to string representation.

            >>> convert_digits_to_words('1234,0245123')
            u'bin iki yüz otuz dört virgül sıfır iki yüz kırk beş bin yüz yirmi üç'
            >>> convert_digits_to_words('-1.234,0245123')
            u'eksi bin iki yüz otuz dört virgül sıfır iki yüz kırk beş bin yüz yirmi üç'

        @type digits: str or unicode
        @rtype: unicode
        @raise: Exception if P{digits} is not a valid Turkish number
        """
        if not digits:
            return None

        digits = unicode(digits)
        digits = digits.replace(cls.GROUPING_SEPARATOR, '')

        if not cls.TURKISH_NUMBER_REGEX.match(digits):
            raise Exception(u'{} is not a valid number. The allowed pattern is : {}'.format(digits, str(cls.TURKISH_NUMBER_PATTERN)))

        integer_str = None
        fraction_str = None

        if cls.FRACTION_SEPARATOR in digits:
            integer_str = digits[:digits.find(cls.FRACTION_SEPARATOR)]
            fraction_str = digits[digits.find(cls.FRACTION_SEPARATOR) + 1:]
        else:
            integer_str = digits
            fraction_str = None

        integer_part = int(integer_str)
        fraction_part = int(fraction_str) if fraction_str else 0

        word_integer_part = cls._convert_natural_number_to_words(abs(integer_part))
        word_fraction_part = cls._convert_natural_number_to_words(fraction_part)

        word_integer_part = cls._add_text_for_leading_zeros(integer_str, word_integer_part)
        word_fraction_part = cls._add_text_for_leading_zeros(fraction_str, word_fraction_part) if fraction_str else word_fraction_part

        if integer_part < 0:
            word_integer_part = cls.MINUS_NAME + u' ' + word_integer_part

        if cls.FRACTION_SEPARATOR in digits:
            return u'{} {} {}'.format(word_integer_part, cls.COMMA_NAME, word_fraction_part)
        else:
            return word_integer_part

    @classmethod
    def _convert_natural_number_to_words(cls, integer_nr):
        if integer_nr < 0:
            raise Exception('Argument is negative : {}'.format(integer_nr))

        if integer_nr > cls.MAX_NATURAL_NUMBER_SUPPORTED:
            raise Exception(
                'Fraction {} of the given number is larger than the maximum supported natural number: {}'.format(integer_nr, cls.MAX_NATURAL_NUMBER_SUPPORTED))

        result = u''

        integer_nr = abs(integer_nr)

        # do it manually for words below 1000
        if integer_nr < 10:
            result = cls.NUMERAL_SYMBOL_NAMES[integer_nr]
        elif integer_nr < 100:
            tens_digit = integer_nr / 10
            ones_digit = integer_nr % 10
            result = u'{} {}'.format(cls.TENS_MULTIPLES_NAMES[tens_digit], cls._convert_natural_number_to_words(ones_digit) if ones_digit > 0 else u'')
        elif integer_nr < 1000:
            hundreds_digit = integer_nr / 100
            rest = integer_nr % 100
            rest_str = cls._convert_natural_number_to_words(rest) if rest > 0 else u''
            if hundreds_digit == 0:
                result = rest_str
            elif hundreds_digit == 1:
                result = u'{} {}'.format(cls.HUNDRED_NAME, rest_str)
            else:
                result = u'{} {} {}'.format(cls._convert_natural_number_to_words(hundreds_digit), cls.HUNDRED_NAME, rest_str)
        else:
            most_significant_group_base = cls._find_most_significant_group_base(integer_nr)
            for i in range(most_significant_group_base / 3, 0, -1):
                group_nr = cls._get_nth_group_nr(integer_nr, i)
                if group_nr == 0:       # don't write 'sifir milyon'
                    pass
                elif group_nr == 1 and i == 1:      # don't write 'bir bin', but write 'bir milyon'(below)
                    result += u' {}'.format(cls.THOUSAND_NAME)
                else:
                    group_nr_str = cls._convert_natural_number_to_words(group_nr)
                    result += u' {} {} '.format(group_nr_str, cls.THOUSAND_POWER_NAMES[i])

                result = result.strip()

            last_group_nr = integer_nr % 1000
            if last_group_nr > 0:
                result += u' ' + cls._convert_natural_number_to_words(last_group_nr)

        return result.strip()

    @classmethod
    def _find_most_significant_group_base(cls, integer_nr):
        i = cls.MAX_GROUP_BASE / 3
        while pow(10, i * 3) > integer_nr:
            i -= 1

        return i * 3

    @classmethod
    def _get_nth_group_nr(cls, integer_nr, n):
        integer_nr /= pow(1000, n)
        integer_nr %= 1000
        return integer_nr

    @classmethod
    def _get_number_of_leading_zeros(cls, integer_str):
        if integer_str.startswith(cls.NEGATIVE_SIGN) or integer_str.startswith(cls.POSITIVE_SIGN):
            integer_str = integer_str[1:]
        integer_str_wo_leading_zeros = str(int(integer_str))
        return len(integer_str) - len(integer_str_wo_leading_zeros)