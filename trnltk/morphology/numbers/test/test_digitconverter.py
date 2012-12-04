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
import unittest
from hamcrest import *
from trnltk.morphology.numbers.digitconverter import DigitsToNumberConverter

class DigitsToNumberConverterTest(unittest.TestCase):
    def test_should_parse(self):
        cdtw = DigitsToNumberConverter.convert_digits_to_words

        assert_that(cdtw(u'0'), equal_to(u'sıfır'))
        assert_that(cdtw(u'5'), equal_to(u'beş'))
        assert_that(cdtw(u'10'), equal_to(u'on'))
        assert_that(cdtw(u'12'), equal_to(u'on iki'))
        assert_that(cdtw(u'200'), equal_to(u'iki yüz'))
        assert_that(cdtw(u'1000'), equal_to(u'bin'))
        assert_that(cdtw(u'1001'), equal_to(u'bin bir'))
        assert_that(cdtw(u'1010'), equal_to(u'bin on'))
        assert_that(cdtw(u'1100'), equal_to(u'bin yüz'))
        assert_that(cdtw(u'1110'), equal_to(u'bin yüz on'))
        assert_that(cdtw(u'1111'), equal_to(u'bin yüz on bir'))
        assert_that(cdtw(u'5601'), equal_to(u'beş bin altı yüz bir'))
        assert_that(cdtw(u'999999'), equal_to(u'dokuz yüz doksan dokuz bin dokuz yüz doksan dokuz'))
        assert_that(cdtw(u'1000000'), equal_to(u'bir milyon'))
        assert_that(cdtw(u'999999999999999999999999999999999999999999999999999999999999999999'), equal_to(
            u'dokuz yüz doksan dokuz vigintilyon dokuz yüz doksan dokuz novemdesilyon dokuz yüz doksan dokuz oktodesilyon dokuz yüz doksan dokuz septendesilyon dokuz yüz doksan dokuz seksdesilyon dokuz yüz doksan dokuz kendesilyon dokuz yüz doksan dokuz katordesilyon dokuz yüz doksan dokuz tredesilyon dokuz yüz doksan dokuz dodesilyon dokuz yüz doksan dokuz undesilyon dokuz yüz doksan dokuz desilyon dokuz yüz doksan dokuz nonilyon dokuz yüz doksan dokuz oktilyon dokuz yüz doksan dokuz septilyon dokuz yüz doksan dokuz seksilyon dokuz yüz doksan dokuz kentilyon dokuz yüz doksan dokuz katrilyon dokuz yüz doksan dokuz trilyon dokuz yüz doksan dokuz milyar dokuz yüz doksan dokuz milyon dokuz yüz doksan dokuz bin dokuz yüz doksan dokuz'))

        assert_that(cdtw(u'-0'), equal_to(u'sıfır'))
        assert_that(cdtw(u'-5'), equal_to(u'eksi beş'))
        assert_that(cdtw(u'-10'), equal_to(u'eksi on'))
        assert_that(cdtw(u'-12'), equal_to(u'eksi on iki'))
        assert_that(cdtw(u'-200'), equal_to(u'eksi iki yüz'))
        assert_that(cdtw(u'-1000'), equal_to(u'eksi bin'))
        assert_that(cdtw(u'-1001'), equal_to(u'eksi bin bir'))
        assert_that(cdtw(u'-1010'), equal_to(u'eksi bin on'))
        assert_that(cdtw(u'-1100'), equal_to(u'eksi bin yüz'))
        assert_that(cdtw(u'-1110'), equal_to(u'eksi bin yüz on'))
        assert_that(cdtw(u'-1111'), equal_to(u'eksi bin yüz on bir'))
        assert_that(cdtw(u'-5601'), equal_to(u'eksi beş bin altı yüz bir'))
        assert_that(cdtw(u'-999999'), equal_to(u'eksi dokuz yüz doksan dokuz bin dokuz yüz doksan dokuz'))
        assert_that(cdtw(u'-1000000'), equal_to(u'eksi bir milyon'))
        assert_that(cdtw(u'-999999999999999999999999999999999999999999999999999999999999999999'), equal_to(
            u'eksi dokuz yüz doksan dokuz vigintilyon dokuz yüz doksan dokuz novemdesilyon dokuz yüz doksan dokuz oktodesilyon dokuz yüz doksan dokuz septendesilyon dokuz yüz doksan dokuz seksdesilyon dokuz yüz doksan dokuz kendesilyon dokuz yüz doksan dokuz katordesilyon dokuz yüz doksan dokuz tredesilyon dokuz yüz doksan dokuz dodesilyon dokuz yüz doksan dokuz undesilyon dokuz yüz doksan dokuz desilyon dokuz yüz doksan dokuz nonilyon dokuz yüz doksan dokuz oktilyon dokuz yüz doksan dokuz septilyon dokuz yüz doksan dokuz seksilyon dokuz yüz doksan dokuz kentilyon dokuz yüz doksan dokuz katrilyon dokuz yüz doksan dokuz trilyon dokuz yüz doksan dokuz milyar dokuz yüz doksan dokuz milyon dokuz yüz doksan dokuz bin dokuz yüz doksan dokuz'))

        assert_that(cdtw(u'+0'), equal_to(u'sıfır'))
        assert_that(cdtw(u'+5'), equal_to(u'beş'))
        assert_that(cdtw(u'+10'), equal_to(u'on'))
        assert_that(cdtw(u'+12'), equal_to(u'on iki'))
        assert_that(cdtw(u'+200'), equal_to(u'iki yüz'))
        assert_that(cdtw(u'+1000'), equal_to(u'bin'))
        assert_that(cdtw(u'+1001'), equal_to(u'bin bir'))
        assert_that(cdtw(u'+1010'), equal_to(u'bin on'))
        assert_that(cdtw(u'+1100'), equal_to(u'bin yüz'))
        assert_that(cdtw(u'+1110'), equal_to(u'bin yüz on'))
        assert_that(cdtw(u'+1111'), equal_to(u'bin yüz on bir'))
        assert_that(cdtw(u'+5601'), equal_to(u'beş bin altı yüz bir'))
        assert_that(cdtw(u'+999999'), equal_to(u'dokuz yüz doksan dokuz bin dokuz yüz doksan dokuz'))
        assert_that(cdtw(u'+1000000'), equal_to(u'bir milyon'))
        assert_that(cdtw(u'+999999999999999999999999999999999999999999999999999999999999999999'), equal_to(
            u'dokuz yüz doksan dokuz vigintilyon dokuz yüz doksan dokuz novemdesilyon dokuz yüz doksan dokuz oktodesilyon dokuz yüz doksan dokuz septendesilyon dokuz yüz doksan dokuz seksdesilyon dokuz yüz doksan dokuz kendesilyon dokuz yüz doksan dokuz katordesilyon dokuz yüz doksan dokuz tredesilyon dokuz yüz doksan dokuz dodesilyon dokuz yüz doksan dokuz undesilyon dokuz yüz doksan dokuz desilyon dokuz yüz doksan dokuz nonilyon dokuz yüz doksan dokuz oktilyon dokuz yüz doksan dokuz septilyon dokuz yüz doksan dokuz seksilyon dokuz yüz doksan dokuz kentilyon dokuz yüz doksan dokuz katrilyon dokuz yüz doksan dokuz trilyon dokuz yüz doksan dokuz milyar dokuz yüz doksan dokuz milyon dokuz yüz doksan dokuz bin dokuz yüz doksan dokuz'))

        assert_that(cdtw(u'0,0'), equal_to(u'sıfır virgül sıfır'))
        assert_that(cdtw(u'0,000'), equal_to(u'sıfır virgül sıfır sıfır sıfır'))
        assert_that(cdtw(u'0,001'), equal_to(u'sıfır virgül sıfır sıfır bir'))
        assert_that(cdtw(u'-10,896'), equal_to(u'eksi on virgül sekiz yüz doksan altı'))
        assert_that(cdtw(u'+2567,01000'), equal_to(u'iki bin beş yüz altmış yedi virgül sıfır bin'))
        assert_that(
            cdtw(u'-999999999999999999999999999999999999999999999999999999999999999999,999999999999999999999999999999999999999999999999999999999999999999'),
            equal_to(
                u'eksi dokuz yüz doksan dokuz vigintilyon dokuz yüz doksan dokuz novemdesilyon dokuz yüz doksan dokuz oktodesilyon dokuz yüz doksan dokuz septendesilyon dokuz yüz doksan dokuz seksdesilyon dokuz yüz doksan dokuz kendesilyon dokuz yüz doksan dokuz katordesilyon dokuz yüz doksan dokuz tredesilyon dokuz yüz doksan dokuz dodesilyon dokuz yüz doksan dokuz undesilyon dokuz yüz doksan dokuz desilyon dokuz yüz doksan dokuz nonilyon dokuz yüz doksan dokuz oktilyon dokuz yüz doksan dokuz septilyon dokuz yüz doksan dokuz seksilyon dokuz yüz doksan dokuz kentilyon dokuz yüz doksan dokuz katrilyon dokuz yüz doksan dokuz trilyon dokuz yüz doksan dokuz milyar dokuz yüz doksan dokuz milyon dokuz yüz doksan dokuz bin dokuz yüz doksan dokuz virgül dokuz yüz doksan dokuz vigintilyon dokuz yüz doksan dokuz novemdesilyon dokuz yüz doksan dokuz oktodesilyon dokuz yüz doksan dokuz septendesilyon dokuz yüz doksan dokuz seksdesilyon dokuz yüz doksan dokuz kendesilyon dokuz yüz doksan dokuz katordesilyon dokuz yüz doksan dokuz tredesilyon dokuz yüz doksan dokuz dodesilyon dokuz yüz doksan dokuz undesilyon dokuz yüz doksan dokuz desilyon dokuz yüz doksan dokuz nonilyon dokuz yüz doksan dokuz oktilyon dokuz yüz doksan dokuz septilyon dokuz yüz doksan dokuz seksilyon dokuz yüz doksan dokuz kentilyon dokuz yüz doksan dokuz katrilyon dokuz yüz doksan dokuz trilyon dokuz yüz doksan dokuz milyar dokuz yüz doksan dokuz milyon dokuz yüz doksan dokuz bin dokuz yüz doksan dokuz'))

        assert_that(cdtw(u'000200'), equal_to(u'sıfır sıfır sıfır iki yüz'))
        assert_that(cdtw(u'-000200'), equal_to(u'eksi sıfır sıfır sıfır iki yüz'))
        assert_that(cdtw(u'+000200'), equal_to(u'sıfır sıfır sıfır iki yüz'))

        assert_that(cdtw(u'5,0'), equal_to(u'beş virgül sıfır'))
        assert_that(cdtw(u'-5,000'), equal_to(u'eksi beş virgül sıfır sıfır sıfır'))
        assert_that(cdtw(u'+5,000'), equal_to(u'beş virgül sıfır sıfır sıfır'))

if __name__ == '__main__':
    unittest.main()