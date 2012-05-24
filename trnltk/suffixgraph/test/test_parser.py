# coding=utf-8
import logging
import os
import unittest
from hamcrest import *
from hamcrest.core.base_matcher import BaseMatcher
from trnltk.stem.dictionaryitem import  PrimaryPosition
from trnltk.stem.dictionaryloader import DictionaryLoader
from trnltk.stem.stemgenerator import StemGenerator
from trnltk.suffixgraph.parser import Parser, logger as parser_logger

class ParserTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(ParserTest, cls).setUpClass()
        cls.all_stems = []

        dictionary_items = DictionaryLoader.load_from_file(os.path.join(os.path.dirname(__file__), '../../resources/master_dictionary.txt'))
        for di in dictionary_items:
            if di.primary_position in [PrimaryPosition.NOUN, PrimaryPosition.VERB]:
                cls.all_stems.extend(StemGenerator.generate(di))

        cls.parser = Parser(cls.all_stems)

    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        parser_logger.setLevel(logging.INFO)

    def test_should_parse_noun_cases(self):
        self.assert_parse_correct(u'sokak',            u'sokak(sokak)+Noun+A3Sg+Pnon+Nom')

        self.assert_parse_correct(u'kapıyı',           u'kapı(kapı)+Noun+A3Sg+Pnon+Acc(+yI[yı])')
        self.assert_parse_correct(u'kapıya',           u'kapı(kapı)+Noun+A3Sg+Pnon+Dat(+yA[ya])')
        self.assert_parse_correct(u'kapıda',           u'kapı(kapı)+Noun+A3Sg+Pnon+Loc(dA[da])')
        self.assert_parse_correct(u'kapıdan',          u'kapı(kapı)+Noun+A3Sg+Pnon+Abl(dAn[dan])')
        self.assert_parse_correct(u'kapının',          u'kapı(kapı)+Noun+A3Sg+Pnon+Gen(+nIn[nın])')
        self.assert_parse_correct(u'sokağın',          u'sokağ(sokak)+Noun+A3Sg+Pnon+Gen(+nIn[ın])')
        self.assert_parse_correct(u'sokakla',          u'sokak(sokak)+Noun+A3Sg+Pnon+Inst(+ylA[la])')

        self.assert_parse_correct(u'sokaklar',         u'sokak(sokak)+Noun+A3Pl(lAr[lar])+Pnon+Nom')
        self.assert_parse_correct(u'sokakları',        u'sokak(sokak)+Noun+A3Pl(lAr[lar])+Pnon+Acc(+yI[ı])')
        self.assert_parse_correct(u'sokaklara',        u'sokak(sokak)+Noun+A3Pl(lAr[lar])+Pnon+Dat(+yA[a])')
        self.assert_parse_correct(u'sokaklarda',       u'sokak(sokak)+Noun+A3Pl(lAr[lar])+Pnon+Loc(dA[da])')
        self.assert_parse_correct(u'sokaklardan',      u'sokak(sokak)+Noun+A3Pl(lAr[lar])+Pnon+Abl(dAn[dan])')
        self.assert_parse_correct(u'sokakların',       u'sokak(sokak)+Noun+A3Pl(lAr[lar])+Pnon+Gen(+nIn[ın])')
        self.assert_parse_correct(u'sokaklarla',       u'sokak(sokak)+Noun+A3Pl(lAr[lar])+Pnon+Inst(+ylA[la])')

    def test_should_parse_noun_to_noun_derivations(self):
        self.assert_parse_correct(u'korucu',           u'koru(koru)+Noun+A3Sg+Pnon+Nom+Noun+Agt(cI[cu])+A3Sg+Pnon+Nom')
        self.assert_parse_correct(u'korucuyu',         u'koru(koru)+Noun+A3Sg+Pnon+Nom+Noun+Agt(cI[cu])+A3Sg+Pnon+Acc(+yI[yu])')
        self.assert_parse_correct(u'korucuya',         u'koru(koru)+Noun+A3Sg+Pnon+Nom+Noun+Agt(cI[cu])+A3Sg+Pnon+Dat(+yA[ya])')
        self.assert_parse_correct(u'korucuda',         u'koru(koru)+Noun+A3Sg+Pnon+Nom+Noun+Agt(cI[cu])+A3Sg+Pnon+Loc(dA[da])')
        self.assert_parse_correct(u'korucudan',        u'koru(koru)+Noun+A3Sg+Pnon+Nom+Noun+Agt(cI[cu])+A3Sg+Pnon+Abl(dAn[dan])')
        self.assert_parse_correct(u'korucunun',        u'koru(koru)+Noun+A3Sg+Pnon+Nom+Noun+Agt(cI[cu])+A3Sg+Pnon+Gen(+nIn[nun])')
        self.assert_parse_correct(u'korucuyla',        u'koru(koru)+Noun+A3Sg+Pnon+Nom+Noun+Agt(cI[cu])+A3Sg+Pnon+Inst(+ylA[yla])')

    def test_should_parse_noun_to_verb_derivations(self):
        #heyecanlan
        pass


    def test_should_parse_positive_verb_tenses(self):
        self.assert_parse_correct(u'yaparım',           u'yap(yapmak)+Verb+Pos+Aor(+Ar[ar])+A1Sg(+Im[ım])')
        self.assert_parse_correct(u'yaparsın',          u'yap(yapmak)+Verb+Pos+Aor(+Ar[ar])+A2Sg(sIn[sın])')
        self.assert_parse_correct(u'yapar',             u'yap(yapmak)+Verb+Pos+Aor(+Ar[ar])+A3Sg')

        self.assert_parse_correct(u'yapıyorum',         u'yap(yapmak)+Verb+Pos+Prog(Iyor[ıyor])+A1Sg(+Im[um])')
        self.assert_parse_correct(u'yapıyorsun',        u'yap(yapmak)+Verb+Pos+Prog(Iyor[ıyor])+A2Sg(sIn[sun])')
        self.assert_parse_correct(u'yapıyor',           u'yap(yapmak)+Verb+Pos+Prog(Iyor[ıyor])+A3Sg')

        self.assert_parse_correct(u'yapmaktayım',       u'yap(yapmak)+Verb+Pos+Prog(mAktA[makta])+A1Sg(yIm[yım])')
        self.assert_parse_correct(u'yapmaktasın',       u'yap(yapmak)+Verb+Pos+Prog(mAktA[makta])+A2Sg(sIn[sın])')
        self.assert_parse_correct(u'yapmakta',          u'yap(yapmak)+Verb+Pos+Prog(mAktA[makta])+A3Sg')

        self.assert_parse_correct(u'yapacağım',         u'yap(yapmak)+Verb+Pos+Fut(+yAcAk[acağ])+A1Sg(+Im[ım])')
        self.assert_parse_correct(u'yapacaksın',        u'yap(yapmak)+Verb+Pos+Fut(+yAcAk[acak])+A2Sg(sIn[sın])')
        self.assert_parse_correct(u'yapacak',           u'yap(yapmak)+Verb+Pos+Fut(+yAcAk[acak])+A3Sg')

        self.assert_parse_correct(u'yaptım',            u'yap(yapmak)+Verb+Pos+Past(dI[tı])+A1Sg(+Im[m])')
        self.assert_parse_correct(u'yaptın',            u'yap(yapmak)+Verb+Pos+Past(dI[tı])+A2Sg(n[n])')
        self.assert_parse_correct(u'yaptı',             u'yap(yapmak)+Verb+Pos+Past(dI[tı])+A3Sg')

        self.assert_parse_correct(u'yapmışım',          u'yap(yapmak)+Verb+Pos+Evid(mIş[mış])+A1Sg(+Im[ım])')
        self.assert_parse_correct(u'yapmışsın',         u'yap(yapmak)+Verb+Pos+Evid(mIş[mış])+A2Sg(sIn[sın])')
        self.assert_parse_correct(u'yapmış',            u'yap(yapmak)+Verb+Pos+Evid(mIş[mış])+A3Sg')


        self.assert_parse_correct(u'çeviririm',         u'çevir(çevirmek)+Verb+Pos+Aor(+Ir[ir])+A1Sg(+Im[im])')
        self.assert_parse_correct(u'çevirirsin',        u'çevir(çevirmek)+Verb+Pos+Aor(+Ir[ir])+A2Sg(sIn[sin])')
        self.assert_parse_correct(u'çevirir',           u'çevir(çevirmek)+Verb+Pos+Aor(+Ir[ir])+A3Sg')

        self.assert_parse_correct(u'çeviriyorum',       u'çevir(çevirmek)+Verb+Pos+Prog(Iyor[iyor])+A1Sg(+Im[um])')
        self.assert_parse_correct(u'çeviriyorsun',      u'çevir(çevirmek)+Verb+Pos+Prog(Iyor[iyor])+A2Sg(sIn[sun])')
        self.assert_parse_correct(u'çeviriyor',         u'çevir(çevirmek)+Verb+Pos+Prog(Iyor[iyor])+A3Sg')

        self.assert_parse_correct(u'çevirmekteyim',     u'çevir(çevirmek)+Verb+Pos+Prog(mAktA[mekte])+A1Sg(yIm[yim])')
        self.assert_parse_correct(u'çevirmektesin',     u'çevir(çevirmek)+Verb+Pos+Prog(mAktA[mekte])+A2Sg(sIn[sin])')
        self.assert_parse_correct(u'çevirmekte',        u'çevir(çevirmek)+Verb+Pos+Prog(mAktA[mekte])+A3Sg')

        self.assert_parse_correct(u'çevireceğim',       u'çevir(çevirmek)+Verb+Pos+Fut(+yAcAk[eceğ])+A1Sg(+Im[im])')
        self.assert_parse_correct(u'çevireceksin',      u'çevir(çevirmek)+Verb+Pos+Fut(+yAcAk[ecek])+A2Sg(sIn[sin])')
        self.assert_parse_correct(u'çevirecek',         u'çevir(çevirmek)+Verb+Pos+Fut(+yAcAk[ecek])+A3Sg')

        self.assert_parse_correct(u'çevirdim',          u'çevir(çevirmek)+Verb+Pos+Past(dI[di])+A1Sg(+Im[m])')
        self.assert_parse_correct(u'çevirdin',          u'çevir(çevirmek)+Verb+Pos+Past(dI[di])+A2Sg(n[n])')
        self.assert_parse_correct(u'çevirdi',           u'çevir(çevirmek)+Verb+Pos+Past(dI[di])+A3Sg')

        self.assert_parse_correct(u'çevirmişim',        u'çevir(çevirmek)+Verb+Pos+Evid(mIş[miş])+A1Sg(+Im[im])')
        self.assert_parse_correct(u'çevirmişsin',       u'çevir(çevirmek)+Verb+Pos+Evid(mIş[miş])+A2Sg(sIn[sin])')
        self.assert_parse_correct(u'çevirmiş',          u'çevir(çevirmek)+Verb+Pos+Evid(mIş[miş])+A3Sg')


        self.assert_parse_correct(u'elerim',            u'ele(elemek)+Verb+Pos+Aor(+Ir[r])+A1Sg(+Im[im])', u'ele(elemek)+Verb+Pos+Aor(+Ar[r])+A1Sg(+Im[im])')
        self.assert_parse_correct(u'elersin',           u'ele(elemek)+Verb+Pos+Aor(+Ir[r])+A2Sg(sIn[sin])', u'ele(elemek)+Verb+Pos+Aor(+Ar[r])+A2Sg(sIn[sin])')
        self.assert_parse_correct(u'eler',              u'ele(elemek)+Verb+Pos+Aor(+Ir[r])+A3Sg', u'ele(elemek)+Verb+Pos+Aor(+Ar[r])+A3Sg')

        self.assert_parse_correct(u'eliyorum',          u'el(elemek)+Verb+Pos+Prog(Iyor[iyor])+A1Sg(+Im[um])')
        self.assert_parse_correct(u'eliyorsun',         u'el(elemek)+Verb+Pos+Prog(Iyor[iyor])+A2Sg(sIn[sun])')
        self.assert_parse_correct(u'eliyor',            u'el(elemek)+Verb+Pos+Prog(Iyor[iyor])+A3Sg')

        self.assert_parse_correct(u'elemekteyim',       u'ele(elemek)+Verb+Pos+Prog(mAktA[mekte])+A1Sg(yIm[yim])')
        self.assert_parse_correct(u'elemektesin',       u'ele(elemek)+Verb+Pos+Prog(mAktA[mekte])+A2Sg(sIn[sin])')
        self.assert_parse_correct(u'elemekte',          u'ele(elemek)+Verb+Pos+Prog(mAktA[mekte])+A3Sg')

        self.assert_parse_correct(u'eleyeceğim',        u'ele(elemek)+Verb+Pos+Fut(+yAcAk[yeceğ])+A1Sg(+Im[im])')
        self.assert_parse_correct(u'eleyeceksin',       u'ele(elemek)+Verb+Pos+Fut(+yAcAk[yecek])+A2Sg(sIn[sin])')
        self.assert_parse_correct(u'eleyecek',          u'ele(elemek)+Verb+Pos+Fut(+yAcAk[yecek])+A3Sg')

        self.assert_parse_correct(u'eledim',            u'ele(elemek)+Verb+Pos+Past(dI[di])+A1Sg(+Im[m])')
        self.assert_parse_correct(u'eledin',            u'ele(elemek)+Verb+Pos+Past(dI[di])+A2Sg(n[n])')
        self.assert_parse_correct(u'eledi',             u'ele(elemek)+Verb+Pos+Past(dI[di])+A3Sg')

        self.assert_parse_correct(u'elemişim',          u'ele(elemek)+Verb+Pos+Evid(mIş[miş])+A1Sg(+Im[im])')
        self.assert_parse_correct(u'elemişsin',         u'ele(elemek)+Verb+Pos+Evid(mIş[miş])+A2Sg(sIn[sin])')
        self.assert_parse_correct(u'elemiş',            u'ele(elemek)+Verb+Pos+Evid(mIş[miş])+A3Sg')

    def test_should_parse_negative_verb_tenses(self):
        self.assert_parse_correct(u'yapmam',             u'yap(yapmak)+Verb+Neg(mA[ma])+Aor+A1Sg(+Im[m])')
        self.assert_parse_correct(u'yapmazsın',          u'yap(yapmak)+Verb+Neg(mA[ma])+Aor(z[z])+A2Sg(sIn[sın])')
        self.assert_parse_correct(u'yapmaz',             u'yap(yapmak)+Verb+Neg(mA[ma])+Aor(z[z])+A3Sg')

        self.assert_parse_correct(u'yapmıyorum',         u'yap(yapmak)+Verb+Neg(m[m])+Prog(Iyor[ıyor])+A1Sg(+Im[um])')
        self.assert_parse_correct(u'yapmıyorsun',        u'yap(yapmak)+Verb+Neg(m[m])+Prog(Iyor[ıyor])+A2Sg(sIn[sun])')
        self.assert_parse_correct(u'yapmıyor',           u'yap(yapmak)+Verb+Neg(m[m])+Prog(Iyor[ıyor])+A3Sg')

        self.assert_parse_correct(u'yapmamaktayım',      u'yap(yapmak)+Verb+Neg(mA[ma])+Prog(mAktA[makta])+A1Sg(yIm[yım])')
        self.assert_parse_correct(u'yapmamaktasın',      u'yap(yapmak)+Verb+Neg(mA[ma])+Prog(mAktA[makta])+A2Sg(sIn[sın])')
        self.assert_parse_correct(u'yapmamakta',         u'yap(yapmak)+Verb+Neg(mA[ma])+Prog(mAktA[makta])+A3Sg')

        self.assert_parse_correct(u'yapmayacağım',       u'yap(yapmak)+Verb+Neg(mA[ma])+Fut(+yAcAk[yacağ])+A1Sg(+Im[ım])')
        self.assert_parse_correct(u'yapmayacaksın',      u'yap(yapmak)+Verb+Neg(mA[ma])+Fut(+yAcAk[yacak])+A2Sg(sIn[sın])')
        self.assert_parse_correct(u'yapmayacak',         u'yap(yapmak)+Verb+Neg(mA[ma])+Fut(+yAcAk[yacak])+A3Sg')

        self.assert_parse_correct(u'yapmadım',           u'yap(yapmak)+Verb+Neg(mA[ma])+Past(dI[dı])+A1Sg(+Im[m])')
        self.assert_parse_correct(u'yapmadın',           u'yap(yapmak)+Verb+Neg(mA[ma])+Past(dI[dı])+A2Sg(n[n])')
        self.assert_parse_correct(u'yapmadı',            u'yap(yapmak)+Verb+Neg(mA[ma])+Past(dI[dı])+A3Sg')

        self.assert_parse_correct(u'yapmamışım',         u'yap(yapmak)+Verb+Neg(mA[ma])+Evid(mIş[mış])+A1Sg(+Im[ım])')
        self.assert_parse_correct(u'yapmamışsın',        u'yap(yapmak)+Verb+Neg(mA[ma])+Evid(mIş[mış])+A2Sg(sIn[sın])')
        self.assert_parse_correct(u'yapmamış',           u'yap(yapmak)+Verb+Neg(mA[ma])+Evid(mIş[mış])+A3Sg')


        self.assert_parse_correct(u'çevirmem',           u'çevir(çevirmek)+Verb+Neg(mA[me])+Aor+A1Sg(+Im[m])')
        self.assert_parse_correct(u'çevirmezsin',        u'çevir(çevirmek)+Verb+Neg(mA[me])+Aor(z[z])+A2Sg(sIn[sin])')
        self.assert_parse_correct(u'çevirmez',           u'çevir(çevirmek)+Verb+Neg(mA[me])+Aor(z[z])+A3Sg')

        self.assert_parse_correct(u'çevirmiyorum',       u'çevir(çevirmek)+Verb+Neg(m[m])+Prog(Iyor[iyor])+A1Sg(+Im[um])')
        self.assert_parse_correct(u'çevirmiyorsun',      u'çevir(çevirmek)+Verb+Neg(m[m])+Prog(Iyor[iyor])+A2Sg(sIn[sun])')
        self.assert_parse_correct(u'çevirmiyor',         u'çevir(çevirmek)+Verb+Neg(m[m])+Prog(Iyor[iyor])+A3Sg')

        self.assert_parse_correct(u'çevirmemekteyim',    u'çevir(çevirmek)+Verb+Neg(mA[me])+Prog(mAktA[mekte])+A1Sg(yIm[yim])')
        self.assert_parse_correct(u'çevirmemektesin',    u'çevir(çevirmek)+Verb+Neg(mA[me])+Prog(mAktA[mekte])+A2Sg(sIn[sin])')
        self.assert_parse_correct(u'çevirmemekte',       u'çevir(çevirmek)+Verb+Neg(mA[me])+Prog(mAktA[mekte])+A3Sg')

        self.assert_parse_correct(u'çevirmeyeceğim',     u'çevir(çevirmek)+Verb+Neg(mA[me])+Fut(+yAcAk[yeceğ])+A1Sg(+Im[im])')
        self.assert_parse_correct(u'çevirmeyeceksin',    u'çevir(çevirmek)+Verb+Neg(mA[me])+Fut(+yAcAk[yecek])+A2Sg(sIn[sin])')
        self.assert_parse_correct(u'çevirmeyecek',       u'çevir(çevirmek)+Verb+Neg(mA[me])+Fut(+yAcAk[yecek])+A3Sg')

        self.assert_parse_correct(u'çevirmedim',         u'çevir(çevirmek)+Verb+Neg(mA[me])+Past(dI[di])+A1Sg(+Im[m])')
        self.assert_parse_correct(u'çevirmedin',         u'çevir(çevirmek)+Verb+Neg(mA[me])+Past(dI[di])+A2Sg(n[n])')
        self.assert_parse_correct(u'çevirmedi',          u'çevir(çevirmek)+Verb+Neg(mA[me])+Past(dI[di])+A3Sg')

        self.assert_parse_correct(u'çevirmemişim',       u'çevir(çevirmek)+Verb+Neg(mA[me])+Evid(mIş[miş])+A1Sg(+Im[im])')
        self.assert_parse_correct(u'çevirmemişsin',      u'çevir(çevirmek)+Verb+Neg(mA[me])+Evid(mIş[miş])+A2Sg(sIn[sin])')
        self.assert_parse_correct(u'çevirmemiş',         u'çevir(çevirmek)+Verb+Neg(mA[me])+Evid(mIş[miş])+A3Sg')


        self.assert_parse_correct(u'elemem',             u'ele(elemek)+Verb+Neg(mA[me])+Aor+A1Sg(+Im[m])')
        self.assert_parse_correct(u'elemezsin',          u'ele(elemek)+Verb+Neg(mA[me])+Aor(z[z])+A2Sg(sIn[sin])')
        self.assert_parse_correct(u'elemez',             u'ele(elemek)+Verb+Neg(mA[me])+Aor(z[z])+A3Sg')

        self.assert_parse_correct(u'elemiyorum',         u'ele(elemek)+Verb+Neg(m[m])+Prog(Iyor[iyor])+A1Sg(+Im[um])')
        self.assert_parse_correct(u'elemiyorsun',        u'ele(elemek)+Verb+Neg(m[m])+Prog(Iyor[iyor])+A2Sg(sIn[sun])')
        self.assert_parse_correct(u'elemiyor',           u'ele(elemek)+Verb+Neg(m[m])+Prog(Iyor[iyor])+A3Sg')

        self.assert_parse_correct(u'elememekteyim',      u'ele(elemek)+Verb+Neg(mA[me])+Prog(mAktA[mekte])+A1Sg(yIm[yim])')
        self.assert_parse_correct(u'elememektesin',      u'ele(elemek)+Verb+Neg(mA[me])+Prog(mAktA[mekte])+A2Sg(sIn[sin])')
        self.assert_parse_correct(u'elememekte',         u'ele(elemek)+Verb+Neg(mA[me])+Prog(mAktA[mekte])+A3Sg')

        self.assert_parse_correct(u'elemeyeceğim',       u'ele(elemek)+Verb+Neg(mA[me])+Fut(+yAcAk[yeceğ])+A1Sg(+Im[im])')
        self.assert_parse_correct(u'elemeyeceksin',      u'ele(elemek)+Verb+Neg(mA[me])+Fut(+yAcAk[yecek])+A2Sg(sIn[sin])')
        self.assert_parse_correct(u'elemeyecek',         u'ele(elemek)+Verb+Neg(mA[me])+Fut(+yAcAk[yecek])+A3Sg')

        self.assert_parse_correct(u'elemedim',           u'ele(elemek)+Verb+Neg(mA[me])+Past(dI[di])+A1Sg(+Im[m])')
        self.assert_parse_correct(u'elemedin',           u'ele(elemek)+Verb+Neg(mA[me])+Past(dI[di])+A2Sg(n[n])')
        self.assert_parse_correct(u'elemedi',            u'ele(elemek)+Verb+Neg(mA[me])+Past(dI[di])+A3Sg')

        self.assert_parse_correct(u'elememişim',         u'ele(elemek)+Verb+Neg(mA[me])+Evid(mIş[miş])+A1Sg(+Im[im])')
        self.assert_parse_correct(u'elememişsin',        u'ele(elemek)+Verb+Neg(mA[me])+Evid(mIş[miş])+A2Sg(sIn[sin])')
        self.assert_parse_correct(u'elememiş',           u'ele(elemek)+Verb+Neg(mA[me])+Evid(mIş[miş])+A3Sg')

    def test_should_parse_positive_multiple_verb_tenses(self):
        self.assert_parse_correct(u'yapardım',          u'yap(yapmak)+Verb+Pos+Aor(+Ar[ar])+Past(dI[dı])+A1Sg(+Im[m])')
        self.assert_parse_correct(u'yapardın',          u'yap(yapmak)+Verb+Pos+Aor(+Ar[ar])+Past(dI[dı])+A2Sg(n[n])')
        self.assert_parse_correct(u'yapardı',           u'yap(yapmak)+Verb+Pos+Aor(+Ar[ar])+Past(dI[dı])+A3Sg')

        self.assert_parse_correct(u'yapıyordum',        u'yap(yapmak)+Verb+Pos+Prog(Iyor[ıyor])+Past(dI[du])+A1Sg(+Im[m])')
        self.assert_parse_correct(u'yapıyordun',        u'yap(yapmak)+Verb+Pos+Prog(Iyor[ıyor])+Past(dI[du])+A2Sg(n[n])')
        self.assert_parse_correct(u'yapıyordu',         u'yap(yapmak)+Verb+Pos+Prog(Iyor[ıyor])+Past(dI[du])+A3Sg')

        self.assert_parse_correct(u'yapmaktaydım',      u'yap(yapmak)+Verb+Pos+Prog(mAktA[makta])+Past(ydI[ydı])+A1Sg(+Im[m])')
        self.assert_parse_correct(u'yapmaktaydın',      u'yap(yapmak)+Verb+Pos+Prog(mAktA[makta])+Past(ydI[ydı])+A2Sg(n[n])')
        self.assert_parse_correct(u'yapmaktaydı',       u'yap(yapmak)+Verb+Pos+Prog(mAktA[makta])+Past(ydI[ydı])+A3Sg')

        self.assert_parse_correct(u'yapacaktım',        u'yap(yapmak)+Verb+Pos+Fut(+yAcAk[acak])+Past(dI[tı])+A1Sg(+Im[m])')
        self.assert_parse_correct(u'yapacaktın',        u'yap(yapmak)+Verb+Pos+Fut(+yAcAk[acak])+Past(dI[tı])+A2Sg(n[n])')
        self.assert_parse_correct(u'yapacaktı',         u'yap(yapmak)+Verb+Pos+Fut(+yAcAk[acak])+Past(dI[tı])+A3Sg')

