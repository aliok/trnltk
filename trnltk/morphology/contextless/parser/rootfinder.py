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
from trnltk.morphology.model.lexeme import SyntacticCategory, DynamicLexeme, LexemeAttribute
from trnltk.morphology.model.root import NumeralRoot, AbbreviationRoot, ProperNounRoot, DynamicRoot
from trnltk.morphology.phonetics.alphabet import TurkishAlphabet
from trnltk.morphology.phonetics.phonetics import Phonetics, PhoneticAttributes

class RootFinder(object):
    def find_roots_for_partial_input(self, partial_input, whole_surface):
        """
        @type partial_input: unicode
        @type whole_surface: unicode
        @rtype: list of Root
        """
        raise NotImplementedError()


class WordRootFinder(RootFinder):
    def __init__(self, lexeme_map):
        self.lexeme_map = lexeme_map

    def find_roots_for_partial_input(self, partial_input, whole_surface):
        """
        @type partial_input: unicode
        @type whole_surface: unicode
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

    def find_roots_for_partial_input(self, partial_input, whole_surface):
        """
        @type partial_input: unicode
        @type whole_surface: unicode
        @rtype: list of Root
        """
        if self.lexeme_map.has_key(partial_input):
            roots = self.lexeme_map[partial_input][:]
            return filter(lambda root: root.lexeme.syntactic_category == SyntacticCategory.NUMERAL, roots)
        else:
            return []


class DigitNumeralRootFinder(RootFinder):
    NUMBER_REGEXES = [re.compile(u'^[-+]?\d+(,\d)?\d*$'), re.compile(u'^[-+]?(\d{1,3}\.)+\d{3}(,\d)?\d*$')]

    def find_roots_for_partial_input(self, partial_input, whole_surface):
        """
        @type partial_input: unicode
        @type whole_surface: unicode
        @rtype: list of Root
        """
        for regex in self.NUMBER_REGEXES:
            if regex.match(partial_input):
                return [NumeralRoot(partial_input)]

        return []


class ProperNounFromApostropheRootFinder(RootFinder):
    APOSTROPHE = u"'"

    def find_roots_for_partial_input(self, partial_input, whole_surface):
        """
        @type partial_input: unicode
        @type whole_surface: unicode
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

    def find_roots_for_partial_input(self, partial_input, whole_surface):
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


class BruteForceNounRootFinder(RootFinder):
    def find_roots_for_partial_input(self, partial_input, whole_surface):
        """
        @type partial_input: unicode
        @type whole_surface: unicode
        @rtype: list of Root
        """
        assert partial_input and whole_surface
        assert len(partial_input) <= len(whole_surface)

        root = partial_input
        lemma = root
        lemma_root = lemma
        syntactic_category = SyntacticCategory.NOUN
        secondary_syntactic_category = None
        lexeme_attributes = set()

        lexeme = DynamicLexeme(lemma, lemma_root, syntactic_category, secondary_syntactic_category,
            lexeme_attributes)

        phonetic_expectations = set()
        phonetic_attributes = set()

        no_orthographics_root = DynamicRoot(root, lexeme, phonetic_expectations, phonetic_attributes)

        if whole_surface == partial_input or len(partial_input) < 2:
            return [no_orthographics_root]

        last_vowel = Phonetics.get_last_vowel(partial_input)

        if not last_vowel:
            return [no_orthographics_root]

        last_char = partial_input[-1]
        first_char_after_partial_input = whole_surface[len(partial_input)]
        if last_char.isupper() or first_char_after_partial_input.isupper():
            return [no_orthographics_root]

        roots = self._get_voicing_and_doubling_roots(partial_input, last_char, first_char_after_partial_input,
            no_orthographics_root)

        first_vowel_letter_after_partial_input = self._get_first_vowel(whole_surface[len(partial_input) - 1:])
        if first_vowel_letter_after_partial_input:
            if last_vowel.frontal != first_vowel_letter_after_partial_input.frontal:
                for r in roots:
                    r.lexeme.attributes = set(r.lexeme.attributes)
                    r.lexeme.attributes.add(LexemeAttribute.InverseHarmony)

        return roots

    def _get_voicing_and_doubling_roots(self, partial_input, last_char, first_char_after_partial_input,
                                        no_orthographics_root):
        last_letter = TurkishAlphabet.get_letter_for_char(last_char)
        first_letter_after_partial_input = TurkishAlphabet.get_letter_for_char(first_char_after_partial_input)

        no_voicing_rule_applies = last_letter in TurkishAlphabet.Voicing_Map and first_letter_after_partial_input.vowel
        voicing_might_have_happened = last_letter in TurkishAlphabet.Inverse_Voicing_Map and first_letter_after_partial_input.vowel
        doubling_might_have_happened = len(partial_input) > 2 and\
                                       not last_letter.vowel and\
                                       partial_input[-1] == partial_input[-2] and\
                                       first_letter_after_partial_input.vowel

        if doubling_might_have_happened:
            if no_voicing_rule_applies:
                doubling_root = self._create_doubling_root(no_orthographics_root, last_char)
                no_orthographics_root.lexeme.attributes = {LexemeAttribute.NoVoicing}
                doubling_root.lexeme.attributes.add(LexemeAttribute.NoVoicing)
                return [no_orthographics_root, doubling_root]
            elif voicing_might_have_happened:
                inverse_devoicing_roots = self._inverse_devoice_last_letter(no_orthographics_root, last_letter)
                devoicing_doubling_roots = [self._create_doubling_root(r, r.lexeme.root[-1]) for r in inverse_devoicing_roots]
                doubling_root = self._create_doubling_root(no_orthographics_root, last_char)
                return [no_orthographics_root] + [doubling_root] + devoicing_doubling_roots
            else:
                return [no_orthographics_root] + [self._create_doubling_root(no_orthographics_root, last_char)]
        else:
            if no_voicing_rule_applies:
                no_orthographics_root.lexeme.attributes = {LexemeAttribute.NoVoicing}
                return [no_orthographics_root]
            elif voicing_might_have_happened:
                return [no_orthographics_root] + self._inverse_devoice_last_letter(no_orthographics_root, last_letter)
            else:
                return [no_orthographics_root]

    def _inverse_devoice_last_letter(self, no_orthographics_root, last_letter):
        inverse_devoicing_letters = TurkishAlphabet.Inverse_Voicing_Map[last_letter]
        inverse_devoiced_roots = []
        for inverse_devoicing_letter in inverse_devoicing_letters:
            voicing_root = no_orthographics_root._clone(True)
            voicing_root.lexeme.root = voicing_root.lexeme.root[:-1] + inverse_devoicing_letter.char_value
            voicing_root.lexeme.lemma = voicing_root.lexeme.root
            inverse_devoiced_roots.append(voicing_root)

        return inverse_devoiced_roots

    def _create_doubling_root(self, no_orthographics_root, last_char):
        doubling_root = no_orthographics_root._clone(True)
        doubling_root.lexeme.root = doubling_root.lexeme.root[:-2] + last_char
        doubling_root.lexeme.lemma = doubling_root.lexeme.root
        doubling_root.lexeme.attributes = set(doubling_root.lexeme.attributes)
        doubling_root.lexeme.attributes.add(LexemeAttribute.Doubling)
        return doubling_root


    def _get_first_vowel(self, seq):
        for s in seq:
            letter = TurkishAlphabet.get_letter_for_char(s)
            if letter and letter.vowel:
                return letter

        return None
