from trnltk.morphology.morphotactics.suffixgraphmodel import FreeTransitionSuffix, ZeroTransitionSuffix

# http://en.wikipedia.org/wiki/Specification_pattern

class Specification(object):
    def is_satisfied_by(self, obj):
        raise NotImplementedError( "Should have implemented this" )

    def __or__(self, other):
        return OrSpecification([self,other])

    def __and__(self, other):
        return AndSpecification([self, other])

    def __invert__(self):
        return NotSpecification(self)

    def __str__(self):
        raise NotImplementedError( "Should have implemented this" )

    def __repr__(self):
        raise NotImplementedError( "Should have implemented this" )

class AndSpecification(Specification):
    def __init__(self, specifications):
        self._specifications = specifications

    def is_satisfied_by(self, obj):
        for specification in self._specifications:
            if not specification.is_satisfied_by(obj):
                return False

        return True

    def __str__(self):
        return u' & '.join(repr(c) for c in self._specifications)

    def __repr__(self):
        return self.__str__()

class OrSpecification(Specification):
    def __init__(self, specifications):
        self._specifications = specifications

    def is_satisfied_by(self, obj):
        for specification in self._specifications:
            if specification.is_satisfied_by(obj):
                return True

        return False

    def __str__(self):
        return u' | '.join(repr(c) for c in self._specifications)

    def __repr__(self):
        return self.__str__()

class NotSpecification(Specification):
    def __init__(self, specification):
        self._wrapped = specification

    def is_satisfied_by(self, obj):
        return not self._wrapped.is_satisfied_by(obj)

    def __str__(self):
        return u'~{}'.format(repr(self._wrapped))

    def __repr__(self):
        return self.__str__()

class AlwaysFalseSpecification(Specification):
    def is_satisfied_by(self, obj):
        return False

    def __str__(self):
        return u'False'

    def __repr__(self):
        return self.__str__()

class AlwaysTrueSpecification(Specification):
    def is_satisfied_by(self, obj):
        return True

    def __str__(self):
        return u'True'

    def __repr__(self):
        return self.__str__()




class HasSuffixFormSinceLastDerivation(Specification):
    def __init__(self, _suffix, _form_str=None):
        self._suffix = _suffix
        self._form_str = _form_str

    def is_satisfied_by(self, parse_token):
        if not parse_token:
            return False

        suffixes_since_derivation_suffix = parse_token.get_suffixes_since_derivation_suffix()
        if not suffixes_since_derivation_suffix:
            return False

        if self._form_str is not None:
            transitions_since_derivation_suffix = parse_token.get_transitions_since_derivation_suffix()
            if any([transition.suffix_form_application.suffix_form.suffix==self._suffix and transition.suffix_form_application.suffix_form.form==self._form_str
                        for transition in transitions_since_derivation_suffix]):
                return True
            else:
                return False
        else:
            return self._suffix in suffixes_since_derivation_suffix

    def __str__(self):
        if self._form_str is not None:
            return u'has_suffix_form_since_last_deriv({}[{}])'.format(self._suffix, self._form_str)
        else:
            return u'has_suffix_since_last_deriv({})'.format(self._suffix)

    def __repr__(self):
        return self.__str__()


class HasSuffixFormAsLastDerivation(Specification):
    def __init__(self, _suffix, _form_str=None):
        self._suffix = _suffix
        self._form_str = _form_str

    def is_satisfied_by(self, parse_token):
        if not parse_token:
            return False

        last_derivation_transition = parse_token.get_last_derivation_transition()
        if not last_derivation_transition:
            return False

        if self._form_str:
            return last_derivation_transition.suffix_form_application.suffix_form.suffix==self._suffix \
                and last_derivation_transition.suffix_form_application.suffix_form.form==self._form_str
        else:
            return last_derivation_transition.suffix_form_application.suffix_form.suffix==self._suffix

    def __str__(self):
        if self._form_str:
            return u'has_suffix_form_as_last_deriv({}[{}])'.format(self._suffix, self._form_str)
        else:
            return u'has_suffix_as_last_deriv({})'.format(self._suffix)

    def __repr__(self):
        return self.__str__()



class AppliesToStem(Specification):
    def __init__(self, stem_str):
        self._stem_str = stem_str

    def is_satisfied_by(self, parse_token):
        if not parse_token:
            return False
        return parse_token.get_stem().root==self._stem_str

    def __str__(self):
        return u'applies_to_stem({})'.format(self._stem_str)

    def __repr__(self):
        return self.__str__()



