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
from __future__ import unicode_literals
from __future__ import division
import codecs
import logging
import os
import unittest
from hamcrest import *
from hamcrest.core.base_matcher import BaseMatcher
from trnltk.morphology.contextless.parser.test.parser_test import ParserTest
from trnltk.morphology.lexicon.lexiconloader import LexiconLoader
from trnltk.morphology.lexicon.rootgenerator import CircumflexConvertingRootGenerator, RootMapGenerator
from trnltk.morphology.model import formatter
from trnltk.morphology.morphotactics.basicsuffixgraph import BasicSuffixGraph
from trnltk.morphology.morphotactics.copulasuffixgraph import CopulaSuffixGraph
from trnltk.morphology.contextless.parser.parser import  logger as parser_logger, UpperCaseSupportingContextlessMorphologicalParser
from trnltk.morphology.contextless.parser.rootfinder import WordRootFinder, DigitNumeralRootFinder, TextNumeralRootFinder, ProperNounFromApostropheRootFinder, ProperNounWithoutApostropheRootFinder
from trnltk.morphology.contextless.parser.suffixapplier import logger as suffix_applier_logger
from trnltk.morphology.morphotactics.numeralsuffixgraph import NumeralSuffixGraph
from trnltk.morphology.morphotactics.predefinedpaths import PredefinedPaths

#TODO
from trnltk.morphology.morphotactics.propernounsuffixgraph import ProperNounSuffixGraph
from trnltk.morphology.phonetics.alphabet import TurkishAlphabet
cases_to_skip = {
    u'1+Num+Card',
    u'70+Num+Card',
    u'Num+Distrib',

    # sacmalik!
    u'ikibin+Num', u'sekizonikibindokuzyuzdoksansekiz', u'onsekiz', u'onyedi',
    u'doksandokuz', u'bindokuzyüzseksendokuz', u'onbirbindokuzyüzdoksansekiz',
    u'binyediyüzotuzdört', u'onbir',

    u'Verb+Reflex', u'Verb+Stay+',

    u'incecik+',        # Think about it!

    #
    u'_', u'+Prop', u'+Abbr+',

    u'Postp',
    u'biri+Pron',

    u'üzer+',
    u'üzeri',
    u'hiçbiri',

    u'â', u'î', u'û',

    # passives to be changed in treebank
    u'vurul+Verb', u'dikil',


    # add to master dictionary and check tb for usages
    u'önceleri', u'böylesine', u'sonraları',

    # not sure what to do
    u'şakalaş+Verb', u'önceden', u'böylesi',

    #
    u'ayırdet+Verb', u'elatma+Noun', u'varet', u'sözet', u'terket', u'yeral', u'sağol', u'terket', u'yolaç',

    #
    u'+A3pl+Past',    # yaparlardi
    u'+A3pl+Narr',    # yaparlarmis
    u'+A3pl+Cond',    # yapiyorsalar
    u'+Cop+A3pl',     # hazirdirlar <> hazirlardir , similarly for "Ques"s : midirler
    u'+A2pl+Cond',     # yapmadinizsa
    u'+A2sg+Cond',     # yaptinsa

    u'kadar',
    u'Postp',

    u'(1,"yıl+Noun+A3sg+Pnon+Nom")(2,"Adv+Since")', u'yıl+Noun+A3pl+Pnon+Nom")(2,"Adv+Since")', # yildir, yillardir

    # -sel
    u'dinsel+Adj', u'(1,"toplumsal+Adj")', u'kişisel+Adj', u'tarihsel', u'içgüdüsel',
    u'matematiksel', u'mantıksal', u'deneysel', u'gözlemsel', u'kimyasal',
    u'ereksel', u'nedensel', u'fiziksel', u'bütünsel', u'duygusal', u'ruhsal',
    u'kavramsal', u'nesnel+Adj', u'algısal', u'içsel', u'geleneksel', u'madensel',
    u'hukuksal', u'parasal',

    u'+Related',    # metodolojik, teknolojik, etc
    u'+NotState',

    u'stoku+Noun+',      # Does optional voicing work? gotta create 2 roots like normal voicing case

    u'yetkili+Noun', u'ilgili+Noun', u'köylü+Noun',

    # TODO: check languages like Ingilizce, Almanca, Turkce vs...
    u'(1,"ingilizce+Adj"',

    # TODO: think about taralı, kapali, takili vs
    u'yazılı', u'kapalı', u'takılı', u'taralı',

    # milletvekilleri, zeytinyaglari etc.
    u'milletvekil+Noun+A3pl',

    # sistemlesme, evlesme, mekanlasma
    u'+Noun+A3sg+Pnon+Nom")(2,"Verb+Become',

    # yapim, cizim, etc.
    u'kestirim', u'kazanım', u'kullanım', u'yapım', u'çizim', u'aşım', u'bileşim',

    # material used as adjective
    u'kadife+Adj', u'mermer+Adj', u'ipek+Adj',

    # çalı malı
    u'malı+Noun+',

    u'dokun+Verb")(2,"Verb+Caus',
    u'donan+Verb',
    u'(1,"dokun+Verb+Pos")(2,"Adv+WithoutHavingDoneSo2")',
    u'(1,"barış+Verb+Pos")(2,"Noun+Inf1+A3sg+Pnon+Loc")',

    u'(1,"kullanım+Noun+A3sg+Pnon+Nom")',

    u'(1,"anlat+Verb")(2,"Verb+Able+Neg")(3,"Adv+WithoutHavingDoneSo1")'        # very complicated!
}