#        well, the following is not valid
#        self.assert_parse_correct(u'yaptıydım',         u'yap(yapmak)+Verb+Pos+Past(dI[tı])+Past(ydI[ydı])+A1Sg(+Im[m])')
#        self.assert_parse_correct(u'yaptıydın',         u'yap(yapmak)+Verb+Pos+Past(dI[tı])+Past(ydI[ydı])+A2Sg(n[n])')
#        self.assert_parse_correct(u'yaptıydı',          u'yap(yapmak)+Verb+Pos+Past(dI[tı])+Past(ydI[ydı])+A3Sg')

        self.assert_parse_correct(u'yapmıştım',         u'yap(yapmak)+Verb+Pos+Evid(mIş[mış])+Past(dI[tı])+A1Sg(+Im[m])')
        self.assert_parse_correct(u'yapmıştın',         u'yap(yapmak)+Verb+Pos+Evid(mIş[mış])+Past(dI[tı])+A2Sg(n[n])')
        self.assert_parse_correct(u'yapmıştı',          u'yap(yapmak)+Verb+Pos+Evid(mIş[mış])+Past(dI[tı])+A3Sg')


        self.assert_parse_correct(u'yaparmışım',        u'yap(yapmak)+Verb+Pos+Aor(+Ar[ar])+Evid(mIş[mış])+A1Sg(+Im[ım])')
        self.assert_parse_correct(u'yaparmışsın',       u'yap(yapmak)+Verb+Pos+Aor(+Ar[ar])+Evid(mIş[mış])+A2Sg(sIn[sın])')
        self.assert_parse_correct(u'yaparmış',          u'yap(yapmak)+Verb+Pos+Aor(+Ar[ar])+Evid(mIş[mış])+A3Sg')

        self.assert_parse_correct(u'yapıyormuşum',      u'yap(yapmak)+Verb+Pos+Prog(Iyor[ıyor])+Evid(mIş[muş])+A1Sg(+Im[um])')
        self.assert_parse_correct(u'yapıyormuşsun',     u'yap(yapmak)+Verb+Pos+Prog(Iyor[ıyor])+Evid(mIş[muş])+A2Sg(sIn[sun])')
        self.assert_parse_correct(u'yapıyormuş',        u'yap(yapmak)+Verb+Pos+Prog(Iyor[ıyor])+Evid(mIş[muş])+A3Sg')

        self.assert_parse_correct(u'yapmaktaymışım',    u'yap(yapmak)+Verb+Pos+Prog(mAktA[makta])+Evid(ymIş[ymış])+A1Sg(+Im[ım])')
        self.assert_parse_correct(u'yapmaktaymışsın',   u'yap(yapmak)+Verb+Pos+Prog(mAktA[makta])+Evid(ymIş[ymış])+A2Sg(sIn[sın])')
        self.assert_parse_correct(u'yapmaktaymış',      u'yap(yapmak)+Verb+Pos+Prog(mAktA[makta])+Evid(ymIş[ymış])+A3Sg')

        self.assert_parse_correct(u'yapacakmışım',      u'yap(yapmak)+Verb+Pos+Fut(+yAcAk[acak])+Evid(mIş[mış])+A1Sg(+Im[ım])')
        self.assert_parse_correct(u'yapacakmışsın',     u'yap(yapmak)+Verb+Pos+Fut(+yAcAk[acak])+Evid(mIş[mış])+A2Sg(sIn[sın])')
        self.assert_parse_correct(u'yapacakmış',        u'yap(yapmak)+Verb+Pos+Fut(+yAcAk[acak])+Evid(mIş[mış])+A3Sg')


        self.assert_parse_correct(u'elerdim',           u'ele(elemek)+Verb+Pos+Aor(+Ir[r])+Past(dI[di])+A1Sg(+Im[m])', u'ele(elemek)+Verb+Pos+Aor(+Ar[r])+Past(dI[di])+A1Sg(+Im[m])')
        self.assert_parse_correct(u'elerdin',           u'ele(elemek)+Verb+Pos+Aor(+Ir[r])+Past(dI[di])+A2Sg(n[n])', u'ele(elemek)+Verb+Pos+Aor(+Ar[r])+Past(dI[di])+A2Sg(n[n])')
        self.assert_parse_correct(u'elerdi',            u'ele(elemek)+Verb+Pos+Aor(+Ir[r])+Past(dI[di])+A3Sg', u'ele(elemek)+Verb+Pos+Aor(+Ar[r])+Past(dI[di])+A3Sg')

        self.assert_parse_correct(u'eliyordum',         u'el(elemek)+Verb+Pos+Prog(Iyor[iyor])+Past(dI[du])+A1Sg(+Im[m])')
        self.assert_parse_correct(u'eliyordun',         u'el(elemek)+Verb+Pos+Prog(Iyor[iyor])+Past(dI[du])+A2Sg(n[n])')
        self.assert_parse_correct(u'eliyordu',          u'el(elemek)+Verb+Pos+Prog(Iyor[iyor])+Past(dI[du])+A3Sg')

        self.assert_parse_correct(u'elemekteydim',      u'ele(elemek)+Verb+Pos+Prog(mAktA[mekte])+Past(ydI[ydi])+A1Sg(+Im[m])')
        self.assert_parse_correct(u'elemekteydin',      u'ele(elemek)+Verb+Pos+Prog(mAktA[mekte])+Past(ydI[ydi])+A2Sg(n[n])')
        self.assert_parse_correct(u'elemekteydi',       u'ele(elemek)+Verb+Pos+Prog(mAktA[mekte])+Past(ydI[ydi])+A3Sg')

        self.assert_parse_correct(u'eleyecektim',       u'ele(elemek)+Verb+Pos+Fut(+yAcAk[yecek])+Past(dI[ti])+A1Sg(+Im[m])')
        self.assert_parse_correct(u'eleyecektin',       u'ele(elemek)+Verb+Pos+Fut(+yAcAk[yecek])+Past(dI[ti])+A2Sg(n[n])')
        self.assert_parse_correct(u'eleyecekti',        u'ele(elemek)+Verb+Pos+Fut(+yAcAk[yecek])+Past(dI[ti])+A3Sg')

        self.assert_parse_correct(u'elemiştim',         u'ele(elemek)+Verb+Pos+Evid(mIş[miş])+Past(dI[ti])+A1Sg(+Im[m])')
        self.assert_parse_correct(u'elemiştin',         u'ele(elemek)+Verb+Pos+Evid(mIş[miş])+Past(dI[ti])+A2Sg(n[n])')
        self.assert_parse_correct(u'elemişti',          u'ele(elemek)+Verb+Pos+Evid(mIş[miş])+Past(dI[ti])+A3Sg')


        self.assert_parse_correct(u'elermişim',         u'ele(elemek)+Verb+Pos+Aor(+Ir[r])+Evid(mIş[miş])+A1Sg(+Im[im])', u'ele(elemek)+Verb+Pos+Aor(+Ar[r])+Evid(mIş[miş])+A1Sg(+Im[im])')
        self.assert_parse_correct(u'elermişsin',        u'ele(elemek)+Verb+Pos+Aor(+Ir[r])+Evid(mIş[miş])+A2Sg(sIn[sin])', u'ele(elemek)+Verb+Pos+Aor(+Ar[r])+Evid(mIş[miş])+A2Sg(sIn[sin])')
        self.assert_parse_correct(u'elermiş',           u'ele(elemek)+Verb+Pos+Aor(+Ir[r])+Evid(mIş[miş])+A3Sg', u'ele(elemek)+Verb+Pos+Aor(+Ar[r])+Evid(mIş[miş])+A3Sg')

        self.assert_parse_correct(u'eliyormuşum',       u'el(elemek)+Verb+Pos+Prog(Iyor[iyor])+Evid(mIş[muş])+A1Sg(+Im[um])')
        self.assert_parse_correct(u'eliyormuşsun',      u'el(elemek)+Verb+Pos+Prog(Iyor[iyor])+Evid(mIş[muş])+A2Sg(sIn[sun])')
        self.assert_parse_correct(u'eliyormuş',         u'el(elemek)+Verb+Pos+Prog(Iyor[iyor])+Evid(mIş[muş])+A3Sg')

        self.assert_parse_correct(u'elemekteymişim',    u'ele(elemek)+Verb+Pos+Prog(mAktA[mekte])+Evid(ymIş[ymiş])+A1Sg(+Im[im])')
        self.assert_parse_correct(u'elemekteymişsin',   u'ele(elemek)+Verb+Pos+Prog(mAktA[mekte])+Evid(ymIş[ymiş])+A2Sg(sIn[sin])')
        self.assert_parse_correct(u'elemekteymiş',      u'ele(elemek)+Verb+Pos+Prog(mAktA[mekte])+Evid(ymIş[ymiş])+A3Sg')

        self.assert_parse_correct(u'eleyecekmişim',     u'ele(elemek)+Verb+Pos+Fut(+yAcAk[yecek])+Evid(mIş[miş])+A1Sg(+Im[im])')
        self.assert_parse_correct(u'eleyecekmişsin',    u'ele(elemek)+Verb+Pos+Fut(+yAcAk[yecek])+Evid(mIş[miş])+A2Sg(sIn[sin])')
        self.assert_parse_correct(u'eleyecekmiş',       u'ele(elemek)+Verb+Pos+Fut(+yAcAk[yecek])+Evid(mIş[miş])+A3Sg')

    def test_should_parse_negative_multiple_verb_tenses(self):
        self.assert_parse_correct(u'yapmazdım',         u'yap(yapmak)+Verb+Neg(mA[ma])+Aor(z[z])+Past(dI[dı])+A1Sg(+Im[m])')
        self.assert_parse_correct(u'yapmazdın',         u'yap(yapmak)+Verb+Neg(mA[ma])+Aor(z[z])+Past(dI[dı])+A2Sg(n[n])')
        self.assert_parse_correct(u'yapmazdı',          u'yap(yapmak)+Verb+Neg(mA[ma])+Aor(z[z])+Past(dI[dı])+A3Sg')

        self.assert_parse_correct(u'yapmıyordum',       u'yap(yapmak)+Verb+Neg(m[m])+Prog(Iyor[ıyor])+Past(dI[du])+A1Sg(+Im[m])')
        self.assert_parse_correct(u'yapmıyordun',       u'yap(yapmak)+Verb+Neg(m[m])+Prog(Iyor[ıyor])+Past(dI[du])+A2Sg(n[n])')
        self.assert_parse_correct(u'yapmıyordu',        u'yap(yapmak)+Verb+Neg(m[m])+Prog(Iyor[ıyor])+Past(dI[du])+A3Sg')

        self.assert_parse_correct(u'yapmamaktaydım',    u'yap(yapmak)+Verb+Neg(mA[ma])+Prog(mAktA[makta])+Past(ydI[ydı])+A1Sg(+Im[m])')
        self.assert_parse_correct(u'yapmamaktaydın',    u'yap(yapmak)+Verb+Neg(mA[ma])+Prog(mAktA[makta])+Past(ydI[ydı])+A2Sg(n[n])')
        self.assert_parse_correct(u'yapmamaktaydı',     u'yap(yapmak)+Verb+Neg(mA[ma])+Prog(mAktA[makta])+Past(ydI[ydı])+A3Sg')

        self.assert_parse_correct(u'yapmayacaktım',     u'yap(yapmak)+Verb+Neg(mA[ma])+Fut(+yAcAk[yacak])+Past(dI[tı])+A1Sg(+Im[m])')
        self.assert_parse_correct(u'yapmayacaktın',     u'yap(yapmak)+Verb+Neg(mA[ma])+Fut(+yAcAk[yacak])+Past(dI[tı])+A2Sg(n[n])')
        self.assert_parse_correct(u'yapmayacaktı',      u'yap(yapmak)+Verb+Neg(mA[ma])+Fut(+yAcAk[yacak])+Past(dI[tı])+A3Sg')

        self.assert_parse_correct(u'yapmamıştım',       u'yap(yapmak)+Verb+Neg(mA[ma])+Evid(mIş[mış])+Past(dI[tı])+A1Sg(+Im[m])')
        self.assert_parse_correct(u'yapmamıştın',       u'yap(yapmak)+Verb+Neg(mA[ma])+Evid(mIş[mış])+Past(dI[tı])+A2Sg(n[n])')
        self.assert_parse_correct(u'yapmamıştı',        u'yap(yapmak)+Verb+Neg(mA[ma])+Evid(mIş[mış])+Past(dI[tı])+A3Sg')


        self.assert_parse_correct(u'yapmazmışım',       u'yap(yapmak)+Verb+Neg(mA[ma])+Aor(z[z])+Evid(mIş[mış])+A1Sg(+Im[ım])')
        self.assert_parse_correct(u'yapmazmışsın',      u'yap(yapmak)+Verb+Neg(mA[ma])+Aor(z[z])+Evid(mIş[mış])+A2Sg(sIn[sın])')
        self.assert_parse_correct(u'yapmazmış',         u'yap(yapmak)+Verb+Neg(mA[ma])+Aor(z[z])+Evid(mIş[mış])+A3Sg')

        self.assert_parse_correct(u'yapmıyormuşum',     u'yap(yapmak)+Verb+Neg(m[m])+Prog(Iyor[ıyor])+Evid(mIş[muş])+A1Sg(+Im[um])')
        self.assert_parse_correct(u'yapmıyormuşsun',    u'yap(yapmak)+Verb+Neg(m[m])+Prog(Iyor[ıyor])+Evid(mIş[muş])+A2Sg(sIn[sun])')
        self.assert_parse_correct(u'yapmıyormuş',       u'yap(yapmak)+Verb+Neg(m[m])+Prog(Iyor[ıyor])+Evid(mIş[muş])+A3Sg')

        self.assert_parse_correct(u'yapmamaktaymışım',  u'yap(yapmak)+Verb+Neg(mA[ma])+Prog(mAktA[makta])+Evid(ymIş[ymış])+A1Sg(+Im[ım])')
        self.assert_parse_correct(u'yapmamaktaymışsın', u'yap(yapmak)+Verb+Neg(mA[ma])+Prog(mAktA[makta])+Evid(ymIş[ymış])+A2Sg(sIn[sın])')
        self.assert_parse_correct(u'yapmamaktaymış',    u'yap(yapmak)+Verb+Neg(mA[ma])+Prog(mAktA[makta])+Evid(ymIş[ymış])+A3Sg')

        self.assert_parse_correct(u'yapmayacakmışım',   u'yap(yapmak)+Verb+Neg(mA[ma])+Fut(+yAcAk[yacak])+Evid(mIş[mış])+A1Sg(+Im[ım])')
        self.assert_parse_correct(u'yapmayacakmışsın',  u'yap(yapmak)+Verb+Neg(mA[ma])+Fut(+yAcAk[yacak])+Evid(mIş[mış])+A2Sg(sIn[sın])')
        self.assert_parse_correct(u'yapmayacakmış',     u'yap(yapmak)+Verb+Neg(mA[ma])+Fut(+yAcAk[yacak])+Evid(mIş[mış])+A3Sg')


        self.assert_parse_correct(u'elemezdim',         u'ele(elemek)+Verb+Neg(mA[me])+Aor(z[z])+Past(dI[di])+A1Sg(+Im[m])')
        self.assert_parse_correct(u'elemezdin',         u'ele(elemek)+Verb+Neg(mA[me])+Aor(z[z])+Past(dI[di])+A2Sg(n[n])')
        self.assert_parse_correct(u'elemezdi',          u'ele(elemek)+Verb+Neg(mA[me])+Aor(z[z])+Past(dI[di])+A3Sg')

        self.assert_parse_correct(u'elemiyordum',       u'ele(elemek)+Verb+Neg(m[m])+Prog(Iyor[iyor])+Past(dI[du])+A1Sg(+Im[m])')
        self.assert_parse_correct(u'elemiyordun',       u'ele(elemek)+Verb+Neg(m[m])+Prog(Iyor[iyor])+Past(dI[du])+A2Sg(n[n])')
        self.assert_parse_correct(u'elemiyordu',        u'ele(elemek)+Verb+Neg(m[m])+Prog(Iyor[iyor])+Past(dI[du])+A3Sg')

        self.assert_parse_correct(u'elememekteydim',    u'ele(elemek)+Verb+Neg(mA[me])+Prog(mAktA[mekte])+Past(ydI[ydi])+A1Sg(+Im[m])')
        self.assert_parse_correct(u'elememekteydin',    u'ele(elemek)+Verb+Neg(mA[me])+Prog(mAktA[mekte])+Past(ydI[ydi])+A2Sg(n[n])')
        self.assert_parse_correct(u'elememekteydi',     u'ele(elemek)+Verb+Neg(mA[me])+Prog(mAktA[mekte])+Past(ydI[ydi])+A3Sg')

        self.assert_parse_correct(u'elemeyecektim',     u'ele(elemek)+Verb+Neg(mA[me])+Fut(+yAcAk[yecek])+Past(dI[ti])+A1Sg(+Im[m])')
        self.assert_parse_correct(u'elemeyecektin',     u'ele(elemek)+Verb+Neg(mA[me])+Fut(+yAcAk[yecek])+Past(dI[ti])+A2Sg(n[n])')
        self.assert_parse_correct(u'elemeyecekti',      u'ele(elemek)+Verb+Neg(mA[me])+Fut(+yAcAk[yecek])+Past(dI[ti])+A3Sg')

        self.assert_parse_correct(u'elememiştim',       u'ele(elemek)+Verb+Neg(mA[me])+Evid(mIş[miş])+Past(dI[ti])+A1Sg(+Im[m])')
        self.assert_parse_correct(u'elememiştin',       u'ele(elemek)+Verb+Neg(mA[me])+Evid(mIş[miş])+Past(dI[ti])+A2Sg(n[n])')
        self.assert_parse_correct(u'elememişti',        u'ele(elemek)+Verb+Neg(mA[me])+Evid(mIş[miş])+Past(dI[ti])+A3Sg')


        self.assert_parse_correct(u'elemezmişim',       u'ele(elemek)+Verb+Neg(mA[me])+Aor(z[z])+Evid(mIş[miş])+A1Sg(+Im[im])')
        self.assert_parse_correct(u'elemezmişsin',      u'ele(elemek)+Verb+Neg(mA[me])+Aor(z[z])+Evid(mIş[miş])+A2Sg(sIn[sin])')
        self.assert_parse_correct(u'elemezmiş',         u'ele(elemek)+Verb+Neg(mA[me])+Aor(z[z])+Evid(mIş[miş])+A3Sg')

        self.assert_parse_correct(u'elemiyormuşum',     u'ele(elemek)+Verb+Neg(m[m])+Prog(Iyor[iyor])+Evid(mIş[muş])+A1Sg(+Im[um])')
        self.assert_parse_correct(u'elemiyormuşsun',    u'ele(elemek)+Verb+Neg(m[m])+Prog(Iyor[iyor])+Evid(mIş[muş])+A2Sg(sIn[sun])')
        self.assert_parse_correct(u'elemiyormuş',       u'ele(elemek)+Verb+Neg(m[m])+Prog(Iyor[iyor])+Evid(mIş[muş])+A3Sg')

        self.assert_parse_correct(u'elememekteymişim',  u'ele(elemek)+Verb+Neg(mA[me])+Prog(mAktA[mekte])+Evid(ymIş[ymiş])+A1Sg(+Im[im])')
        self.assert_parse_correct(u'elememekteymişsin', u'ele(elemek)+Verb+Neg(mA[me])+Prog(mAktA[mekte])+Evid(ymIş[ymiş])+A2Sg(sIn[sin])')
        self.assert_parse_correct(u'elememekteymiş',    u'ele(elemek)+Verb+Neg(mA[me])+Prog(mAktA[mekte])+Evid(ymIş[ymiş])+A3Sg')

        self.assert_parse_correct(u'elemeyecekmişim',   u'ele(elemek)+Verb+Neg(mA[me])+Fut(+yAcAk[yecek])+Evid(mIş[miş])+A1Sg(+Im[im])')
        self.assert_parse_correct(u'elemeyecekmişsin',  u'ele(elemek)+Verb+Neg(mA[me])+Fut(+yAcAk[yecek])+Evid(mIş[miş])+A2Sg(sIn[sin])')
        self.assert_parse_correct(u'elemeyecekmiş',     u'ele(elemek)+Verb+Neg(mA[me])+Fut(+yAcAk[yecek])+Evid(mIş[miş])+A3Sg')

    def test_should_parse_some_verbs(self):
        self.assert_parse_correct(u'yapardık',          u'yap(yapmak)+Verb+Pos+Aor(+Ar[ar])+Past(dI[dı])+A1Pl(k[k])')
        self.assert_parse_correct(u'yapardınız',        u'yap(yapmak)+Verb+Pos+Aor(+Ar[ar])+Past(dI[dı])+A2Pl(nIz[nız])')
        self.assert_parse_correct(u'yapardılar',        u'yap(yapmak)+Verb+Pos+Aor(+Ar[ar])+Past(dI[dı])+A3Pl(lAr[lar])')
