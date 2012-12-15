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

class BruteForceVerbRootFinder(RootFinder):
    """
    Finds the possible roots by brute force.

    Checks for the signs of the orthographic changes, and finds roots according to that.
    Considers progressive vowel drop (başla+ıyor -> başlıyor), voicing (git+er -> gider), aorist A (yap+ar), aorist I (gel+ir),
    causatives and passives.

    Returns phonetically valid verbs. For example 'ürk' and 'büyült' are valid, but 'zanh' is not valid.

    In verbs voicing only occurs on roots ending with 't', so others (pçk) are ignored.
    Ignores inverse harmony, since verbs don't have it.
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

        if len(partial_input) < 2:      # not possible except (d,diyor) and (y,yiyor). but they are already in the dictionary
            return []

        last_vowel = Phonetics.get_last_vowel(partial_input)

        if not last_vowel:
            return []

        root = partial_input
        lemma = root
        lemma_root = lemma
        syntactic_category = SyntacticCategory.VERB
        secondary_syntactic_category = None
        lexeme_attributes = set()

        lexeme = DynamicLexeme(lemma, lemma_root, syntactic_category, secondary_syntactic_category,
            lexeme_attributes)

        phonetic_expectations = set()
        phonetic_attributes = Phonetics.calculate_phonetic_attributes_of_plain_sequence(partial_input)

        no_attr_root = DynamicRoot(root, lexeme, phonetic_expectations, phonetic_attributes)

        self._set_lexeme_and_phonetic_attributes([no_attr_root])
        self._set_lemma([no_attr_root])

        last_char = partial_input[-1]
        last_letter = TurkishAlphabet.get_letter_for_char(last_char)

        partial_surface_can_be_root_of_a_verb = self._seems_like_a_valid_verb_root(partial_input)

        if whole_surface==partial_input:
            return [no_attr_root] if partial_surface_can_be_root_of_a_verb else []


        first_char_after_partial_input = whole_surface[len(partial_input)]

        if first_char_after_partial_input.isupper():
            return []

        first_letter_after_partial_input = TurkishAlphabet.get_letter_for_char(first_char_after_partial_input)


        might_have_ProgressiveVowelDrop = not last_letter.vowel and\
                                          any([whole_surface.startswith(partial_input+s) for s in [u'iyor', u'ıyor', u'uyor', u'üyor']])

        might_have_Aorist_A = not last_letter.vowel and \
                              (whole_surface.startswith(partial_input + u'ar') or whole_surface.startswith(partial_input + u'er'))

        # no Aorist_I for -ur, -ür
        might_have_Aorist_I = not last_letter.vowel and\
                              (whole_surface.startswith(partial_input + u'ır') or whole_surface.startswith(partial_input + u'ir'))

        # for other letters, no voicing in verbs. {git+er->gider} vs {yapar, açar, diker}
        voicing_might_have_happened = last_letter==TurkishAlphabet.L_d and first_letter_after_partial_input.vowel

        possible_progressive_vowel_drop_roots = self._get_progressive_vowel_drop_roots(partial_input, whole_surface, no_attr_root, last_vowel) if might_have_ProgressiveVowelDrop else set()
        possible_aorist_A_roots = self._get_aorist_A_roots(no_attr_root) if might_have_Aorist_A else set()
        possible_aorist_I_roots = self._get_aorist_I_roots(no_attr_root) if might_have_Aorist_I else set()
        possible_causative_roots = self._get_possible_causative_roots(partial_input, whole_surface, no_attr_root)
        possible_passive_roots = self._get_possible_passive_roots(last_letter, partial_input, whole_surface, no_attr_root)


        if voicing_might_have_happened:
            possible_progressive_vowel_drop_roots = possible_progressive_vowel_drop_roots.union(set([self._get_possible_voicing_root(r) for r in possible_progressive_vowel_drop_roots]))
            possible_aorist_A_roots = possible_aorist_A_roots.union(set([self._get_possible_voicing_root(r) for r in possible_aorist_A_roots]))
            possible_aorist_I_roots = possible_aorist_I_roots.union(set([self._get_possible_voicing_root(r) for r in possible_aorist_I_roots]))
            possible_causative_roots = possible_causative_roots.union(set([self._get_possible_voicing_root(r) for r in possible_causative_roots]))
            possible_passive_roots = possible_passive_roots.union(set([self._get_possible_voicing_root(r) for r in possible_passive_roots]))

        generated_roots = set()

        generated_roots.add(no_attr_root)

        if voicing_might_have_happened:
            generated_roots.add(self._get_possible_voicing_root(no_attr_root))

        generated_roots = generated_roots.union(possible_progressive_vowel_drop_roots)
        generated_roots = generated_roots.union(possible_aorist_A_roots)
        generated_roots = generated_roots.union(possible_aorist_I_roots)
        generated_roots = generated_roots.union(possible_causative_roots)
        generated_roots = generated_roots.union(possible_passive_roots)

        self._set_lexeme_and_phonetic_attributes(generated_roots)
        self._set_lemma(generated_roots)

        generated_roots = list(generated_roots)

        generated_roots = filter(lambda r: self._seems_like_a_valid_verb_root(r.lexeme.root), generated_roots)

        return generated_roots

    def _get_progressive_vowel_drop_roots(self, partial_input, whole_surface, no_attr_root, last_vowel):
        # başla - +Iyor --> başlıyor
        # elle  - +Iyor --> elliyor
        # oyna  - +Iyor --> oynuyor
        # söyle - +Iyor --> söylüyor
        # kazı  - +Iyor --> kazıyor
        # kaz   - +Iyor --> kazıyor

        # başıyor   : başlamak or başlımak (skip başlumak)
        # elliyor   : ellemek or ellimek (skip ellümek)
        # oynuyor   : oynamak or oynumak (skip oynımak)
        # söylüyor  : söylemek or söylümek (skip söylimek)
        # kazıyor   : kazamak or kazımak (skip kazumak)

        dropped_vowels = []

        # since there is no inverse harmony in verbs
        if not last_vowel.frontal:
            dropped_vowels.append(u'a')
            if not last_vowel.rounded:
                dropped_vowels.append(u'ı')
            else:
                dropped_vowels.append(u'u')
        else:
            dropped_vowels.append(u'e')
            if not last_vowel.rounded:
                dropped_vowels.append(u'i')
            else:
                dropped_vowels.append(u'ü')

        generated_roots = set()

        for vowel in dropped_vowels:
            generated_root = no_attr_root._clone(True)
            generated_root.lexeme.root += vowel
            generated_root.lexeme.attributes.add(LexemeAttribute.ProgressiveVowelDrop)
            generated_roots.add(generated_root)

        return generated_roots


    def _get_aorist_A_roots(self, no_attr_root):
        generated_root = no_attr_root._clone(True)
        generated_root.lexeme.attributes.add(LexemeAttribute.Aorist_A)
        return {generated_root}

    def _get_aorist_I_roots(self, no_attr_root):
        generated_root = no_attr_root._clone(True)
        generated_root.lexeme.attributes.add(LexemeAttribute.Aorist_I)
        return {generated_root}

    def _get_possible_causative_roots(self, partial_input, whole_surface, no_attr_root):
        # no voicing can happen on causative_t
        might_have_Causative_t = whole_surface.startswith(partial_input + u't')

        might_have_Causative_Ir = any([whole_surface.startswith(partial_input+s) for s in [u'ir', u'ır', u'ur', u'ür']])

        # no voicing can happen on causative_It
        might_have_Causative_It = any([whole_surface.startswith(partial_input+s) for s in [u'it', u'ıt', u'ut', u'üt']])

        might_have_Causative_Ar = any([whole_surface.startswith(partial_input+s) for s in [u'ar', u'er']])

        might_have_Causative_dIr = any([whole_surface.startswith(partial_input+s) for s in [u'dir', u'dır', u'dur', u'dür']]) or\
                                   any([whole_surface.startswith(partial_input+s) for s in [u'tir', u'tır', u'tur', u'tür']])

        might_have_causatives = {(LexemeAttribute.Causative_t, might_have_Causative_t),
                                 (LexemeAttribute.Causative_Ir, might_have_Causative_Ir),
                                 (LexemeAttribute.Causative_It, might_have_Causative_It),
                                 (LexemeAttribute.Causative_Ar, might_have_Causative_Ar),
                                 (LexemeAttribute.Causative_dIr, might_have_Causative_dIr)}

        might_have_causatives = filter(lambda t : t[1], might_have_causatives)

        causative_roots = set()

        for causative_attr, might_have_happened in might_have_causatives:
            # cannot have other causatives at the same time
            # cannot have any other passive at the same time
            # cannot have progressive vowel drop at the same time
            # cannot have aorist_A or aorist_I at the same time
            generated_root = no_attr_root._clone(True)

            generated_root.lexeme.attributes = {causative_attr} if causative_attr else set()

            generated_root.lexeme.phonetic_attributes = Phonetics.calculate_phonetic_attributes(partial_input, generated_root.lexeme.attributes)

            causative_roots.add(generated_root)

        return causative_roots

    def _get_possible_passive_roots(self, last_letter,  partial_input, whole_surface, no_attr_root):
        might_have_Passive_Il = (not last_letter.vowel and any([whole_surface.startswith(partial_input+s) for s in [u'il', u'ıl', u'ul', u'ül']])) or\
                                (last_letter.vowel and whole_surface.startswith(partial_input+ u'l'))

        might_have_Passive_In = (not last_letter.vowel and any([whole_surface.startswith(partial_input+s) for s in [u'in', u'ın', u'un', u'ün']])) or\
                                (last_letter.vowel and whole_surface.startswith(partial_input+ u'n'))

        might_have_Passive_InIl = (not last_letter.vowel and any([whole_surface.startswith(partial_input+s) for s in [u'inil', u'ınıl', u'unul', u'ünül']])) or\
                                  (last_letter.vowel and any([whole_surface.startswith(partial_input+s) for s in [u'nil', u'nıl', u'nul', u'nül']]))

        might_have_passives = {(LexemeAttribute.Passive_Il, might_have_Passive_Il),
                               (LexemeAttribute.Passive_In, might_have_Passive_In),
                               (LexemeAttribute.Passive_InIl, might_have_Passive_InIl)}

        might_have_passives = filter(lambda t : t[1], might_have_passives)

        passive_roots = set()

        for passive_attr, might_have_happened in might_have_passives:
            # cannot have other passives at the same time
            # cannot have any other causative at the same time
            # cannot have progressive vowel drop at the same time
            # cannot have aorist_A or aorist_I at the same time
            generated_root = no_attr_root._clone(True)

            generated_root.lexeme.attributes = {passive_attr} if passive_attr else set()

            generated_root.lexeme.phonetic_attributes = Phonetics.calculate_phonetic_attributes(partial_input, generated_root.lexeme.attributes)

            passive_roots.add(generated_root)

        return passive_roots

    def _get_possible_voicing_root(self, root):
        # return only the reverse_voiced root
        assert root.str[-1]==u'd', "This is weird! This method should have been called after possible voicing was already checked."

        clone = root._clone(deep=True)
        # ignoring Voicing+ProgressiveVowelDrop
        clone.lexeme.lemma = clone.lexeme.root[:-1] + TurkishAlphabet.L_t.char_value
        clone.lexeme.root = clone.lexeme.lemma
        clone.lexeme.attributes = {LexemeAttribute.Voicing}.union(clone.lexeme.attributes)
        return clone

    def _get_first_vowel(self, seq):
        for s in seq:
            letter = TurkishAlphabet.get_letter_for_char(s)
            if letter and letter.vowel:
                return letter

        return None

    def _set_lexeme_and_phonetic_attributes(self, generated_roots):
        for r in generated_roots:
            r.phonetic_attributes = Phonetics.calculate_phonetic_attributes(r.str, r.lexeme.attributes)
            if r.str.endswith(u'd') and r.lexeme.root.endswith(u't'):
                if LexemeAttribute.NoVoicing in r.lexeme.attributes:
                    r.lexeme.attributes.remove(LexemeAttribute.NoVoicing)
                r.lexeme.attributes.add(LexemeAttribute.Voicing)
            else:
                if LexemeAttribute.Voicing in r.lexeme.attributes:
                    r.lexeme.attributes.remove(LexemeAttribute.Voicing)
                r.lexeme.attributes.add(LexemeAttribute.NoVoicing)


    def _set_lemma(self, generated_roots):
        for r in generated_roots:
            word, applied_suffix_form = Phonetics.apply(r.lexeme.root, r.phonetic_attributes, u'mAk',
                r.lexeme.attributes)
            assert word and applied_suffix_form
            r.lexeme.lemma = word + applied_suffix_form

    def _seems_like_a_valid_verb_root(self, seq):
        last_char = seq[-1]
        last_letter = TurkishAlphabet.get_letter_for_char(last_char)

        previous_char = seq[-2]
        previous_letter = TurkishAlphabet.get_letter_for_char(previous_char)

        return last_letter.vowel or previous_letter.vowel or\
               (any([previous_letter == l for l in [TurkishAlphabet.L_l, TurkishAlphabet.L_r, TurkishAlphabet.L_n]])
                and not last_letter.continuant)
