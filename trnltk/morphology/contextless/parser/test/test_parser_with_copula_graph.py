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
from trnltk.morphology.model.lexeme import SyntacticCategory
from trnltk.morphology.lexicon.lexiconloader import LexiconLoader
from trnltk.morphology.lexicon.rootgenerator import RootGenerator, RootMapGenerator
from trnltk.morphology.morphotactics.basicsuffixgraph import BasicSuffixGraph
from trnltk.morphology.morphotactics.copulasuffixgraph import CopulaSuffixGraph
from trnltk.morphology.contextless.parser.parser import ContextlessMorphologicalParser, logger as parser_logger
from trnltk.morphology.contextless.parser.rootfinder import WordRootFinder
from trnltk.morphology.contextless.parser.suffixapplier import logger as suffix_applier_logger
from trnltk.morphology.morphotactics.predefinedpaths import PredefinedPaths

class ParserTestWithExtendedGraph(ParserTest):

    @classmethod
    def setUpClass(cls):
        super(ParserTestWithExtendedGraph, cls).setUpClass()
        all_roots = []

        lexemes = LexiconLoader.load_from_file(os.path.join(os.path.dirname(__file__), '../../../../resources/master_dictionary.txt'))
        for di in lexemes:
            all_roots.extend(RootGenerator.generate(di))


        cls._org_root_map = (RootMapGenerator()).generate(all_roots)

    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        parser_logger.setLevel(logging.INFO)
        suffix_applier_logger.setLevel(logging.INFO)

        self.cloned_root_map = copy(self._org_root_map)

        suffix_graph = CopulaSuffixGraph(BasicSuffixGraph())
        suffix_graph.initialize()
        predefined_paths = PredefinedPaths(self.cloned_root_map, suffix_graph)
        predefined_paths.create_predefined_paths()

        word_root_finder = WordRootFinder(self.cloned_root_map)

        self.parser = ContextlessMorphologicalParser(suffix_graph, predefined_paths,
            [word_root_finder])

    def test_should_parse_other_categories_to_verbs_zero_transition(self):
        #remove some roots for keeping the tests simple!
        self.cloned_root_map['elmas'] = []
        self.cloned_root_map['bent'] = []
        self.cloned_root_map['bend'] = []
        self.cloned_root_map['se'] = []
        self.cloned_root_map['oy'] = []
        self.cloned_root_map['ben'] = filter(lambda root : root.lexeme.syntactic_category==SyntacticCategory.PRONOUN, self.cloned_root_map['ben'])


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

        self.assert_parse_correct_for_verb(u'iyiyim',             u'iyi(iyi)+Adj+Verb+Zero+Pres+A1sg(+yIm[yim])', u'iyi(iyi)+Adj+Adv+Zero+Verb+Zero+Pres+A1sg(+yIm[yim])', u'iyi(iyi)+Adj+Noun+Zero+A3sg+Pnon+Nom+Verb+Zero+Pres+A1sg(+yIm[yim])')
        self.assert_parse_correct_for_verb(u'küçüğümüzdeyseler',  u'küçüğ(küçük)+Adj+Noun+Zero+A3sg+P1pl(+ImIz[ümüz])+Loc(dA[de])+Verb+Zero+Cond(+ysA[yse])+A3pl(lAr[ler])')
        self.assert_parse_correct_for_verb(u'küçüklerimizindiler',u'küçük(küçük)+Adj+Noun+Zero+A3pl(lAr[ler])+P1pl(+ImIz[imiz])+Gen(+nIn[in])+Verb+Zero+Past(+ydI[di])+A3pl(lAr[ler])')
        self.assert_parse_correct_for_verb(u'küçüğüm',
            u'küçüğ(küçük)+Adj+Verb+Zero+Pres+A1sg(+yIm[üm])',                          # ben kucugum.
            u'küçüğ(küçük)+Adj+Noun+Zero+A3sg+P1sg(+Im[üm])+Nom',                       # kucugum geldi.
            u'küçüğ(küçük)+Adj+Adv+Zero+Verb+Zero+Pres+A1sg(+yIm[üm])',                        # TODO: sacma
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
            u'hızlı(hızlı)+Adj+Adj+Equ(cA[ca])+Verb+Zero+Narr(+ymIş[ymış])+A3pl(lAr[lar])',
            u'hızlı(hızlı)+Adj+Adj+Quite(cA[ca])+Verb+Zero+Narr(+ymIş[ymış])+A3pl(lAr[lar])', 
            u'hızlı(hızlı)+Adj+Adv+Ly(cA[ca])+Verb+Zero+Narr(+ymIş[ymış])+A3pl(lAr[lar])', 
            u'hızlı(hızlı)+Adj+Adj+Equ(cA[ca])+Adv+Zero+Verb+Zero+Narr(+ymIş[ymış])+A3pl(lAr[lar])',
            u'hızlı(hızlı)+Adj+Adj+Quite(cA[ca])+Adv+Zero+Verb+Zero+Narr(+ymIş[ymış])+A3pl(lAr[lar])', 
            u'hız(hız)+Noun+A3sg+Pnon+Nom+Adj+With(lI[lı])+Adj+Equ(cA[ca])+Verb+Zero+Narr(+ymIş[ymış])+A3pl(lAr[lar])', 
            u'hız(hız)+Noun+A3sg+Pnon+Nom+Adj+With(lI[lı])+Adj+Quite(cA[ca])+Verb+Zero+Narr(+ymIş[ymış])+A3pl(lAr[lar])', 
            u'hız(hız)+Noun+A3sg+Pnon+Nom+Adj+With(lI[lı])+Adv+Ly(cA[ca])+Verb+Zero+Narr(+ymIş[ymış])+A3pl(lAr[lar])', 
            u'hızlı(hızlı)+Adj+Noun+Zero+A3sg+Pnon+Nom+Adj+Equ(cA[ca])+Verb+Zero+Narr(+ymIş[ymış])+A3pl(lAr[lar])', 
            u'hızlı(hızlı)+Adj+Noun+Zero+A3sg+Pnon+Nom+Adv+InTermsOf(cA[ca])+Verb+Zero+Narr(+ymIş[ymış])+A3pl(lAr[lar])', 
            u'hızlı(hızlı)+Adj+Noun+Zero+A3sg+Pnon+Nom+Adv+By(cA[ca])+Verb+Zero+Narr(+ymIş[ymış])+A3pl(lAr[lar])', 
            u'hızlı(hızlı)+Adj+Adj+Equ(cA[ca])+Noun+Zero+A3sg+Pnon+Nom+Verb+Zero+Narr(+ymIş[ymış])+A3pl(lAr[lar])', 
            u'hızlı(hızlı)+Adj+Adj+Quite(cA[ca])+Noun+Zero+A3sg+Pnon+Nom+Verb+Zero+Narr(+ymIş[ymış])+A3pl(lAr[lar])', 
            u'hız(hız)+Noun+A3sg+Pnon+Nom+Adj+With(lI[lı])+Adj+Equ(cA[ca])+Adv+Zero+Verb+Zero+Narr(+ymIş[ymış])+A3pl(lAr[lar])', 
            u'hız(hız)+Noun+A3sg+Pnon+Nom+Adj+With(lI[lı])+Adj+Quite(cA[ca])+Adv+Zero+Verb+Zero+Narr(+ymIş[ymış])+A3pl(lAr[lar])', 
            u'hızlı(hızlı)+Adj+Noun+Zero+A3sg+Pnon+Nom+Adj+Equ(cA[ca])+Adv+Zero+Verb+Zero+Narr(+ymIş[ymış])+A3pl(lAr[lar])', 
            u'hız(hız)+Noun+A3sg+Pnon+Nom+Adj+With(lI[lı])+Noun+Zero+A3sg+Pnon+Nom+Adj+Equ(cA[ca])+Verb+Zero+Narr(+ymIş[ymış])+A3pl(lAr[lar])', 
            u'hız(hız)+Noun+A3sg+Pnon+Nom+Adj+With(lI[lı])+Noun+Zero+A3sg+Pnon+Nom+Adv+InTermsOf(cA[ca])+Verb+Zero+Narr(+ymIş[ymış])+A3pl(lAr[lar])', 
            u'hız(hız)+Noun+A3sg+Pnon+Nom+Adj+With(lI[lı])+Noun+Zero+A3sg+Pnon+Nom+Adv+By(cA[ca])+Verb+Zero+Narr(+ymIş[ymış])+A3pl(lAr[lar])', 
            u'hız(hız)+Noun+A3sg+Pnon+Nom+Adj+With(lI[lı])+Adj+Equ(cA[ca])+Noun+Zero+A3sg+Pnon+Nom+Verb+Zero+Narr(+ymIş[ymış])+A3pl(lAr[lar])', 
            u'hız(hız)+Noun+A3sg+Pnon+Nom+Adj+With(lI[lı])+Adj+Quite(cA[ca])+Noun+Zero+A3sg+Pnon+Nom+Verb+Zero+Narr(+ymIş[ymış])+A3pl(lAr[lar])', 
            u'hızlı(hızlı)+Adj+Noun+Zero+A3sg+Pnon+Nom+Adj+Equ(cA[ca])+Noun+Zero+A3sg+Pnon+Nom+Verb+Zero+Narr(+ymIş[ymış])+A3pl(lAr[lar])', 
            u'hız(hız)+Noun+A3sg+Pnon+Nom+Adj+With(lI[lı])+Noun+Zero+A3sg+Pnon+Nom+Adj+Equ(cA[ca])+Adv+Zero+Verb+Zero+Narr(+ymIş[ymış])+A3pl(lAr[lar])', 
            u'hız(hız)+Noun+A3sg+Pnon+Nom+Adj+With(lI[lı])+Noun+Zero+A3sg+Pnon+Nom+Adj+Equ(cA[ca])+Noun+Zero+A3sg+Pnon+Nom+Verb+Zero+Narr(+ymIş[ymış])+A3pl(lAr[lar])'
        )

    def test_should_parse_copula_derivations(self):
        self.cloned_root_map['elmas'] = []
        self.cloned_root_map['on'] = []
        self.cloned_root_map['se'] = []

        self.assert_parse_correct_for_verb(u'elmayken',            u'elma(elma)+Noun+A3sg+Pnon+Nom+Verb+Zero+Adv+While(+yken[yken])', u'elma(elma)+Noun+A3sg+Pnon+Nom+Verb+Zero+Adv+While(+yken[yken])+Verb+Zero+Pres+A3sg')
        self.assert_parse_correct_for_verb(u'elmasıyken',          u'elma(elma)+Noun+A3sg+P3sg(+sI[sı])+Nom+Verb+Zero+Adv+While(+yken[yken])', u'elma(elma)+Noun+A3sg+P3sg(+sI[sı])+Nom+Verb+Zero+Adv+While(+yken[yken])+Verb+Zero+Pres+A3sg')
        self.assert_parse_correct_for_verb(u'kitapken',            u'kitap(kitap)+Noun+A3sg+Pnon+Nom+Verb+Zero+Adv+While(+yken[ken])', u'kitap(kitap)+Noun+A3sg+Pnon+Nom+Verb+Zero+Adv+While(+yken[ken])+Verb+Zero+Pres+A3sg')
        self.assert_parse_correct_for_verb(u'kitaplarıyken',       u'kitap(kitap)+Noun+A3sg+P3pl(lArI![ları])+Nom+Verb+Zero+Adv+While(+yken[yken])', u'kitap(kitap)+Noun+A3pl(lAr[lar])+Pnon+Acc(+yI[ı])+Verb+Zero+Adv+While(+yken[yken])', u'kitap(kitap)+Noun+A3pl(lAr[lar])+P3sg(+sI[ı])+Nom+Verb+Zero+Adv+While(+yken[yken])', u'kitap(kitap)+Noun+A3pl(lAr[lar])+P3pl(I![ı])+Nom+Verb+Zero+Adv+While(+yken[yken])', u'kitap(kitap)+Noun+A3sg+P3pl(lArI![ları])+Nom+Verb+Zero+Adv+While(+yken[yken])+Verb+Zero+Pres+A3sg', u'kitap(kitap)+Noun+A3pl(lAr[lar])+Pnon+Acc(+yI[ı])+Verb+Zero+Adv+While(+yken[yken])+Verb+Zero+Pres+A3sg', u'kitap(kitap)+Noun+A3pl(lAr[lar])+P3sg(+sI[ı])+Nom+Verb+Zero+Adv+While(+yken[yken])+Verb+Zero+Pres+A3sg', u'kitap(kitap)+Noun+A3pl(lAr[lar])+P3pl(I![ı])+Nom+Verb+Zero+Adv+While(+yken[yken])+Verb+Zero+Pres+A3sg')
        self.assert_parse_correct_for_verb(u'küçükken',
            u'küçük(küçük)+Adj+Verb+Zero+Adv+While(+yken[ken])',
            u'küçük(küçük)+Adj+Verb+Zero+Adv+While(+yken[ken])+Verb+Zero+Pres+A3sg',
            u'küçük(küçük)+Adj+Adv+Zero+Verb+Zero+Adv+While(+yken[ken])',
            u'küçük(küçük)+Adj+Noun+Zero+A3sg+Pnon+Nom+Verb+Zero+Adv+While(+yken[ken])',
            u'küçük(küçük)+Adj+Adv+Zero+Verb+Zero+Adv+While(+yken[ken])+Verb+Zero+Pres+A3sg',   # TODO: sacma
            u'küçük(küçük)+Adj+Noun+Zero+A3sg+Pnon+Nom+Verb+Zero+Adv+While(+yken[ken])+Verb+Zero+Pres+A3sg')
        self.assert_parse_correct_for_verb(u'küçüğümüzdeyken',     u'küçüğ(küçük)+Adj+Noun+Zero+A3sg+P1pl(+ImIz[ümüz])+Loc(dA[de])+Verb+Zero+Adv+While(+yken[yken])', u'küçüğ(küçük)+Adj+Noun+Zero+A3sg+P1pl(+ImIz[ümüz])+Loc(dA[de])+Verb+Zero+Adv+While(+yken[yken])+Verb+Zero+Pres+A3sg')
        self.assert_parse_correct_for_verb(u'maviceyken',
            u'mavi(mavi)+Adj+Adj+Equ(cA[ce])+Verb+Zero+Adv+While(+yken[yken])',
            u'mavi(mavi)+Adj+Adj+Quite(cA[ce])+Verb+Zero+Adv+While(+yken[yken])',
            u'mavi(mavi)+Adj+Adv+Ly(cA[ce])+Verb+Zero+Adv+While(+yken[yken])',
            u'mavi(mavi)+Adj+Adj+Equ(cA[ce])+Adv+Zero+Verb+Zero+Adv+While(+yken[yken])',
            u'mavi(mavi)+Adj+Adj+Quite(cA[ce])+Adv+Zero+Verb+Zero+Adv+While(+yken[yken])',
            u'mavi(mavi)+Adj+Noun+Zero+A3sg+Pnon+Nom+Adj+Equ(cA[ce])+Verb+Zero+Adv+While(+yken[yken])',
            u'mavi(mavi)+Adj+Noun+Zero+A3sg+Pnon+Nom+Adv+InTermsOf(cA[ce])+Verb+Zero+Adv+While(+yken[yken])',
            u'mavi(mavi)+Adj+Noun+Zero+A3sg+Pnon+Nom+Adv+By(cA[ce])+Verb+Zero+Adv+While(+yken[yken])',
            u'mavi(mavi)+Adj+Adj+Equ(cA[ce])+Verb+Zero+Adv+While(+yken[yken])+Verb+Zero+Pres+A3sg',
            u'mavi(mavi)+Adj+Adj+Quite(cA[ce])+Verb+Zero+Adv+While(+yken[yken])+Verb+Zero+Pres+A3sg',
            u'mavi(mavi)+Adj+Adv+Ly(cA[ce])+Verb+Zero+Adv+While(+yken[yken])+Verb+Zero+Pres+A3sg',
            u'mavi(mavi)+Adj+Adj+Equ(cA[ce])+Noun+Zero+A3sg+Pnon+Nom+Verb+Zero+Adv+While(+yken[yken])',
            u'mavi(mavi)+Adj+Adj+Quite(cA[ce])+Noun+Zero+A3sg+Pnon+Nom+Verb+Zero+Adv+While(+yken[yken])',
            u'mavi(mavi)+Adj+Noun+Zero+A3sg+Pnon+Nom+Adj+Equ(cA[ce])+Adv+Zero+Verb+Zero+Adv+While(+yken[yken])',
            u'mavi(mavi)+Adj+Adj+Equ(cA[ce])+Adv+Zero+Verb+Zero+Adv+While(+yken[yken])+Verb+Zero+Pres+A3sg',
            u'mavi(mavi)+Adj+Adj+Quite(cA[ce])+Adv+Zero+Verb+Zero+Adv+While(+yken[yken])+Verb+Zero+Pres+A3sg',
            u'mavi(mavi)+Adj+Noun+Zero+A3sg+Pnon+Nom+Adj+Equ(cA[ce])+Verb+Zero+Adv+While(+yken[yken])+Verb+Zero+Pres+A3sg',
            u'mavi(mavi)+Adj+Noun+Zero+A3sg+Pnon+Nom+Adv+InTermsOf(cA[ce])+Verb+Zero+Adv+While(+yken[yken])+Verb+Zero+Pres+A3sg',
            u'mavi(mavi)+Adj+Noun+Zero+A3sg+Pnon+Nom+Adv+By(cA[ce])+Verb+Zero+Adv+While(+yken[yken])+Verb+Zero+Pres+A3sg',
            u'mavi(mavi)+Adj+Noun+Zero+A3sg+Pnon+Nom+Adj+Equ(cA[ce])+Noun+Zero+A3sg+Pnon+Nom+Verb+Zero+Adv+While(+yken[yken])',
            u'mavi(mavi)+Adj+Adj+Equ(cA[ce])+Noun+Zero+A3sg+Pnon+Nom+Verb+Zero+Adv+While(+yken[yken])+Verb+Zero+Pres+A3sg',
            u'mavi(mavi)+Adj+Adj+Quite(cA[ce])+Noun+Zero+A3sg+Pnon+Nom+Verb+Zero+Adv+While(+yken[yken])+Verb+Zero+Pres+A3sg',
            u'mavi(mavi)+Adj+Noun+Zero+A3sg+Pnon+Nom+Adj+Equ(cA[ce])+Adv+Zero+Verb+Zero+Adv+While(+yken[yken])+Verb+Zero+Pres+A3sg',
            u'mavi(mavi)+Adj+Noun+Zero+A3sg+Pnon+Nom+Adj+Equ(cA[ce])+Noun+Zero+A3sg+Pnon+Nom+Verb+Zero+Adv+While(+yken[yken])+Verb+Zero+Pres+A3sg')
        self.assert_parse_correct_for_verb(u'seninken',            u'sen(sen)+Pron+Pers+A2sg+Pnon+Gen(in[in])+Verb+Zero+Adv+While(+yken[ken])', u'sen(sen)+Pron+Pers+A2sg+Pnon+Gen(in[in])+Verb+Zero+Adv+While(+yken[ken])+Verb+Zero+Pres+A3sg')
        self.assert_parse_correct_for_verb(u'onlarken',            u'o(o)+Pron+Pers+A3pl(nlar[nlar])+Pnon+Nom+Verb+Zero+Adv+While(+yken[ken])', u'o(o)+Pron+Demons+A3pl(nlar[nlar])+Pnon+Nom+Verb+Zero+Adv+While(+yken[ken])', u'o(o)+Pron+Pers+A3pl(nlar[nlar])+Pnon+Nom+Verb+Zero+Adv+While(+yken[ken])+Verb+Zero+Pres+A3sg', u'o(o)+Pron+Demons+A3pl(nlar[nlar])+Pnon+Nom+Verb+Zero+Adv+While(+yken[ken])+Verb+Zero+Pres+A3sg')

    def test_should_parse_verb_degil(self):
        self.assert_parse_correct_for_verb(u'değil',               u'de\u011fil(de\u011fil)+Conj', u'değil(değil)+Verb+Pres+A3sg')
        self.assert_parse_correct_for_verb(u'değilim',             u'değil(değil)+Verb+Pres+A1sg(+yIm[im])')
        self.assert_parse_correct_for_verb(u'değilsin',            u'değil(değil)+Verb+Pres+A2sg(sIn[sin])')
        self.assert_parse_correct_for_verb(u'değildik',            u'değil(değil)+Verb+Past(+ydI[di])+A1pl(k[k])')
        self.assert_parse_correct_for_verb(u'değilmişsiniz',       u'değil(değil)+Verb+Narr(+ymIş[miş])+A2pl(sInIz[siniz])')
        self.assert_parse_correct_for_verb(u'değildiler',          u'değil(değil)+Verb+Past(+ydI[di])+A3pl(lAr[ler])')
        self.assert_parse_correct_for_verb(u'değilseler',          u'değil(değil)+Verb+Cond(+ysA[se])+A3pl(lAr[ler])')
        #TODO: degillerdi, degillerse, degillermis

    def test_should_parse_verbs_with_explicit_copula(self):
        # remove some roots to keep tests simple
        self.cloned_root_map['on'] = []
        self.cloned_root_map['gelecek'] = []
        self.cloned_root_map['ben'] = filter(lambda root : root.lexeme.syntactic_category==SyntacticCategory.PRONOUN, self.cloned_root_map['ben'])

        self.assert_parse_correct_for_verb(u'elmadır',             u'elma(elma)+Noun+A3sg+Pnon+Nom+Verb+Zero+Pres+A3sg+Cop(dIr[dır])')
        self.assert_parse_correct_for_verb(u'müdürdür',            u'müdür(müdür)+Noun+A3sg+Pnon+Nom+Verb+Zero+Pres+A3sg+Cop(dIr[dür])')
        self.assert_parse_correct_for_verb(u'zilidir',             u'zil(zil)+Noun+A3sg+Pnon+Acc(+yI[i])+Verb+Zero+Pres+A3sg+Cop(dIr[dir])', u'zil(zil)+Noun+A3sg+P3sg(+sI[i])+Nom+Verb+Zero+Pres+A3sg+Cop(dIr[dir])')
        self.assert_parse_correct_for_verb(u'mavidir',             u'mavi(mavi)+Adj+Verb+Zero+Pres+A3sg+Cop(dIr[dir])', u'mavi(mavi)+Adj+Adv+Zero+Verb+Zero+Pres+A3sg+Cop(dIr[dir])', u'mavi(mavi)+Adj+Noun+Zero+A3sg+Pnon+Nom+Verb+Zero+Pres+A3sg+Cop(dIr[dir])')
        self.assert_parse_correct_for_verb(u'mavisindir',          u'mavi(mavi)+Adj+Verb+Zero+Pres+A2sg(sIn[sin])+Cop(dIr[dir])', u'mavi(mavi)+Adj+Adv+Zero+Verb+Zero+Pres+A2sg(sIn[sin])+Cop(dIr[dir])', u'mavi(mavi)+Adj+Noun+Zero+A3sg+Pnon+Nom+Verb+Zero+Pres+A2sg(sIn[sin])+Cop(dIr[dir])')
        self.assert_parse_correct_for_verb(u'benimdir',            u'ben(ben)+Pron+Pers+A1sg+Pnon+Nom+Verb+Zero+Pres+A1sg(+yIm[im])+Cop(dIr[dir])', u'ben(ben)+Pron+Pers+A1sg+Pnon+Gen(im[im])+Verb+Zero+Pres+A3sg+Cop(dIr[dir])')
        self.assert_parse_correct_for_verb(u'onlardır',            u'o(o)+Pron+Pers+A3pl(nlar[nlar])+Pnon+Nom+Verb+Zero+Pres+A3sg+Cop(dIr[dır])', u'o(o)+Pron+Demons+A3pl(nlar[nlar])+Pnon+Nom+Verb+Zero+Pres+A3sg+Cop(dIr[dır])')
        self.assert_parse_correct_for_verb(u'benimledir',          u'ben(ben)+Pron+Pers+A1sg+Pnon+Ins(imle[imle])+Verb+Zero+Pres+A3sg+Cop(dIr[dir])')
        self.assert_parse_correct_for_verb(u'sıcakçayımdır',
            u'sıcak(sıcak)+Adj+Adj+Equ(cA[ça])+Verb+Zero+Pres+A1sg(+yIm[yım])+Cop(dIr[dır])',
            u'sıcak(sıcak)+Adj+Adj+Quite(cA[ça])+Verb+Zero+Pres+A1sg(+yIm[yım])+Cop(dIr[dır])',
            u'sıcak(sıcak)+Adj+Adv+Ly(cA[ça])+Verb+Zero+Pres+A1sg(+yIm[yım])+Cop(dIr[dır])',
            u'sıcak(sıcak)+Adj+Adj+Equ(cA[ça])+Adv+Zero+Verb+Zero+Pres+A1sg(+yIm[yım])+Cop(dIr[dır])',
            u'sıcak(sıcak)+Adj+Adj+Quite(cA[ça])+Adv+Zero+Verb+Zero+Pres+A1sg(+yIm[yım])+Cop(dIr[dır])',
            u'sıcak(sıcak)+Adj+Noun+Zero+A3sg+Pnon+Nom+Adj+Equ(cA[ça])+Verb+Zero+Pres+A1sg(+yIm[yım])+Cop(dIr[dır])',
            u'sıcak(sıcak)+Adj+Noun+Zero+A3sg+Pnon+Nom+Adv+InTermsOf(cA[ça])+Verb+Zero+Pres+A1sg(+yIm[yım])+Cop(dIr[dır])',
            u'sıcak(sıcak)+Adj+Noun+Zero+A3sg+Pnon+Nom+Adv+By(cA[ça])+Verb+Zero+Pres+A1sg(+yIm[yım])+Cop(dIr[dır])',
            u'sıcak(sıcak)+Adj+Adj+Equ(cA[ça])+Noun+Zero+A3sg+Pnon+Nom+Verb+Zero+Pres+A1sg(+yIm[yım])+Cop(dIr[dır])',
            u'sıcak(sıcak)+Adj+Adj+Quite(cA[ça])+Noun+Zero+A3sg+Pnon+Nom+Verb+Zero+Pres+A1sg(+yIm[yım])+Cop(dIr[dır])',
            u'sıcak(sıcak)+Adj+Noun+Zero+A3sg+Pnon+Nom+Adj+Equ(cA[ça])+Adv+Zero+Verb+Zero+Pres+A1sg(+yIm[yım])+Cop(dIr[dır])',
            u'sıcak(sıcak)+Adj+Noun+Zero+A3sg+Pnon+Nom+Adj+Equ(cA[ça])+Noun+Zero+A3sg+Pnon+Nom+Verb+Zero+Pres+A1sg(+yIm[yım])+Cop(dIr[dır])'
        )
        self.assert_parse_correct_for_verb(u'gelmektedir',         u'gel(gelmek)+Verb+Pos+Prog(mAktA[mekte])+A3sg+Cop(dIr[dir])', u'gel(gelmek)+Verb+Pos+Noun+Inf(mAk[mek])+A3sg+Pnon+Loc(dA[te])+Verb+Zero+Pres+A3sg+Cop(dIr[dir])')
        self.assert_parse_correct_for_verb(u'geliyorlardır',       u'gel(gelmek)+Verb+Pos+Prog(Iyor[iyor])+A3pl(lAr[lar])+Cop(dIr[dır])')
        self.assert_parse_correct_for_verb(u'gelmiştir',           u'gel(gelmek)+Verb+Pos+Narr(mIş[miş])+A3sg+Cop(dIr[tir])', u'gel(gelmek)+Verb+Pos+Narr(mIş[miş])+Adj+Zero+Verb+Zero+Pres+A3sg+Cop(dIr[tir])', u'gel(gelmek)+Verb+Pos+Narr(mIş[miş])+Adj+Zero+Adv+Zero+Verb+Zero+Pres+A3sg+Cop(dIr[tir])', u'gel(gelmek)+Verb+Pos+Narr(mIş[miş])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom+Verb+Zero+Pres+A3sg+Cop(dIr[tir])')
        self.assert_parse_correct_for_verb(u'geleceksinizdir',     u'gel(gelmek)+Verb+Pos+Fut(+yAcAk[ecek])+A2pl(sInIz[siniz])+Cop(dIr[dir])', u'gel(gelmek)+Verb+Pos+Adj+FutPart(+yAcAk[ecek])+Pnon+Verb+Zero+Pres+A2pl(sInIz[siniz])+Cop(dIr[dir])', u'gel(gelmek)+Verb+Pos+Fut(+yAcAk[ecek])+Adj+Zero+Verb+Zero+Pres+A2pl(sInIz[siniz])+Cop(dIr[dir])', u'gel(gelmek)+Verb+Pos+Fut(+yAcAk[ecek])+Adj+Zero+Adv+Zero+Verb+Zero+Pres+A2pl(sInIz[siniz])+Cop(dIr[dir])', u'gel(gelmek)+Verb+Pos+Noun+FutPart(+yAcAk[ecek])+A3sg+Pnon+Nom+Verb+Zero+Pres+A2pl(sInIz[siniz])+Cop(dIr[dir])', u'gel(gelmek)+Verb+Pos+Fut(+yAcAk[ecek])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom+Verb+Zero+Pres+A2pl(sInIz[siniz])+Cop(dIr[dir])')
        self.assert_parse_correct_for_verb(u'gelmelilerdir',
            u'gel(gelmek)+Verb+Pos+Neces(mAlI![meli])+A3pl(lAr[ler])+Cop(dIr[dir])',
            u'gel(gelmek)+Verb+Pos+Noun+Inf(mA[me])+A3sg+Pnon+Nom+Adj+With(lI[li])+Verb+Zero+Pres+A3pl(lAr[ler])+Cop(dIr[dir])',
            u'gel(gelmek)+Verb+Pos+Noun+Inf(mA[me])+A3sg+Pnon+Nom+Adj+With(lI[li])+Adv+Zero+Verb+Zero+Pres+A3pl(lAr[ler])+Cop(dIr[dir])',
            u'gel(gelmek)+Verb+Pos+Noun+Inf(mA[me])+A3sg+Pnon+Nom+Adj+With(lI[li])+Noun+Zero+A3sg+Pnon+Nom+Verb+Zero+Pres+A3pl(lAr[ler])+Cop(dIr[dir])',
            u'gel(gelmek)+Verb+Pos+Noun+Inf(mA[me])+A3sg+Pnon+Nom+Adj+With(lI[li])+Noun+Zero+A3pl(lAr[ler])+Pnon+Nom+Verb+Zero+Pres+A3sg+Cop(dIr[dir])'
        )
        self.assert_parse_correct_for_verb(u'değildir',            u'değil(değil)+Verb+Pres+A3sg+Cop(dIr[dir])')
        self.assert_parse_correct_for_verb(u'değillerdir',         u'değil(değil)+Verb+Pres+A3pl(lAr[ler])+Cop(dIr[dir])')
        self.assert_parse_correct_for_verb(u'mıdır',               u'mı(mı)+Ques+Pres+A3sg+Cop(dIr[dır])')
        self.assert_parse_correct_for_verb(u'mıyımdır',            u'mı(mı)+Ques+Pres+A1sg(yım[yım])+Cop(dIr[dır])')

    def test_should_parse_adjectives_as_adverbs(self):
        self.assert_parse_exists(u'mavi',                         u'mavi(mavi)+Adj+Adv+Zero')
        self.assert_parse_exists(u'yapan',                        u'yap(yapmak)+Verb+Pos+Adj+PresPart(+yAn[an])+Adv+Zero')
        self.assert_parse_exists(u'kesici',                       u'kes(kesmek)+Verb+Pos+Adj+Agt(+yIcI[ici])+Adv+Zero')
        self.assert_parse_exists(u'pembemsi',                     u'pembe(pembe)+Adj+Adj+JustLike(+ImsI[msi])+Adv+Zero')
        self.assert_parse_exists(u'delice',                       u'deli(deli)+Adj+Adj+Equ(cA[ce])+Adv+Zero')

    def test_should_parse_pronoun_tenses(self):
        # remove some roots to make the test simple
        self.cloned_root_map[u'bend'] = []
        self.cloned_root_map[u'kimi'] = []
        self.cloned_root_map[u'kimse'] = []
        self.cloned_root_map[u'ben'] = filter(lambda root : root.lexeme.syntactic_category==SyntacticCategory.PRONOUN, self.cloned_root_map[u'ben'])
        self.cloned_root_map[u'ban'] = filter(lambda root : root.lexeme.syntactic_category==SyntacticCategory.PRONOUN, self.cloned_root_map[u'ban'])
        self.cloned_root_map[u'san'] = filter(lambda root : root.lexeme.syntactic_category==SyntacticCategory.PRONOUN, self.cloned_root_map[u'san'])
        self.cloned_root_map[u'biz'] = filter(lambda root : root.lexeme.syntactic_category==SyntacticCategory.PRONOUN, self.cloned_root_map[u'biz'])

        self.assert_parse_exists(u'benim',              u'ben(ben)+Pron+Pers+A1sg+Pnon+Nom+Verb+Zero+Pres+A1sg(+yIm[im])')
        self.assert_parse_correct_for_verb(u'bendim',             u'ben(ben)+Pron+Pers+A1sg+Pnon+Nom+Verb+Zero+Past(+ydI[di])+A1sg(m[m])')
        self.assert_parse_correct_for_verb(u'benmişim',           u'ben(ben)+Pron+Pers+A1sg+Pnon+Nom+Verb+Zero+Narr(+ymIş[miş])+A1sg(+yIm[im])')

        self.assert_parse_correct_for_verb(u'bensem',             u'ben(ben)+Pron+Pers+A1sg+Pnon+Nom+Verb+Zero+Cond(+ysA[se])+A1sg(m[m])')
        self.assert_parse_correct_for_verb(u'bense',              u'ben(ben)+Pron+Pers+A1sg+Pnon+Nom+Verb+Zero+Cond(+ysA[se])+A3sg')
        self.assert_parse_correct_for_verb(u'bendiyse',           u'ben(ben)+Pron+Pers+A1sg+Pnon+Nom+Verb+Zero+Past(+ydI[di])+Cond(+ysA[yse])+A3sg')
