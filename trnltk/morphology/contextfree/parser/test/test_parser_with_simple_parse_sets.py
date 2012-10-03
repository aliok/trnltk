from __future__ import unicode_literals
# coding=utf-8
import codecs
import logging
import os
import unittest
from hamcrest import *
from hamcrest.core.base_matcher import BaseMatcher
from trnltk.morphology.contextfree.parser.test.parser_test import ParserTest
from trnltk.morphology.lexicon.lexiconloader import LexiconLoader
from trnltk.morphology.lexicon.rootgenerator import CircumflexConvertingRootGenerator, RootMapGenerator
from trnltk.morphology.model import formatter
from trnltk.morphology.morphotactics.extendedsuffixgraph import ExtendedSuffixGraph
from trnltk.morphology.contextfree.parser.parser import ContextFreeMorphologicalParser, logger as parser_logger
from trnltk.morphology.contextfree.parser.rootfinder import WordRootFinder, NumeralRootFinder
from trnltk.morphology.contextfree.parser.suffixapplier import logger as suffix_applier_logger
from trnltk.morphology.morphotactics.predefinedpaths import PredefinedPaths

#TODO
from trnltk.morphology.phonetics.alphabet import TurkishAlphabet
cases_to_skip = {
    u'1+Num+Card',
    u'70+Num+Card',
    u'Num+Distrib',

    u'Verb+Reflex',

    u'incecik+',        # Think about it!

    u'birşey+Noun',        # Must be pron!

    u'_',
    u'+Prop',
    u'+Abbr+',

    u'Postp',
    u'biri+Pron',

    u'üzer+',
    u'üzeri',
    u'hiçbiri',

    u'â', u'î',
    u'sanayi+Noun',

    # diyerek, yiyerek
    u'(1,"de+Verb+Pos")(2,"Adv+ByDoingSo")', u'(1,"ye+Verb+Pos")(2,"Adv+ByDoingSo")',
    # diyecek, yiyecek,
    u'de+Verb+Pos+Fut+', u'ye+Verb+Pos+Fut+',
    # diyemez, diyemezdim, yiyemez, yiyemezdim
    u'(1,"de+Verb")(2,"Verb+Able+Neg+Aor', u'(1,"ye+Verb")(2,"Verb+Able+Neg+Aor',

    # passives to be changed in treebank
    u'vurul+Verb', u'dikil',


    # add to master dictionary and check tb for usages
    u'önceleri', u'böylesine', u'yenik',

    # not sure what to do
    u'şakalaş+Verb', u'önceden', u'böylesi',

    #
    u'ayırdet+Verb', u'elatma+Noun', u'varet', u'sözet',

    #
    u'A3pl+Past',    # yaparlardi
    u'Prog+A3pl+Cond'     # yapiyorsalar
    u'+Cop+A3pl',         # hazirdirlar <> hazirlardir , similarly for "Ques"s : midirler

    u'kadar',
    u'(1,"değil+Conj")',
    u'Postp',
    u'içeri',
    u'yaşa+Verb+Neg+Past+A2pl+Cond"',
    u'(1,"boğul+Verb+Pos")',

    u'sonraları+Adv',      # aksamlari, geceleri, vs...
    u'(1,"yıl+Noun+A3sg+Pnon+Nom")(2,"Adv+Since")', u'yıl+Noun+A3pl+Pnon+Nom")(2,"Adv+Since")',
    u'hiçlik+Noun', u'gençlik+Noun', u'ayrılık+Noun', u'aracılık',
    u'birçok+Det',
    u'iğretileme',

    u'dinsel+Adj', u'(1,"toplumsal+Adj")', u'kişisel+Adj', u'tarihsel', u'içgüdüsel', u'matematiksel', u'mantıksal', u'deneysel', u'gözlemsel',
    u'ereksel', u'nedensel', u'fiziksel', u'bütünsel',

    u'çarpıcı+Adj', u'matematikçi+Noun+',   u'itici+', u'inandırıcı',

    # sacmalik!
    u'ikibin+Num', u'sekizonikibindokuzyuzdoksansekiz', u'onsekiz', u'onyedi',
    u'doksandokuz', u'bindokuzyüzseksendokuz', u'onbirbindokuzyüzdoksansekiz',
    u'binyediyüzotuzdört', u'onbir',

    u'+Related', u'kavramsal', u'nesnel+Adj', u'algısal', u'içsel',
    u'+NotState',

    u'stoku+Noun+',      # Does optional voicing work? gotta create 2 roots like normal voicing case

    u'(1,"yakın+Noun+A3sg+Pnon+Loc")(2,"Adj+PointQual")',
    u'yakın+Noun',
    u'yetkili+Noun', u'ilgili+Noun', u'köylü+Noun',

    u'(1,"siz+Pron+Pers+A2pl+Pnon+Gen")(2,"Pron+A3sg+Pnon+Nom")',      # sizinki ?
    u'(1,"bugün+Noun+A3sg+Pnon+Nom")(2,"Adj+PointQual")',
    u'bura+',

    # TODO: check languages like Ingilizce, Almanca, Turkce vs...
    u'(1,"ingilizce+Adj"',

    u'tümü+Pron',

    # TODO: think about taralı, kapali, takili vs
    # TODO: word tuerlue is used much different in various cases
    u'türlü',


    u'kestirim+Noun', u'(1,"kazanımlar+Noun+A3sg+Pnon+Abl")',       # yapim, cizim, etc.
    u'nesi+Noun',
    u'dokun+Verb")(2,"Verb+Caus',
    u'kop+Verb")(2,"Verb+Caus',     # kopar
    u'(1,"sık+Verb")(2,"Verb+Recip")(3,"Verb+Caus")(4,"Verb+Pass+Pos+Narr+A3sg+Cop")',
    u'(1,"\xf6t+Verb")(2,"Verb+Caus+Pos")',
    u'(1,"sistem+Noun+A3sg+Pnon+Nom")(2,"Verb+Become")(3,"Verb+Caus")',
    u'(1,"doğ+Verb")(2,"Verb+Caus+Pos+Narr+A3sg+Cop")',
    u'(1,"hız+Noun+A3sg+Pnon+Nom")(2,"Verb+Become")(3,"Verb+Caus+Pos")(4,"Noun+Inf2+A3sg+Pnon+Nom")',
    u'ahali+Noun',
    u'(1,"dokun+Verb+Pos")(2,"Adv+WithoutHavingDoneSo2")',
    u'donan+Verb',
    u'(1,"barış+Verb+Pos")(2,"Noun+Inf1+A3sg+Pnon+Loc")',

    u'var+', u'yok+', u'tamam+Adv', u'evet+', u'hayır',         # Part or Adv?

    u'(1,"kullanım+Noun+A3sg+Pnon+Nom")',

    u'(1,"anlat+Verb")(2,"Verb+Able+Neg")(3,"Adv+WithoutHavingDoneSo1")'        # very complicated!
}


