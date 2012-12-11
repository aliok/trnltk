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
import re
from trnltk.morphology.model.lexeme import SyntacticCategory
from trnltk.morphology.model.root import NumeralRoot, AbbreviationRoot, ProperNounRoot

class RootFinder(object):
    def find_roots_for_partial_input(self, partial_input, whole_surface=None):
        """
        @type partial_input: unicode
        @type whole_surface: unicode or None
        @rtype: list of Root
        """
        raise NotImplementedError()


class WordRootFinder(RootFinder):
    def __init__(self, lexeme_map):
        self.lexeme_map = lexeme_map

    def find_roots_for_partial_input(self, partial_input, whole_surface=None):
        """
        @type partial_input: unicode
        @type whole_surface: unicode or None
        @rtype: list of Root
        """
        if self.lexeme_map.has_key(partial_input):
            roots = self.lexeme_map[partial_input][:]
            return filter(lambda root: root.lexeme.syntactic_category != SyntacticCategory.NUMERAL, roots)
        else:
            return []


class TextNumeralRootFinder(RootFinder):
    def __init__(self, lexeme_map):
        self.lexeme_map = lexeme_map

    def find_roots_for_partial_input(self, partial_input, whole_surface=None):
        """
        @type partial_input: unicode
        @type whole_surface: unicode or None
        @rtype: list of Root
        """
        if self.lexeme_map.has_key(partial_input):
            roots = self.lexeme_map[partial_input][:]
            return filter(lambda root: root.lexeme.syntactic_category == SyntacticCategory.NUMERAL, roots)
        else:
            return []


class DigitNumeralRootFinder(RootFinder):
    NUMBER_REGEXES = [re.compile(u'^[-+]?\d+(,\d)?\d*$'), re.compile(u'^[-+]?(\d{1,3}\.)+\d{3}(,\d)?\d*$')]

    def find_roots_for_partial_input(self, partial_input, whole_surface=None):
        """
        @type partial_input: unicode
        @type whole_surface: unicode or None
        @rtype: list of Root
        """
        for regex in self.NUMBER_REGEXES:
            if regex.match(partial_input):
                return [NumeralRoot(partial_input)]

        return []


class ProperNounFromApostropheRootFinder(RootFinder):
    APOSTROPHE = u"'"

    def find_roots_for_partial_input(self, partial_input, whole_surface=None):
        """
        @type partial_input: unicode
        @type whole_surface: unicode or None
        @rtype: list of Root
        """
        if partial_input.endswith(self.APOSTROPHE):
            proper_noun_candidate = partial_input[:-1]
            if proper_noun_candidate:
                if proper_noun_candidate.isupper():
                    return [AbbreviationRoot(partial_input[:-1])]
                elif proper_noun_candidate[0].isupper():
                    return [ProperNounRoot(partial_input[:-1])]

        return []


class ProperNounWithoutApostropheRootFinder(RootFinder):
    APOSTROPHE = u"'"

    def find_roots_for_partial_input(self, partial_input, whole_surface=None):
        """
        @type partial_input: unicode
        @type whole_surface: unicode
        @rtype: list of Root
        """
        if whole_surface and self.APOSTROPHE in whole_surface:
            return []
        if not partial_input[0].isalpha() or not partial_input[0].isupper() or self.APOSTROPHE in partial_input:
            return []

        if partial_input == whole_surface and partial_input.isupper():
            return [AbbreviationRoot(partial_input)]

        # TODO: might be a known proper noun like "Turkce" or "Istanbul". no support for them yet

        # TODO: might be a known proper noun with implicit P3sg. like : Eminonu, Kusadasi.
        # it is important since :
        # 1. Ankara'_y_a but Eminonu'_n_e    : Since this case has apostrophe, it is handled in ProperNounFromApostropheRootFinder
        # 2: P3sg doesn't apply to these words: onun Kusadasi, onun Eminonu
        # 3. Possessions are applied to 'root' : benim Kusadam etc. SKIP this case!

        return [ProperNounRoot(partial_input)]