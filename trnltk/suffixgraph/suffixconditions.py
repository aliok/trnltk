from trnltk.suffixgraph.suffixgraphmodel import FreeTransitionSuffix, ZeroTransitionSuffix

class SuffixFormCondition:
    def matches(self, parse_token):
        raise NotImplementedError( "Should have implemented this" )

    def __or__(self, other):
        return Or([self,other])

    def __and__(self, other):
        return And([self, other])

    def __invert__(self):
        return Invert(self)

    def __str__(self):
        raise NotImplementedError( "Should have implemented this" )

    def __repr__(self):
        raise NotImplementedError( "Should have implemented this" )

class And(SuffixFormCondition):
    def __init__(self, conditions):
        self._conditions = conditions

    def matches(self, parse_token):
        for condition in self._conditions:
            if not condition.matches(parse_token):
                return False

        return True

    def __str__(self):
        return u' & '.join(repr(c) for c in self._conditions)

    def __repr__(self):
        return self.__str__()

class Or(SuffixFormCondition):
    def __init__(self, conditions):
        self._conditions = conditions

    def matches(self, parse_token):
        for condition in self._conditions:
            if condition.matches(parse_token):
                return True

        return False

    def __str__(self):
        return u' | '.join(repr(c) for c in self._conditions)

    def __repr__(self):
        return self.__str__()

class Invert(SuffixFormCondition):
    def __init__(self, condition):
        self._condition = condition

    def matches(self, parse_token):
        return not self._condition.matches(parse_token)

    def __str__(self):
        return u'~{}'.format(repr(self._condition))

    def __repr__(self):
        return self.__str__()

class FalseCondition(SuffixFormCondition):
    def matches(self, parse_token):
        return False

    def __str__(self):
        return u'False'

    def __repr__(self):
        return self.__str__()

class TrueCondition(SuffixFormCondition):
    def matches(self, parse_token):
        return True

    def __str__(self):
        return u'True'

    def __repr__(self):
        return self.__str__()

class HasOne(SuffixFormCondition):
    def __init__(self, _suffix, _form_str=None):
        self._suffix = _suffix
        self._form_str = _form_str

    def matches(self, parse_token):
        if not parse_token:
            return False
        since_derivation_suffix = parse_token.get_suffixes_since_derivation_suffix()
        if not since_derivation_suffix:
            return False

        if self._form_str is not None:
            transitions_since_derivation_suffix = parse_token.get_transitions_since_derivation_suffix()
            if any([transition.suffix_form_application.suffix_form.suffix==self._suffix and transition.suffix_form_application.suffix_form.form==self._form_str
                        for transition in transitions_since_derivation_suffix]):
                return True
            else:
                return False
        else:
            return self._suffix in since_derivation_suffix

    def __str__(self):
        if self._form_str is not None:
            return u'has_one({}[{}])'.format(self._suffix, self._form_str)
        else:
            return u'has_one({})'.format(self._suffix)

    def __repr__(self):
        return self.__str__()

class HasLastDerivation(SuffixFormCondition):
    def __init__(self, _suffix, _form_str=None):
        self._suffix = _suffix
        self._form_str = _form_str

    def matches(self, parse_token):
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
            return u'has_last_derivation({}[{}])'.format(self._suffix, self._form_str)
        else:
            return u'has_last_derivation({})'.format(self._suffix)

    def __repr__(self):
        return self.__str__()

class AppliesToStem(SuffixFormCondition):
    def __init__(self, stem_str):
        self._stem_str = stem_str

    def matches(self, parse_token):
        if not parse_token:
            return False
        return parse_token.stem.root==self._stem_str

    def __str__(self):
        return u'applies_to_stem({})'.format(self._stem_str)

    def __repr__(self):
        return self.__str__()

class SuffixGoesTo(SuffixFormCondition):
    def __init__(self, state_type):
        self._state_type = state_type

    def matches(self, parse_token):
        if not parse_token or not parse_token.transitions:
            return False

        if not parse_token.transitions[-1]:
            return False

        return parse_token.transitions[-1].to_state.type==self._state_type

    def __str__(self):
        return u'suffix_goes_to({})'.format(self._state_type)

    def __repr__(self):
        return self.__str__()

class HasRootAttributes(SuffixFormCondition):
    def __init__(self, root_attrs):
        self._root_attrs = root_attrs

    def matches(self, parse_token):
        if not parse_token:
            return False

        transitions = parse_token.transitions
        transitions = filter(lambda transition : not isinstance(transition.suffix_form_application.suffix_form.suffix, FreeTransitionSuffix), transitions)
        transitions = filter(lambda transition : not isinstance(transition.suffix_form_application.suffix_form.suffix, ZeroTransitionSuffix), transitions)
        transitions = filter(lambda transition : transition.suffix_form_application.applied_suffix_form, transitions)

        if transitions:
            return True

        if not parse_token.stem.dictionary_item.attributes:
            return False

        return all(r in parse_token.stem.dictionary_item.attributes for r in self._root_attrs)

    def __str__(self):
        return u'has_root_attributes({})'.format(self._root_attrs)

    def __repr__(self):
        return self.__str__()

class DoesntHaveRootAttributes(SuffixFormCondition):
    def __init__(self, root_attrs):
        self._root_attrs = root_attrs

    def matches(self, parse_token):
        if not parse_token:
            return False

        transitions = parse_token.transitions
        transitions = filter(lambda transition : not isinstance(transition.suffix_form_application.suffix_form.suffix, FreeTransitionSuffix), transitions)
        transitions = filter(lambda transition : not isinstance(transition.suffix_form_application.suffix_form.suffix, ZeroTransitionSuffix), transitions)
        transitions = filter(lambda transition : transition.suffix_form_application.applied_suffix_form, transitions)

        if transitions:
            return True

        if not parse_token.stem.dictionary_item.attributes:
            return True

        return not any(r in parse_token.stem.dictionary_item.attributes for r in self._root_attrs)

    def __str__(self):
        return u'doesnt_have_root_attributes({})'.format(self._root_attrs)

    def __repr__(self):
        return self.__str__()

_false_condition = FalseCondition()

def comes_after(suffix, form_str=None):
    return HasOne(suffix, form_str)

def comes_after_derivation(suffix, form_str=None):
    return HasLastDerivation(suffix, form_str)

def doesnt(condition):
    return ~condition

def doesnt_come_after(suffix, form_str=None):
    return doesnt(comes_after(suffix, form_str))

def doesnt_come_after_derivation(suffix, form_str=None):
    return doesnt(comes_after_derivation(suffix, form_str))

def followed_by(suffix, form_str=None):
    return HasOne(suffix, form_str)

def followed_by_one_from_group(suffix_group):
    condition = _false_condition
    for suffix in suffix_group.suffixes:
        condition = condition | followed_by(suffix)

    return condition

def followed_by_derivation(suffix, form_str=None):
    return HasLastDerivation(suffix, form_str)

def followed_by_suffix(condition):
    return condition

def that_goes_to(state_type):
    return SuffixGoesTo(state_type)

def applies_to_stem(stem_str):
    return AppliesToStem(stem_str)

def has_root_attributes(root_attrs):
    return HasRootAttributes(root_attrs)

def has_root_attribute(root_attr):
    return has_root_attributes([root_attr])

def doesnt_have_root_attributes(root_attrs):
    return DoesntHaveRootAttributes(root_attrs)

def doesnt_have_root_attribute(root_attr):
    return doesnt_have_root_attributes([root_attr])
