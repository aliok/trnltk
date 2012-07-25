from trnltk.phonetics.phonetics import Phonetics
from trnltk.stem.dictionaryitem import RootAttribute, PrimaryPosition
from trnltk.stem.stemgenerator import NumeralStem
from trnltk.suffixgraph.suffixgraphmodel import State, FreeTransitionSuffix

class SuffixFormApplication(object):
    def __init__(self, suffix_form, applied_suffix_form):
        self.suffix_form = suffix_form
        self.applied_suffix_form = applied_suffix_form

class Transition(object):
    def __init__(self, from_state, suffix_form_application, to_state):
        self.from_state = from_state
        self.suffix_form_application = suffix_form_application
        self.to_state = to_state

    def __str__(self):
        return u'{}:{}({}->{})=>{}'.format(self.from_state, self.suffix_form_application.suffix_form.suffix.name,
            self.suffix_form_application.suffix_form.form, self.suffix_form_application.applied_suffix_form, self.to_state)

    def __repr__(self):
        return repr(self.__str__())

    #TODO: get rid of the usages : use formatter.format_transition
    def to_pretty_str(self):
        returnVal = u''
        if self.from_state.type==State.DERIV:
            returnVal = self.to_state.pretty_name + '+'

        if self.suffix_form_application.applied_suffix_form and self.suffix_form_application.applied_suffix_form.isalnum():
            returnVal += u'{}({}[{}])'.format(self.suffix_form_application.suffix_form.suffix.pretty_name,
                self.suffix_form_application.suffix_form.form, self.suffix_form_application.applied_suffix_form)
        else:
            returnVal += u'{}'.format(self.suffix_form_application.suffix_form.suffix.pretty_name)

        return returnVal

    def is_derivational(self):
        return self.from_state.type==State.DERIV

class ParseToken(object):
    def __init__(self, _stem, _stem_state, _remaining):
        self._stem = _stem
        self._stem_state = _stem_state
        self._so_far = _stem.root
        self._remaining = _remaining
        self._transitions = []
        self._phonetic_expectations = _stem.phonetic_expectations

    def clone(self):
        clone = ParseToken(self._stem, self._stem_state, self._remaining)
        clone._so_far = self._so_far
        clone._transitions = []
        clone._transitions.extend(self._transitions)
        clone._phonetic_expectations = self._phonetic_expectations
        return clone

    def get_last_state(self):
        if self._transitions:
            return self._transitions[-1].to_state
        else:
            return self._stem_state

    def get_last_derivation_transition(self):
        for transition in reversed(self._transitions):
            if transition.from_state.type==State.DERIV:
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
            if transition.from_state.type==State.DERIV:
                break
            else:
                result.append(transition.suffix_form_application.suffix_form.suffix)

        return result

    def get_transitions_since_derivation_suffix(self):
        result = []
        for transition in reversed(self._transitions):
            if transition.from_state.type==State.DERIV:
                break
            else:
                result.append(transition)

        return result

    def get_transitions_from_derivation_suffix(self):
        result = []
        for transition in reversed(self._transitions):
            if transition.from_state.type==State.DERIV:
                result.append(transition)
                break
            else:
                result.append(transition)

        return result

    def get_suffix_groups_since_last_derivation(self):
        return [s.group for s in self.get_suffixes_since_derivation_suffix()]

    def get_attributes(self):
        if self._transitions and any(t.suffix_form_application.applied_suffix_form for t in self._transitions):
            #TODO:!!!!  necessary for the case yurutemeyecekmisim !-> yurudemeyecekmisim
            if self.get_last_state().primary_position==PrimaryPosition.VERB and (
                self.get_last_state().type==State.DERIV or not self._transitions[-1].suffix_form_application.applied_suffix_form):
                return [RootAttribute.NoVoicing]
            else:
                return None
        else:
            return self._stem.dictionary_item.attributes

    def get_phonetic_attributes(self):
        if self.has_transitions():
            suffix_so_far = self.get_so_far()[len(self._stem.root):]
            if not suffix_so_far or suffix_so_far.isspace() or not suffix_so_far.isalnum():
                return self._stem.phonetic_attributes
            else:
                return Phonetics.calculate_phonetic_attributes(self.get_so_far(), self.get_attributes())
        else:
            return self._stem.phonetic_attributes


    def add_transition(self, suffix_form_application, to_state):
        last_state = self.get_last_state()
        self._transitions.append(Transition(last_state, suffix_form_application, to_state))
        self._so_far += suffix_form_application.applied_suffix_form
        self._remaining = self._remaining[len(suffix_form_application.applied_suffix_form):]

        if suffix_form_application.suffix_form.form:
            self._phonetic_expectations = []

    def has_transitions(self):
        return self._transitions and True

    def get_last_transition(self):
        return self._transitions[-1]

    def __str__(self):
        returnValue = '{}+{}'.format(self._stem, self._stem_state)
        if self._transitions:
            returnValue = returnValue + "+" + str(self._transitions)

        return returnValue

    def __repr__(self):
        return self.__str__()

    def to_pretty_str(self):    #TODO: migrate usages of this to formatter
        returnValue = u'{}({})+{}'.format(self._stem.root, self._stem.dictionary_item.lemma, self._stem_state.pretty_name)
        if self._stem.dictionary_item.secondary_position:
            returnValue += u'+{}'.format(self._stem.dictionary_item.secondary_position)

        if self._transitions:
            non_free_transitions = filter(lambda t: not isinstance(t.suffix_form_application.suffix_form.suffix, FreeTransitionSuffix), self._transitions)
            if non_free_transitions:
                returnValue = returnValue + u'+' + u'+'.join([t.to_pretty_str() for t in non_free_transitions])

        return returnValue

    def get_stem(self):
        return self._stem

    def get_stem_state(self):
        return self._stem_state

    def get_phonetic_expectations(self):
        return self._phonetic_expectations

    def get_so_far(self):
        return self._so_far

    def get_remaining(self):
        return self._remaining

    def get_transitions(self):
        return self._transitions

    def set_remaining(self, remaining):
        self._remaining = remaining


class NumeralParseToken(ParseToken):
    def __init__(self, stem, stem_state, remaining):
        if not isinstance(stem, NumeralStem):
            raise Exception("NumeralParseToken can be initialized with a NumeralStem. " + stem)
        super(NumeralParseToken, self).__init__(stem, stem_state, remaining)