#        self.assert_parse_correct_for_verb(u'bendimse',           u'xxxx')   TODO
        self.assert_parse_correct_for_verb(u'bendiysem',          u'ben(ben)+Pron+Pers+A1sg+Pnon+Nom+Verb+Zero+Past(+ydI[di])+Cond(+ysA[yse])+A1sg(m[m])')
        self.assert_parse_correct_for_verb(u'benmişsem',          u'ben(ben)+Pron+Pers+A1sg+Pnon+Nom+Verb+Zero+Narr(+ymIş[miş])+Cond(+ysA[se])+A1sg(m[m])')

        self.assert_parse_correct_for_verb(u'beniyse',            u'ben(ben)+Pron+Pers+A1sg+Pnon+Acc(i[i])+Verb+Zero+Cond(+ysA[yse])+A3sg')
        self.assert_parse_correct_for_verb(u'banaymışsa',         u'ban(ben)+Pron+Pers+A1sg+Pnon+Dat(a[a])+Verb+Zero+Narr(+ymIş[ymış])+Cond(+ysA[sa])+A3sg')
        self.assert_parse_correct_for_verb(u'bendeymişseler',     u'ben(ben)+Pron+Pers+A1sg+Pnon+Loc(de[de])+Verb+Zero+Narr(+ymIş[ymiş])+Cond(+ysA[se])+A3pl(lAr[ler])')
        self.assert_parse_correct_for_verb(u'bendendiyse',        u'ben(ben)+Pron+Pers+A1sg+Pnon+Abl(den[den])+Verb+Zero+Past(+ydI[di])+Cond(+ysA[yse])+A3sg')
        self.assert_parse_correct_for_verb(u'benimleydiysen',     u'ben(ben)+Pron+Pers+A1sg+Pnon+Ins(imle[imle])+Verb+Zero+Past(+ydI[ydi])+Cond(+ysA[yse])+A2sg(n[n])')
        self.assert_parse_correct_for_verb(u'benimleymişseler',   u'ben(ben)+Pron+Pers+A1sg+Pnon+Ins(imle[imle])+Verb+Zero+Narr(+ymIş[ymiş])+Cond(+ysA[se])+A3pl(lAr[ler])')
