# coding=utf-8
import os
import pymongo
from trnltk.morphology.contextful.variantcontiguity.calculator import InMemoryCachingContextParsingLikelihoodCalculator
from trnltk.morphology.contextless.parser.parser import ContextlessMorphologicalParser, UpperCaseSupportingContextlessMorphologicalParser
from trnltk.morphology.contextless.parser.rootfinder import ProperNounWithoutApostropheRootFinder, ProperNounFromApostropheRootFinder, WordRootFinder, DigitNumeralRootFinder, TextNumeralRootFinder
from trnltk.morphology.learner.controller.learnercontroller import ParseContextCreator
from trnltk.morphology.learner.dbmanager.dbmanager import DbManager
from trnltk.morphology.lexicon.lexiconloader import LexiconLoader
from trnltk.morphology.lexicon.rootgenerator import RootGenerator, RootMapGenerator
from trnltk.morphology.morphotactics.basicsuffixgraph import BasicSuffixGraph
from trnltk.morphology.morphotactics.copulasuffixgraph import CopulaSuffixGraph
from trnltk.morphology.morphotactics.numeralsuffixgraph import NumeralSuffixGraph
from trnltk.morphology.morphotactics.predefinedpaths import PredefinedPaths
from trnltk.morphology.morphotactics.propernounsuffixgraph import ProperNounSuffixGraph

class ApplicationContext(object):
    # some parameters
    PARSESET_INDEX = "999"      # this is the id of the knowledge ngrams collections
    DB_HOST = '127.0.0.1'

    def __init__(self):
        all_roots = []

        lexemes = LexiconLoader.load_from_file(os.path.join(os.path.dirname(__file__), '../../../resources/master_dictionary.txt'))
        for di in lexemes:
            all_roots.extend(RootGenerator.generate(di))

        root_map_generator = RootMapGenerator()
        root_map = root_map_generator.generate(all_roots)

        suffix_graph = CopulaSuffixGraph(NumeralSuffixGraph(ProperNounSuffixGraph(BasicSuffixGraph())))
        suffix_graph.initialize()

        predefined_paths = PredefinedPaths(root_map, suffix_graph)
        predefined_paths.create_predefined_paths()

        word_root_finder = WordRootFinder(root_map)
        digit_numeral_root_finder = DigitNumeralRootFinder()
        text_numeral_root_finder = TextNumeralRootFinder(root_map)
        proper_noun_from_apostrophe_root_finder = ProperNounFromApostropheRootFinder()
        proper_noun_without_apostrophe_root_finder = ProperNounWithoutApostropheRootFinder()

        mongodb_connection = pymongo.Connection(host=ApplicationContext.DB_HOST)

        self.contextless_morphological_parser = UpperCaseSupportingContextlessMorphologicalParser(suffix_graph, predefined_paths,
            [word_root_finder, digit_numeral_root_finder, text_numeral_root_finder,
             proper_noun_from_apostrophe_root_finder, proper_noun_without_apostrophe_root_finder])

        self.dbmanager = DbManager(mongodb_connection)

        self.likelihood_calculator = self._create_likelihood_calculator(mongodb_connection)

        self.parse_context_creator = ParseContextCreator(self.contextless_morphological_parser)

        self.sessions = {}

    @classmethod
    def _create_likelihood_calculator(cls, mongodb_connection):
        collection_map = {
            1: mongodb_connection['trnltk']['wordUnigrams{}'.format(ApplicationContext.PARSESET_INDEX)],
            2: mongodb_connection['trnltk']['wordBigrams{}'.format(ApplicationContext.PARSESET_INDEX)],
            3: mongodb_connection['trnltk']['wordTrigrams{}'.format(ApplicationContext.PARSESET_INDEX)]
        }

        return InMemoryCachingContextParsingLikelihoodCalculator(collection_map)


application_context_instance = ApplicationContext()