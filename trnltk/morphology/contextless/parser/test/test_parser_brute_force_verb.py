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
from trnltk.morphology.contextless.parser.bruteforceverbrootfinder import BruteForceVerbRootFinder
from trnltk.morphology.contextless.parser.test.parser_test import ParserTest
from trnltk.morphology.contextless.parser.parser import ContextlessMorphologicalParser, logger as parser_logger
from trnltk.morphology.contextless.parser.suffixapplier import logger as suffix_applier_logger
from trnltk.morphology.morphotactics.basicsuffixgraph import BasicSuffixGraph

class ParserTestWithBruteForceVerbRootFinder(ParserTest):
    @classmethod
    def setUpClass(cls):
        super(ParserTestWithBruteForceVerbRootFinder, cls).setUpClass()

    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        parser_logger.setLevel(logging.INFO)
        suffix_applier_logger.setLevel(logging.INFO)

        suffix_graph = BasicSuffixGraph()
        suffix_graph.initialize()

        self.mock_brute_force_noun_root_finder = BruteForceVerbRootFinder()

        self.parser = ContextlessMorphologicalParser(suffix_graph, None, [self.mock_brute_force_noun_root_finder])

    def test_should_mark_unparsable(self):
        self.assert_not_parsable(u'd')
        self.assert_not_parsable(u'dp')
        self.assert_not_parsable(u'ayl')
        self.assert_not_parsable(u'anf')
        self.assert_not_parsable(u'azz')
        self.assert_not_parsable(u'ddr')
        self.assert_not_parsable(u'xxx')

    def test_should_find_one_result_for_words_not_acceptable_by_suffix_graph(self):
        self.assert_parse_correct(u'asdasmo',      u'asdasmo(asdasmomak)+Verb+Pos+Imp+A2sg')
        self.assert_parse_correct(u'balpaze',      u'balpaze(balpazemek)+Verb+Pos+Imp+A2sg')

    def test_should_parse_simple_verbs(self):
        self.assert_parse_correct(u'de',           u'de(demek)+Verb+Pos+Imp+A2sg')

        self.assert_parse_correct(u'git',          u'git(gitmek)+Verb+Pos+Imp+A2sg', u'gi(gimek)+Verb+Verb+Caus(t[t])+Pos+Imp+A2sg')

        self.assert_parse_correct(u'sok',          u'sok(sokmak)+Verb+Pos+Imp+A2sg')

        self.assert_parse_correct(u'deyip',
            u'deyip(deyipmek)+Verb+Pos+Imp+A2sg',
            u'de(demek)+Verb+Pos+Adv+AfterDoingSo(+yIp[yip])',
            u'dey(deymek)+Verb+Pos+Adv+AfterDoingSo(+yIp[ip])')

        self.assert_parse_correct(u'sokacak',
            u'sok(sokmak)+Verb+Pos+Fut(+yAcAk[acak])+A3sg',
            u'sok(sokmak)+Verb+Pos+Fut(+yAcAk[acak])+Adj+Zero',
            u'sok(sokmak)+Verb+Pos+Adj+FutPart(+yAcAk[acak])+Pnon',
            u'sok(sokmak)+Verb+Pos+Noun+FutPart(+yAcAk[acak])+A3sg+Pnon+Nom',
            u'sok(sokmak)+Verb+Pos+Fut(+yAcAk[acak])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom',
            u'sokacak(sokacakmak)+Verb+Pos+Imp+A2sg')

        self.assert_parse_correct(u'saldı',        u'sal(salmak)+Verb+Pos+Past(dI[dı])+A3sg', u'saldı(saldımak)+Verb+Pos+Imp+A2sg')

    def test_should_parse_verbs_with_progressive_vowel_drop(self):
        self.assert_parse_correct(u'başlıyor',
            u'başl(başlamak)+Verb+Pos+Prog(Iyor[ıyor])+A3sg',
            u'başl(başlımak)+Verb+Pos+Prog(Iyor[ıyor])+A3sg',
            u'başlıyo(başlıyomak)+Verb+Pos+Aor(+Ar[r])+A3sg',
            u'başlıyor(başlıyormak)+Verb+Pos+Imp+A2sg',
            u'başlıyo(başlıyomak)+Verb+Pos+Aor(+Ar[r])+Adj+Zero',
            u'başlıyo(başlıyomak)+Verb+Pos+Aor(+Ar[r])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')

        self.assert_parse_correct(u'elliyorduk',
            u'ell(ellemek)+Verb+Pos+Prog(Iyor[iyor])+Past(dI[du])+A1pl(k[k])',
            u'ell(ellimek)+Verb+Pos+Prog(Iyor[iyor])+Past(dI[du])+A1pl(k[k])',
            u'elliyor(elliyormak)+Verb+Pos+Past(dI[du])+A1pl(k[k])',
            u'elliyorduk(elliyordukmak)+Verb+Pos+Imp+A2sg',
            u'elliyo(elliyomak)+Verb+Pos+Aor(+Ar[r])+Past(dI[du])+A1pl(k[k])',
            u'elliyor(elliyormak)+Verb+Pos+Adj+PastPart(dIk[duk])+Pnon',
            u'elliyor(elliyormak)+Verb+Pos+Noun+PastPart(dIk[duk])+A3sg+Pnon+Nom')

        self.assert_parse_correct(u'oynuyorlar',
            u'oyn(oynamak)+Verb+Pos+Prog(Iyor[uyor])+A3pl(lAr[lar])',
            u'oyn(oynumak)+Verb+Pos+Prog(Iyor[uyor])+A3pl(lAr[lar])',
            u'oynuyo(oynuyomak)+Verb+Pos+Aor(+Ar[r])+A3pl(lAr[lar])',
            u'oynuyorla(oynuyorlamak)+Verb+Pos+Aor(+Ar[r])+A3sg',
            u'oynuyorlar(oynuyorlarmak)+Verb+Pos+Imp+A2sg',
            u'oynuyorla(oynuyorlamak)+Verb+Pos+Aor(+Ar[r])+Adj+Zero',
            u'oynuyo(oynuyomak)+Verb+Pos+Aor(+Ar[r])+Adj+Zero+Noun+Zero+A3pl(lAr[lar])+Pnon+Nom',
            u'oynuyorla(oynuyorlamak)+Verb+Pos+Aor(+Ar[r])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')

        self.assert_parse_correct(u'söylüyorsun',
            u'söyl(söylemek)+Verb+Pos+Prog(Iyor[üyor])+A2sg(sIn[sun])',
            u'söyl(söylümek)+Verb+Pos+Prog(Iyor[üyor])+A2sg(sIn[sun])',
            u'söylüyo(söylüyomak)+Verb+Pos+Aor(+Ar[r])+A2sg(sIn[sun])',
            u'söylüyor(söylüyormak)+Verb+Pos+Imp+A3sg(sIn[sun])',
            u'söylüyorsun(söylüyorsunmak)+Verb+Pos+Imp+A2sg',
            u'söylüyorsu(söylüyorsumak)+Verb+Verb+Pass(+In[n])+Pos+Imp+A2sg')

        self.assert_parse_correct(u'atlıyorsunuz',
            u'atl(atlamak)+Verb+Pos+Prog(Iyor[ıyor])+A2pl(sInIz[sunuz])',
            u'atl(atlımak)+Verb+Pos+Prog(Iyor[ıyor])+A2pl(sInIz[sunuz])',
            u'atlıyo(atlıyomak)+Verb+Pos+Aor(+Ar[r])+A2pl(sInIz[sunuz])',
            u'atlıyorsunuz(atlıyorsunuzmak)+Verb+Pos+Imp+A2sg')

        self.assert_parse_correct(u'kazıyor',
            u'kaz(kazmak)+Verb+Pos+Prog(Iyor[ıyor])+A3sg',
            u'kaz(kazamak)+Verb+Pos+Prog(Iyor[ıyor])+A3sg',
            u'kaz(kazımak)+Verb+Pos+Prog(Iyor[ıyor])+A3sg',
            u'kazıyo(kazıyomak)+Verb+Pos+Aor(+Ar[r])+A3sg',
            u'kazıyor(kazıyormak)+Verb+Pos+Imp+A2sg',
            u'kazıyo(kazıyomak)+Verb+Pos+Aor(+Ar[r])+Adj+Zero',
            u'kazıyo(kazıyomak)+Verb+Pos+Aor(+Ar[r])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')

        self.assert_parse_correct(u'koruyor',
            u'kor(kormak)+Verb+Pos+Prog(Iyor[uyor])+A3sg',
            u'kor(koramak)+Verb+Pos+Prog(Iyor[uyor])+A3sg',
            u'kor(korumak)+Verb+Pos+Prog(Iyor[uyor])+A3sg',
            u'koruyo(koruyomak)+Verb+Pos+Aor(+Ar[r])+A3sg',
            u'koruyor(koruyormak)+Verb+Pos+Imp+A2sg',
            u'koruyo(koruyomak)+Verb+Pos+Aor(+Ar[r])+Adj+Zero',
            u'koruyo(koruyomak)+Verb+Pos+Aor(+Ar[r])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')

    def test_should_parse_verbs_with_aorist_A_and_causative_Ar(self):
        self.assert_parse_correct(u'çıkar',
            u'çık(çıkmak)+Verb+Pos+Aor(+Ar[ar])+A3sg',
            u'çıka(çıkamak)+Verb+Pos+Aor(+Ar[r])+A3sg',
            u'çıkar(çıkarmak)+Verb+Pos+Imp+A2sg',
            u'çık(çıkmak)+Verb+Pos+Aor(+Ar[ar])+Adj+Zero',
            u'çıka(çıkamak)+Verb+Pos+Aor(+Ar[r])+Adj+Zero',
            u'çık(çıkmak)+Verb+Verb+Caus(Ar[ar])+Pos+Imp+A2sg',
            u'çık(çıkmak)+Verb+Pos+Aor(+Ar[ar])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom',
            u'çıka(çıkamak)+Verb+Pos+Aor(+Ar[r])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')

        self.assert_parse_correct(u'ötercesine',
            u'ötercesin(ötercesinmek)+Verb+Pos+Opt(A[e])+A3sg',
            u'ötercesine(ötercesinemek)+Verb+Pos+Imp+A2sg',
            u'öterces(ötercesmek)+Verb+Verb+Pass(+In[in])+Pos+Opt(A[e])+A3sg',
            u'ötercesi(ötercesimek)+Verb+Verb+Pass(+In[n])+Pos+Opt(A[e])+A3sg',
            u'öt(ötmek)+Verb+Pos+Aor(+Ar[er])+Adv+AsIf(cAsI!nA[cesine])',
            u'öte(ötemek)+Verb+Pos+Aor(+Ar[r])+Adv+AsIf(cAsI!nA[cesine])',
            u'öt(ötmek)+Verb+Pos+Aor(+Ar[er])+Adj+Zero+Adj+Equ(cA[ce])+Noun+Zero+A3sg+P3sg(+sI[si])+Dat(nA[ne])',
            u'öt(ötmek)+Verb+Pos+Aor(+Ar[er])+Adj+Zero+Adj+Quite(cA[ce])+Noun+Zero+A3sg+P3sg(+sI[si])+Dat(nA[ne])',
            u'öte(ötemek)+Verb+Pos+Aor(+Ar[r])+Adj+Zero+Adj+Equ(cA[ce])+Noun+Zero+A3sg+P3sg(+sI[si])+Dat(nA[ne])',
            u'öte(ötemek)+Verb+Pos+Aor(+Ar[r])+Adj+Zero+Adj+Quite(cA[ce])+Noun+Zero+A3sg+P3sg(+sI[si])+Dat(nA[ne])',
            u'öt(ötmek)+Verb+Pos+Aor(+Ar[er])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom+Adj+Equ(cA[ce])+Noun+Zero+A3sg+P3sg(+sI[si])+Dat(nA[ne])',
            u'öte(ötemek)+Verb+Pos+Aor(+Ar[r])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom+Adj+Equ(cA[ce])+Noun+Zero+A3sg+P3sg(+sI[si])+Dat(nA[ne])')

        self.assert_parse_correct(u'zebersin',
            u'zeb(zebmek)+Verb+Pos+Aor(+Ar[er])+A2sg(sIn[sin])',
            u'zebe(zebemek)+Verb+Pos+Aor(+Ar[r])+A2sg(sIn[sin])',
            u'zeber(zebermek)+Verb+Pos+Imp+A3sg(sIn[sin])',
            u'zebersin(zebersinmek)+Verb+Pos+Imp+A2sg',
            u'zeb(zebmek)+Verb+Verb+Caus(Ar[er])+Pos+Imp+A3sg(sIn[sin])',
            u'zebersi(zebersimek)+Verb+Verb+Pass(+In[n])+Pos+Imp+A2sg')

    def test_should_parse_verbs_with_aorist_I(self):
        self.assert_parse_correct(u'yatır',
            u'ya(yamak)+Verb+Verb+Caus(t[t])+Pos+Aor(+Ir[ır])+A3sg',
            u'ya(yamak)+Verb+Verb+Caus(t[t])+Verb+Caus(Ir[ır])+Pos+Imp+A2sg',
            u'yat(yatmak)+Verb+Pos+Aor(+Ir[ır])+A3sg',
            u'yat(yatmak)+Verb+Verb+Caus(Ir[ır])+Pos+Imp+A2sg',
            u'yatı(yatımak)+Verb+Pos+Aor(+Ar[r])+A3sg',
            u'yatır(yatırmak)+Verb+Pos+Imp+A2sg',
            u'yat(yatmak)+Verb+Pos+Aor(+Ir[ır])+Adj+Zero',
            u'yatı(yatımak)+Verb+Pos+Aor(+Ar[r])+Adj+Zero',
            u'ya(yamak)+Verb+Verb+Caus(t[t])+Pos+Aor(+Ir[ır])+Adj+Zero',
            u'yat(yatmak)+Verb+Pos+Aor(+Ir[ır])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom',
            u'yatı(yatımak)+Verb+Pos+Aor(+Ar[r])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom',
            u'ya(yamak)+Verb+Verb+Caus(t[t])+Pos+Aor(+Ir[ır])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')

        self.assert_parse_correct(u'gelir',
            u'gel(gelmek)+Verb+Pos+Aor(+Ir[ir])+A3sg',
            u'geli(gelimek)+Verb+Pos+Aor(+Ar[r])+A3sg',
            u'gelir(gelirmek)+Verb+Pos+Imp+A2sg',
            u'gel(gelmek)+Verb+Pos+Aor(+Ir[ir])+Adj+Zero',
            u'geli(gelimek)+Verb+Pos+Aor(+Ar[r])+Adj+Zero',
            u'gel(gelmek)+Verb+Verb+Caus(Ir[ir])+Pos+Imp+A2sg',
            u'gel(gelmek)+Verb+Pos+Aor(+Ir[ir])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom',
            u'geli(gelimek)+Verb+Pos+Aor(+Ar[r])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')

        self.assert_parse_correct(u'zopuracak',
            u'zopur(zopurmak)+Verb+Pos+Fut(+yAcAk[acak])+A3sg',
            u'zopuracak(zopuracakmak)+Verb+Pos+Imp+A2sg',
            u'zopur(zopurmak)+Verb+Pos+Adj+FutPart(+yAcAk[acak])+Pnon',
            u'zopur(zopurmak)+Verb+Pos+Fut(+yAcAk[acak])+Adj+Zero',
            u'zop(zopmak)+Verb+Verb+Caus(Ir[ur])+Pos+Fut(+yAcAk[acak])+A3sg',
            u'zop(zopmak)+Verb+Verb+Caus(Ir[ur])+Pos+Adj+FutPart(+yAcAk[acak])+Pnon',
            u'zop(zopmak)+Verb+Verb+Caus(Ir[ur])+Pos+Fut(+yAcAk[acak])+Adj+Zero',
            u'zopur(zopurmak)+Verb+Pos+Noun+FutPart(+yAcAk[acak])+A3sg+Pnon+Nom',
            u'zop(zopmak)+Verb+Verb+Caus(Ir[ur])+Pos+Noun+FutPart(+yAcAk[acak])+A3sg+Pnon+Nom',
            u'zopur(zopurmak)+Verb+Pos+Fut(+yAcAk[acak])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom',
            u'zop(zopmak)+Verb+Verb+Caus(Ir[ur])+Pos+Fut(+yAcAk[acak])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')

        self.assert_parse_correct(u'zoburacak',
            u'zobur(zoburmak)+Verb+Pos+Fut(+yAcAk[acak])+A3sg',
            u'zoburacak(zoburacakmak)+Verb+Pos+Imp+A2sg',
            u'zobur(zoburmak)+Verb+Pos+Adj+FutPart(+yAcAk[acak])+Pnon',
            u'zobur(zoburmak)+Verb+Pos+Fut(+yAcAk[acak])+Adj+Zero',
            u'zob(zobmak)+Verb+Verb+Caus(Ir[ur])+Pos+Fut(+yAcAk[acak])+A3sg',
            u'zob(zobmak)+Verb+Verb+Caus(Ir[ur])+Pos+Adj+FutPart(+yAcAk[acak])+Pnon',
            u'zob(zobmak)+Verb+Verb+Caus(Ir[ur])+Pos+Fut(+yAcAk[acak])+Adj+Zero',
            u'zobur(zoburmak)+Verb+Pos+Noun+FutPart(+yAcAk[acak])+A3sg+Pnon+Nom',
            u'zob(zobmak)+Verb+Verb+Caus(Ir[ur])+Pos+Noun+FutPart(+yAcAk[acak])+A3sg+Pnon+Nom',
            u'zobur(zoburmak)+Verb+Pos+Fut(+yAcAk[acak])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom',
            u'zob(zobmak)+Verb+Verb+Caus(Ir[ur])+Pos+Fut(+yAcAk[acak])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')

    def test_should_parse_verbs_with_causative_t(self):
        self.assert_parse_correct(u'kapattım',
            u'kapat(kapatmak)+Verb+Pos+Past(dI[tı])+A1sg(+Im[m])',
            u'kapattı(kapattımak)+Verb+Neg(m[m])+Imp+A2sg',
            u'kapattım(kapattımmak)+Verb+Pos+Imp+A2sg',
            u'kapa(kapamak)+Verb+Verb+Caus(t[t])+Pos+Past(dI[tı])+A1sg(+Im[m])')

        self.assert_parse_correct(u'yürütecekmiş',
            u'yürütecek(yürütecekmek)+Verb+Pos+Narr(mIş[miş])+A3sg',
            u'yürütecekmiş(yürütecekmişmek)+Verb+Pos+Imp+A2sg',
            u'yürüt(yürütmek)+Verb+Pos+Fut(+yAcAk[ecek])+Narr(mIş[miş])+A3sg',
            u'yürütecek(yürütecekmek)+Verb+Pos+Narr(mIş[miş])+Adj+Zero',
            u'yürütecekmi(yürütecekmimek)+Verb+Verb+Recip(+Iş[ş])+Pos+Imp+A2sg',
            u'yür(yürmek)+Verb+Verb+Caus(It[üt])+Pos+Fut(+yAcAk[ecek])+Narr(mIş[miş])+A3sg',
            u'yürü(yürümek)+Verb+Verb+Caus(t[t])+Pos+Fut(+yAcAk[ecek])+Narr(mIş[miş])+A3sg',
            u'yürütecek(yürütecekmek)+Verb+Pos+Narr(mIş[miş])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom')

    def test_should_parse_verbs_with_causative_It(self):
        self.assert_parse_correct(u'akıtmışlar',
            u'ak(akmak)+Verb+Verb+Caus(It[ıt])+Pos+Narr(mIş[mış])+A3pl(lAr[lar])',
            u'akı(akımak)+Verb+Verb+Caus(t[t])+Pos+Narr(mIş[mış])+A3pl(lAr[lar])',
            u'akıt(akıtmak)+Verb+Pos+Narr(mIş[mış])+A3pl(lAr[lar])',
            u'akıtmışla(akıtmışlamak)+Verb+Pos+Aor(+Ar[r])+A3sg',
            u'akıtmışlar(akıtmışlarmak)+Verb+Pos+Imp+A2sg',
            u'akıtmışla(akıtmışlamak)+Verb+Pos+Aor(+Ar[r])+Adj+Zero',
            u'akıt(akıtmak)+Verb+Pos+Narr(mIş[mış])+Adj+Zero+Noun+Zero+A3pl(lAr[lar])+Pnon+Nom',
            u'akıtmışla(akıtmışlamak)+Verb+Pos+Aor(+Ar[r])+Adj+Zero+Noun+Zero+A3sg+Pnon+Nom',
            u'ak(akmak)+Verb+Verb+Caus(It[ıt])+Pos+Narr(mIş[mış])+Adj+Zero+Noun+Zero+A3pl(lAr[lar])+Pnon+Nom',
            u'akı(akımak)+Verb+Verb+Caus(t[t])+Pos+Narr(mIş[mış])+Adj+Zero+Noun+Zero+A3pl(lAr[lar])+Pnon+Nom')

        self.assert_parse_correct(u'korkut',
            u'korkut(korkutmak)+Verb+Pos+Imp+A2sg',
            u'kork(korkmak)+Verb+Verb+Caus(It[ut])+Pos+Imp+A2sg',
            u'korku(korkumak)+Verb+Verb+Caus(t[t])+Pos+Imp+A2sg')

    def test_should_parse_verbs_with_causative_dIr(self):
        self.assert_parse_correct(u'aldırsın',
            u'ald(altmak)+Verb+Pos+Aor(+Ir[ır])+A2sg(sIn[sın])',
            u'ald(aldmak)+Verb+Pos+Aor(+Ir[ır])+A2sg(sIn[sın])',
            u'aldı(aldımak)+Verb+Pos+Aor(+Ar[r])+A2sg(sIn[sın])',
            u'aldır(aldırmak)+Verb+Pos+Imp+A3sg(sIn[sın])',
            u'aldırsın(aldırsınmak)+Verb+Pos+Imp+A2sg',
            u'al(almak)+Verb+Verb+Caus(dIr[dır])+Pos+Imp+A3sg(sIn[sın])',
            u'ald(altmak)+Verb+Verb+Caus(Ir[ır])+Pos+Imp+A3sg(sIn[sın])',
            u'ald(aldmak)+Verb+Verb+Caus(Ir[ır])+Pos+Imp+A3sg(sIn[sın])',
            u'aldırsı(aldırsımak)+Verb+Verb+Pass(+In[n])+Pos+Imp+A2sg')

        self.assert_parse_correct(u'öldürelim',
            u'öldür(öldürmek)+Verb+Pos+Opt(A[e])+A1pl(lIm[lim])',
            u'öldüreli(öldürelimek)+Verb+Neg(m[m])+Imp+A2sg',
            u'öldürelim(öldürelimmek)+Verb+Pos+Imp+A2sg',
            u'öl(ölmek)+Verb+Verb+Caus(dIr[dür])+Pos+Opt(A[e])+A1pl(lIm[lim])',
            u'öld(öldmek)+Verb+Verb+Caus(Ir[ür])+Pos+Opt(A[e])+A1pl(lIm[lim])',
            u'öld(öltmek)+Verb+Verb+Caus(Ir[ür])+Pos+Opt(A[e])+A1pl(lIm[lim])')

        self.assert_parse_correct(u'öttürsek',
            u'öttür(öttürmek)+Verb+Pos+Cond(+ysA[se])+A1pl(k[k])',
            u'öttür(öttürmek)+Verb+Pos+Desr(sA[se])+A1pl(k[k])',
            u'öttürsek(öttürsekmek)+Verb+Pos+Imp+A2sg',
            u'öttü(öttümek)+Verb+Pos+Aor(+Ar[r])+Cond(+ysA[se])+A1pl(k[k])',
            u'öt(ötmek)+Verb+Verb+Caus(dIr[tür])+Pos+Cond(+ysA[se])+A1pl(k[k])',
            u'öt(ötmek)+Verb+Verb+Caus(dIr[tür])+Pos+Desr(sA[se])+A1pl(k[k])',
            u'öt(ötmek)+Verb+Verb+Caus(t[t])+Pos+Aor(+Ir[ür])+Cond(+ysA[se])+A1pl(k[k])',
            u'öt(ötmek)+Verb+Verb+Caus(t[t])+Verb+Caus(Ir[ür])+Pos+Cond(+ysA[se])+A1pl(k[k])',
            u'öt(ötmek)+Verb+Verb+Caus(t[t])+Verb+Caus(Ir[ür])+Pos+Desr(sA[se])+A1pl(k[k])')

    def assert_parse_correct(self, word_to_parse, *args):
        super(ParserTestWithBruteForceVerbRootFinder, self).assert_parse_correct(word_to_parse, *args)
        assert len(list(args)) == len(set(args))


if __name__ == '__main__':
    unittest.main()
