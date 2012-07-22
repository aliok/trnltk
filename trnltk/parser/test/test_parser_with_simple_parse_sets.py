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
from trnltk.parser.parser import Parser, logger as parser_logger
from trnltk.parser.stemfinder import WordStemFinder, NumeralStemFinder
from trnltk.parser.suffixapplier import logger as suffix_applier_logger
from trnltk.suffixgraph.predefinedpaths import PredefinedPaths
from trnltk.suffixgraph.suffixgraph import State, FreeTransitionSuffix

#TODO
cases_to_skip = {
    u'FitFor',
    u'Noun+Ness',

    u'1+Num+Card',
    u'70+Num+Card',

    u'(1,"tek+Adj")',

    u'incecik+',        # Think about it!

    u'bir\u015fey+Noun',        # Must be pron!

    u'_',
    u'+Prop+',
    u'+Abbr+',

    u'Postp',
    u'kimi+Pron',  # TODO: check how "bazi" is on the set
    u'baz\u0131+Pron',
    u'biri+Pron',

    #TODO: need to add pron acc form +nA. same for : biri, kimi, cogu, coklari vs....
    u'üzer+',
    u'üzeri',
    u'hi\xe7biri',
    u'birbiri+Pron',
    u'birbiri+Pron+A3pl',  # TODO: birbirleri

    u'â', u'î',
    u'hala+Adv',
    u'sanayi+Noun',
    u'serin+Adv', u"rahat+Adv", u'yeterince+Adv', u'ilk+Adv',       # big thing? using adjectives as adverbs?

    u'(1,"de+Verb+Pos")(2,"Adv+ByDoingSo")',        # diyerek, yiyerek
    u'de+Verb+Pos+Fut+Past+A1pl',                   # diyecek, yiyecek,

    u'kadar',
    u'tamam+Adv',         # Part or Adv?
    u'(1,"de\u011fil+Conj")',
    u'Postp',
    u'Aor+A3pl+Past"',    # yaparlardi
    u'Prog1+A3pl+Past',   # yapiyorlardi
    u'+Cop+A3pl',         # hazirdirlar <> hazirlardir , similarly for "QuesPart"s : midirler
    u'içeri',
    u'yaşa+Verb+Neg+Past+A2pl+Cond"',
    u'(1,"bo\u011ful+Verb+Pos")',

    u'vakit+',            # becomes vaktIn
    u'havil+',            # becomes can havlIyla
    u'(1,"savur+Verb")(2,"Verb+Pass+Pos")',         # savrul <> savrIl
    u'(1,"kavur+Verb")(2,"Verb+Pass+Pos+Narr")(3,"Adj+Zero")', # kavrul <> kavrIl

    u'sonralar\u0131+Adv',      # aksamlari, geceleri, vs...
    u'(1,"y\u0131l+Noun+A3sg+Pnon+Nom")(2,"Adv+Since")', u'yıl+Noun+A3pl+Pnon+Nom")(2,"Adv+Since")',
    u'hiçlik+Noun', u'gençlik+Noun', u'ayr\u0131l\u0131k+Noun', u'arac\u0131l\u0131k',
    u'(1,"yok+Interj")',
    u'yok+Adv',
    u'bir\xe7ok+Det',
    u'iğretileme',
    u'dinsel+Adj', u'(1,"toplumsal+Adj")', u'kişisel+Adj', u'tarihsel',
    u'çarpıcı+Adj', u'matematikçi+Noun+',   u'itici+',

    u'ikibin+Num',  # sacmalik!

    u'+Related', u'kavramsal', u'nesnel+Adj',
    u'+NotState',

    u'stoku+Noun+',      # Does optional voicing work? gotta create 2 stems like normal voicing case

    u'(1,"yak\u0131n+Noun+A3sg+Pnon+Loc")(2,"Adj+Rel")',
    u'yakın+Noun',
    u'yetkili+Noun', u'ilgili+Noun', u'köylü+Noun',
    u'(1,"ku\u015fkusuz+Adv")', u'(1,"s\xf6zgelimi+Adv")', u'(1,"mesela+Adv")', u'kimbilir+', u'(1,"sahi+Adv")', u'aslında+Adv', # "örneğin" var, ama o Conj
    u'(1,"siz+Pron+PersP+A2pl+Pnon+Gen")(2,"Pron+A3sg+Pnon+Nom")',      # sizinki ?

    # TODO: check languages like Ingilizce, Almanca, Turkce vs...
    u'(1,"ingilizce+Adj"',

    u'tümü+Pron',

    u'yeni+Adv',        # yeni yeni alismisti

    # TODO: think about taralı, kapali, takili vs
    # TODO: word tuerlue is used much different in various cases
    u't\xfcrl\xfc',

    u'b\xfct\xfcn\xfcyle+Adv', # tamamiyle, etc.

    u'kestirim+Noun', u'(1,"kazanımlar+Noun+A3sg+Pnon+Abl")',       # yapim, cizim, etc.
    u'nesi+Noun',
    u'dokun+Verb")(2,"Verb+Caus',
    u'kop+Verb")(2,"Verb+Caus',     # kopar
    u'(1,"sık+Verb")(2,"Verb+Recip")(3,"Verb+Caus")(4,"Verb+Pass+Pos+Narr+A3sg+Cop")',
    u'(1,"sistem+Noun+A3sg+Pnon+Nom")(2,"Verb+Become")(3,"Verb+Caus")(4,"Verb+Pass+Pos+Narr")(5,"Adj+Zero")',
    u'(1,"sistem+Noun+A3sg+Pnon+Nom")(2,"Verb+Become")(3,"Verb+Caus")(4,"Verb+Pass+Pos")(5,"Noun+Inf2+A3sg+P3sg+Nom")',
    u'(1,"doğ+Verb")(2,"Verb+Caus+Pos+Narr+A3sg+Cop")',
    u'(1,"hız+Noun+A3sg+Pnon+Nom")(2,"Verb+Become")(3,"Verb+Caus+Pos")(4,"Noun+Inf2+A3sg+Pnon+Nom")',
    u'ahali+Noun',
    u'tıpkı+Noun',
    u'salt+Adv',
    u'(1,"dokun+Verb+Pos")(2,"Adv+WithoutHavingDoneSo2")',
    u'gittik\xe7e+Adv',
    u'(1,"barış+Verb+Pos")(2,"Noun+Inf1+A3sg+Pnon+Loc")',

    u'Noun+Agt',
    u'(1,"ön+Noun+A3sg+Pnon+Nom")(2,"Adj+Agt")', u'(1,"art+Noun+A3sg+Pnon+Nom")(2,"Adj+Agt")',

    u'(1,"anlat+Verb")(2,"Verb+Able+Neg")(3,"Adv+WithoutHavingDoneSo1")'        # very complicated!

}

