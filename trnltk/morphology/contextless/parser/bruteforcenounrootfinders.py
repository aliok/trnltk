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
from trnltk.morphology.contextless.parser.rootfinder import RootFinder
from trnltk.morphology.model.lexeme import SyntacticCategory, DynamicLexeme, LexemeAttribute
from trnltk.morphology.model.root import DynamicRoot
from trnltk.morphology.phonetics.alphabet import TurkishAlphabet
from trnltk.morphology.phonetics.phonetics import Phonetics

class BruteForceNounRootFinder(RootFinder):
    """
    Tries to find the root by brute force.

    Checks for the signs of the orthographic changes, and finds roots according to that.
    Checks for possible inverse harmony, doubling, voicing (except nk->nG voicing) and explicit no voicing.
    Doesn't check possible vowel drops.
    """
    def find_roots_for_partial_input(self, partial_input, whole_surface=None):
        """
        @type partial_input: unicode
        @type whole_surface: unicode
        @rtype: list of Root
        """
        assert partial_input and whole_surface
        assert len(partial_input) <= len(whole_surface)
        assert whole_surface.startswith(partial_input)
        if len(whole_surface) == len(partial_input):
            assert whole_surface == partial_input

        root = partial_input
        lemma = root
        lemma_root = lemma
        syntactic_category = SyntacticCategory.NOUN
        secondary_syntactic_category = None
        lexeme_attributes = set()

        lexeme = DynamicLexeme(lemma, lemma_root, syntactic_category, secondary_syntactic_category,
            lexeme_attributes)

        phonetic_expectations = set()
        phonetic_attributes = Phonetics.calculate_phonetic_attributes(partial_input, lexeme_attributes)

        no_orthographics_root = DynamicRoot(root, lexeme, phonetic_expectations, phonetic_attributes)

        if len(partial_input) < 2 <= len(whole_surface):
            return []

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

        for r in roots:
            phonetic_attributes = Phonetics.calculate_phonetic_attributes(r.str, r.lexeme.attributes)
            r.phonetic_attributes = phonetic_attributes

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
                devoicing_doubling_roots = [self._create_doubling_root(r, r.lexeme.root[-1]) for r in
                                            inverse_devoicing_roots]
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


class BruteForceCompoundNounRootFinder(RootFinder):
    """
    Finds roots that seem like a compoundP3sg noun.

    A compoundP3sg noun is for example 'acemborusu' or 'keçiboynuzu', but not 'akarsu'.

    This class is basically trying to explain why a noun would get Accusative form -nI
    when the root is not in the dictionary.

    These are supported:

    bacakkalemi, adamotu, aslankuyruğu, dünyahali, yaşhaddi etc.

    These are not supported:

    * soboruları
    * soborum
    * çeşmesuyunu
    * ademoğlunu

    >>> rf = BruteForceCompoundNounRootFinder()
    >>> rf.find_roots_for_partial_input(u'suborusu', u'suborusuna')

    <Root:u'suboru', Lexeme:u'soburusu'>
    """

    def __init__(self):
        self.brute_force_noun_root_finder = BruteForceNounRootFinder()

    def find_roots_for_partial_input(self, partial_input, whole_surface=None):
        """
        @type partial_input: unicode
        @type whole_surface: unicode
        @rtype: list of Root
        """
        assert partial_input and whole_surface
        assert len(partial_input) <= len(whole_surface)
        assert whole_surface.startswith(partial_input)
        if len(whole_surface) == len(partial_input):
            assert whole_surface == partial_input

        # no compound should be found an input shorter than sth like "atsu-yu". even that doesn't make sense
        if len(partial_input) < 5:
            return []

        if whole_surface == partial_input:
            return []

        last_char = partial_input[-1]
        previous_char = partial_input[-2]

        if last_char.isupper() or previous_char.isupper():
            return []

        last_letter = TurkishAlphabet.get_letter_for_char(last_char)

        if last_letter!=TurkishAlphabet.L_i and last_letter!=TurkishAlphabet.L_u and\
           last_letter!=TurkishAlphabet.L_ii and last_letter!=TurkishAlphabet.L_uu:
            return []

        first_char_after_partial_input = whole_surface[len(partial_input)]

        if first_char_after_partial_input.isupper():
            return []

        first_letter_after_partial_input = TurkishAlphabet.get_letter_for_char(first_char_after_partial_input)

        if first_letter_after_partial_input != TurkishAlphabet.L_n:
            return []

        if len(whole_surface) < len(partial_input) + 2: # need a char after char 'n'
            return []

        compound_results = []

        results_with_partial_input_one_char_missing = self.brute_force_noun_root_finder.find_roots_for_partial_input(partial_input[:-1], whole_surface)

        # illustrate:
        # partial_input = suborusu, whole_surface = suborusuna
        # results_with_partial_input_one_char_missing : <'suborus','suborus'>
        # partial_input = bacakkalemi, whole_surface = bacakkalemini
        # results_with_partial_input_one_char_missing : <'bacakkalem','bacakkalem'>

        for normal_noun_result in results_with_partial_input_one_char_missing:
            clone_result = normal_noun_result._clone(True)
            clone_result.str = clone_result.lexeme.root
            clone_result.lexeme.root = partial_input
            clone_result.lexeme.lemma = partial_input

            compound_results.append(clone_result)


        previous_letter = TurkishAlphabet.get_letter_for_char(previous_char)

        if previous_letter==TurkishAlphabet.L_s:
            results_with_partial_input_two_chars_missing = self.brute_force_noun_root_finder.find_roots_for_partial_input(partial_input[:-2], whole_surface)

            # illustrate:
            # partial_input = suborusu, whole_surface = suborusuna
            # results_with_partial_input_two_chars_missing : <'suboru','suboru'>

            for normal_noun_result in results_with_partial_input_two_chars_missing:
                clone_result = normal_noun_result._clone(True)
                clone_result.lexeme.root = partial_input
                clone_result.lexeme.lemma = partial_input

                compound_results.append(clone_result)


        for compound_result in compound_results:
            compound_result.lexeme.attributes.add(LexemeAttribute.CompoundP3sg)

        return compound_results
