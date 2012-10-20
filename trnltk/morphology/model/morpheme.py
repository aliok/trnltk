from trnltk.morphology.model.graphmodel import State
from trnltk.morphology.model.root import NumeralRoot
from trnltk.morphology.phonetics.phonetics import Phonetics
from trnltk.morphology.model.lexeme import RootAttribute, SyntacticCategory

# coding=utf-8
class Suffix(object):
    def __init__(self, name, group=None, pretty_name=None, allow_repetition=False):
        """
        @type name: str or unicode
        @type group: SuffixGroup or None
        @type pretty_name: str or unicode or None
        @type allow_repetition: bool
        """
        self.name = name
        self.suffix_forms = []
        self.group = None
        self.pretty_name = pretty_name or name
        self.allow_repetition = allow_repetition

        if group:
            self.group = group
            group.suffixes.append(self)

    def add_suffix_form(self, suffix_form, precondition=None, postcondition=None, post_derivation_condition=None):
        """
        @type suffix_form: SuffixForm or str or unicode
        @type precondition: Specification or None
        @type postcondition: Specification or None
        @type post_derivation_condition: Specification or None
        """
        form = None
        if type(suffix_form) is str or type(suffix_form) is unicode:
            form = SuffixForm(suffix_form, precondition, postcondition, post_derivation_condition)
        elif type(suffix_form) is SuffixForm:
            assert precondition is None and  postcondition is None and post_derivation_condition is None
        else:
            raise Exception("Unknown type for suffixForm" + repr(suffix_form))

        form.suffix=self
        self.suffix_forms.append(form)

    def get_suffix_form(self, suffix_form_str):
        """
        @type suffix_form_str: str or unicode
        @rtype: SuffixForm
        """
        result = None
        for suffix_form in self.suffix_forms:
            if suffix_form.form==suffix_form_str:
                if result:
                    raise Exception("Multiple suffix forms found for suffix {} and form {}".format(self, suffix_form_str))
                else:
                    result = suffix_form

        return result

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.name==other.name

class FreeTransitionSuffix(Suffix):
    def __init__(self, name):
        super(FreeTransitionSuffix, self).__init__(name)
        self.add_suffix_form("")

class ZeroTransitionSuffix(Suffix):
    def __init__(self, name):
        super(ZeroTransitionSuffix, self).__init__(name, None, pretty_name="Zero")
        self.add_suffix_form("")

class SuffixForm(object):
    def __init__(self, form, precondition=None, postcondition=None, post_derivation_condition=None):
        """
        @type form: str or unicode
        @type precondition: Specification or None
        @type postcondition: Specification or None
        @type post_derivation_condition: Specification or None
        """
        self.form = form
        self.suffix = None
        self.precondition = precondition
        self.postcondition = postcondition
        self.post_derivation_condition = post_derivation_condition

    def __str__(self):
        return self.form

    def __repr__(self):
        return repr(self.form)


class SuffixFormApplication(object):
    def __init__(self, suffix_form, actual_suffix_form, fitting_suffix_form):
        """
        @type suffix_form: SuffixForm
        @type actual_suffix_form: str or unicode
        @type fitting_suffix_form: str or unicode
        """
        self.suffix_form = suffix_form
        self.actual_suffix_form = actual_suffix_form
        self.fitting_suffix_form = fitting_suffix_form

class Transition(object):
    def __init__(self, from_state, suffix_form_application, to_state):
        """
        @type from_state: State
        @type suffix_form_application: SuffixFormApplication
        @type to_state: State
        """
        self.from_state = from_state
        self.suffix_form_application = suffix_form_application
        self.to_state = to_state

    def __str__(self):
        return u'{}:{}({}->{})=>{}'.format(self.from_state, self.suffix_form_application.suffix_form.suffix.name,
            self.suffix_form_application.suffix_form.form, self.suffix_form_application.actual_suffix_form, self.to_state)

    def __repr__(self):
        return repr(self.__str__())

    def is_derivational(self):
        return self.from_state.type==State.DERIVATIONAL

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


    def get_stem(self):
        if not self._transitions:
            return self._root.lexeme.root

        indexes_of_derivational_suffixes = [i for i in range(len(self._transitions)) if self._transitions[i].is_derivational()]
        if indexes_of_derivational_suffixes:
            index_of_last_derivational_suffix = indexes_of_derivational_suffixes[-1]
            stem_so_far = self._root.str
            for i in range(0, index_of_last_derivational_suffix + 1):
                stem_so_far += self._transitions[i].suffix_form_application.fitting_suffix_form
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

    def get_lemma_root(self):
        return self._root.lexeme.root

    def get_lemma_root_syntactic_category(self):
        return self._root.lexeme.syntactic_category

    def get_lemma_root_secondary_syntactic_category(self):
        return self._root.lexeme.secondary_syntactic_category

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

    def get_attributes(self):
        if self._transitions and any(t.suffix_form_application.actual_suffix_form for t in self._transitions):
            #TODO:!!!!  necessary for the case yurutemeyecekmisim !-> yurudemeyecekmisim
            if self.get_last_state().syntactic_category==SyntacticCategory.VERB and (
                self.get_last_state().type==State.DERIVATIONAL or not self._transitions[-1].suffix_form_application.actual_suffix_form):
                return [RootAttribute.NoVoicing]
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
                return Phonetics.calculate_phonetic_attributes(self.get_surface_so_far(), self.get_attributes())
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


class NumeralMorphemeContainer(MorphemeContainer):
    def __init__(self, root, root_state, remaining_surface):
        if not isinstance(root, NumeralRoot):
            raise Exception("NumeralMorphemeContainer can be initialized with a NumeralRoot. " + root)
        super(NumeralMorphemeContainer, self).__init__(root, root_state, remaining_surface)

class SuffixGroup(object):
    def __init__(self, name):
        self.name = name
        self.suffixes = []

    def __str__(self):
        return self.name

    def __repr__(self):
        return repr(self.name)