#        self.assert_parse_correct(u'yaparlardı',        u'yap(yapmak)+Verb+Pos+Aor(+Ar[ar])+Past(dI[dı])+A3Sg')    ##TODO

    def test_should_parse_modals(self):
        self.assert_parse_correct(u'eleyebilirim',      u'ele(elemek)+Verb+Pos+Abil(+yAbil[yebil])+Aor(+Ir[ir])+A1Sg(+Im[im])')
        self.assert_parse_correct(u'eleyemem',          u'ele(elemek)+Verb+Neg+Abil(+yAmA[yeme])+Aor+A1Sg(+Im[m])')
        self.assert_parse_correct(u'eleyemezsin',       u'ele(elemek)+Verb+Neg+Abil(+yAmA[yeme])+Aor(z[z])+A2Sg(sIn[sin])')
        self.assert_parse_correct(u'yapamazdım',        u'yap(yapmak)+Verb+Neg+Abil(+yAmA[ama])+Aor(z[z])+Past(dI[dı])+A1Sg(+Im[m])')
        self.assert_parse_correct(u'eleyemeyeceğim',    u'ele(elemek)+Verb+Neg+Abil(+yAmA[yeme])+Fut(+yAcAk[yeceğ])+A1Sg(+Im[im])')

        self.assert_parse_correct(u'yapabilirdim',      u'yap(yapmak)+Verb+Pos+Abil(+yAbil[abil])+Aor(+Ir[ir])+Past(dI[di])+A1Sg(+Im[m])')
        self.assert_parse_correct(u'yapabileceksin',    u'yap(yapmak)+Verb+Pos+Abil(+yAbil[abil])+Fut(+yAcAk[ecek])+A2Sg(sIn[sin])')

        self.assert_parse_correct(u'yapmalıyım',        u'yap(yapmak)+Verb+Pos+Necess(mAlI[malı])+A1Sg(yIm[yım])')
        self.assert_parse_correct(u'yapmalıydım',       u'yap(yapmak)+Verb+Pos+Necess(mAlI[malı])+Past(ydI[ydı])+A1Sg(+Im[m])')
        self.assert_parse_correct(u'yapmamalıyım',      u'yap(yapmak)+Verb+Neg(mA[ma])+Necess(mAlI[malı])+A1Sg(yIm[yım])')
        self.assert_parse_correct(u'yapmamalıydım',     u'yap(yapmak)+Verb+Neg(mA[ma])+Necess(mAlI[malı])+Past(ydI[ydı])+A1Sg(+Im[m])')

        self.assert_parse_correct(u'elemeliymiş',       u'ele(elemek)+Verb+Pos+Necess(mAlI[meli])+Evid(ymIş[ymiş])+A3Sg')
        self.assert_parse_correct(u'elememeliymiş',     u'ele(elemek)+Verb+Neg(mA[me])+Necess(mAlI[meli])+Evid(ymIş[ymiş])+A3Sg')

        self.assert_parse_correct(u'eleyesin',          u'ele(elemek)+Verb+Pos+Opt(yA[ye])+A2Sg(sIn[sin])')
        self.assert_parse_correct(u'elemeyeydim',       u'ele(elemek)+Verb+Neg(mA[me])+Opt(yAy[yey])+Past(dI[di])+A1Sg(+Im[m])', u'ele(elemek)+Verb+Neg(mA[me])+Opt(yA[ye])+Past(ydI[ydi])+A1Sg(+Im[m])')

        self.assert_parse_correct(u'eleyebilmeliydim',  u'ele(elemek)+Verb+Pos+Abil(+yAbil[yebil])+Necess(mAlI[meli])+Past(ydI[ydi])+A1Sg(+Im[m])')
        self.assert_parse_correct(u'eleyememeliydi',    u'ele(elemek)+Verb+Neg+Abil(+yAmA[yeme])+Necess(mAlI[meli])+Past(ydI[ydi])+A3Sg')

    def test_should_possessives(self):
        parser_logger.setLevel(logging.DEBUG)

        self.assert_parse_correct(u'kalemim',           u'kalem(kalem)+Noun+A3Sg+P1Sg(+Im[im])+Nom')
        self.assert_parse_correct(u'kalemimi',          u'kalem(kalem)+Noun+A3Sg+P1Sg(+Im[im])+Acc(+yI[i])')
        self.assert_parse_correct(u'kalemimden',        u'kalem(kalem)+Noun+A3Sg+P1Sg(+Im[im])+Abl(dAn[den])')
        self.assert_parse_correct(u'kalemimin',         u'kalem(kalem)+Noun+A3Sg+P1Sg(+Im[im])+Gen(+nIn[in])')

        self.assert_parse_correct(u'danam',             u'dana(dana)+Noun+A3Sg+P1Sg(+Im[m])+Nom')
        self.assert_parse_correct(u'danamı',            u'dana(dana)+Noun+A3Sg+P1Sg(+Im[m])+Acc(+yI[ı])')

        self.assert_parse_correct(u'kitabın',           u'kitab(kitap)+Noun+A3Sg+Pnon+Gen(+nIn[ın])', u'kitab(kitap)+Noun+A3Sg+P2Sg(+In[ın])+Nom')
        self.assert_parse_correct(u'kitabını',          u'kitab(kitap)+Noun+A3Sg+P2Sg(+In[ın])+Acc(+yI[ı])', u'kitab(kitap)+Noun+A3Sg+P3Sg(+sI[ı])+Acc(nI[nı])')

        self.assert_parse_correct(u'danası',            u'dana(dana)+Noun+A3Sg+P3Sg(+sI[sı])+Nom')
        self.assert_parse_correct(u'danasında',         u'dana(dana)+Noun+A3Sg+P3Sg(+sI[sı])+Loc(ndA[nda])')

        self.assert_parse_correct(u'danamız',           u'dana(dana)+Noun+A3Sg+P1Pl(+ImIz[mız])+Nom')
        self.assert_parse_correct(u'danamızdan',        u'dana(dana)+Noun+A3Sg+P1Pl(+ImIz[mız])+Abl(dAn[dan])')

        self.assert_parse_correct(u'sandalyeniz',       u'sandalye(sandalye)+Noun+A3Sg+P2Pl(+InIz[niz])+Nom')
        self.assert_parse_correct(u'sandalyelerinizden',u'sandalye(sandalye)+Noun+A3Pl(lAr[ler])+P2Pl(+InIz[iniz])+Abl(dAn[den])')

        self.assert_parse_correct(u'sandalyeleri',      u'sandalye(sandalye)+Noun+A3Pl(lAr[ler])+Pnon+Acc(+yI[i])', u'sandalye(sandalye)+Noun+A3Pl(lAr[ler])+P3Sg(+sI[i])+Nom', u'sandalye(sandalye)+Noun+A3Sg+P3Pl(lArI[leri])+Nom')   # TODO: 2nd and 3rd!
        self.assert_parse_correct(u'sandalyelerini',    u'sandalye(sandalye)+Noun+A3Pl(lAr[ler])+P2Sg(+In[in])+Acc(+yI[i])', u'sandalye(sandalye)+Noun+A3Pl(lAr[ler])+P3Sg(+sI[i])+Acc(nI[ni])', u'sandalye(sandalye)+Noun+A3Sg+P3Pl(lArI[leri])+Acc(nI[ni])')

    def assert_parse_correct(self, word_to_parse, *args):
        assert_that(self.parse_result(word_to_parse), IsParseResultMatches([a for a in args]))

    def parse_result(self, word):
        return [r.to_pretty_str() for r in (self.parser.parse(word))]

class IsParseResultMatches(BaseMatcher):
    def __init__(self, expected_results):
        self.expected_results = expected_results

    def _matches(self, item):
        return item==self.expected_results

    def describe_to(self, description):
        description.append_text(u'     ' + str(self.expected_results))

if __name__ == '__main__':
    unittest.main()
