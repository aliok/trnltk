# coding=utf-8
"""
There is no verification -yet- in test of this class.
The tests are there for making sure there is no run time exceptions
"""
import logging
from operator import itemgetter
import os
import unittest
from xml.dom.minidom import parse
import pymongo
from hamcrest import *
from mock import Mock
from trnltk.morphology.contextfree.parser.parser import ContextFreeMorphologicalParser
from trnltk.morphology.contextfree.parser.rootfinder import WordRootFinder, DigitNumeralRootFinder, ProperNounFromApostropheRootFinder, ProperNounWithoutApostropheRootFinder, TextNumeralRootFinder
from trnltk.morphology.model import formatter
from trnltk.morphology.morphotactics.basicsuffixgraph import BasicSuffixGraph
from trnltk.morphology.morphotactics.copulasuffixgraph import CopulaSuffixGraph
from trnltk.morphology.morphotactics.numeralsuffixgraph import NumeralSuffixGraph
from trnltk.morphology.morphotactics.predefinedpaths import PredefinedPaths
from trnltk.morphology.lexicon.lexiconloader import LexiconLoader
from trnltk.morphology.lexicon.rootgenerator import RootGenerator, RootMapGenerator
from trnltk.morphology.morphotactics.propernounsuffixgraph import ProperNounSuffixGraph
from trnltk.morphology.phonetics.alphabet import TurkishAlphabet
from trnltk.ngrams.ngramgenerator import WordNGramGenerator
from trnltk.parseset.xmlbindings import ParseSetBinding, UnparsableWordBinding
from trnltk.statistics.contextstats import  ContextParsingLikelihoodCalculator
from trnltk.statistics.contextstats import logger as context_stats_logger
from trnltk.statistics.query import logger as query_logger

class MockContainerBuilder(object):
    def __init__(self, surface_str, surface_syntactic_category, surface_secondary_syntactic_category=None):
        self.surface_str = surface_str
        self.surface_syntactic_category = surface_syntactic_category
        self.surface_secondary_syntactic_category = surface_secondary_syntactic_category
        self.stem_str = None
        self.stem_syntactic_category = None
        self.stem_secondary_syntactic_category = None
        self.lemma_root_str = None
        self.lemma_root_syntactic_category = None
        self.lemma_root_secondary_syntactic_category = None

    def stem(self, stem_str, stem_syntactic_category=None, stem_secondary_syntactic_category=None):
        self.stem_str = stem_str
        self.stem_syntactic_category = stem_syntactic_category
        self.stem_secondary_syntactic_category = stem_secondary_syntactic_category

        return self

    def lexeme(self, lemma_root_str, lemma_root_syntactic_category=None, lemma_root_secondary_syntactic_category=None):
        self.lemma_root_str = lemma_root_str
        self.lemma_root_syntactic_category = lemma_root_syntactic_category
        self.lemma_root_secondary_syntactic_category = lemma_root_syntactic_category

        return self

    def build(self):
        mock = Mock()

        mock.get_surface.return_value  = self.surface_str
        mock.get_surface_syntactic_category.return_value  = self.surface_syntactic_category
        mock.get_surface_secondary_syntactic_category.return_value = self.surface_secondary_syntactic_category

        mock.get_stem.return_value = self.stem_str if self.stem_str else self.surface_str
        mock.get_stem_syntactic_category.return_value = self.stem_syntactic_category if self.stem_syntactic_category else self.surface_syntactic_category
        mock.get_stem_secondary_syntactic_category.return_value = self.stem_secondary_syntactic_category if self.stem_syntactic_category else self.surface_secondary_syntactic_category

        mock.get_lemma_root.return_value = self.lemma_root_str if self.lemma_root_str else self.surface_str
        mock.get_lemma_root_syntactic_category.return_value = self.lemma_root_syntactic_category if self.lemma_root_syntactic_category else self.surface_syntactic_category
        mock.get_lemma_root_secondary_syntactic_category.return_value = self.lemma_root_secondary_syntactic_category if self.lemma_root_syntactic_category else self.surface_secondary_syntactic_category

        return mock

def _container_builder(surface_str, surface_syntactic_category, surface_secondary_syntactic_category=None):
    return MockContainerBuilder(surface_str, surface_syntactic_category, surface_secondary_syntactic_category)

class LikelihoodCalculatorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(LikelihoodCalculatorTest, cls).setUpClass()
        all_roots = []

        lexemes = LexiconLoader.load_from_file(os.path.join(os.path.dirname(__file__), '../../resources/master_dictionary.txt'))
        for di in lexemes:
            all_roots.extend(RootGenerator.generate(di))

        root_map_generator = RootMapGenerator()
        cls.root_map = root_map_generator.generate(all_roots)

        suffix_graph = CopulaSuffixGraph(NumeralSuffixGraph(ProperNounSuffixGraph(BasicSuffixGraph())))
        suffix_graph.initialize()

        predefined_paths = PredefinedPaths(cls.root_map, suffix_graph)
        predefined_paths.create_predefined_paths()

        word_root_finder = WordRootFinder(cls.root_map)
        digit_numeral_root_finder = DigitNumeralRootFinder()
        text_numeral_root_finder = TextNumeralRootFinder(cls.root_map)
        proper_noun_from_apostrophe_root_finder = ProperNounFromApostropheRootFinder()
        proper_noun_without_apostrophe_root_finder = ProperNounWithoutApostropheRootFinder()

        cls.context_free_parser = ContextFreeMorphologicalParser(suffix_graph, predefined_paths,
            [word_root_finder, digit_numeral_root_finder, text_numeral_root_finder,
             proper_noun_from_apostrophe_root_finder, proper_noun_without_apostrophe_root_finder])

    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        query_logger.setLevel(logging.INFO)
        context_stats_logger.setLevel(logging.INFO)

    def test_contextstats_with_parseset_001(self):
        self._test_contextstats_with_parseset_n("001")

    def test_contextstats_with_parseset_002(self):
        self._test_contextstats_with_parseset_n("002")

    def test_contextstats_with_parseset_003(self):
        self._test_contextstats_with_parseset_n("003")

    def test_contextstats_with_parseset_004(self):
        self._test_contextstats_with_parseset_n("004")

    def test_contextstats_with_parseset_005(self):
        self._test_contextstats_with_parseset_n("005")

    def test_contextstats_with_parseset_999(self):
        self._test_contextstats_with_parseset_n("999")

    def _test_contextstats_with_parseset_n(self, n):
        mongodb_connection = pymongo.Connection()
        self.collection_map = {
            1: mongodb_connection['trnltk']['wordUnigrams{}'.format(n)],
            2: mongodb_connection['trnltk']['wordBigrams{}'.format(n)],
            3: mongodb_connection['trnltk']['wordTrigrams{}'.format(n)]
        }

        self.generator = ContextParsingLikelihoodCalculator(self.collection_map)

        dom = parse(os.path.join(os.path.dirname(__file__), '../../testresources/parsesets/parseset{}.xml'.format(n)))
        parseset = ParseSetBinding.build(dom.getElementsByTagName("parseset")[0])
        self.parse_set_word_list = []
        for sentence in parseset.sentences:
            self.parse_set_word_list.extend(sentence.words)

        self._test_generate_likelihood_of_one_word_given_one_leading_context_word()

    def _generate_likelihood(self, surface, leading_context=None, following_context=None):
        assert leading_context or following_context

        likelihoods = []
        results = self.context_free_parser.parse(surface)
        if surface[0].isupper():
            results += self.context_free_parser.parse(TurkishAlphabet.lower(surface[0]) + surface[1:])

        for result in results:
            formatted_parse_result = formatter.format_morpheme_container_for_parseset(result)
            likelihood = 0.0
            if leading_context and following_context:
                likelihood = self.generator.calculate_likelihood(result, leading_context, following_context)
            elif leading_context:
                likelihood = self.generator.calculate_oneway_likelihood(result, leading_context, True)
            elif following_context:
                likelihood = self.generator.calculate_oneway_likelihood(result, following_context, False)

            likelihoods.append((formatted_parse_result, likelihood))

        return likelihoods

    def _test_generate_likelihood_of_one_word_given_one_leading_context_word(self):
#        query_logger.setLevel(logging.DEBUG)
#        context_stats_logger.setLevel(logging.DEBUG)

        for index,word in enumerate(self.parse_set_word_list):
            print u'Checking word {} {}'.format(index, word.str)
            if index==0:
                continue
            if isinstance(word, UnparsableWordBinding):
                print u'Word is unparsable, skipped'
                continue

            previous_word = self.parse_set_word_list[index-1]

            if isinstance(previous_word, UnparsableWordBinding):
                print u'Previous word is unparsable, skipped'
                continue

            surface_str, surface_syntactic_category = previous_word.str, previous_word.syntactic_category
            stem_str, stem_syntactic_category, stem_secondary_syntactic_category = WordNGramGenerator._get_stem(previous_word)
            lemma_root_str, lemma_root_syntactic_category = previous_word.root.lemma_root, previous_word.root.syntactic_category

            if previous_word.secondary_syntactic_category:
                surface_syntactic_category += u'_' + previous_word.secondary_syntactic_category
            if stem_secondary_syntactic_category:
                stem_syntactic_category += u'_' + stem_secondary_syntactic_category
            if previous_word.root.secondary_syntactic_category:
                lemma_root_syntactic_category += u'_' + previous_word.root.secondary_syntactic_category

            context = [[_container_builder(surface_str, surface_syntactic_category)
                        .stem(stem_str, stem_syntactic_category)
                        .lexeme(lemma_root_str, lemma_root_syntactic_category)
                        .build()]]

            surface = word.str
            likelihoods = self._generate_likelihood(surface=surface, leading_context=context, following_context=None)

            for item in likelihoods:
                print u'\t' + str(item)

            most_probable_parse_result = max(likelihoods, key=itemgetter(1))
            most_probable_parse_results = filter(lambda t : t[1]==most_probable_parse_result[1], likelihoods)
            print u'Most probable parse results are {}'.format(most_probable_parse_results)
            print u'Correct parse result is {}'.format(word.parse_result)
            if word.parse_result in [t[0] for t in most_probable_parse_results]:
                print u'Correct result is found in statistical parse results'
            else:
#                 self.fail(u'Correct result is NOT found in statistical parse results')
                print u'Correct result is NOT found in statistical parse results'

            print '\n'

if __name__ == '__main__':
    unittest.main()
