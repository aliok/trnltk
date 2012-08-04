# coding=utf-8
import logging
import os
import unittest
from hamcrest import *
from hamcrest.core.base_matcher import BaseMatcher
from trnltk.morphology.model import formatter
from trnltk.morphology.model.lexeme import  SyntacticCategory, SecondarySyntacticCategory
from trnltk.morphology.lexicon.lexiconloader import LexiconLoader
from trnltk.morphology.lexicon.rootgenerator import RootGenerator, RootMapGenerator
from trnltk.morphology.morphotactics.predefinedpaths import PredefinedPaths
from trnltk.morphology.contextfree.parser.parser import  logger as parser_logger
from trnltk.morphology.contextfree.parser.suffixapplier import logger as suffix_applier_logger
from trnltk.morphology.morphotactics.suffixgraph import SuffixGraph

class PredefinedPathsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(PredefinedPathsTest, cls).setUpClass()
        all_roots = []

        lexemes = LexiconLoader.load_from_file(os.path.join(os.path.dirname(__file__), '../../../resources/master_dictionary.txt'))
        for di in lexemes:
            all_roots.extend(RootGenerator.generate(di))

        root_map_generator = RootMapGenerator()
        cls.root_map = root_map_generator.generate(all_roots)

        cls.morpheme_container_map = {}

        cls.suffix_graph = SuffixGraph()

    def setUp(self):
        super(PredefinedPathsTest, self).setUp()

        logging.basicConfig(level=logging.INFO)
        parser_logger.setLevel(logging.INFO)
        suffix_applier_logger.setLevel(logging.INFO)

        self.predefined_paths = PredefinedPaths(self.root_map, self.suffix_graph)

    def tearDown(self):
        self.predefined_paths = None
        self.morpheme_container_map = {}


    def test_should_have_paths_for_personal_pronouns(self):
        self.predefined_paths._create_predefined_path_of_ben()
        self.predefined_paths._create_predefined_path_of_sen()

        self.morpheme_container_map = self.predefined_paths._morpheme_container_map

        PRON = SyntacticCategory.PRONOUN
        PERS = SecondarySyntacticCategory.PERSONAL

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

        self.morpheme_container_map = self.predefined_paths._morpheme_container_map

        PRON = SyntacticCategory.PRONOUN

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

        self.morpheme_container_map = self.predefined_paths._morpheme_container_map

        QUES = SyntacticCategory.QUESTION

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
        
    def assert_defined_path(self, root, syntactic_category, secondary_syntactic_category, *args):
        assert_that(self.predefined_morpheme_containers(root, syntactic_category, secondary_syntactic_category), AreMorphemeContainersMatch([a for a in args]))

    def predefined_morpheme_containers(self, root_str, syntactic_category, secondary_syntactic_category):
        predefined_morpheme_containers = []
        for root in self.morpheme_container_map.keys():
            if root.str==root_str and root.lexeme.syntactic_category==syntactic_category and root.lexeme.secondary_syntactic_category==secondary_syntactic_category:
                predefined_morpheme_containers.extend(self.morpheme_container_map[root])

        return [formatter.format_morpheme_container_for_tests(r) for r in predefined_morpheme_containers]


class AreMorphemeContainersMatch(BaseMatcher):
    def __init__(self, expected_results):
        self.expected_results = expected_results

    def _matches(self, item):
        return item == self.expected_results

    def describe_to(self, description):
        description.append_text(u'     ' + str(self.expected_results))

if __name__ == '__main__':
    unittest.main()
