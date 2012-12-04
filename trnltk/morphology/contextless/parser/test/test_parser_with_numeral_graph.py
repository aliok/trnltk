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
from copy import copy
import logging
import os
import unittest
from trnltk.morphology.contextless.parser.test.parser_test import ParserTest
from trnltk.morphology.lexicon.lexiconloader import LexiconLoader
from trnltk.morphology.lexicon.rootgenerator import RootGenerator, RootMapGenerator
from trnltk.morphology.contextless.parser.parser import ContextlessMorphologicalParser, logger as parser_logger
from trnltk.morphology.contextless.parser.rootfinder import DigitNumeralRootFinder, TextNumeralRootFinder
from trnltk.morphology.contextless.parser.suffixapplier import logger as suffix_applier_logger
from trnltk.morphology.morphotactics.numeralsuffixgraph import NumeralSuffixGraph
from trnltk.morphology.morphotactics.predefinedpaths import PredefinedPaths
from trnltk.morphology.morphotactics.basicsuffixgraph import BasicSuffixGraph

class ParserTestWithNumeralGraph(ParserTest):

    @classmethod
    def setUpClass(cls):
        super(ParserTestWithNumeralGraph, cls).setUpClass()
        all_roots = []

        lexemes = LexiconLoader.load_from_file(os.path.join(os.path.dirname(__file__), '../../../../resources/master_dictionary.txt'))
        for di in lexemes:
            all_roots.extend(RootGenerator.generate(di))

        cls._org_root_map = (RootMapGenerator()).generate(all_roots)


    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        parser_logger.setLevel(logging.INFO)
        suffix_applier_logger.setLevel(logging.INFO)

        suffix_graph = NumeralSuffixGraph(BasicSuffixGraph())
        suffix_graph.initialize()

        self.cloned_root_map = copy(self._org_root_map)
        predefined_paths = PredefinedPaths(self.cloned_root_map, suffix_graph)
        predefined_paths.create_predefined_paths()

        text_numeral_root_finder = TextNumeralRootFinder(self.cloned_root_map)
        digit_numeral_root_finder = DigitNumeralRootFinder()

        self.parser = ContextlessMorphologicalParser(suffix_graph, predefined_paths, [text_numeral_root_finder, digit_numeral_root_finder])

    def test_should_parse_numerals_to_adjective_derivations(self):
        self.assert_parse_correct(u'onlarca',
            u'on(on)+Num+Card+Adj+NumbersOf(lArcA[larca])',
            u'on(on)+Num+Card+Adj+NumbersOf(lArcA[larca])+Noun+Zero+A3sg+Pnon+Nom',
            u'on(on)+Num+Card+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom+Adv+ManyOf(lArcA[larca])',
            u'on(on)+Num+Card+Adj+Zero+Noun+Zero+A3pl(lAr[lar])+Pnon+Nom+Adj+Equ(cA[ca])',
            u'on(on)+Num+Card+Adj+Zero+Noun+Zero+A3pl(lAr[lar])+Pnon+Nom+Adv+InTermsOf(cA[ca])',
            u'on(on)+Num+Card+Adj+Zero+Noun+Zero+A3pl(lAr[lar])+Pnon+Nom+Adv+By(cA[ca])',
            u'on(on)+Num+Card+Adj+Zero+Noun+Zero+A3pl(lAr[lar])+Pnon+Nom+Adj+Equ(cA[ca])+Noun+Zero+A3sg+Pnon+Nom')

        self.assert_parse_correct(u'binlerce',
            u'bin(bin)+Num+Card+Adj+NumbersOf(lArcA[lerce])',
            u'bin(bin)+Num+Card+Adj+NumbersOf(lArcA[lerce])+Noun+Zero+A3sg+Pnon+Nom',
            u'bin(bin)+Num+Card+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom+Adv+ManyOf(lArcA[lerce])',
            u'bin(bin)+Num+Card+Adj+Zero+Noun+Zero+A3pl(lAr[ler])+Pnon+Nom+Adj+Equ(cA[ce])',
            u'bin(bin)+Num+Card+Adj+Zero+Noun+Zero+A3pl(lAr[ler])+Pnon+Nom+Adv+InTermsOf(cA[ce])',
            u'bin(bin)+Num+Card+Adj+Zero+Noun+Zero+A3pl(lAr[ler])+Pnon+Nom+Adv+By(cA[ce])',
            u'bin(bin)+Num+Card+Adj+Zero+Noun+Zero+A3pl(lAr[ler])+Pnon+Nom+Adj+Equ(cA[ce])+Noun+Zero+A3sg+Pnon+Nom')

        self.assert_parse_exists(u'milyarlık',                  u'milyar(milyar)+Num+Card+Adj+OfUnit(lIk[lık])')
        self.assert_parse_exists(u'ellilik',                    u'elli(elli)+Num+Card+Adj+OfUnit(lIk[lik])')

    def test_should_parse_cardinal_numerals(self):
        self.assert_parse_correct(u'sıfır',                 u'sıfır(sıfır)+Num+Card+Adj+Zero', u'sıfır(sıfır)+Num+Card+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'bir',                   u'bir(bir)+Num+Card+Adj+Zero', u'bir(bir)+Num+Card+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'iki',                   u'iki(iki)+Num+Card+Adj+Zero', u'iki(iki)+Num+Card+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'üç',                    u'üç(üç)+Num+Card+Adj+Zero', u'üç(üç)+Num+Card+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'dört',                  u'dört(dört)+Num+Card+Adj+Zero', u'dört(dört)+Num+Card+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'beş',                   u'beş(beş)+Num+Card+Adj+Zero', u'beş(beş)+Num+Card+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'altı',                  u'altı(altı)+Num+Card+Adj+Zero', u'altı(altı)+Num+Card+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'yedi',                  u'yedi(yedi)+Num+Card+Adj+Zero', u'yedi(yedi)+Num+Card+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'sekiz',                 u'sekiz(sekiz)+Num+Card+Adj+Zero', u'sekiz(sekiz)+Num+Card+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'dokuz',                 u'dokuz(dokuz)+Num+Card+Adj+Zero', u'dokuz(dokuz)+Num+Card+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'on',                    u'on(on)+Num+Card+Adj+Zero', u'on(on)+Num+Card+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'yirmi',                 u'yirmi(yirmi)+Num+Card+Adj+Zero', u'yirmi(yirmi)+Num+Card+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'otuz',                  u'otuz(otuz)+Num+Card+Adj+Zero', u'otuz(otuz)+Num+Card+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'kırk',                  u'kırk(kırk)+Num+Card+Adj+Zero', u'kırk(kırk)+Num+Card+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'elli',                  u'elli(elli)+Num+Card+Adj+Zero', u'elli(elli)+Num+Card+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'altmış',                u'altmış(altmış)+Num+Card+Adj+Zero', u'altmış(altmış)+Num+Card+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'yetmiş',                u'yetmiş(yetmiş)+Num+Card+Adj+Zero', u'yetmiş(yetmiş)+Num+Card+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'seksen',                u'seksen(seksen)+Num+Card+Adj+Zero', u'seksen(seksen)+Num+Card+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'doksan',                u'doksan(doksan)+Num+Card+Adj+Zero', u'doksan(doksan)+Num+Card+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'yüz',                   u'yüz(yüz)+Num+Card+Adj+Zero', u'yüz(yüz)+Num+Card+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'bin',                   u'bin(bin)+Num+Card+Adj+Zero', u'bin(bin)+Num+Card+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'milyon',                u'milyon(milyon)+Num+Card+Adj+Zero', u'milyon(milyon)+Num+Card+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'milyar',                u'milyar(milyar)+Num+Card+Adj+Zero', u'milyar(milyar)+Num+Card+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'trilyon',               u'trilyon(trilyon)+Num+Card+Adj+Zero', u'trilyon(trilyon)+Num+Card+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'katrilyon',             u'katrilyon(katrilyon)+Num+Card+Adj+Zero', u'katrilyon(katrilyon)+Num+Card+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'kentilyon',             u'kentilyon(kentilyon)+Num+Card+Adj+Zero', u'kentilyon(kentilyon)+Num+Card+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')

    def test_should_parse_ordinal_numerals(self):
        self.assert_parse_correct(u'sıfırıncı',        u'sıfırıncı(sıfırıncı)+Num+Ord+Adj+Zero', u'sıfırıncı(sıfırıncı)+Num+Ord+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'birinci',          u'birinci(birinci)+Num+Ord+Adj+Zero', u'birinci(birinci)+Num+Ord+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'ikinci',           u'ikinci(ikinci)+Num+Ord+Adj+Zero', u'ikinci(ikinci)+Num+Ord+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'üçüncü',           u'üçüncü(üçüncü)+Num+Ord+Adj+Zero', u'üçüncü(üçüncü)+Num+Ord+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'dördüncü',         u'dördüncü(dördüncü)+Num+Ord+Adj+Zero', u'dördüncü(dördüncü)+Num+Ord+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'beşinci',          u'beşinci(beşinci)+Num+Ord+Adj+Zero', u'beşinci(beşinci)+Num+Ord+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'altıncı',          u'altıncı(altıncı)+Num+Ord+Adj+Zero', u'altıncı(altıncı)+Num+Ord+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'yedinci',          u'yedinci(yedinci)+Num+Ord+Adj+Zero', u'yedinci(yedinci)+Num+Ord+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'sekizinci',        u'sekizinci(sekizinci)+Num+Ord+Adj+Zero', u'sekizinci(sekizinci)+Num+Ord+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'dokuzuncu',        u'dokuzuncu(dokuzuncu)+Num+Ord+Adj+Zero', u'dokuzuncu(dokuzuncu)+Num+Ord+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'onuncu',           u'onuncu(onuncu)+Num+Ord+Adj+Zero', u'onuncu(onuncu)+Num+Ord+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'yirminci',         u'yirminci(yirminci)+Num+Ord+Adj+Zero', u'yirminci(yirminci)+Num+Ord+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'otuzuncu',         u'otuzuncu(otuzuncu)+Num+Ord+Adj+Zero', u'otuzuncu(otuzuncu)+Num+Ord+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'kırkıncı',         u'kırkıncı(kırkıncı)+Num+Ord+Adj+Zero', u'kırkıncı(kırkıncı)+Num+Ord+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'ellinci',          u'ellinci(ellinci)+Num+Ord+Adj+Zero', u'ellinci(ellinci)+Num+Ord+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'altmışıncı',       u'altmışıncı(altmışıncı)+Num+Ord+Adj+Zero', u'altmışıncı(altmışıncı)+Num+Ord+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'yetmişinci',       u'yetmişinci(yetmişinci)+Num+Ord+Adj+Zero', u'yetmişinci(yetmişinci)+Num+Ord+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'sekseninci',       u'sekseninci(sekseninci)+Num+Ord+Adj+Zero', u'sekseninci(sekseninci)+Num+Ord+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'doksanıncı',       u'doksanıncı(doksanıncı)+Num+Ord+Adj+Zero', u'doksanıncı(doksanıncı)+Num+Ord+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'yüzüncü',          u'yüzüncü(yüzüncü)+Num+Ord+Adj+Zero', u'yüzüncü(yüzüncü)+Num+Ord+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'bininci',          u'bininci(bininci)+Num+Ord+Adj+Zero', u'bininci(bininci)+Num+Ord+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'milyonuncu',       u'milyonuncu(milyonuncu)+Num+Ord+Adj+Zero', u'milyonuncu(milyonuncu)+Num+Ord+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'milyarıncı',       u'milyarıncı(milyarıncı)+Num+Ord+Adj+Zero', u'milyarıncı(milyarıncı)+Num+Ord+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'trilyonuncu',      u'trilyonuncu(trilyonuncu)+Num+Ord+Adj+Zero', u'trilyonuncu(trilyonuncu)+Num+Ord+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'katrilyonuncu',    u'katrilyonuncu(katrilyonuncu)+Num+Ord+Adj+Zero', u'katrilyonuncu(katrilyonuncu)+Num+Ord+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'kentilyonuncu',    u'kentilyonuncu(kentilyonuncu)+Num+Ord+Adj+Zero', u'kentilyonuncu(kentilyonuncu)+Num+Ord+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')

    def test_should_parse_digits(self):
        self.assert_parse_correct_for_verb(u'0',                     u'0(0)+Num+Digits+Adj+Zero', u'0(0)+Num+Digits+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct_for_verb(u'1',                     u'1(1)+Num+Digits+Adj+Zero', u'1(1)+Num+Digits+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct_for_verb(u'-1',                    u'-1(-1)+Num+Digits+Adj+Zero', u'-1(-1)+Num+Digits+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct_for_verb(u'9999999999',            u'9999999999(9999999999)+Num+Digits+Adj+Zero', u'9999999999(9999999999)+Num+Digits+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct_for_verb(u'-9999999999',           u'-9999999999(-9999999999)+Num+Digits+Adj+Zero', u'-9999999999(-9999999999)+Num+Digits+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')

        # In Turkish, comma is the fraction separator
        self.assert_parse_correct_for_verb(u'0,0',                   u'0,0(0,0)+Num+Digits+Adj+Zero', u'0,0(0,0)+Num+Digits+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct_for_verb(u'0,1',                   u'0,1(0,1)+Num+Digits+Adj+Zero', u'0,1(0,1)+Num+Digits+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct_for_verb(u'-0,0',                  u'-0,0(-0,0)+Num+Digits+Adj+Zero', u'-0,0(-0,0)+Num+Digits+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct_for_verb(u'-0,1',                  u'-0,1(-0,1)+Num+Digits+Adj+Zero', u'-0,1(-0,1)+Num+Digits+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct_for_verb(u'0,000000001',           u'0,000000001(0,000000001)+Num+Digits+Adj+Zero', u'0,000000001(0,000000001)+Num+Digits+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct_for_verb(u'-0,000000001',          u'-0,000000001(-0,000000001)+Num+Digits+Adj+Zero', u'-0,000000001(-0,000000001)+Num+Digits+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')

        # In Turkish, full stop is the grouping separator
        self.assert_parse_correct_for_verb(u'1.000',                 u'1.000(1.000)+Num+Digits+Adj+Zero', u'1.000(1.000)+Num+Digits+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct_for_verb(u'9.999.999.999.999',     u'9.999.999.999.999(9.999.999.999.999)+Num+Digits+Adj+Zero', u'9.999.999.999.999(9.999.999.999.999)+Num+Digits+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct_for_verb(u'-1.000',                u'-1.000(-1.000)+Num+Digits+Adj+Zero', u'-1.000(-1.000)+Num+Digits+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct_for_verb(u'-9.999.999.999.999',    u'-9.999.999.999.999(-9.999.999.999.999)+Num+Digits+Adj+Zero', u'-9.999.999.999.999(-9.999.999.999.999)+Num+Digits+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')

        self.assert_parse_correct_for_verb(u'1.000,0001212',         u'1.000,0001212(1.000,0001212)+Num+Digits+Adj+Zero', u'1.000,0001212(1.000,0001212)+Num+Digits+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct_for_verb(u'9.999.999.999.999,01',  u'9.999.999.999.999,01(9.999.999.999.999,01)+Num+Digits+Adj+Zero', u'9.999.999.999.999,01(9.999.999.999.999,01)+Num+Digits+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct_for_verb(u'-1.000,0001212',        u'-1.000,0001212(-1.000,0001212)+Num+Digits+Adj+Zero', u'-1.000,0001212(-1.000,0001212)+Num+Digits+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct_for_verb(u'-9.999.999.999.999,01', u'-9.999.999.999.999,01(-9.999.999.999.999,01)+Num+Digits+Adj+Zero', u'-9.999.999.999.999,01(-9.999.999.999.999,01)+Num+Digits+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')

    def test_should_parse_digits_with_suffixes(self):
        self.assert_parse_correct_for_verb(u'0\'ı',                 u'0(0)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[ı])', u'0(0)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[ı])+Nom')
        self.assert_parse_correct_for_verb(u'1\'i',                 u'1(1)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'1(1)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom')
        self.assert_parse_correct_for_verb(u'2\'si',                u'2(2)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[si])+Nom')
        self.assert_parse_correct_for_verb(u'3\'ü',                 u'3(3)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[ü])', u'3(3)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[ü])+Nom')
        self.assert_parse_correct_for_verb(u'4\'ü',                 u'4(4)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[ü])', u'4(4)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[ü])+Nom')
        self.assert_parse_correct_for_verb(u'5\'i',                 u'5(5)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'5(5)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom')
        self.assert_parse_correct_for_verb(u'6\'sı',                u'6(6)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[sı])+Nom')
        self.assert_parse_correct_for_verb(u'7\'si',                u'7(7)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[si])+Nom')
        self.assert_parse_correct_for_verb(u'8\'i',                 u'8(8)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'8(8)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom')
        self.assert_parse_correct_for_verb(u'9\'u',                 u'9(9)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'9(9)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom')

        # 10-99
        self.assert_parse_correct_for_verb(u'10\'u',                 u'10(10)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'10(10)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom')
        self.assert_parse_correct_for_verb(u'11\'i',                 u'11(11)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'11(11)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom')
        self.assert_parse_correct_for_verb(u'20\'si',                u'20(20)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[si])+Nom')
        self.assert_parse_correct_for_verb(u'30\'u',                 u'30(30)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'30(30)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom')
        self.assert_parse_correct_for_verb(u'40\'ı',                 u'40(40)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[ı])', u'40(40)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[ı])+Nom')
        self.assert_parse_correct_for_verb(u'50\'si',                u'50(50)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[si])+Nom')
        self.assert_parse_correct_for_verb(u'60\'ı',                 u'60(60)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[ı])', u'60(60)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[ı])+Nom')
        self.assert_parse_correct_for_verb(u'70\'i',                 u'70(70)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'70(70)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'          )
        self.assert_parse_correct_for_verb(u'80\'i',                 u'80(80)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'80(80)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'          )
        self.assert_parse_correct_for_verb(u'90\'ı',                 u'90(90)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[ı])', u'90(90)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[ı])+Nom')

        # 100-999
        self.assert_parse_correct_for_verb(u'100\'ü',                 u'100(100)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[ü])', u'100(100)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[ü])+Nom')
        self.assert_parse_correct_for_verb(u'110\'u',                 u'110(110)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'110(110)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'      )
        self.assert_parse_correct_for_verb(u'111\'i',                 u'111(111)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'111(111)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'      )
        self.assert_parse_correct_for_verb(u'200\'ü',                 u'200(200)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[ü])', u'200(200)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[ü])+Nom')

        # 1000-9999 (bin)
        self.assert_parse_correct_for_verb(u'1000\'i',                 u'1000(1000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'1000(1000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'      )
        self.assert_parse_correct_for_verb(u'1100\'ü',                 u'1100(1100)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[ü])', u'1100(1100)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[ü])+Nom')
        self.assert_parse_correct_for_verb(u'1110\'u',                 u'1110(1110)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'1110(1110)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'      )
        self.assert_parse_correct_for_verb(u'1111\'i',                 u'1111(1111)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'1111(1111)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'      )
        self.assert_parse_correct_for_verb(u'2000\'i',                 u'2000(2000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'2000(2000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'      )

        # 10000-99999 (on bin)
        self.assert_parse_correct_for_verb(u'10000\'i',                 u'10000(10000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'10000(10000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'      )
        self.assert_parse_correct_for_verb(u'11000\'i',                 u'11000(11000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'11000(11000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'      )
        self.assert_parse_correct_for_verb(u'11100\'ü',                 u'11100(11100)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[ü])', u'11100(11100)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[ü])+Nom')
        self.assert_parse_correct_for_verb(u'11110\'u',                 u'11110(11110)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'11110(11110)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'      )
        self.assert_parse_correct_for_verb(u'11111\'i',                 u'11111(11111)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'11111(11111)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'      )
        self.assert_parse_correct_for_verb(u'20000\'i',                 u'20000(20000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'20000(20000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'      )

        # 100000-999999 (yüz bin)
        self.assert_parse_correct_for_verb(u'100000\'i',                 u'100000(100000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'100000(100000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'      )
        self.assert_parse_correct_for_verb(u'110000\'i',                 u'110000(110000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'110000(110000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'      )
        self.assert_parse_correct_for_verb(u'111000\'i',                 u'111000(111000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'111000(111000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'      )
        self.assert_parse_correct_for_verb(u'111100\'ü',                 u'111100(111100)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[ü])', u'111100(111100)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[ü])+Nom')
        self.assert_parse_correct_for_verb(u'111110\'u',                 u'111110(111110)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'111110(111110)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'      )
        self.assert_parse_correct_for_verb(u'111111\'i',                 u'111111(111111)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'111111(111111)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'      )
        self.assert_parse_correct_for_verb(u'200000\'i',                 u'200000(200000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'200000(200000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'      )

        # 1000000-9999999 (milyon)
        self.assert_parse_correct_for_verb(u'1000000\'u',                 u'1000000(1000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'1000000(1000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'      )
        self.assert_parse_correct_for_verb(u'1100000\'i',                 u'1100000(1100000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'1100000(1100000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'      )
        self.assert_parse_correct_for_verb(u'1110000\'i',                 u'1110000(1110000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'1110000(1110000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'      )
        self.assert_parse_correct_for_verb(u'1111000\'i',                 u'1111000(1111000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'1111000(1111000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'      )
        self.assert_parse_correct_for_verb(u'1111100\'ü',                 u'1111100(1111100)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[ü])', u'1111100(1111100)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[ü])+Nom')
        self.assert_parse_correct_for_verb(u'1111110\'u',                 u'1111110(1111110)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'1111110(1111110)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'      )
        self.assert_parse_correct_for_verb(u'1111111\'i',                 u'1111111(1111111)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'1111111(1111111)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'      )
        self.assert_parse_correct_for_verb(u'2000000\'u',                 u'2000000(2000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'2000000(2000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'      )

        # 10000000-99999999 (on milyon)
        self.assert_parse_correct_for_verb(u'10000000\'u',                 u'10000000(10000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'10000000(10000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'      )
        self.assert_parse_correct_for_verb(u'11000000\'u',                 u'11000000(11000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'11000000(11000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'      )
        self.assert_parse_correct_for_verb(u'11100000\'i',                 u'11100000(11100000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'11100000(11100000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'      )
        self.assert_parse_correct_for_verb(u'11110000\'i',                 u'11110000(11110000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'11110000(11110000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'      )
        self.assert_parse_correct_for_verb(u'11111000\'i',                 u'11111000(11111000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'11111000(11111000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'      )
        self.assert_parse_correct_for_verb(u'11111100\'ü',                 u'11111100(11111100)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[ü])', u'11111100(11111100)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[ü])+Nom')
        self.assert_parse_correct_for_verb(u'11111110\'u',                 u'11111110(11111110)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'11111110(11111110)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'      )
        self.assert_parse_correct_for_verb(u'11111111\'i',                 u'11111111(11111111)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'11111111(11111111)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'      )
        self.assert_parse_correct_for_verb(u'20000000\'u',                 u'20000000(20000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'20000000(20000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'      )

        # 100000000-999999999 (yüz milyon)
        self.assert_parse_correct_for_verb(u'100000000\'u',                u'100000000(100000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'100000000(100000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'      )
        self.assert_parse_correct_for_verb(u'110000000\'u',                u'110000000(110000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'110000000(110000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'      )
        self.assert_parse_correct_for_verb(u'111000000\'u',                u'111000000(111000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'111000000(111000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'      )
        self.assert_parse_correct_for_verb(u'111100000\'i',                u'111100000(111100000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'111100000(111100000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'      )
        self.assert_parse_correct_for_verb(u'111110000\'i',                u'111110000(111110000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'111110000(111110000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'      )
        self.assert_parse_correct_for_verb(u'111111000\'i',                u'111111000(111111000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'111111000(111111000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'      )
        self.assert_parse_correct_for_verb(u'111111100\'ü',                u'111111100(111111100)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[ü])', u'111111100(111111100)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[ü])+Nom')
        self.assert_parse_correct_for_verb(u'111111110\'u',                u'111111110(111111110)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'111111110(111111110)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'      )
        self.assert_parse_correct_for_verb(u'111111111\'i',                u'111111111(111111111)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'111111111(111111111)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'      )
        self.assert_parse_correct_for_verb(u'200000000\'u',                u'200000000(200000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'200000000(200000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'      )

        # 1000000000-9999999999 (milyar)
        self.assert_parse_correct_for_verb(u'1000000000\'ı',               u'1000000000(1000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[ı])', u'1000000000(1000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[ı])+Nom')
        self.assert_parse_correct_for_verb(u'1100000000\'u',               u'1100000000(1100000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'1100000000(1100000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )
        self.assert_parse_correct_for_verb(u'1110000000\'u',               u'1110000000(1110000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'1110000000(1110000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )
        self.assert_parse_correct_for_verb(u'1111000000\'u',               u'1111000000(1111000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'1111000000(1111000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )
        self.assert_parse_correct_for_verb(u'1111100000\'i',               u'1111100000(1111100000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'1111100000(1111100000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'          )
        self.assert_parse_correct_for_verb(u'1111110000\'i',               u'1111110000(1111110000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'1111110000(1111110000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'          )
        self.assert_parse_correct_for_verb(u'1111111000\'i',               u'1111111000(1111111000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'1111111000(1111111000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'          )
        self.assert_parse_correct_for_verb(u'1111111100\'ü',               u'1111111100(1111111100)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[ü])', u'1111111100(1111111100)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[ü])+Nom'    )
        self.assert_parse_correct_for_verb(u'1111111110\'u',               u'1111111110(1111111110)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'1111111110(1111111110)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )
        self.assert_parse_correct_for_verb(u'1111111111\'i',               u'1111111111(1111111111)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'1111111111(1111111111)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'          )
        self.assert_parse_correct_for_verb(u'2000000000\'ı',               u'2000000000(2000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[ı])', u'2000000000(2000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[ı])+Nom')

        # 10000000000-99999999999 (on milyar)
        self.assert_parse_correct_for_verb(u'10000000000\'ı',               u'10000000000(10000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[ı])', u'10000000000(10000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[ı])+Nom')
        self.assert_parse_correct_for_verb(u'11000000000\'ı',               u'11000000000(11000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[ı])', u'11000000000(11000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[ı])+Nom')
        self.assert_parse_correct_for_verb(u'11100000000\'u',               u'11100000000(11100000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'11100000000(11100000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )
        self.assert_parse_correct_for_verb(u'11110000000\'u',               u'11110000000(11110000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'11110000000(11110000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )
        self.assert_parse_correct_for_verb(u'11111000000\'u',               u'11111000000(11111000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'11111000000(11111000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )
        self.assert_parse_correct_for_verb(u'11111100000\'i',               u'11111100000(11111100000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'11111100000(11111100000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'          )
        self.assert_parse_correct_for_verb(u'11111110000\'i',               u'11111110000(11111110000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'11111110000(11111110000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'          )
        self.assert_parse_correct_for_verb(u'11111111000\'i',               u'11111111000(11111111000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'11111111000(11111111000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'          )
        self.assert_parse_correct_for_verb(u'11111111100\'ü',               u'11111111100(11111111100)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[ü])', u'11111111100(11111111100)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[ü])+Nom'    )
        self.assert_parse_correct_for_verb(u'11111111110\'u',               u'11111111110(11111111110)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'11111111110(11111111110)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )
        self.assert_parse_correct_for_verb(u'11111111111\'i',               u'11111111111(11111111111)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'11111111111(11111111111)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'          )
        self.assert_parse_correct_for_verb(u'20000000000\'ı',               u'20000000000(20000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[ı])', u'20000000000(20000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[ı])+Nom')

        # 10000000000-99999999999 (yüz milyar)
        self.assert_parse_correct_for_verb(u'100000000000\'ı',               u'100000000000(100000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[ı])', u'100000000000(100000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[ı])+Nom')
        self.assert_parse_correct_for_verb(u'110000000000\'ı',               u'110000000000(110000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[ı])', u'110000000000(110000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[ı])+Nom')
        self.assert_parse_correct_for_verb(u'111000000000\'ı',               u'111000000000(111000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[ı])', u'111000000000(111000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[ı])+Nom')
        self.assert_parse_correct_for_verb(u'111100000000\'u',               u'111100000000(111100000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'111100000000(111100000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )
        self.assert_parse_correct_for_verb(u'111110000000\'u',               u'111110000000(111110000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'111110000000(111110000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )
        self.assert_parse_correct_for_verb(u'111111000000\'u',               u'111111000000(111111000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'111111000000(111111000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )
        self.assert_parse_correct_for_verb(u'111111100000\'i',               u'111111100000(111111100000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'111111100000(111111100000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'          )
        self.assert_parse_correct_for_verb(u'111111110000\'i',               u'111111110000(111111110000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'111111110000(111111110000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'          )
        self.assert_parse_correct_for_verb(u'111111111000\'i',               u'111111111000(111111111000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'111111111000(111111111000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'          )
        self.assert_parse_correct_for_verb(u'111111111100\'ü',               u'111111111100(111111111100)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[ü])', u'111111111100(111111111100)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[ü])+Nom'    )
        self.assert_parse_correct_for_verb(u'111111111110\'u',               u'111111111110(111111111110)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'111111111110(111111111110)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )
        self.assert_parse_correct_for_verb(u'111111111111\'i',               u'111111111111(111111111111)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'111111111111(111111111111)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'          )
        self.assert_parse_correct_for_verb(u'200000000000\'ı',               u'200000000000(200000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[ı])', u'200000000000(200000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[ı])+Nom')

        # 100000000000-999999999999 (trilyon)
        self.assert_parse_correct_for_verb(u'1000000000000\'u',               u'1000000000000(1000000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'1000000000000(1000000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'            )
        self.assert_parse_correct_for_verb(u'1100000000000\'ı',               u'1100000000000(1100000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[ı])', u'1100000000000(1100000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[ı])+Nom'  )
        self.assert_parse_correct_for_verb(u'1110000000000\'ı',               u'1110000000000(1110000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[ı])', u'1110000000000(1110000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[ı])+Nom'  )
        self.assert_parse_correct_for_verb(u'1111000000000\'ı',               u'1111000000000(1111000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[ı])', u'1111000000000(1111000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[ı])+Nom'  )
        self.assert_parse_correct_for_verb(u'1111100000000\'u',               u'1111100000000(1111100000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'1111100000000(1111100000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'            )
        self.assert_parse_correct_for_verb(u'1111110000000\'u',               u'1111110000000(1111110000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'1111110000000(1111110000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'            )
        self.assert_parse_correct_for_verb(u'1111111000000\'u',               u'1111111000000(1111111000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'1111111000000(1111111000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'            )
        self.assert_parse_correct_for_verb(u'1111111100000\'i',               u'1111111100000(1111111100000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'1111111100000(1111111100000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'            )
        self.assert_parse_correct_for_verb(u'1111111110000\'i',               u'1111111110000(1111111110000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'1111111110000(1111111110000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'            )
        self.assert_parse_correct_for_verb(u'1111111111000\'i',               u'1111111111000(1111111111000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'1111111111000(1111111111000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'            )
        self.assert_parse_correct_for_verb(u'1111111111100\'ü',               u'1111111111100(1111111111100)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[ü])', u'1111111111100(1111111111100)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[ü])+Nom'      )
        self.assert_parse_correct_for_verb(u'1111111111110\'u',               u'1111111111110(1111111111110)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'1111111111110(1111111111110)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'            )
        self.assert_parse_correct_for_verb(u'1111111111111\'i',               u'1111111111111(1111111111111)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'1111111111111(1111111111111)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'            )
        self.assert_parse_correct_for_verb(u'2000000000000\'u',               u'2000000000000(2000000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'2000000000000(2000000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'            )

        # 1000000000000-9999999999999 (on trilyon)
        self.assert_parse_correct_for_verb(u'10000000000000\'u',               u'10000000000000(10000000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'10000000000000(10000000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )
        self.assert_parse_correct_for_verb(u'11000000000000\'u',               u'11000000000000(11000000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'11000000000000(11000000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )
        self.assert_parse_correct_for_verb(u'11100000000000\'ı',               u'11100000000000(11100000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[ı])', u'11100000000000(11100000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[ı])+Nom')
        self.assert_parse_correct_for_verb(u'11110000000000\'ı',               u'11110000000000(11110000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[ı])', u'11110000000000(11110000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[ı])+Nom')
        self.assert_parse_correct_for_verb(u'11111000000000\'ı',               u'11111000000000(11111000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[ı])', u'11111000000000(11111000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[ı])+Nom')
        self.assert_parse_correct_for_verb(u'11111100000000\'u',               u'11111100000000(11111100000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'11111100000000(11111100000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )
        self.assert_parse_correct_for_verb(u'11111110000000\'u',               u'11111110000000(11111110000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'11111110000000(11111110000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )
        self.assert_parse_correct_for_verb(u'11111111000000\'u',               u'11111111000000(11111111000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'11111111000000(11111111000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )
        self.assert_parse_correct_for_verb(u'11111111100000\'i',               u'11111111100000(11111111100000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'11111111100000(11111111100000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'          )
        self.assert_parse_correct_for_verb(u'11111111110000\'i',               u'11111111110000(11111111110000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'11111111110000(11111111110000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'          )
        self.assert_parse_correct_for_verb(u'11111111111000\'i',               u'11111111111000(11111111111000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'11111111111000(11111111111000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'          )
        self.assert_parse_correct_for_verb(u'11111111111100\'ü',               u'11111111111100(11111111111100)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[ü])', u'11111111111100(11111111111100)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[ü])+Nom'    )
        self.assert_parse_correct_for_verb(u'11111111111110\'u',               u'11111111111110(11111111111110)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'11111111111110(11111111111110)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )
        self.assert_parse_correct_for_verb(u'11111111111111\'i',               u'11111111111111(11111111111111)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'11111111111111(11111111111111)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'          )
        self.assert_parse_correct_for_verb(u'20000000000000\'u',               u'20000000000000(20000000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'20000000000000(20000000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )

        # 10000000000000-99999999999999 (yüz trilyon)
        self.assert_parse_correct_for_verb(u'100000000000000\'u',               u'100000000000000(100000000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'100000000000000(100000000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )
        self.assert_parse_correct_for_verb(u'110000000000000\'u',               u'110000000000000(110000000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'110000000000000(110000000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )
        self.assert_parse_correct_for_verb(u'111000000000000\'u',               u'111000000000000(111000000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'111000000000000(111000000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )
        self.assert_parse_correct_for_verb(u'111100000000000\'ı',               u'111100000000000(111100000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[ı])', u'111100000000000(111100000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[ı])+Nom')
        self.assert_parse_correct_for_verb(u'111110000000000\'ı',               u'111110000000000(111110000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[ı])', u'111110000000000(111110000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[ı])+Nom')
        self.assert_parse_correct_for_verb(u'111111000000000\'ı',               u'111111000000000(111111000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[ı])', u'111111000000000(111111000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[ı])+Nom')
        self.assert_parse_correct_for_verb(u'111111100000000\'u',               u'111111100000000(111111100000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'111111100000000(111111100000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )
        self.assert_parse_correct_for_verb(u'111111110000000\'u',               u'111111110000000(111111110000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'111111110000000(111111110000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )
        self.assert_parse_correct_for_verb(u'111111111000000\'u',               u'111111111000000(111111111000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'111111111000000(111111111000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )
        self.assert_parse_correct_for_verb(u'111111111100000\'i',               u'111111111100000(111111111100000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'111111111100000(111111111100000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'          )
        self.assert_parse_correct_for_verb(u'111111111110000\'i',               u'111111111110000(111111111110000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'111111111110000(111111111110000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'          )
        self.assert_parse_correct_for_verb(u'111111111111000\'i',               u'111111111111000(111111111111000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'111111111111000(111111111111000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'          )
        self.assert_parse_correct_for_verb(u'111111111111100\'ü',               u'111111111111100(111111111111100)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[ü])', u'111111111111100(111111111111100)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[ü])+Nom'    )
        self.assert_parse_correct_for_verb(u'111111111111110\'u',               u'111111111111110(111111111111110)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'111111111111110(111111111111110)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )
        self.assert_parse_correct_for_verb(u'111111111111111\'i',               u'111111111111111(111111111111111)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'111111111111111(111111111111111)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'          )
        self.assert_parse_correct_for_verb(u'200000000000000\'u',               u'200000000000000(200000000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'200000000000000(200000000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )

        # 100000000000000-999999999999999 (katrilyon)
        self.assert_parse_correct_for_verb(u'1000000000000000\'u',               u'1000000000000000(1000000000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'1000000000000000(1000000000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )
        self.assert_parse_correct_for_verb(u'1100000000000000\'u',               u'1100000000000000(1100000000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'1100000000000000(1100000000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )
        self.assert_parse_correct_for_verb(u'1110000000000000\'u',               u'1110000000000000(1110000000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'1110000000000000(1110000000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )
        self.assert_parse_correct_for_verb(u'1111000000000000\'u',               u'1111000000000000(1111000000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'1111000000000000(1111000000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )
        self.assert_parse_correct_for_verb(u'1111100000000000\'ı',               u'1111100000000000(1111100000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[ı])', u'1111100000000000(1111100000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[ı])+Nom')
        self.assert_parse_correct_for_verb(u'1111110000000000\'ı',               u'1111110000000000(1111110000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[ı])', u'1111110000000000(1111110000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[ı])+Nom')
        self.assert_parse_correct_for_verb(u'1111111000000000\'ı',               u'1111111000000000(1111111000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[ı])', u'1111111000000000(1111111000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[ı])+Nom')
        self.assert_parse_correct_for_verb(u'1111111100000000\'u',               u'1111111100000000(1111111100000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'1111111100000000(1111111100000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )
        self.assert_parse_correct_for_verb(u'1111111110000000\'u',               u'1111111110000000(1111111110000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'1111111110000000(1111111110000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )
        self.assert_parse_correct_for_verb(u'1111111111000000\'u',               u'1111111111000000(1111111111000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'1111111111000000(1111111111000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )
        self.assert_parse_correct_for_verb(u'1111111111100000\'i',               u'1111111111100000(1111111111100000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'1111111111100000(1111111111100000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'          )
        self.assert_parse_correct_for_verb(u'1111111111110000\'i',               u'1111111111110000(1111111111110000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'1111111111110000(1111111111110000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'          )
        self.assert_parse_correct_for_verb(u'1111111111111000\'i',               u'1111111111111000(1111111111111000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'1111111111111000(1111111111111000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'          )
        self.assert_parse_correct_for_verb(u'1111111111111100\'ü',               u'1111111111111100(1111111111111100)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[ü])', u'1111111111111100(1111111111111100)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[ü])+Nom'    )
        self.assert_parse_correct_for_verb(u'1111111111111110\'u',               u'1111111111111110(1111111111111110)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'1111111111111110(1111111111111110)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )
        self.assert_parse_correct_for_verb(u'1111111111111111\'i',               u'1111111111111111(1111111111111111)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'1111111111111111(1111111111111111)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'          )
        self.assert_parse_correct_for_verb(u'2000000000000000\'u',               u'2000000000000000(2000000000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'2000000000000000(2000000000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )

        # 1000000000000000-9999999999999999 (on katrilyon)
        self.assert_parse_correct_for_verb(u'10000000000000000\'u',               u'10000000000000000(10000000000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'10000000000000000(10000000000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )
        self.assert_parse_correct_for_verb(u'11000000000000000\'u',               u'11000000000000000(11000000000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'11000000000000000(11000000000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )
        self.assert_parse_correct_for_verb(u'11100000000000000\'u',               u'11100000000000000(11100000000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'11100000000000000(11100000000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )
        self.assert_parse_correct_for_verb(u'11110000000000000\'u',               u'11110000000000000(11110000000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'11110000000000000(11110000000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )
        self.assert_parse_correct_for_verb(u'11111000000000000\'u',               u'11111000000000000(11111000000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'11111000000000000(11111000000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )
        self.assert_parse_correct_for_verb(u'11111100000000000\'ı',               u'11111100000000000(11111100000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[ı])', u'11111100000000000(11111100000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[ı])+Nom')
        self.assert_parse_correct_for_verb(u'11111110000000000\'ı',               u'11111110000000000(11111110000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[ı])', u'11111110000000000(11111110000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[ı])+Nom')
        self.assert_parse_correct_for_verb(u'11111111000000000\'ı',               u'11111111000000000(11111111000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[ı])', u'11111111000000000(11111111000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[ı])+Nom')
        self.assert_parse_correct_for_verb(u'11111111100000000\'u',               u'11111111100000000(11111111100000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'11111111100000000(11111111100000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )
        self.assert_parse_correct_for_verb(u'11111111110000000\'u',               u'11111111110000000(11111111110000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'11111111110000000(11111111110000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )
        self.assert_parse_correct_for_verb(u'11111111111000000\'u',               u'11111111111000000(11111111111000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'11111111111000000(11111111111000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )
        self.assert_parse_correct_for_verb(u'11111111111100000\'i',               u'11111111111100000(11111111111100000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'11111111111100000(11111111111100000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'          )
        self.assert_parse_correct_for_verb(u'11111111111110000\'i',               u'11111111111110000(11111111111110000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'11111111111110000(11111111111110000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'          )
        self.assert_parse_correct_for_verb(u'11111111111111000\'i',               u'11111111111111000(11111111111111000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'11111111111111000(11111111111111000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'          )
        self.assert_parse_correct_for_verb(u'11111111111111100\'ü',               u'11111111111111100(11111111111111100)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[ü])', u'11111111111111100(11111111111111100)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[ü])+Nom'    )
        self.assert_parse_correct_for_verb(u'11111111111111110\'u',               u'11111111111111110(11111111111111110)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'11111111111111110(11111111111111110)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )
        self.assert_parse_correct_for_verb(u'11111111111111111\'i',               u'11111111111111111(11111111111111111)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'11111111111111111(11111111111111111)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'          )
        self.assert_parse_correct_for_verb(u'20000000000000000\'u',               u'20000000000000000(20000000000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'20000000000000000(20000000000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )

        # 10000000000000000-99999999999999999 (yüz katrilyon)
        self.assert_parse_correct_for_verb(u'100000000000000000\'u',              u'100000000000000000(100000000000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'100000000000000000(100000000000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )
        self.assert_parse_correct_for_verb(u'110000000000000000\'u',              u'110000000000000000(110000000000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'110000000000000000(110000000000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )
        self.assert_parse_correct_for_verb(u'111000000000000000\'u',              u'111000000000000000(111000000000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'111000000000000000(111000000000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )
        self.assert_parse_correct_for_verb(u'111100000000000000\'u',              u'111100000000000000(111100000000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'111100000000000000(111100000000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )
        self.assert_parse_correct_for_verb(u'111110000000000000\'u',              u'111110000000000000(111110000000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'111110000000000000(111110000000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )
        self.assert_parse_correct_for_verb(u'111111000000000000\'u',              u'111111000000000000(111111000000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'111111000000000000(111111000000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )
        self.assert_parse_correct_for_verb(u'111111100000000000\'ı',              u'111111100000000000(111111100000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[ı])', u'111111100000000000(111111100000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[ı])+Nom')
        self.assert_parse_correct_for_verb(u'111111110000000000\'ı',              u'111111110000000000(111111110000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[ı])', u'111111110000000000(111111110000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[ı])+Nom')
        self.assert_parse_correct_for_verb(u'111111111000000000\'ı',              u'111111111000000000(111111111000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[ı])', u'111111111000000000(111111111000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[ı])+Nom')
        self.assert_parse_correct_for_verb(u'111111111100000000\'u',              u'111111111100000000(111111111100000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'111111111100000000(111111111100000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )
        self.assert_parse_correct_for_verb(u'111111111110000000\'u',              u'111111111110000000(111111111110000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'111111111110000000(111111111110000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )
        self.assert_parse_correct_for_verb(u'111111111111000000\'u',              u'111111111111000000(111111111111000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'111111111111000000(111111111111000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )
        self.assert_parse_correct_for_verb(u'111111111111100000\'i',              u'111111111111100000(111111111111100000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'111111111111100000(111111111111100000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'          )
        self.assert_parse_correct_for_verb(u'111111111111110000\'i',              u'111111111111110000(111111111111110000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'111111111111110000(111111111111110000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'          )
        self.assert_parse_correct_for_verb(u'111111111111111000\'i',              u'111111111111111000(111111111111111000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'111111111111111000(111111111111111000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'          )
        self.assert_parse_correct_for_verb(u'111111111111111100\'ü',              u'111111111111111100(111111111111111100)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[ü])', u'111111111111111100(111111111111111100)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[ü])+Nom'    )
        self.assert_parse_correct_for_verb(u'111111111111111110\'u',              u'111111111111111110(111111111111111110)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'111111111111111110(111111111111111110)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )
        self.assert_parse_correct_for_verb(u'111111111111111111\'i',              u'111111111111111111(111111111111111111)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[i])', u'111111111111111111(111111111111111111)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[i])+Nom'          )
        self.assert_parse_correct_for_verb(u'200000000000000000\'u',              u'200000000000000000(200000000000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+Pnon+Acc(+yI[u])', u'200000000000000000(200000000000000000)+Num+Digits+Apos+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[u])+Nom'          )

if __name__ == '__main__':
    unittest.main()