words_to_skip={
    u'yapıyon', u'korkuyo', u'yakak',
    u'Hiiç', u'Giir', u'hii', u'Geeç', u'yo', u'Yoo', u'ööö',      # mark as "Arbitrary Interjection"
    u'Aaa', u'ham', u'aga', u'Eee',
    u'Börtü',
    u'eşşek',
    u'vb.', u'vb',

    # "beyin meyin kalmamisti"
    u'meyin', u'melektronik', u'mekonomi', u'mişletme', u'miçki', u'mumar', u'mefahat', u'moşku',
    u'mırık', u'meker',

    u'Dördü',
    u'çocuksu',

    # words ending with arabic "Ayn"
    u'mevzuu', u'camii', u'sanayii',

    # "until" suffix
    u'duyumsatıncaya', u'kızarıncaya', u'deyinceye',

    u'psikolog', u'antropolog'

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

        suffix_graph = CopulaSuffixGraph(NumeralSuffixGraph(ProperNounSuffixGraph(BasicSuffixGraph())))
        suffix_graph.initialize()

        predefined_paths = PredefinedPaths(cls.root_map, suffix_graph)
        predefined_paths.create_predefined_paths()

        word_root_finder = WordRootFinder(cls.root_map)
        text_numeral_root_finder = TextNumeralRootFinder(cls.root_map)
        digit_numeral_root_finder = DigitNumeralRootFinder()
        proper_noun_from_apostrophe_root_finder = ProperNounFromApostropheRootFinder()
        proper_noun_without_apostrophe_root_finder = ProperNounWithoutApostropheRootFinder()

        cls.parser = UpperCaseSupportingContextlessMorphologicalParser(suffix_graph, predefined_paths,
            [word_root_finder, text_numeral_root_finder, digit_numeral_root_finder,
             proper_noun_from_apostrophe_root_finder, proper_noun_without_apostrophe_root_finder])

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

    def test_should_parse_simple_parse_set_004_SLOW(self):
#        parser_logger.setLevel(logging.DEBUG)
#        suffix_applier_logger.setLevel(logging.DEBUG)
        self._test_should_parse_simple_parse_set("004")

    def test_should_parse_simple_parse_set_005_SLOW(self):
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
                        self.assert_parse_correct(word, index, parse_result)
                    except Exception:
                        unparsable +=1
                        logger.info(u'Unparsable : {} {} {}'.format(index, word, parse_result))
                else:
                    self.assert_parse_correct(TurkishAlphabet.lower(word), index, parse_result)

                index += 1

        if self.STATS_MODE:
            logger.info("Finished simple parse set {}".format(path))
            logger.info("Found {} lines, with {} lines of comments".format(index, comment))
            logger.info("Skipped {}, unparsable {}".format(skipped, unparsable))
            logger.info("Words that should be parsable : {}".format(index-comment))
            logger.info("Parse success rate : {}".format(float(index-comment-skipped-unparsable)/float(index-comment)))

    def assert_parse_correct(self, word_to_parse, index, *args):
        parse_result = self.parse_result(word_to_parse)
        assert_that(parse_result, IsParseResultMatches([a for a in args]), u'Error in word : {} at index {}'.format(repr(word_to_parse), index))

    def parse_result(self, word):
        return [formatter.format_morpheme_container_for_simple_parseset(r) for r in (self.parser.parse(word))]

class IsParseResultMatches(BaseMatcher):
    def __init__(self, expected_results):
        self.expected_results = expected_results

    def _matches(self, item):
        return all([expected_result in item for expected_result in self.expected_results])

    def describe_to(self, description):
        description.append_text(u'     ' + str(self.expected_results))

if __name__ == '__main__':
    unittest.main()