#        self.assert_parse_correct_for_verb(u'benimleymişlerse',   u'xxxx')  TODO

        self.assert_parse_correct_for_verb(u'kimim',              u'kim(kim)+Pron+Ques+A3sg+P1sg(+Im[im])+Nom', u'kim(kim)+Pron+Ques+A3sg+Pnon+Nom+Verb+Zero+Pres+A1sg(+yIm[im])', u'kim(kim)+Pron+Ques+A3sg+P1sg(+Im[im])+Nom+Verb+Zero+Pres+A3sg')
        self.assert_parse_correct_for_verb(u'kimdim',             u'kim(kim)+Pron+Ques+A3sg+Pnon+Nom+Verb+Zero+Past(+ydI[di])+A1sg(m[m])')
        self.assert_parse_correct_for_verb(u'kimmişim',           u'kim(kim)+Pron+Ques+A3sg+Pnon+Nom+Verb+Zero+Narr(+ymIş[miş])+A1sg(+yIm[im])')

        self.assert_parse_correct_for_verb(u'kimsem',             u'kim(kim)+Pron+Ques+A3sg+Pnon+Nom+Verb+Zero+Cond(+ysA[se])+A1sg(m[m])')
        self.assert_parse_correct_for_verb(u'kimse',              u'kim(kim)+Pron+Ques+A3sg+Pnon+Nom+Verb+Zero+Cond(+ysA[se])+A3sg')
        self.assert_parse_correct_for_verb(u'kimdiyse',           u'kim(kim)+Pron+Ques+A3sg+Pnon+Nom+Verb+Zero+Past(+ydI[di])+Cond(+ysA[yse])+A3sg')