words_to_skip={
    u'yapıyon', u'korkuyo',
    u'Hiiç', u'Giir', u'hii', u'Geeç',      # mark as "Arbitrary Interjection"
    u'Aaa', u'ham', u'aga', u'Eee',
    u'Börtü',
    u'eşşek',
    u'vb.', u'vb',
    u'meyin',   # "beyin meyin kalmamisti"

    u'yiyecek',
    u'Dördü',
    u'çocuksu',
}

logger = logging.getLogger('parser')

class ParserTestWithSimpleParseSets(ParserTest):
    STATS_MODE=True
    LOG_SKIPPED=False

    @classmethod
    def setUpClass(cls):
        super(ParserTestWithSimpleParseSets, cls).setUpClass()
        all_roots = []

        lexemes = LexiconLoader.load_from_file(os.path.join(os.path.dirname(__file__), '../../../../resources/master_dictionary.txt'))
        for di in lexemes:
            all_roots.extend(CircumflexConvertingRootGenerator.generate(di))

        root_map_generator = RootMapGenerator()
        cls.root_map = root_map_generator.generate(all_roots)

        suffix_graph = ExtendedSuffixGraph()
        predefined_paths = PredefinedPaths(cls.root_map, suffix_graph)
        predefined_paths.create_predefined_paths()

        word_root_finder = WordRootFinder(cls.root_map)
        numeral_root_finder = NumeralRootFinder()

        cls.parser = ContextFreeMorphologicalParser(suffix_graph, predefined_paths, [word_root_finder, numeral_root_finder])

    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        parser_logger.setLevel(logging.INFO)
        suffix_applier_logger.setLevel(logging.INFO)
        logger.setLevel(logging.INFO)

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

