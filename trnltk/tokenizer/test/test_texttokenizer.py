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
from trnltk.tokenizer.texttokenizer import TextTokenizer

class TextTokenizerTest(unittest.TestCase):
    def setUp(self):
        self.tokenizer = TextTokenizer()

    def test_should_tokenize_text(self):
        text = u"""Fiyatları uçuşa geçti."""
        tokens = self.tokenizer.tokenize(text)
        assert_that(tokens, has_items(u'Fiyatları', u'uçuşa', u'geçti', u'.'))

        text = u"""Fiyatları uçuşa geçti. """
        tokens = self.tokenizer.tokenize(text)
        assert_that(tokens, has_items(u'Fiyatları', u'uçuşa', u'geçti', u'.'))

        text = u""" Fiyatları uçuşa geçti."""
        tokens = self.tokenizer.tokenize(text)
        assert_that(tokens, has_items(u'Fiyatları', u'uçuşa', u'geçti', u'.'))

        text = u"""Fiyatları uçuşa geçti ."""
        tokens = self.tokenizer.tokenize(text)
        assert_that(tokens, has_items(u'Fiyatları', u'uçuşa', u'geçti', u'.'))

        text = u"""\r\t\p\nFiyatları\n \t\r\n  uçuşa \rgeçti .   \t"""
        tokens = self.tokenizer.tokenize(text)
        assert_that(tokens, has_items(u'Fiyatları', u'uçuşa', u'geçti', u'.'))


    def test_should_tokenize_text_with_exceptions(self):
        text = u"""\r\tABD'de\n elma fiyatları\n \t\r\n  uçuşa \rgeçti .   \t"""
        tokens = self.tokenizer.tokenize(text)
        assert_that(tokens, has_items(u'ABD\'de', u'elma', u'fiyatları', u'uçuşa', u'geçti', u'.'))

        text = u"""\r\tABD'de\n elma fiyatları\n \t\r\n  uçuşa \rgeçti ..   \t"""
        tokens = self.tokenizer.tokenize(text)
        assert_that(tokens, has_items(u'ABD\'de', u'elma', u'fiyatları', u'uçuşa', u'geçti', u'..'))

        text = u"""\r\tABD'de\n elma fiyatları\n \t\r\n  uçuşa \rgeçti !..   \t"""
        tokens = self.tokenizer.tokenize(text)
        assert_that(tokens, has_items(u'ABD\'de', u'elma', u'fiyatları', u'uçuşa', u'geçti', u'!..'))

        text = u"""\r\tABD'de\n elma fiyatları\n \t\r\n 3.  uçuşa \rgeçti .   \t"""
        tokens = self.tokenizer.tokenize(text)
        assert_that(tokens, has_items(u'ABD\'de', u'elma', u'fiyatları', u'3.', u'uçuşa', u'geçti', u'.'))

        text = u"""\r\tABD'de\n elma fiyatları\n \t\r\n 5'te uçuşa \rgeçti .   \t"""
        tokens = self.tokenizer.tokenize(text)
        assert_that(tokens, has_items(u'ABD\'de', u'elma', u'fiyatları', u'5\'te', u'uçuşa', u'geçti', u'.'))

        text = u"""\r\tABD'de\n elma fiyatları\n \t\r\n 5.'de uçuşa \rgeçti .   \t"""
        tokens = self.tokenizer.tokenize(text)
        assert_that(tokens, has_items(u'ABD\'de', u'elma', u'fiyatları', u'5.\'de', u'uçuşa', u'geçti', u'.'))

        text = u"5:20 gibi gelecek."
        tokens = self.tokenizer.tokenize(text)
        assert_that(tokens, has_items(u'5:20', u'gibi', u'gelecek', u'.'))

        text = u"5,60 TL verdim."
        tokens = self.tokenizer.tokenize(text)
        assert_that(tokens, has_items(u'5,60', u'TL', u'verdim', u'.'))

        text = u"5.600 TL verdim."
        tokens = self.tokenizer.tokenize(text)
        assert_that(tokens, has_items(u'5.600', u'TL', u'verdim', u'.'))

        text = u"5.600,1234 TL verdim."
        tokens = self.tokenizer.tokenize(text)
        assert_that(tokens, has_items(u'5.600,1234', u'TL', u'verdim', u'.'))

        text = u"100'le gidiyor."
        tokens = self.tokenizer.tokenize(text)
        assert_that(tokens, has_items(u'100\'le', u'gidiyor', u'.'))

        text = u"5:20'de geliyorum."
        tokens = self.tokenizer.tokenize(text)
        assert_that(tokens, has_items(u'5:20\'de', u'geliyorum', u'.'))

        text = u"5,74'te bir ihtimal."
        tokens = self.tokenizer.tokenize(text)
        assert_that(tokens, has_items(u'5,74\'te', u'bir', u'ihtimal', u'.'))

        text = u"6, 7 ve 8 numara gelsin."
        tokens = self.tokenizer.tokenize(text)
        assert_that(tokens, has_items(u'6', u'7', u've', u'8', u'numara', u'gelsin', u'.'))

        text = u"6., 7. ve 8. adamlar gelsin."
        tokens = self.tokenizer.tokenize(text)
        assert_that(tokens, has_items(u'6.', u'7.', u've', u'8.', u'adamlar', u'gelsin', u'.'))


    def test_should_tokenize_longer_text(self):
        text = u"""
ABD'den gelen veriyle altın fiyatları uçuşa geçti.
ABD'de tarım dışı istihdamın beklentilerin altında artmasının ardından küresel piyasalarda ABD Merkez Bankası'nın yavaşlayan ekonomiye önlem olarak yeni bir parasal gevşemeye gideceğine yönelik beklentilerle altın 6 ayın en yüksek düzeyini gördü.
Altının ons fiyatı ABD'den 15.30'da gelen verinin hemen ardından dakikalar içinde yüzde 1.5 yükselişle 1730 dolara kadar yükseldi.
ABD'den gelen zayıf veriler yatırımcıları güvenli liman olan altına yönlendiriyor.
Altının yıl başından bu yana değer kazancı yüzde 10'u aştı.
Uluslararası piyasalarda altının onsu yıl içerinde en düşük 1527,22 doları en yüksek ise 1790,79 doları gördü.
        """
        tokens = self.tokenizer.tokenize(text)

        assert_that('' not in tokens)                                   # no empty text
        assert_that(all([lambda x : all([c not in x for c in [u'\r', u'\n', u' ']]) for x in tokens]))     # no whitespace
        for a in tokens:
            print u'=={}=='.format(a)

if __name__ == '__main__':
    unittest.main()
