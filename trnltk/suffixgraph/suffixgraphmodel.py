# coding=utf-8
class State:
    TERMINAL = "TERMINAL"
    TRANSFER = "TRANSFER"
    DERIV = "DERIVATIONAL"

    def __init__(self, name, pretty_name, type):
        self.name = name
        self.pretty_name = pretty_name
        self.outputs = [] #(suffix, out_state) tuples
        self.type = type

    def add_out_suffix(self, suffix, to_state):
        self.outputs.append((suffix, to_state))

    def __str__(self):
        return self.name

    def __repr__(self):
        return repr(self.name)

class SuffixGroup:
    def __init__(self, name):
        self.name = name
        self.suffixes = []

    def __str__(self):
        return self.name

    def __repr__(self):
        return repr(self.name)

class Suffix:
    def __init__(self, name, rank=0, group=None, pretty_name=None, allow_repetition=False):
        self.name = name
        self.suffix_forms = []
        self.rank = rank
        self.group = None
        self.pretty_name = pretty_name or name
        self.allow_repetition = allow_repetition

        if group:
            self.group = group
            group.suffixes.append(self)

    def add_suffix_form(self, suffix_form, precondition=None, postcondition=None):
        form = None
        if type(suffix_form) is str or type(suffix_form) is unicode:
            form = SuffixForm(suffix_form, precondition, postcondition)
        elif type(suffix_form) is SuffixForm:
            assert precondition is None and  postcondition is None
        else:
            raise Exception("Unknown type for suffixForm" + repr(suffix_form))

        form.suffix=self
        self.suffix_forms.append(form)

    def __str__(self):
        return "{}({})".format(self.name, self.rank)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.name==other.name

class FreeTransitionSuffix(Suffix):
    def __init__(self, name, from_state, to_state):
        Suffix.__init__(self, name, 0 if from_state.type==State.DERIV else 999, None)
        self.add_suffix_form("")
        from_state.add_out_suffix(self, to_state)

class ZeroTransitionSuffix(Suffix):
    def __init__(self, name, from_state, to_state, pretty_name="Zero"):
        Suffix.__init__(self, name, 0 if from_state.type==State.DERIV else 999, None, pretty_name)
        self.add_suffix_form("")
        from_state.add_out_suffix(self, to_state)

class SuffixForm:
    def __init__(self, form, precondition=None, postcondition=None):
        self.form = form
        self.suffix = None
        self.precondition = precondition
        self.postcondition = postcondition

    def __str__(self):
        return self.form

    def __repr__(self):
        return repr(self.form)