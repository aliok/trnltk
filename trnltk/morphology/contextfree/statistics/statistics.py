from collections import defaultdict
from trnltk.morphology.model.morpheme import FreeTransitionSuffix
from trnltk.parseset.xmlbindings import UnparsableWordBinding

class MorphemeContainerContextFreeProbabilityGenerator(object):
    def __init__(self, word_bindings):
        self.suffix_transition_count_matrix = defaultdict(lambda: defaultdict(int))
        self.suffix_transition_probability_matrix = defaultdict(lambda: defaultdict(float))
        self.first_suffix_transition_count_matrix = defaultdict(lambda: defaultdict(float))
        self.first_suffix_transition_probability_matrix = defaultdict(lambda: defaultdict(float))

        for word_binding in word_bindings:
            if isinstance(word_binding, UnparsableWordBinding):
                continue
            if word_binding.suffixes:
                first_suffix = word_binding.suffixes[0]
                self.first_suffix_transition_count_matrix[word_binding.root.syntactic_category][first_suffix.id] += 1

                for i in range(0, len(word_binding.suffixes) - 1):
                    from_suffix = word_binding.suffixes[i].id
                    to_suffix = word_binding.suffixes[i + 1].id
                    self.suffix_transition_count_matrix[from_suffix][to_suffix] += 1

        self._normalize()

    def _normalize(self):
        for from_suffix, suffix_transitions in self.suffix_transition_count_matrix.iteritems():
            transition_count_from_suffix = sum(suffix_transitions.values())
            for transition_suffix, count in suffix_transitions.iteritems():
                self.suffix_transition_probability_matrix[from_suffix][transition_suffix] = float(count) / float(transition_count_from_suffix)

        for syntactic_category, suffix_transitions in self.first_suffix_transition_count_matrix.iteritems():
            transition_count_from_syntactic_category = sum(suffix_transitions.values())
            for transition_suffix, count in suffix_transitions.iteritems():
                self.first_suffix_transition_probability_matrix[syntactic_category][transition_suffix] = float(count) / float(transition_count_from_syntactic_category)

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