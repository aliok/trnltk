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
from trnltk.morphology.contextful.likelihoodmetrics.contextlessdistribution.contextlessdistributioncalculator import ContextlessDistributionCalculator
from trnltk.morphology.contextful.likelihoodmetrics.contextlessdistribution.contextlessdistributionsmoother import CachedContextlessDistributionSmoother
from trnltk.morphology.contextful.likelihoodmetrics.hidden.database import DatabaseIndexBuilder
from trnltk.morphology.contextful.likelihoodmetrics.hidden.targetformgivencontextcounter import InMemoryCachingTargetFormGivenContextCounter
from trnltk.morphology.contextful.likelihoodmetrics.wordformcollocation.contextparsingcalculator import ContextParsingLikelihoodCalculator
from trnltk.morphology.contextful.likelihoodmetrics.wordformcollocation.interpolatingcalculator import InterpolatingLikelihoodCalculator
from trnltk.morphology.contextful.likelihoodmetrics.wordformcollocation.ngramfrequencysmoother import CachedSimpleGoodTuringNGramFrequencySmoother
from trnltk.morphology.contextful.parser.contextfullikelihoodcalculator import ContextfulLikelihoodCalculator
from trnltk.morphology.contextful.parser.sequencelikelihoodcalculator import SequenceLikelihoodCalculator
from trnltk.morphology.contextless.parser.parser import UpperCaseSupportingContextlessMorphologicalParser
from trnltk.morphology.contextless.parser.rootfinder import WordRootFinder, DigitNumeralRootFinder, TextNumeralRootFinder, ProperNounFromApostropheRootFinder, ProperNounWithoutApostropheRootFinder
from trnltk.morphology.lexicon.lexiconloader import LexiconLoader
from trnltk.morphology.lexicon.rootgenerator import RootGenerator, RootMapGenerator
from trnltk.morphology.morphotactics.basicsuffixgraph import BasicSuffixGraph
from trnltk.morphology.morphotactics.copulasuffixgraph import CopulaSuffixGraph
from trnltk.morphology.morphotactics.numeralsuffixgraph import NumeralSuffixGraph
from trnltk.morphology.morphotactics.predefinedpaths import PredefinedPaths
from trnltk.morphology.morphotactics.propernounsuffixgraph import ProperNounSuffixGraph

class ContextfulMorphologicalParser(object):
    def __init__(self, contextless_parser, contextful_likelihood_calculator):
        """
        @type contextless_parser: ContextlessMorphologicalParser
        @type contextful_likelihood_calculator: ContextfulLikelihoodCalculator
        """
        self._contextless_parser = contextless_parser
        self._contextful_likelihood_calculator = contextful_likelihood_calculator

    def build_indexes(self):
        self._contextful_likelihood_calculator.build_indexes()

    def parse_with_likelihoods(self, target_surface, leading_context, following_context, calculation_context=None):
        """
        @type target_surface: str or unicode
        @type leading_context: list<list<MorphemeContainer>>
        @type following_context: list<list<MorphemeContainer>>
        @type calculation_context: dict
        """
        target_parse_results = self._contextless_parser.parse(target_surface)

        if not target_parse_results:
            return None
        else:
            likelihoods = []
            for index, target_parse_result in enumerate(target_parse_results):
                item_calculation_context = {} if calculation_context is not None else None

                likelihood_for_item = self._contextful_likelihood_calculator.calculate_likelihood(target_parse_result,
                    leading_context, following_context,
                    item_calculation_context)
                likelihoods.append((target_parse_result, likelihood_for_item))

                if item_calculation_context:
                    calculation_context[index] = item_calculation_context

            return likelihoods


class ContextfulMorphologicalParserFactory(object):
    @classmethod
    def create(cls, master_dictionary_path, ngram_collection_map):
        """
        @type master_dictionary_path: str or unicode
        @param ngram_collection_map: list<Collection>
        @rtype ContextfulMorphologicalParser
        """
        all_roots = []

        lexemes = LexiconLoader.load_from_file(master_dictionary_path)
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

        contextless_parser = UpperCaseSupportingContextlessMorphologicalParser(suffix_graph, predefined_paths,
            [word_root_finder, digit_numeral_root_finder, text_numeral_root_finder,
             proper_noun_from_apostrophe_root_finder, proper_noun_without_apostrophe_root_finder])

        database_index_builder = DatabaseIndexBuilder(ngram_collection_map)
        target_form_given_context_counter = InMemoryCachingTargetFormGivenContextCounter(ngram_collection_map)
        ngram_frequency_smoother = CachedSimpleGoodTuringNGramFrequencySmoother()
        sequence_likelihood_calculator = SequenceLikelihoodCalculator(None)

        collocation_metric_calculator = ContextParsingLikelihoodCalculator(database_index_builder,
            target_form_given_context_counter, ngram_frequency_smoother,
            sequence_likelihood_calculator)

        interpolating_collocation_metric_calculator = InterpolatingLikelihoodCalculator(collocation_metric_calculator)

        cached_contextless_distribution_smoother = CachedContextlessDistributionSmoother()
        contextless_distribution_metric_calculator = ContextlessDistributionCalculator(database_index_builder,
            target_form_given_context_counter, cached_contextless_distribution_smoother)

        contextful_likelihood_calculator = ContextfulLikelihoodCalculator(interpolating_collocation_metric_calculator,
            contextless_distribution_metric_calculator)

        sequence_likelihood_calculator._contextful_likelihood_calculator = contextful_likelihood_calculator

        contextful_morphological_parser = ContextfulMorphologicalParser(contextless_parser,
            contextful_likelihood_calculator)

        return contextful_morphological_parser