#    def test_should_parse_simple_parse_set_999(self):
#    #        parser_logger.setLevel(logging.DEBUG)
#    #        suffix_applier_logger.setLevel(logging.DEBUG)
#        self._test_should_parse_simple_parse_set("999")

    def _test_should_parse_simple_parse_set(self, set_number, start_index=0):
        path = os.path.join(os.path.dirname(__file__), '../../../../testresources/simpleparsesets/simpleparseset{}.txt'.format(set_number))
        logger.info("Parsing simple parse set {}".format(path))
        skipped = 0
        unparsable = 0
        comment = 0
        with codecs.open(path, 'r', 'utf-8-sig') as parse_set_file:
            index = 0
            for line in parse_set_file:
                if start_index>index:
                    index +=1
                    continue

                if line.startswith('#'):
                    comment +=1
                    index +=1
                    continue

                line = line.strip()
                (word, parse_result) = line.split('=')
                if any([case_to_skip in parse_result for case_to_skip in cases_to_skip]) or word in words_to_skip:
                    if self.LOG_SKIPPED:
                        logger.info(u'Skipped : {} {} {}'.format(index, word, parse_result))
                    skipped +=1
                    index +=1
                    continue

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

                if self.STATS_MODE:
                    try:
                        self.assert_parse_correct(lower(word), index, parse_result)
                    except:
                        unparsable +=1
                        logger.info(u'Unparsable : {} {} {}'.format(index, word, parse_result))
                else:
                    self.assert_parse_correct(lower(word), index, parse_result)

                index += 1

        if self.STATS_MODE:
            logger.info("Finished simple parse set {}".format(path))
            logger.info("Found {} lines, with {} lines of comments".format(index, comment))
            logger.info("Skipped {}, unparsable {}".format(skipped, unparsable))
            logger.info("Words that should be parsable : {}".format(index-comment))
            logger.info("Parse success rate : {}".format(float(index-comment-skipped-unparsable)/float(index-comment)))

    def assert_parse_correct(self, word_to_parse, index, *args):
        assert_that(self.parse_result(word_to_parse), IsParseResultMatches([a for a in args]), u'Error in word : {} at index {}'.format(repr(word_to_parse), index))

    def parse_result(self, word):
        return [formatter.format_morpheme_container_for_simple_parseset(r) for r in (self.parser.parse(word))]

class IsParseResultMatches(BaseMatcher):
    def __init__(self, expected_results):
        self.expected_results = expected_results

    def _matches(self, item):
        return all([expected_result in item for expected_result in self.expected_results])

    def describe_to(self, description):
        description.append_text(u'     ' + str(self.expected_results))

def lower(word):
    if not word:
        return word
    lower_word = u''
    for c in word:
        if c.isupper():
            letter_for_upper_char = TurkishAlphabet.get_letter_for_upper_case_char(c)
            if letter_for_upper_char:
                lower_word += letter_for_upper_char.char_value
            else:
                lower_word += letter_for_upper_char.lower()
        else:
            lower_word += c.lower()

    return lower_word

if __name__ == '__main__':
    unittest.main()
