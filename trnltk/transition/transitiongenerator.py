from trnltk.parser.token import ParseToken

class Transition(object):
    def __init__(self, transition_str, parse_token):
        self.transition_str = transition_str
        self.parse_token = parse_token

class TransitionGenerator(object):

    def __init__(self, parser):
        self._parser = parser

    def generate_transitions(self, full_word, parse_token):
        result = []

        transition_token = ParseToken(parse_token.get_stem(), parse_token.get_stem_state(), full_word)
        result.append(Transition(parse_token.get_stem().root, transition_token))

        for transition in parse_token.get_transitions():
            transition_token = transition_token.clone()
            transition_token.add_transition(transition.suffix_form_application, transition.to_state)
            transition_token._so_far += transition.suffix_form_application.applied_suffix_form
            transition_token._remaining = full_word[len(transition_token._so_far):]
            result.append(Transition(transition_token._so_far, transition_token))

        return result