class State(object):
    TERMINAL = "TERMINAL"
    TRANSFER = "TRANSFER"
    DERIVATIONAL = "DERIVATIONAL"

    def __init__(self, name, type, syntactic_category):
        self.name = name
        self.pretty_name = syntactic_category     ##TODO: get rid of this!
        self.syntactic_category = syntactic_category
        self.outputs = [] #(suffix, out_state) tuples
        self.type = type

    def add_out_suffix(self, suffix, to_state):
        self.outputs.append((suffix, to_state))

    def __str__(self):
        return self.name

    def __repr__(self):
        return repr(self.name)