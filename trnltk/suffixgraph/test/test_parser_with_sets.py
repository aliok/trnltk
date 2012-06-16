# coding=utf-8
import codecs
import logging
import os
import unittest
from hamcrest import *
from hamcrest.core.base_matcher import BaseMatcher
from trnltk.stem.dictionaryitem import  PrimaryPosition, SecondaryPosition
from trnltk.stem.dictionaryloader import DictionaryLoader
from trnltk.stem.stemgenerator import CircumflexConvertingStemGenerator, StemRootMapGenerator
from trnltk.suffixgraph.extendedsuffixgraph import ExtendedSuffixGraph
from trnltk.suffixgraph.parser import Parser, logger as parser_logger
from trnltk.suffixgraph.suffixapplier import logger as suffix_applier_logger
from trnltk.suffixgraph.predefinedpaths import PredefinedPaths
from trnltk.suffixgraph.suffixgraph import State, FreeTransitionSuffix, SuffixGraph

#TODO
cases_to_skip = {
    u'Equ',
    u'FitFor',
    u'AsIf',
    u'JustLike',
    u'Noun+Ness',

    u'(1,"s\xfcr+Verb")(2,"Verb+Caus")(3,"Verb+Pass+Pos")(4,"Adj+PresPart")',
    u'(1,"yerle\u015f+Verb")(2,"Verb+Caus")(3,"Verb+Pass+Pos+Narr")(4,"Adj+Zero")',

    u'(1,"kapa+Verb")(2,"Verb+Caus")(3,"Verb+Pass+Pos+Narr")(4,"Adj+Zero")',
    u'(1,"d\xfc\u015f\xfcn+Verb")(2,"Verb+Caus")(3,"Verb+Caus+Pos+Prog1+Past+A3sg")',    #dusunduyordu <> dusundurtuyordu

    u'incecik+',        # Think about it!

    u'_',
    u'+Prop+',
    u'Postp',
    u'kimi+Pron',  # TODO: check how "bazi" is on the set

    #TODO: need to add pron acc form +nA. same for : biri, kimi, cogu, coklari vs....
    u'üzer+',
    u'üzeri',
    u'hi\xe7biri',
    u'birbiri+Pron',
    u'birbiri+Pron+A3pl',  # TODO: birbirleri
    u'çoğu',

    u'â',
    u'kadar',
    u'tamam+Adv',         # Part or Adv?
    u'Postp',
    u'Aor+A3pl+Past"',    # yaparlardi
    u'Prog1+A3pl+Past',   # yapiyorlardi
    u'+Cop+A3pl',         # hazirdirlar <> hazirlardir , similarly for "QuesPart"s : midirler
    u'içeri',
    u'yaşa+Verb+Neg+Past+A2pl+Cond"',

    u'vakit+',            # becomes vaktIn
    u'havil+',            # becomes can havlIyla
    u'(1,"savur+Verb")(2,"Verb+Pass+Pos")',         # savrul <> savrIl

    u'sonralar\u0131+Adv',      # aksamlari, geceleri, vs...


    u'kimbilir+',
    u'(1,"anlat+Verb")(2,"Verb+Able+Neg")(3,"Adv+WithoutHavingDoneSo1")'        # very complicated!
}