class ParserTestWithSimpleParseSets(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(ParserTestWithSimpleParseSets, cls).setUpClass()
        all_stems = []

        dictionary_items = DictionaryLoader.load_from_file(os.path.join(os.path.dirname(__file__), '../../resources/master_dictionary.txt'))
        for di in dictionary_items:
            all_stems.extend(CircumflexConvertingStemGenerator.generate(di))

        stem_root_map_generator = StemRootMapGenerator()
        cls.stem_root_map = stem_root_map_generator.generate(all_stems)

        suffix_graph = ExtendedSuffixGraph()
        predefined_paths = PredefinedPaths(cls.stem_root_map, suffix_graph)
        predefined_paths.create_predefined_paths()

        word_stem_finder = WordStemFinder(cls.stem_root_map)
        numeral_stem_finder = NumeralStemFinder()

        cls.parser = Parser(suffix_graph, predefined_paths, [word_stem_finder, numeral_stem_finder])

    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        parser_logger.setLevel(logging.INFO)
        suffix_applier_logger.setLevel(logging.INFO)

    def test_should_parse_simple_parse_set_001(self):
#        parser_logger.setLevel(logging.DEBUG)
#        suffix_applier_logger.setLevel(logging.DEBUG)
        self._test_should_parse_simple_parse_set("001")

    def test_should_parse_simple_parse_set_002(self):
#        parser_logger.setLevel(logging.DEBUG)
#        suffix_applier_logger.setLevel(logging.DEBUG)
        self._test_should_parse_simple_parse_set("002")

    def test_should_parse_simple_parse_set_003(self):
#        parser_logger.setLevel(logging.DEBUG)
#        suffix_applier_logger.setLevel(logging.DEBUG)
        self._test_should_parse_simple_parse_set("003")

    def test_should_parse_simple_parse_set_004(self):
#        parser_logger.setLevel(logging.DEBUG)
#        suffix_applier_logger.setLevel(logging.DEBUG)
        self._test_should_parse_simple_parse_set("004")

    def test_should_parse_simple_parse_set_005(self):
    #        parser_logger.setLevel(logging.DEBUG)
    #        suffix_applier_logger.setLevel(logging.DEBUG)
        self._test_should_parse_simple_parse_set("005")

    def _test_should_parse_simple_parse_set(self, set_number, start_index=0):
        path = os.path.join(os.path.dirname(__file__), '../../testresources/simpleparsesets/simpleparseset{}.txt'.format(set_number))
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
        for transition in result.get_transitions():
            if transition.from_state.type==State.DERIV:
                groups.append(current_group)
                current_group = [transition.to_state.pretty_name]
            else:
                pass

            if not isinstance(transition.suffix_form_application.suffix_form.suffix, FreeTransitionSuffix):
                current_group.append(transition.suffix_form_application.suffix_form.suffix.pretty_name)

        groups.append(current_group)

        root = result.get_stem().dictionary_item.root

        secondary_position_str = None

        ##TODO:
        if result.get_stem().dictionary_item.primary_position==PrimaryPosition.PRONOUN:
            if result.get_stem().dictionary_item.secondary_position==SecondaryPosition.PERSONAL:
                secondary_position_str = "PersP"
            elif result.get_stem().dictionary_item.secondary_position==SecondaryPosition.DEMONSTRATIVE:
                secondary_position_str = "DemonsP"
            elif result.get_stem().dictionary_item.secondary_position==SecondaryPosition.QUESTION:
                secondary_position_str = "QuesP"
            elif result.get_stem().dictionary_item.secondary_position==SecondaryPosition.REFLEXIVE:
                secondary_position_str = "ReflexP"

        if result.get_stem().dictionary_item.primary_position==PrimaryPosition.NUMERAL:
            if result.get_stem().dictionary_item.secondary_position==SecondaryPosition.CARD:
                secondary_position_str = "Card"
            elif result.get_stem().dictionary_item.secondary_position==SecondaryPosition.ORD:
                secondary_position_str = "Ord"
            elif result.get_stem().dictionary_item.secondary_position==SecondaryPosition.DIGITS:
                secondary_position_str = "Digits"


        if not groups:
            if not secondary_position_str:
                return u'({},"{}+{}")'.format(1, root, result.get_stem_state().pretty_name)
            else:
                return u'({},"{}+{}+{}")'.format(1, root, result.get_stem_state().pretty_name, secondary_position_str)



        return_value = None

        if not secondary_position_str:
            return_value = u'({},"{}+{}")'.format(1, root, result.get_stem_state().pretty_name)
        else:
            return_value = u'({},"{}+{}+{}")'.format(1, root, result.get_stem_state().pretty_name, secondary_position_str)

        if not groups[0]:
            if not secondary_position_str:
                return_value = u'({},"{}+{}")'.format(1, root, result.get_stem_state().pretty_name)
            else:
                return_value = u'({},"{}+{}+{}")'.format(1, root, result.get_stem_state().pretty_name, secondary_position_str)
        else:
            if not secondary_position_str:
                return_value = u'({},"{}+{}+{}")'.format(1, root, result.get_stem_state().pretty_name, u'+'.join(groups[0]))
            else:
                return_value = u'({},"{}+{}+{}+{}")'.format(1, root, result.get_stem_state().pretty_name, secondary_position_str, u'+'.join(groups[0]))


        for i in range(1, len(groups)):
            group = groups[i]
            return_value += u'({},"{}")'.format(i+1, u'+'.join(group))

        ##TODO:
        if any(c in CircumflexConvertingStemGenerator.Circumflex_Chars for c in return_value):
            for (cir, pla) in CircumflexConvertingStemGenerator.Circumflex_Letters_Map.iteritems():
                return_value = return_value.replace(cir, pla)

        ##TODO:
        if u'+Apos' in return_value:
            return_value = return_value.replace(u'+Apos', u'')

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