#        self.assert_parse_correct_for_verb(u'kimdimse',           u'xxxx') TODO
        self.assert_parse_correct_for_verb(u'kimdiysem',          u'kim(kim)+Pron+Ques+A3sg+Pnon+Nom+Verb+Zero+Past(+ydI[di])+Cond(+ysA[yse])+A1sg(m[m])')
        self.assert_parse_correct_for_verb(u'kimmişsem',          u'kim(kim)+Pron+Ques+A3sg+Pnon+Nom+Verb+Zero+Narr(+ymIş[miş])+Cond(+ysA[se])+A1sg(m[m])')

        self.assert_parse_correct_for_verb(u'kimiyse',            u'kim(kim)+Pron+Ques+A3sg+Pnon+Acc(+yI[i])+Verb+Zero+Cond(+ysA[yse])+A3sg', u'kim(kim)+Pron+Ques+A3sg+P3sg(+sI[i])+Nom+Verb+Zero+Cond(+ysA[yse])+A3sg')
        self.assert_parse_correct_for_verb(u'kimeymişse',         u'kim(kim)+Pron+Ques+A3sg+Pnon+Dat(+yA[e])+Verb+Zero+Narr(+ymIş[ymiş])+Cond(+ysA[se])+A3sg')
        self.assert_parse_correct_for_verb(u'kimdeymişse',        u'kim(kim)+Pron+Ques+A3sg+Pnon+Loc(dA[de])+Verb+Zero+Narr(+ymIş[ymiş])+Cond(+ysA[se])+A3sg')
        self.assert_parse_correct_for_verb(u'kimdendiyse',        u'kim(kim)+Pron+Ques+A3sg+Pnon+Abl(dAn[den])+Verb+Zero+Past(+ydI[di])+Cond(+ysA[yse])+A3sg')
        self.assert_parse_correct_for_verb(u'kimlerdendiyse',     u'kim(kim)+Pron+Ques+A3pl(lAr[ler])+Pnon+Abl(dAn[den])+Verb+Zero+Past(+ydI[di])+Cond(+ysA[yse])+A3sg')
        self.assert_parse_correct_for_verb(u'kimimleydiysen',     u'kim(kim)+Pron+Ques+A3sg+P1sg(+Im[im])+Ins(+ylA[le])+Verb+Zero+Past(+ydI[ydi])+Cond(+ysA[yse])+A2sg(n[n])')
#        self.assert_parse_correct_for_verb(u'kimimleymişlerse',   u'xxxx') TODO

if __name__ == '__main__':
    unittest.main()