class ParserTestWithSets(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(ParserTestWithSets, cls).setUpClass()
        all_stems = []

        dictionary_items = DictionaryLoader.load_from_file(os.path.join(os.path.dirname(__file__), '../../resources/master_dictionary.txt'))
        for di in dictionary_items:
            all_stems.extend(CircumflexConvertingStemGenerator.generate(di))

        stem_root_map_generator = StemRootMapGenerator()
        cls.stem_root_map = stem_root_map_generator.generate(all_stems)

        suffix_graph = ExtendedSuffixGraph()
        predefined_paths = PredefinedPaths(cls.stem_root_map, suffix_graph)
        predefined_paths.create_predefined_paths()

        cls.parser = Parser(cls.stem_root_map, suffix_graph, predefined_paths)

    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        parser_logger.setLevel(logging.INFO)
        suffix_applier_logger.setLevel(logging.INFO)

    def test_should_parse_set_001(self):
#        parser_logger.setLevel(logging.DEBUG)
#        suffix_applier_logger.setLevel(logging.DEBUG)
        self._test_should_parse_set("001")

    def test_should_parse_set_002(self):
#        parser_logger.setLevel(logging.DEBUG)
#        suffix_applier_logger.setLevel(logging.DEBUG)
        self._test_should_parse_set("002")

    def test_should_parse_set_003(self):
#        parser_logger.setLevel(logging.DEBUG)
#        suffix_applier_logger.setLevel(logging.DEBUG)
        self._test_should_parse_set("003")

    def test_should_parse_set_004(self):
        parser_logger.setLevel(logging.DEBUG)
        suffix_applier_logger.setLevel(logging.DEBUG)
        self._test_should_parse_set("004", 1466)

    def _test_should_parse_set(self, set_number, start_index=0):
        path = os.path.join(os.path.dirname(__file__), '../../testresources/parsesets/parseset{}.txt'.format(set_number))
        with codecs.open(path, 'r', 'utf-8') as parse_set_file:
            index = 0
            for line in parse_set_file:
                if line.startswith('#'):
                    continue

                line = line.strip()
                (word, parse_result) = line.split('=')
                if any([case_to_skip in parse_result for case_to_skip in cases_to_skip]):
                    index +=1
                    continue

                if start_index<=index:
                    #TODO
                    parse_result = parse_result.replace('Prog1', 'Prog')
                    parse_result = parse_result.replace('Prog2', 'Prog')
                    parse_result = parse_result.replace('Inf1', 'Inf')
                    parse_result = parse_result.replace('Inf2', 'Inf')
                    parse_result = parse_result.replace('Inf3', 'Inf')
                    parse_result = parse_result.replace('WithoutHavingDoneSo1', 'WithoutHavingDoneSo')
                    parse_result = parse_result.replace('WithoutHavingDoneSo2', 'WithoutHavingDoneSo')


                    #TODO
                    parse_result = parse_result.replace('Hastily', 'Hastily+Pos')

                    parse_result = parse_result.replace('Postp+PCNom', 'Part')
                    parse_result = parse_result.replace('Postp+PCDat', 'Postp')
                    parse_result = parse_result.replace('Postp+PCAcc', 'Postp')
                    parse_result = parse_result.replace('Postp+PCLoc', 'Postp')
                    parse_result = parse_result.replace('Postp+PCAbl', 'Postp')
                    parse_result = parse_result.replace('Postp+PCIns', 'Postp')
                    parse_result = parse_result.replace('Postp+PCGen', 'Postp')

                    self.assert_parse_correct(word.lower(), index, parse_result)

                index += 1

    def assert_parse_correct(self, word_to_parse, index, *args):
        assert_that(self.parse_result(word_to_parse), IsParseResultMatches([a for a in args]), u'Error in word : {} at index {}'.format(repr(word_to_parse), index))

    def parse_result(self, word):
        return [self._parse_token_to_parse_set_str(r) for r in (self.parser.parse(word))]

    @classmethod
    def _parse_token_to_parse_set_str(cls, result):
        groups = []
        current_group = []
        for transition in result.transitions:
            if transition.from_state.type==State.DERIV:
                groups.append(current_group)
                current_group = [transition.to_state.pretty_name]
            else:
                pass

            if not isinstance(transition.suffix_form_application.suffix_form.suffix, FreeTransitionSuffix):
                current_group.append(transition.suffix_form_application.suffix_form.suffix.pretty_name)

        groups.append(current_group)

        root = result.stem.dictionary_item.root

        secondary_position_str = None

        ##TODO:
        if result.stem.dictionary_item.primary_position==PrimaryPosition.PRONOUN:
            if result.stem.dictionary_item.secondary_position==SecondaryPosition.PERSONAL:
                secondary_position_str = "PersP"
            elif result.stem.dictionary_item.secondary_position==SecondaryPosition.DEMONSTRATIVE:
                secondary_position_str = "DemonsP"
            elif result.stem.dictionary_item.secondary_position==SecondaryPosition.QUESTION:
                secondary_position_str = "QuesP"
            elif result.stem.dictionary_item.secondary_position==SecondaryPosition.REFLEXIVE:
                secondary_position_str = "ReflexP"

        if result.stem.dictionary_item.primary_position==PrimaryPosition.NUMERAL:
            if result.stem.dictionary_item.secondary_position==SecondaryPosition.CARD:
                secondary_position_str = "Card"


        if not groups:
            if not secondary_position_str:
                return u'({},"{}+{}")'.format(1, root, result.stem_state.pretty_name)
            else:
                return u'({},"{}+{}+{}")'.format(1, root, result.stem_state.pretty_name, secondary_position_str)



        return_value = None

        if not secondary_position_str:
            return_value = u'({},"{}+{}")'.format(1, root, result.stem_state.pretty_name)
        else:
            return_value = u'({},"{}+{}+{}")'.format(1, root, result.stem_state.pretty_name, secondary_position_str)

        if not groups[0]:
            if not secondary_position_str:
                return_value = u'({},"{}+{}")'.format(1, root, result.stem_state.pretty_name)
            else:
                return_value = u'({},"{}+{}+{}")'.format(1, root, result.stem_state.pretty_name, secondary_position_str)
        else:
            if not secondary_position_str:
                return_value = u'({},"{}+{}+{}")'.format(1, root, result.stem_state.pretty_name, u'+'.join(groups[0]))
            else:
                return_value = u'({},"{}+{}+{}+{}")'.format(1, root, result.stem_state.pretty_name, secondary_position_str, u'+'.join(groups[0]))


        for i in range(1, len(groups)):
            group = groups[i]
            return_value += u'({},"{}")'.format(i+1, u'+'.join(group))

        ##TODO:
        if any(c in CircumflexConvertingStemGenerator.Circumflex_Chars for c in return_value):
            for (cir, pla) in CircumflexConvertingStemGenerator.Circumflex_Letters_Map.iteritems():
                return_value = return_value.replace(cir, pla)

        return return_value

class IsParseResultMatches(BaseMatcher):
    def __init__(self, expected_results):
        self.expected_results = expected_results

    def _matches(self, item):
        return all([expected_result in item for expected_result in self.expected_results])

    def describe_to(self, description):
        description.append_text(u'     ' + str(self.expected_results))

if __name__ == '__main__':
    unittest.main()
