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
from trnltk.morphology.contextless.parser.parser import ContextlessMorphologicalParser, logger as parser_logger
from trnltk.morphology.contextless.parser.rootfinder import  WordRootFinder
from trnltk.morphology.contextless.parser.suffixapplier import logger as suffix_applier_logger
from trnltk.morphology.morphotactics.predefinedpaths import PredefinedPaths
from trnltk.morphology.morphotactics.basicsuffixgraph import BasicSuffixGraph

class ParserTestWithBasicGraph(ParserTest):

    @classmethod
    def setUpClass(cls):
        super(ParserTestWithBasicGraph, cls).setUpClass()
        all_roots = []

        lexemes = LexiconLoader.load_from_file(os.path.join(os.path.dirname(__file__), '../../../../resources/master_dictionary.txt'))
        for di in lexemes:
            all_roots.extend(RootGenerator.generate(di))

        cls._org_root_map = (RootMapGenerator()).generate(all_roots)


    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        parser_logger.setLevel(logging.INFO)
        suffix_applier_logger.setLevel(logging.INFO)

        suffix_graph = BasicSuffixGraph()
        suffix_graph.initialize()

        self.cloned_root_map = copy(self._org_root_map)
        predefined_paths = PredefinedPaths(self.cloned_root_map, suffix_graph)
        predefined_paths.create_predefined_paths()

        word_root_finder = WordRootFinder(self.cloned_root_map)

        self.parser = ContextlessMorphologicalParser(suffix_graph, predefined_paths, [word_root_finder])

    def test_should_parse_noun_cases(self):
        self.assert_parse_correct(u'sokak',            u'sokak(sokak)+Noun+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'dikkatle',         u'dikkat(dikkat)+Noun+A3sg+Pnon+Ins(+ylA[le])')

        self.assert_parse_correct(u'kapıyı',           u'kapı(kapı)+Noun+A3sg+Pnon+Acc(+yI[yı])')
        self.assert_parse_correct(u'kapıya',           u'kapı(kapı)+Noun+A3sg+Pnon+Dat(+yA[ya])')
        self.assert_parse_correct(u'kapıda',           u'kapı(kapı)+Noun+A3sg+Pnon+Loc(dA[da])')
        self.assert_parse_correct(u'kapıdan',          u'kapı(kapı)+Noun+A3sg+Pnon+Abl(dAn[dan])')
        self.assert_parse_correct(u'dayının',          u'dayı(dayı)+Noun+A3sg+Pnon+Gen(+nIn[nın])', u'dayı(dayı)+Noun+A3sg+P2sg(+In[n])+Gen(+nIn[ın])', u'dayı(dayı)+Adj+Noun+Zero+A3sg+Pnon+Gen(+nIn[nın])', u'dayı(dayı)+Adj+Noun+Zero+A3sg+P2sg(+In[n])+Gen(+nIn[ın])')
        self.assert_parse_correct(u'sokağın',          u'sokağ(sokak)+Noun+A3sg+Pnon+Gen(+nIn[ın])', u'sokağ(sokak)+Noun+A3sg+P2sg(+In[ın])+Nom')
        self.assert_parse_correct(u'sokakla',          u'sokak(sokak)+Noun+A3sg+Pnon+Ins(+ylA[la])')

        self.assert_parse_correct(u'sokaklar',         u'sokak(sokak)+Noun+A3pl(lAr[lar])+Pnon+Nom')
        self.assert_parse_correct(u'sokakları',        u'sokak(sokak)+Noun+A3pl(lAr[lar])+Pnon+Acc(+yI[ı])', u'sokak(sokak)+Noun+A3pl(lAr[lar])+P3sg(+sI[ı])+Nom', u'sokak(sokak)+Noun+A3pl(lAr[lar])+P3pl(I![ı])+Nom', u'sokak(sokak)+Noun+A3sg+P3pl(lArI![ları])+Nom')
        self.assert_parse_correct(u'sokaklara',        u'sokak(sokak)+Noun+A3pl(lAr[lar])+Pnon+Dat(+yA[a])')
        self.assert_parse_correct(u'sokaklarda',       u'sokak(sokak)+Noun+A3pl(lAr[lar])+Pnon+Loc(dA[da])')
        self.assert_parse_correct(u'sokaklardan',      u'sokak(sokak)+Noun+A3pl(lAr[lar])+Pnon+Abl(dAn[dan])')
        self.assert_parse_correct(u'sokakların',       u'sokak(sokak)+Noun+A3pl(lAr[lar])+Pnon+Gen(+nIn[ın])', u'sokak(sokak)+Noun+A3pl(lAr[lar])+P2sg(+In[ın])+Nom')
        self.assert_parse_correct(u'sokaklarla',       u'sokak(sokak)+Noun+A3pl(lAr[lar])+Pnon+Ins(+ylA[la])')


    def test_should_parse_noun_to_noun_derivations(self):
        self.assert_parse_correct(u'kitapçık',         u'kitap(kitap)+Noun+A3sg+Pnon+Nom+Noun+Dim(cIk[\xe7\u0131k])+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'kitapçığa',        u'kitap(kitap)+Noun+A3sg+Pnon+Nom+Noun+Dim(cIk[\xe7\u0131\u011f])+A3sg+Pnon+Dat(+yA[a])')
        self.assert_parse_correct(u'parçacık',         u'par\xe7a(par\xe7a)+Noun+A3sg+Pnon+Nom+Noun+Dim(cIk[c\u0131k])+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'parçacıklarla',    u'par\xe7a(par\xe7a)+Noun+A3sg+Pnon+Nom+Noun+Dim(cIk[c\u0131k])+A3pl(lAr[lar])+Pnon+Ins(+ylA[la])')
        self.assert_not_parsable(u'parçacıkcık')


    def test_should_parse_noun_to_adjective_derivations(self):
        self.cloned_root_map[u'kut'] = []

        self.assert_parse_correct(u'kutulu',           u'kutu(kutu)+Noun+A3sg+Pnon+Nom+Adj+With(lI[lu])', u'kutu(kutu)+Noun+A3sg+Pnon+Nom+Adj+With(lI[lu])+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'kutusuz',          u'kutu(kutu)+Noun+A3sg+Pnon+Nom+Adj+Without(sIz[suz])', u'kutu(kutu)+Noun+A3sg+Pnon+Nom+Adj+Without(sIz[suz])+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'kutumsu',          u'kutu(kutu)+Noun+A3sg+Pnon+Nom+Adj+JustLike(+ImsI[msu])', u'kutu(kutu)+Noun+A3sg+Pnon+Nom+Adj+JustLike(+ImsI[msu])+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'telefonumsu',      u'telefon(telefon)+Noun+A3sg+Pnon+Nom+Adj+JustLike(+ImsI[umsu])', u'telefon(telefon)+Noun+A3sg+Pnon+Nom+Adj+JustLike(+ImsI[umsu])+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'meleğimsi',        u'meleğ(melek)+Noun+A3sg+Pnon+Nom+Adj+JustLike(+ImsI[imsi])', u'meleğ(melek)+Noun+A3sg+Pnon+Nom+Adj+JustLike(+ImsI[imsi])+Noun+Zero+A3sg+Pnon+Nom')

        self.assert_parse_correct(u'korucu',           u'koru(koru)+Noun+A3sg+Pnon+Nom+Adj+Agt(cI[cu])', u'koru(koru)+Noun+A3sg+Pnon+Nom+Adj+Agt(cI[cu])+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'korucuyu',         u'koru(koru)+Noun+A3sg+Pnon+Nom+Adj+Agt(cI[cu])+Noun+Zero+A3sg+Pnon+Acc(+yI[yu])')
        self.assert_parse_correct(u'korucuya',         u'koru(koru)+Noun+A3sg+Pnon+Nom+Adj+Agt(cI[cu])+Noun+Zero+A3sg+Pnon+Dat(+yA[ya])')
        self.assert_parse_correct(u'korucuda',         u'koru(koru)+Noun+A3sg+Pnon+Nom+Adj+Agt(cI[cu])+Noun+Zero+A3sg+Pnon+Loc(dA[da])')
        self.assert_parse_correct(u'korucudan',        u'koru(koru)+Noun+A3sg+Pnon+Nom+Adj+Agt(cI[cu])+Noun+Zero+A3sg+Pnon+Abl(dAn[dan])')
        self.assert_parse_correct(u'korucunun',        u'koru(koru)+Noun+A3sg+Pnon+Nom+Adj+Agt(cI[cu])+Noun+Zero+A3sg+Pnon+Gen(+nIn[nun])', u'koru(koru)+Noun+A3sg+Pnon+Nom+Adj+Agt(cI[cu])+Noun+Zero+A3sg+P2sg(+In[n])+Gen(+nIn[un])')
        self.assert_parse_correct(u'korucuyla',        u'koru(koru)+Noun+A3sg+Pnon+Nom+Adj+Agt(cI[cu])+Noun+Zero+A3sg+Pnon+Ins(+ylA[yla])')

    def test_should_parse_noun_to_verb_derivations(self):
        #heyecanlan
        pass


    def test_should_parse_positive_verb_tenses(self):
        self.assert_parse_correct(u'yaparım',           u'yap(yapmak)+Verb+Pos+Aor(+Ar[ar])+A1sg(+Im[ım])', u'yap(yapmak)+Verb+Pos+Aor(+Ar[ar])+Adj+Zero+Noun+Zero+A3sg+P1sg(+Im[ım])+Nom')
        self.assert_parse_correct(u'yaparsın',          u'yap(yapmak)+Verb+Pos+Aor(+Ar[ar])+A2sg(sIn[sın])')
        self.assert_parse_correct(u'yapar',             u'yap(yapmak)+Verb+Pos+Aor(+Ar[ar])+A3sg', u'yap(yapmak)+Verb+Pos+Aor(+Ar[ar])+Adj+Zero', u'yap(yapmak)+Verb+Pos+Aor(+Ar[ar])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'yaparız',           u'yap(yapmak)+Verb+Pos+Aor(+Ar[ar])+A1pl(+Iz[ız])')

        self.assert_parse_correct(u'yapıyorum',         u'yap(yapmak)+Verb+Pos+Prog(Iyor[ıyor])+A1sg(+Im[um])')
        self.assert_parse_correct(u'yapıyorsun',        u'yap(yapmak)+Verb+Pos+Prog(Iyor[ıyor])+A2sg(sIn[sun])')
        self.assert_parse_correct(u'yapıyor',           u'yap(yapmak)+Verb+Pos+Prog(Iyor[ıyor])+A3sg')
        self.assert_parse_correct(u'yapıyoruz',         u'yap(yapmak)+Verb+Pos+Prog(Iyor[ıyor])+A1pl(+Iz[uz])')

        self.assert_parse_correct(u'yapmaktayım',       u'yap(yapmak)+Verb+Pos+Prog(mAktA[makta])+A1sg(yIm[yım])')
        self.assert_parse_correct(u'yapmaktasın',       u'yap(yapmak)+Verb+Pos+Prog(mAktA[makta])+A2sg(sIn[sın])')
        self.assert_parse_correct(u'yapmakta',          u'yap(yapmak)+Verb+Pos+Prog(mAktA[makta])+A3sg', u'yap(yapmak)+Verb+Pos+Noun+Inf(mAk[mak])+A3sg+Pnon+Loc(dA[ta])')
        self.assert_parse_correct(u'yapmaktayız',       u'yap(yapmak)+Verb+Pos+Prog(mAktA[makta])+A1pl(yIz[yız])')

        self.assert_parse_correct(u'yapacağım',         u'yap(yapmak)+Verb+Pos+Fut(+yAcAk[acağ])+A1sg(+Im[ım])', u'yap(yapmak)+Verb+Pos+Adj+FutPart(+yAcAk[acağ])+P1sg(+Im[ım])', u'yap(yapmak)+Verb+Pos+Noun+FutPart(+yAcAk[acağ])+A3sg+P1sg(+Im[ım])+Nom', u'yap(yapmak)+Verb+Pos+Fut(+yAcAk[aca\u011f])+Adj+Zero+Noun+Zero+A3sg+P1sg(+Im[\u0131m])+Nom')
        self.assert_parse_correct(u'yapacaksın',        u'yap(yapmak)+Verb+Pos+Fut(+yAcAk[acak])+A2sg(sIn[sın])')
        self.assert_parse_correct(u'yapacak',           u'yap(yapmak)+Verb+Pos+Fut(+yAcAk[acak])+A3sg', u'yap(yapmak)+Verb+Pos+Adj+FutPart(+yAcAk[acak])+Pnon', u'yap(yapmak)+Verb+Pos+Fut(+yAcAk[acak])+Adj+Zero', u'yap(yapmak)+Verb+Pos+Noun+FutPart(+yAcAk[acak])+A3sg+Pnon+Nom', u'yap(yapmak)+Verb+Pos+Fut(+yAcAk[acak])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'yapacağız',         u'yap(yapmak)+Verb+Pos+Fut(+yAcAk[acağ])+A1pl(+Iz[ız])')

        self.assert_parse_correct(u'yaptım',            u'yap(yapmak)+Verb+Pos+Past(dI[tı])+A1sg(+Im[m])')
        self.assert_parse_correct(u'yaptın',            u'yap(yapmak)+Verb+Pos+Past(dI[tı])+A2sg(n[n])')
        self.assert_parse_correct(u'yaptı',             u'yap(yapmak)+Verb+Pos+Past(dI[tı])+A3sg')
        self.assert_parse_correct(u'yaptık',            u'yap(yapmak)+Verb+Pos+Past(dI[tı])+A1pl(k[k])', u'yap(yapmak)+Verb+Pos+Adj+PastPart(dIk[t\u0131k])+Pnon', u'yap(yapmak)+Verb+Pos+Noun+PastPart(dIk[t\u0131k])+A3sg+Pnon+Nom')

        self.assert_parse_correct(u'yapmışım',          u'yap(yapmak)+Verb+Pos+Narr(mIş[mış])+A1sg(+Im[ım])', u'yap(yapmak)+Verb+Pos+Narr(mIş[mış])+Adj+Zero+Noun+Zero+A3sg+P1sg(+Im[ım])+Nom')
        self.assert_parse_correct(u'yapmışsın',         u'yap(yapmak)+Verb+Pos+Narr(mIş[mış])+A2sg(sIn[sın])')
        self.assert_parse_correct(u'yapmış',            u'yap(yapmak)+Verb+Pos+Narr(mIş[mış])+A3sg', u'yap(yapmak)+Verb+Pos+Narr(mIş[mış])+Adj+Zero', u'yap(yapmak)+Verb+Pos+Narr(mIş[mış])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'yapmışız',          u'yap(yapmak)+Verb+Pos+Narr(mIş[mış])+A1pl(+Iz[ız])')

        self.assert_parse_correct(u'çeviririm',         u'çevir(çevirmek)+Verb+Pos+Aor(+Ir[ir])+A1sg(+Im[im])', u'çevir(çevirmek)+Verb+Pos+Aor(+Ir[ir])+Adj+Zero+Noun+Zero+A3sg+P1sg(+Im[im])+Nom')
        self.assert_parse_correct(u'çevirirsin',        u'çevir(çevirmek)+Verb+Pos+Aor(+Ir[ir])+A2sg(sIn[sin])')
        self.assert_parse_correct(u'çevirir',           u'çevir(çevirmek)+Verb+Pos+Aor(+Ir[ir])+A3sg', u'çevir(çevirmek)+Verb+Pos+Aor(+Ir[ir])+Adj+Zero', u'çevir(çevirmek)+Verb+Pos+Aor(+Ir[ir])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')

        self.assert_parse_correct(u'çeviriyorum',       u'çevir(çevirmek)+Verb+Pos+Prog(Iyor[iyor])+A1sg(+Im[um])')
        self.assert_parse_correct(u'çeviriyorsun',      u'çevir(çevirmek)+Verb+Pos+Prog(Iyor[iyor])+A2sg(sIn[sun])')
        self.assert_parse_correct(u'çeviriyor',         u'çevir(çevirmek)+Verb+Pos+Prog(Iyor[iyor])+A3sg')

        self.assert_parse_correct(u'çevirmekteyim',     u'çevir(çevirmek)+Verb+Pos+Prog(mAktA[mekte])+A1sg(yIm[yim])')
        self.assert_parse_correct(u'çevirmektesin',     u'çevir(çevirmek)+Verb+Pos+Prog(mAktA[mekte])+A2sg(sIn[sin])')
        self.assert_parse_correct(u'çevirmekte',        u'çevir(çevirmek)+Verb+Pos+Prog(mAktA[mekte])+A3sg', u'\xe7evir(\xe7evirmek)+Verb+Pos+Noun+Inf(mAk[mek])+A3sg+Pnon+Loc(dA[te])')

        self.assert_parse_correct(u'çevireceğim',       u'\xe7evir(\xe7evirmek)+Verb+Pos+Fut(+yAcAk[ece\u011f])+A1sg(+Im[im])', u'\xe7evir(\xe7evirmek)+Verb+Pos+Adj+FutPart(+yAcAk[ece\u011f])+P1sg(+Im[im])', u'\xe7evir(\xe7evirmek)+Verb+Pos+Noun+FutPart(+yAcAk[ece\u011f])+A3sg+P1sg(+Im[im])+Nom', u'\xe7evir(\xe7evirmek)+Verb+Pos+Fut(+yAcAk[ece\u011f])+Adj+Zero+Noun+Zero+A3sg+P1sg(+Im[im])+Nom')
        self.assert_parse_correct(u'çevireceksin',      u'çevir(çevirmek)+Verb+Pos+Fut(+yAcAk[ecek])+A2sg(sIn[sin])')
        self.assert_parse_correct(u'çevirecek',         u'\xe7evir(\xe7evirmek)+Verb+Pos+Fut(+yAcAk[ecek])+A3sg', u'\xe7evir(\xe7evirmek)+Verb+Pos+Adj+FutPart(+yAcAk[ecek])+Pnon', u'\xe7evir(\xe7evirmek)+Verb+Pos+Fut(+yAcAk[ecek])+Adj+Zero', u'\xe7evir(\xe7evirmek)+Verb+Pos+Noun+FutPart(+yAcAk[ecek])+A3sg+Pnon+Nom', u'\xe7evir(\xe7evirmek)+Verb+Pos+Fut(+yAcAk[ecek])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')

        self.assert_parse_correct(u'çevirdim',          u'çevir(çevirmek)+Verb+Pos+Past(dI[di])+A1sg(+Im[m])')
        self.assert_parse_correct(u'çevirdin',          u'çevir(çevirmek)+Verb+Pos+Past(dI[di])+A2sg(n[n])')
        self.assert_parse_correct(u'çevirdi',           u'çevir(çevirmek)+Verb+Pos+Past(dI[di])+A3sg')

        self.assert_parse_correct(u'çevirmişim',        u'çevir(çevirmek)+Verb+Pos+Narr(mIş[miş])+A1sg(+Im[im])', u'çevir(çevirmek)+Verb+Pos+Narr(mIş[miş])+Adj+Zero+Noun+Zero+A3sg+P1sg(+Im[im])+Nom')
        self.assert_parse_correct(u'çevirmişsin',       u'çevir(çevirmek)+Verb+Pos+Narr(mIş[miş])+A2sg(sIn[sin])')
        self.assert_parse_correct(u'çevirmiş',          u'çevir(çevirmek)+Verb+Pos+Narr(mIş[miş])+A3sg', u'çevir(çevirmek)+Verb+Pos+Narr(mIş[miş])+Adj+Zero', u'çevir(çevirmek)+Verb+Pos+Narr(mIş[miş])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')


        self.cloned_root_map[u'el'] = filter(lambda root : root.lexeme.lemma==u'elemek', self.cloned_root_map[u'el'])

        self.assert_parse_correct(u'elerim',            u'ele(elemek)+Verb+Pos+Aor(+Ir[r])+A1sg(+Im[im])', u'ele(elemek)+Verb+Pos+Aor(+Ar[r])+A1sg(+Im[im])', u'ele(elemek)+Verb+Pos+Aor(+Ir[r])+Adj+Zero+Noun+Zero+A3sg+P1sg(+Im[im])+Nom', u'ele(elemek)+Verb+Pos+Aor(+Ar[r])+Adj+Zero+Noun+Zero+A3sg+P1sg(+Im[im])+Nom')
        self.assert_parse_correct(u'elersin',           u'ele(elemek)+Verb+Pos+Aor(+Ir[r])+A2sg(sIn[sin])', u'ele(elemek)+Verb+Pos+Aor(+Ar[r])+A2sg(sIn[sin])')
        self.assert_parse_correct(u'eler',              u'ele(elemek)+Verb+Pos+Aor(+Ir[r])+A3sg', u'ele(elemek)+Verb+Pos+Aor(+Ar[r])+A3sg', u'ele(elemek)+Verb+Pos+Aor(+Ir[r])+Adj+Zero', u'ele(elemek)+Verb+Pos+Aor(+Ar[r])+Adj+Zero', u'ele(elemek)+Verb+Pos+Aor(+Ir[r])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom', u'ele(elemek)+Verb+Pos+Aor(+Ar[r])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')

        self.assert_parse_correct(u'eliyorum',          u'el(elemek)+Verb+Pos+Prog(Iyor[iyor])+A1sg(+Im[um])')
        self.assert_parse_correct(u'eliyorsun',         u'el(elemek)+Verb+Pos+Prog(Iyor[iyor])+A2sg(sIn[sun])')
        self.assert_parse_correct(u'eliyor',            u'el(elemek)+Verb+Pos+Prog(Iyor[iyor])+A3sg')

        self.assert_parse_correct(u'elemekteyim',       u'ele(elemek)+Verb+Pos+Prog(mAktA[mekte])+A1sg(yIm[yim])')
        self.assert_parse_correct(u'elemektesin',       u'ele(elemek)+Verb+Pos+Prog(mAktA[mekte])+A2sg(sIn[sin])')
        self.assert_parse_correct(u'elemekte',          u'ele(elemek)+Verb+Pos+Prog(mAktA[mekte])+A3sg', u'ele(elemek)+Verb+Pos+Noun+Inf(mAk[mek])+A3sg+Pnon+Loc(dA[te])')

        self.assert_parse_correct(u'eleyeceğim',        u'ele(elemek)+Verb+Pos+Fut(+yAcAk[yece\u011f])+A1sg(+Im[im])', u'ele(elemek)+Verb+Pos+Adj+FutPart(+yAcAk[yece\u011f])+P1sg(+Im[im])', u'ele(elemek)+Verb+Pos+Noun+FutPart(+yAcAk[yece\u011f])+A3sg+P1sg(+Im[im])+Nom', u'ele(elemek)+Verb+Pos+Fut(+yAcAk[yece\u011f])+Adj+Zero+Noun+Zero+A3sg+P1sg(+Im[im])+Nom')
        self.assert_parse_correct(u'eleyeceksin',       u'ele(elemek)+Verb+Pos+Fut(+yAcAk[yecek])+A2sg(sIn[sin])')
        self.assert_parse_correct(u'eleyecek',          u'ele(elemek)+Verb+Pos+Fut(+yAcAk[yecek])+A3sg', u'ele(elemek)+Verb+Pos+Adj+FutPart(+yAcAk[yecek])+Pnon', u'ele(elemek)+Verb+Pos+Fut(+yAcAk[yecek])+Adj+Zero', u'ele(elemek)+Verb+Pos+Noun+FutPart(+yAcAk[yecek])+A3sg+Pnon+Nom', u'ele(elemek)+Verb+Pos+Fut(+yAcAk[yecek])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')

        self.assert_parse_correct(u'eledim',            u'ele(elemek)+Verb+Pos+Past(dI[di])+A1sg(+Im[m])') # TODO: Wrong! "el-e-ydim" is also parsed with 'el-e-dim' if dictionary item "el" wasn't removed
        self.assert_parse_correct(u'eledin',            u'ele(elemek)+Verb+Pos+Past(dI[di])+A2sg(n[n])')
        self.assert_parse_correct(u'eledi',             u'ele(elemek)+Verb+Pos+Past(dI[di])+A3sg')

        self.assert_parse_correct(u'elemişim',          u'ele(elemek)+Verb+Pos+Narr(mIş[miş])+A1sg(+Im[im])', u'ele(elemek)+Verb+Pos+Narr(mIş[miş])+Adj+Zero+Noun+Zero+A3sg+P1sg(+Im[im])+Nom')
        self.assert_parse_correct(u'elemişsin',         u'ele(elemek)+Verb+Pos+Narr(mIş[miş])+A2sg(sIn[sin])')
        self.assert_parse_correct(u'elemiş',            u'ele(elemek)+Verb+Pos+Narr(mIş[miş])+A3sg', u'ele(elemek)+Verb+Pos+Narr(mIş[miş])+Adj+Zero', u'ele(elemek)+Verb+Pos+Narr(mIş[miş])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')

    def test_should_parse_negative_verb_tenses(self):
        self.assert_parse_correct_for_verb(u'yapmam',             u'yap(yapmak)+Verb+Neg(mA[ma])+Aor+A1sg(+Im[m])', u'yap(yapmak)+Verb+Pos+Noun+Inf(mA[ma])+A3sg+P1sg(+Im[m])+Nom')
        self.assert_parse_correct_for_verb(u'yapmazsın',          u'yap(yapmak)+Verb+Neg(mA[ma])+Aor(z[z])+A2sg(sIn[sın])')
        self.assert_parse_correct_for_verb(u'yapmaz',             u'yap(yapmak)+Verb+Neg(mA[ma])+Aor(z[z])+A3sg', u'yap(yapmak)+Verb+Neg(mA[ma])+Aor(z[z])+Adj+Zero', u'yap(yapmak)+Verb+Neg(mA[ma])+Aor(z[z])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct_for_verb(u'yapmayız',           u'yap(yapmak)+Verb+Neg(mA[ma])+Aor+A1pl(yIz[y\u0131z])')

        self.assert_parse_correct_for_verb(u'yapmıyorum',         u'yap(yapmak)+Verb+Neg(m[m])+Prog(Iyor[ıyor])+A1sg(+Im[um])')
        self.assert_parse_correct_for_verb(u'yapmıyorsun',        u'yap(yapmak)+Verb+Neg(m[m])+Prog(Iyor[ıyor])+A2sg(sIn[sun])')
        self.assert_parse_correct_for_verb(u'yapmıyor',           u'yap(yapmak)+Verb+Neg(m[m])+Prog(Iyor[ıyor])+A3sg')

        self.assert_parse_correct_for_verb(u'yapmamaktayım',      u'yap(yapmak)+Verb+Neg(mA[ma])+Prog(mAktA[makta])+A1sg(yIm[yım])')
        self.assert_parse_correct_for_verb(u'yapmamaktasın',      u'yap(yapmak)+Verb+Neg(mA[ma])+Prog(mAktA[makta])+A2sg(sIn[sın])')
        self.assert_parse_correct_for_verb(u'yapmamakta',         u'yap(yapmak)+Verb+Neg(mA[ma])+Prog(mAktA[makta])+A3sg', u'yap(yapmak)+Verb+Neg(mA[ma])+Noun+Inf(mAk[mak])+A3sg+Pnon+Loc(dA[ta])')

        self.assert_parse_correct_for_verb(u'yapmayacağım',       u'yap(yapmak)+Verb+Neg(mA[ma])+Fut(+yAcAk[yaca\u011f])+A1sg(+Im[\u0131m])', u'yap(yapmak)+Verb+Neg(mA[ma])+Adj+FutPart(+yAcAk[yaca\u011f])+P1sg(+Im[\u0131m])', u'yap(yapmak)+Verb+Neg(mA[ma])+Noun+FutPart(+yAcAk[yaca\u011f])+A3sg+P1sg(+Im[\u0131m])+Nom', u'yap(yapmak)+Verb+Neg(mA[ma])+Fut(+yAcAk[yaca\u011f])+Adj+Zero+Noun+Zero+A3sg+P1sg(+Im[\u0131m])+Nom')
        self.assert_parse_correct_for_verb(u'yapmayacaksın',      u'yap(yapmak)+Verb+Neg(mA[ma])+Fut(+yAcAk[yacak])+A2sg(sIn[sın])')
        self.assert_parse_correct_for_verb(u'yapmayacak',         u'yap(yapmak)+Verb+Neg(mA[ma])+Fut(+yAcAk[yacak])+A3sg', u'yap(yapmak)+Verb+Neg(mA[ma])+Adj+FutPart(+yAcAk[yacak])+Pnon', u'yap(yapmak)+Verb+Neg(mA[ma])+Fut(+yAcAk[yacak])+Adj+Zero', u'yap(yapmak)+Verb+Neg(mA[ma])+Noun+FutPart(+yAcAk[yacak])+A3sg+Pnon+Nom', u'yap(yapmak)+Verb+Neg(mA[ma])+Fut(+yAcAk[yacak])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')

        self.assert_parse_correct_for_verb(u'yapmadım',           u'yap(yapmak)+Verb+Neg(mA[ma])+Past(dI[dı])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'yapmadın',           u'yap(yapmak)+Verb+Neg(mA[ma])+Past(dI[dı])+A2sg(n[n])')
        self.assert_parse_correct_for_verb(u'yapmadı',            u'yap(yapmak)+Verb+Neg(mA[ma])+Past(dI[dı])+A3sg')

        self.assert_parse_correct_for_verb(u'yapmamışım',         u'yap(yapmak)+Verb+Neg(mA[ma])+Narr(mIş[mış])+A1sg(+Im[ım])', u'yap(yapmak)+Verb+Neg(mA[ma])+Narr(mIş[mış])+Adj+Zero+Noun+Zero+A3sg+P1sg(+Im[ım])+Nom')
        self.assert_parse_correct_for_verb(u'yapmamışsın',        u'yap(yapmak)+Verb+Neg(mA[ma])+Narr(mIş[mış])+A2sg(sIn[sın])')
        self.assert_parse_correct_for_verb(u'yapmamış',           u'yap(yapmak)+Verb+Neg(mA[ma])+Narr(mIş[mış])+A3sg', u'yap(yapmak)+Verb+Neg(mA[ma])+Narr(mIş[mış])+Adj+Zero', u'yap(yapmak)+Verb+Neg(mA[ma])+Narr(mIş[mış])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')


        self.assert_parse_correct_for_verb(u'çevirmem',           u'çevir(çevirmek)+Verb+Neg(mA[me])+Aor+A1sg(+Im[m])', u'çevirme(çevirme)+Noun+A3sg+P1sg(+Im[m])+Nom', u'çevir(çevirmek)+Verb+Pos+Noun+Inf(mA[me])+A3sg+P1sg(+Im[m])+Nom', u'çevirme(çevirme)+Adj+Noun+Zero+A3sg+P1sg(+Im[m])+Nom')
        self.assert_parse_correct_for_verb(u'çevirmezsin',        u'çevir(çevirmek)+Verb+Neg(mA[me])+Aor(z[z])+A2sg(sIn[sin])')
        self.assert_parse_correct_for_verb(u'çevirmez',           u'çevir(çevirmek)+Verb+Neg(mA[me])+Aor(z[z])+A3sg', u'çevir(çevirmek)+Verb+Neg(mA[me])+Aor(z[z])+Adj+Zero', u'çevir(çevirmek)+Verb+Neg(mA[me])+Aor(z[z])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')

        self.assert_parse_correct_for_verb(u'çevirmiyorum',       u'çevir(çevirmek)+Verb+Neg(m[m])+Prog(Iyor[iyor])+A1sg(+Im[um])')
        self.assert_parse_correct_for_verb(u'çevirmiyorsun',      u'çevir(çevirmek)+Verb+Neg(m[m])+Prog(Iyor[iyor])+A2sg(sIn[sun])')
        self.assert_parse_correct_for_verb(u'çevirmiyor',         u'çevir(çevirmek)+Verb+Neg(m[m])+Prog(Iyor[iyor])+A3sg')

        self.assert_parse_correct_for_verb(u'çevirmemekteyim',    u'çevir(çevirmek)+Verb+Neg(mA[me])+Prog(mAktA[mekte])+A1sg(yIm[yim])')
        self.assert_parse_correct_for_verb(u'çevirmemektesin',    u'çevir(çevirmek)+Verb+Neg(mA[me])+Prog(mAktA[mekte])+A2sg(sIn[sin])')
        self.assert_parse_correct_for_verb(u'çevirmemekte',       u'çevir(çevirmek)+Verb+Neg(mA[me])+Prog(mAktA[mekte])+A3sg', u'\xe7evir(\xe7evirmek)+Verb+Neg(mA[me])+Noun+Inf(mAk[mek])+A3sg+Pnon+Loc(dA[te])')

        self.assert_parse_correct_for_verb(u'çevirmeyeceğim',     u'\xe7evir(\xe7evirmek)+Verb+Neg(mA[me])+Fut(+yAcAk[yece\u011f])+A1sg(+Im[im])', u'\xe7evir(\xe7evirmek)+Verb+Neg(mA[me])+Adj+FutPart(+yAcAk[yece\u011f])+P1sg(+Im[im])', u'\xe7evir(\xe7evirmek)+Verb+Neg(mA[me])+Noun+FutPart(+yAcAk[yece\u011f])+A3sg+P1sg(+Im[im])+Nom', u'\xe7evir(\xe7evirmek)+Verb+Neg(mA[me])+Fut(+yAcAk[yece\u011f])+Adj+Zero+Noun+Zero+A3sg+P1sg(+Im[im])+Nom')
        self.assert_parse_correct_for_verb(u'çevirmeyeceksin',    u'çevir(çevirmek)+Verb+Neg(mA[me])+Fut(+yAcAk[yecek])+A2sg(sIn[sin])')
        self.assert_parse_correct_for_verb(u'çevirmeyecek',       u'\xe7evir(\xe7evirmek)+Verb+Neg(mA[me])+Fut(+yAcAk[yecek])+A3sg', u'\xe7evir(\xe7evirmek)+Verb+Neg(mA[me])+Adj+FutPart(+yAcAk[yecek])+Pnon', u'\xe7evir(\xe7evirmek)+Verb+Neg(mA[me])+Fut(+yAcAk[yecek])+Adj+Zero', u'\xe7evir(\xe7evirmek)+Verb+Neg(mA[me])+Noun+FutPart(+yAcAk[yecek])+A3sg+Pnon+Nom', u'\xe7evir(\xe7evirmek)+Verb+Neg(mA[me])+Fut(+yAcAk[yecek])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')

        self.assert_parse_correct_for_verb(u'çevirmedim',         u'çevir(çevirmek)+Verb+Neg(mA[me])+Past(dI[di])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'çevirmedin',         u'çevir(çevirmek)+Verb+Neg(mA[me])+Past(dI[di])+A2sg(n[n])')
        self.assert_parse_correct_for_verb(u'çevirmedi',          u'çevir(çevirmek)+Verb+Neg(mA[me])+Past(dI[di])+A3sg')

        self.assert_parse_correct_for_verb(u'çevirmemişim',       u'çevir(çevirmek)+Verb+Neg(mA[me])+Narr(mIş[miş])+A1sg(+Im[im])', u'çevir(çevirmek)+Verb+Neg(mA[me])+Narr(mIş[miş])+Adj+Zero+Noun+Zero+A3sg+P1sg(+Im[im])+Nom')
        self.assert_parse_correct_for_verb(u'çevirmemişsin',      u'çevir(çevirmek)+Verb+Neg(mA[me])+Narr(mIş[miş])+A2sg(sIn[sin])')
        self.assert_parse_correct_for_verb(u'çevirmemiş',         u'çevir(çevirmek)+Verb+Neg(mA[me])+Narr(mIş[miş])+A3sg', u'çevir(çevirmek)+Verb+Neg(mA[me])+Narr(mIş[miş])+Adj+Zero', u'çevir(çevirmek)+Verb+Neg(mA[me])+Narr(mIş[miş])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')


        self.assert_parse_correct_for_verb(u'elemem',             u'ele(elemek)+Verb+Neg(mA[me])+Aor+A1sg(+Im[m])', u'ele(elemek)+Verb+Pos+Noun+Inf(mA[me])+A3sg+P1sg(+Im[m])+Nom')
        self.assert_parse_correct_for_verb(u'elemezsin',          u'ele(elemek)+Verb+Neg(mA[me])+Aor(z[z])+A2sg(sIn[sin])')
        self.assert_parse_correct_for_verb(u'elemez',             u'ele(elemek)+Verb+Neg(mA[me])+Aor(z[z])+A3sg', u'ele(elemek)+Verb+Neg(mA[me])+Aor(z[z])+Adj+Zero', u'ele(elemek)+Verb+Neg(mA[me])+Aor(z[z])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')

        self.assert_parse_correct_for_verb(u'elemiyorum',         u'ele(elemek)+Verb+Neg(m[m])+Prog(Iyor[iyor])+A1sg(+Im[um])')
        self.assert_parse_correct_for_verb(u'elemiyorsun',        u'ele(elemek)+Verb+Neg(m[m])+Prog(Iyor[iyor])+A2sg(sIn[sun])')
        self.assert_parse_correct_for_verb(u'elemiyor',           u'ele(elemek)+Verb+Neg(m[m])+Prog(Iyor[iyor])+A3sg')

        self.assert_parse_correct_for_verb(u'elememekteyim',      u'ele(elemek)+Verb+Neg(mA[me])+Prog(mAktA[mekte])+A1sg(yIm[yim])')
        self.assert_parse_correct_for_verb(u'elememektesin',      u'ele(elemek)+Verb+Neg(mA[me])+Prog(mAktA[mekte])+A2sg(sIn[sin])')
        self.assert_parse_correct_for_verb(u'elememekte',         u'ele(elemek)+Verb+Neg(mA[me])+Prog(mAktA[mekte])+A3sg', u'ele(elemek)+Verb+Neg(mA[me])+Noun+Inf(mAk[mek])+A3sg+Pnon+Loc(dA[te])')

        self.assert_parse_correct_for_verb(u'elemeyeceğim',       u'ele(elemek)+Verb+Neg(mA[me])+Fut(+yAcAk[yece\u011f])+A1sg(+Im[im])', u'ele(elemek)+Verb+Neg(mA[me])+Adj+FutPart(+yAcAk[yece\u011f])+P1sg(+Im[im])', u'ele(elemek)+Verb+Neg(mA[me])+Noun+FutPart(+yAcAk[yece\u011f])+A3sg+P1sg(+Im[im])+Nom', u'ele(elemek)+Verb+Neg(mA[me])+Fut(+yAcAk[yece\u011f])+Adj+Zero+Noun+Zero+A3sg+P1sg(+Im[im])+Nom')
        self.assert_parse_correct_for_verb(u'elemeyeceksin',      u'ele(elemek)+Verb+Neg(mA[me])+Fut(+yAcAk[yecek])+A2sg(sIn[sin])')
        self.assert_parse_correct_for_verb(u'elemeyecek',         u'ele(elemek)+Verb+Neg(mA[me])+Fut(+yAcAk[yecek])+A3sg', u'ele(elemek)+Verb+Neg(mA[me])+Adj+FutPart(+yAcAk[yecek])+Pnon', u'ele(elemek)+Verb+Neg(mA[me])+Fut(+yAcAk[yecek])+Adj+Zero', u'ele(elemek)+Verb+Neg(mA[me])+Noun+FutPart(+yAcAk[yecek])+A3sg+Pnon+Nom', u'ele(elemek)+Verb+Neg(mA[me])+Fut(+yAcAk[yecek])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')

        self.assert_parse_correct_for_verb(u'elemedim',           u'ele(elemek)+Verb+Neg(mA[me])+Past(dI[di])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'elemedin',           u'ele(elemek)+Verb+Neg(mA[me])+Past(dI[di])+A2sg(n[n])')
        self.assert_parse_correct_for_verb(u'elemedi',            u'ele(elemek)+Verb+Neg(mA[me])+Past(dI[di])+A3sg')

        self.assert_parse_correct_for_verb(u'elememişim',         u'ele(elemek)+Verb+Neg(mA[me])+Narr(mIş[miş])+A1sg(+Im[im])', u'ele(elemek)+Verb+Neg(mA[me])+Narr(mIş[miş])+Adj+Zero+Noun+Zero+A3sg+P1sg(+Im[im])+Nom')
        self.assert_parse_correct_for_verb(u'elememişsin',        u'ele(elemek)+Verb+Neg(mA[me])+Narr(mIş[miş])+A2sg(sIn[sin])')
        self.assert_parse_correct_for_verb(u'elememiş',           u'ele(elemek)+Verb+Neg(mA[me])+Narr(mIş[miş])+A3sg', u'ele(elemek)+Verb+Neg(mA[me])+Narr(mIş[miş])+Adj+Zero', u'ele(elemek)+Verb+Neg(mA[me])+Narr(mIş[miş])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')

    def test_should_parse_positive_multiple_verb_tenses(self):
        self.assert_parse_correct_for_verb(u'yapardım',          u'yap(yapmak)+Verb+Pos+Aor(+Ar[ar])+Past(dI[dı])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'yapardın',          u'yap(yapmak)+Verb+Pos+Aor(+Ar[ar])+Past(dI[dı])+A2sg(n[n])')
        self.assert_parse_correct_for_verb(u'yapardı',           u'yap(yapmak)+Verb+Pos+Aor(+Ar[ar])+Past(dI[dı])+A3sg')

        self.assert_parse_correct_for_verb(u'yapıyordum',        u'yap(yapmak)+Verb+Pos+Prog(Iyor[ıyor])+Past(dI[du])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'yapıyordun',        u'yap(yapmak)+Verb+Pos+Prog(Iyor[ıyor])+Past(dI[du])+A2sg(n[n])')
        self.assert_parse_correct_for_verb(u'yapıyordu',         u'yap(yapmak)+Verb+Pos+Prog(Iyor[ıyor])+Past(dI[du])+A3sg')

        self.assert_parse_correct_for_verb(u'yapmaktaydım',      u'yap(yapmak)+Verb+Pos+Prog(mAktA[makta])+Past(ydI[ydı])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'yapmaktaydın',      u'yap(yapmak)+Verb+Pos+Prog(mAktA[makta])+Past(ydI[ydı])+A2sg(n[n])')
        self.assert_parse_correct_for_verb(u'yapmaktaydı',       u'yap(yapmak)+Verb+Pos+Prog(mAktA[makta])+Past(ydI[ydı])+A3sg')

        self.assert_parse_correct_for_verb(u'yapacaktım',        u'yap(yapmak)+Verb+Pos+Fut(+yAcAk[acak])+Past(dI[tı])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'yapacaktın',        u'yap(yapmak)+Verb+Pos+Fut(+yAcAk[acak])+Past(dI[tı])+A2sg(n[n])')
        self.assert_parse_correct_for_verb(u'yapacaktı',         u'yap(yapmak)+Verb+Pos+Fut(+yAcAk[acak])+Past(dI[tı])+A3sg')

#        well, the following is not valid
#        self.assert_parse_correct(u'yaptıydım',         u'yap(yapmak)+Verb+Pos+Past(dI[tı])+Past(ydI[ydı])+A1sg(+Im[m])')
#        self.assert_parse_correct(u'yaptıydın',         u'yap(yapmak)+Verb+Pos+Past(dI[tı])+Past(ydI[ydı])+A2sg(n[n])')
#        self.assert_parse_correct(u'yaptıydı',          u'yap(yapmak)+Verb+Pos+Past(dI[tı])+Past(ydI[ydı])+A3sg')

        self.assert_parse_correct_for_verb(u'yapmıştım',         u'yap(yapmak)+Verb+Pos+Narr(mIş[mış])+Past(dI[tı])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'yapmıştın',         u'yap(yapmak)+Verb+Pos+Narr(mIş[mış])+Past(dI[tı])+A2sg(n[n])')
        self.assert_parse_correct_for_verb(u'yapmıştı',          u'yap(yapmak)+Verb+Pos+Narr(mIş[mış])+Past(dI[tı])+A3sg')


        self.assert_parse_correct_for_verb(u'yaparmışım',        u'yap(yapmak)+Verb+Pos+Aor(+Ar[ar])+Narr(mIş[mış])+A1sg(+Im[ım])')
        self.assert_parse_correct_for_verb(u'yaparmışsın',       u'yap(yapmak)+Verb+Pos+Aor(+Ar[ar])+Narr(mIş[mış])+A2sg(sIn[sın])')
        self.assert_parse_correct_for_verb(u'yaparmış',          u'yap(yapmak)+Verb+Pos+Aor(+Ar[ar])+Narr(mIş[mış])+A3sg')

        self.assert_parse_correct_for_verb(u'yapıyormuşum',      u'yap(yapmak)+Verb+Pos+Prog(Iyor[ıyor])+Narr(mIş[muş])+A1sg(+Im[um])')
        self.assert_parse_correct_for_verb(u'yapıyormuşsun',     u'yap(yapmak)+Verb+Pos+Prog(Iyor[ıyor])+Narr(mIş[muş])+A2sg(sIn[sun])')
        self.assert_parse_correct_for_verb(u'yapıyormuş',        u'yap(yapmak)+Verb+Pos+Prog(Iyor[ıyor])+Narr(mIş[muş])+A3sg')

        self.assert_parse_correct_for_verb(u'yapmaktaymışım',    u'yap(yapmak)+Verb+Pos+Prog(mAktA[makta])+Narr(ymIş[ymış])+A1sg(+Im[ım])')
        self.assert_parse_correct_for_verb(u'yapmaktaymışsın',   u'yap(yapmak)+Verb+Pos+Prog(mAktA[makta])+Narr(ymIş[ymış])+A2sg(sIn[sın])')
        self.assert_parse_correct_for_verb(u'yapmaktaymış',      u'yap(yapmak)+Verb+Pos+Prog(mAktA[makta])+Narr(ymIş[ymış])+A3sg')

        self.assert_parse_correct_for_verb(u'yapacakmışım',      u'yap(yapmak)+Verb+Pos+Fut(+yAcAk[acak])+Narr(mIş[mış])+A1sg(+Im[ım])')
        self.assert_parse_correct_for_verb(u'yapacakmışsın',     u'yap(yapmak)+Verb+Pos+Fut(+yAcAk[acak])+Narr(mIş[mış])+A2sg(sIn[sın])')
        self.assert_parse_correct_for_verb(u'yapacakmış',        u'yap(yapmak)+Verb+Pos+Fut(+yAcAk[acak])+Narr(mIş[mış])+A3sg')


        self.assert_parse_correct_for_verb(u'elerdim',           u'ele(elemek)+Verb+Pos+Aor(+Ir[r])+Past(dI[di])+A1sg(+Im[m])', u'ele(elemek)+Verb+Pos+Aor(+Ar[r])+Past(dI[di])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'elerdin',           u'ele(elemek)+Verb+Pos+Aor(+Ir[r])+Past(dI[di])+A2sg(n[n])', u'ele(elemek)+Verb+Pos+Aor(+Ar[r])+Past(dI[di])+A2sg(n[n])')
        self.assert_parse_correct_for_verb(u'elerdi',            u'ele(elemek)+Verb+Pos+Aor(+Ir[r])+Past(dI[di])+A3sg', u'ele(elemek)+Verb+Pos+Aor(+Ar[r])+Past(dI[di])+A3sg')

        self.assert_parse_correct_for_verb(u'eliyordum',         u'el(elemek)+Verb+Pos+Prog(Iyor[iyor])+Past(dI[du])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'eliyordun',         u'el(elemek)+Verb+Pos+Prog(Iyor[iyor])+Past(dI[du])+A2sg(n[n])')
        self.assert_parse_correct_for_verb(u'eliyordu',          u'el(elemek)+Verb+Pos+Prog(Iyor[iyor])+Past(dI[du])+A3sg')

        self.assert_parse_correct_for_verb(u'elemekteydim',      u'ele(elemek)+Verb+Pos+Prog(mAktA[mekte])+Past(ydI[ydi])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'elemekteydin',      u'ele(elemek)+Verb+Pos+Prog(mAktA[mekte])+Past(ydI[ydi])+A2sg(n[n])')
        self.assert_parse_correct_for_verb(u'elemekteydi',       u'ele(elemek)+Verb+Pos+Prog(mAktA[mekte])+Past(ydI[ydi])+A3sg')

        self.assert_parse_correct_for_verb(u'eleyecektim',       u'ele(elemek)+Verb+Pos+Fut(+yAcAk[yecek])+Past(dI[ti])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'eleyecektin',       u'ele(elemek)+Verb+Pos+Fut(+yAcAk[yecek])+Past(dI[ti])+A2sg(n[n])')
        self.assert_parse_correct_for_verb(u'eleyecekti',        u'ele(elemek)+Verb+Pos+Fut(+yAcAk[yecek])+Past(dI[ti])+A3sg')

        self.assert_parse_correct_for_verb(u'elemiştim',         u'ele(elemek)+Verb+Pos+Narr(mIş[miş])+Past(dI[ti])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'elemiştin',         u'ele(elemek)+Verb+Pos+Narr(mIş[miş])+Past(dI[ti])+A2sg(n[n])')
        self.assert_parse_correct_for_verb(u'elemişti',          u'ele(elemek)+Verb+Pos+Narr(mIş[miş])+Past(dI[ti])+A3sg')


        self.assert_parse_correct_for_verb(u'elermişim',         u'ele(elemek)+Verb+Pos+Aor(+Ir[r])+Narr(mIş[miş])+A1sg(+Im[im])', u'ele(elemek)+Verb+Pos+Aor(+Ar[r])+Narr(mIş[miş])+A1sg(+Im[im])')
        self.assert_parse_correct_for_verb(u'elermişsin',        u'ele(elemek)+Verb+Pos+Aor(+Ir[r])+Narr(mIş[miş])+A2sg(sIn[sin])', u'ele(elemek)+Verb+Pos+Aor(+Ar[r])+Narr(mIş[miş])+A2sg(sIn[sin])')
        self.assert_parse_correct_for_verb(u'elermiş',           u'ele(elemek)+Verb+Pos+Aor(+Ir[r])+Narr(mIş[miş])+A3sg', u'ele(elemek)+Verb+Pos+Aor(+Ar[r])+Narr(mIş[miş])+A3sg')

        self.assert_parse_correct_for_verb(u'eliyormuşum',       u'el(elemek)+Verb+Pos+Prog(Iyor[iyor])+Narr(mIş[muş])+A1sg(+Im[um])')
        self.assert_parse_correct_for_verb(u'eliyormuşsun',      u'el(elemek)+Verb+Pos+Prog(Iyor[iyor])+Narr(mIş[muş])+A2sg(sIn[sun])')
        self.assert_parse_correct_for_verb(u'eliyormuş',         u'el(elemek)+Verb+Pos+Prog(Iyor[iyor])+Narr(mIş[muş])+A3sg')

        self.assert_parse_correct_for_verb(u'elemekteymişim',    u'ele(elemek)+Verb+Pos+Prog(mAktA[mekte])+Narr(ymIş[ymiş])+A1sg(+Im[im])')
        self.assert_parse_correct_for_verb(u'elemekteymişsin',   u'ele(elemek)+Verb+Pos+Prog(mAktA[mekte])+Narr(ymIş[ymiş])+A2sg(sIn[sin])')
        self.assert_parse_correct_for_verb(u'elemekteymiş',      u'ele(elemek)+Verb+Pos+Prog(mAktA[mekte])+Narr(ymIş[ymiş])+A3sg')

        self.assert_parse_correct_for_verb(u'eleyecekmişim',     u'ele(elemek)+Verb+Pos+Fut(+yAcAk[yecek])+Narr(mIş[miş])+A1sg(+Im[im])')
        self.assert_parse_correct_for_verb(u'eleyecekmişsin',    u'ele(elemek)+Verb+Pos+Fut(+yAcAk[yecek])+Narr(mIş[miş])+A2sg(sIn[sin])')
        self.assert_parse_correct_for_verb(u'eleyecekmiş',       u'ele(elemek)+Verb+Pos+Fut(+yAcAk[yecek])+Narr(mIş[miş])+A3sg')

    def test_should_parse_negative_multiple_verb_tenses(self):
        self.assert_parse_correct_for_verb(u'yapmazdım',         u'yap(yapmak)+Verb+Neg(mA[ma])+Aor(z[z])+Past(dI[dı])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'yapmazdın',         u'yap(yapmak)+Verb+Neg(mA[ma])+Aor(z[z])+Past(dI[dı])+A2sg(n[n])')
        self.assert_parse_correct_for_verb(u'yapmazdı',          u'yap(yapmak)+Verb+Neg(mA[ma])+Aor(z[z])+Past(dI[dı])+A3sg')

        self.assert_parse_correct_for_verb(u'yapmıyordum',       u'yap(yapmak)+Verb+Neg(m[m])+Prog(Iyor[ıyor])+Past(dI[du])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'yapmıyordun',       u'yap(yapmak)+Verb+Neg(m[m])+Prog(Iyor[ıyor])+Past(dI[du])+A2sg(n[n])')
        self.assert_parse_correct_for_verb(u'yapmıyordu',        u'yap(yapmak)+Verb+Neg(m[m])+Prog(Iyor[ıyor])+Past(dI[du])+A3sg')

        self.assert_parse_correct_for_verb(u'yapmamaktaydım',    u'yap(yapmak)+Verb+Neg(mA[ma])+Prog(mAktA[makta])+Past(ydI[ydı])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'yapmamaktaydın',    u'yap(yapmak)+Verb+Neg(mA[ma])+Prog(mAktA[makta])+Past(ydI[ydı])+A2sg(n[n])')
        self.assert_parse_correct_for_verb(u'yapmamaktaydı',     u'yap(yapmak)+Verb+Neg(mA[ma])+Prog(mAktA[makta])+Past(ydI[ydı])+A3sg')

        self.assert_parse_correct_for_verb(u'yapmayacaktım',     u'yap(yapmak)+Verb+Neg(mA[ma])+Fut(+yAcAk[yacak])+Past(dI[tı])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'yapmayacaktın',     u'yap(yapmak)+Verb+Neg(mA[ma])+Fut(+yAcAk[yacak])+Past(dI[tı])+A2sg(n[n])')
        self.assert_parse_correct_for_verb(u'yapmayacaktı',      u'yap(yapmak)+Verb+Neg(mA[ma])+Fut(+yAcAk[yacak])+Past(dI[tı])+A3sg')

        self.assert_parse_correct_for_verb(u'yapmamıştım',       u'yap(yapmak)+Verb+Neg(mA[ma])+Narr(mIş[mış])+Past(dI[tı])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'yapmamıştın',       u'yap(yapmak)+Verb+Neg(mA[ma])+Narr(mIş[mış])+Past(dI[tı])+A2sg(n[n])')
        self.assert_parse_correct_for_verb(u'yapmamıştı',        u'yap(yapmak)+Verb+Neg(mA[ma])+Narr(mIş[mış])+Past(dI[tı])+A3sg')


        self.assert_parse_correct_for_verb(u'yapmazmışım',       u'yap(yapmak)+Verb+Neg(mA[ma])+Aor(z[z])+Narr(mIş[mış])+A1sg(+Im[ım])')
        self.assert_parse_correct_for_verb(u'yapmazmışsın',      u'yap(yapmak)+Verb+Neg(mA[ma])+Aor(z[z])+Narr(mIş[mış])+A2sg(sIn[sın])')
        self.assert_parse_correct_for_verb(u'yapmazmış',         u'yap(yapmak)+Verb+Neg(mA[ma])+Aor(z[z])+Narr(mIş[mış])+A3sg')

        self.assert_parse_correct_for_verb(u'yapmıyormuşum',     u'yap(yapmak)+Verb+Neg(m[m])+Prog(Iyor[ıyor])+Narr(mIş[muş])+A1sg(+Im[um])')
        self.assert_parse_correct_for_verb(u'yapmıyormuşsun',    u'yap(yapmak)+Verb+Neg(m[m])+Prog(Iyor[ıyor])+Narr(mIş[muş])+A2sg(sIn[sun])')
        self.assert_parse_correct_for_verb(u'yapmıyormuş',       u'yap(yapmak)+Verb+Neg(m[m])+Prog(Iyor[ıyor])+Narr(mIş[muş])+A3sg')

        self.assert_parse_correct_for_verb(u'yapmamaktaymışım',  u'yap(yapmak)+Verb+Neg(mA[ma])+Prog(mAktA[makta])+Narr(ymIş[ymış])+A1sg(+Im[ım])')
        self.assert_parse_correct_for_verb(u'yapmamaktaymışsın', u'yap(yapmak)+Verb+Neg(mA[ma])+Prog(mAktA[makta])+Narr(ymIş[ymış])+A2sg(sIn[sın])')
        self.assert_parse_correct_for_verb(u'yapmamaktaymış',    u'yap(yapmak)+Verb+Neg(mA[ma])+Prog(mAktA[makta])+Narr(ymIş[ymış])+A3sg')

        self.assert_parse_correct_for_verb(u'yapmayacakmışım',   u'yap(yapmak)+Verb+Neg(mA[ma])+Fut(+yAcAk[yacak])+Narr(mIş[mış])+A1sg(+Im[ım])')
        self.assert_parse_correct_for_verb(u'yapmayacakmışsın',  u'yap(yapmak)+Verb+Neg(mA[ma])+Fut(+yAcAk[yacak])+Narr(mIş[mış])+A2sg(sIn[sın])')
        self.assert_parse_correct_for_verb(u'yapmayacakmış',     u'yap(yapmak)+Verb+Neg(mA[ma])+Fut(+yAcAk[yacak])+Narr(mIş[mış])+A3sg')


        self.assert_parse_correct_for_verb(u'elemezdim',         u'ele(elemek)+Verb+Neg(mA[me])+Aor(z[z])+Past(dI[di])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'elemezdin',         u'ele(elemek)+Verb+Neg(mA[me])+Aor(z[z])+Past(dI[di])+A2sg(n[n])')
        self.assert_parse_correct_for_verb(u'elemezdi',          u'ele(elemek)+Verb+Neg(mA[me])+Aor(z[z])+Past(dI[di])+A3sg')

        self.assert_parse_correct_for_verb(u'elemiyordum',       u'ele(elemek)+Verb+Neg(m[m])+Prog(Iyor[iyor])+Past(dI[du])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'elemiyordun',       u'ele(elemek)+Verb+Neg(m[m])+Prog(Iyor[iyor])+Past(dI[du])+A2sg(n[n])')
        self.assert_parse_correct_for_verb(u'elemiyordu',        u'ele(elemek)+Verb+Neg(m[m])+Prog(Iyor[iyor])+Past(dI[du])+A3sg')

        self.assert_parse_correct_for_verb(u'elememekteydim',    u'ele(elemek)+Verb+Neg(mA[me])+Prog(mAktA[mekte])+Past(ydI[ydi])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'elememekteydin',    u'ele(elemek)+Verb+Neg(mA[me])+Prog(mAktA[mekte])+Past(ydI[ydi])+A2sg(n[n])')
        self.assert_parse_correct_for_verb(u'elememekteydi',     u'ele(elemek)+Verb+Neg(mA[me])+Prog(mAktA[mekte])+Past(ydI[ydi])+A3sg')

        self.assert_parse_correct_for_verb(u'elemeyecektim',     u'ele(elemek)+Verb+Neg(mA[me])+Fut(+yAcAk[yecek])+Past(dI[ti])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'elemeyecektin',     u'ele(elemek)+Verb+Neg(mA[me])+Fut(+yAcAk[yecek])+Past(dI[ti])+A2sg(n[n])')
        self.assert_parse_correct_for_verb(u'elemeyecekti',      u'ele(elemek)+Verb+Neg(mA[me])+Fut(+yAcAk[yecek])+Past(dI[ti])+A3sg')

        self.assert_parse_correct_for_verb(u'elememiştim',       u'ele(elemek)+Verb+Neg(mA[me])+Narr(mIş[miş])+Past(dI[ti])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'elememiştin',       u'ele(elemek)+Verb+Neg(mA[me])+Narr(mIş[miş])+Past(dI[ti])+A2sg(n[n])')
        self.assert_parse_correct_for_verb(u'elememişti',        u'ele(elemek)+Verb+Neg(mA[me])+Narr(mIş[miş])+Past(dI[ti])+A3sg')


        self.assert_parse_correct_for_verb(u'elemezmişim',       u'ele(elemek)+Verb+Neg(mA[me])+Aor(z[z])+Narr(mIş[miş])+A1sg(+Im[im])')
        self.assert_parse_correct_for_verb(u'elemezmişsin',      u'ele(elemek)+Verb+Neg(mA[me])+Aor(z[z])+Narr(mIş[miş])+A2sg(sIn[sin])')
        self.assert_parse_correct_for_verb(u'elemezmiş',         u'ele(elemek)+Verb+Neg(mA[me])+Aor(z[z])+Narr(mIş[miş])+A3sg')

        self.assert_parse_correct_for_verb(u'elemiyormuşum',     u'ele(elemek)+Verb+Neg(m[m])+Prog(Iyor[iyor])+Narr(mIş[muş])+A1sg(+Im[um])')
        self.assert_parse_correct_for_verb(u'elemiyormuşsun',    u'ele(elemek)+Verb+Neg(m[m])+Prog(Iyor[iyor])+Narr(mIş[muş])+A2sg(sIn[sun])')
        self.assert_parse_correct_for_verb(u'elemiyormuş',       u'ele(elemek)+Verb+Neg(m[m])+Prog(Iyor[iyor])+Narr(mIş[muş])+A3sg')

        self.assert_parse_correct_for_verb(u'elememekteymişim',  u'ele(elemek)+Verb+Neg(mA[me])+Prog(mAktA[mekte])+Narr(ymIş[ymiş])+A1sg(+Im[im])')
        self.assert_parse_correct_for_verb(u'elememekteymişsin', u'ele(elemek)+Verb+Neg(mA[me])+Prog(mAktA[mekte])+Narr(ymIş[ymiş])+A2sg(sIn[sin])')
        self.assert_parse_correct_for_verb(u'elememekteymiş',    u'ele(elemek)+Verb+Neg(mA[me])+Prog(mAktA[mekte])+Narr(ymIş[ymiş])+A3sg')

        self.assert_parse_correct_for_verb(u'elemeyecekmişim',   u'ele(elemek)+Verb+Neg(mA[me])+Fut(+yAcAk[yecek])+Narr(mIş[miş])+A1sg(+Im[im])')
        self.assert_parse_correct_for_verb(u'elemeyecekmişsin',  u'ele(elemek)+Verb+Neg(mA[me])+Fut(+yAcAk[yecek])+Narr(mIş[miş])+A2sg(sIn[sin])')
        self.assert_parse_correct_for_verb(u'elemeyecekmiş',     u'ele(elemek)+Verb+Neg(mA[me])+Fut(+yAcAk[yecek])+Narr(mIş[miş])+A3sg')

    def test_should_parse_some_verbs(self):
        self.assert_parse_correct_for_verb(u'yapardık',          u'yap(yapmak)+Verb+Pos+Aor(+Ar[ar])+Past(dI[dı])+A1pl(k[k])')
        self.assert_parse_correct_for_verb(u'yapardınız',        u'yap(yapmak)+Verb+Pos+Aor(+Ar[ar])+Past(dI[dı])+A2pl(nIz[nız])')
        self.assert_parse_correct_for_verb(u'yapardılar',        u'yap(yapmak)+Verb+Pos+Aor(+Ar[ar])+Past(dI[dı])+A3pl(lAr[lar])')
#        self.assert_parse_correct(u'yaparlardı',        u'yap(yapmak)+Verb+Pos+Aor(+Ar[ar])+Past(dI[dı])+A3sg')    ##TODO

    def test_should_parse_modals(self):
        self.assert_parse_correct_for_verb(u'eleyebilirim',      u'ele(elemek)+Verb+Verb+Able(+yAbil[yebil])+Pos+Aor(+Ir[ir])+A1sg(+Im[im])', u'ele(elemek)+Verb+Verb+Able(+yAbil[yebil])+Pos+Aor(+Ir[ir])+Adj+Zero+Noun+Zero+A3sg+P1sg(+Im[im])+Nom')
        self.assert_parse_correct_for_verb(u'eleyemem',          u'ele(elemek)+Verb+Verb+Able(+yA[ye])+Neg(mA[me])+Aor+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'eleyemezsin',       u'ele(elemek)+Verb+Verb+Able(+yA[ye])+Neg(mA[me])+Aor(z[z])+A2sg(sIn[sin])')
        self.assert_parse_correct_for_verb(u'yapamazdım',        u'yap(yapmak)+Verb+Verb+Able(+yA[a])+Neg(mA[ma])+Aor(z[z])+Past(dI[dı])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'eleyemeyeceğim',    u'ele(elemek)+Verb+Verb+Able(+yA[ye])+Neg(mA[me])+Fut(+yAcAk[yeceğ])+A1sg(+Im[im])', u'ele(elemek)+Verb+Verb+Able(+yA[ye])+Neg(mA[me])+Adj+FutPart(+yAcAk[yeceğ])+P1sg(+Im[im])', u'ele(elemek)+Verb+Verb+Able(+yA[ye])+Neg(mA[me])+Noun+FutPart(+yAcAk[yeceğ])+A3sg+P1sg(+Im[im])+Nom', u'ele(elemek)+Verb+Verb+Able(+yA[ye])+Neg(mA[me])+Fut(+yAcAk[yece\u011f])+Adj+Zero+Noun+Zero+A3sg+P1sg(+Im[im])+Nom')

        self.assert_parse_correct_for_verb(u'yapabilirdim',      u'yap(yapmak)+Verb+Verb+Able(+yAbil[abil])+Pos+Aor(+Ir[ir])+Past(dI[di])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'yapabileceksin',    u'yap(yapmak)+Verb+Verb+Able(+yAbil[abil])+Pos+Fut(+yAcAk[ecek])+A2sg(sIn[sin])')

        self.assert_parse_correct_for_verb(u'yapmalıyım',        u'yap(yapmak)+Verb+Pos+Neces(mAlI![malı])+A1sg(yIm[yım])')
        self.assert_parse_correct_for_verb(u'yapmalıydım',       u'yap(yapmak)+Verb+Pos+Neces(mAlI![malı])+Past(ydI[ydı])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'yapmamalıyım',      u'yap(yapmak)+Verb+Neg(mA[ma])+Neces(mAlI![malı])+A1sg(yIm[yım])')
        self.assert_parse_correct_for_verb(u'yapmamalıydım',     u'yap(yapmak)+Verb+Neg(mA[ma])+Neces(mAlI![malı])+Past(ydI[ydı])+A1sg(+Im[m])')

        self.assert_parse_correct_for_verb(u'elemeliymiş',       u'ele(elemek)+Verb+Pos+Neces(mAlI![meli])+Narr(ymIş[ymiş])+A3sg')
        self.assert_parse_correct_for_verb(u'elememeliymiş',     u'ele(elemek)+Verb+Neg(mA[me])+Neces(mAlI![meli])+Narr(ymIş[ymiş])+A3sg')

        self.assert_parse_correct_for_verb(u'eleyesin',          u'ele(elemek)+Verb+Pos+Opt(yA[ye])+A2sg(sIn[sin])')
        self.assert_parse_correct_for_verb(u'elemeyeydim',       u'ele(elemek)+Verb+Neg(mA[me])+Opt(yAy[yey])+Past(dI[di])+A1sg(+Im[m])', u'ele(elemek)+Verb+Neg(mA[me])+Opt(yA[ye])+Past(ydI[ydi])+A1sg(+Im[m])')

        self.assert_parse_correct_for_verb(u'eleyebilmeliydim',  u'ele(elemek)+Verb+Verb+Able(+yAbil[yebil])+Pos+Neces(mAlI![meli])+Past(ydI[ydi])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'eleyememeliydi',    u'ele(elemek)+Verb+Verb+Able(+yA[ye])+Neg(mA[me])+Neces(mAlI![meli])+Past(ydI[ydi])+A3sg')

    def test_should_possessives(self):
        self.assert_parse_correct_for_verb(u'kalemim',           u'kalem(kalem)+Noun+A3sg+P1sg(+Im[im])+Nom')
        self.assert_parse_correct_for_verb(u'kalemimi',          u'kalem(kalem)+Noun+A3sg+P1sg(+Im[im])+Acc(+yI[i])')
        self.assert_parse_correct_for_verb(u'kalemimden',        u'kalem(kalem)+Noun+A3sg+P1sg(+Im[im])+Abl(dAn[den])')
        self.assert_parse_correct_for_verb(u'kalemimin',         u'kalem(kalem)+Noun+A3sg+P1sg(+Im[im])+Gen(+nIn[in])')

        self.assert_parse_correct_for_verb(u'danam',             u'dana(dana)+Noun+A3sg+P1sg(+Im[m])+Nom')
        self.assert_parse_correct_for_verb(u'danamı',            u'dana(dana)+Noun+A3sg+P1sg(+Im[m])+Acc(+yI[ı])')

        self.assert_parse_correct_for_verb(u'kitabın',           u'kitab(kitap)+Noun+A3sg+Pnon+Gen(+nIn[ın])', u'kitab(kitap)+Noun+A3sg+P2sg(+In[ın])+Nom')
        self.assert_parse_correct_for_verb(u'kitabını',          u'kitab(kitap)+Noun+A3sg+P2sg(+In[ın])+Acc(+yI[ı])', u'kitab(kitap)+Noun+A3sg+P3sg(+sI[ı])+Acc(nI[nı])')

        self.assert_parse_correct_for_verb(u'danası',            u'dana(dana)+Noun+A3sg+P3sg(+sI[sı])+Nom')
        self.assert_parse_correct_for_verb(u'danasında',         u'dana(dana)+Noun+A3sg+P3sg(+sI[sı])+Loc(ndA[nda])')

        self.assert_parse_correct_for_verb(u'danamız',           u'dana(dana)+Noun+A3sg+P1pl(+ImIz[mız])+Nom')
        self.assert_parse_correct_for_verb(u'danamızdan',        u'dana(dana)+Noun+A3sg+P1pl(+ImIz[mız])+Abl(dAn[dan])')

        self.assert_parse_correct_for_verb(u'sandalyeniz',       u'sandalye(sandalye)+Noun+A3sg+P2pl(+InIz[niz])+Nom')
        self.assert_parse_correct_for_verb(u'sandalyelerinizden',u'sandalye(sandalye)+Noun+A3pl(lAr[ler])+P2pl(+InIz[iniz])+Abl(dAn[den])')

        self.assert_parse_correct_for_verb(u'sandalyeleri',
            u'sandalye(sandalye)+Noun+A3pl(lAr[ler])+Pnon+Acc(+yI[i])',
            u'sandalye(sandalye)+Noun+A3pl(lAr[ler])+P3sg(+sI[i])+Nom',
            u'sandalye(sandalye)+Noun+A3pl(lAr[ler])+P3pl(I![i])+Nom',
            u'sandalye(sandalye)+Noun+A3sg+P3pl(lArI![leri])+Nom'
        )   # TODO
        self.assert_parse_correct_for_verb(u'sandalyelerini',
            u'sandalye(sandalye)+Noun+A3pl(lAr[ler])+P2sg(+In[in])+Acc(+yI[i])',
            u'sandalye(sandalye)+Noun+A3pl(lAr[ler])+P3sg(+sI[i])+Acc(nI[ni])',
            u'sandalye(sandalye)+Noun+A3pl(lAr[ler])+P3pl(I![i])+Acc(nI[ni])',
            u'sandalye(sandalye)+Noun+A3sg+P3pl(lArI![leri])+Acc(nI[ni])'
        )
        self.assert_parse_correct_for_verb(u'sandalyelerine',
            u'sandalye(sandalye)+Noun+A3pl(lAr[ler])+P2sg(+In[in])+Dat(+yA[e])',
            u'sandalye(sandalye)+Noun+A3pl(lAr[ler])+P3sg(+sI[i])+Dat(nA[ne])',
            u'sandalye(sandalye)+Noun+A3pl(lAr[ler])+P3pl(I![i])+Dat(nA[ne])',
            u'sandalye(sandalye)+Noun+A3sg+P3pl(lArI![leri])+Dat(nA[ne])'
        )
        self.assert_parse_correct_for_verb(u'sandalyelerinde',
            u'sandalye(sandalye)+Noun+A3pl(lAr[ler])+P2sg(+In[in])+Loc(dA[de])',
            u'sandalye(sandalye)+Noun+A3pl(lAr[ler])+P3sg(+sI[i])+Loc(ndA[nde])',
            u'sandalye(sandalye)+Noun+A3pl(lAr[ler])+P3pl(I![i])+Loc(ndA[nde])',
            u'sandalye(sandalye)+Noun+A3sg+P3pl(lArI![leri])+Loc(ndA[nde])'
        )
        self.assert_parse_correct_for_verb(u'sandalyelerinin',
            u'sandalye(sandalye)+Noun+A3pl(lAr[ler])+P2sg(+In[in])+Gen(+nIn[in])',
            u'sandalye(sandalye)+Noun+A3pl(lAr[ler])+P3sg(+sI[i])+Gen(+nIn[nin])',
            u'sandalye(sandalye)+Noun+A3pl(lAr[ler])+P3pl(I![i])+Gen(+nIn[nin])',
            u'sandalye(sandalye)+Noun+A3sg+P3pl(lArI![leri])+Gen(+nIn[nin])'

        )
        self.assert_parse_correct_for_verb(u'sandalyeleriyle',
            u'sandalye(sandalye)+Noun+A3pl(lAr[ler])+P3sg(+sI[i])+Ins(+ylA[yle])',
            u'sandalye(sandalye)+Noun+A3pl(lAr[ler])+P3pl(I![i])+Ins(+ylA[yle])',
            u'sandalye(sandalye)+Noun+A3sg+P3pl(lArI![leri])+Ins(+ylA[yle])'
        )
        self.assert_parse_correct_for_verb(u'sandalyelerinle',
            u'sandalye(sandalye)+Noun+A3pl(lAr[ler])+P2sg(+In[in])+Ins(+ylA[le])'
        )

    def test_should_parse_some_adverbs(self):
        self.assert_parse_correct_for_verb(u'aceleten',          u'aceleten(aceleten)+Adv')

    def test_should_parse_pronouns(self):
        # remove some roots to make the test simple
        self.cloned_root_map[u'on'] = []
        self.cloned_root_map[u'ona'] = []
        self.cloned_root_map[u'bend'] = []
        self.cloned_root_map[u'bun'] = []
        self.cloned_root_map[u'bizle'] = []
        self.cloned_root_map[u'se'] = []
        self.cloned_root_map[u'bur'] = []
        self.cloned_root_map[u'ben'] = filter(lambda root : root.lexeme.syntactic_category==SyntacticCategory.PRONOUN, self.cloned_root_map[u'ben'])
        self.cloned_root_map[u'ban'] = filter(lambda root : root.lexeme.syntactic_category==SyntacticCategory.PRONOUN, self.cloned_root_map[u'ban'])
        self.cloned_root_map[u'san'] = filter(lambda root : root.lexeme.syntactic_category==SyntacticCategory.PRONOUN, self.cloned_root_map[u'san'])
        self.cloned_root_map[u'biz'] = filter(lambda root : root.lexeme.syntactic_category==SyntacticCategory.PRONOUN, self.cloned_root_map[u'biz'])

        self.assert_parse_correct(u'ben',               u'ben(ben)+Pron+Pers+A1sg+Pnon+Nom')
        self.assert_parse_correct(u'sen',               u'sen(sen)+Pron+Pers+A2sg+Pnon+Nom')
        self.assert_parse_correct(u'o',                 u'o(o)+Det', u'o(o)+Pron+Pers+A3sg+Pnon+Nom', u'o(o)+Pron+Demons+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'biz',               u'biz(biz)+Pron+Pers+A1pl+Pnon+Nom')
        self.assert_parse_correct(u'siz',               u'siz(siz)+Pron+Pers+A2pl+Pnon+Nom')
        self.assert_parse_correct(u'onlar',             u'o(o)+Pron+Pers+A3pl(nlar[nlar])+Pnon+Nom', u'o(o)+Pron+Demons+A3pl(nlar[nlar])+Pnon+Nom')
        self.assert_parse_correct(u'bizler',            u'biz(biz)+Pron+Pers+A1pl(ler[ler])+Pnon+Nom')
        self.assert_parse_correct(u'sizler',            u'siz(siz)+Pron+Pers+A2pl(ler[ler])+Pnon+Nom')

        self.assert_parse_correct(u'beni',              u'ben(ben)+Pron+Pers+A1sg+Pnon+Acc(i[i])')
        self.assert_parse_correct(u'seni',              u'sen(sen)+Pron+Pers+A2sg+Pnon+Acc(i[i])')
        self.assert_parse_correct(u'onu',               u'o(o)+Pron+Pers+A3sg+Pnon+Acc(nu[nu])', u'o(o)+Pron+Demons+A3sg+Pnon+Acc(nu[nu])')
        self.assert_parse_correct(u'bizi',              u'biz(biz)+Pron+Pers+A1pl+Pnon+Acc(i[i])')
        self.assert_parse_correct(u'sizi',              u'siz(siz)+Pron+Pers+A2pl+Pnon+Acc(i[i])')
        self.assert_parse_correct(u'onları',            u'o(o)+Pron+Pers+A3pl(nlar[nlar])+Pnon+Acc(ı[ı])', u'o(o)+Pron+Demons+A3pl(nlar[nlar])+Pnon+Acc(ı[ı])')
        self.assert_parse_correct(u'bizleri',           u'biz(biz)+Pron+Pers+A1pl(ler[ler])+Pnon+Acc(i[i])')
        self.assert_parse_correct(u'sizleri',           u'siz(siz)+Pron+Pers+A2pl(ler[ler])+Pnon+Acc(i[i])')

        self.assert_parse_correct(u'bana',              u'ban(ben)+Pron+Pers+A1sg+Pnon+Dat(a[a])')
        self.assert_parse_correct(u'sana',              u'san(sen)+Pron+Pers+A2sg+Pnon+Dat(a[a])')
        self.assert_parse_correct(u'ona',               u'o(o)+Pron+Pers+A3sg+Pnon+Dat(na[na])', u'o(o)+Pron+Demons+A3sg+Pnon+Dat(na[na])')
        self.assert_parse_correct(u'bize',              u'biz(biz)+Pron+Pers+A1pl+Pnon+Dat(e[e])')
        self.assert_parse_correct(u'size',              u'siz(siz)+Pron+Pers+A2pl+Pnon+Dat(e[e])')
        self.assert_parse_correct(u'onlara',            u'o(o)+Pron+Pers+A3pl(nlar[nlar])+Pnon+Dat(a[a])', u'o(o)+Pron+Demons+A3pl(nlar[nlar])+Pnon+Dat(a[a])')
        self.assert_parse_correct(u'bizlere',           u'biz(biz)+Pron+Pers+A1pl(ler[ler])+Pnon+Dat(e[e])')
        self.assert_parse_correct(u'sizlere',           u'siz(siz)+Pron+Pers+A2pl(ler[ler])+Pnon+Dat(e[e])')

        self.assert_parse_correct(u'bende',             u'ben(ben)+Pron+Pers+A1sg+Pnon+Loc(de[de])')
        self.assert_parse_correct(u'sende',             u'sen(sen)+Pron+Pers+A2sg+Pnon+Loc(de[de])')
        self.assert_parse_correct(u'onda',              u'o(o)+Pron+Pers+A3sg+Pnon+Loc(nda[nda])', u'o(o)+Pron+Demons+A3sg+Pnon+Loc(nda[nda])')
        self.assert_parse_correct(u'bizde',             u'biz(biz)+Pron+Pers+A1pl+Pnon+Loc(de[de])')
        self.assert_parse_correct(u'sizde',             u'siz(siz)+Pron+Pers+A2pl+Pnon+Loc(de[de])')
        self.assert_parse_correct(u'onlarda',           u'o(o)+Pron+Pers+A3pl(nlar[nlar])+Pnon+Loc(da[da])', u'o(o)+Pron+Demons+A3pl(nlar[nlar])+Pnon+Loc(da[da])')
        self.assert_parse_correct(u'bizlerde',          u'biz(biz)+Pron+Pers+A1pl(ler[ler])+Pnon+Loc(de[de])')
        self.assert_parse_correct(u'sizlerde',          u'siz(siz)+Pron+Pers+A2pl(ler[ler])+Pnon+Loc(de[de])')

        self.assert_parse_correct(u'benden',            u'ben(ben)+Pron+Pers+A1sg+Pnon+Abl(den[den])')
        self.assert_parse_correct(u'senden',            u'sen(sen)+Pron+Pers+A2sg+Pnon+Abl(den[den])')
        self.assert_parse_correct(u'ondan',             u'o(o)+Pron+Pers+A3sg+Pnon+Abl(ndan[ndan])', u'o(o)+Pron+Demons+A3sg+Pnon+Abl(ndan[ndan])')
        self.assert_parse_correct(u'bizden',            u'biz(biz)+Pron+Pers+A1pl+Pnon+Abl(den[den])')
        self.assert_parse_correct(u'sizden',            u'siz(siz)+Pron+Pers+A2pl+Pnon+Abl(den[den])')
        self.assert_parse_correct(u'onlardan',          u'o(o)+Pron+Pers+A3pl(nlar[nlar])+Pnon+Abl(dan[dan])', u'o(o)+Pron+Demons+A3pl(nlar[nlar])+Pnon+Abl(dan[dan])')
        self.assert_parse_correct(u'bizlerden',         u'biz(biz)+Pron+Pers+A1pl(ler[ler])+Pnon+Abl(den[den])')
        self.assert_parse_correct(u'sizlerden',         u'siz(siz)+Pron+Pers+A2pl(ler[ler])+Pnon+Abl(den[den])')

        self.assert_parse_correct(u'benim',             u'ben(ben)+Pron+Pers+A1sg+Pnon+Gen(im[im])')
        self.assert_parse_correct(u'senin',             u'sen(sen)+Pron+Pers+A2sg+Pnon+Gen(in[in])')
        self.assert_parse_correct(u'onun',              u'o(o)+Pron+Pers+A3sg+Pnon+Gen(nun[nun])', u'o(o)+Pron+Demons+A3sg+Pnon+Gen(nun[nun])')
        self.assert_parse_correct(u'bizim',             u'biz(biz)+Pron+Pers+A1pl+Pnon+Gen(im[im])')
        self.assert_parse_correct(u'sizin',             u'siz(siz)+Pron+Pers+A2pl+Pnon+Gen(in[in])')
        self.assert_parse_correct(u'onların',           u'o(o)+Pron+Pers+A3pl(nlar[nlar])+Pnon+Gen(ın[ın])', u'o(o)+Pron+Demons+A3pl(nlar[nlar])+Pnon+Gen(ın[ın])')
        self.assert_parse_correct(u'bizlerin',          u'biz(biz)+Pron+Pers+A1pl(ler[ler])+Pnon+Gen(in[in])')
        self.assert_parse_correct(u'sizlerin',          u'siz(siz)+Pron+Pers+A2pl(ler[ler])+Pnon+Gen(in[in])')

        self.assert_parse_correct(u'benimle',           u'ben(ben)+Pron+Pers+A1sg+Pnon+Ins(imle[imle])')
        self.assert_parse_correct(u'seninle',           u'sen(sen)+Pron+Pers+A2sg+Pnon+Ins(inle[inle])')
        self.assert_parse_correct(u'onunla',            u'o(o)+Pron+Pers+A3sg+Pnon+Ins(nunla[nunla])', u'o(o)+Pron+Demons+A3sg+Pnon+Ins(nunla[nunla])')
        self.assert_parse_correct(u'bizimle',           u'biz(biz)+Pron+Pers+A1pl+Pnon+Ins(imle[imle])')
        self.assert_parse_correct(u'sizinle',           u'siz(siz)+Pron+Pers+A2pl+Pnon+Ins(inle[inle])')
        self.assert_parse_correct(u'onlarla',           u'o(o)+Pron+Pers+A3pl(nlar[nlar])+Pnon+Ins(la[la])', u'o(o)+Pron+Demons+A3pl(nlar[nlar])+Pnon+Ins(la[la])')
        self.assert_parse_correct(u'bizlerle',          u'biz(biz)+Pron+Pers+A1pl(ler[ler])+Pnon+Ins(le[le])')
        self.assert_parse_correct(u'sizlerle',          u'siz(siz)+Pron+Pers+A2pl(ler[ler])+Pnon+Ins(le[le])')

        self.assert_parse_correct(u'benle',             u'ben(ben)+Pron+Pers+A1sg+Pnon+Ins(le[le])')
        self.assert_parse_correct(u'senle',             u'sen(sen)+Pron+Pers+A2sg+Pnon+Ins(le[le])')
        self.assert_parse_correct(u'onla',              u'o(o)+Pron+Pers+A3sg+Pnon+Ins(nla[nla])', u'o(o)+Pron+Demons+A3sg+Pnon+Ins(nla[nla])')
        self.assert_parse_correct(u'bizle',             u'biz(biz)+Pron+Pers+A1pl+Pnon+Ins(le[le])')
        self.assert_parse_correct(u'sizle',             u'siz(siz)+Pron+Pers+A2pl+Pnon+Ins(le[le])')

        self.assert_parse_correct(u'bu',                u'bu(bu)+Det', u'bu(bu)+Pron+Demons+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'şu',                u'şu(şu)+Pron+Demons+A3sg+Pnon+Nom', u'şu(şu)+Det')
        self.assert_parse_correct(u'bunlar',            u'bu(bu)+Pron+Demons+A3pl(nlar[nlar])+Pnon+Nom')
        self.assert_parse_correct(u'şunlar',            u'şu(şu)+Pron+Demons+A3pl(nlar[nlar])+Pnon+Nom')

        self.assert_parse_correct(u'bunu',              u'bu(bu)+Pron+Demons+A3sg+Pnon+Acc(nu[nu])')
        self.assert_parse_correct(u'şunu',              u'şu(şu)+Pron+Demons+A3sg+Pnon+Acc(nu[nu])')
        self.assert_parse_correct(u'bunları',           u'bu(bu)+Pron+Demons+A3pl(nlar[nlar])+Pnon+Acc(ı[ı])')
        self.assert_parse_correct(u'şunları',           u'şu(şu)+Pron+Demons+A3pl(nlar[nlar])+Pnon+Acc(ı[ı])')

        self.assert_parse_correct(u'nere',              u'nere(nere)+Pron+Ques+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'nereyi',            u'nere(nere)+Pron+Ques+A3sg+Pnon+Acc(+yI[yi])')
        self.assert_parse_correct(u'nereye',            u'nere(nere)+Pron+Ques+A3sg+Pnon+Dat(+yA[ye])')
        self.assert_parse_correct(u'nerede',            u'nere(nere)+Pron+Ques+A3sg+Pnon+Loc(dA[de])', u'nerede(nerede)+Interj')
        self.assert_parse_correct(u'nereden',           u'nere(nere)+Pron+Ques+A3sg+Pnon+Abl(dAn[den])')
        self.assert_parse_correct(u'nerenin',           u'nere(nere)+Pron+Ques+A3sg+Pnon+Gen(+nIn[nin])', u'nere(nere)+Pron+Ques+A3sg+P2sg(+In[n])+Gen(+nIn[in])')
        self.assert_parse_correct(u'nereyle',           u'nere(nere)+Pron+Ques+A3sg+Pnon+Ins(+ylA[yle])')

        self.assert_parse_correct(u'nerem',             u'nere(nere)+Pron+Ques+A3sg+P1sg(+Im[m])+Nom')
        self.assert_parse_correct(u'neren',             u'nere(nere)+Pron+Ques+A3sg+P2sg(+In[n])+Nom')
        self.assert_parse_correct(u'neresi',            u'nere(nere)+Pron+Ques+A3sg+P3sg(+sI[si])+Nom')
        self.assert_parse_correct(u'neremiz',           u'nere(nere)+Pron+Ques+A3sg+P1pl(+ImIz[miz])+Nom')
        self.assert_parse_correct(u'nereniz',           u'nere(nere)+Pron+Ques+A3sg+P2pl(+InIz[niz])+Nom')
        self.assert_parse_correct(u'nereleri',          u'nere(nere)+Pron+Ques+A3sg+P3pl(lArI![leri])+Nom', u'nere(nere)+Pron+Ques+A3pl(lAr[ler])+Pnon+Acc(+yI[i])', u'nere(nere)+Pron+Ques+A3pl(lAr[ler])+P3sg(+sI[i])+Nom', u'nere(nere)+Pron+Ques+A3pl(lAr[ler])+P3pl(I![i])+Nom')

        self.assert_parse_correct(u'nerenden',          u'nere(nere)+Pron+Ques+A3sg+P2sg(+In[n])+Abl(dAn[den])')
        self.assert_parse_correct(u'neresine',          u'nere(nere)+Pron+Ques+A3sg+P3sg(+sI[si])+Dat(nA[ne])')

        self.assert_parse_correct(u'kimse',              u'kimse(kimse)+Pron+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'kimseyi',            u'kimse(kimse)+Pron+A3sg+Pnon+Acc(+yI[yi])')
        self.assert_parse_correct(u'kimseye',            u'kimse(kimse)+Pron+A3sg+Pnon+Dat(+yA[ye])')
        self.assert_parse_correct(u'kimsede',            u'kimse(kimse)+Pron+A3sg+Pnon+Loc(dA[de])')
        self.assert_parse_correct(u'kimseden',           u'kimse(kimse)+Pron+A3sg+Pnon+Abl(dAn[den])')
        self.assert_parse_correct(u'kimsenin',           u'kimse(kimse)+Pron+A3sg+Pnon+Gen(+nIn[nin])', u'kimse(kimse)+Pron+A3sg+P2sg(+In[n])+Gen(+nIn[in])')
        self.assert_parse_correct(u'kimseyle',           u'kimse(kimse)+Pron+A3sg+Pnon+Ins(+ylA[yle])')

        self.assert_parse_correct(u'kimsem',             u'kimse(kimse)+Pron+A3sg+P1sg(+Im[m])+Nom')
        self.assert_parse_correct(u'kimsen',             u'kimse(kimse)+Pron+A3sg+P2sg(+In[n])+Nom')
        self.assert_parse_correct(u'kimsesi',            u'kimse(kimse)+Pron+A3sg+P3sg(+sI[si])+Nom')
        self.assert_parse_correct(u'kimsemiz',           u'kimse(kimse)+Pron+A3sg+P1pl(+ImIz[miz])+Nom')
        self.assert_parse_correct(u'kimseniz',           u'kimse(kimse)+Pron+A3sg+P2pl(+InIz[niz])+Nom')
        self.assert_parse_correct(u'kimseleri',          u'kimse(kimse)+Pron+A3sg+P3pl(lArI![leri])+Nom', u'kimse(kimse)+Pron+A3pl(lAr[ler])+Pnon+Acc(+yI[i])', u'kimse(kimse)+Pron+A3pl(lAr[ler])+P3sg(+sI[i])+Nom', u'kimse(kimse)+Pron+A3pl(lAr[ler])+P3pl(I![i])+Nom')
        self.assert_parse_correct(u'kimselerim',         u'kimse(kimse)+Pron+A3pl(lAr[ler])+P1sg(+Im[im])+Nom')
        self.assert_parse_correct(u'kimselerimizde',     u'kimse(kimse)+Pron+A3pl(lAr[ler])+P1pl(+ImIz[imiz])+Loc(dA[de])')
        self.assert_parse_correct(u'kimseler',           u'kimse(kimse)+Pron+A3pl(lAr[ler])+Pnon+Nom')

        self.assert_parse_correct(u'kimsecikler',        u'kimsecik(kimsecik)+Pron+A3pl(lAr[ler])+Pnon+Nom')
        self.assert_parse_correct(u'kimseciklerde',      u'kimsecik(kimsecik)+Pron+A3pl(lAr[ler])+Pnon+Loc(dA[de])')


        self.assert_parse_correct(u'nerenden',          u'nere(nere)+Pron+Ques+A3sg+P2sg(+In[n])+Abl(dAn[den])')

        self.assert_parse_correct(u'kimimizle',         u'kim(kim)+Pron+Ques+A3sg+P1pl(+ImIz[imiz])+Ins(+ylA[le])', u'kimi(kimi)+Pron+A3sg+P1pl(miz[miz])+Ins(+ylA[le])')
        self.assert_parse_correct(u'kimleri',           u'kim(kim)+Pron+Ques+A3sg+P3pl(lArI![leri])+Nom', u'kim(kim)+Pron+Ques+A3pl(lAr[ler])+Pnon+Acc(+yI[i])', u'kim(kim)+Pron+Ques+A3pl(lAr[ler])+P3sg(+sI[i])+Nom', u'kim(kim)+Pron+Ques+A3pl(lAr[ler])+P3pl(I![i])+Nom')
        self.assert_parse_correct(u'kimlerimiz',        u'kim(kim)+Pron+Ques+A3pl(lAr[ler])+P1pl(+ImIz[imiz])+Nom')
        self.assert_parse_correct(u'kimlerimize',       u'kim(kim)+Pron+Ques+A3pl(lAr[ler])+P1pl(+ImIz[imiz])+Dat(+yA[e])')
        self.assert_parse_correct(u'kimlerimizin',      u'kim(kim)+Pron+Ques+A3pl(lAr[ler])+P1pl(+ImIz[imiz])+Gen(+nIn[in])')

        self.assert_parse_correct(u'kimim',             u'kim(kim)+Pron+Ques+A3sg+P1sg(+Im[im])+Nom')
        self.assert_parse_correct(u'kimin',             u'kim(kim)+Pron+Ques+A3sg+P2sg(+In[in])+Nom', u'kim(kim)+Pron+Ques+A3sg+Pnon+Gen(+nIn[in])')

        self.assert_parse_correct(u'bura',              u'bura(bura)+Pron+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'burayı',            u'bura(bura)+Pron+A3sg+Pnon+Acc(+yI[yı])')
        self.assert_parse_correct(u'buraya',            u'bura(bura)+Pron+A3sg+Pnon+Dat(+yA[ya])')
        self.assert_parse_correct(u'burada',            u'bura(bura)+Pron+A3sg+Pnon+Loc(dA[da])')
        self.assert_parse_correct(u'buradan',           u'bura(bura)+Pron+A3sg+Pnon+Abl(dAn[dan])')
        self.assert_parse_correct(u'buranın',           u'bura(bura)+Pron+A3sg+Pnon+Gen(+nIn[nın])', u'bura(bura)+Pron+A3sg+P2sg(+In[n])+Gen(+nIn[ın])')
        self.assert_parse_correct(u'burayla',           u'bura(bura)+Pron+A3sg+Pnon+Ins(+ylA[yla])')

        self.assert_parse_correct(u'buram',             u'bura(bura)+Pron+A3sg+P1sg(+Im[m])+Nom')
        self.assert_parse_correct(u'buran',             u'bura(bura)+Pron+A3sg+P2sg(+In[n])+Nom')
        self.assert_parse_correct(u'burası',            u'bura(bura)+Pron+A3sg+P3sg(+sI[sı])+Nom')
        self.assert_parse_correct(u'buramız',           u'bura(bura)+Pron+A3sg+P1pl(+ImIz[mız])+Nom')
        self.assert_parse_correct(u'buranız',           u'bura(bura)+Pron+A3sg+P2pl(+InIz[nız])+Nom')
        self.assert_parse_correct(u'buraları',          u'bura(bura)+Pron+A3sg+P3pl(lArI![ları])+Nom', u'bura(bura)+Pron+A3pl(lAr[lar])+Pnon+Acc(+yI[ı])', u'bura(bura)+Pron+A3pl(lAr[lar])+P3sg(+sI[ı])+Nom', u'bura(bura)+Pron+A3pl(lAr[lar])+P3pl(I![ı])+Nom')

        self.assert_parse_correct(u'burandan',          u'bura(bura)+Pron+A3sg+P2sg(+In[n])+Abl(dAn[dan])')
        self.assert_parse_correct(u'burasına',          u'bura(bura)+Pron+A3sg+P3sg(+sI[sı])+Dat(nA[na])')

        self.assert_parse_correct(u'oradan',            u'ora(ora)+Pron+A3sg+Pnon+Abl(dAn[dan])')
        self.assert_parse_correct(u'şuranla',           u'şura(şura)+Pron+A3sg+P2sg(+In[n])+Ins(+ylA[la])')

    def test_should_parse_point_qualifiers(self):
        self.cloned_root_map[u'masad'] = []
        self.cloned_root_map[u'bend'] = []
        self.cloned_root_map[u'on'] = []
        self.cloned_root_map[u'yar'] = []
        self.cloned_root_map[u'bizle'] = []
        self.cloned_root_map[u'ben'] = filter(lambda root : root.lexeme.syntactic_category==SyntacticCategory.PRONOUN, self.cloned_root_map[u'ben'])
        self.cloned_root_map[u'biz'] = filter(lambda root : root.lexeme.syntactic_category==SyntacticCategory.PRONOUN, self.cloned_root_map[u'biz'])

        self.assert_parse_correct(u'masadaki',             u'masa(masa)+Noun+A3sg+Pnon+Loc(dA[da])+Adj+PointQual(ki[ki])', u'masa(masa)+Noun+A3sg+Pnon+Loc(dA[da])+Adj+PointQual(ki[ki])+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'masamdaki',            u'masa(masa)+Noun+A3sg+P1sg(+Im[m])+Loc(dA[da])+Adj+PointQual(ki[ki])', u'masa(masa)+Noun+A3sg+P1sg(+Im[m])+Loc(dA[da])+Adj+PointQual(ki[ki])+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'masalarındaki',        u'masa(masa)+Noun+A3sg+P3pl(lArI![ları])+Loc(ndA[nda])+Adj+PointQual(ki[ki])', u'masa(masa)+Noun+A3pl(lAr[lar])+P2sg(+In[ın])+Loc(dA[da])+Adj+PointQual(ki[ki])', u'masa(masa)+Noun+A3pl(lAr[lar])+P3sg(+sI[ı])+Loc(ndA[nda])+Adj+PointQual(ki[ki])', u'masa(masa)+Noun+A3pl(lAr[lar])+P3pl(I![ı])+Loc(ndA[nda])+Adj+PointQual(ki[ki])', u'masa(masa)+Noun+A3sg+P3pl(lArI![ları])+Loc(ndA[nda])+Adj+PointQual(ki[ki])+Noun+Zero+A3sg+Pnon+Nom', u'masa(masa)+Noun+A3pl(lAr[lar])+P2sg(+In[ın])+Loc(dA[da])+Adj+PointQual(ki[ki])+Noun+Zero+A3sg+Pnon+Nom', u'masa(masa)+Noun+A3pl(lAr[lar])+P3sg(+sI[ı])+Loc(ndA[nda])+Adj+PointQual(ki[ki])+Noun+Zero+A3sg+Pnon+Nom', u'masa(masa)+Noun+A3pl(lAr[lar])+P3pl(I![ı])+Loc(ndA[nda])+Adj+PointQual(ki[ki])+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'kısadaki',             u'kısa(kısa)+Adj+Noun+Zero+A3sg+Pnon+Loc(dA[da])+Adj+PointQual(ki[ki])', u'kısa(kısa)+Adj+Noun+Zero+A3sg+Pnon+Loc(dA[da])+Adj+PointQual(ki[ki])+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'bendeki',              u'ben(ben)+Pron+Pers+A1sg+Pnon+Loc(de[de])+Adj+PointQual(ki[ki])', u'ben(ben)+Pron+Pers+A1sg+Pnon+Loc(de[de])+Adj+PointQual(ki[ki])+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'ondaki',               u'o(o)+Pron+Demons+A3sg+Pnon+Loc(nda[nda])+Adj+PointQual(ki[ki])', u'o(o)+Pron+Pers+A3sg+Pnon+Loc(nda[nda])+Adj+PointQual(ki[ki])', u'o(o)+Pron+Demons+A3sg+Pnon+Loc(nda[nda])+Adj+PointQual(ki[ki])+Noun+Zero+A3sg+Pnon+Nom', u'o(o)+Pron+Pers+A3sg+Pnon+Loc(nda[nda])+Adj+PointQual(ki[ki])+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'bizlerdeki',           u'biz(biz)+Pron+Pers+A1pl(ler[ler])+Pnon+Loc(de[de])+Adj+PointQual(ki[ki])', u'biz(biz)+Pron+Pers+A1pl(ler[ler])+Pnon+Loc(de[de])+Adj+PointQual(ki[ki])+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'küçüğümdekilere',      u'küçüğ(küçük)+Adj+Noun+Zero+A3sg+P1sg(+Im[üm])+Loc(dA[de])+Adj+PointQual(ki[ki])+Noun+Zero+A3pl(lAr[ler])+Pnon+Dat(+yA[e])')
        self.assert_parse_correct(u'küçüğümdekilerde',     u'küçüğ(küçük)+Adj+Noun+Zero+A3sg+P1sg(+Im[üm])+Loc(dA[de])+Adj+PointQual(ki[ki])+Noun+Zero+A3pl(lAr[ler])+Pnon+Loc(dA[de])')
        self.assert_parse_correct(u'küçüğümdekilerdeki',   u'küçüğ(küçük)+Adj+Noun+Zero+A3sg+P1sg(+Im[üm])+Loc(dA[de])+Adj+PointQual(ki[ki])+Noun+Zero+A3pl(lAr[ler])+Pnon+Loc(dA[de])+Adj+PointQual(ki[ki])', u'küçüğ(küçük)+Adj+Noun+Zero+A3sg+P1sg(+Im[üm])+Loc(dA[de])+Adj+PointQual(ki[ki])+Noun+Zero+A3pl(lAr[ler])+Pnon+Loc(dA[de])+Adj+PointQual(ki[ki])+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'oradaki',              u'ora(ora)+Pron+A3sg+Pnon+Loc(dA[da])+Adj+PointQual(ki[ki])', u'ora(ora)+Pron+A3sg+Pnon+Loc(dA[da])+Adj+PointQual(ki[ki])+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'oradakilerin',         u'ora(ora)+Pron+A3sg+Pnon+Loc(dA[da])+Adj+PointQual(ki[ki])+Noun+Zero+A3pl(lAr[ler])+Pnon+Gen(+nIn[in])')
        self.assert_parse_correct(u'yarınki',              u'yarın(yarın)+Adv+Time+Adj+PointQual(ki[ki])', u'yarın(yarın)+Adv+Time+Adj+PointQual(ki[ki])+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'bugünkünden',          u'bugün(bugün)+Adv+Time+Adj+PointQual(kü[kü])+Noun+Zero+A3sg+Pnon+Abl(ndAn[nden])')
        self.assert_parse_correct(u'bugünkülerden',        u'bugün(bugün)+Adv+Time+Adj+PointQual(kü[kü])+Noun+Zero+A3pl(lAr[ler])+Pnon+Abl(dAn[den])')
        self.assert_parse_correct(u'dünkünün',             u'dün(dün)+Adv+Adj+PointQual(kü[kü])+Noun+Zero+A3sg+Pnon+Gen(+nIn[nün])')
        self.assert_parse_correct(u'bendekileri',          u'ben(ben)+Pron+Pers+A1sg+Pnon+Loc(de[de])+Adj+PointQual(ki[ki])+Noun+Zero+A3pl(lAr[ler])+Pnon+Acc(+yI[i])')

        self.assert_not_parsable(u'masadakim')
        self.assert_not_parsable(u'masamdakin')
        self.assert_not_parsable(u'masalarındakisi')
        self.assert_not_parsable(u'sekizdekimiz')
        self.assert_not_parsable(u'kısadakiniz')
        self.assert_not_parsable(u'ondakisi')
        self.assert_not_parsable(u'bizlerdekim')
        self.assert_not_parsable(u'küçüğümdekilerdekiniz')
        self.assert_not_parsable(u'oradakim')
        self.assert_not_parsable(u'oradakilerisi')
        self.assert_not_parsable(u'oradakilerinden')
        self.assert_not_parsable(u'yarınkim')
        self.assert_not_parsable(u'yarınkin')
        self.assert_not_parsable(u'dünküsü')
        self.assert_not_parsable(u'bendekimiz')

        self.assert_parse_correct(u'masadakini',             u'masa(masa)+Noun+A3sg+Pnon+Loc(dA[da])+Adj+PointQual(ki[ki])+Noun+Zero+A3sg+Pnon+Acc(nI[ni])')
        self.assert_parse_correct(u'masamdakine',            u'masa(masa)+Noun+A3sg+P1sg(+Im[m])+Loc(dA[da])+Adj+PointQual(ki[ki])+Noun+Zero+A3sg+Pnon+Dat(nA[ne])')
        self.assert_parse_correct(u'masalarındakinde',       u'masa(masa)+Noun+A3sg+P3pl(lArI![ları])+Loc(ndA[nda])+Adj+PointQual(ki[ki])+Noun+Zero+A3sg+Pnon+Loc(ndA[nde])', u'masa(masa)+Noun+A3pl(lAr[lar])+P2sg(+In[ın])+Loc(dA[da])+Adj+PointQual(ki[ki])+Noun+Zero+A3sg+Pnon+Loc(ndA[nde])', u'masa(masa)+Noun+A3pl(lAr[lar])+P3sg(+sI[ı])+Loc(ndA[nda])+Adj+PointQual(ki[ki])+Noun+Zero+A3sg+Pnon+Loc(ndA[nde])', u'masa(masa)+Noun+A3pl(lAr[lar])+P3pl(I![ı])+Loc(ndA[nda])+Adj+PointQual(ki[ki])+Noun+Zero+A3sg+Pnon+Loc(ndA[nde])')
        self.assert_parse_correct(u'kısadakini',             u'kısa(kısa)+Adj+Noun+Zero+A3sg+Pnon+Loc(dA[da])+Adj+PointQual(ki[ki])+Noun+Zero+A3sg+Pnon+Acc(nI[ni])')
        self.assert_parse_correct(u'bendekinden',            u'ben(ben)+Pron+Pers+A1sg+Pnon+Loc(de[de])+Adj+PointQual(ki[ki])+Noun+Zero+A3sg+Pnon+Abl(ndAn[nden])')
        self.assert_parse_correct(u'ondakinde',              u'o(o)+Pron+Demons+A3sg+Pnon+Loc(nda[nda])+Adj+PointQual(ki[ki])+Noun+Zero+A3sg+Pnon+Loc(ndA[nde])', u'o(o)+Pron+Pers+A3sg+Pnon+Loc(nda[nda])+Adj+PointQual(ki[ki])+Noun+Zero+A3sg+Pnon+Loc(ndA[nde])')
        self.assert_parse_correct(u'bendekine',              u'ben(ben)+Pron+Pers+A1sg+Pnon+Loc(de[de])+Adj+PointQual(ki[ki])+Noun+Zero+A3sg+Pnon+Dat(nA[ne])')
        self.assert_parse_correct(u'bizdekine',              u'biz(biz)+Pron+Pers+A1pl+Pnon+Loc(de[de])+Adj+PointQual(ki[ki])+Noun+Zero+A3sg+Pnon+Dat(nA[ne])')
        self.assert_parse_correct(u'bizlerdekine',           u'biz(biz)+Pron+Pers+A1pl(ler[ler])+Pnon+Loc(de[de])+Adj+PointQual(ki[ki])+Noun+Zero+A3sg+Pnon+Dat(nA[ne])')
        self.assert_parse_correct(u'küçüğümdekilerdekinden', u'küçüğ(küçük)+Adj+Noun+Zero+A3sg+P1sg(+Im[üm])+Loc(dA[de])+Adj+PointQual(ki[ki])+Noun+Zero+A3pl(lAr[ler])+Pnon+Loc(dA[de])+Adj+PointQual(ki[ki])+Noun+Zero+A3sg+Pnon+Abl(ndAn[nden])')
        self.assert_parse_correct(u'oradakine',              u'ora(ora)+Pron+A3sg+Pnon+Loc(dA[da])+Adj+PointQual(ki[ki])+Noun+Zero+A3sg+Pnon+Dat(nA[ne])')
        self.assert_parse_correct(u'oradakilerden',          u'ora(ora)+Pron+A3sg+Pnon+Loc(dA[da])+Adj+PointQual(ki[ki])+Noun+Zero+A3pl(lAr[ler])+Pnon+Abl(dAn[den])')
        self.assert_parse_correct(u'bendekinin',             u'ben(ben)+Pron+Pers+A1sg+Pnon+Loc(de[de])+Adj+PointQual(ki[ki])+Noun+Zero+A3sg+Pnon+Gen(+nIn[nin])')
        self.assert_parse_correct(u'ankini',                 u'an(an)+Adv+Time+Adj+PointQual(ki[ki])+Noun+Zero+A3sg+Pnon+Acc(nI[ni])')
        self.assert_parse_correct(u'günkünde',               u'gün(gün)+Adv+Time+Adj+PointQual(kü[kü])+Noun+Zero+A3sg+Pnon+Loc(ndA[nde])')
        self.assert_parse_correct(u'dünkünden',              u'dün(dün)+Adv+Adj+PointQual(kü[kü])+Noun+Zero+A3sg+Pnon+Abl(ndAn[nden])')
        self.assert_parse_correct(u'zamankini',              u'zaman(zaman)+Adv+Time+Adj+PointQual(ki[ki])+Noun+Zero+A3sg+Pnon+Acc(nI[ni])')

    def test_should_parse_point_qualifiers_for_derived_adverbs(self):
        self.assert_parse_correct(u'yaparkenki',           u'yap(yapmak)+Verb+Pos+Aor(+Ar[ar])+Adv+While(ken[ken])+Adj+PointQual(ki[ki])', u'yap(yapmak)+Verb+Pos+Aor(+Ar[ar])+Adv+While(ken[ken])+Adj+PointQual(ki[ki])+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'yapıncaki',            u'yap(yapmak)+Verb+Pos+Adv+When(+yIncA[ınca])+Adj+PointQual(ki[ki])', u'yap(yapmak)+Verb+Pos+Adv+When(+yIncA[ınca])+Adj+PointQual(ki[ki])+Noun+Zero+A3sg+Pnon+Nom')

        # there are more forms of derived adverbs, but they don't make sense with "ki" suffix

    def test_should_parse_pronoun_derivations(self):
        self.cloned_root_map[u'on'] = []
        self.cloned_root_map[u'biz'] = filter(lambda root : root.lexeme.syntactic_category==SyntacticCategory.PRONOUN, self.cloned_root_map[u'biz'])

        self.assert_parse_correct(u'bensiz',
            u'ben(ben)+Pron+Pers+A1sg+Pnon+Nom+Adj+Without(sIz[siz])',
            u'ben(ben)+Noun+A3sg+Pnon+Nom+Adj+Without(sIz[siz])',
            u'ben(ben)+Pron+Pers+A1sg+Pnon+Nom+Adj+Without(sIz[siz])+Noun+Zero+A3sg+Pnon+Nom',
            u'ben(ben)+Noun+A3sg+Pnon+Nom+Adj+Without(sIz[siz])+Noun+Zero+A3sg+Pnon+Nom'
        )   #TODO: what about 3?
        self.assert_parse_correct(u'sensiz',
            u'sen(sen)+Pron+Pers+A2sg+Pnon+Nom+Adj+Without(sIz[siz])',
            u'sen(sen)+Pron+Pers+A2sg+Pnon+Nom+Adj+Without(sIz[siz])+Noun+Zero+A3sg+Pnon+Nom'
        )
        self.assert_parse_correct(u'onsuz',
            u'o(o)+Pron+Pers+A3sg+Pnon+Nom+Adj+Without(nsuz[nsuz])',
            u'o(o)+Pron+Demons+A3sg+Pnon+Nom+Adj+Without(nsuz[nsuz])',
            u'o(o)+Pron+Pers+A3sg+Pnon+Nom+Adj+Without(nsuz[nsuz])+Noun+Zero+A3sg+Pnon+Nom',
            u'o(o)+Pron+Demons+A3sg+Pnon+Nom+Adj+Without(nsuz[nsuz])+Noun+Zero+A3sg+Pnon+Nom'
        )
        self.assert_parse_correct(u'bizsiz',
            u'biz(biz)+Pron+Pers+A1pl+Pnon+Nom+Adj+Without(sIz[siz])',
            u'biz(biz)+Pron+Pers+A1pl+Pnon+Nom+Adj+Without(sIz[siz])+Noun+Zero+A3sg+Pnon+Nom'
        )
        self.assert_parse_correct(u'sizsiz',
            u'siz(siz)+Pron+Pers+A2pl+Pnon+Nom+Adj+Without(sIz[siz])',
            u'siz(siz)+Pron+Pers+A2pl+Pnon+Nom+Adj+Without(sIz[siz])+Noun+Zero+A3sg+Pnon+Nom'
        )
        self.assert_parse_correct(u'onlarsız',
            u'o(o)+Pron+Pers+A3pl(nlar[nlar])+Pnon+Nom+Adj+Without(sIz[sız])',
            u'o(o)+Pron+Demons+A3pl(nlar[nlar])+Pnon+Nom+Adj+Without(sIz[sız])',
            u'o(o)+Pron+Pers+A3pl(nlar[nlar])+Pnon+Nom+Adj+Without(sIz[sız])+Noun+Zero+A3sg+Pnon+Nom',
            u'o(o)+Pron+Demons+A3pl(nlar[nlar])+Pnon+Nom+Adj+Without(sIz[sız])+Noun+Zero+A3sg+Pnon+Nom'
        )
        self.assert_parse_correct(u'bunsuz',
            u'bu(bu)+Pron+Demons+A3sg+Pnon+Nom+Adj+Without(nsuz[nsuz])',
            u'bun(bun)+Noun+A3sg+Pnon+Nom+Adj+Without(sIz[suz])',
            u'bu(bu)+Pron+Demons+A3sg+Pnon+Nom+Adj+Without(nsuz[nsuz])+Noun+Zero+A3sg+Pnon+Nom',
            u'bun(bun)+Noun+A3sg+Pnon+Nom+Adj+Without(sIz[suz])+Noun+Zero+A3sg+Pnon+Nom'
        )
        self.assert_parse_correct(u'şunsuz',
            u'şu(şu)+Pron+Demons+A3sg+Pnon+Nom+Adj+Without(nsuz[nsuz])',
            u'şu(şu)+Pron+Demons+A3sg+Pnon+Nom+Adj+Without(nsuz[nsuz])+Noun+Zero+A3sg+Pnon+Nom'
        )
        self.assert_parse_correct(u'bunlarsız',
            u'bu(bu)+Pron+Demons+A3pl(nlar[nlar])+Pnon+Nom+Adj+Without(sIz[sız])',
            u'bu(bu)+Pron+Demons+A3pl(nlar[nlar])+Pnon+Nom+Adj+Without(sIz[sız])+Noun+Zero+A3sg+Pnon+Nom'
        )
        self.assert_parse_correct(u'şunlarsız',
            u'şu(şu)+Pron+Demons+A3pl(nlar[nlar])+Pnon+Nom+Adj+Without(sIz[sız])',
            u'şu(şu)+Pron+Demons+A3pl(nlar[nlar])+Pnon+Nom+Adj+Without(sIz[sız])+Noun+Zero+A3sg+Pnon+Nom'
        )

    def test_should_parse_some_imperatives(self):
        self.cloned_root_map[u'gelin'] = []
        self.cloned_root_map[u'ge'] = []

        self.assert_parse_correct_for_verb(u'gel',               u'gel(gelmek)+Verb+Pos+Imp+A2sg')
        self.assert_parse_correct_for_verb(u'gelsin',            u'gel(gelmek)+Verb+Pos+Imp+A3sg(sIn[sin])')
        self.assert_parse_correct_for_verb(u'gelin',             u'gel(gelmek)+Verb+Pos+Imp+A2pl(+yIn[in])', u'gel(gelmek)+Verb+Verb+Pass(+In[in])+Pos+Imp+A2sg')
        self.assert_parse_correct_for_verb(u'geliniz',           u'gel(gelmek)+Verb+Pos+Imp+A2pl(+yInIz[iniz])')
        self.assert_parse_correct_for_verb(u'gelsinler',         u'gel(gelmek)+Verb+Pos+Imp+A3pl(sInlAr[sinler])')

        self.assert_parse_correct_for_verb(u'gelme',             u'gel(gelmek)+Verb+Neg(mA[me])+Imp+A2sg', u'gel(gelmek)+Verb+Pos+Noun+Inf(mA[me])+A3sg+Pnon+Nom')
        self.assert_parse_correct_for_verb(u'gelmesin',          u'gel(gelmek)+Verb+Neg(mA[me])+Imp+A3sg(sIn[sin])')
        self.assert_parse_correct_for_verb(u'gelmeyin',          u'gel(gelmek)+Verb+Neg(mA[me])+Imp+A2pl(+yIn[yin])')
        self.assert_parse_correct_for_verb(u'gelmeyiniz',        u'gel(gelmek)+Verb+Neg(mA[me])+Imp+A2pl(+yInIz[yiniz])')
        self.assert_parse_correct_for_verb(u'gelmesinler',       u'gel(gelmek)+Verb+Neg(mA[me])+Imp+A3pl(sInlAr[sinler])')

        self.assert_parse_correct_for_verb(u'söyle',             u'söyle(söylemek)+Verb+Pos+Imp+A2sg')
        self.assert_parse_correct_for_verb(u'söylesin',          u'söyle(söylemek)+Verb+Pos+Imp+A3sg(sIn[sin])')
        self.assert_parse_correct_for_verb(u'söyleyin',          u'söyle(söylemek)+Verb+Pos+Imp+A2pl(+yIn[yin])')
        self.assert_parse_correct_for_verb(u'söyleyiniz',        u'söyle(söylemek)+Verb+Pos+Imp+A2pl(+yInIz[yiniz])')
        self.assert_parse_correct_for_verb(u'söylesinler',       u'söyle(söylemek)+Verb+Pos+Imp+A3pl(sInlAr[sinler])')

        self.assert_parse_correct_for_verb(u'söyleme',
            u'söyle(söylemek)+Verb+Neg(mA[me])+Imp+A2sg',
            u'söylem(söylem)+Noun+A3sg+Pnon+Dat(+yA[e])',
            u'söyle(söylemek)+Verb+Pos+Noun+Inf(mA[me])+A3sg+Pnon+Nom'
        )
        self.assert_parse_correct_for_verb(u'söylemesin',
            u'söyle(söylemek)+Verb+Neg(mA[me])+Imp+A3sg(sIn[sin])'
        )
        self.assert_parse_correct_for_verb(u'söylemeyin',        u'söyle(söylemek)+Verb+Neg(mA[me])+Imp+A2pl(+yIn[yin])')
        self.assert_parse_correct_for_verb(u'söylemeyiniz',      u'söyle(söylemek)+Verb+Neg(mA[me])+Imp+A2pl(+yInIz[yiniz])')
        self.assert_parse_correct_for_verb(u'söylemesinler',     u'söyle(söylemek)+Verb+Neg(mA[me])+Imp+A3pl(sInlAr[sinler])')

    def test_should_parse_verb_to_noun_derivations(self):
        self.assert_parse_correct(u'yapmak',            u'yap(yapmak)+Verb+Pos+Noun+Inf(mAk[mak])+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'yapma',             u'yap(yapmak)+Verb+Neg(mA[ma])+Imp+A2sg', u'yap(yapmak)+Verb+Pos+Noun+Inf(mA[ma])+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'yapış',             u'yapış(yapışmak)+Verb+Pos+Imp+A2sg', u'yap(yapmak)+Verb+Verb+Recip(+Iş[ış])+Pos+Imp+A2sg', u'yap(yapmak)+Verb+Pos+Noun+Inf(+yIş[ış])+A3sg+Pnon+Nom')

        self.assert_parse_correct(u'gelmek',            u'gel(gelmek)+Verb+Pos+Noun+Inf(mAk[mek])+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'gelme',             u'gel(gelmek)+Verb+Neg(mA[me])+Imp+A2sg', u'gel(gelmek)+Verb+Pos+Noun+Inf(mA[me])+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'geliş',             u'geliş(gelişmek)+Verb+Pos+Imp+A2sg', u'gel(gelmek)+Verb+Verb+Recip(+Iş[iş])+Pos+Imp+A2sg', u'gel(gelmek)+Verb+Pos+Noun+Inf(+yIş[iş])+A3sg+Pnon+Nom')

        self.assert_parse_correct(u'söylemek',          u'söyle(söylemek)+Verb+Pos+Noun+Inf(mAk[mek])+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'söyleme',           u'söyle(söylemek)+Verb+Neg(mA[me])+Imp+A2sg', u'söylem(söylem)+Noun+A3sg+Pnon+Dat(+yA[e])', u'söyle(söylemek)+Verb+Pos+Noun+Inf(mA[me])+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'söyleyiş',          u'söyle(söylemek)+Verb+Pos+Noun+Inf(+yIş[yiş])+A3sg+Pnon+Nom')

        self.assert_parse_correct(u'yapmamak',          u'yap(yapmak)+Verb+Neg(mA[ma])+Noun+Inf(mAk[mak])+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'yapmama',           u'yap(yapmak)+Verb+Neg(mA[ma])+Noun+Inf(mA[ma])+A3sg+Pnon+Nom', u'yap(yapmak)+Verb+Pos+Noun+Inf(mA[ma])+A3sg+P1sg(+Im[m])+Dat(+yA[a])')
        self.assert_parse_correct(u'yapmayış',          u'yap(yapmak)+Verb+Neg(mA[ma])+Noun+Inf(+yIş[yış])+A3sg+Pnon+Nom')

        self.assert_parse_correct(u'gelmemek',          u'gel(gelmek)+Verb+Neg(mA[me])+Noun+Inf(mAk[mek])+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'gelmeyiş',          u'gel(gelmek)+Verb+Neg(mA[me])+Noun+Inf(+yIş[yiş])+A3sg+Pnon+Nom')

        self.assert_parse_correct(u'söylememek',        u'söyle(söylemek)+Verb+Neg(mA[me])+Noun+Inf(mAk[mek])+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'söylememe',         u'söyle(söylemek)+Verb+Neg(mA[me])+Noun+Inf(mA[me])+A3sg+Pnon+Nom', u'söyle(söylemek)+Verb+Pos+Noun+Inf(mA[me])+A3sg+P1sg(+Im[m])+Dat(+yA[e])')
        self.assert_parse_correct(u'söylemeyiş',        u'söyle(söylemek)+Verb+Neg(mA[me])+Noun+Inf(+yIş[yiş])+A3sg+Pnon+Nom')

    def test_should_parse_passives(self):
        self.assert_parse_correct_for_verb(u'yazıldı',         u'yaz(yazmak)+Verb+Verb+Pass(+nIl[ıl])+Pos+Past(dI[dı])+A3sg')
        self.assert_parse_correct_for_verb(u'yaptırıldı',      u'yap(yapmak)+Verb+Verb+Caus(dIr[tır])+Verb+Pass(+nIl[ıl])+Pos+Past(dI[dı])+A3sg')
        self.assert_parse_correct_for_verb(u'geliniyor',       u'gel(gelmek)+Verb+Verb+Pass(+In[in])+Pos+Prog(Iyor[iyor])+A3sg')
        self.assert_parse_correct_for_verb(u'düşüldü',         u'düş(düşmek)+Verb+Verb+Pass(+nIl[ül])+Pos+Past(dI[dü])+A3sg')
        self.assert_parse_correct_for_verb(u'düşünüldü',       u'düşün(düşünmek)+Verb+Verb+Pass(+nIl[ül])+Pos+Past(dI[dü])+A3sg')
        self.assert_parse_correct_for_verb(u'silinecekti',     u'sil(silmek)+Verb+Verb+Pass(+In[in])+Pos+Fut(+yAcAk[ecek])+Past(dI[ti])+A3sg')
        self.assert_parse_correct_for_verb(u'dendi',           u'de(demek)+Verb+Verb+Pass(+In[n])+Pos+Past(dI[di])+A3sg')
        self.assert_parse_correct_for_verb(u'denildi',         u'de(demek)+Verb+Verb+Pass(+InIl[nil])+Pos+Past(dI[di])+A3sg')
        self.assert_parse_correct_for_verb(u'yendi',           u'yen(yenmek)+Verb+Pos+Past(dI[di])+A3sg', u'ye(yemek)+Verb+Verb+Pass(+In[n])+Pos+Past(dI[di])+A3sg')
        self.assert_parse_correct_for_verb(u'yenildi',         u'ye(yemek)+Verb+Verb+Pass(+InIl[nil])+Pos+Past(dI[di])+A3sg', u'yen(yenmek)+Verb+Verb+Pass(+nIl[il])+Pos+Past(dI[di])+A3sg')

        self.cloned_root_map[u'ye'] = []
        self.assert_parse_correct_for_verb(u'yerleştirilmiş',  u'yerleş(yerleşmek)+Verb+Verb+Caus(dIr[tir])+Verb+Pass(+nIl[il])+Pos+Narr(mIş[miş])+A3sg', u'yerleş(yerleşmek)+Verb+Verb+Caus(dIr[tir])+Verb+Pass(+nIl[il])+Pos+Narr(mIş[miş])+Adj+Zero', u'yerleş(yerleşmek)+Verb+Verb+Caus(dIr[tir])+Verb+Pass(+nIl[il])+Pos+Narr(mIş[miş])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')

    def test_should_parse_causatives(self):
        self.assert_parse_correct_for_verb(u'düzelttim',         u'düzel(düzelmek)+Verb+Verb+Caus(t[t])+Pos+Past(dI[ti])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'çevirttim',         u'çevir(çevirmek)+Verb+Verb+Caus(t[t])+Pos+Past(dI[ti])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'kapattım',          u'kapa(kapamak)+Verb+Verb+Caus(t[t])+Pos+Past(dI[tı])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'bitirdim',          u'bit(bitmek)+Verb+Verb+Caus(Ir[ir])+Pos+Past(dI[di])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'yitirdim',          u'yit(yitmek)+Verb+Verb+Caus(Ir[ir])+Pos+Past(dI[di])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'ürküttüm',          u'ürk(ürkmek)+Verb+Verb+Caus(It[üt])+Pos+Past(dI[tü])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'çıkardım',          u'çık(çıkmak)+Verb+Pos+Aor(+Ar[ar])+Past(dI[dı])+A1sg(+Im[m])', u'çık(çıkmak)+Verb+Verb+Caus(Ar[ar])+Pos+Past(dI[dı])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'ettirdim',          u'et(etmek)+Verb+Verb+Caus(dIr[tir])+Pos+Past(dI[di])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'yaptırdım',         u'yap(yapmak)+Verb+Verb+Caus(dIr[tır])+Pos+Past(dI[dı])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'doldurdum',         u'dol(dolmak)+Verb+Verb+Caus(dIr[dur])+Pos+Past(dI[du])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'azalttım',          u'azal(azalmak)+Verb+Verb+Caus(t[t])+Pos+Past(dI[tı])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'azaltıyordu',       u'azal(azalmak)+Verb+Verb+Caus(t[t])+Pos+Prog(Iyor[ıyor])+Past(dI[du])+A3sg')
        self.assert_parse_correct_for_verb(u'sürdürülen',        u'sür(sürmek)+Verb+Verb+Caus(dIr[dür])+Verb+Pass(+nIl[ül])+Pos+Adj+PresPart(+yAn[en])', u'sür(sürmek)+Verb+Verb+Caus(dIr[dür])+Verb+Pass(+nIl[ül])+Pos+Adj+PresPart(+yAn[en])+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct_for_verb(u'kapatılmış',        u'kapa(kapamak)+Verb+Verb+Caus(t[t])+Verb+Pass(+nIl[ıl])+Pos+Narr(mIş[mış])+A3sg', u'kapa(kapamak)+Verb+Verb+Caus(t[t])+Verb+Pass(+nIl[ıl])+Pos+Narr(mIş[mış])+Adj+Zero', u'kapa(kapamak)+Verb+Verb+Caus(t[t])+Verb+Pass(+nIl[ıl])+Pos+Narr(mIş[mış])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct_for_verb(u'düşündürtüyordu',   u'düşün(düşünmek)+Verb+Verb+Caus(dIr[dür])+Verb+Caus(t[t])+Pos+Prog(Iyor[üyor])+Past(dI[du])+A3sg')
        self.assert_parse_correct_for_verb(u'korkutmamalı',      u'kork(korkmak)+Verb+Verb+Caus(It[ut])+Neg(mA[ma])+Neces(mAlI![malı])+A3sg', u'kork(korkmak)+Verb+Verb+Caus(It[ut])+Neg(mA[ma])+Noun+Inf(mA[ma])+A3sg+Pnon+Nom+Adj+With(lI[lı])', u'kork(korkmak)+Verb+Verb+Caus(It[ut])+Neg(mA[ma])+Noun+Inf(mA[ma])+A3sg+Pnon+Nom+Adj+With(lI[lı])+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct_for_verb(u'sıkıştırıldığı',    u's\u0131k(s\u0131kmak)+Verb+Verb+Recip(+I\u015f[\u0131\u015f])+Verb+Caus(dIr[t\u0131r])+Verb+Pass(+nIl[\u0131l])+Pos+Adj+PastPart(dIk[d\u0131\u011f])+P3sg(+sI[\u0131])', u's\u0131k(s\u0131kmak)+Verb+Verb+Recip(+I\u015f[\u0131\u015f])+Verb+Caus(dIr[t\u0131r])+Verb+Pass(+nIl[\u0131l])+Pos+Noun+PastPart(dIk[d\u0131\u011f])+A3sg+Pnon+Acc(+yI[\u0131])', u's\u0131k(s\u0131kmak)+Verb+Verb+Recip(+I\u015f[\u0131\u015f])+Verb+Caus(dIr[t\u0131r])+Verb+Pass(+nIl[\u0131l])+Pos+Noun+PastPart(dIk[d\u0131\u011f])+A3sg+P3sg(+sI[\u0131])+Nom')


    def test_should_parse_double_causatives(self):
        self.assert_parse_correct_for_verb(u'düzelttirdim',      u'düzel(düzelmek)+Verb+Verb+Caus(t[t])+Verb+Caus(dIr[tir])+Pos+Past(dI[di])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'çevirttirdim',      u'çevir(çevirmek)+Verb+Verb+Caus(t[t])+Verb+Caus(dIr[tir])+Pos+Past(dI[di])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'kapattırdım',       u'kapa(kapamak)+Verb+Verb+Caus(t[t])+Verb+Caus(dIr[tır])+Pos+Past(dI[dı])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'bitirttim',         u'bit(bitmek)+Verb+Verb+Caus(Ir[ir])+Verb+Caus(t[t])+Pos+Past(dI[ti])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'yitirttim',         u'yit(yitmek)+Verb+Verb+Caus(Ir[ir])+Verb+Caus(t[t])+Pos+Past(dI[ti])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'ürküttürdüm',       u'ürk(ürkmek)+Verb+Verb+Caus(It[üt])+Verb+Caus(dIr[tür])+Pos+Past(dI[dü])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'çıkarttım',         u'çık(çıkmak)+Verb+Verb+Caus(Ar[ar])+Verb+Caus(t[t])+Pos+Past(dI[tı])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'ettirttim',         u'et(etmek)+Verb+Verb+Caus(dIr[tir])+Verb+Caus(t[t])+Pos+Past(dI[ti])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'yaptırttım',        u'yap(yapmak)+Verb+Verb+Caus(dIr[tır])+Verb+Caus(t[t])+Pos+Past(dI[tı])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'doldurttum',        u'dol(dolmak)+Verb+Verb+Caus(dIr[dur])+Verb+Caus(t[t])+Pos+Past(dI[tu])+A1sg(+Im[m])')

    def test_should_parse_triple_causatives(self):
        self.assert_parse_correct_for_verb(u'düzelttirttim',     u'düzel(düzelmek)+Verb+Verb+Caus(t[t])+Verb+Caus(dIr[tir])+Verb+Caus(t[t])+Pos+Past(dI[ti])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'çevirttirttim',     u'çevir(çevirmek)+Verb+Verb+Caus(t[t])+Verb+Caus(dIr[tir])+Verb+Caus(t[t])+Pos+Past(dI[ti])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'kapattırttım',      u'kapa(kapamak)+Verb+Verb+Caus(t[t])+Verb+Caus(dIr[tır])+Verb+Caus(t[t])+Pos+Past(dI[tı])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'bitirttirdim',      u'bit(bitmek)+Verb+Verb+Caus(Ir[ir])+Verb+Caus(t[t])+Verb+Caus(dIr[tir])+Pos+Past(dI[di])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'yitirttirdim',      u'yit(yitmek)+Verb+Verb+Caus(Ir[ir])+Verb+Caus(t[t])+Verb+Caus(dIr[tir])+Pos+Past(dI[di])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'ürküttürttüm',      u'ürk(ürkmek)+Verb+Verb+Caus(It[üt])+Verb+Caus(dIr[tür])+Verb+Caus(t[t])+Pos+Past(dI[tü])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'çıkarttırdım',      u'çık(çıkmak)+Verb+Verb+Caus(Ar[ar])+Verb+Caus(t[t])+Verb+Caus(dIr[tır])+Pos+Past(dI[dı])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'ettirttirdim',      u'et(etmek)+Verb+Verb+Caus(dIr[tir])+Verb+Caus(t[t])+Verb+Caus(dIr[tir])+Pos+Past(dI[di])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'yaptırttırdım',     u'yap(yapmak)+Verb+Verb+Caus(dIr[tır])+Verb+Caus(t[t])+Verb+Caus(dIr[tır])+Pos+Past(dI[dı])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'doldurtturdum',     u'dol(dolmak)+Verb+Verb+Caus(dIr[dur])+Verb+Caus(t[t])+Verb+Caus(dIr[tur])+Pos+Past(dI[du])+A1sg(+Im[m])')

    def test_should_parse_fut_parts(self):
        self.assert_parse_correct(u'kalacak',           u'kal(kalmak)+Verb+Pos+Fut(+yAcAk[acak])+A3sg', u'kal(kalmak)+Verb+Pos+Adj+FutPart(+yAcAk[acak])+Pnon', u'kal(kalmak)+Verb+Pos+Fut(+yAcAk[acak])+Adj+Zero', u'kal(kalmak)+Verb+Pos+Noun+FutPart(+yAcAk[acak])+A3sg+Pnon+Nom', u'kal(kalmak)+Verb+Pos+Fut(+yAcAk[acak])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'kalmayacak',        u'kal(kalmak)+Verb+Neg(mA[ma])+Fut(+yAcAk[yacak])+A3sg', u'kal(kalmak)+Verb+Neg(mA[ma])+Adj+FutPart(+yAcAk[yacak])+Pnon', u'kal(kalmak)+Verb+Neg(mA[ma])+Fut(+yAcAk[yacak])+Adj+Zero', u'kal(kalmak)+Verb+Neg(mA[ma])+Noun+FutPart(+yAcAk[yacak])+A3sg+Pnon+Nom', u'kal(kalmak)+Verb+Neg(mA[ma])+Fut(+yAcAk[yacak])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')

        self.assert_parse_correct(u'bitecek',           u'bit(bitmek)+Verb+Pos+Fut(+yAcAk[ecek])+A3sg', u'bit(bitmek)+Verb+Pos+Adj+FutPart(+yAcAk[ecek])+Pnon', u'bit(bitmek)+Verb+Pos+Fut(+yAcAk[ecek])+Adj+Zero', u'bit(bitmek)+Verb+Pos+Noun+FutPart(+yAcAk[ecek])+A3sg+Pnon+Nom', u'bit(bitmek)+Verb+Pos+Fut(+yAcAk[ecek])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'bitmeyecek',        u'bit(bitmek)+Verb+Neg(mA[me])+Fut(+yAcAk[yecek])+A3sg', u'bit(bitmek)+Verb+Neg(mA[me])+Adj+FutPart(+yAcAk[yecek])+Pnon', u'bit(bitmek)+Verb+Neg(mA[me])+Fut(+yAcAk[yecek])+Adj+Zero', u'bit(bitmek)+Verb+Neg(mA[me])+Noun+FutPart(+yAcAk[yecek])+A3sg+Pnon+Nom', u'bit(bitmek)+Verb+Neg(mA[me])+Fut(+yAcAk[yecek])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')

        self.assert_parse_correct(u'kalacağım',         u'kal(kalmak)+Verb+Pos+Fut(+yAcAk[aca\u011f])+A1sg(+Im[\u0131m])', u'kal(kalmak)+Verb+Pos+Adj+FutPart(+yAcAk[aca\u011f])+P1sg(+Im[\u0131m])', u'kal(kalmak)+Verb+Pos+Noun+FutPart(+yAcAk[aca\u011f])+A3sg+P1sg(+Im[\u0131m])+Nom', u'kal(kalmak)+Verb+Pos+Fut(+yAcAk[aca\u011f])+Adj+Zero+Noun+Zero+A3sg+P1sg(+Im[\u0131m])+Nom')
        self.assert_parse_correct(u'kalmayacağım',      u'kal(kalmak)+Verb+Neg(mA[ma])+Fut(+yAcAk[yaca\u011f])+A1sg(+Im[\u0131m])', u'kal(kalmak)+Verb+Neg(mA[ma])+Adj+FutPart(+yAcAk[yaca\u011f])+P1sg(+Im[\u0131m])', u'kal(kalmak)+Verb+Neg(mA[ma])+Noun+FutPart(+yAcAk[yaca\u011f])+A3sg+P1sg(+Im[\u0131m])+Nom', u'kal(kalmak)+Verb+Neg(mA[ma])+Fut(+yAcAk[yaca\u011f])+Adj+Zero+Noun+Zero+A3sg+P1sg(+Im[\u0131m])+Nom')

        self.assert_parse_correct(u'kalacağımı',        u'kal(kalmak)+Verb+Pos+Noun+FutPart(+yAcAk[aca\u011f])+A3sg+P1sg(+Im[\u0131m])+Acc(+yI[\u0131])', u'kal(kalmak)+Verb+Pos+Fut(+yAcAk[aca\u011f])+Adj+Zero+Noun+Zero+A3sg+P1sg(+Im[\u0131m])+Acc(+yI[\u0131])')
        self.assert_parse_correct(u'kalmayacağımı',     u'kal(kalmak)+Verb+Neg(mA[ma])+Noun+FutPart(+yAcAk[yaca\u011f])+A3sg+P1sg(+Im[\u0131m])+Acc(+yI[\u0131])', u'kal(kalmak)+Verb+Neg(mA[ma])+Fut(+yAcAk[yaca\u011f])+Adj+Zero+Noun+Zero+A3sg+P1sg(+Im[\u0131m])+Acc(+yI[\u0131])')

        self.assert_parse_correct(u'kalacağıma',        u'kal(kalmak)+Verb+Pos+Noun+FutPart(+yAcAk[aca\u011f])+A3sg+P1sg(+Im[\u0131m])+Dat(+yA[a])', u'kal(kalmak)+Verb+Pos+Fut(+yAcAk[aca\u011f])+Adj+Zero+Noun+Zero+A3sg+P1sg(+Im[\u0131m])+Dat(+yA[a])')
        self.assert_parse_correct(u'kalmayacağıma',     u'kal(kalmak)+Verb+Neg(mA[ma])+Noun+FutPart(+yAcAk[yaca\u011f])+A3sg+P1sg(+Im[\u0131m])+Dat(+yA[a])', u'kal(kalmak)+Verb+Neg(mA[ma])+Fut(+yAcAk[yaca\u011f])+Adj+Zero+Noun+Zero+A3sg+P1sg(+Im[\u0131m])+Dat(+yA[a])')

        self.assert_parse_correct(u'kalacağın',         u'kal(kalmak)+Verb+Pos+Adj+FutPart(+yAcAk[aca\u011f])+P2sg(+In[\u0131n])', u'kal(kalmak)+Verb+Pos+Noun+FutPart(+yAcAk[aca\u011f])+A3sg+Pnon+Gen(+nIn[\u0131n])', u'kal(kalmak)+Verb+Pos+Noun+FutPart(+yAcAk[aca\u011f])+A3sg+P2sg(+In[\u0131n])+Nom', u'kal(kalmak)+Verb+Pos+Fut(+yAcAk[aca\u011f])+Adj+Zero+Noun+Zero+A3sg+Pnon+Gen(+nIn[\u0131n])', u'kal(kalmak)+Verb+Pos+Fut(+yAcAk[aca\u011f])+Adj+Zero+Noun+Zero+A3sg+P2sg(+In[\u0131n])+Nom')
        self.assert_parse_correct(u'kalmayacağın',      u'kal(kalmak)+Verb+Neg(mA[ma])+Adj+FutPart(+yAcAk[yaca\u011f])+P2sg(+In[\u0131n])', u'kal(kalmak)+Verb+Neg(mA[ma])+Noun+FutPart(+yAcAk[yaca\u011f])+A3sg+Pnon+Gen(+nIn[\u0131n])', u'kal(kalmak)+Verb+Neg(mA[ma])+Noun+FutPart(+yAcAk[yaca\u011f])+A3sg+P2sg(+In[\u0131n])+Nom', u'kal(kalmak)+Verb+Neg(mA[ma])+Fut(+yAcAk[yaca\u011f])+Adj+Zero+Noun+Zero+A3sg+Pnon+Gen(+nIn[\u0131n])', u'kal(kalmak)+Verb+Neg(mA[ma])+Fut(+yAcAk[yaca\u011f])+Adj+Zero+Noun+Zero+A3sg+P2sg(+In[\u0131n])+Nom')

        self.assert_parse_correct(u'kalacağını',        u'kal(kalmak)+Verb+Pos+Noun+FutPart(+yAcAk[aca\u011f])+A3sg+P2sg(+In[\u0131n])+Acc(+yI[\u0131])', u'kal(kalmak)+Verb+Pos+Noun+FutPart(+yAcAk[aca\u011f])+A3sg+P3sg(+sI[\u0131])+Acc(nI[n\u0131])', u'kal(kalmak)+Verb+Pos+Fut(+yAcAk[aca\u011f])+Adj+Zero+Noun+Zero+A3sg+P2sg(+In[\u0131n])+Acc(+yI[\u0131])', u'kal(kalmak)+Verb+Pos+Fut(+yAcAk[aca\u011f])+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[\u0131])+Acc(nI[n\u0131])')
        self.assert_parse_correct(u'kalmayacağını',     u'kal(kalmak)+Verb+Neg(mA[ma])+Noun+FutPart(+yAcAk[yaca\u011f])+A3sg+P2sg(+In[\u0131n])+Acc(+yI[\u0131])', u'kal(kalmak)+Verb+Neg(mA[ma])+Noun+FutPart(+yAcAk[yaca\u011f])+A3sg+P3sg(+sI[\u0131])+Acc(nI[n\u0131])', u'kal(kalmak)+Verb+Neg(mA[ma])+Fut(+yAcAk[yaca\u011f])+Adj+Zero+Noun+Zero+A3sg+P2sg(+In[\u0131n])+Acc(+yI[\u0131])', u'kal(kalmak)+Verb+Neg(mA[ma])+Fut(+yAcAk[yaca\u011f])+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[\u0131])+Acc(nI[n\u0131])')

        self.assert_parse_correct(u'kalacağına',        u'kal(kalmak)+Verb+Pos+Noun+FutPart(+yAcAk[aca\u011f])+A3sg+P2sg(+In[\u0131n])+Dat(+yA[a])', u'kal(kalmak)+Verb+Pos+Noun+FutPart(+yAcAk[aca\u011f])+A3sg+P3sg(+sI[\u0131])+Dat(nA[na])', u'kal(kalmak)+Verb+Pos+Fut(+yAcAk[aca\u011f])+Adj+Zero+Noun+Zero+A3sg+P2sg(+In[\u0131n])+Dat(+yA[a])', u'kal(kalmak)+Verb+Pos+Fut(+yAcAk[aca\u011f])+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[\u0131])+Dat(nA[na])')
        self.assert_parse_correct(u'kalmayacağına',     u'kal(kalmak)+Verb+Neg(mA[ma])+Noun+FutPart(+yAcAk[yaca\u011f])+A3sg+P2sg(+In[\u0131n])+Dat(+yA[a])', u'kal(kalmak)+Verb+Neg(mA[ma])+Noun+FutPart(+yAcAk[yaca\u011f])+A3sg+P3sg(+sI[\u0131])+Dat(nA[na])', u'kal(kalmak)+Verb+Neg(mA[ma])+Fut(+yAcAk[yaca\u011f])+Adj+Zero+Noun+Zero+A3sg+P2sg(+In[\u0131n])+Dat(+yA[a])', u'kal(kalmak)+Verb+Neg(mA[ma])+Fut(+yAcAk[yaca\u011f])+Adj+Zero+Noun+Zero+A3sg+P3sg(+sI[\u0131])+Dat(nA[na])')

        self.assert_parse_correct(u'kalacaklar',        u'kal(kalmak)+Verb+Pos+Fut(+yAcAk[acak])+A3pl(lAr[lar])', u'kal(kalmak)+Verb+Pos+Noun+FutPart(+yAcAk[acak])+A3pl(lAr[lar])+Pnon+Nom', u'kal(kalmak)+Verb+Pos+Fut(+yAcAk[acak])+Adj+Zero+Noun+Zero+A3pl(lAr[lar])+Pnon+Nom')
        self.assert_parse_correct(u'kalmayacaklar',     u'kal(kalmak)+Verb+Neg(mA[ma])+Fut(+yAcAk[yacak])+A3pl(lAr[lar])', u'kal(kalmak)+Verb+Neg(mA[ma])+Noun+FutPart(+yAcAk[yacak])+A3pl(lAr[lar])+Pnon+Nom', u'kal(kalmak)+Verb+Neg(mA[ma])+Fut(+yAcAk[yacak])+Adj+Zero+Noun+Zero+A3pl(lAr[lar])+Pnon+Nom')

        self.assert_parse_correct(u'kalacakları',       u'kal(kalmak)+Verb+Pos+Adj+FutPart(+yAcAk[acak])+P3pl(lArI![lar\u0131])', u'kal(kalmak)+Verb+Pos+Noun+FutPart(+yAcAk[acak])+A3sg+P3pl(lArI![lar\u0131])+Nom', u'kal(kalmak)+Verb+Pos+Noun+FutPart(+yAcAk[acak])+A3pl(lAr[lar])+Pnon+Acc(+yI[\u0131])', u'kal(kalmak)+Verb+Pos+Noun+FutPart(+yAcAk[acak])+A3pl(lAr[lar])+P3sg(+sI[\u0131])+Nom', u'kal(kalmak)+Verb+Pos+Noun+FutPart(+yAcAk[acak])+A3pl(lAr[lar])+P3pl(I![\u0131])+Nom', u'kal(kalmak)+Verb+Pos+Fut(+yAcAk[acak])+Adj+Zero+Noun+Zero+A3sg+P3pl(lArI![lar\u0131])+Nom', u'kal(kalmak)+Verb+Pos+Fut(+yAcAk[acak])+Adj+Zero+Noun+Zero+A3pl(lAr[lar])+Pnon+Acc(+yI[\u0131])', u'kal(kalmak)+Verb+Pos+Fut(+yAcAk[acak])+Adj+Zero+Noun+Zero+A3pl(lAr[lar])+P3sg(+sI[\u0131])+Nom', u'kal(kalmak)+Verb+Pos+Fut(+yAcAk[acak])+Adj+Zero+Noun+Zero+A3pl(lAr[lar])+P3pl(I![\u0131])+Nom')
        self.assert_parse_correct(u'kalmayacakları',    u'kal(kalmak)+Verb+Neg(mA[ma])+Adj+FutPart(+yAcAk[yacak])+P3pl(lArI![lar\u0131])', u'kal(kalmak)+Verb+Neg(mA[ma])+Noun+FutPart(+yAcAk[yacak])+A3sg+P3pl(lArI![lar\u0131])+Nom', u'kal(kalmak)+Verb+Neg(mA[ma])+Noun+FutPart(+yAcAk[yacak])+A3pl(lAr[lar])+Pnon+Acc(+yI[\u0131])', u'kal(kalmak)+Verb+Neg(mA[ma])+Noun+FutPart(+yAcAk[yacak])+A3pl(lAr[lar])+P3sg(+sI[\u0131])+Nom', u'kal(kalmak)+Verb+Neg(mA[ma])+Noun+FutPart(+yAcAk[yacak])+A3pl(lAr[lar])+P3pl(I![\u0131])+Nom', u'kal(kalmak)+Verb+Neg(mA[ma])+Fut(+yAcAk[yacak])+Adj+Zero+Noun+Zero+A3sg+P3pl(lArI![lar\u0131])+Nom', u'kal(kalmak)+Verb+Neg(mA[ma])+Fut(+yAcAk[yacak])+Adj+Zero+Noun+Zero+A3pl(lAr[lar])+Pnon+Acc(+yI[\u0131])', u'kal(kalmak)+Verb+Neg(mA[ma])+Fut(+yAcAk[yacak])+Adj+Zero+Noun+Zero+A3pl(lAr[lar])+P3sg(+sI[\u0131])+Nom', u'kal(kalmak)+Verb+Neg(mA[ma])+Fut(+yAcAk[yacak])+Adj+Zero+Noun+Zero+A3pl(lAr[lar])+P3pl(I![\u0131])+Nom')

        self.assert_parse_correct(u'kalacaklarımı',     u'kal(kalmak)+Verb+Pos+Noun+FutPart(+yAcAk[acak])+A3pl(lAr[lar])+P1sg(+Im[\u0131m])+Acc(+yI[\u0131])', u'kal(kalmak)+Verb+Pos+Fut(+yAcAk[acak])+Adj+Zero+Noun+Zero+A3pl(lAr[lar])+P1sg(+Im[\u0131m])+Acc(+yI[\u0131])')
        self.assert_parse_correct(u'kalmayacaklarımı',  u'kal(kalmak)+Verb+Neg(mA[ma])+Noun+FutPart(+yAcAk[yacak])+A3pl(lAr[lar])+P1sg(+Im[\u0131m])+Acc(+yI[\u0131])', u'kal(kalmak)+Verb+Neg(mA[ma])+Fut(+yAcAk[yacak])+Adj+Zero+Noun+Zero+A3pl(lAr[lar])+P1sg(+Im[\u0131m])+Acc(+yI[\u0131])')

    def test_should_parse_past_parts(self):
        self.assert_parse_correct(u'ettiklerin',
            u'et(etmek)+Verb+Pos+Noun+PastPart(dIk[tik])+A3pl(lAr[ler])+Pnon+Gen(+nIn[in])',
            u'et(etmek)+Verb+Pos+Noun+PastPart(dIk[tik])+A3pl(lAr[ler])+P2sg(+In[in])+Nom'
        )
        self.assert_parse_correct(u'yediklerin',
            u'ye(yemek)+Verb+Pos+Noun+PastPart(dIk[dik])+A3pl(lAr[ler])+Pnon+Gen(+nIn[in])',
            u'ye(yemek)+Verb+Pos+Noun+PastPart(dIk[dik])+A3pl(lAr[ler])+P2sg(+In[in])+Nom'
        )

        self.assert_parse_correct(u'yediği',
            u'ye(yemek)+Verb+Pos+Adj+PastPart(dIk[diğ])+P3sg(+sI[i])',
            u'ye(yemek)+Verb+Pos+Noun+PastPart(dIk[diğ])+A3sg+Pnon+Acc(+yI[i])',
            u'ye(yemek)+Verb+Pos+Noun+PastPart(dIk[diğ])+A3sg+P3sg(+sI[i])+Nom'
        )
        self.assert_parse_correct(u'yedik',
            u'ye(yemek)+Verb+Pos+Past(dI[di])+A1pl(k[k])',
            u'ye(yemek)+Verb+Pos+Adj+PastPart(dIk[dik])+Pnon',
            u'ye(yemek)+Verb+Pos+Noun+PastPart(dIk[dik])+A3sg+Pnon+Nom'
        )


    def test_should_parse_recip_verbs(self):
        self.assert_parse_correct_for_verb(u'bakıştılar', u'bak(bakmak)+Verb+Verb+Recip(+Iş[ış])+Pos+Past(dI[tı])+A3pl(lAr[lar])')

    def test_should_parse_reflexive_pronouns(self):
        self.assert_parse_correct(u'kendim',             u'kendi(kendi)+Pron+Reflex+A1sg+P1sg(m[m])+Nom')
        self.assert_parse_correct(u'kendin',             u'kendi(kendi)+Pron+Reflex+A2sg+P2sg(n[n])+Nom')
        self.assert_parse_correct(u'kendi',              u'kendi(kendi)+Pron+Reflex+A3sg+P3sg+Nom')
        self.assert_parse_correct(u'kendimiz',           u'kendi(kendi)+Pron+Reflex+A1pl+P1pl(miz[miz])+Nom')
        self.assert_parse_correct(u'kendiniz',           u'kendi(kendi)+Pron+Reflex+A2pl+P2pl(niz[niz])+Nom')
        self.assert_parse_correct(u'kendileri',          u'kendi(kendi)+Pron+Reflex+A3pl(leri[leri])+P3pl+Nom')
        self.assert_parse_correct(u'kendisi',            u'kendi(kendi)+Pron+Reflex+A3sg+P3sg(si[si])+Nom')
        self.assert_parse_correct(u'kendilerimiz',       u'kendi(kendi)+Pron+Reflex+A1pl(ler[ler])+P1pl(imiz[imiz])+Nom')
        self.assert_parse_correct(u'kendileriniz',       u'kendi(kendi)+Pron+Reflex+A2pl(ler[ler])+P2pl(iniz[iniz])+Nom')

        self.assert_parse_correct(u'kendimi',            u'kendi(kendi)+Pron+Reflex+A1sg+P1sg(m[m])+Acc(i[i])')
        self.assert_parse_correct(u'kendini',            u'kendi(kendi)+Pron+Reflex+A2sg+P2sg(n[n])+Acc(i[i])', u'kendi(kendi)+Pron+Reflex+A3sg+P3sg+Acc(ni[ni])')
        self.assert_parse_correct(u'kendimizi',          u'kendi(kendi)+Pron+Reflex+A1pl+P1pl(miz[miz])+Acc(i[i])')
        self.assert_parse_correct(u'kendinizi',          u'kendi(kendi)+Pron+Reflex+A2pl+P2pl(niz[niz])+Acc(i[i])')
        self.assert_parse_correct(u'kendilerini',        u'kendi(kendi)+Pron+Reflex+A3pl(leri[leri])+P3pl+Acc(ni[ni])')
        self.assert_parse_correct(u'kendisini',          u'kendi(kendi)+Pron+Reflex+A3sg+P3sg(si[si])+Acc(ni[ni])')
        self.assert_parse_correct(u'kendilerimizi',      u'kendi(kendi)+Pron+Reflex+A1pl(ler[ler])+P1pl(imiz[imiz])+Acc(i[i])')
        self.assert_parse_correct(u'kendilerinizi',      u'kendi(kendi)+Pron+Reflex+A2pl(ler[ler])+P2pl(iniz[iniz])+Acc(i[i])')

        self.assert_parse_correct(u'kendime',            u'kendi(kendi)+Pron+Reflex+A1sg+P1sg(m[m])+Dat(e[e])')
        self.assert_parse_correct(u'kendine',            u'kendi(kendi)+Pron+Reflex+A2sg+P2sg(n[n])+Dat(e[e])', u'kendi(kendi)+Pron+Reflex+A3sg+P3sg+Dat(ne[ne])')
        self.assert_parse_correct(u'kendimize',          u'kendi(kendi)+Pron+Reflex+A1pl+P1pl(miz[miz])+Dat(e[e])')
        self.assert_parse_correct(u'kendinize',          u'kendi(kendi)+Pron+Reflex+A2pl+P2pl(niz[niz])+Dat(e[e])')
        self.assert_parse_correct(u'kendilerine',        u'kendi(kendi)+Pron+Reflex+A3pl(leri[leri])+P3pl+Dat(ne[ne])')
        self.assert_parse_correct(u'kendisine',          u'kendi(kendi)+Pron+Reflex+A3sg+P3sg(si[si])+Dat(ne[ne])')
        self.assert_parse_correct(u'kendilerimize',      u'kendi(kendi)+Pron+Reflex+A1pl(ler[ler])+P1pl(imiz[imiz])+Dat(e[e])')
        self.assert_parse_correct(u'kendilerinize',      u'kendi(kendi)+Pron+Reflex+A2pl(ler[ler])+P2pl(iniz[iniz])+Dat(e[e])')

        self.assert_parse_correct(u'kendimde',           u'kendi(kendi)+Pron+Reflex+A1sg+P1sg(m[m])+Loc(de[de])')
        self.assert_parse_correct(u'kendinde',           u'kendi(kendi)+Pron+Reflex+A2sg+P2sg(n[n])+Loc(de[de])', u'kendi(kendi)+Pron+Reflex+A3sg+P3sg+Loc(nde[nde])')
        self.assert_parse_correct(u'kendimizde',         u'kendi(kendi)+Pron+Reflex+A1pl+P1pl(miz[miz])+Loc(de[de])')
        self.assert_parse_correct(u'kendinizde',         u'kendi(kendi)+Pron+Reflex+A2pl+P2pl(niz[niz])+Loc(de[de])')
        self.assert_parse_correct(u'kendilerinde',       u'kendi(kendi)+Pron+Reflex+A3pl(leri[leri])+P3pl+Loc(nde[nde])')
        self.assert_parse_correct(u'kendisinde',         u'kendi(kendi)+Pron+Reflex+A3sg+P3sg(si[si])+Loc(nde[nde])')
        self.assert_parse_correct(u'kendilerimizde',     u'kendi(kendi)+Pron+Reflex+A1pl(ler[ler])+P1pl(imiz[imiz])+Loc(de[de])')
        self.assert_parse_correct(u'kendilerinizde',     u'kendi(kendi)+Pron+Reflex+A2pl(ler[ler])+P2pl(iniz[iniz])+Loc(de[de])')

        self.assert_parse_correct(u'kendimden',          u'kendi(kendi)+Pron+Reflex+A1sg+P1sg(m[m])+Abl(den[den])')
        self.assert_parse_correct(u'kendinden',          u'kendi(kendi)+Pron+Reflex+A2sg+P2sg(n[n])+Abl(den[den])', u'kendi(kendi)+Pron+Reflex+A3sg+P3sg+Abl(nden[nden])', u'kendinden(kendinden)+Adv')
        self.assert_parse_correct(u'kendimizden',        u'kendi(kendi)+Pron+Reflex+A1pl+P1pl(miz[miz])+Abl(den[den])')
        self.assert_parse_correct(u'kendinizden',        u'kendi(kendi)+Pron+Reflex+A2pl+P2pl(niz[niz])+Abl(den[den])')
        self.assert_parse_correct(u'kendilerinden',      u'kendi(kendi)+Pron+Reflex+A3pl(leri[leri])+P3pl+Abl(nden[nden])')
        self.assert_parse_correct(u'kendisinden',        u'kendi(kendi)+Pron+Reflex+A3sg+P3sg(si[si])+Abl(nden[nden])')
        self.assert_parse_correct(u'kendilerimizden',    u'kendi(kendi)+Pron+Reflex+A1pl(ler[ler])+P1pl(imiz[imiz])+Abl(den[den])')
        self.assert_parse_correct(u'kendilerinizden',    u'kendi(kendi)+Pron+Reflex+A2pl(ler[ler])+P2pl(iniz[iniz])+Abl(den[den])')

        self.assert_parse_correct(u'kendimin',           u'kendi(kendi)+Pron+Reflex+A1sg+P1sg(m[m])+Gen(in[in])')
        self.assert_parse_correct(u'kendinin',           u'kendi(kendi)+Pron+Reflex+A2sg+P2sg(n[n])+Gen(in[in])', u'kendi(kendi)+Pron+Reflex+A3sg+P3sg+Gen(nin[nin])')
        self.assert_parse_correct(u'kendimizin',         u'kendi(kendi)+Pron+Reflex+A1pl+P1pl(miz[miz])+Gen(in[in])')
        self.assert_parse_correct(u'kendinizin',         u'kendi(kendi)+Pron+Reflex+A2pl+P2pl(niz[niz])+Gen(in[in])')
        self.assert_parse_correct(u'kendilerinin',       u'kendi(kendi)+Pron+Reflex+A3pl(leri[leri])+P3pl+Gen(nin[nin])')
        self.assert_parse_correct(u'kendisinin',         u'kendi(kendi)+Pron+Reflex+A3sg+P3sg(si[si])+Gen(nin[nin])')
        self.assert_parse_correct(u'kendilerimizin',     u'kendi(kendi)+Pron+Reflex+A1pl(ler[ler])+P1pl(imiz[imiz])+Gen(in[in])')
        self.assert_parse_correct(u'kendilerinizin',     u'kendi(kendi)+Pron+Reflex+A2pl(ler[ler])+P2pl(iniz[iniz])+Gen(in[in])')

        self.assert_parse_correct(u'kendimle',           u'kendi(kendi)+Pron+Reflex+A1sg+P1sg(m[m])+Ins(le[le])')
        self.assert_parse_correct(u'kendinle',           u'kendi(kendi)+Pron+Reflex+A2sg+P2sg(n[n])+Ins(le[le])')
        self.assert_parse_correct(u'kendiyle',           u'kendi(kendi)+Pron+Reflex+A3sg+P3sg+Ins(yle[yle])')
        self.assert_parse_correct(u'kendimizle',         u'kendi(kendi)+Pron+Reflex+A1pl+P1pl(miz[miz])+Ins(le[le])')
        self.assert_parse_correct(u'kendinizle',         u'kendi(kendi)+Pron+Reflex+A2pl+P2pl(niz[niz])+Ins(le[le])')
        self.assert_parse_correct(u'kendileriyle',       u'kendi(kendi)+Pron+Reflex+A3pl(leri[leri])+P3pl+Ins(yle[yle])')
        self.assert_parse_correct(u'kendisiyle',         u'kendi(kendi)+Pron+Reflex+A3sg+P3sg(si[si])+Ins(yle[yle])')
        self.assert_parse_correct(u'kendilerimizle',     u'kendi(kendi)+Pron+Reflex+A1pl(ler[ler])+P1pl(imiz[imiz])+Ins(le[le])')
        self.assert_parse_correct(u'kendilerinizle',     u'kendi(kendi)+Pron+Reflex+A2pl(ler[ler])+P2pl(iniz[iniz])+Ins(le[le])')

    def test_should_parse_pronoun_hepsi(self):
        self.assert_parse_correct(u'hepsi',              u'hepsi(hepsi)+Pron+A3pl+P3pl+Nom')
        self.assert_parse_correct(u'hepsini',            u'hepsi(hepsi)+Pron+A3pl+P3pl+Acc(ni[ni])')
        self.assert_parse_correct(u'hepimize',           u'hep(hepsi)+Pron+A1pl+P1pl(imiz[imiz])+Dat(e[e])')
        self.assert_parse_correct(u'hepinizle',          u'hep(hepsi)+Pron+A2pl+P2pl(iniz[iniz])+Ins(le[le])')

    def test_should_parse_adj_to_noun_zero_transition(self):
        self.cloned_root_map[u'gen'] = []

        self.assert_parse_correct(u'maviye',             u'mavi(mavi)+Adj+Noun+Zero+A3sg+Pnon+Dat(+yA[ye])')
        self.assert_parse_correct(u'gencin',             u'genc(genç)+Adj+Noun+Zero+A3sg+Pnon+Gen(+nIn[in])',  u'genc(genç)+Adj+Noun+Zero+A3sg+P2sg(+In[in])+Nom')

    def test_should_parse_verb_to_adv_derivations(self):
        self.assert_parse_correct(u'yapınca',             u'yap(yapmak)+Verb+Pos+Adv+When(+yIncA[ınca])')
        self.assert_parse_correct(u'yapmayınca',          u'yap(yapmak)+Verb+Neg(mA[ma])+Adv+When(+yIncA[yınca])')
        self.assert_parse_correct(u'dönünce',             u'dön(dönmek)+Verb+Pos+Adv+When(+yIncA[ünce])')
        self.assert_parse_correct(u'dönmeyince',          u'dön(dönmek)+Verb+Neg(mA[me])+Adv+When(+yIncA[yince])')
        self.assert_parse_correct(u'yalayınca',           u'yala(yalamak)+Verb+Pos+Adv+When(+yIncA[yınca])')
        self.assert_parse_correct(u'yalamayınca',         u'yala(yalamak)+Verb+Neg(mA[ma])+Adv+When(+yIncA[yınca])')
        self.assert_parse_correct(u'çıkarttırabilince',   u'çık(çıkmak)+Verb+Verb+Caus(Ar[ar])+Verb+Caus(t[t])+Verb+Caus(dIr[tır])+Verb+Able(+yAbil[abil])+Pos+Adv+When(+yIncA[ince])')
        self.assert_parse_correct(u'yaptıramayınca',      u'yap(yapmak)+Verb+Verb+Caus(dIr[tır])+Verb+Able(+yA[a])+Neg(mA[ma])+Adv+When(+yIncA[yınca])')

        self.cloned_root_map[u'dönel'] = []

        self.assert_parse_correct(u'yapalı',              u'yap(yapmak)+Verb+Pos+Adv+SinceDoingSo(+yAlI![alı])')
        self.assert_parse_correct(u'yapmayalı',           u'yap(yapmak)+Verb+Neg(mA[ma])+Adv+SinceDoingSo(+yAlI![yalı])')
        self.assert_parse_correct(u'döneli',              u'dön(dönmek)+Verb+Pos+Adv+SinceDoingSo(+yAlI![eli])')
        self.assert_parse_correct(u'dönmeyeli',           u'dön(dönmek)+Verb+Neg(mA[me])+Adv+SinceDoingSo(+yAlI![yeli])')
        self.assert_parse_correct(u'yalayalı',            u'yala(yalamak)+Verb+Pos+Adv+SinceDoingSo(+yAlI![yalı])')
        self.assert_parse_correct(u'yalamayalı',          u'yala(yalamak)+Verb+Neg(mA[ma])+Adv+SinceDoingSo(+yAlI![yalı])')
        self.assert_parse_correct(u'çıkarttırabileli',    u'çık(çıkmak)+Verb+Verb+Caus(Ar[ar])+Verb+Caus(t[t])+Verb+Caus(dIr[tır])+Verb+Able(+yAbil[abil])+Pos+Adv+SinceDoingSo(+yAlI![eli])')
        self.assert_parse_correct(u'yaptıramayalı',       u'yap(yapmak)+Verb+Verb+Caus(dIr[tır])+Verb+Able(+yA[a])+Neg(mA[ma])+Adv+SinceDoingSo(+yAlI![yalı])')

        self.assert_parse_correct(u'yaparken',            u'yap(yapmak)+Verb+Pos+Aor(+Ar[ar])+Adv+While(ken[ken])')
        self.assert_parse_correct(u'yapmazken',           u'yap(yapmak)+Verb+Neg(mA[ma])+Aor(z[z])+Adv+While(ken[ken])')
        self.assert_parse_correct(u'dönerlerken',         u'd\xf6n(d\xf6nmek)+Verb+Pos+Aor(+Ar[er])+A3pl(lAr[ler])+Adv+While(ken[ken])')
        self.assert_parse_correct(u'dönmezlerken',        u'd\xf6n(d\xf6nmek)+Verb+Neg(mA[me])+Aor(z[z])+A3pl(lAr[ler])+Adv+While(ken[ken])')
        self.assert_parse_correct(u'yalayacakken',        u'yala(yalamak)+Verb+Pos+Fut(+yAcAk[yacak])+Adv+While(ken[ken])')
        self.assert_parse_correct(u'yalamayacakken',      u'yala(yalamak)+Verb+Neg(mA[ma])+Fut(+yAcAk[yacak])+Adv+While(ken[ken])')
        self.assert_parse_correct(u'çıkarttırabilmişken', u'\xe7\u0131k(\xe7\u0131kmak)+Verb+Verb+Caus(Ar[ar])+Verb+Caus(t[t])+Verb+Caus(dIr[t\u0131r])+Verb+Able(+yAbil[abil])+Pos+Narr(mI\u015f[mi\u015f])+Adv+While(ken[ken])')
        self.assert_parse_correct(u'yaptıramıyorken',     u'yap(yapmak)+Verb+Verb+Caus(dIr[t\u0131r])+Verb+Able(+yA[a])+Neg(m[m])+Prog(Iyor[\u0131yor])+Adv+While(ken[ken])')
        self.assert_parse_correct(u'yaptıramıyorlarken',  u'yap(yapmak)+Verb+Verb+Caus(dIr[t\u0131r])+Verb+Able(+yA[a])+Neg(m[m])+Prog(Iyor[\u0131yor])+A3pl(lAr[lar])+Adv+While(ken[ken])')
        self.assert_parse_correct(u'yaptıramamışlarken',  u'yap(yapmak)+Verb+Verb+Caus(dIr[t\u0131r])+Verb+Able(+yA[a])+Neg(mA[ma])+Narr(mI\u015f[m\u0131\u015f])+A3pl(lAr[lar])+Adv+While(ken[ken])')

        self.assert_parse_correct(u'yaparcasına',
            u'yap(yapmak)+Verb+Pos+Aor(+Ar[ar])+Adv+AsIf(cAsI!nA[casına])',
            u'yap(yapmak)+Verb+Pos+Aor(+Ar[ar])+Adj+Zero+Adj+Equ(cA[ca])+Noun+Zero+A3sg+P3sg(+sI[sı])+Dat(nA[na])',
            u'yap(yapmak)+Verb+Pos+Aor(+Ar[ar])+Adj+Zero+Adj+Quite(cA[ca])+Noun+Zero+A3sg+P3sg(+sI[sı])+Dat(nA[na])',
            u'yap(yapmak)+Verb+Pos+Aor(+Ar[ar])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom+Adj+Equ(cA[ca])+Noun+Zero+A3sg+P3sg(+sI[sı])+Dat(nA[na])')
        self.assert_parse_correct(u'yaparlarcasına',
            u'yap(yapmak)+Verb+Pos+Aor(+Ar[ar])+A3pl(lAr[lar])+Adv+AsIf(cAsI!nA[cas\u0131na])',
            u'yap(yapmak)+Verb+Pos+Aor(+Ar[ar])+Adj+Zero+Noun+Zero+A3pl(lAr[lar])+Pnon+Nom+Adj+Equ(cA[ca])+Noun+Zero+A3sg+P3sg(+sI[s\u0131])+Dat(nA[na])')
        self.assert_parse_correct(u'yaparmışçasına',      u'yap(yapmak)+Verb+Pos+Aor(+Ar[ar])+Narr(mIş[mış])+Adv+AsIf(cAsI!nA[çasına])')
        self.assert_parse_correct(u'yapmamışçasına',
            u'yap(yapmak)+Verb+Neg(mA[ma])+Narr(mIş[mış])+Adv+AsIf(cAsI!nA[çasına])',
            u'yap(yapmak)+Verb+Neg(mA[ma])+Narr(mIş[mış])+Adj+Zero+Adj+Equ(cA[ça])+Noun+Zero+A3sg+P3sg(+sI[sı])+Dat(nA[na])',
            u'yap(yapmak)+Verb+Neg(mA[ma])+Narr(mIş[mış])+Adj+Zero+Adj+Quite(cA[ça])+Noun+Zero+A3sg+P3sg(+sI[sı])+Dat(nA[na])',
            u'yap(yapmak)+Verb+Neg(mA[ma])+Narr(mIş[mış])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom+Adj+Equ(cA[ça])+Noun+Zero+A3sg+P3sg(+sI[sı])+Dat(nA[na])')
        self.assert_parse_correct(u'yapmamışlarcasına',
            u'yap(yapmak)+Verb+Neg(mA[ma])+Narr(mI\u015f[m\u0131\u015f])+A3pl(lAr[lar])+Adv+AsIf(cAsI!nA[cas\u0131na])',
            u'yap(yapmak)+Verb+Neg(mA[ma])+Narr(mI\u015f[m\u0131\u015f])+Adj+Zero+Noun+Zero+A3pl(lAr[lar])+Pnon+Nom+Adj+Equ(cA[ca])+Noun+Zero+A3sg+P3sg(+sI[s\u0131])+Dat(nA[na])')
        self.assert_parse_correct(u'yapacakmışçasına',    u'yap(yapmak)+Verb+Pos+Fut(+yAcAk[acak])+Narr(mIş[mış])+Adv+AsIf(cAsI!nA[çasına])')
        self.assert_parse_correct(u'yapacakmışlarcasına',    u'yap(yapmak)+Verb+Pos+Fut(+yAcAk[acak])+Narr(mI\u015f[m\u0131\u015f])+A3pl(lAr[lar])+Adv+AsIf(cAsI!nA[cas\u0131na])')
        self.assert_parse_correct(u'yaptıramazcasına',
            u'yap(yapmak)+Verb+Verb+Caus(dIr[tır])+Verb+Able(+yA[a])+Neg(mA[ma])+Aor(z[z])+Adv+AsIf(cAsI!nA[casına])',
            u'yap(yapmak)+Verb+Verb+Caus(dIr[tır])+Verb+Able(+yA[a])+Neg(mA[ma])+Aor(z[z])+Adj+Zero+Adj+Equ(cA[ca])+Noun+Zero+A3sg+P3sg(+sI[sı])+Dat(nA[na])',
            u'yap(yapmak)+Verb+Verb+Caus(dIr[tır])+Verb+Able(+yA[a])+Neg(mA[ma])+Aor(z[z])+Adj+Zero+Adj+Quite(cA[ca])+Noun+Zero+A3sg+P3sg(+sI[sı])+Dat(nA[na])',
            u'yap(yapmak)+Verb+Verb+Caus(dIr[tır])+Verb+Able(+yA[a])+Neg(mA[ma])+Aor(z[z])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom+Adj+Equ(cA[ca])+Noun+Zero+A3sg+P3sg(+sI[sı])+Dat(nA[na])')
        self.assert_parse_correct(u'yaptıramazlarcasına',
            u'yap(yapmak)+Verb+Verb+Caus(dIr[t\u0131r])+Verb+Able(+yA[a])+Neg(mA[ma])+Aor(z[z])+A3pl(lAr[lar])+Adv+AsIf(cAsI!nA[cas\u0131na])',
            u'yap(yapmak)+Verb+Verb+Caus(dIr[t\u0131r])+Verb+Able(+yA[a])+Neg(mA[ma])+Aor(z[z])+Adj+Zero+Noun+Zero+A3pl(lAr[lar])+Pnon+Nom+Adj+Equ(cA[ca])+Noun+Zero+A3sg+P3sg(+sI[s\u0131])+Dat(nA[na])')

    def test_should_parse_adj_to_adj_derivations(self):
        self.cloned_root_map[u'koy'] = []
        self.cloned_root_map[u'kırmız'] = []

        self.assert_parse_correct(u'kırmızımsı',          u'kırmızı(kırmızı)+Adj+Adj+JustLike(+ImsI[msı])', u'kırmızı(kırmızı)+Adj+Noun+Zero+A3sg+Pnon+Nom+Adj+JustLike(+ImsI[msı])', u'kırmızı(kırmızı)+Adj+Adj+JustLike(+ImsI[msı])+Noun+Zero+A3sg+Pnon+Nom', u'kırmızı(kırmızı)+Adj+Noun+Zero+A3sg+Pnon+Nom+Adj+JustLike(+ImsI[msı])+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'yeşilimsi',           u'yeşil(yeşil)+Adj+Adj+JustLike(+ImsI[imsi])', u'yeşil(yeşil)+Adj+Noun+Zero+A3sg+Pnon+Nom+Adj+JustLike(+ImsI[imsi])', u'yeşil(yeşil)+Adj+Adj+JustLike(+ImsI[imsi])+Noun+Zero+A3sg+Pnon+Nom', u'yeşil(yeşil)+Adj+Noun+Zero+A3sg+Pnon+Nom+Adj+JustLike(+ImsI[imsi])+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'koyumsu',             u'koyu(koyu)+Adj+Adj+JustLike(+ImsI[msu])', u'koyu(koyu)+Adj+Noun+Zero+A3sg+Pnon+Nom+Adj+JustLike(+ImsI[msu])', u'koyu(koyu)+Adj+Adj+JustLike(+ImsI[msu])+Noun+Zero+A3sg+Pnon+Nom', u'koyu(koyu)+Adj+Noun+Zero+A3sg+Pnon+Nom+Adj+JustLike(+ImsI[msu])+Noun+Zero+A3sg+Pnon+Nom')

    def test_should_parse_words_with_suffixes_ce(self):

        self.assert_parse_correct(u'aptalca',
            u'aptal(aptal)+Adj+Adj+Equ(cA[ca])',
            u'aptal(aptal)+Adj+Adj+Quite(cA[ca])',
            u'aptal(aptal)+Adj+Adv+Ly(cA[ca])',
            u'aptal(aptal)+Adj+Noun+Zero+A3sg+Pnon+Nom+Adj+Equ(cA[ca])',
            u'aptal(aptal)+Adj+Noun+Zero+A3sg+Pnon+Nom+Adv+InTermsOf(cA[ca])',
            u'aptal(aptal)+Adj+Noun+Zero+A3sg+Pnon+Nom+Adv+By(cA[ca])',
            u'aptal(aptal)+Adj+Adj+Equ(cA[ca])+Noun+Zero+A3sg+Pnon+Nom',
            u'aptal(aptal)+Adj+Adj+Quite(cA[ca])+Noun+Zero+A3sg+Pnon+Nom',
            u'aptal(aptal)+Adj+Noun+Zero+A3sg+Pnon+Nom+Adj+Equ(cA[ca])+Noun+Zero+A3sg+Pnon+Nom')

        self.assert_parse_correct(u'delice',
            u'deli(deli)+Adj+Adj+Equ(cA[ce])',
            u'deli(deli)+Adj+Adj+Quite(cA[ce])',
            u'deli(deli)+Adj+Adv+Ly(cA[ce])',
            u'delice(delice)+Noun+A3sg+Pnon+Nom',
            u'deli(deli)+Adj+Noun+Zero+A3sg+Pnon+Nom+Adj+Equ(cA[ce])',
            u'deli(deli)+Adj+Noun+Zero+A3sg+Pnon+Nom+Adv+InTermsOf(cA[ce])',
            u'deli(deli)+Adj+Noun+Zero+A3sg+Pnon+Nom+Adv+By(cA[ce])',
            u'deli(deli)+Adj+Adj+Equ(cA[ce])+Noun+Zero+A3sg+Pnon+Nom',
            u'deli(deli)+Adj+Adj+Quite(cA[ce])+Noun+Zero+A3sg+Pnon+Nom',
            u'deli(deli)+Adj+Noun+Zero+A3sg+Pnon+Nom+Adj+Equ(cA[ce])+Noun+Zero+A3sg+Pnon+Nom')

        self.cloned_root_map[u'babac'] = []
        self.assert_parse_correct(u'babaca',
            u'baba(baba)+Adj+Adj+Equ(cA[ca])',
            u'baba(baba)+Adj+Adj+Quite(cA[ca])',
            u'baba(baba)+Adj+Adv+Ly(cA[ca])',
            u'baba(baba)+Noun+A3sg+Pnon+Nom+Adj+Equ(cA[ca])',
            u'baba(baba)+Noun+A3sg+Pnon+Nom+Adv+InTermsOf(cA[ca])',
            u'baba(baba)+Noun+A3sg+Pnon+Nom+Adv+By(cA[ca])',
            u'baba(baba)+Adj+Noun+Zero+A3sg+Pnon+Nom+Adj+Equ(cA[ca])',
            u'baba(baba)+Adj+Noun+Zero+A3sg+Pnon+Nom+Adv+InTermsOf(cA[ca])',
            u'baba(baba)+Adj+Noun+Zero+A3sg+Pnon+Nom+Adv+By(cA[ca])',
            u'baba(baba)+Adj+Adj+Equ(cA[ca])+Noun+Zero+A3sg+Pnon+Nom',
            u'baba(baba)+Adj+Adj+Quite(cA[ca])+Noun+Zero+A3sg+Pnon+Nom',
            u'baba(baba)+Noun+A3sg+Pnon+Nom+Adj+Equ(cA[ca])+Noun+Zero+A3sg+Pnon+Nom',
            u'baba(baba)+Adj+Noun+Zero+A3sg+Pnon+Nom+Adj+Equ(cA[ca])+Noun+Zero+A3sg+Pnon+Nom')

        self.assert_parse_correct(u'iyice',
            u'iyi(iyi)+Adj+Adj+Equ(cA[ce])',
            u'iyi(iyi)+Adj+Adj+Quite(cA[ce])',
            u'iyi(iyi)+Adj+Adv+Ly(cA[ce])',
            u'iyi(iyi)+Adj+Noun+Zero+A3sg+Pnon+Nom+Adj+Equ(cA[ce])',
            u'iyi(iyi)+Adj+Noun+Zero+A3sg+Pnon+Nom+Adv+InTermsOf(cA[ce])',
            u'iyi(iyi)+Adj+Noun+Zero+A3sg+Pnon+Nom+Adv+By(cA[ce])',
            u'iyi(iyi)+Adj+Adj+Equ(cA[ce])+Noun+Zero+A3sg+Pnon+Nom',
            u'iyi(iyi)+Adj+Adj+Quite(cA[ce])+Noun+Zero+A3sg+Pnon+Nom',
            u'iyi(iyi)+Adj+Noun+Zero+A3sg+Pnon+Nom+Adj+Equ(cA[ce])+Noun+Zero+A3sg+Pnon+Nom')

        self.assert_parse_correct(u'öylece',
            u'öyle(öyle)+Adj+Adj+Equ(cA[ce])', 
            u'öyle(öyle)+Adj+Adj+Quite(cA[ce])', 
            u'öyle(öyle)+Adj+Adv+Ly(cA[ce])', 
            u'öyle(öyle)+Adj+Noun+Zero+A3sg+Pnon+Nom+Adj+Equ(cA[ce])', 
            u'öyle(öyle)+Adj+Noun+Zero+A3sg+Pnon+Nom+Adv+InTermsOf(cA[ce])',
            u'öyle(öyle)+Adj+Noun+Zero+A3sg+Pnon+Nom+Adv+By(cA[ce])',
            u'öyle(öyle)+Adj+Adj+Equ(cA[ce])+Noun+Zero+A3sg+Pnon+Nom', 
            u'öyle(öyle)+Adj+Adj+Quite(cA[ce])+Noun+Zero+A3sg+Pnon+Nom', 
            u'öyle(öyle)+Adj+Noun+Zero+A3sg+Pnon+Nom+Adj+Equ(cA[ce])+Noun+Zero+A3sg+Pnon+Nom')

        self.assert_parse_correct(u'sayıca',
            u'sayıca(sayıca)+Noun+A3sg+Pnon+Nom',
            u'sayı(sayı)+Noun+A3sg+Pnon+Nom+Adj+Equ(cA[ca])',
            u'sayı(sayı)+Noun+A3sg+Pnon+Nom+Adv+InTermsOf(cA[ca])',
            u'sayı(sayı)+Noun+A3sg+Pnon+Nom+Adv+By(cA[ca])',
            u'sayı(sayı)+Noun+A3sg+Pnon+Nom+Adj+Equ(cA[ca])+Noun+Zero+A3sg+Pnon+Nom')

        self.assert_parse_correct(u'onlarca',
            u'o(o)+Pron+Pers+A3pl(nlar[nlar])+Pnon+AccordingTo(ca[ca])')

        self.assert_parse_correct(u'saatlerce',
            u'saat(saat)+Noun+A3sg+Pnon+Nom+Adv+ManyOf(lArcA[lerce])',
            u'saat(saat)+Noun+A3pl(lAr[ler])+Pnon+Nom+Adj+Equ(cA[ce])',
            u'saat(saat)+Noun+A3pl(lAr[ler])+Pnon+Nom+Adv+InTermsOf(cA[ce])',
            u'saat(saat)+Noun+A3pl(lAr[ler])+Pnon+Nom+Adv+By(cA[ce])',
            u'saat(saat)+Noun+Time+A3sg+Pnon+Nom+Adv+ManyOf(lArcA[lerce])',
            u'saat(saat)+Noun+Time+A3sg+Pnon+Nom+Adv+ForALotOfTime(lArcA[lerce])',
            u'saat(saat)+Noun+Time+A3pl(lAr[ler])+Pnon+Nom+Adj+Equ(cA[ce])',
            u'saat(saat)+Noun+Time+A3pl(lAr[ler])+Pnon+Nom+Adv+InTermsOf(cA[ce])',
            u'saat(saat)+Noun+Time+A3pl(lAr[ler])+Pnon+Nom+Adv+By(cA[ce])',
            u'saat(saat)+Noun+A3pl(lAr[ler])+Pnon+Nom+Adj+Equ(cA[ce])+Noun+Zero+A3sg+Pnon+Nom',
            u'saat(saat)+Noun+Time+A3pl(lAr[ler])+Pnon+Nom+Adj+Equ(cA[ce])+Noun+Zero+A3sg+Pnon+Nom')

        self.assert_parse_correct(u'saliselerce',
            u'salise(salise)+Noun+Time+A3sg+Pnon+Nom+Adv+ManyOf(lArcA[lerce])',
            u'salise(salise)+Noun+Time+A3sg+Pnon+Nom+Adv+ForALotOfTime(lArcA[lerce])',
            u'salise(salise)+Noun+Time+A3pl(lAr[ler])+Pnon+Nom+Adj+Equ(cA[ce])',
            u'salise(salise)+Noun+Time+A3pl(lAr[ler])+Pnon+Nom+Adv+InTermsOf(cA[ce])',
            u'salise(salise)+Noun+Time+A3pl(lAr[ler])+Pnon+Nom+Adv+By(cA[ce])',
            u'salise(salise)+Noun+Time+A3pl(lAr[ler])+Pnon+Nom+Adj+Equ(cA[ce])+Noun+Zero+A3sg+Pnon+Nom')

        self.assert_parse_correct(u'makamlarca',
            u'makam(makam)+Noun+A3sg+Pnon+Nom+Adv+ManyOf(lArcA[larca])',
            u'makam(makam)+Noun+A3pl(lAr[lar])+Pnon+Nom+Adj+Equ(cA[ca])',
            u'makam(makam)+Noun+A3pl(lAr[lar])+Pnon+Nom+Adv+InTermsOf(cA[ca])',
            u'makam(makam)+Noun+A3pl(lAr[lar])+Pnon+Nom+Adv+By(cA[ca])',
            u'makam(makam)+Noun+A3pl(lAr[lar])+Pnon+Nom+Adj+Equ(cA[ca])+Noun+Zero+A3sg+Pnon+Nom')

        self.assert_parse_correct(u'organlarınca',      # as in "bu islem duyu organlarinca yapilir."
            u'organ(organ)+Noun+A3sg+P3pl(lArI![ları])+Nom+Adv+By(ncA[nca])', 
            u'organ(organ)+Noun+A3pl(lAr[lar])+P3sg(+sI[ı])+Nom+Adv+By(ncA[nca])', 
            u'organ(organ)+Noun+A3pl(lAr[lar])+P3pl(I![ı])+Nom+Adv+By(ncA[nca])')

        self.cloned_root_map[u'ben'] = filter(lambda root : root.lexeme.syntactic_category==SyntacticCategory.PRONOUN, self.cloned_root_map[u'ben'])
        self.cloned_root_map[u'biz'] = filter(lambda root : root.lexeme.syntactic_category==SyntacticCategory.PRONOUN, self.cloned_root_map[u'biz'])
        self.cloned_root_map[u'on'] = []
        self.cloned_root_map[u'onca'] = []
        self.cloned_root_map[u'bizle'] = []
        self.assert_parse_correct(u'bence',         u'ben(ben)+Pron+Pers+A1sg+Pnon+AccordingTo(ce[ce])')
        self.assert_parse_correct(u'sence',         u'sen(sen)+Pron+Pers+A2sg+Pnon+AccordingTo(ce[ce])')
        self.assert_parse_correct(u'onca',          u'o(o)+Pron+Pers+A3sg+Pnon+AccordingTo(nca[nca])')
        self.assert_parse_correct(u'bizce',         u'biz(biz)+Pron+Pers+A1pl+Pnon+AccordingTo(ce[ce])')
        self.assert_parse_correct(u'sizce',         u'siz(siz)+Pron+Pers+A2pl+Pnon+AccordingTo(ce[ce])')
        self.assert_parse_correct(u'onlarca',       u'o(o)+Pron+Pers+A3pl(nlar[nlar])+Pnon+AccordingTo(ca[ca])')
        self.assert_parse_correct(u'bizlerce',      u'biz(biz)+Pron+Pers+A1pl(ler[ler])+Pnon+AccordingTo(ce[ce])')
        self.assert_parse_correct(u'sizlerce',      u'siz(siz)+Pron+Pers+A2pl(ler[ler])+Pnon+AccordingTo(ce[ce])')
        self.assert_parse_correct(u'hepimizce',     u'hep(hepsi)+Pron+A1pl+P1pl(imiz[imiz])+AccordingTo(ce[ce])')
        self.assert_parse_correct(u'hepinizce',     u'hep(hepsi)+Pron+A2pl+P2pl(iniz[iniz])+AccordingTo(ce[ce])')
        self.assert_parse_correct(u'hepsince',      u'hepsi(hepsi)+Pron+A3pl+P3pl+AccordingTo(nce[nce])')

        # kendince, kendimce, kendilerince vs...



    def test_should_parse_verb_to_adj_zero_transition(self):
        self.assert_parse_correct_for_verb(u'pişmiş',
            u'piş(pişmek)+Verb+Pos+Narr(mIş[miş])+A3sg',                                # yemek pismis.
            u'piş(pişmek)+Verb+Pos+Narr(mIş[miş])+Adj+Zero',                            # pismis asa su katilmaz
            u'piş(pişmek)+Verb+Pos+Narr(mIş[miş])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom'     # onu degil, pismisi getir
        )

        self.assert_parse_correct_for_verb(u'bilir',
            u'bil(bilmek)+Verb+Pos+Aor(+Ir[ir])+A3sg',                                  # ali gelir.
            u'bil(bilmek)+Verb+Pos+Aor(+Ir[ir])+Adj+Zero',                              # tartışılır konu
            u'bil(bilmek)+Verb+Pos+Aor(+Ir[ir])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom'       # oluru bu
        )

        self.assert_parse_correct_for_verb(u'pişmemiş',
            u'piş(pişmek)+Verb+Neg(mA[me])+Narr(mIş[miş])+A3sg',
            u'piş(pişmek)+Verb+Neg(mA[me])+Narr(mIş[miş])+Adj+Zero',
            u'piş(pişmek)+Verb+Neg(mA[me])+Narr(mIş[miş])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom'
        )

        self.assert_parse_correct_for_verb(u'bilmez',
            u'bil(bilmek)+Verb+Neg(mA[me])+Aor(z[z])+A3sg',
            u'bil(bilmek)+Verb+Neg(mA[me])+Aor(z[z])+Adj+Zero',
            u'bil(bilmek)+Verb+Neg(mA[me])+Aor(z[z])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom'
        )

    def test_should_parse_de_ye(self):
        self.cloned_root_map[u'der'] = []
        self.cloned_root_map[u'deri'] = []
        self.cloned_root_map[u'derle'] = []
        self.cloned_root_map[u'derd'] = []
        self.cloned_root_map[u'dirim'] = []
        self.cloned_root_map[u'diri'] = []

        #TODO
        self.assert_not_parsable(u'dirim')
#        self.assert_not_parsable(u'deyecek')
        self.assert_not_parsable(u'deyor')
#        self.assert_not_parsable(u'deyen')

        self.assert_parse_correct_for_verb(u'derim',         u'de(demek)+Verb+Pos+Aor(+Ar[r])+A1sg(+Im[im])', u'de(demek)+Verb+Pos+Aor(+Ar[r])+Adj+Zero+Noun+Zero+A3sg+P1sg(+Im[im])+Nom')
        self.assert_parse_correct_for_verb(u'derler',        u'de(demek)+Verb+Pos+Aor(+Ar[r])+A3pl(lAr[ler])', u'de(demek)+Verb+Pos+Aor(+Ar[r])+Adj+Zero+Noun+Zero+A3pl(lAr[ler])+Pnon+Nom')
        self.assert_parse_correct_for_verb(u'dedim',         u'de(demek)+Verb+Pos+Past(dI[di])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'dediler',       u'de(demek)+Verb+Pos+Past(dI[di])+A3pl(lAr[ler])')
        self.assert_parse_correct_for_verb(u'demişim',       u'de(demek)+Verb+Pos+Narr(mI\u015f[mi\u015f])+A1sg(+Im[im])', u'de(demek)+Verb+Pos+Narr(mI\u015f[mi\u015f])+Adj+Zero+Noun+Zero+A3sg+P1sg(+Im[im])+Nom')
        self.assert_parse_correct_for_verb(u'demişler',      u'de(demek)+Verb+Pos+Narr(mI\u015f[mi\u015f])+A3pl(lAr[ler])', u'de(demek)+Verb+Pos+Narr(mI\u015f[mi\u015f])+Adj+Zero+Noun+Zero+A3pl(lAr[ler])+Pnon+Nom')
        self.assert_parse_correct_for_verb(u'diyeceğim',     u'di(demek)+Verb+Pos+Fut(yece\u011f[yece\u011f])+A1sg(+Im[im])', u'di(demek)+Verb+Pos+Adj+FutPart(yece\u011f[yece\u011f])+P1sg(+Im[im])', u'di(demek)+Verb+Pos+Noun+FutPart(yece\u011f[yece\u011f])+A3sg+P1sg(+Im[im])+Nom', u'di(demek)+Verb+Pos+Fut(yece\u011f[yece\u011f])+Adj+Zero+Noun+Zero+A3sg+P1sg(+Im[im])+Nom')
        self.assert_parse_correct_for_verb(u'diyecekler',    u'di(demek)+Verb+Pos+Fut(yecek[yecek])+A3pl(lAr[ler])', u'di(demek)+Verb+Pos+Noun+FutPart(yecek[yecek])+A3pl(lAr[ler])+Pnon+Nom', u'di(demek)+Verb+Pos+Fut(yecek[yecek])+Adj+Zero+Noun+Zero+A3pl(lAr[ler])+Pnon+Nom')
        self.assert_parse_correct_for_verb(u'diyorum',       u'di(demek)+Verb+Pos+Prog(yor[yor])+A1sg(+Im[um])')
        self.assert_parse_correct_for_verb(u'diyorlar',      u'di(demek)+Verb+Pos+Prog(yor[yor])+A3pl(lAr[lar])')
        self.assert_parse_correct_for_verb(u'demekteyim',    u'de(demek)+Verb+Pos+Prog(mAktA[mekte])+A1sg(yIm[yim])')
        self.assert_parse_correct_for_verb(u'demekteler',    u'de(demek)+Verb+Pos+Prog(mAktA[mekte])+A3pl(lAr[ler])')
        self.assert_parse_correct_for_verb(u'diyen',         u'di(demek)+Verb+Pos+Adj+PresPart(yen[yen])', u'di(demek)+Verb+Pos+Adj+PresPart(yen[yen])+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct_for_verb(u'dediğim',       u'de(demek)+Verb+Pos+Adj+PastPart(dIk[di\u011f])+P1sg(+Im[im])', u'de(demek)+Verb+Pos+Noun+PastPart(dIk[di\u011f])+A3sg+P1sg(+Im[im])+Nom')
        self.assert_parse_correct_for_verb(u'dedikleri',     u'de(demek)+Verb+Pos+Adj+PastPart(dIk[dik])+P3pl(lArI![leri])', u'de(demek)+Verb+Pos+Noun+PastPart(dIk[dik])+A3sg+P3pl(lArI![leri])+Nom', u'de(demek)+Verb+Pos+Noun+PastPart(dIk[dik])+A3pl(lAr[ler])+Pnon+Acc(+yI[i])', u'de(demek)+Verb+Pos+Noun+PastPart(dIk[dik])+A3pl(lAr[ler])+P3sg(+sI[i])+Nom', u'de(demek)+Verb+Pos+Noun+PastPart(dIk[dik])+A3pl(lAr[ler])+P3pl(I![i])+Nom')
        self.assert_parse_correct_for_verb(u'diyecekleri',   u'di(demek)+Verb+Pos+Adj+FutPart(yecek[yecek])+P3pl(lArI![leri])', u'di(demek)+Verb+Pos+Noun+FutPart(yecek[yecek])+A3sg+P3pl(lArI![leri])+Nom', u'di(demek)+Verb+Pos+Noun+FutPart(yecek[yecek])+A3pl(lAr[ler])+Pnon+Acc(+yI[i])', u'di(demek)+Verb+Pos+Noun+FutPart(yecek[yecek])+A3pl(lAr[ler])+P3sg(+sI[i])+Nom', u'di(demek)+Verb+Pos+Noun+FutPart(yecek[yecek])+A3pl(lAr[ler])+P3pl(I![i])+Nom', u'di(demek)+Verb+Pos+Fut(yecek[yecek])+Adj+Zero+Noun+Zero+A3sg+P3pl(lArI![leri])+Nom', u'di(demek)+Verb+Pos+Fut(yecek[yecek])+Adj+Zero+Noun+Zero+A3pl(lAr[ler])+Pnon+Acc(+yI[i])', u'di(demek)+Verb+Pos+Fut(yecek[yecek])+Adj+Zero+Noun+Zero+A3pl(lAr[ler])+P3sg(+sI[i])+Nom', u'di(demek)+Verb+Pos+Fut(yecek[yecek])+Adj+Zero+Noun+Zero+A3pl(lAr[ler])+P3pl(I![i])+Nom')
        self.assert_parse_correct_for_verb(u'diyebilirim',   u'di(demek)+Verb+Verb+Able(yebil[yebil])+Pos+Aor(+Ir[ir])+A1sg(+Im[im])', u'di(demek)+Verb+Verb+Able(yebil[yebil])+Pos+Aor(+Ir[ir])+Adj+Zero+Noun+Zero+A3sg+P1sg(+Im[im])+Nom')
        self.assert_parse_correct_for_verb(u'diyebilirler',  u'di(demek)+Verb+Verb+Able(yebil[yebil])+Pos+Aor(+Ir[ir])+A3pl(lAr[ler])', u'di(demek)+Verb+Verb+Able(yebil[yebil])+Pos+Aor(+Ir[ir])+Adj+Zero+Noun+Zero+A3pl(lAr[ler])+Pnon+Nom')
        self.assert_parse_correct_for_verb(u'dendim',        u'de(demek)+Verb+Verb+Pass(+In[n])+Pos+Past(dI[di])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'dendiler',      u'de(demek)+Verb+Verb+Pass(+In[n])+Pos+Past(dI[di])+A3pl(lAr[ler])')
        self.assert_parse_correct_for_verb(u'denildim',      u'de(demek)+Verb+Verb+Pass(+InIl[nil])+Pos+Past(dI[di])+A1sg(+Im[m])')
        self.assert_parse_correct_for_verb(u'denildiler',    u'de(demek)+Verb+Verb+Pass(+InIl[nil])+Pos+Past(dI[di])+A3pl(lAr[ler])')
        self.assert_parse_correct_for_verb(u'dedirir',       u'de(demek)+Verb+Verb+Caus(dIr[dir])+Pos+Aor(+Ir[ir])+A3sg', u'de(demek)+Verb+Verb+Caus(dIr[dir])+Pos+Aor(+Ir[ir])+Adj+Zero', u'de(demek)+Verb+Verb+Caus(dIr[dir])+Verb+Caus(Ir[ir])+Pos+Imp+A2sg', u'de(demek)+Verb+Verb+Caus(dIr[dir])+Pos+Aor(+Ir[ir])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct_for_verb(u'dedirirler',    u'de(demek)+Verb+Verb+Caus(dIr[dir])+Pos+Aor(+Ir[ir])+A3pl(lAr[ler])', u'de(demek)+Verb+Verb+Caus(dIr[dir])+Pos+Aor(+Ir[ir])+Adj+Zero+Noun+Zero+A3pl(lAr[ler])+Pnon+Nom')
        self.assert_parse_correct_for_verb(u'dediyse',       u'de(demek)+Verb+Pos+Past(dI[di])+Cond(+ysA[yse])+A3sg')
        self.assert_parse_correct_for_verb(u'dediyseler',    u'de(demek)+Verb+Pos+Past(dI[di])+Cond(+ysA[yse])+A3pl(lAr[ler])')
        self.assert_parse_correct_for_verb(u'demeliyim',     u'de(demek)+Verb+Pos+Neces(mAlI![meli])+A1sg(yIm[yim])')
        self.assert_parse_correct_for_verb(u'demeliler',     u'de(demek)+Verb+Pos+Neces(mAlI![meli])+A3pl(lAr[ler])', u'de(demek)+Verb+Pos+Noun+Inf(mA[me])+A3sg+Pnon+Nom+Adj+With(lI[li])+Noun+Zero+A3pl(lAr[ler])+Pnon+Nom')
        self.assert_parse_correct_for_verb(u'diye',          u'di(demek)+Verb+Pos+Opt(ye[ye])+A3sg', u'diye(diye)+Adv')
        self.assert_parse_correct_for_verb(u'dese',          u'de(demek)+Verb+Pos+Desr(sA[se])+A3sg')
        self.assert_parse_correct_for_verb(u'deseler',       u'de(demek)+Verb+Pos+Desr(sA[se])+A3pl(lAr[ler])')
        self.assert_parse_correct_for_verb(u'diyordular',    u'di(demek)+Verb+Pos+Prog(yor[yor])+Past(dI[du])+A3pl(lAr[lar])')
        self.assert_parse_correct_for_verb(u'demekteydiler', u'de(demek)+Verb+Pos+Prog(mAktA[mekte])+Past(ydI[ydi])+A3pl(lAr[ler])')
        self.assert_parse_correct_for_verb(u'derdiniz',      u'de(demek)+Verb+Pos+Aor(+Ar[r])+Past(dI[di])+A2pl(nIz[niz])')
        self.assert_parse_correct_for_verb(u'der',           u'de(demek)+Verb+Pos+Aor(+Ar[r])+A3sg', u'de(demek)+Verb+Pos+Aor(+Ar[r])+Adj+Zero', u'de(demek)+Verb+Pos+Aor(+Ar[r])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct_for_verb(u'denir',         u'de(demek)+Verb+Verb+Pass(+In[n])+Pos+Aor(+Ir[ir])+A3sg', u'de(demek)+Verb+Verb+Pass(+In[n])+Pos+Aor(+Ir[ir])+Adj+Zero', u'de(demek)+Verb+Verb+Pass(+In[n])+Verb+Caus(Ir[ir])+Pos+Imp+A2sg', u'de(demek)+Verb+Verb+Pass(+In[n])+Pos+Aor(+Ir[ir])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct_for_verb(u'denmiş',        u'de(demek)+Verb+Verb+Pass(+In[n])+Pos+Narr(mI\u015f[mi\u015f])+A3sg', u'de(demek)+Verb+Verb+Pass(+In[n])+Pos+Narr(mI\u015f[mi\u015f])+Adj+Zero', u'de(demek)+Verb+Verb+Pass(+In[n])+Pos+Narr(mI\u015f[mi\u015f])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct_for_verb(u'denilmiş',      u'de(demek)+Verb+Verb+Pass(+InIl[nil])+Pos+Narr(mI\u015f[mi\u015f])+A3sg', u'de(demek)+Verb+Verb+Pass(+InIl[nil])+Pos+Narr(mI\u015f[mi\u015f])+Adj+Zero', u'de(demek)+Verb+Verb+Pass(+InIl[nil])+Pos+Narr(mI\u015f[mi\u015f])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct_for_verb(u'diyen',         u'di(demek)+Verb+Pos+Adj+PresPart(yen[yen])', u'di(demek)+Verb+Pos+Adj+PresPart(yen[yen])+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct_for_verb(u'diyenler',      u'di(demek)+Verb+Pos+Adj+PresPart(yen[yen])+Noun+Zero+A3pl(lAr[ler])+Pnon+Nom')
        self.assert_parse_correct_for_verb(u'de',            u'de(de)+Conj', u'de(demek)+Verb+Pos+Imp+A2sg')
        self.assert_parse_correct_for_verb(u'desinler',      u'de(demek)+Verb+Pos+Imp+A3pl(sInlAr[sinler])')
        self.assert_parse_correct_for_verb(u'diyerek',       u'di(demek)+Verb+Pos+Adv+ByDoingSo(yerek[yerek])')


    def test_should_parse_some_problematic_words(self):
        self.cloned_root_map[u'ney'] = []

        self.assert_parse_correct_for_verb(u'bitirelim',         u'bit(bitmek)+Verb+Verb+Caus(Ir[ir])+Pos+Opt(A[e])+A1pl(lIm[lim])')
        self.assert_parse_correct_for_verb(u'bulmalıyım',        u'bul(bulmak)+Verb+Pos+Neces(mAlI![malı])+A1sg(yIm[yım])')
        self.assert_parse_correct_for_verb(u'diyordunuz',        u'di(demek)+Verb+Pos+Prog(yor[yor])+Past(dI[du])+A2pl(nIz[nuz])')
        self.assert_parse_correct_for_verb(u'yiyoruz',           u'yi(yemek)+Verb+Pos+Prog(yor[yor])+A1pl(+Iz[uz])')
        self.assert_parse_correct_for_verb(u'baksana',           u'bak(bakmak)+Verb+Pos+Imp(sAnA[sana])+A2sg')
        self.assert_parse_correct_for_verb(u'gelsenize',         u'gel(gelmek)+Verb+Pos+Imp(sAnIzA[senize])+A2pl')
        self.assert_parse_correct_for_verb(u'yapan',             u'yap(yapmak)+Verb+Pos+Adj+PresPart(+yAn[an])', u'yap(yapmak)+Verb+Pos+Adj+PresPart(+yAn[an])+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct_for_verb(u'diyen',             u'di(demek)+Verb+Pos+Adj+PresPart(yen[yen])', u'di(demek)+Verb+Pos+Adj+PresPart(yen[yen])+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct_for_verb(u'duyumsatınca',      u'duyumsa(duyumsamak)+Verb+Verb+Caus(t[t])+Pos+Adv+When(+yIncA[\u0131nca])')
#        self.assert_parse_correct_for_verb(u'duyumsatıncaya',    u'xxxxxxxxx')     #TODO
        self.assert_parse_doesnt_exist(u'yaparkene')
        self.assert_parse_doesnt_exist(u'yapıba')
        self.assert_parse_doesnt_exist(u'yaparcasınaya')
        self.assert_parse_correct_for_verb(u'evsahibi',         u'evsahib(evsahibi)+Noun+A3sg+P3sg(+sI[i])+Nom')
        self.assert_parse_correct_for_verb(u'serpiştirilmiş',   u'serp(serpmek)+Verb+Verb+Recip(+I\u015f[i\u015f])+Verb+Caus(dIr[tir])+Verb+Pass(+nIl[il])+Pos+Narr(mI\u015f[mi\u015f])+A3sg', u'serp(serpmek)+Verb+Verb+Recip(+I\u015f[i\u015f])+Verb+Caus(dIr[tir])+Verb+Pass(+nIl[il])+Pos+Narr(mI\u015f[mi\u015f])+Adj+Zero', u'serp(serpmek)+Verb+Verb+Recip(+I\u015f[i\u015f])+Verb+Caus(dIr[tir])+Verb+Pass(+nIl[il])+Pos+Narr(mI\u015f[mi\u015f])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct_for_verb(u'reddine',          u'redd(ret)+Noun+A3sg+P2sg(+In[in])+Dat(+yA[e])', u'redd(ret)+Noun+A3sg+P3sg(+sI[i])+Dat(nA[ne])')
        self.assert_parse_exists(u'yanlışlanabilirlik',         u'yanl\u0131\u015fla(yanl\u0131\u015flamak)+Verb+Verb+Pass(+In[n])+Verb+Able(+yAbil[abil])+Pos+Aor(+Ir[ir])+Adj+Zero+Noun+Ness(lIk[lik])+A3sg+Pnon+Nom')
        self.assert_parse_correct_for_verb(u'neyi',             u'ne(ne)+Pron+Ques+A3sg+P3sg(yi[yi])+Nom', u'ne(ne)+Pron+Ques+A3sg+Pnon+Acc(+yI[yi])', u'ne(ne)+Adj+Ques+Noun+Zero+A3sg+Pnon+Acc(+yI[yi])')
        self.assert_parse_correct_for_verb(u'neyin',            u'ne(ne)+Pron+Ques+A3sg+Pnon+Gen(yin[yin])', u'ne(ne)+Pron+Ques+A3sg+P2sg(yin[yin])+Nom')
        self.assert_parse_correct_for_verb(u'nesi',             u'ne(ne)+Pron+Ques+A3sg+P3sg(si[si])+Nom', u'ne(ne)+Adj+Ques+Noun+Zero+A3sg+P3sg(+sI[si])+Nom')
        self.assert_parse_correct_for_verb(u'neyim',            u'ne(ne)+Pron+Ques+A3sg+P1sg(yim[yim])+Nom')
        self.assert_parse_correct_for_verb(u'nen',              u'ne(ne)+Pron+Ques+A3sg+P2sg(n[n])+Nom', u'ne(ne)+Adj+Ques+Noun+Zero+A3sg+P2sg(+In[n])+Nom')
        self.assert_parse_correct_for_verb(u'neyine',           u'ne(ne)+Pron+Ques+A3sg+P2sg(yin[yin])+Dat(+yA[e])', u'ne(ne)+Pron+Ques+A3sg+P3sg(yi[yi])+Dat(nA[ne])')
        self.assert_parse_correct_for_verb(u'içerde',           u'i\xe7er(i\xe7eri)+Noun+A3sg+Pnon+Loc(de[de])', u'i\xe7(i\xe7mek)+Verb+Pos+Aor(+Ar[er])+Adj+Zero+Noun+Zero+A3sg+Pnon+Loc(dA[de])')
        self.assert_parse_correct_for_verb(u'içerden',          u'i\xe7er(i\xe7eri)+Noun+A3sg+Pnon+Abl(den[den])', u'i\xe7(i\xe7mek)+Verb+Pos+Aor(+Ar[er])+Adj+Zero+Noun+Zero+A3sg+Pnon+Abl(dAn[den])')
        self.assert_parse_correct_for_verb(u'dışarda',          u'd\u0131\u015far(d\u0131\u015far\u0131)+Noun+A3sg+Pnon+Loc(da[da])')
        self.assert_parse_correct_for_verb(u'dışardan',         u'd\u0131\u015far(d\u0131\u015far\u0131)+Noun+A3sg+Pnon+Abl(dan[dan])')
        self.assert_parse_correct_for_verb(u'inandırıcı',       u'inan(inanmak)+Verb+Verb+Caus(dIr[d\u0131r])+Pos+Adj+Agt(+yIcI[\u0131c\u0131])', u'inan(inanmak)+Verb+Verb+Caus(dIr[d\u0131r])+Pos+Adj+Agt(+yIcI[\u0131c\u0131])+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct_for_verb(u'hangisini',        u'hangi(hangi)+Adj+Noun+Zero+A3sg+P3sg(+sI[si])+Acc(nI[ni])')
        self.assert_parse_exists          (u'kaynakçılığını',   u'kaynak(kaynak)+Noun+A3sg+Pnon+Nom+Adj+Agt(cI[çı])+Noun+Zero+A3sg+Pnon+Nom+Noun+Title(lIk[lığ])+A3sg+P2sg(+In[ın])+Acc(+yI[ı])')
        self.assert_parse_correct_for_verb(u'yediremiyordu',    u'ye(yemek)+Verb+Verb+Caus(dIr[dir])+Verb+Able(+yA[e])+Neg(m[m])+Prog(Iyor[iyor])+Past(dI[du])+A3sg')
        self.assert_parse_exists          (u'saatlerce',        u'saat(saat)+Noun+Time+A3sg+Pnon+Nom+Adv+ForALotOfTime(lArcA[lerce])')
        self.assert_parse_exists          (u'defalarca',        u'defa(defa)+Noun+A3sg+Pnon+Nom+Adv+ManyOf(lArcA[larca])')
        self.assert_parse_correct_for_verb(u'deyip',            u'de(demek)+Verb+Pos+Adv+AfterDoingSo(+yIp[yip])')
        self.assert_parse_correct_for_verb(u'yiyip',            u'yi(yemek)+Verb+Pos+Adv+AfterDoingSo(yip[yip])')
        self.assert_parse_correct_for_verb(u'tıkıştırmak',      u't\u0131k(t\u0131kmak)+Verb+Verb+Recip(+I\u015f[\u0131\u015f])+Verb+Caus(dIr[t\u0131r])+Pos+Noun+Inf(mAk[mak])+A3sg+Pnon+Nom')
        self.assert_parse_correct_for_verb(u'büyütülüyor',      u'b\xfcy\xfc(b\xfcy\xfcmek)+Verb+Verb+Caus(t[t])+Verb+Pass(+nIl[\xfcl])+Pos+Prog(Iyor[\xfcyor])+A3sg')
        self.assert_parse_correct_for_verb(u'dayatabilir',      u'daya(dayamak)+Verb+Verb+Caus(t[t])+Verb+Able(+yAbil[abil])+Pos+Aor(+Ir[ir])+A3sg', u'daya(dayamak)+Verb+Verb+Caus(t[t])+Verb+Able(+yAbil[abil])+Pos+Aor(+Ir[ir])+Adj+Zero', u'daya(dayamak)+Verb+Verb+Caus(t[t])+Verb+Able(+yAbil[abil])+Pos+Aor(+Ir[ir])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct_for_verb(u'çağrılıyor',       u'\xe7a\u011fr(\xe7a\u011f\u0131rmak)+Verb+Verb+Pass(+nIl[\u0131l])+Pos+Prog(Iyor[\u0131yor])+A3sg')
        self.assert_parse_correct_for_verb(u'tutturmuştuk',     u'tut(tutmak)+Verb+Verb+Caus(dIr[tur])+Pos+Narr(mI\u015f[mu\u015f])+Past(dI[tu])+A1pl(k[k])')
        self.assert_parse_exists          (u'yaparcasına',      u'yap(yapmak)+Verb+Pos+Aor(+Ar[ar])+Adv+AsIf(cAsI!nA[cas\u0131na])')
        self.assert_parse_exists          (u'okur',             u'oku(okumak)+Verb+Pos+Aor(+Ar[r])+A3sg')
        self.assert_parse_exists          (u'okurcasına',       u'oku(okumak)+Verb+Pos+Aor(+Ar[r])+Adv+AsIf(cAsI!nA[casına])')
        self.assert_parse_exists          (u'okumuşçasına',     u'oku(okumak)+Verb+Pos+Narr(mI\u015f[mu\u015f])+Adv+AsIf(cAsI!nA[\xe7as\u0131na])')
        self.assert_parse_exists          (u'yeşillikleri',     u'yeşil(yeşil)+Adj+Noun+Zero+A3sg+Pnon+Nom+Adj+Y(lIk[lik])+Noun+Zero+A3sg+P3pl(lArI![leri])+Nom')
        self.assert_parse_correct_for_verb(u'sulandı',          u'sula(sulamak)+Verb+Verb+Pass(+In[n])+Pos+Past(dI[d\u0131])+A3sg', u'su(su)+Noun+A3sg+Pnon+Nom+Verb+Acquire(lAn[lan])+Pos+Past(dI[d\u0131])+A3sg')


    def test_should_parse_question_particles(self):
        self.assert_parse_correct_for_verb(u'mı',                u'mı(mı)+Ques+Pres+A3sg')
        self.assert_parse_correct_for_verb(u'mü',                u'mü(mü)+Ques+Pres+A3sg')
        self.assert_parse_correct_for_verb(u'müydük',            u'mü(mü)+Ques+Past(ydü[ydü])+A1pl(k[k])')
        self.assert_parse_correct_for_verb(u'mıydılar',          u'mı(mı)+Ques+Past(ydı[ydı])+A3pl(lar[lar])')
        self.assert_parse_correct_for_verb(u'mıyız',             u'mı(mı)+Ques+Pres+A1pl(yız[yız])')
        self.assert_parse_correct_for_verb(u'miymiş',            u'mi(mi)+Ques+Narr(ymiş[ymiş])+A3sg')
        self.assert_parse_correct_for_verb(u'miymişsiniz',       u'mi(mi)+Ques+Narr(ymiş[ymiş])+A2pl(siniz[siniz])')

    def test_should_parse_noun_compounds(self):
        self.assert_parse_correct_for_verb(u'zeytinyağı',        u'zeytinyağ(zeytinyağı)+Noun+A3sg+P3sg(+sI[ı])+Nom')
        self.assert_parse_correct_for_verb(u'zeytinyağına',      u'zeytinyağ(zeytinyağı)+Noun+A3sg+P3sg(+sI[ı])+Dat(nA[na])')
        self.assert_parse_correct_for_verb(u'zeytinyağlı',       u'zeytinyağ(zeytinyağı)+Noun+A3sg+Pnon+Nom+Adj+With(lI[lı])', u'zeytinyağ(zeytinyağı)+Noun+A3sg+Pnon+Nom+Adj+With(lI[lı])+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct_for_verb(u'zeytinyağlıya',     u'zeytinyağ(zeytinyağı)+Noun+A3sg+Pnon+Nom+Adj+With(lI[lı])+Noun+Zero+A3sg+Pnon+Dat(+yA[ya])')
        self.assert_parse_correct_for_verb(u'zeytinyağları',     u'zeytinyağ(zeytinyağı)+Noun+A3sg+P3pl(lArI![ları])+Nom')
        self.assert_parse_correct_for_verb(u'zeytinyağlarını',   u'zeytinyağ(zeytinyağı)+Noun+A3sg+P3pl(lArI![ları])+Acc(nI[nı])')

        self.cloned_root_map[u'a'] = []
        self.cloned_root_map[u'ak'] = []
        self.cloned_root_map[u'akşam'] = []
        self.cloned_root_map[u'akşamüstü'] = filter(lambda _root : _root.lexeme.syntactic_category==SyntacticCategory.NOUN, self.cloned_root_map[u'akşamüstü'])

        self.assert_parse_correct_for_verb(u'akşamüstü',         u'akşamüst(akşamüstü)+Noun+Time+A3sg+P3sg(+sI[ü])+Nom')
        self.assert_parse_correct_for_verb(u'akşamüstleri',      u'akşamüst(akşamüstü)+Noun+Time+A3sg+P3pl(lArI![leri])+Nom')
        self.assert_parse_correct_for_verb(u'akşamüstüne',       u'akşamüst(akşamüstü)+Noun+Time+A3sg+P3sg(+sI[ü])+Dat(nA[ne])')
        self.assert_parse_correct_for_verb(u'akşamüstlü',        u'akşamüst(akşamüstü)+Noun+Time+A3sg+Pnon+Nom+Adj+With(lI[lü])', u'akşamüst(akşamüstü)+Noun+Time+A3sg+Pnon+Nom+Adj+With(lI[lü])+Noun+Zero+A3sg+Pnon+Nom')

        #TODO:
        #self.assert_parse_correct_for_verb(u'zeytinyağım',       xxxx)
        #self.assert_parse_correct_for_verb(u'zeytinyağın',       xxxx)
        #self.assert_parse_correct_for_verb(u'zeytinyağı',        xxxx)
        #self.assert_parse_correct_for_verb(u'zeytinyağlarım',       xxxx)
        #self.assert_parse_correct_for_verb(u'zeytinyağların',       xxxx)
        #self.assert_parse_correct_for_verb(u'zeytinyağları',        xxxx)

    def test_should_parse_cogu_bircogu(self):
        self.assert_parse_correct_for_verb(u'çoğu',                u'çoğu(çoğu)+Adj', u'çoğu(çoğu)+Pron+A3sg+P3sg+Nom', u'çoğu(çoğu)+Adj+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct_for_verb(u'çoğumuz',             u'çoğu(çoğu)+Pron+A3sg+P1pl(muz[muz])+Nom', u'çoğu(çoğu)+Adj+Noun+Zero+A3sg+P1pl(+ImIz[muz])+Nom')
        self.assert_parse_correct_for_verb(u'çoğunun',             u'çoğu(çoğu)+Pron+A3sg+P3sg+Gen(+nIn[nun])', u'çoğu(çoğu)+Adj+Noun+Zero+A3sg+Pnon+Gen(+nIn[nun])', u'çoğu(çoğu)+Adj+Noun+Zero+A3sg+P2sg(+In[n])+Gen(+nIn[un])')
        self.assert_parse_correct_for_verb(u'çoğumuzdan',          u'çoğu(çoğu)+Pron+A3sg+P1pl(muz[muz])+Abl(dAn[dan])', u'çoğu(çoğu)+Adj+Noun+Zero+A3sg+P1pl(+ImIz[muz])+Abl(dAn[dan])')
        self.assert_parse_correct_for_verb(u'birçoğu',             u'bir\xe7o\u011fu(bir\xe7o\u011fu)+Pron+A3sg+P3sg+Nom')
        self.assert_parse_correct_for_verb(u'birçoğumuz',          u'birçoğu(birçoğu)+Pron+A3sg+P1pl(muz[muz])+Nom')
        self.assert_parse_correct_for_verb(u'birçoğunun',          u'birçoğu(birçoğu)+Pron+A3sg+P3sg+Gen(+nIn[nun])')
        self.assert_parse_correct_for_verb(u'birçoğumuzdan',       u'birçoğu(birçoğu)+Pron+A3sg+P1pl(muz[muz])+Abl(dAn[dan])')

    def test_should_parse_some_words_with_vowel_drops(self):
        self.assert_parse_correct(u'vaktimi',                 u'vakt(vakit)+Noun+A3sg+P1sg(+Im[im])+Acc(+yI[i])')
        self.assert_parse_correct(u'havliyle',                u'havl(havil)+Noun+A3sg+P3sg(+sI[i])+Ins(+ylA[yle])')
        self.assert_parse_correct(u'savruldu',                u'savr(savurmak)+Verb+Verb+Pass(+nIl[ul])+Pos+Past(dI[du])+A3sg')
        self.assert_parse_correct(u'kavruldu',                u'kavr(kavurmak)+Verb+Verb+Pass(+nIl[ul])+Pos+Past(dI[du])+A3sg')
        self.assert_parse_correct(u'sıyrılıyor',              u'sıyr(sıyırmak)+Verb+Verb+Pass(+nIl[ıl])+Pos+Prog(Iyor[ıyor])+A3sg')

    def test_should_parse_pronouns_with_implicit_possession(self):
        self.assert_parse_exists(u'bazıları',                   u'bazıları(bazıları)+Pron+A3sg+P3sg+Nom')
        self.assert_parse_doesnt_exist(u'bazıları',             u'bazıları(bazıları)+Pron+A3sg+Pnon+Nom')
        self.assert_parse_exists(u'bazılarına',                 u'bazıları(bazıları)+Pron+A3sg+P3sg+Dat(nA[na])')
        self.assert_parse_exists(u'bazılarımız',                u'bazıları(bazıları)+Pron+A3sg+P1pl(mız[mız])+Nom')
        self.assert_parse_exists(u'bazılarının',                u'bazıları(bazıları)+Pron+A3sg+P3sg+Gen(+nIn[nın])')
        self.assert_parse_exists(u'bazısı',                     u'bazısı(bazısı)+Pron+A3sg+P3sg+Nom')

        self.assert_parse_exists(u'kimileri',                   u'kimileri(kimileri)+Pron+A3sg+P3sg+Nom')
        self.assert_parse_doesnt_exist(u'kimileri',             u'kimileri(kimileri)+Pron+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'kimilerimiz',               u'kimileri(kimileri)+Pron+A3sg+P1pl(miz[miz])+Nom')
        self.assert_parse_correct(u'kimileriniz',               u'kimileri(kimileri)+Pron+A3sg+P2pl(niz[niz])+Nom')
        self.assert_parse_exists(u'kimilerinin',                u'kimileri(kimileri)+Pron+A3sg+P3sg+Gen(+nIn[nin])')
        self.assert_parse_correct(u'kimisi',                    u'kimisi(kimisi)+Pron+A3sg+P3sg+Nom')
        self.assert_parse_correct(u'kimisini',                  u'kimisi(kimisi)+Pron+A3sg+P3sg+Acc(nI[ni])')
        self.assert_parse_correct(u'kimisinin',                 u'kimisi(kimisi)+Pron+A3sg+P3sg+Gen(+nIn[nin])')
        self.assert_parse_exists(u'kimi',                       u'kimi(kimi)+Pron+A3sg+P3sg+Nom')
        self.assert_parse_correct(u'kimimiz',                   u'kimi(kimi)+Pron+A3sg+P1pl(miz[miz])+Nom', u'kim(kim)+Pron+Ques+A3sg+P1pl(+ImIz[imiz])+Nom')
        self.assert_parse_correct(u'kiminiz',                   u'kimi(kimi)+Pron+A3sg+P2pl(niz[niz])+Nom', u'kim(kim)+Pron+Ques+A3sg+P2pl(+InIz[iniz])+Nom')

        self.assert_parse_exists(u'birileri',                   u'birileri(birileri)+Pron+A3sg+P3sg+Nom')
        self.assert_parse_doesnt_exist(u'birileri',             u'birileri(birileri)+Pron+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'birilerimiz',               u'birileri(birileri)+Pron+A3sg+P1pl(miz[miz])+Nom')
        self.assert_parse_correct(u'birileriniz',               u'birileri(birileri)+Pron+A3sg+P2pl(niz[niz])+Nom')
        self.assert_parse_exists(u'birilerinin',                u'birileri(birileri)+Pron+A3sg+P3sg+Gen(+nIn[nin])')
        self.assert_parse_correct(u'birisi',                    u'birisi(birisi)+Pron+A3sg+P3sg+Nom')
        self.assert_parse_correct(u'birisinde',                 u'birisi(birisi)+Pron+A3sg+P3sg+Loc(ndA[nde])')
        self.assert_parse_correct(u'birisinin',                 u'birisi(birisi)+Pron+A3sg+P3sg+Gen(+nIn[nin])')
        self.assert_parse_exists(u'biri',                       u'biri(biri)+Pron+A3sg+P3sg+Nom')
        self.assert_parse_exists(u'birimiz',                    u'biri(biri)+Pron+A3sg+P1pl(miz[miz])+Nom')
        self.assert_parse_exists(u'biriniz',                    u'biri(biri)+Pron+A3sg+P2pl(niz[niz])+Nom')

        self.assert_parse_correct(u'hiçbirisi',                 u'hiçbirisi(hiçbirisi)+Pron+A3sg+P3sg+Nom')
        self.assert_parse_correct(u'hiçbirisinde',              u'hiçbirisi(hiçbirisi)+Pron+A3sg+P3sg+Loc(ndA[nde])')
        self.assert_parse_correct(u'hiçbirisinin',              u'hiçbirisi(hiçbirisi)+Pron+A3sg+P3sg+Gen(+nIn[nin])')
        self.assert_parse_correct(u'hiçbiri',                   u'hiçbiri(hiçbiri)+Pron+A3sg+P3sg+Nom')
        self.assert_parse_correct(u'hiçbirimiz',                u'hiçbiri(hiçbiri)+Pron+A3sg+P1pl(miz[miz])+Nom')
        self.assert_parse_correct(u'hiçbiriniz',                u'hiçbiri(hiçbiri)+Pron+A3sg+P2pl(niz[niz])+Nom')

        self.assert_parse_exists(u'birbiri',                    u'birbiri(birbiri)+Pron+A3sg+P3sg+Nom')
        self.assert_parse_exists(u'birbirine',                  u'birbiri(birbiri)+Pron+A3sg+P3sg+Dat(nA[ne])')
        self.assert_parse_exists(u'birbirinden',                u'birbiri(birbiri)+Pron+A3sg+P3sg+Abl(ndAn[nden])')
        self.assert_parse_exists(u'birbirimiz',                 u'birbiri(birbiri)+Pron+A1pl+P1pl(miz[miz])+Nom')
        self.assert_parse_exists(u'birbiriniz',                 u'birbiri(birbiri)+Pron+A2pl+P2pl(niz[niz])+Nom')
        self.assert_parse_exists(u'birbirinize',                u'birbiri(birbiri)+Pron+A2pl+P2pl(niz[niz])+Dat(+yA[e])')
        self.assert_parse_exists(u'birbirleri',                 u'birbir(birbiri)+Pron+A3pl+P3pl(leri[leri])+Nom')
        self.assert_parse_exists(u'birbirlerine',               u'birbir(birbiri)+Pron+A3pl+P3pl(leri[leri])+Dat(nA[ne])')

        self.assert_parse_exists(u'çoğu',                       u'çoğu(çoğu)+Pron+A3sg+P3sg+Nom')
        self.assert_parse_exists(u'çoğumuz',                    u'çoğu(çoğu)+Pron+A3sg+P1pl(muz[muz])+Nom')
        self.assert_parse_exists(u'çoğunuz',                    u'çoğu(çoğu)+Pron+A3sg+P2pl(nuz[nuz])+Nom')
        self.assert_parse_exists(u'birçoğu',                    u'birçoğu(birçoğu)+Pron+A3sg+P3sg+Nom')
        self.assert_parse_exists(u'birçoğumuz',                 u'birçoğu(birçoğu)+Pron+A3sg+P1pl(muz[muz])+Nom')
        self.assert_parse_exists(u'birçoğunuz',                 u'birçoğu(birçoğu)+Pron+A3sg+P2pl(nuz[nuz])+Nom')
        self.assert_parse_exists(u'çokları',                    u'çokları(çokları)+Pron+A3sg+P3pl+Nom')
        self.assert_parse_exists(u'birçokları',                 u'birçokları(birçokları)+Pron+A3sg+P3pl+Nom')

        self.assert_parse_exists(u'birkaçı',                    u'birkaçı(birkaçı)+Pron+A3sg+P3sg+Nom')
        self.assert_parse_exists(u'birkaçımız',                 u'birkaçı(birkaçı)+Pron+A3sg+P1pl(mız[mız])+Nom')
        self.assert_parse_exists(u'birkaçınız',                 u'birkaçı(birkaçı)+Pron+A3sg+P2pl(nız[nız])+Nom')

        self.assert_parse_exists(u'cümlesi',                    u'cümlesi(cümlesi)+Pron+A3sg+P3sg+Nom')
        self.assert_parse_exists(u'cümlesine',                  u'cümlesi(cümlesi)+Pron+A3sg+P3sg+Dat(nA[ne])')

        self.assert_parse_exists(u'diğeri',                     u'diğeri(diğeri)+Pron+A3sg+P3sg+Nom')
        self.assert_parse_exists(u'diğerinde',                  u'diğeri(diğeri)+Pron+A3sg+P3sg+Loc(ndA[nde])')
        self.assert_parse_exists(u'diğerimize',                 u'diğeri(diğeri)+Pron+A3sg+P1pl(miz[miz])+Dat(+yA[e])')
        self.assert_parse_exists(u'diğerinizin',                u'diğeri(diğeri)+Pron+A3sg+P2pl(niz[niz])+Gen(+nIn[in])')
        self.assert_parse_exists(u'diğerleri',                  u'diğerleri(diğerleri)+Pron+A3sg+P3pl+Nom')
        self.assert_parse_exists(u'diğerlerini',                u'diğerleri(diğerleri)+Pron+A3sg+P3pl+Acc(nI[ni])')
        self.assert_parse_exists(u'diğerlerimizle',             u'diğerleri(diğerleri)+Pron+A3sg+P1pl(miz[miz])+Ins(+ylA[le])')
        self.assert_parse_exists(u'diğerlerinize',              u'diğerleri(diğerleri)+Pron+A3sg+P2pl(niz[niz])+Dat(+yA[e])')

    def test_should_parse_irregular_pronouns(self):
        self.assert_parse_correct(u'herkes',            u'herkes(herkes)+Pron+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'herkese',           u'herkes(herkes)+Pron+A3sg+Pnon+Dat(+yA[e])')
        self.assert_parse_correct(u'herkesin',          u'herkes(herkes)+Pron+A3sg+Pnon+Gen(+nIn[in])')
        self.assert_parse_correct(u'herkeste',          u'herkes(herkes)+Pron+A3sg+Pnon+Loc(dA[te])')
        self.assert_parse_correct(u'herkesle',          u'herkes(herkes)+Pron+A3sg+Pnon+Ins(+ylA[le])')
        self.assert_parse_correct(u'herkesim',          )

    def test_should_parse_LIK_suffixes(self):
        self.assert_parse_exists(u'güzellik',              u'güzel(güzel)+Adj+Noun+Ness(lIk[lik])+A3sg+Pnon+Nom')
        self.assert_parse_exists(u'ustalık',               u'usta(usta)+Noun+A3sg+Pnon+Nom+Noun+Prof(lIk[lık])+A3sg+Pnon+Nom')
        self.assert_parse_exists(u'kitaplık',              u'kitap(kitap)+Noun+A3sg+Pnon+Nom+Noun+FitFor(lIk[lık])+A3sg+Pnon+Nom')
        self.assert_parse_exists(u'çamlık',                u'çam(çam)+Noun+A3sg+Pnon+Nom+Adj+Y(lIk[lık])')
        self.assert_parse_exists(u'kiralık',               u'kira(kira)+Noun+A3sg+Pnon+Nom+Adj+For(lIk[lık])')
        self.assert_parse_exists(u'savcılık',              u'savcı(savcı)+Noun+A3sg+Pnon+Nom+Noun+Title(lIk[lık])+A3sg+Pnon+Nom')
        self.assert_parse_exists(u'yıllık',                u'yıl(yıl)+Noun+Time+A3sg+Pnon+Nom+Adj+DurationOf(lIk[lık])')
        self.assert_parse_exists(u'dolarlık',              u'dolar(dolar)+Noun+A3sg+Pnon+Nom+Adj+OfUnit(lIk[lık])')

    def test_should_parse_relative_pronouns(self):
        self.cloned_root_map[u'on'] = []
        self.cloned_root_map[u'se'] = []
        self.cloned_root_map[u'bizle'] = []
        self.cloned_root_map[u'biz'] = filter(lambda root : root.lexeme.syntactic_category==SyntacticCategory.PRONOUN, self.cloned_root_map[u'biz'])

        self.assert_parse_correct(u'masamınki',            u'masa(masa)+Noun+A3sg+P1sg(+Im[m])+Gen(+nIn[ın])+Pron+A3sg(ki[ki])+Pnon+Nom')
        self.assert_parse_correct(u'masanınki',            u'masa(masa)+Noun+A3sg+Pnon+Gen(+nIn[nın])+Pron+A3sg(ki[ki])+Pnon+Nom', u'masa(masa)+Noun+A3sg+P2sg(+In[n])+Gen(+nIn[ın])+Pron+A3sg(ki[ki])+Pnon+Nom')
        self.assert_parse_correct(u'masamınkiler',         u'masa(masa)+Noun+A3sg+P1sg(+Im[m])+Gen(+nIn[ın])+Pron+A3pl(kiler[kiler])+Pnon+Nom')
        self.assert_parse_correct(u'masalarınınkiler',     u'masa(masa)+Noun+A3sg+P3pl(lArI![ları])+Gen(+nIn[nın])+Pron+A3pl(kiler[kiler])+Pnon+Nom', u'masa(masa)+Noun+A3pl(lAr[lar])+P2sg(+In[ın])+Gen(+nIn[ın])+Pron+A3pl(kiler[kiler])+Pnon+Nom', u'masa(masa)+Noun+A3pl(lAr[lar])+P3sg(+sI[ı])+Gen(+nIn[nın])+Pron+A3pl(kiler[kiler])+Pnon+Nom', u'masa(masa)+Noun+A3pl(lAr[lar])+P3pl(I![ı])+Gen(+nIn[nın])+Pron+A3pl(kiler[kiler])+Pnon+Nom')

        self.assert_parse_correct(u'masamınkine',          u'masa(masa)+Noun+A3sg+P1sg(+Im[m])+Gen(+nIn[ın])+Pron+A3sg(ki[ki])+Pnon+Dat(nA[ne])')
        self.assert_parse_correct(u'masanınkini',          u'masa(masa)+Noun+A3sg+Pnon+Gen(+nIn[nın])+Pron+A3sg(ki[ki])+Pnon+Acc(nI[ni])', u'masa(masa)+Noun+A3sg+P2sg(+In[n])+Gen(+nIn[ın])+Pron+A3sg(ki[ki])+Pnon+Acc(nI[ni])')
        self.assert_parse_correct(u'masamınkinde',         u'masa(masa)+Noun+A3sg+P1sg(+Im[m])+Gen(+nIn[ın])+Pron+A3sg(ki[ki])+Pnon+Loc(ndA[nde])')
        self.assert_parse_correct(u'masalarınınkilere',    u'masa(masa)+Noun+A3sg+P3pl(lArI![ları])+Gen(+nIn[nın])+Pron+A3pl(kiler[kiler])+Pnon+Dat(+yA[e])', u'masa(masa)+Noun+A3pl(lAr[lar])+P2sg(+In[ın])+Gen(+nIn[ın])+Pron+A3pl(kiler[kiler])+Pnon+Dat(+yA[e])', u'masa(masa)+Noun+A3pl(lAr[lar])+P3sg(+sI[ı])+Gen(+nIn[nın])+Pron+A3pl(kiler[kiler])+Pnon+Dat(+yA[e])', u'masa(masa)+Noun+A3pl(lAr[lar])+P3pl(I![ı])+Gen(+nIn[nın])+Pron+A3pl(kiler[kiler])+Pnon+Dat(+yA[e])')

        self.assert_parse_correct(u'benimki',              u'ben(ben)+Pron+Pers+A1sg+Pnon+Gen(im[im])+Pron+A3sg(ki[ki])+Pnon+Nom')
        self.assert_parse_correct(u'seninki',              u'sen(sen)+Pron+Pers+A2sg+Pnon+Gen(in[in])+Pron+A3sg(ki[ki])+Pnon+Nom')
        self.assert_parse_correct(u'onunki',               u'o(o)+Pron+Demons+A3sg+Pnon+Gen(nun[nun])+Pron+A3sg(ki[ki])+Pnon+Nom', u'o(o)+Pron+Pers+A3sg+Pnon+Gen(nun[nun])+Pron+A3sg(ki[ki])+Pnon+Nom')
        self.assert_parse_correct(u'onlarınkiler',         u'o(o)+Pron+Demons+A3pl(nlar[nlar])+Pnon+Gen(ın[ın])+Pron+A3pl(kiler[kiler])+Pnon+Nom', u'o(o)+Pron+Pers+A3pl(nlar[nlar])+Pnon+Gen(ın[ın])+Pron+A3pl(kiler[kiler])+Pnon+Nom')
        self.assert_parse_correct(u'bizlerinkilerin',      u'biz(biz)+Pron+Pers+A1pl(ler[ler])+Pnon+Gen(in[in])+Pron+A3pl(kiler[kiler])+Pnon+Gen(+nIn[in])')
        self.assert_parse_correct(u'bizlerinkilerinki',    u'biz(biz)+Pron+Pers+A1pl(ler[ler])+Pnon+Gen(in[in])+Pron+A3pl(kiler[kiler])+Pnon+Gen(+nIn[in])+Pron+A3sg(ki[ki])+Pnon+Nom')

        self.assert_parse_correct(u'benimkine',            u'ben(ben)+Pron+Pers+A1sg+Pnon+Gen(im[im])+Pron+A3sg(ki[ki])+Pnon+Dat(nA[ne])')
        self.assert_parse_correct(u'seninkini',            u'sen(sen)+Pron+Pers+A2sg+Pnon+Gen(in[in])+Pron+A3sg(ki[ki])+Pnon+Acc(nI[ni])')
        self.assert_parse_correct(u'onunkinden',           u'o(o)+Pron+Demons+A3sg+Pnon+Gen(nun[nun])+Pron+A3sg(ki[ki])+Pnon+Abl(ndAn[nden])', u'o(o)+Pron+Pers+A3sg+Pnon+Gen(nun[nun])+Pron+A3sg(ki[ki])+Pnon+Abl(ndAn[nden])')
        self.assert_parse_correct(u'onlarınkilerinkini',   u'o(o)+Pron+Demons+A3pl(nlar[nlar])+Pnon+Gen(ın[ın])+Pron+A3pl(kiler[kiler])+Pnon+Gen(+nIn[in])+Pron+A3sg(ki[ki])+Pnon+Acc(nI[ni])', u'o(o)+Pron+Pers+A3pl(nlar[nlar])+Pnon+Gen(ın[ın])+Pron+A3pl(kiler[kiler])+Pnon+Gen(+nIn[in])+Pron+A3sg(ki[ki])+Pnon+Acc(nI[ni])')
        self.assert_parse_correct(u'bizlerinkilerde',      u'biz(biz)+Pron+Pers+A1pl(ler[ler])+Pnon+Gen(in[in])+Pron+A3pl(kiler[kiler])+Pnon+Loc(dA[de])')
        self.assert_parse_correct(u'bizlerinkilere',       u'biz(biz)+Pron+Pers+A1pl(ler[ler])+Pnon+Gen(in[in])+Pron+A3pl(kiler[kiler])+Pnon+Dat(+yA[e])')

        self.assert_parse_correct(u'nereninki',            u'nere(nere)+Pron+Ques+A3sg+Pnon+Gen(+nIn[nin])+Pron+A3sg(ki[ki])+Pnon+Nom', u'nere(nere)+Pron+Ques+A3sg+P2sg(+In[n])+Gen(+nIn[in])+Pron+A3sg(ki[ki])+Pnon+Nom')
        self.assert_parse_correct(u'buramınki',            u'bura(bura)+Pron+A3sg+P1sg(+Im[m])+Gen(+nIn[ın])+Pron+A3sg(ki[ki])+Pnon+Nom')
        self.assert_parse_correct(u'nerelerimizinkiler',   u'nere(nere)+Pron+Ques+A3pl(lAr[ler])+P1pl(+ImIz[imiz])+Gen(+nIn[in])+Pron+A3pl(kiler[kiler])+Pnon+Nom')
        self.assert_parse_correct(u'nerelerimizinkilerin', u'nere(nere)+Pron+Ques+A3pl(lAr[ler])+P1pl(+ImIz[imiz])+Gen(+nIn[in])+Pron+A3pl(kiler[kiler])+Pnon+Gen(+nIn[in])')
        self.assert_parse_correct(u'nerelerimizinkilerde', u'nere(nere)+Pron+Ques+A3pl(lAr[ler])+P1pl(+ImIz[imiz])+Gen(+nIn[in])+Pron+A3pl(kiler[kiler])+Pnon+Loc(dA[de])')

        self.assert_not_parsable(u'masamınkin')
        self.assert_not_parsable(u'benimkilerim')
        self.assert_not_parsable(u'nereninkisi')

#        TODO
#        'beriki, öteki, öbürkü' --> complicated stuff
#        support all: "senin ötekin nereder", "berikini getir", "berikiyi getir", 'berikisi bizim ev'
#        self.assert_parse_correct(u'berikini',              u'xxx')
#        self.assert_parse_correct(u'berikisi',              u'xxx')
#        self.assert_parse_correct(u'berikiyi',              u'xxx')

if __name__ == '__main__':
    unittest.main()
