from trnltk.parser.token import ParseToken

class TransitionGenerator(object):

    def __init__(self, parser):
        self._parser = parser

    def generate_transitions(self, full_word, parse_token):
        result = []

        transition_token = ParseToken(parse_token.get_stem(), parse_token.get_stem_state(), full_word)
        result.append(transition_token)

        for transition in parse_token.get_transitions():
            transition_token = transition_token.clone()
            transition_token.add_transition(transition.suffix_form_application, transition.to_state)
            result.append(transition_token)

        return result