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
import os
from trnltk.morphology.contextless.parser.parser import ContextlessMorphologicalParser
from trnltk.morphology.contextless.parser.rootfinder import *
from trnltk.morphology.lexicon.lexiconloader import LexiconLoader
from trnltk.morphology.lexicon.rootgenerator import CircumflexConvertingRootGenerator, RootMapGenerator
from trnltk.morphology.model import formatter
from trnltk.morphology.morphotactics.basicsuffixgraph import BasicSuffixGraph
from trnltk.morphology.morphotactics.copulasuffixgraph import CopulaSuffixGraph
from trnltk.morphology.morphotactics.numeralsuffixgraph import NumeralSuffixGraph
from trnltk.morphology.morphotactics.predefinedpaths import PredefinedPaths
from trnltk.morphology.morphotactics.propernounsuffixgraph import ProperNounSuffixGraph


contextless_parser = None

def initialize():
    all_roots = []
    lexemes = LexiconLoader.load_from_file(os.path.join(os.path.dirname(__file__), '../resources/master_dictionary.txt'))
    for di in lexemes:
        all_roots.extend(CircumflexConvertingRootGenerator.generate(di))

    root_map_generator = RootMapGenerator()
    root_map = root_map_generator.generate(all_roots)

    suffix_graph = CopulaSuffixGraph(NumeralSuffixGraph(ProperNounSuffixGraph(BasicSuffixGraph())))
    suffix_graph.initialize()

    predefined_paths = PredefinedPaths(root_map, suffix_graph)
    predefined_paths.create_predefined_paths()

    word_root_finder = WordRootFinder(root_map)
    text_numeral_root_finder = TextNumeralRootFinder(root_map)
    digit_numeral_root_finder = DigitNumeralRootFinder()
    proper_noun_from_apostrophe_root_finder = ProperNounFromApostropheRootFinder()
    proper_noun_without_apostrophe_root_finder = ProperNounWithoutApostropheRootFinder()

    global contextless_parser
    contextless_parser = ContextlessMorphologicalParser(suffix_graph, predefined_paths,
        [word_root_finder, text_numeral_root_finder, digit_numeral_root_finder,
         proper_noun_from_apostrophe_root_finder, proper_noun_without_apostrophe_root_finder])

initialize()

def parse_contextless(word_str, *syntactic_categories):
    if not isinstance(word_str, unicode) and isinstance(word_str, str):
        word_str = word_str.decode('utf-8')

    parse_results = contextless_parser.parse(word_str)
    if syntactic_categories:
        parse_results = filter(lambda parse_result: parse_result.get_last_state().syntactic_category in syntactic_categories, parse_results)

    if not parse_results:
        print u'No parse result found'
    else:
        for parse_result in parse_results:
            formatted_output = formatter.format_morpheme_container_for_tests(parse_result)
            if formatted_output.endswith(u'Verb+Zero+Pres+A3sg'):
                continue
            else:
                print formatted_output

# yapacagimi, yapacagimi -> true
def concordance_full_word(full_word, syntactic_category=None, secondary_syntactic_category=None):
    pass

# kitabimi, kitab -> true
def concordance_root(root, syntactic_category=None, secondary_syntactic_category=None):
    pass

# kitabimi, kitap -> true
def concordance_lemma(lemma, syntactic_category=None, secondary_syntactic_category=None):
    pass

# yapacagimi, yapacak -> true
def concordance_transition_word(transition_word, syntactic_category=None, secondary_syntactic_category=None):
    pass

# yapacagimi, yapacag => true
def concordance_transition_matched_word(transition_matched_word, syntactic_category=None, secondary_syntactic_category=None):
    pass



def print_concordance(word_list, offsets, width=75, lines=25):
    if offsets:
        half_width = (width - len(word_list[offsets[0]].str) - 2) / 2
        context = width/4 # approx number of words of context

        lines = min(lines, len(offsets))
        print "Displaying %s of %s matches:" % (lines, len(offsets))
        for i in offsets:
            if lines <= 0:
                break
            left = (' ' * half_width +
                    ' '.join([word.str for word in word_list[i-context:i]]))
            right = ' '.join([word.str for word in word_list[i+1:i+context]])
            word = word_list[i].str
            left = left[-half_width:]
            right = right[:half_width]
            sum = left + u' ' + word + u' ' + right
            sum = sum[0:width] if len(sum)>=width else sum
            print sum
            lines -= 1
    else:
        print "No matches"