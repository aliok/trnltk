from trnltk.morphology.model.morpheme import FreeTransitionSuffix

class MorphemeContainerContextFreeProbabilityGenerator(object):
    def __init__(self, first_suffix_transition_probability_matrix, suffix_transition_probability_matrix):
        self.first_suffix_transition_probability_matrix = first_suffix_transition_probability_matrix
        self.suffix_transition_probability_matrix = suffix_transition_probability_matrix

    def get_probability(self, morpheme_container):
        """
        Calculates the probability of a morpheme container without considering the context.
        @type morpheme_container: MorphemeContainer
        @rtype: float
        """
        if not morpheme_container.has_transitions():
            return 1.0

        transitions = morpheme_container.get_transitions()
        transitions = filter(lambda transition: not isinstance(transition.suffix_form_application.suffix_form.suffix, FreeTransitionSuffix), transitions)
        if not transitions:
            return 1.0

        first_suffix = transitions[0].suffix_form_application.suffix_form.suffix
        probability_of_first_suffix = self.first_suffix_transition_probability_matrix[morpheme_container.get_root().lexeme.syntactic_category][first_suffix.name]

        probability_of_morpheme_container = probability_of_first_suffix

        for i in range(0, len(transitions) - 1):
            previous_suffix = transitions[i].suffix_form_application.suffix_form.suffix
            latter_suffix = transitions[i + 1].suffix_form_application.suffix_form.suffix
            probability_of_morpheme_container *= self.suffix_transition_probability_matrix[previous_suffix.name][latter_suffix.name]

        return probability_of_morpheme_container