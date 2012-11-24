from trnltk.morphology.model.morphemecontainer import MorphemeContainer

class TransitionGenerator(object):

    def __init__(self, parser):
        self._parser = parser

    def generate_transitions(self, full_word, morpheme_container):
        result = []

        transition_morpheme_container = MorphemeContainer(morpheme_container.get_root(), morpheme_container.get_root_state(), full_word)
        result.append(transition_morpheme_container)

        for transition in morpheme_container.get_transitions():
            transition_morpheme_container = transition_morpheme_container.clone()
            transition_morpheme_container.add_transition(transition.suffix_form_application, transition.to_state)
            result.append(transition_morpheme_container)

        return result