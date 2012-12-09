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
from exceptions import Exception
from trnltk.morphology.model import formatter
import trnltk.morphology.model.formatter
from trnltk.morphology.model.graphmodel import State
from trnltk.morphology.model.lexeme import SyntacticCategory, LexemeAttribute
from trnltk.morphology.model.morpheme import Transition
from trnltk.morphology.model.root import NumeralRoot
from trnltk.morphology.phonetics.phonetics import Phonetics

class MorphemeContainer(object):
    def __init__(self, root, root_state, remaining_surface):
        """
        @type root: Root
        @type root_state: State
        @type remaining_surface: str or unicode
        """
        self._root = root
        self._root_state = root_state
        self._surface_so_far = root.str
        self._remaining_surface = remaining_surface
        self._transitions = []
        self._phonetic_expectations = root.phonetic_expectations

    def __str__(self):
        returnValue = '{}+{}'.format(self._root, self._root_state)
        if self._transitions:
            returnValue = returnValue + "+" + str(self._transitions)

        return returnValue

    def __repr__(self):
        return self.__str__()

    def clone(self):
        clone = MorphemeContainer(self._root, self._root_state, self._remaining_surface)
        clone._surface_so_far = self._surface_so_far
        clone._transitions = []
        clone._transitions.extend(self._transitions)
        clone._phonetic_expectations = self._phonetic_expectations
        return clone

    def get_last_state(self):
        if self._transitions:
            return self._transitions[-1].to_state
        else:
            return self._root_state

    def get_surface(self):
        return (self._surface_so_far or "") + self._remaining_surface

    def get_surface_syntactic_category(self):
        return self.get_last_state().syntactic_category

    def get_surface_secondary_syntactic_category(self):
        word_secondary_syntactic_category = self.get_root().lexeme.secondary_syntactic_category

        if self.has_transitions():
            last_derivation_transition = self.get_last_derivation_transition()
            if last_derivation_transition:
                word_secondary_syntactic_category = None

        return word_secondary_syntactic_category

    def get_surface_with_syntactic_categories(self):
        surface = self.get_surface()
        syntactic_category = self.get_surface_syntactic_category()
        secondary_category = self.get_surface_secondary_syntactic_category()

        if secondary_category:
            return u"{}+{}+{}".format(surface, syntactic_category, secondary_category)
        else:
            return u"{}+{}".format(surface, syntactic_category)

    def get_stem(self):
        if not self._transitions:
            return self._root.lexeme.root

        indexes_of_derivational_suffixes = [i for i in range(len(self._transitions)) if self._transitions[i].is_derivational()]
        if indexes_of_derivational_suffixes:
            index_of_last_derivational_suffix = indexes_of_derivational_suffixes[-1]
            stem_so_far = self._root.str
            for i in range(0, index_of_last_derivational_suffix + 1):
                stem_so_far += self._transitions[i].suffix_form_application.fitting_suffix_form
            return stem_so_far
        else:
            return self._root.lexeme.root

    def get_stem_syntactic_category(self):
        if not self._transitions:
            return self._root.lexeme.syntactic_category

        indexes_of_derivational_suffixes = [i for i in range(len(self._transitions)) if self._transitions[i].is_derivational()]
        if indexes_of_derivational_suffixes:
            index_of_last_derivational_suffix = indexes_of_derivational_suffixes[-1]
            return self._transitions[index_of_last_derivational_suffix].to_state.syntactic_category
        else:
            return self._root.lexeme.syntactic_category

    def get_stem_secondary_syntactic_category(self):
        if not self._transitions:
            return self._root.lexeme.secondary_syntactic_category

        indexes_of_derivational_suffixes = [i for i in range(len(self._transitions)) if self._transitions[i].is_derivational()]
        if indexes_of_derivational_suffixes:
            return None
        else:
            return self._root.lexeme.secondary_syntactic_category

    def get_stem_with_syntactic_categories(self):
        stem = self.get_stem()
        syntactic_category = self.get_stem_syntactic_category()
        secondary_category = self.get_stem_secondary_syntactic_category()

        if secondary_category:
            return u"{}+{}+{}".format(stem, syntactic_category, secondary_category)
        else:
            return u"{}+{}".format(stem, syntactic_category)

    def get_lemma_root(self):
        return self._root.lexeme.root

    def get_lemma_root_syntactic_category(self):
        return self._root.lexeme.syntactic_category

    def get_lemma_root_secondary_syntactic_category(self):
        return self._root.lexeme.secondary_syntactic_category

    def get_lemma_root_with_syntactic_categories(self):
        lemma_root = self.get_lemma_root()
        syntactic_category = self.get_lemma_root_syntactic_category()
        secondary_category = self.get_lemma_root_secondary_syntactic_category()

        if secondary_category:
            return u"{}+{}+{}".format(lemma_root, syntactic_category, secondary_category)
        else:
            return u"{}+{}".format(lemma_root, syntactic_category)

    def get_last_derivation_transition(self):
        for transition in reversed(self._transitions):
            if transition.is_derivational():
                return transition

        return None

    def get_last_derivation_suffix(self):
        transition = self.get_last_derivation_transition()
        if transition:
            return transition.suffix_form_application.suffix_form.suffix
        else:
            return None

    def get_suffixes_since_derivation_suffix(self):
        result = []
        for transition in reversed(self._transitions):
            if transition.is_derivational():
                break
            else:
                result.append(transition.suffix_form_application.suffix_form.suffix)

        return result

    def get_transitions_since_derivation_suffix(self):
        result = []
        for transition in reversed(self._transitions):
            if transition.is_derivational():
                break
            else:
                result.append(transition)

        return result

    def get_transitions_from_derivation_suffix(self):
        result = []
        for transition in reversed(self._transitions):
            if transition.is_derivational():
                result.append(transition)
                break
            else:
                result.append(transition)

        return result

    def get_suffix_groups_since_last_derivation(self):
        return [s.group for s in self.get_suffixes_since_derivation_suffix()]

    def get_last_non_blank_transition(self):
        if not self._transitions:
            return None
        for transition in reversed(self._transitions):
            if transition.suffix_form_application.suffix_form.form:
                return transition

        return None

    def get_last_non_blank_derivation(self):
        if not self._transitions:
            return None
        for transition in reversed(self._transitions):
            if transition.is_derivational() and transition.suffix_form_application.suffix_form.form:
                return transition

        return None

    def get_lexeme_attributes(self):
        if self._transitions and any(t.suffix_form_application.actual_suffix_form for t in self._transitions):
            #TODO:!!!!  necessary for the case yurutemeyecekmisim !-> yurudemeyecekmisim
            if self.get_last_state().syntactic_category == SyntacticCategory.VERB and (
                self.get_last_state().type == State.DERIVATIONAL or not self.get_last_transition().suffix_form_application.actual_suffix_form):
                return {LexemeAttribute.NoVoicing}
            else:
                return None
        else:
            return self._root.lexeme.attributes

    def get_phonetic_attributes(self):
        if self.has_transitions():
            suffix_so_far = self.get_surface_so_far()[len(self._root.str):]
            if not suffix_so_far or suffix_so_far.isspace() or not suffix_so_far.isalnum():
                return self._root.phonetic_attributes
            else:
                return Phonetics.calculate_phonetic_attributes(self.get_surface_so_far(), self.get_lexeme_attributes())
        else:
            return self._root.phonetic_attributes


    def add_transition(self, suffix_form_application, to_state):
        last_state = self.get_last_state()
        self._transitions.append(Transition(last_state, suffix_form_application, to_state))
        self._surface_so_far += suffix_form_application.actual_suffix_form
        self._remaining_surface = self._remaining_surface[len(suffix_form_application.actual_suffix_form):]

        if suffix_form_application.suffix_form.form:
            self._phonetic_expectations = []

    def has_transitions(self):
        return self._transitions and True

    def get_last_transition(self):
        return self._transitions[-1]

    def get_root(self):
        return self._root

    def get_root_state(self):
        return self._root_state

    def get_phonetic_expectations(self):
        return self._phonetic_expectations

    def get_surface_so_far(self):
        return self._surface_so_far

    def get_remaining_surface(self):
        return self._remaining_surface

    def get_transitions(self):
        return self._transitions

    def set_remaining_surface(self, remaining):
        self._remaining_surface = remaining

    def format(self, add_space=False):
        return formatter.format_morpheme_container_for_parseset(self, add_space)


class NumeralMorphemeContainer(MorphemeContainer):
    def __init__(self, root, root_state, remaining_surface):
        if not isinstance(root, NumeralRoot):
            raise Exception("NumeralMorphemeContainer can be initialized with a NumeralRoot. " + root)
        super(NumeralMorphemeContainer, self).__init__(root, root_state, remaining_surface)