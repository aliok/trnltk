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


class And(SuffixFormCondition):
    def __init__(self, conditions):
        self._conditions = conditions

    def matches(self, parse_token):
        for condition in self._conditions:
            if not condition.matches(parse_token):
                return False

        return True

class Or(SuffixFormCondition):
    def __init__(self, conditions):
        self._conditions = conditions

    def matches(self, parse_token):
        for condition in self._conditions:
            if condition.matches(parse_token):
                return True

        return False

class Invert(SuffixFormCondition):
    def __init__(self, condition):
        self._condition = condition

    def matches(self, parse_token):
        return not self._condition.matches(parse_token)

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


class AppliesToStem(SuffixFormCondition):
    def __init__(self, stem_str):
        self._stem_str = stem_str

    def matches(self, parse_token):
        if not parse_token:
            return False
        return parse_token.stem.root==self._stem_str

def comes_after(suffix):
    return HasOne(suffix)

def followed_by(suffix):
    return HasOne(suffix)

def applies_to_stem(stem_str):
    return AppliesToStem(stem_str)