# coding=utf-8
import codecs
import os
import unittest
from hamcrest.core.assert_that import assert_that
from hamcrest.core.core.isequal import equal_to
from trnltk.parser.parser import Parser
from trnltk.parseset.creator import ParseSetCreator
from trnltk.parser.stemfinder import NumeralStemFinder, WordStemFinder, ProperNounFromApostropheStemFinder, ProperNounWithoutApostropheStemFinder
from trnltk.stem.dictionaryitem import PrimaryPosition, SecondaryPosition
from trnltk.stem.dictionaryloader import DictionaryLoader
from trnltk.stem.stemgenerator import StemGenerator, StemRootMapGenerator, CircumflexConvertingStemGenerator
from trnltk.suffixgraph.predefinedpaths import PredefinedPaths
from trnltk.suffixgraph.suffixgraph import SuffixGraph
from trnltk.suffixgraph.suffixgraphmodel import State, FreeTransitionSuffix

END_OF_SENTENCE_MARKER = '#END#OF#SENTENCE#'

class ParseSetCreatorWithSimpleParsesetsTest(unittest.TestCase):

    def setUp(self):
        self.parseset_creator = ParseSetCreator()

        all_stems = []

        dictionary_items = DictionaryLoader.load_from_file(os.path.join(os.path.dirname(__file__), '../../resources/master_dictionary.txt'))
        for di in dictionary_items:
            all_stems.extend(StemGenerator.generate(di))

        stem_root_map = (StemRootMapGenerator()).generate(all_stems)

        suffix_graph = SuffixGraph()
        predefined_paths = PredefinedPaths(stem_root_map, suffix_graph)
        predefined_paths.create_predefined_paths()

        word_stem_finder = WordStemFinder(stem_root_map)
        numeral_stem_finder = NumeralStemFinder()
        proper_noun_from_apostrophe_stem_finder = ProperNounFromApostropheStemFinder()
        proper_noun_without_apostrophe_stem_finder = ProperNounWithoutApostropheStemFinder()

        self.parser = Parser(suffix_graph, predefined_paths,
            [word_stem_finder, numeral_stem_finder, proper_noun_from_apostrophe_stem_finder, proper_noun_without_apostrophe_stem_finder])

    def test_should_create_parseset_001(self):
        self._create_parseset_n("001")

    def _create_parseset_n(self, set_number):
        source_file_path = os.path.join(os.path.dirname(__file__), '../../testresources/simpleparsesets/simpleparseset{}.txt'.format(set_number))
        destination_file_path = os.path.join(os.path.dirname(__file__), '../../testresources/parsesets/parseset{}.xml'.format(set_number))

        sentences = []
        with codecs.open(source_file_path, mode='r', encoding='utf-8') as src:
            entries_for_sentence = []
            for line in src:
                if not line:
                    continue
                elif line.startswith(END_OF_SENTENCE_MARKER):
                    sentence_binding = self.parseset_creator.create_sentence_binding_from_tokens(entries_for_sentence)
                    sentences.append(sentence_binding)
                    entries_for_sentence = []
                elif line.startswith("#"):
                    continue
                else:
                    word_part = line[:line.find('=')].strip()
                    parse_result_part = line[line.find('=')+1:].strip()

                    parse_result_matching_simple_parseset = self._find_parse_result_matching_simple_parseset(word_part, parse_result_part)

                    entries_for_sentence.append((word_part, parse_result_matching_simple_parseset))

        with codecs.open(destination_file_path, mode='w', encoding='utf-8') as output:
            for sentence_binding in sentences:
                output.write(sentence_binding.to_dom().toprettyxml())


    def _find_parse_result_matching_simple_parseset(self, word_part, parse_result_part):
        parse_results = self.parser.parse(word_part)
        for parse_result in parse_results:
            if parse_result_part==self._parse_token_to_parse_set_str(parse_result):
                return parse_result

        return None


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
                secondary_position_str = "Pers"
            elif result.get_stem().dictionary_item.secondary_position==SecondaryPosition.DEMONSTRATIVE:
                secondary_position_str = "Demons"
            elif result.get_stem().dictionary_item.secondary_position==SecondaryPosition.QUESTION:
                secondary_position_str = "Ques"
            elif result.get_stem().dictionary_item.secondary_position==SecondaryPosition.REFLEXIVE:
                secondary_position_str = "Reflex"

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


if __name__ == '__main__':
    unittest.main()
