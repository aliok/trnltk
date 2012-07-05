# coding=utf-8
import logging
import os
import unittest
from hamcrest import *
from hamcrest.core.base_matcher import BaseMatcher
from trnltk.stem.dictionaryitem import  PrimaryPosition, SecondaryPosition
from trnltk.stem.dictionaryloader import DictionaryLoader
from trnltk.stem.stemgenerator import StemGenerator, StemRootMapGenerator
from trnltk.suffixgraph.predefinedpaths import PredefinedPaths
from trnltk.suffixgraph.parser import Parser, logger as parser_logger
from trnltk.suffixgraph.suffixapplier import logger as suffix_applier_logger
from trnltk.suffixgraph.suffixgraph import SuffixGraph

class PredefinedPathsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(PredefinedPathsTest, cls).setUpClass()
        all_stems = []

        dictionary_items = DictionaryLoader.load_from_file(os.path.join(os.path.dirname(__file__), '../../resources/master_dictionary.txt'))
        for di in dictionary_items:
            all_stems.extend(StemGenerator.generate(di))

        stem_root_map_generator = StemRootMapGenerator()
        cls.stem_root_map = stem_root_map_generator.generate(all_stems)

        cls.token_map = {}

        cls.suffix_graph = SuffixGraph()

    def setUp(self):
        super(PredefinedPathsTest, self).setUp()

        logging.basicConfig(level=logging.INFO)
        parser_logger.setLevel(logging.INFO)
        suffix_applier_logger.setLevel(logging.INFO)

        self.predefined_paths = PredefinedPaths(self.stem_root_map, self.suffix_graph)

    def tearDown(self):
        self.predefined_paths = None
        self.token_map = {}


    def test_should_have_paths_for_personal_pronouns(self):
        self.predefined_paths._create_predefined_path_of_ben()
        self.predefined_paths._create_predefined_path_of_sen()

        self.token_map = self.predefined_paths.token_map

        PRON = PrimaryPosition.PRONOUN
        PERS = SecondaryPosition.PERSONAL

        # last one ends with transition to derivation state
        self.assert_defined_path(u'ben', PRON, PERS,
            u'ben(ben)+Pron+Pers+A1sg+Pnon+Nom',
            u'ben(ben)+Pron+Pers+A1sg+Pnon+Acc(i[i])',
            u'ben(ben)+Pron+Pers+A1sg+Pnon+Loc(de[de])',
            u'ben(ben)+Pron+Pers+A1sg+Pnon+Abl(den[den])',
            u'ben(ben)+Pron+Pers+A1sg+Pnon+Ins(le[le])',
            u'ben(ben)+Pron+Pers+A1sg+Pnon+Ins(imle[imle])',
            u'ben(ben)+Pron+Pers+A1sg+Pnon+Gen(im[im])',
            u'ben(ben)+Pron+Pers+A1sg+Pnon+AccordingTo(ce[ce])',
            u'ben(ben)+Pron+Pers+A1sg+Pnon+Nom')

        self.assert_defined_path(u'ban', PRON, PERS,
            u'ban(ben)+Pron+Pers+A1sg+Pnon+Dat(a[a])')

        # last one ends with transition to derivation state
        self.assert_defined_path(u'sen', PRON, PERS,
            u'sen(sen)+Pron+Pers+A2sg+Pnon+Nom',
            u'sen(sen)+Pron+Pers+A2sg+Pnon+Acc(i[i])',
            u'sen(sen)+Pron+Pers+A2sg+Pnon+Loc(de[de])',
            u'sen(sen)+Pron+Pers+A2sg+Pnon+Abl(den[den])',
            u'sen(sen)+Pron+Pers+A2sg+Pnon+Ins(le[le])',
            u'sen(sen)+Pron+Pers+A2sg+Pnon+Ins(inle[inle])',
            u'sen(sen)+Pron+Pers+A2sg+Pnon+Gen(in[in])',
            u'sen(sen)+Pron+Pers+A2sg+Pnon+AccordingTo(ce[ce])',
            u'sen(sen)+Pron+Pers+A2sg+Pnon+Nom')

        self.assert_defined_path(u'san', PRON, PERS,
            u'san(sen)+Pron+Pers+A2sg+Pnon+Dat(a[a])')

    def test_should_have_paths_for_hepsi(self):
        parser_logger.setLevel(logging.DEBUG)
        suffix_applier_logger.setLevel(logging.DEBUG)

        self.predefined_paths._create_predefined_path_of_hepsi()

        self.token_map = self.predefined_paths.token_map

        PRON = PrimaryPosition.PRONOUN

        # last one ends with transition to derivation state
        self.assert_defined_path(u'hepsi', PRON, None,
            u'hepsi(hepsi)+Pron+A3pl+P3pl+Nom',
            u'hepsi(hepsi)+Pron+A3pl+P3pl+Acc(ni[ni])',
            u'hepsi(hepsi)+Pron+A3pl+P3pl+Dat(ne[ne])',
            u'hepsi(hepsi)+Pron+A3pl+P3pl+Loc(nde[nde])',
            u'hepsi(hepsi)+Pron+A3pl+P3pl+Abl(nden[nden])',
            u'hepsi(hepsi)+Pron+A3pl+P3pl+Ins(yle[yle])',
            u'hepsi(hepsi)+Pron+A3pl+P3pl+Gen(nin[nin])',
            u'hepsi(hepsi)+Pron+A3pl+P3pl+AccordingTo(nce[nce])',
            u'hepsi(hepsi)+Pron+A3pl+P3pl+Nom')

        # last one ends with transition to derivation state
        self.assert_defined_path(u'hep', PRON, None,
            u'hep(hepsi)+Pron+A1pl+P1pl(imiz[imiz])+Nom',
            u'hep(hepsi)+Pron+A1pl+P1pl(imiz[imiz])+Acc(i[i])',
            u'hep(hepsi)+Pron+A1pl+P1pl(imiz[imiz])+Dat(e[e])',
            u'hep(hepsi)+Pron+A1pl+P1pl(imiz[imiz])+Loc(de[de])',
            u'hep(hepsi)+Pron+A1pl+P1pl(imiz[imiz])+Abl(den[den])',
            u'hep(hepsi)+Pron+A1pl+P1pl(imiz[imiz])+Ins(le[le])',
            u'hep(hepsi)+Pron+A1pl+P1pl(imiz[imiz])+Gen(in[in])',
            u'hep(hepsi)+Pron+A1pl+P1pl(imiz[imiz])+AccordingTo(ce[ce])',
            u'hep(hepsi)+Pron+A1pl+P1pl(imiz[imiz])+Nom',
            u'hep(hepsi)+Pron+A2pl+P2pl(iniz[iniz])+Nom',
            u'hep(hepsi)+Pron+A2pl+P2pl(iniz[iniz])+Acc(i[i])',
            u'hep(hepsi)+Pron+A2pl+P2pl(iniz[iniz])+Dat(e[e])',
            u'hep(hepsi)+Pron+A2pl+P2pl(iniz[iniz])+Loc(de[de])',
            u'hep(hepsi)+Pron+A2pl+P2pl(iniz[iniz])+Abl(den[den])',
            u'hep(hepsi)+Pron+A2pl+P2pl(iniz[iniz])+Ins(le[le])',
            u'hep(hepsi)+Pron+A2pl+P2pl(iniz[iniz])+Gen(in[in])',
            u'hep(hepsi)+Pron+A2pl+P2pl(iniz[iniz])+AccordingTo(ce[ce])',
            u'hep(hepsi)+Pron+A2pl+P2pl(iniz[iniz])+Nom')

    def test_should_have_paths_for_ques(self):
        parser_logger.setLevel(logging.DEBUG)
        suffix_applier_logger.setLevel(logging.DEBUG)

        self.predefined_paths._create_predefined_path_of_question_particles()

        self.token_map = self.predefined_paths.token_map

        QUES = PrimaryPosition.QUESTION

        # last one ends with transition to derivation state
        self.assert_defined_path(u'mı', QUES, None,
            u'mı(mı)+Ques+Pres+A1sg(yım[yım])',
            u'mı(mı)+Ques+Pres+A2sg(sın[sın])',
            u'mı(mı)+Ques+Pres+A3sg',
            u'mı(mı)+Ques+Pres+A1pl(yız[yız])',
            u'mı(mı)+Ques+Pres+A2pl(sınız[sınız])',
            u'mı(mı)+Ques+Pres+A3pl(lar[lar])',
            u'mı(mı)+Ques+Past(ydı[ydı])+A1sg(m[m])',
            u'mı(mı)+Ques+Past(ydı[ydı])+A2sg(n[n])',
            u'mı(mı)+Ques+Past(ydı[ydı])+A3sg',
            u'mı(mı)+Ques+Past(ydı[ydı])+A1pl(k[k])',
            u'mı(mı)+Ques+Past(ydı[ydı])+A2pl(nız[nız])',
            u'mı(mı)+Ques+Past(ydı[ydı])+A3pl(lar[lar])',
            u'mı(mı)+Ques+Past(ymış[ymış])+A1sg(ım[ım])',
            u'mı(mı)+Ques+Past(ymış[ymış])+A2sg(sın[sın])',
            u'mı(mı)+Ques+Past(ymış[ymış])+A3sg',
            u'mı(mı)+Ques+Past(ymış[ymış])+A1pl(ız[ız])',
            u'mı(mı)+Ques+Past(ymış[ymış])+A2pl(sınız[sınız])',
            u'mı(mı)+Ques+Past(ymış[ymış])+A3pl(lar[lar])')
        
    def assert_defined_path(self, stem_root, primary_position, secondary_position, *args):
        assert_that(self.predefined_tokens(stem_root, primary_position, secondary_position), IsTokensMatches([a for a in args]))

    def predefined_tokens(self, stem_root, primary_position, secondary_position):
        predefined_tokens = []
        for stem in self.token_map.keys():
            if stem.root==stem_root and stem.dictionary_item.primary_position==primary_position and stem.dictionary_item.secondary_position==secondary_position:
                predefined_tokens.extend(self.token_map[stem])

        return [r.to_pretty_str() for r in predefined_tokens]


class IsTokensMatches(BaseMatcher):
    def __init__(self, expected_results):
        self.expected_results = expected_results

    def _matches(self, item):
        return item == self.expected_results

    def describe_to(self, description):
        description.append_text(u'     ' + str(self.expected_results))

if __name__ == '__main__':
    unittest.main()
