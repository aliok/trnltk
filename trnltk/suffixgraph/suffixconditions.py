__author__ = 'ali'

class SuffixFormCondition:
    def matches(self, suffixes):
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

    def matches(self, suffixes):
        for condition in self._conditions:
            if not condition.matches(suffixes):
                return False

        return True

class Or(SuffixFormCondition):
    def __init__(self, conditions):
        self._conditions = conditions

    def matches(self, suffixes):
        for condition in self._conditions:
            if condition.matches(suffixes):
                return True

        return False

class Invert(SuffixFormCondition):
    def __init__(self, condition):
        self._condition = condition

    def matches(self, suffixes):
        return not self._condition.matches(suffixes)

class HasOne(SuffixFormCondition):
    def __init__(self, _suffix):
        self._suffix = _suffix

    def matches(self, suffixes):
        if not suffixes:
            return False
        return self._suffix in suffixes


def comes_after(suffix):
    return HasOne(suffix)

def followed_by(suffix):
    return HasOne(suffix)