class LastSuffixGoesToState(Specification):
    def __init__(self, state_type):
        self._state_type = state_type

    def is_satisfied_by(self, parse_token):
        if not parse_token or not parse_token.has_transitions():
            return False

        if not parse_token.get_last_transition():
            return False

        return parse_token.get_last_transition().to_state.type==self._state_type

    def __str__(self):
        return u'suffix_goes_to({})'.format(self._state_type)

    def __repr__(self):
        return self.__str__()



class HasRootAttributes(Specification):
    def __init__(self, root_attrs):
        self._root_attrs = root_attrs

    def is_satisfied_by(self, parse_token):
        if not parse_token:
            return False

        transitions = parse_token.get_transitions()
        transitions = filter(lambda transition : not isinstance(transition.suffix_form_application.suffix_form.suffix, FreeTransitionSuffix), transitions)
        transitions = filter(lambda transition : not isinstance(transition.suffix_form_application.suffix_form.suffix, ZeroTransitionSuffix), transitions)
        transitions = filter(lambda transition : transition.suffix_form_application.actual_suffix_form, transitions)

        if transitions:
            return True

        if not parse_token.get_stem().dictionary_item.attributes:
            return False

        return all(r in parse_token.get_stem().dictionary_item.attributes for r in self._root_attrs)

    def __str__(self):
        return u'has_root_attributes({})'.format(self._root_attrs)

    def __repr__(self):
        return self.__str__()


class DoesntHaveRootAttributes(Specification):
    def __init__(self, root_attrs):
        self._root_attrs = root_attrs

    def is_satisfied_by(self, parse_token):
        if not parse_token:
            return False

        transitions = parse_token.get_transitions()
        transitions = filter(lambda transition : not isinstance(transition.suffix_form_application.suffix_form.suffix, FreeTransitionSuffix), transitions)
        transitions = filter(lambda transition : not isinstance(transition.suffix_form_application.suffix_form.suffix, ZeroTransitionSuffix), transitions)
        transitions = filter(lambda transition : transition.suffix_form_application.actual_suffix_form, transitions)

        if transitions:
            return True

        if not parse_token.get_stem().dictionary_item.attributes:
            return True

        return not any(r in parse_token.get_stem().dictionary_item.attributes for r in self._root_attrs)

    def __str__(self):
        return u'doesnt_have_root_attributes({})'.format(self._root_attrs)

    def __repr__(self):
        return self.__str__()


class RootHasSecondarySyntacticCategory(Specification):
    def __init__(self, secondary_syntactic_category):
            self._secondary_syntactic_category = secondary_syntactic_category

    def is_satisfied_by(self, parse_token):
        if not parse_token:
            return False
        return parse_token.get_stem().dictionary_item.secondary_syntactic_category==self._secondary_syntactic_category

    def __str__(self):
        return u'root_has_secondary_syntactic_category({})'.format(self._secondary_syntactic_category)

    def __repr__(self):
        return self.__str__()


########### preconditions
def doesnt(condition):
    return ~condition

def comes_after(suffix, form_str=None):
    return HasSuffixFormSinceLastDerivation(suffix, form_str)

def comes_after_derivation(suffix, form_str=None):
    return HasSuffixFormAsLastDerivation(suffix, form_str)

def doesnt_come_after(suffix, form_str=None):
    return doesnt(comes_after(suffix, form_str))

def doesnt_come_after_derivation(suffix, form_str=None):
    return doesnt(comes_after_derivation(suffix, form_str))

def applies_to_stem(stem_str):
    return AppliesToStem(stem_str)

def root_has_secondary_syntactic_category(secondary_syntactic_category):
    return RootHasSecondarySyntacticCategory(secondary_syntactic_category)

def has_root_attributes(root_attrs):
    return HasRootAttributes(root_attrs)

def has_root_attribute(root_attr):
    return has_root_attributes([root_attr])

def doesnt_have_root_attributes(root_attrs):
    return DoesntHaveRootAttributes(root_attrs)

def doesnt_have_root_attribute(root_attr):
    return doesnt_have_root_attributes([root_attr])

########### postconditions
def followed_by(suffix, form_str=None):
    return HasSuffixFormSinceLastDerivation(suffix, form_str)

def followed_by_one_from_group(suffix_group):
    condition = AlwaysFalseSpecification()

    for suffix in suffix_group.suffixes:
        condition = condition | followed_by(suffix)

    return condition

def followed_by_derivation(suffix, form_str=None):
    return HasSuffixFormAsLastDerivation(suffix, form_str)

def followed_by_suffix_goes_to(state_type):
    return LastSuffixGoesToState(state_type)