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
from trnltk.morphology.contextless.parser.bruteforcenounrootfinders import BruteForceNounRootFinder, BruteForceCompoundNounRootFinder
from trnltk.morphology.contextless.parser.test.parser_test import ParserTest
from trnltk.morphology.contextless.parser.parser import ContextlessMorphologicalParser, logger as parser_logger
from trnltk.morphology.contextless.parser.suffixapplier import logger as suffix_applier_logger
from trnltk.morphology.morphotactics.basicsuffixgraph import BasicSuffixGraph

class ParserTestWithBruteForceNounRootFinder(ParserTest):

    @classmethod
    def setUpClass(cls):
        super(ParserTestWithBruteForceNounRootFinder, cls).setUpClass()


    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        parser_logger.setLevel(logging.INFO)
        suffix_applier_logger.setLevel(logging.INFO)

        suffix_graph = BasicSuffixGraph()
        suffix_graph.initialize()

        self.mock_brute_force_noun_root_finder = BruteForceNounRootFinder()

        self.parser = ContextlessMorphologicalParser(suffix_graph, None, [self.mock_brute_force_noun_root_finder])

    def test_should_find_one_result_for_words_not_acceptable_by_suffix_graph(self):
        self.assert_parse_correct(u'asdasmo',      u'asdasmo(asdasmo)+Noun+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'asdassü',      u'asdassü(asdassü)+Noun+A3sg+Pnon+Nom')

    def test_should_parse_simple_nouns(self):
        self.assert_parse_correct(u'o',            u'o(o)+Noun+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'om',           u'om(om)+Noun+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'b',            u'b(b)+Noun+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'be',           u'be(be)+Noun+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'bem',          u'be(be)+Noun+A3sg+P1sg(+Im[m])+Nom', u'bem(bem)+Noun+A3sg+Pnon+Nom')

    def test_should_parse_with_possible_voicing(self):
        self.assert_parse_correct(u'oda',          u'od(od)+Noun+A3sg+Pnon+Dat(+yA[a])', u'od(ot)+Noun+A3sg+Pnon+Dat(+yA[a])', u'oda(oda)+Noun+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'kağa',         u'kağ(kağ)+Noun+A3sg+Pnon+Dat(+yA[a])', u'kağ(kag)+Noun+A3sg+Pnon+Dat(+yA[a])', u'kağ(kak)+Noun+A3sg+Pnon+Dat(+yA[a])', u'kağa(kağa)+Noun+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'zogu',         u'zog(zog)+Noun+A3sg+Pnon+Acc(+yI[u])', u'zog(zog)+Noun+A3sg+P3sg(+sI[u])+Nom', u'zogu(zogu)+Noun+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'ıba',          u'ıb(ıb)+Noun+A3sg+Pnon+Dat(+yA[a])', u'ıb(ıp)+Noun+A3sg+Pnon+Dat(+yA[a])', u'ıba(ıba)+Noun+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'acı',          u'ac(ac)+Noun+A3sg+Pnon+Acc(+yI[ı])', u'ac(ac)+Noun+A3sg+P3sg(+sI[ı])+Nom', u'ac(aç)+Noun+A3sg+Pnon+Acc(+yI[ı])', u'ac(aç)+Noun+A3sg+P3sg(+sI[ı])+Nom', u'acı(acı)+Noun+A3sg+Pnon+Nom')
        # skip nK -> nG voicing as in cenk->cengi
        self.assert_parse_correct(u'cengi',        u'ceng(ceng)+Noun+A3sg+Pnon+Acc(+yI[i])', u'ceng(ceng)+Noun+A3sg+P3sg(+sI[i])+Nom', u'cengi(cengi)+Noun+A3sg+Pnon+Nom')

    def test_should_parse_with_explicit_no_voicing(self):
        self.assert_parse_correct(u'ota',          u'ot(ot)+Noun+A3sg+Pnon+Dat(+yA[a])', u'ota(ota)+Noun+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'kaka',         u'kak(kak)+Noun+A3sg+Pnon+Dat(+yA[a])', u'kaka(kaka)+Noun+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'zoku',         u'zok(zok)+Noun+A3sg+Pnon+Acc(+yI[u])', u'zok(zok)+Noun+A3sg+P3sg(+sI[u])+Nom', u'zoku(zoku)+Noun+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'zogu',         u'zog(zog)+Noun+A3sg+Pnon+Acc(+yI[u])', u'zog(zog)+Noun+A3sg+P3sg(+sI[u])+Nom', u'zogu(zogu)+Noun+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'ıpa',          u'ıp(ıp)+Noun+A3sg+Pnon+Dat(+yA[a])', u'ıpa(ıpa)+Noun+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'açı',          u'aç(aç)+Noun+A3sg+Pnon+Acc(+yI[ı])', u'aç(aç)+Noun+A3sg+P3sg(+sI[ı])+Nom', u'açı(açı)+Noun+A3sg+Pnon+Nom')

    def test_should_parse_with_explicit_inverse_harmony(self):
        self.assert_parse_correct(u'ome',          u'om(om)+Noun+A3sg+Pnon+Dat(+yA[e])', u'ome(ome)+Noun+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'ani',          u'an(an)+Noun+A3sg+Pnon+Acc(+yI[i])', u'an(an)+Noun+A3sg+P3sg(+sI[i])+Nom', u'ani(ani)+Noun+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'bema',         u'bem(bem)+Noun+A3sg+Pnon+Dat(+yA[a])', u'bema(bema)+Noun+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'bomü',         u'bom(bom)+Noun+A3sg+Pnon+Acc(+yI[ü])', u'bom(bom)+Noun+A3sg+P3sg(+sI[ü])+Nom', u'bomü(bomü)+Noun+A3sg+Pnon+Nom')

    def test_should_parse_with_possible_voicing_and_explicit_inverse_harmony(self):
        self.assert_parse_correct(u'ode',          u'od(od)+Noun+A3sg+Pnon+Dat(+yA[e])', u'od(ot)+Noun+A3sg+Pnon+Dat(+yA[e])', u'ode(ode)+Noun+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'kağe',         u'kağ(kağ)+Noun+A3sg+Pnon+Dat(+yA[e])', u'kağ(kag)+Noun+A3sg+Pnon+Dat(+yA[e])', u'kağ(kak)+Noun+A3sg+Pnon+Dat(+yA[e])', u'kağe(kağe)+Noun+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'zogü',         u'zog(zog)+Noun+A3sg+Pnon+Acc(+yI[ü])', u'zog(zog)+Noun+A3sg+P3sg(+sI[ü])+Nom', u'zogü(zogü)+Noun+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'ıbe',          u'ıb(ıb)+Noun+A3sg+Pnon+Dat(+yA[e])', u'ıb(ıp)+Noun+A3sg+Pnon+Dat(+yA[e])', u'ıbe(ıbe)+Noun+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'aci',          u'ac(ac)+Noun+A3sg+Pnon+Acc(+yI[i])', u'ac(ac)+Noun+A3sg+P3sg(+sI[i])+Nom', u'ac(aç)+Noun+A3sg+Pnon+Acc(+yI[i])', u'ac(aç)+Noun+A3sg+P3sg(+sI[i])+Nom', u'aci(aci)+Noun+A3sg+Pnon+Nom')
        # skip nK -> nG voicing as in cenk->cengi
        self.assert_parse_correct(u'cengı',        u'ceng(ceng)+Noun+A3sg+Pnon+Acc(+yI[ı])', u'ceng(ceng)+Noun+A3sg+P3sg(+sI[ı])+Nom', u'cengı(cengı)+Noun+A3sg+Pnon+Nom')

    def test_should_parse_with_explicit_no_voicing_and_inverse_harmony(self):
        self.assert_parse_correct(u'ote',          u'ot(ot)+Noun+A3sg+Pnon+Dat(+yA[e])', u'ote(ote)+Noun+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'kake',         u'kak(kak)+Noun+A3sg+Pnon+Dat(+yA[e])', u'kake(kake)+Noun+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'zokü',         u'zok(zok)+Noun+A3sg+Pnon+Acc(+yI[ü])', u'zok(zok)+Noun+A3sg+P3sg(+sI[ü])+Nom', u'zokü(zokü)+Noun+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'zogü',         u'zog(zog)+Noun+A3sg+Pnon+Acc(+yI[ü])', u'zog(zog)+Noun+A3sg+P3sg(+sI[ü])+Nom', u'zogü(zogü)+Noun+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'ıpe',          u'ıp(ıp)+Noun+A3sg+Pnon+Dat(+yA[e])', u'ıpe(ıpe)+Noun+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'açi',          u'aç(aç)+Noun+A3sg+Pnon+Acc(+yI[i])', u'aç(aç)+Noun+A3sg+P3sg(+sI[i])+Nom', u'açi(açi)+Noun+A3sg+Pnon+Nom')

    def test_should_parse_with_doubling(self):
        self.assert_parse_correct(u'assı',          u'ass(ass)+Noun+A3sg+Pnon+Acc(+yI[ı])', u'ass(ass)+Noun+A3sg+P3sg(+sI[ı])+Nom', u'ass(as)+Noun+A3sg+Pnon+Acc(+yI[ı])', u'ass(as)+Noun+A3sg+P3sg(+sI[ı])+Nom', u'assı(assı)+Noun+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'tıbbı',         u'tıbb(tıbb)+Noun+A3sg+Pnon+Acc(+yI[ı])', u'tıbb(tıbb)+Noun+A3sg+P3sg(+sI[ı])+Nom', u'tıbb(tıb)+Noun+A3sg+Pnon+Acc(+yI[ı])', u'tıbb(tıb)+Noun+A3sg+P3sg(+sI[ı])+Nom', u'tıbb(tıp)+Noun+A3sg+Pnon+Acc(+yI[ı])', u'tıbb(tıp)+Noun+A3sg+P3sg(+sI[ı])+Nom', u'tıbbı(tıbbı)+Noun+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'hakka',         u'hakk(hakk)+Noun+A3sg+Pnon+Dat(+yA[a])', u'hakk(hak)+Noun+A3sg+Pnon+Dat(+yA[a])', u'hakka(hakka)+Noun+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'hallini',       u'hall(hall)+Noun+A3sg+P2sg(+In[in])+Acc(+yI[i])', u'hall(hall)+Noun+A3sg+P3sg(+sI[i])+Acc(nI[ni])', u'hall(hal)+Noun+A3sg+P2sg(+In[in])+Acc(+yI[i])', u'hall(hal)+Noun+A3sg+P3sg(+sI[i])+Acc(nI[ni])', u'halli(halli)+Noun+A3sg+P2sg(+In[n])+Acc(+yI[i])', u'hallin(hallin)+Noun+A3sg+Pnon+Acc(+yI[i])', u'hallin(hallin)+Noun+A3sg+P3sg(+sI[i])+Nom', u'hallini(hallini)+Noun+A3sg+Pnon+Nom', u'hal(hal)+Noun+A3sg+Pnon+Nom+Adj+With(lI[li])+Noun+Zero+A3sg+P2sg(+In[n])+Acc(+yI[i])')
        self.assert_parse_correct(u'serhaddime',    u'serhadd(serhadd)+Noun+A3sg+P1sg(+Im[im])+Dat(+yA[e])', u'serhadd(serhad)+Noun+A3sg+P1sg(+Im[im])+Dat(+yA[e])', u'serhadd(serhat)+Noun+A3sg+P1sg(+Im[im])+Dat(+yA[e])', u'serhaddi(serhaddi)+Noun+A3sg+P1sg(+Im[m])+Dat(+yA[e])', u'serhaddim(serhaddim)+Noun+A3sg+Pnon+Dat(+yA[e])', u'serhaddime(serhaddime)+Noun+A3sg+Pnon+Nom')

class ParserTestWithBruteForceCompoundNounRootFinder(ParserTest):

    @classmethod
    def setUpClass(cls):
        super(ParserTestWithBruteForceCompoundNounRootFinder, cls).setUpClass()


    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        parser_logger.setLevel(logging.INFO)
        suffix_applier_logger.setLevel(logging.INFO)

        suffix_graph = BasicSuffixGraph()
        suffix_graph.initialize()

        self.mock_brute_force_noun_compound_root_finder = BruteForceCompoundNounRootFinder()

        self.parser = ContextlessMorphologicalParser(suffix_graph, None, [self.mock_brute_force_noun_compound_root_finder])

    def test_should_not_parse_some_cases_without_consontant_S_insertion(self):
        # used imaginary compound "ateli" to keep it short
        self.assert_not_parsable(u'a')
        self.assert_not_parsable(u'an')
        self.assert_not_parsable(u'anu')

        self.assert_not_parsable(u'at')
        self.assert_not_parsable(u'atn')
        self.assert_not_parsable(u'atnu')

        self.assert_not_parsable(u'ate')
        self.assert_not_parsable(u'aten')
        self.assert_not_parsable(u'ateni')

        self.assert_not_parsable(u'atel')
        self.assert_not_parsable(u'ateli')
        self.assert_not_parsable(u'atelni')

        self.assert_not_parsable(u'ateli')
        self.assert_not_parsable(u'atelin')
        # following is parsable, which is correct!
        self.assert_parse_correct(u'atelini',            u'atel(ateli)+Noun+A3sg+P3sg(+sI[i])+Acc(nI[ni])')

        self.assert_not_parsable(u'ateleni')
        self.assert_not_parsable(u'atelani')
        self.assert_not_parsable(u'ateluni')
        self.assert_not_parsable(u'atelüni')
        self.assert_not_parsable(u'ateloni')
        self.assert_not_parsable(u'atelöni')

        self.assert_not_parsable(u'atsdefani')
        self.assert_not_parsable(u'atsdefoni')
        self.assert_not_parsable(u'atsdefuni')
        self.assert_not_parsable(u'atsdefüni')

        self.assert_not_parsable(u'atsdefanu')
        self.assert_not_parsable(u'atsdefonu')
        self.assert_not_parsable(u'atsdefunu')
        self.assert_not_parsable(u'atsdefünu')

    def test_should_not_parse_some_cases_with_consontant_S_insertion(self):
        # used imaginary compound "suağası" to keep it short
        self.assert_not_parsable(u's')
        self.assert_not_parsable(u'sn')
        self.assert_not_parsable(u'snu')

        self.assert_not_parsable(u'su')
        self.assert_not_parsable(u'sun')
        self.assert_not_parsable(u'sunu')

        self.assert_not_parsable(u'sua')
        self.assert_not_parsable(u'suan')
        self.assert_not_parsable(u'suanı')

        self.assert_not_parsable(u'suağ')
        self.assert_not_parsable(u'suağı')
        self.assert_not_parsable(u'suağnı')

        self.assert_not_parsable(u'suağa')
        self.assert_not_parsable(u'suağan')
        self.assert_not_parsable(u'suağanı')        # actually, this is also compound, but this case is not supported

        self.assert_not_parsable(u'suağas')
        self.assert_not_parsable(u'suağası')
        self.assert_not_parsable(u'suağasnı')

        self.assert_not_parsable(u'suağası')
        self.assert_not_parsable(u'suağasın')
        # following is parsable, which is correct!
        self.assert_parse_correct(u'suağasını',     u'suağas(suağası)+Noun+A3sg+P3sg(+sI[ı])+Acc(nI[nı])', u'suağa(suağası)+Noun+A3sg+P3sg(+sI[sı])+Acc(nI[nı])')

        self.assert_not_parsable(u'suağassn')

        self.assert_not_parsable(u'suağasanı')
        self.assert_not_parsable(u'suağasenı')
        self.assert_not_parsable(u'suağasunı')
        self.assert_not_parsable(u'suağasünı')
        self.assert_not_parsable(u'suağasonı')
        self.assert_not_parsable(u'suağasönı')

        self.assert_not_parsable(u'suağasanu')
        self.assert_not_parsable(u'suağasenu')
        self.assert_not_parsable(u'suağasunu')
        self.assert_not_parsable(u'suağasünu')
        self.assert_not_parsable(u'suağasonu')
        self.assert_not_parsable(u'suağasönu')


    def test_should_parse_simple_compounds(self):
        self.assert_parse_correct(u'bacakkalemini',        u'bacakkalem(bacakkalemi)+Noun+A3sg+P3sg(+sI[i])+Acc(nI[ni])')
        self.assert_parse_correct(u'suborusuna',           u'suborus(suborusu)+Noun+A3sg+P3sg(+sI[u])+Dat(nA[na])', u'suboru(suborusu)+Noun+A3sg+P3sg(+sI[su])+Dat(nA[na])')

    def test_should_parse_with_possible_voicing(self):
        self.assert_parse_correct(u'kuzukulağını',         u'kuzukulağ(kuzukulağı)+Noun+A3sg+P3sg(+sI[ı])+Acc(nI[nı])')
        self.assert_parse_correct(u'eczadolabında',        u'eczadolab(eczadolabı)+Noun+A3sg+P3sg(+sI[ı])+Loc(ndA[nda])')
        self.assert_parse_correct(u'kafakağıdından',       u'kafakağıd(kafakağıdı)+Noun+A3sg+P3sg(+sI[ı])+Abl(ndAn[ndan])')

    def test_should_parse_with_explicit_no_voicing(self):
        self.assert_parse_correct(u'adamotuna',          u'adamot(adamotu)+Noun+A3sg+P3sg(+sI[u])+Dat(nA[na])')
        self.assert_parse_correct(u'kaleiçinden',        u'kaleiç(kaleiçi)+Noun+A3sg+P3sg(+sI[i])+Abl(ndAn[nden])')
        self.assert_parse_correct(u'uykuhapını',         u'uykuhap(uykuhapı)+Noun+A3sg+P3sg(+sI[ı])+Acc(nI[nı])')
        self.assert_parse_correct(u'anaerkine',          u'anaerk(anaerki)+Noun+A3sg+P3sg(+sI[i])+Dat(nA[ne])')

    def test_should_parse_with_explicit_inverse_harmony(self):
        self.assert_parse_correct(u'dünyahaline',          u'dünyahal(dünyahali)+Noun+A3sg+P3sg(+sI[i])+Dat(nA[ne])')
        self.assert_parse_correct(u'doğuekolünü',          u'doğuekol(doğuekolü)+Noun+A3sg+P3sg(+sI[ü])+Acc(nI[nü])')
        self.assert_parse_correct(u'adamkatlini',          u'adamkatl(adamkatli)+Noun+A3sg+P3sg(+sI[i])+Acc(nI[ni])')

    def test_should_parse_with_possible_voicing_and_explicit_inverse_harmony(self):
        self.assert_parse_correct(u'saçmakelime_abine',    u'saçmakelime_ab(saçmakelime_abi)+Noun+A3sg+P3sg(+sI[i])+Dat(nA[ne])')

    def test_should_parse_with_doubling(self):
        self.assert_parse_correct(u'yaşhaddinden',         u'yaşhadd(yaşhaddi)+Noun+A3sg+P3sg(+sI[i])+Abl(ndAn[nden])')


if __name__ == '__main__':
    unittest.main()
