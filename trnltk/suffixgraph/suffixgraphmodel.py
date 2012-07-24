# coding=utf-8
class State(object):
    TERMINAL = "TERMINAL"
    TRANSFER = "TRANSFER"
    DERIV = "DERIVATIONAL"

    def __init__(self, name, type, primary_position):
        self.name = name
        self.pretty_name = primary_position     ##TODO: get rid of this!
        self.primary_position = primary_position
        self.outputs = [] #(suffix, out_state) tuples
        self.type = type

    def add_out_suffix(self, suffix, to_state):
        self.outputs.append((suffix, to_state))

    def __str__(self):
        return self.name

    def __repr__(self):
        return repr(self.name)

class SuffixGroup(object):
    def __init__(self, name):
        self.name = name
        self.suffixes = []

    def __str__(self):
        return self.name

    def __repr__(self):
        return repr(self.name)

class Suffix(object):
    def __init__(self, name, group=None, pretty_name=None, allow_repetition=False):
        self.name = name
        self.suffix_forms = []
        self.group = None
        self.pretty_name = pretty_name or name
        self.allow_repetition = allow_repetition

        if group:
            self.group = group
            group.suffixes.append(self)

    def add_suffix_form(self, suffix_form, precondition=None, postcondition=None, post_derivation_condition=None):
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
    def __init__(self, name, from_state, to_state):
        super(FreeTransitionSuffix, self).__init__(name)
        self.add_suffix_form("")
        from_state.add_out_suffix(self, to_state)

class ZeroTransitionSuffix(Suffix):
    def __init__(self, name, from_state, to_state, pretty_name="Zero"):
        super(ZeroTransitionSuffix, self).__init__(name, None, pretty_name)
        self.add_suffix_form("")
        from_state.add_out_suffix(self, to_state)

class SuffixForm(object):
    def __init__(self, form, precondition=None, postcondition=None, post_derivation_condition=None):
        self.form = form
        self.suffix = None
        self.precondition = precondition
        self.postcondition = postcondition
        self.post_derivation_condition = post_derivation_condition

    def __str__(self):
        return self.form

    def __repr__(self):
        return repr(self.form)