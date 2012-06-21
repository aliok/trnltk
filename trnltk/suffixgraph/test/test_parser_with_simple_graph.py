# coding=utf-8
from copy import copy
import logging
import os
import unittest
from hamcrest import *
from hamcrest.core.base_matcher import BaseMatcher
from trnltk.stem.dictionaryitem import PrimaryPosition
from trnltk.stem.dictionaryloader import DictionaryLoader
from trnltk.stem.stemgenerator import StemGenerator, StemRootMapGenerator
from trnltk.suffixgraph.parser import Parser, logger as parser_logger
from trnltk.suffixgraph.suffixapplier import logger as suffix_applier_logger
from trnltk.suffixgraph.predefinedpaths import PredefinedPaths
from trnltk.suffixgraph.suffixgraph import SuffixGraph

class ParserTestWithSimpleGraph(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(ParserTestWithSimpleGraph, cls).setUpClass()
        all_stems = []

        dictionary_items = DictionaryLoader.load_from_file(os.path.join(os.path.dirname(__file__), '../../resources/master_dictionary.txt'))
        for di in dictionary_items:
            all_stems.extend(StemGenerator.generate(di))

        cls._org_stem_root_map = (StemRootMapGenerator()).generate(all_stems)


    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        parser_logger.setLevel(logging.INFO)
        suffix_applier_logger.setLevel(logging.INFO)

        suffix_graph = SuffixGraph()
        cloned_stem_root_map = copy(self._org_stem_root_map)
        predefined_paths = PredefinedPaths(cloned_stem_root_map, suffix_graph)
        predefined_paths.create_predefined_paths()

        self.parser = Parser(cloned_stem_root_map, suffix_graph, predefined_paths)

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
        self.assert_parse_correct(u'korucu',           u'koru(koru)+Noun+A3sg+Pnon+Nom+Noun+Agt(cI[cu])+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'korucuyu',         u'koru(koru)+Noun+A3sg+Pnon+Nom+Noun+Agt(cI[cu])+A3sg+Pnon+Acc(+yI[yu])')
        self.assert_parse_correct(u'korucuya',         u'koru(koru)+Noun+A3sg+Pnon+Nom+Noun+Agt(cI[cu])+A3sg+Pnon+Dat(+yA[ya])')
        self.assert_parse_correct(u'korucuda',         u'koru(koru)+Noun+A3sg+Pnon+Nom+Noun+Agt(cI[cu])+A3sg+Pnon+Loc(dA[da])')
        self.assert_parse_correct(u'korucudan',        u'koru(koru)+Noun+A3sg+Pnon+Nom+Noun+Agt(cI[cu])+A3sg+Pnon+Abl(dAn[dan])')
        self.assert_parse_correct(u'korucunun',        u'koru(koru)+Noun+A3sg+Pnon+Nom+Noun+Agt(cI[cu])+A3sg+Pnon+Gen(+nIn[nun])', u'koru(koru)+Noun+A3sg+Pnon+Nom+Noun+Agt(cI[cu])+A3sg+P2sg(+In[n])+Gen(+nIn[un])')
        self.assert_parse_correct(u'korucuyla',        u'koru(koru)+Noun+A3sg+Pnon+Nom+Noun+Agt(cI[cu])+A3sg+Pnon+Ins(+ylA[yla])')

    def test_should_parse_noun_to_adjective_derivations(self):
        self.parser.stem_root_map[u'kut'] = []

        self.assert_parse_correct(u'kutulu',           u'kutu(kutu)+Noun+A3sg+Pnon+Nom+Adj+With(lI[lu])', u'kutu(kutu)+Noun+A3sg+Pnon+Nom+Adj+With(lI[lu])+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'kutusuz',          u'kutu(kutu)+Noun+A3sg+Pnon+Nom+Adj+Without(sIz[suz])', u'kutu(kutu)+Noun+A3sg+Pnon+Nom+Adj+Without(sIz[suz])+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'kutumsu',          u'kutu(kutu)+Noun+A3sg+Pnon+Nom+Adj+JustLike(+ImsI[msu])', u'kutu(kutu)+Noun+A3sg+Pnon+Nom+Adj+JustLike(+ImsI[msu])+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'telefonumsu',      u'telefon(telefon)+Noun+A3sg+Pnon+Nom+Adj+JustLike(+ImsI[umsu])', u'telefon(telefon)+Noun+A3sg+Pnon+Nom+Adj+JustLike(+ImsI[umsu])+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'meleğimsi',        u'meleğ(melek)+Noun+A3sg+Pnon+Nom+Adj+JustLike(+ImsI[imsi])', u'meleğ(melek)+Noun+A3sg+Pnon+Nom+Adj+JustLike(+ImsI[imsi])+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'masamınki',        u'masa(masa)+Noun+A3sg+P1sg(+Im[m])+Gen(+nIn[ın])+Adj+Rel(ki[ki])', u'masa(masa)+Noun+A3sg+P1sg(+Im[m])+Gen(+nIn[ın])+Adj+Rel(ki[ki])+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'masanınki',        u'masa(masa)+Noun+A3sg+Pnon+Gen(+nIn[nın])+Adj+Rel(ki[ki])', u'masa(masa)+Noun+A3sg+P2sg(+In[n])+Gen(+nIn[ın])+Adj+Rel(ki[ki])', u'masa(masa)+Noun+A3sg+Pnon+Gen(+nIn[nın])+Adj+Rel(ki[ki])+Noun+Zero+A3sg+Pnon+Nom', u'masa(masa)+Noun+A3sg+P2sg(+In[n])+Gen(+nIn[ın])+Adj+Rel(ki[ki])+Noun+Zero+A3sg+Pnon+Nom')

    def test_should_parse_noun_to_verb_derivations(self):
        #heyecanlan
        pass


    def test_should_parse_positive_verb_tenses(self):
        self.assert_parse_correct(u'yaparım',           u'yap(yapmak)+Verb+Pos+Aor(+Ar[ar])+A1sg(+Im[ım])', u'yap(yapmak)+Verb+Pos+Aor(+Ar[ar])+Adj+Zero+Noun+Zero+A3sg+P1sg(+Im[ım])+Nom')
        self.assert_parse_correct(u'yaparsın',          u'yap(yapmak)+Verb+Pos+Aor(+Ar[ar])+A2sg(sIn[sın])')
        self.assert_parse_correct(u'yapar',             u'yap(yapmak)+Verb+Pos+Aor(+Ar[ar])+A3sg', u'yap(yapmak)+Verb+Pos+Aor(+Ar[ar])+Adj+Zero', u'yap(yapmak)+Verb+Pos+Aor(+Ar[ar])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')

        self.assert_parse_correct(u'yapıyorum',         u'yap(yapmak)+Verb+Pos+Prog(Iyor[ıyor])+A1sg(+Im[um])')
        self.assert_parse_correct(u'yapıyorsun',        u'yap(yapmak)+Verb+Pos+Prog(Iyor[ıyor])+A2sg(sIn[sun])')
        self.assert_parse_correct(u'yapıyor',           u'yap(yapmak)+Verb+Pos+Prog(Iyor[ıyor])+A3sg')

        self.assert_parse_correct(u'yapmaktayım',       u'yap(yapmak)+Verb+Pos+Prog(mAktA[makta])+A1sg(yIm[yım])')
        self.assert_parse_correct(u'yapmaktasın',       u'yap(yapmak)+Verb+Pos+Prog(mAktA[makta])+A2sg(sIn[sın])')
        self.assert_parse_correct(u'yapmakta',          u'yap(yapmak)+Verb+Pos+Prog(mAktA[makta])+A3sg')

        self.assert_parse_correct(u'yapacağım',         u'yap(yapmak)+Verb+Pos+Fut(+yAcAk[acağ])+A1sg(+Im[ım])', u'yap(yapmak)+Verb+Pos+Adj+FutPart(+yAcAk[acağ])+P1sg(+Im[ım])', u'yap(yapmak)+Verb+Pos+Noun+FutPart(+yAcAk[acağ])+A3sg+P1sg(+Im[ım])+Nom')
        self.assert_parse_correct(u'yapacaksın',        u'yap(yapmak)+Verb+Pos+Fut(+yAcAk[acak])+A2sg(sIn[sın])')
        self.assert_parse_correct(u'yapacak',           u'yap(yapmak)+Verb+Pos+Fut(+yAcAk[acak])+A3sg', u'yap(yapmak)+Verb+Pos+Adj+FutPart(+yAcAk[acak])+Pnon', u'yap(yapmak)+Verb+Pos+Noun+FutPart(+yAcAk[acak])+A3sg+Pnon+Nom')

        self.assert_parse_correct(u'yaptım',            u'yap(yapmak)+Verb+Pos+Past(dI[tı])+A1sg(+Im[m])')
        self.assert_parse_correct(u'yaptın',            u'yap(yapmak)+Verb+Pos+Past(dI[tı])+A2sg(n[n])')
        self.assert_parse_correct(u'yaptı',             u'yap(yapmak)+Verb+Pos+Past(dI[tı])+A3sg')

        self.assert_parse_correct(u'yapmışım',          u'yap(yapmak)+Verb+Pos+Narr(mIş[mış])+A1sg(+Im[ım])', u'yap(yapmak)+Verb+Pos+Narr(mIş[mış])+Adj+Zero+Noun+Zero+A3sg+P1sg(+Im[ım])+Nom')
        self.assert_parse_correct(u'yapmışsın',         u'yap(yapmak)+Verb+Pos+Narr(mIş[mış])+A2sg(sIn[sın])')
        self.assert_parse_correct(u'yapmış',            u'yap(yapmak)+Verb+Pos+Narr(mIş[mış])+A3sg', u'yap(yapmak)+Verb+Pos+Narr(mIş[mış])+Adj+Zero', u'yap(yapmak)+Verb+Pos+Narr(mIş[mış])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')


        self.assert_parse_correct(u'çeviririm',         u'çevir(çevirmek)+Verb+Pos+Aor(+Ir[ir])+A1sg(+Im[im])', u'çevir(çevirmek)+Verb+Pos+Aor(+Ir[ir])+Adj+Zero+Noun+Zero+A3sg+P1sg(+Im[im])+Nom')
        self.assert_parse_correct(u'çevirirsin',        u'çevir(çevirmek)+Verb+Pos+Aor(+Ir[ir])+A2sg(sIn[sin])')
        self.assert_parse_correct(u'çevirir',           u'çevir(çevirmek)+Verb+Pos+Aor(+Ir[ir])+A3sg', u'çevir(çevirmek)+Verb+Pos+Aor(+Ir[ir])+Adj+Zero', u'çevir(çevirmek)+Verb+Pos+Aor(+Ir[ir])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')

        self.assert_parse_correct(u'çeviriyorum',       u'çevir(çevirmek)+Verb+Pos+Prog(Iyor[iyor])+A1sg(+Im[um])')
        self.assert_parse_correct(u'çeviriyorsun',      u'çevir(çevirmek)+Verb+Pos+Prog(Iyor[iyor])+A2sg(sIn[sun])')
        self.assert_parse_correct(u'çeviriyor',         u'çevir(çevirmek)+Verb+Pos+Prog(Iyor[iyor])+A3sg')

        self.assert_parse_correct(u'çevirmekteyim',     u'çevir(çevirmek)+Verb+Pos+Prog(mAktA[mekte])+A1sg(yIm[yim])')
        self.assert_parse_correct(u'çevirmektesin',     u'çevir(çevirmek)+Verb+Pos+Prog(mAktA[mekte])+A2sg(sIn[sin])')
        self.assert_parse_correct(u'çevirmekte',        u'çevir(çevirmek)+Verb+Pos+Prog(mAktA[mekte])+A3sg')

        self.assert_parse_correct(u'çevireceğim',       u'çevir(çevirmek)+Verb+Pos+Fut(+yAcAk[eceğ])+A1sg(+Im[im])', u'çevir(çevirmek)+Verb+Pos+Adj+FutPart(+yAcAk[eceğ])+P1sg(+Im[im])', u'çevir(çevirmek)+Verb+Pos+Noun+FutPart(+yAcAk[eceğ])+A3sg+P1sg(+Im[im])+Nom')
        self.assert_parse_correct(u'çevireceksin',      u'çevir(çevirmek)+Verb+Pos+Fut(+yAcAk[ecek])+A2sg(sIn[sin])')
        self.assert_parse_correct(u'çevirecek',         u'çevir(çevirmek)+Verb+Pos+Fut(+yAcAk[ecek])+A3sg', u'çevir(çevirmek)+Verb+Pos+Adj+FutPart(+yAcAk[ecek])+Pnon', u'çevir(çevirmek)+Verb+Pos+Noun+FutPart(+yAcAk[ecek])+A3sg+Pnon+Nom')

        self.assert_parse_correct(u'çevirdim',          u'çevir(çevirmek)+Verb+Pos+Past(dI[di])+A1sg(+Im[m])')
        self.assert_parse_correct(u'çevirdin',          u'çevir(çevirmek)+Verb+Pos+Past(dI[di])+A2sg(n[n])')
        self.assert_parse_correct(u'çevirdi',           u'çevir(çevirmek)+Verb+Pos+Past(dI[di])+A3sg')

        self.assert_parse_correct(u'çevirmişim',        u'çevir(çevirmek)+Verb+Pos+Narr(mIş[miş])+A1sg(+Im[im])', u'çevir(çevirmek)+Verb+Pos+Narr(mIş[miş])+Adj+Zero+Noun+Zero+A3sg+P1sg(+Im[im])+Nom')
        self.assert_parse_correct(u'çevirmişsin',       u'çevir(çevirmek)+Verb+Pos+Narr(mIş[miş])+A2sg(sIn[sin])')
        self.assert_parse_correct(u'çevirmiş',          u'çevir(çevirmek)+Verb+Pos+Narr(mIş[miş])+A3sg', u'çevir(çevirmek)+Verb+Pos+Narr(mIş[miş])+Adj+Zero', u'çevir(çevirmek)+Verb+Pos+Narr(mIş[miş])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')


        self.parser.stem_root_map[u'el'] = filter(lambda stem : stem.dictionary_item.lemma==u'elemek', self.parser.stem_root_map[u'el'])

        self.assert_parse_correct(u'elerim',            u'ele(elemek)+Verb+Pos+Aor(+Ir[r])+A1sg(+Im[im])', u'ele(elemek)+Verb+Pos+Aor(+Ar[r])+A1sg(+Im[im])', u'ele(elemek)+Verb+Pos+Aor(+Ir[r])+Adj+Zero+Noun+Zero+A3sg+P1sg(+Im[im])+Nom', u'ele(elemek)+Verb+Pos+Aor(+Ar[r])+Adj+Zero+Noun+Zero+A3sg+P1sg(+Im[im])+Nom')
        self.assert_parse_correct(u'elersin',           u'ele(elemek)+Verb+Pos+Aor(+Ir[r])+A2sg(sIn[sin])', u'ele(elemek)+Verb+Pos+Aor(+Ar[r])+A2sg(sIn[sin])')
        self.assert_parse_correct(u'eler',              u'ele(elemek)+Verb+Pos+Aor(+Ir[r])+A3sg', u'ele(elemek)+Verb+Pos+Aor(+Ar[r])+A3sg', u'ele(elemek)+Verb+Pos+Aor(+Ir[r])+Adj+Zero', u'ele(elemek)+Verb+Pos+Aor(+Ar[r])+Adj+Zero', u'ele(elemek)+Verb+Pos+Aor(+Ir[r])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom', u'ele(elemek)+Verb+Pos+Aor(+Ar[r])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')

        self.assert_parse_correct(u'eliyorum',          u'el(elemek)+Verb+Pos+Prog(Iyor[iyor])+A1sg(+Im[um])')
        self.assert_parse_correct(u'eliyorsun',         u'el(elemek)+Verb+Pos+Prog(Iyor[iyor])+A2sg(sIn[sun])')
        self.assert_parse_correct(u'eliyor',            u'el(elemek)+Verb+Pos+Prog(Iyor[iyor])+A3sg')

        self.assert_parse_correct(u'elemekteyim',       u'ele(elemek)+Verb+Pos+Prog(mAktA[mekte])+A1sg(yIm[yim])')
        self.assert_parse_correct(u'elemektesin',       u'ele(elemek)+Verb+Pos+Prog(mAktA[mekte])+A2sg(sIn[sin])')
        self.assert_parse_correct(u'elemekte',          u'ele(elemek)+Verb+Pos+Prog(mAktA[mekte])+A3sg')

        self.assert_parse_correct(u'eleyeceğim',        u'ele(elemek)+Verb+Pos+Fut(+yAcAk[yeceğ])+A1sg(+Im[im])', u'ele(elemek)+Verb+Pos+Adj+FutPart(+yAcAk[yeceğ])+P1sg(+Im[im])', u'ele(elemek)+Verb+Pos+Noun+FutPart(+yAcAk[yeceğ])+A3sg+P1sg(+Im[im])+Nom')
        self.assert_parse_correct(u'eleyeceksin',       u'ele(elemek)+Verb+Pos+Fut(+yAcAk[yecek])+A2sg(sIn[sin])')
        self.assert_parse_correct(u'eleyecek',          u'ele(elemek)+Verb+Pos+Fut(+yAcAk[yecek])+A3sg', u'ele(elemek)+Verb+Pos+Adj+FutPart(+yAcAk[yecek])+Pnon', u'ele(elemek)+Verb+Pos+Noun+FutPart(+yAcAk[yecek])+A3sg+Pnon+Nom')

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

        self.assert_parse_correct_for_verb(u'yapmıyorum',         u'yap(yapmak)+Verb+Neg(m[m])+Prog(Iyor[ıyor])+A1sg(+Im[um])')
        self.assert_parse_correct_for_verb(u'yapmıyorsun',        u'yap(yapmak)+Verb+Neg(m[m])+Prog(Iyor[ıyor])+A2sg(sIn[sun])')
        self.assert_parse_correct_for_verb(u'yapmıyor',           u'yap(yapmak)+Verb+Neg(m[m])+Prog(Iyor[ıyor])+A3sg')

        self.assert_parse_correct_for_verb(u'yapmamaktayım',      u'yap(yapmak)+Verb+Neg(mA[ma])+Prog(mAktA[makta])+A1sg(yIm[yım])')
        self.assert_parse_correct_for_verb(u'yapmamaktasın',      u'yap(yapmak)+Verb+Neg(mA[ma])+Prog(mAktA[makta])+A2sg(sIn[sın])')
        self.assert_parse_correct_for_verb(u'yapmamakta',         u'yap(yapmak)+Verb+Neg(mA[ma])+Prog(mAktA[makta])+A3sg')

        self.assert_parse_correct_for_verb(u'yapmayacağım',       u'yap(yapmak)+Verb+Neg(mA[ma])+Fut(+yAcAk[yacağ])+A1sg(+Im[ım])', u'yap(yapmak)+Verb+Neg(mA[ma])+Adj+FutPart(+yAcAk[yacağ])+P1sg(+Im[ım])', u'yap(yapmak)+Verb+Neg(mA[ma])+Noun+FutPart(+yAcAk[yacağ])+A3sg+P1sg(+Im[ım])+Nom')
        self.assert_parse_correct_for_verb(u'yapmayacaksın',      u'yap(yapmak)+Verb+Neg(mA[ma])+Fut(+yAcAk[yacak])+A2sg(sIn[sın])')
        self.assert_parse_correct_for_verb(u'yapmayacak',         u'yap(yapmak)+Verb+Neg(mA[ma])+Fut(+yAcAk[yacak])+A3sg', u'yap(yapmak)+Verb+Neg(mA[ma])+Adj+FutPart(+yAcAk[yacak])+Pnon', u'yap(yapmak)+Verb+Neg(mA[ma])+Noun+FutPart(+yAcAk[yacak])+A3sg+Pnon+Nom')

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
        self.assert_parse_correct_for_verb(u'çevirmemekte',       u'çevir(çevirmek)+Verb+Neg(mA[me])+Prog(mAktA[mekte])+A3sg')

        self.assert_parse_correct_for_verb(u'çevirmeyeceğim',     u'çevir(çevirmek)+Verb+Neg(mA[me])+Fut(+yAcAk[yeceğ])+A1sg(+Im[im])', u'çevir(çevirmek)+Verb+Neg(mA[me])+Adj+FutPart(+yAcAk[yeceğ])+P1sg(+Im[im])', u'çevir(çevirmek)+Verb+Neg(mA[me])+Noun+FutPart(+yAcAk[yeceğ])+A3sg+P1sg(+Im[im])+Nom')
        self.assert_parse_correct_for_verb(u'çevirmeyeceksin',    u'çevir(çevirmek)+Verb+Neg(mA[me])+Fut(+yAcAk[yecek])+A2sg(sIn[sin])')
        self.assert_parse_correct_for_verb(u'çevirmeyecek',       u'çevir(çevirmek)+Verb+Neg(mA[me])+Fut(+yAcAk[yecek])+A3sg', u'çevir(çevirmek)+Verb+Neg(mA[me])+Adj+FutPart(+yAcAk[yecek])+Pnon', u'çevir(çevirmek)+Verb+Neg(mA[me])+Noun+FutPart(+yAcAk[yecek])+A3sg+Pnon+Nom')

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
        self.assert_parse_correct_for_verb(u'elememekte',         u'ele(elemek)+Verb+Neg(mA[me])+Prog(mAktA[mekte])+A3sg')

        self.assert_parse_correct_for_verb(u'elemeyeceğim',       u'ele(elemek)+Verb+Neg(mA[me])+Fut(+yAcAk[yeceğ])+A1sg(+Im[im])', u'ele(elemek)+Verb+Neg(mA[me])+Adj+FutPart(+yAcAk[yeceğ])+P1sg(+Im[im])', u'ele(elemek)+Verb+Neg(mA[me])+Noun+FutPart(+yAcAk[yeceğ])+A3sg+P1sg(+Im[im])+Nom')
        self.assert_parse_correct_for_verb(u'elemeyeceksin',      u'ele(elemek)+Verb+Neg(mA[me])+Fut(+yAcAk[yecek])+A2sg(sIn[sin])')
        self.assert_parse_correct_for_verb(u'elemeyecek',         u'ele(elemek)+Verb+Neg(mA[me])+Fut(+yAcAk[yecek])+A3sg', u'ele(elemek)+Verb+Neg(mA[me])+Adj+FutPart(+yAcAk[yecek])+Pnon', u'ele(elemek)+Verb+Neg(mA[me])+Noun+FutPart(+yAcAk[yecek])+A3sg+Pnon+Nom')

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
        self.assert_parse_correct_for_verb(u'eleyemeyeceğim',    u'ele(elemek)+Verb+Verb+Able(+yA[ye])+Neg(mA[me])+Fut(+yAcAk[yeceğ])+A1sg(+Im[im])', u'ele(elemek)+Verb+Verb+Able(+yA[ye])+Neg(mA[me])+Adj+FutPart(+yAcAk[yeceğ])+P1sg(+Im[im])', u'ele(elemek)+Verb+Verb+Able(+yA[ye])+Neg(mA[me])+Noun+FutPart(+yAcAk[yeceğ])+A3sg+P1sg(+Im[im])+Nom')

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
        # remove some stems to make the test simple
        self.parser.stem_root_map[u'on'] = []
        self.parser.stem_root_map[u'ona'] = []
        self.parser.stem_root_map[u'bend'] = []
        self.parser.stem_root_map[u'bun'] = []
        self.parser.stem_root_map[u'ben'] = filter(lambda stem : stem.dictionary_item.primary_position==PrimaryPosition.PRONOUN, self.parser.stem_root_map[u'ben'])
        self.parser.stem_root_map[u'ban'] = filter(lambda stem : stem.dictionary_item.primary_position==PrimaryPosition.PRONOUN, self.parser.stem_root_map[u'ban'])
        self.parser.stem_root_map[u'san'] = filter(lambda stem : stem.dictionary_item.primary_position==PrimaryPosition.PRONOUN, self.parser.stem_root_map[u'san'])
        self.parser.stem_root_map[u'biz'] = filter(lambda stem : stem.dictionary_item.primary_position==PrimaryPosition.PRONOUN, self.parser.stem_root_map[u'biz'])

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
        self.assert_parse_correct(u'nerede',            u'nere(nere)+Pron+Ques+A3sg+Pnon+Loc(dA[de])')
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
        self.assert_parse_correct(u'kimimizle',         u'kim(kim)+Pron+Ques+A3sg+P1pl(+ImIz[imiz])+Ins(+ylA[le])', u'kimi(kimi)+Pron+A3sg+P1pl(+ImIz[miz])+Ins(+ylA[le])')
        self.assert_parse_correct(u'kimleri',           u'kim(kim)+Pron+Ques+A3sg+P3pl(lArI![leri])+Nom', u'kim(kim)+Pron+Ques+A3pl(lAr[ler])+Pnon+Acc(+yI[i])', u'kim(kim)+Pron+Ques+A3pl(lAr[ler])+P3sg(+sI[i])+Nom', u'kim(kim)+Pron+Ques+A3pl(lAr[ler])+P3pl(I![i])+Nom')
        self.assert_parse_correct(u'kimlerimiz',        u'kim(kim)+Pron+Ques+A3pl(lAr[ler])+P1pl(+ImIz[imiz])+Nom')
        self.assert_parse_correct(u'kimlerimize',       u'kim(kim)+Pron+Ques+A3pl(lAr[ler])+P1pl(+ImIz[imiz])+Dat(+yA[e])')
        self.assert_parse_correct(u'kimlerimizin',      u'kim(kim)+Pron+Ques+A3pl(lAr[ler])+P1pl(+ImIz[imiz])+Gen(+nIn[in])')

    def test_should_parse_pronoun_derivations(self):
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
            u'o(o)+Pron+Demons+A3sg+Pnon+Nom+Adj+Without(nsuz[nsuz])+Noun+Zero+A3sg+Pnon+Nom',
            u'on(on)+Num+Card+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom+Adj+Without(sIz[suz])',
            u'on(on)+Num+Card+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom+Adj+Without(sIz[suz])+Noun+Zero+A3sg+Pnon+Nom'
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
            u'o(o)+Pron+Demons+A3pl(nlar[nlar])+Pnon+Nom+Adj+Without(sIz[sız])+Noun+Zero+A3sg+Pnon+Nom',
            u'on(on)+Num+Card+Adj+Zero+Noun+Zero+A3pl(lAr[lar])+Pnon+Nom+Adj+Without(sIz[sız])',
            u'on(on)+Num+Card+Adj+Zero+Noun+Zero+A3pl(lAr[lar])+Pnon+Nom+Adj+Without(sIz[sız])+Noun+Zero+A3sg+Pnon+Nom'
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
            u'bun(bun)+Noun+A3pl(lAr[lar])+Pnon+Nom+Adj+Without(sIz[sız])',
            u'bu(bu)+Pron+Demons+A3pl(nlar[nlar])+Pnon+Nom+Adj+Without(sIz[sız])+Noun+Zero+A3sg+Pnon+Nom',
            u'bun(bun)+Noun+A3pl(lAr[lar])+Pnon+Nom+Adj+Without(sIz[sız])+Noun+Zero+A3sg+Pnon+Nom'
        )
        self.assert_parse_correct(u'şunlarsız',
            u'şu(şu)+Pron+Demons+A3pl(nlar[nlar])+Pnon+Nom+Adj+Without(sIz[sız])',
            u'şu(şu)+Pron+Demons+A3pl(nlar[nlar])+Pnon+Nom+Adj+Without(sIz[sız])+Noun+Zero+A3sg+Pnon+Nom'
        )

    def test_should_parse_some_imperatives(self):
        self.assert_parse_correct_for_verb(u'gel',               u'gel(gelmek)+Verb+Pos+Imp+A2sg')
        self.assert_parse_correct_for_verb(u'gelsin',            u'gel(gelmek)+Verb+Pos+Imp+A3sg(sIn[sin])')
        self.assert_parse_correct_for_verb(u'gelin',             u'gel(gelmek)+Verb+Pos+Imp+A2pl(+yIn[in])', u'gelin(gelin)+Noun+A3sg+Pnon+Nom', u'gel(gelmek)+Verb+Verb+Pass(+In[in])+Pos+Imp+A2sg')
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

    def test_should_parse_some_numerals(self):
        self.assert_parse_correct(u'iki',               u'iki(iki)+Num+Card+Adj+Zero', u'iki(iki)+Num+Card+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'sekiz',             u'sekiz(sekiz)+Num+Card+Adj+Zero', u'sekiz(sekiz)+Num+Card+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')

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

        self.parser.stem_root_map[u'ye'] = []
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
        self.assert_parse_correct_for_verb(u'sıkıştırıldığı',    u'sıkış(sıkışmak)+Verb+Verb+Caus(dIr[tır])+Verb+Pass(+nIl[ıl])+Pos+Adj+PastPart(dIk[dığ])+P3sg(+sI[ı])', u'sıkış(sıkışmak)+Verb+Verb+Caus(dIr[tır])+Verb+Pass(+nIl[ıl])+Pos+Noun+PastPart(dIk[dığ])+A3sg+Pnon+Acc(+yI[ı])', u'sıkış(sıkışmak)+Verb+Verb+Caus(dIr[tır])+Verb+Pass(+nIl[ıl])+Pos+Noun+PastPart(dIk[dığ])+A3sg+P3sg(+sI[ı])+Nom')


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
        self.assert_parse_correct(u'kalacak',           u'kal(kalmak)+Verb+Pos+Fut(+yAcAk[acak])+A3sg', u'kal(kalmak)+Verb+Pos+Adj+FutPart(+yAcAk[acak])+Pnon', u'kal(kalmak)+Verb+Pos+Noun+FutPart(+yAcAk[acak])+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'kalmayacak',        u'kal(kalmak)+Verb+Neg(mA[ma])+Fut(+yAcAk[yacak])+A3sg', u'kal(kalmak)+Verb+Neg(mA[ma])+Adj+FutPart(+yAcAk[yacak])+Pnon', u'kal(kalmak)+Verb+Neg(mA[ma])+Noun+FutPart(+yAcAk[yacak])+A3sg+Pnon+Nom')

        self.assert_parse_correct(u'bitecek',           u'bit(bitmek)+Verb+Pos+Fut(+yAcAk[ecek])+A3sg', u'bit(bitmek)+Verb+Pos+Adj+FutPart(+yAcAk[ecek])+Pnon', u'bit(bitmek)+Verb+Pos+Noun+FutPart(+yAcAk[ecek])+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'bitmeyecek',        u'bit(bitmek)+Verb+Neg(mA[me])+Fut(+yAcAk[yecek])+A3sg', u'bit(bitmek)+Verb+Neg(mA[me])+Adj+FutPart(+yAcAk[yecek])+Pnon', u'bit(bitmek)+Verb+Neg(mA[me])+Noun+FutPart(+yAcAk[yecek])+A3sg+Pnon+Nom')

        self.assert_parse_correct(u'kalacağım',         u'kal(kalmak)+Verb+Pos+Fut(+yAcAk[acağ])+A1sg(+Im[ım])', u'kal(kalmak)+Verb+Pos+Adj+FutPart(+yAcAk[acağ])+P1sg(+Im[ım])', u'kal(kalmak)+Verb+Pos+Noun+FutPart(+yAcAk[acağ])+A3sg+P1sg(+Im[ım])+Nom')
        self.assert_parse_correct(u'kalmayacağım',      u'kal(kalmak)+Verb+Neg(mA[ma])+Fut(+yAcAk[yacağ])+A1sg(+Im[ım])', u'kal(kalmak)+Verb+Neg(mA[ma])+Adj+FutPart(+yAcAk[yacağ])+P1sg(+Im[ım])', u'kal(kalmak)+Verb+Neg(mA[ma])+Noun+FutPart(+yAcAk[yacağ])+A3sg+P1sg(+Im[ım])+Nom')

        self.assert_parse_correct(u'kalacağımı',        u'kal(kalmak)+Verb+Pos+Noun+FutPart(+yAcAk[acağ])+A3sg+P1sg(+Im[ım])+Acc(+yI[ı])')
        self.assert_parse_correct(u'kalmayacağımı',     u'kal(kalmak)+Verb+Neg(mA[ma])+Noun+FutPart(+yAcAk[yacağ])+A3sg+P1sg(+Im[ım])+Acc(+yI[ı])')

        self.assert_parse_correct(u'kalacağıma',        u'kal(kalmak)+Verb+Pos+Noun+FutPart(+yAcAk[acağ])+A3sg+P1sg(+Im[ım])+Dat(+yA[a])')
        self.assert_parse_correct(u'kalmayacağıma',     u'kal(kalmak)+Verb+Neg(mA[ma])+Noun+FutPart(+yAcAk[yacağ])+A3sg+P1sg(+Im[ım])+Dat(+yA[a])')

        self.assert_parse_correct(u'kalacağın',         u'kal(kalmak)+Verb+Pos+Adj+FutPart(+yAcAk[acağ])+P2sg(+In[ın])', u'kal(kalmak)+Verb+Pos+Noun+FutPart(+yAcAk[acağ])+A3sg+Pnon+Gen(+nIn[ın])', u'kal(kalmak)+Verb+Pos+Noun+FutPart(+yAcAk[acağ])+A3sg+P2sg(+In[ın])+Nom')
        self.assert_parse_correct(u'kalmayacağın',      u'kal(kalmak)+Verb+Neg(mA[ma])+Adj+FutPart(+yAcAk[yacağ])+P2sg(+In[ın])', u'kal(kalmak)+Verb+Neg(mA[ma])+Noun+FutPart(+yAcAk[yacağ])+A3sg+Pnon+Gen(+nIn[ın])', u'kal(kalmak)+Verb+Neg(mA[ma])+Noun+FutPart(+yAcAk[yacağ])+A3sg+P2sg(+In[ın])+Nom')

        self.assert_parse_correct(u'kalacağını',        u'kal(kalmak)+Verb+Pos+Noun+FutPart(+yAcAk[acağ])+A3sg+P2sg(+In[ın])+Acc(+yI[ı])', u'kal(kalmak)+Verb+Pos+Noun+FutPart(+yAcAk[acağ])+A3sg+P3sg(+sI[ı])+Acc(nI[nı])')
        self.assert_parse_correct(u'kalmayacağını',     u'kal(kalmak)+Verb+Neg(mA[ma])+Noun+FutPart(+yAcAk[yacağ])+A3sg+P2sg(+In[ın])+Acc(+yI[ı])', u'kal(kalmak)+Verb+Neg(mA[ma])+Noun+FutPart(+yAcAk[yacağ])+A3sg+P3sg(+sI[ı])+Acc(nI[nı])')

        self.assert_parse_correct(u'kalacağına',        u'kal(kalmak)+Verb+Pos+Noun+FutPart(+yAcAk[acağ])+A3sg+P2sg(+In[ın])+Dat(+yA[a])', u'kal(kalmak)+Verb+Pos+Noun+FutPart(+yAcAk[acağ])+A3sg+P3sg(+sI[ı])+Dat(nA[na])')
        self.assert_parse_correct(u'kalmayacağına',     u'kal(kalmak)+Verb+Neg(mA[ma])+Noun+FutPart(+yAcAk[yacağ])+A3sg+P2sg(+In[ın])+Dat(+yA[a])', u'kal(kalmak)+Verb+Neg(mA[ma])+Noun+FutPart(+yAcAk[yacağ])+A3sg+P3sg(+sI[ı])+Dat(nA[na])')

        self.assert_parse_correct(u'kalacaklar',        u'kal(kalmak)+Verb+Pos+Fut(+yAcAk[acak])+A3pl(lAr[lar])', u'kal(kalmak)+Verb+Pos+Noun+FutPart(+yAcAk[acak])+A3pl(lAr[lar])+Pnon+Nom')
        self.assert_parse_correct(u'kalmayacaklar',     u'kal(kalmak)+Verb+Neg(mA[ma])+Fut(+yAcAk[yacak])+A3pl(lAr[lar])', u'kal(kalmak)+Verb+Neg(mA[ma])+Noun+FutPart(+yAcAk[yacak])+A3pl(lAr[lar])+Pnon+Nom')

        self.assert_parse_correct(u'kalacakları',       u'kal(kalmak)+Verb+Pos+Adj+FutPart(+yAcAk[acak])+P3pl(lArI![ları])', u'kal(kalmak)+Verb+Pos+Noun+FutPart(+yAcAk[acak])+A3pl(lAr[lar])+Pnon+Acc(+yI[ı])', u'kal(kalmak)+Verb+Pos+Noun+FutPart(+yAcAk[acak])+A3pl(lAr[lar])+P3sg(+sI[ı])+Nom', u'kal(kalmak)+Verb+Pos+Noun+FutPart(+yAcAk[acak])+A3pl(lAr[lar])+P3pl(I![ı])+Nom', u'kal(kalmak)+Verb+Pos+Noun+FutPart(+yAcAk[acak])+A3sg+P3pl(lArI![ları])+Nom')
        self.assert_parse_correct(u'kalmayacakları',    u'kal(kalmak)+Verb+Neg(mA[ma])+Adj+FutPart(+yAcAk[yacak])+P3pl(lArI![ları])', u'kal(kalmak)+Verb+Neg(mA[ma])+Noun+FutPart(+yAcAk[yacak])+A3pl(lAr[lar])+Pnon+Acc(+yI[ı])', u'kal(kalmak)+Verb+Neg(mA[ma])+Noun+FutPart(+yAcAk[yacak])+A3pl(lAr[lar])+P3sg(+sI[ı])+Nom', u'kal(kalmak)+Verb+Neg(mA[ma])+Noun+FutPart(+yAcAk[yacak])+A3pl(lAr[lar])+P3pl(I![ı])+Nom', u'kal(kalmak)+Verb+Neg(mA[ma])+Noun+FutPart(+yAcAk[yacak])+A3sg+P3pl(lArI![ları])+Nom')

        self.assert_parse_correct(u'kalacaklarımı',     u'kal(kalmak)+Verb+Pos+Noun+FutPart(+yAcAk[acak])+A3pl(lAr[lar])+P1sg(+Im[ım])+Acc(+yI[ı])')
        self.assert_parse_correct(u'kalmayacaklarımı',  u'kal(kalmak)+Verb+Neg(mA[ma])+Noun+FutPart(+yAcAk[yacak])+A3pl(lAr[lar])+P1sg(+Im[ım])+Acc(+yI[ı])')

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
        self.assert_parse_correct(u'kendinden',          u'kendi(kendi)+Pron+Reflex+A2sg+P2sg(n[n])+Abl(den[den])', u'kendi(kendi)+Pron+Reflex+A3sg+P3sg+Abl(nden[nden])')
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

    def test_should_parse_pronoun_adj_to_noun_zero_transition(self):
        self.assert_parse_correct(u'maviye',             u'mavi(mavi)+Adj+Noun+Zero+A3sg+Pnon+Dat(+yA[ye])')
        self.assert_parse_correct(u'gencin',             u'genc(genç)+Adj+Noun+Zero+A3sg+Pnon+Gen(+nIn[in])',  u'genc(genç)+Adj+Noun+Zero+A3sg+P2sg(+In[in])+Nom', u'gen(gen)+Noun+A3sg+Pnon+Nom+Noun+Agt(cI[ci])+A3sg+P2sg(+In[n])+Nom')

    def test_should_parse_pronoun_verb_to_adv_derivations(self):
        self.assert_parse_correct(u'yapınca',             u'yap(yapmak)+Verb+Pos+Adv+When(+yIncA[ınca])')
        self.assert_parse_correct(u'yapmayınca',          u'yap(yapmak)+Verb+Neg(mA[ma])+Adv+When(+yIncA[yınca])')
        self.assert_parse_correct(u'dönünce',             u'dön(dönmek)+Verb+Pos+Adv+When(+yIncA[ünce])')
        self.assert_parse_correct(u'dönmeyince',          u'dön(dönmek)+Verb+Neg(mA[me])+Adv+When(+yIncA[yince])')
        self.assert_parse_correct(u'yalayınca',           u'yala(yalamak)+Verb+Pos+Adv+When(+yIncA[yınca])')
        self.assert_parse_correct(u'yalamayınca',         u'yala(yalamak)+Verb+Neg(mA[ma])+Adv+When(+yIncA[yınca])')
        self.assert_parse_correct(u'çıkarttırabilince',   u'çık(çıkmak)+Verb+Verb+Caus(Ar[ar])+Verb+Caus(t[t])+Verb+Caus(dIr[tır])+Verb+Able(+yAbil[abil])+Pos+Adv+When(+yIncA[ince])')
        self.assert_parse_correct(u'yaptıramayınca',      u'yap(yapmak)+Verb+Verb+Caus(dIr[tır])+Verb+Able(+yA[a])+Neg(mA[ma])+Adv+When(+yIncA[yınca])')

        self.parser.stem_root_map[u'dönel'] = []

        self.assert_parse_correct(u'yapalı',              u'yap(yapmak)+Verb+Pos+Adv+SinceDoingSo(+yAlI![alı])')
        self.assert_parse_correct(u'yapmayalı',           u'yap(yapmak)+Verb+Neg(mA[ma])+Adv+SinceDoingSo(+yAlI![yalı])')
        self.assert_parse_correct(u'döneli',              u'dön(dönmek)+Verb+Pos+Adv+SinceDoingSo(+yAlI![eli])')
        self.assert_parse_correct(u'dönmeyeli',           u'dön(dönmek)+Verb+Neg(mA[me])+Adv+SinceDoingSo(+yAlI![yeli])')
        self.assert_parse_correct(u'yalayalı',            u'yala(yalamak)+Verb+Pos+Adv+SinceDoingSo(+yAlI![yalı])')
        self.assert_parse_correct(u'yalamayalı',          u'yala(yalamak)+Verb+Neg(mA[ma])+Adv+SinceDoingSo(+yAlI![yalı])')
        self.assert_parse_correct(u'çıkarttırabileli',    u'çık(çıkmak)+Verb+Verb+Caus(Ar[ar])+Verb+Caus(t[t])+Verb+Caus(dIr[tır])+Verb+Able(+yAbil[abil])+Pos+Adv+SinceDoingSo(+yAlI![eli])')
        self.assert_parse_correct(u'yaptıramayalı',       u'yap(yapmak)+Verb+Verb+Caus(dIr[tır])+Verb+Able(+yA[a])+Neg(mA[ma])+Adv+SinceDoingSo(+yAlI![yalı])')

    def test_should_parse_pronoun_adj_to_adj_derivations(self):
        self.parser.stem_root_map[u'koy'] = []

        self.assert_parse_correct(u'kırmızımsı',          u'kırmızı(kırmızı)+Adj+Adj+JustLike(+ImsI[msı])', u'kırmızı(kırmızı)+Adj+Noun+Zero+A3sg+Pnon+Nom+Adj+JustLike(+ImsI[msı])', u'kırmızı(kırmızı)+Adj+Adj+JustLike(+ImsI[msı])+Noun+Zero+A3sg+Pnon+Nom', u'kırmızı(kırmızı)+Adj+Noun+Zero+A3sg+Pnon+Nom+Adj+JustLike(+ImsI[msı])+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'yeşilimsi',           u'yeşil(yeşil)+Adj+Adj+JustLike(+ImsI[imsi])', u'yeşil(yeşil)+Adj+Noun+Zero+A3sg+Pnon+Nom+Adj+JustLike(+ImsI[imsi])', u'yeşil(yeşil)+Adj+Adj+JustLike(+ImsI[imsi])+Noun+Zero+A3sg+Pnon+Nom', u'yeşil(yeşil)+Adj+Noun+Zero+A3sg+Pnon+Nom+Adj+JustLike(+ImsI[imsi])+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct(u'koyumsu',             u'koyu(koyu)+Adj+Adj+JustLike(+ImsI[msu])', u'koyu(koyu)+Adj+Noun+Zero+A3sg+Pnon+Nom+Adj+JustLike(+ImsI[msu])', u'koyu(koyu)+Adj+Adj+JustLike(+ImsI[msu])+Noun+Zero+A3sg+Pnon+Nom', u'koyu(koyu)+Adj+Noun+Zero+A3sg+Pnon+Nom+Adj+JustLike(+ImsI[msu])+Noun+Zero+A3sg+Pnon+Nom')

    def test_should_parse_pronoun_verb_to_adj_zero_transition(self):
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

    def test_should_parse_some_problematic_words(self):
        self.assert_parse_correct_for_verb(u'bitirelim',         u'bit(bitmek)+Verb+Verb+Caus(Ir[ir])+Pos+Opt(A[e])+A1pl(lIm[lim])')
        self.assert_parse_correct_for_verb(u'bulmalıyım',        u'bul(bulmak)+Verb+Pos+Neces(mAlI![malı])+A1sg(yIm[yım])')
        self.assert_parse_correct_for_verb(u'diyordunuz',        u'd(demek)+Verb+Pos+Prog(Iyor[iyor])+Past(dI[du])+A2pl(nIz[nuz])')
        self.assert_parse_correct_for_verb(u'yiyoruz',           u'y(yemek)+Verb+Pos+Prog(Iyor[iyor])+A1pl(+Iz[uz])')
        self.assert_parse_correct_for_verb(u'baksana',           u'bak(bakmak)+Verb+Pos+Imp(sAnA[sana])+A2sg')
        self.assert_parse_correct_for_verb(u'gelsenize',         u'gel(gelmek)+Verb+Pos+Imp(sAnIzA[senize])+A2pl')

        # remove some token to keep the test easier
        # TODO: low priority
#        self.parser.stem_root_map[u'ha'] = []
#        self.parser.stem_root_map[u'hav'] = []
#        self.parser.stem_root_map[u'havl'] = filter(lambda stem : stem.dictionary_item.primary_position==PrimaryPosition.NOUN, self.parser.stem_root_map[u'havl'])
#        self.assert_parse_correct_for_verb(u'havli',             u'gel(gelmek)+Verb+Pos+Imp(sAnIzA[senize])+A2pl')
#        self.assert_parse_correct_for_verb(u'havliyle',          u'gel(gelmek)+Verb+Pos+Imp(sAnIzA[senize])+A2pl')

    def test_should_parse_question_particles(self):
        self.assert_parse_correct_for_verb(u'mı',                u'mı(mı)+Ques+Pres+A3sg')
        self.assert_parse_correct_for_verb(u'mü',                u'mü(mü)+Ques+Pres+A3sg')
        self.assert_parse_correct_for_verb(u'müydük',            u'mü(mü)+Ques+Past(ydü[ydü])+A1pl(k[k])')
        self.assert_parse_correct_for_verb(u'mıydılar',          u'mı(mı)+Ques+Past(ydı[ydı])+A3pl(lar[lar])')
        self.assert_parse_correct_for_verb(u'mıyız',             u'mı(mı)+Ques+Pres+A1pl(yız[yız])')
        self.assert_parse_correct_for_verb(u'miymişsiniz',       u'mi(mi)+Ques+Past(ymiş[ymiş])+A2pl(siniz[siniz])')

    def test_should_parse_noun_compounds(self):
        self.assert_parse_correct_for_verb(u'zeytinyağı',        u'zeytinyağ(zeytinyağı)+Noun+A3sg+P3sg(+sI[ı])+Nom')
        self.assert_parse_correct_for_verb(u'zeytinyağına',      u'zeytinyağ(zeytinyağı)+Noun+A3sg+P3sg(+sI[ı])+Dat(nA[na])')
        self.assert_parse_correct_for_verb(u'zeytinyağlı',       u'zeytinyağ(zeytinyağı)+Noun+A3sg+Pnon+Nom+Adj+With(lI[lı])', u'zeytinyağ(zeytinyağı)+Noun+A3sg+Pnon+Nom+Adj+With(lI[lı])+Noun+Zero+A3sg+Pnon+Nom')
        self.assert_parse_correct_for_verb(u'zeytinyağlıya',     u'zeytinyağ(zeytinyağı)+Noun+A3sg+Pnon+Nom+Adj+With(lI[lı])+Noun+Zero+A3sg+Pnon+Dat(+yA[ya])')
        self.assert_parse_correct_for_verb(u'zeytinyağları',     u'zeytinyağ(zeytinyağı)+Noun+A3sg+P3pl(lArI![ları])+Nom')
        self.assert_parse_correct_for_verb(u'zeytinyağlarını',   u'zeytinyağ(zeytinyağı)+Noun+A3sg+P3pl(lArI![ları])+Acc(nI[nı])')

        self.parser.stem_root_map[u'a'] = []
        self.parser.stem_root_map[u'ak'] = []
        self.parser.stem_root_map[u'akşam'] = []

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
