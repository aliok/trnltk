"""
Copyright  2012  Ali Ok (aliokATapacheDOTorg)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from trnltk.morphology.model.morpheme import FreeTransitionSuffix

class MorphemeContainerContextlessProbabilityGenerator(object):
    """
    Deprecated
    @deprecated
    """

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