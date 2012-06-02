from trnltk.suffixgraph.suffixgraphmodel import FreeTransitionSuffix

__author__ = 'ali'

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

class Invert(SuffixFormCondition):
    def __init__(self, condition):
        self._condition = condition

    def matches(self, parse_token):
        return not self._condition.matches(parse_token)

    def __str__(self):
        return u'~'+repr(self._condition)

class HasOne(SuffixFormCondition):
    def __init__(self, _suffix):
        self._suffix = _suffix

    def matches(self, parse_token):
        if not parse_token:
            return False
        since_derivation_suffix = parse_token.get_suffixes_since_derivation_suffix()
        if not since_derivation_suffix:
            return False

        return self._suffix in since_derivation_suffix

    def __str__(self):
        return u'has_one({})'.format(self._suffix)

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

class RequiresRootAttributes(SuffixFormCondition):
    def __init__(self, root_attrs):
        self._root_attrs = root_attrs

    def matches(self, parse_token):
        if not parse_token:
            return False

        if not parse_token.get_suffixes_since_derivation_suffix() or not filter(lambda s : not isinstance(s, FreeTransitionSuffix), parse_token.get_suffixes_since_derivation_suffix()):
            return True

        if not parse_token.stem.dictionary_item.attributes:
            return False

        return all(r in parse_token.stem.dictionary_item.attributes for r in self._root_attrs)

    def __str__(self):
        return u'requires_root_attributes({})'.format(self._root_attrs)

    def __repr__(self):
        return self.__str__()

def comes_after(suffix):
    return HasOne(suffix)


def doesnt(condition):
    return ~condition

def doesnt_come_after(suffix):
    return doesnt(comes_after(suffix))

def followed_by(suffix):
    return HasOne(suffix)

def followed_by_suffix(condition):
    return condition

def that_goes_to(state_type):
    return SuffixGoesTo(state_type)

def applies_to_stem(stem_str):
    return AppliesToStem(stem_str)

def requires_root_attributes(root_attrs):
    return RequiresRootAttributes(root_attrs)

def requires_root_attribute(root_attr):
    return requires_root_attributes([root_attr])