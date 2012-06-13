# coding=utf-8
import logging
import os
import unittest
from hamcrest import *
from hamcrest.core.base_matcher import BaseMatcher
from trnltk.stem.dictionaryitem import PrimaryPosition
from trnltk.stem.dictionaryloader import DictionaryLoader
from trnltk.stem.stemgenerator import StemGenerator
from trnltk.suffixgraph.extendedsuffixgraph import ExtendedSuffixGraph
from trnltk.suffixgraph.parser import Parser, logger as parser_logger
from trnltk.suffixgraph.suffixapplier import logger as suffix_applier_logger
from trnltk.suffixgraph.predefinedpaths import PredefinedPaths

class ParserTestWithExtendedGraph(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(ParserTestWithExtendedGraph, cls).setUpClass()
        cls.all_stems = []

        dictionary_items = DictionaryLoader.load_from_file(os.path.join(os.path.dirname(__file__), '../../resources/master_dictionary.txt'))
        for di in dictionary_items:
            cls.all_stems.extend(StemGenerator.generate(di))

        suffix_graph = ExtendedSuffixGraph()
        predefined_paths = PredefinedPaths(cls.all_stems, suffix_graph)
        predefined_paths.create_predefined_paths()

        cls.parser = Parser(cls.all_stems, suffix_graph, predefined_paths)

    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        parser_logger.setLevel(logging.INFO)
        suffix_applier_logger.setLevel(logging.INFO)

    def test_should_parse_other_positions_to_verbs_zero_transition(self):
        parser_logger.setLevel(logging.DEBUG)
        suffix_applier_logger.setLevel(logging.DEBUG)

        #remove some stems for keeping the tests simple!
        self.parser.stem_map['elmas'] = []
        self.parser.stem_map['bent'] = []
        self.parser.stem_map['bend'] = []
        self.parser.stem_map['oy'] = []
        self.parser.stem_map['ben'] = filter(lambda stem : stem.dictionary_item.primary_position==PrimaryPosition.PRONOUN, self.parser.stem_map['ben'])


        self.assert_parse_correct_for_verb(u'elmayım',            u'elma(elma)+Noun+A3sg+Pnon+Nom+Verb+Zero+Pres+A1sg(+yIm[yım])')
        self.assert_parse_correct_for_verb(u'elmasın',            u'elma(elma)+Noun+A3sg+Pnon+Nom+Verb+Zero+Pres+A2sg(sIn[sın])')
        self.assert_parse_correct_for_verb(u'elma',               u'elma(elma)+Noun+A3sg+Pnon+Nom', u'elma(elma)+Noun+A3sg+Pnon+Nom+Verb+Zero+Pres+A3sg')
        self.assert_parse_correct_for_verb(u'elmayız',            u'elma(elma)+Noun+A3sg+Pnon+Nom+Verb+Zero+Pres+A1pl(+yIz[yız])')
        self.assert_parse_correct_for_verb(u'elmasınız',          u'elma(elma)+Noun+A3sg+Pnon+Nom+Verb+Zero+Pres+A2pl(sInIz[sınız])')
        self.assert_parse_correct_for_verb(u'elmalar',            u'elma(elma)+Noun+A3sg+Pnon+Nom+Verb+Zero+Pres+A3pl(lAr[lar])', u'elma(elma)+Noun+A3pl(lAr[lar])+Pnon+Nom', u'elma(elma)+Noun+A3pl(lAr[lar])+Pnon+Nom+Verb+Zero+Pres+A3sg')

        self.assert_parse_correct_for_verb(u'elmaymışım',         u'elma(elma)+Noun+A3sg+Pnon+Nom+Verb+Zero+Narr(+ymIş[ymış])+A1sg(+yIm[ım])')
        self.assert_parse_correct_for_verb(u'elmaymışsın',        u'elma(elma)+Noun+A3sg+Pnon+Nom+Verb+Zero+Narr(+ymIş[ymış])+A2sg(sIn[sın])')
        self.assert_parse_correct_for_verb(u'elmaymış',           u'elma(elma)+Noun+A3sg+Pnon+Nom+Verb+Zero+Narr(+ymIş[ymış])+A3sg')
        self.assert_parse_correct_for_verb(u'elmaymışız',         u'elma(elma)+Noun+A3sg+Pnon+Nom+Verb+Zero+Narr(+ymIş[ymış])+A1pl(+yIz[ız])')
        self.assert_parse_correct_for_verb(u'elmaymışsınız',      u'elma(elma)+Noun+A3sg+Pnon+Nom+Verb+Zero+Narr(+ymIş[ymış])+A2pl(sInIz[sınız])')
        self.assert_parse_correct_for_verb(u'elmaymışlar',        u'elma(elma)+Noun+A3sg+Pnon+Nom+Verb+Zero+Narr(+ymIş[ymış])+A3pl(lAr[lar])')

        self.assert_parse_correct_for_verb(u'elmaydım',           u'elma(elma)+Noun+A3sg+Pnon+Nom+Verb+Zero+Past(+ydI[ydı])+A1sg(m[m])')
        self.assert_parse_correct_for_verb(u'elmaydın',           u'elma(elma)+Noun+A3sg+Pnon+Nom+Verb+Zero+Past(+ydI[ydı])+A2sg(n[n])')
        self.assert_parse_correct_for_verb(u'elmaydı',            u'elma(elma)+Noun+A3sg+Pnon+Nom+Verb+Zero+Past(+ydI[ydı])+A3sg')
        self.assert_parse_correct_for_verb(u'elmaydık',           u'elma(elma)+Noun+A3sg+Pnon+Nom+Verb+Zero+Past(+ydI[ydı])+A1pl(k[k])')
        self.assert_parse_correct_for_verb(u'elmaydınız',         u'elma(elma)+Noun+A3sg+Pnon+Nom+Verb+Zero+Past(+ydI[ydı])+A2pl(nIz[nız])')
        self.assert_parse_correct_for_verb(u'elmaydılar',         u'elma(elma)+Noun+A3sg+Pnon+Nom+Verb+Zero+Past(+ydI[ydı])+A3pl(lAr[lar])')

        self.assert_parse_correct_for_verb(u'elmaysam',           u'elma(elma)+Noun+A3sg+Pnon+Nom+Verb+Zero+Cond(+ysA[ysa])+A1sg(m[m])')
        self.assert_parse_correct_for_verb(u'elmaysan',           u'elma(elma)+Noun+A3sg+Pnon+Nom+Verb+Zero+Cond(+ysA[ysa])+A2sg(n[n])')
        self.assert_parse_correct_for_verb(u'elmaysa',            u'elma(elma)+Noun+A3sg+Pnon+Nom+Verb+Zero+Cond(+ysA[ysa])+A3sg')
        self.assert_parse_correct_for_verb(u'elmaysak',           u'elma(elma)+Noun+A3sg+Pnon+Nom+Verb+Zero+Cond(+ysA[ysa])+A1pl(k[k])')
        self.assert_parse_correct_for_verb(u'elmaysanız',         u'elma(elma)+Noun+A3sg+Pnon+Nom+Verb+Zero+Cond(+ysA[ysa])+A2pl(nIz[nız])')
        self.assert_parse_correct_for_verb(u'elmaysalar',         u'elma(elma)+Noun+A3sg+Pnon+Nom+Verb+Zero+Cond(+ysA[ysa])+A3pl(lAr[lar])')

        self.assert_parse_correct_for_verb(u'elmansam',           u'elma(elma)+Noun+A3sg+P2sg(+In[n])+Nom+Verb+Zero+Cond(+ysA[sa])+A1sg(m[m])')
        self.assert_parse_correct_for_verb(u'elmamsa',            u'elma(elma)+Noun+A3sg+P1sg(+Im[m])+Nom+Verb+Zero+Cond(+ysA[sa])+A3sg')
        self.assert_parse_correct_for_verb(u'elmamdın',           u'elma(elma)+Noun+A3sg+P1sg(+Im[m])+Nom+Verb+Zero+Past(+ydI[dı])+A2sg(n[n])')
        self.assert_parse_correct_for_verb(u'elmanızdık',         u'elma(elma)+Noun+A3sg+P2pl(+InIz[nız])+Nom+Verb+Zero+Past(+ydI[dı])+A1pl(k[k])')
        self.assert_parse_correct_for_verb(u'elmamızmışsınız',    u'elma(elma)+Noun+A3sg+P1pl(+ImIz[mız])+Nom+Verb+Zero+Narr(+ymIş[mış])+A2pl(sInIz[sınız])')
        self.assert_parse_correct_for_verb(u'elmalarınızsalar',   u'elma(elma)+Noun+A3pl(lAr[lar])+P2pl(+InIz[ınız])+Nom+Verb+Zero+Cond(+ysA[sa])+A3pl(lAr[lar])')

        self.assert_parse_correct_for_verb(u'iyiyim',             u'iyi(iyi)+Adj+Verb+Zero+Pres+A1sg(+yIm[yim])', u'iyi(iyi)+Adj+Noun+Zero+A3sg+Pnon+Nom+Verb+Zero+Pres+A1sg(+yIm[yim])')
        self.assert_parse_correct_for_verb(u'küçüğümüzdeyseler',  u'küçüğ(küçük)+Adj+Noun+Zero+A3sg+P1pl(+ImIz[ümüz])+Loc(dA[de])+Verb+Zero+Cond(+ysA[yse])+A3pl(lAr[ler])')
        self.assert_parse_correct_for_verb(u'küçüklerimizindiler',u'küçük(küçük)+Adj+Noun+Zero+A3pl(lAr[ler])+P1pl(+ImIz[imiz])+Gen(+nIn[in])+Verb+Zero+Past(+ydI[di])+A3pl(lAr[ler])')
        self.assert_parse_correct_for_verb(u'küçüğüm',
            u'küçüğ(küçük)+Adj+Verb+Zero+Pres+A1sg(+yIm[üm])',                          # ben kucugum.
            u'küçüğ(küçük)+Adj+Noun+Zero+A3sg+P1sg(+Im[üm])+Nom',                       # kucugum geldi.
            u'küçüğ(küçük)+Adj+Noun+Zero+A3sg+Pnon+Nom+Verb+Zero+Pres+A1sg(+yIm[üm])',  # ben kucugum.
            u'küçüğ(küçük)+Adj+Noun+Zero+A3sg+P1sg(+Im[üm])+Nom+Verb+Zero+Pres+A3sg')   # -kim geldi? -kucugum
        self.assert_parse_correct_for_verb(u'bendim',             u'ben(ben)+Pron+Pers+A1sg+Pnon+Nom+Verb+Zero+Past(+ydI[di])+A1sg(m[m])')
        self.assert_parse_correct_for_verb(u'benim',
            u'ben(ben)+Pron+Pers+A1sg+Pnon+Gen(im[im])',                         # benim kitabim.
            u'ben(ben)+Pron+Pers+A1sg+Pnon+Gen(im[im])+Verb+Zero+Pres+A3sg',     # -kimin o? -benim (benim kitabim).
            u'ben(ben)+Pron+Pers+A1sg+Pnon+Nom+Verb+Zero+Pres+A1sg(+yIm[im])'    # -kim o?   -benim (ben geldim).
        )
        self.assert_parse_correct_for_verb(u'sensin',             u'sen(sen)+Pron+Pers+A2sg+Pnon+Nom+Verb+Zero+Pres+A2sg(sIn[sin])')
        self.assert_parse_correct_for_verb(u'oydu',               u'o(o)+Pron+Pers+A3sg+Pnon+Nom+Verb+Zero+Past(+ydI[ydu])+A3sg', u'o(o)+Pron+Demons+A3sg+Pnon+Nom+Verb+Zero+Past(+ydI[ydu])+A3sg')
        self.assert_parse_correct_for_verb(u'hızlıcaymışlar',
            u'hızlı(hızlı)+Adj+Adv+Ly(cA[ca])+Verb+Zero+Narr(+ymIş[ymış])+A3pl(lAr[lar])',
            u'hız(hız)+Noun+A3sg+Pnon+Nom+Adj+With(lI[lı])+Adv+Ly(cA[ca])+Verb+Zero+Narr(+ymIş[ymış])+A3pl(lAr[lar])'
        )

    def test_should_parse_copula_derivations(self):
        parser_logger.setLevel(logging.DEBUG)
        suffix_applier_logger.setLevel(logging.DEBUG)

        self.parser.stem_map['elmas'] = []
        self.parser.stem_map['on'] = []

        self.assert_parse_correct_for_verb(u'elmayken',            u'elma(elma)+Noun+A3sg+Pnon+Nom+Verb+Zero+Adv+While(+yken[yken])', u'elma(elma)+Noun+A3sg+Pnon+Nom+Verb+Zero+Adv+While(+yken[yken])+Verb+Zero+Pres+A3sg')
        self.assert_parse_correct_for_verb(u'elmasıyken',          u'elma(elma)+Noun+A3sg+P3sg(+sI[sı])+Nom+Verb+Zero+Adv+While(+yken[yken])', u'elma(elma)+Noun+A3sg+P3sg(+sI[sı])+Nom+Verb+Zero+Adv+While(+yken[yken])+Verb+Zero+Pres+A3sg')
        self.assert_parse_correct_for_verb(u'kitapken',            u'kitap(kitap)+Noun+A3sg+Pnon+Nom+Verb+Zero+Adv+While(+yken[ken])', u'kitap(kitap)+Noun+A3sg+Pnon+Nom+Verb+Zero+Adv+While(+yken[ken])+Verb+Zero+Pres+A3sg')
        self.assert_parse_correct_for_verb(u'kitaplarıyken',       u'kitap(kitap)+Noun+A3sg+P3pl(lArI[ları])+Nom+Verb+Zero+Adv+While(+yken[yken])', u'kitap(kitap)+Noun+A3pl(lAr[lar])+Pnon+Acc(+yI[ı])+Verb+Zero+Adv+While(+yken[yken])', u'kitap(kitap)+Noun+A3pl(lAr[lar])+P3sg(+sI[ı])+Nom+Verb+Zero+Adv+While(+yken[yken])', u'kitap(kitap)+Noun+A3pl(lAr[lar])+P3pl(I[ı])+Nom+Verb+Zero+Adv+While(+yken[yken])', u'kitap(kitap)+Noun+A3sg+P3pl(lArI[lar\u0131])+Nom+Verb+Zero+Adv+While(+yken[yken])+Verb+Zero+Pres+A3sg', u'kitap(kitap)+Noun+A3pl(lAr[lar])+Pnon+Acc(+yI[\u0131])+Verb+Zero+Adv+While(+yken[yken])+Verb+Zero+Pres+A3sg', u'kitap(kitap)+Noun+A3pl(lAr[lar])+P3sg(+sI[\u0131])+Nom+Verb+Zero+Adv+While(+yken[yken])+Verb+Zero+Pres+A3sg', u'kitap(kitap)+Noun+A3pl(lAr[lar])+P3pl(I[\u0131])+Nom+Verb+Zero+Adv+While(+yken[yken])+Verb+Zero+Pres+A3sg')
        self.assert_parse_correct_for_verb(u'küçükken',            u'küçük(küçük)+Adj+Verb+Zero+Adv+While(+yken[ken])', u'küçük(küçük)+Adj+Verb+Zero+Adv+While(+yken[ken])+Verb+Zero+Pres+A3sg', u'küçük(küçük)+Adj+Noun+Zero+A3sg+Pnon+Nom+Verb+Zero+Adv+While(+yken[ken])', u'küçük(küçük)+Adj+Noun+Zero+A3sg+Pnon+Nom+Verb+Zero+Adv+While(+yken[ken])+Verb+Zero+Pres+A3sg')
        self.assert_parse_correct_for_verb(u'küçüğümüzdeyken',     u'küçüğ(küçük)+Adj+Noun+Zero+A3sg+P1pl(+ImIz[ümüz])+Loc(dA[de])+Verb+Zero+Adv+While(+yken[yken])', u'küçüğ(küçük)+Adj+Noun+Zero+A3sg+P1pl(+ImIz[ümüz])+Loc(dA[de])+Verb+Zero+Adv+While(+yken[yken])+Verb+Zero+Pres+A3sg')
        self.assert_parse_correct_for_verb(u'maviceyken',          u'mavi(mavi)+Adj+Adv+Ly(cA[ce])+Verb+Zero+Adv+While(+yken[yken])', u'mavi(mavi)+Adj+Adv+Ly(cA[ce])+Verb+Zero+Adv+While(+yken[yken])+Verb+Zero+Pres+A3sg')
        self.assert_parse_correct_for_verb(u'seninken',            u'sen(sen)+Pron+Pers+A2sg+Pnon+Gen(in[in])+Verb+Zero+Adv+While(+yken[ken])', u'sen(sen)+Pron+Pers+A2sg+Pnon+Gen(in[in])+Verb+Zero+Adv+While(+yken[ken])+Verb+Zero+Pres+A3sg')
        self.assert_parse_correct_for_verb(u'onlarken',            u'o(o)+Pron+Pers+A3pl(nlar[nlar])+Pnon+Nom+Verb+Zero+Adv+While(+yken[ken])', u'o(o)+Pron+Demons+A3pl(nlar[nlar])+Pnon+Nom+Verb+Zero+Adv+While(+yken[ken])', u'o(o)+Pron+Pers+A3pl(nlar[nlar])+Pnon+Nom+Verb+Zero+Adv+While(+yken[ken])+Verb+Zero+Pres+A3sg', u'o(o)+Pron+Demons+A3pl(nlar[nlar])+Pnon+Nom+Verb+Zero+Adv+While(+yken[ken])+Verb+Zero+Pres+A3sg')

    def assert_parse_correct_for_verb(self, word_to_parse, *args):
        assert_that(self.parse_result(word_to_parse), IsParseResultMatches([a for a in args]))

    def assert_parse_correct(self, word_to_parse, *args):
        assert_that(self.parse_result(word_to_parse), IsParseResultMatchesIgnoreVerbPresA3Sg([a for a in args]))

    def parse_result(self, word):
        return [r.to_pretty_str() for r in (self.parser.parse(word))]

class IsParseResultMatches(BaseMatcher):
    def __init__(self, expected_results):
        self.expected_results = expected_results

    def _matches(self, items):
        return all(er in items for er in self.expected_results) and all(item in self.expected_results for item in items)

    def describe_to(self, description):
        description.append_text(u'     ' + str(self.expected_results))

class IsParseResultMatchesIgnoreVerbPresA3Sg(BaseMatcher):
    def __init__(self, expected_results):
        self.expected_results = expected_results

    def _matches(self, items):
        items = filter(lambda item : u'+Zero+Pres+' not in item, items)
        return all(er in items for er in self.expected_results) and all(item in self.expected_results for item in items)

    def describe_to(self, description):
        description.append_text(u'     ' + str(self.expected_results))

if __name__ == '__main__':
    unittest.main()
