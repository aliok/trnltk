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
import logging
import unittest
from trnltk.morphology.contextless.parser.test.parser_test import ParserTest
from trnltk.morphology.morphotactics.basicsuffixgraph import BasicSuffixGraph
from trnltk.morphology.contextless.parser.parser import ContextlessMorphologicalParser, logger as parser_logger
from trnltk.morphology.contextless.parser.rootfinder import  ProperNounFromApostropheRootFinder, ProperNounWithoutApostropheRootFinder
from trnltk.morphology.contextless.parser.suffixapplier import logger as suffix_applier_logger
from trnltk.morphology.morphotactics.propernounsuffixgraph import ProperNounSuffixGraph

class ParserTestWithProperNouns(ParserTest):

    @classmethod
    def setUpClass(cls):
        super(ParserTestWithProperNouns, cls).setUpClass()
        cls.root_map = dict()

        suffix_graph = ProperNounSuffixGraph(BasicSuffixGraph())
        suffix_graph.initialize()

        proper_noun_from_apostrophe_root_finder = ProperNounFromApostropheRootFinder()
        proper_noun_without_apostrophe_root_finder = ProperNounWithoutApostropheRootFinder()

        cls.parser = ContextlessMorphologicalParser(suffix_graph, None,
            [proper_noun_from_apostrophe_root_finder, proper_noun_without_apostrophe_root_finder])

    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        parser_logger.setLevel(logging.INFO)
        suffix_applier_logger.setLevel(logging.INFO)

    def test_should_parse_proper_nouns(self):
        self.assert_parse_correct(u"Ali",            u"Ali(Ali)+Noun+Prop+A3sg+Pnon+Nom")
        self.assert_parse_correct(u"Ahmet",          u"Ahmet(Ahmet)+Noun+Prop+A3sg+Pnon+Nom")
        self.assert_parse_correct(u"Ali'ye",         u"Ali(Ali)+Noun+Prop+Apos+A3sg+Pnon+Dat(+yA[ye])")

    def test_should_parse_abbreviations(self):
        self.assert_parse_correct(u"AB",            u"AB(AB)+Noun+Abbr+A3sg+Pnon+Nom")
        self.assert_parse_correct(u"AB'ye",         u"AB(AB)+Noun+Abbr+Apos+A3sg+Pnon+Dat(+yA[ye])")
        self.assert_parse_correct(u"ABD",           u"ABD(ABD)+Noun+Abbr+A3sg+Pnon+Nom")

    def test_should_parse_proper_nouns_TDK(self):
        parser_logger.setLevel(logging.DEBUG)
        suffix_applier_logger.setLevel(logging.DEBUG)

        # TODO: implementing these features is almost impossible without context and historical data

        # tests based on TDK
        # http://www.tdk.gov.tr/index.php?option=com_content&view=article&id=187:Noktalama-Isaretleri-Aciklamalar&catid=50:yazm-kurallar&Itemid=132

        # Özel adlara getirilen iyelik, durum ve bildirme ekleri kesme işaretiyle ayrılır
        self.assert_parse_correct(u"Kayseri'm",          u'Kayseri(Kayseri)+Noun+Prop+Apos+A3sg+P1sg(+Im[m])+Nom')
        self.assert_parse_correct(u"Türkiye'mizin",      u'Türkiye(Türkiye)+Noun+Prop+Apos+A3sg+P1sg(+ImIz[miz])+Gen(+nIn[nin])')
        self.assert_parse_correct(u"Muhibbi'nin",        u'Muhibbi(Muhibbi)+Noun+Prop+Apos+A3sg+Pnon+Gen(+nIn[in])')
        self.assert_parse_correct(u"Emre'yi")
        self.assert_parse_correct(u"Şinasi'yle")
        self.assert_parse_correct(u"Alman'sınız")
        self.assert_parse_correct(u"Kırgız'ım")
        self.assert_parse_correct(u"Karakeçili'nin")
        self.assert_parse_correct(u"Cebrail'den")
        self.assert_parse_correct(u"Samanyolu'nda")
        self.assert_parse_correct(u"Eminönü'nde")
        self.assert_parse_correct(u"Ahmet'miş")
        self.assert_parse_correct(u"Ahmet'ti")

        # Sonunda 3. teklik kişi iyelik eki olan özel ada, bu ek dışında başka bir iyelik eki getirildiğinde kesme işareti konmaz
        self.assert_parse_correct(u"Boğaz_Köprümüz")
        self.assert_parse_correct(u"Boğaz_Köprümüzün")
        self.assert_parse_correct(u"Kuşadamızda")

        # Kurum, kuruluş, kurul, birleşim, oturum ve iş yeri adlarına gelen ekler kesmeyle ayrılmaz:
        self.assert_parse_correct(u"Türk_Dil_Kurumundan")
        self.assert_parse_correct(u"Başbakanlığa")

        # Özel adlara getirilen yapım ekleri, çokluk eki ve bunlardan sonra gelen diğer ekler kesmeyle ayrılmaz
        self.assert_parse_correct(u"Türklük")
        self.assert_parse_correct(u"Türkleşmek")
        self.assert_parse_correct(u"Türkçü")
        self.assert_parse_correct(u"Türkçülük")
        self.assert_parse_correct(u"Türkçe")
        self.assert_parse_correct(u"Avrupalı")
        self.assert_parse_correct(u"Avrupalılaşmak")
        self.assert_parse_correct(u"Mehmetler")
        self.assert_parse_correct(u"Mehmetlere")
        self.assert_parse_correct(u"Mehmetgil")
        self.assert_parse_correct(u"Mehmetgile")
        self.assert_parse_correct(u"Türklerin")
        self.assert_parse_correct(u"Türkçenin")
        self.assert_parse_correct(u"Müslümanlıkta")

        # Kişi adlarından sonra gelen saygı ve unvan sözlerine getirilen ekleri ayırmak için konur:
        self.assert_parse_correct(u"Nihat_Bey'e")
        self.assert_parse_correct(u"Ayşe_Hanım'dan")
        self.assert_parse_correct(u"Enver_Paşa'ya")


if __name__ == '__main__':
    unittest.main()
