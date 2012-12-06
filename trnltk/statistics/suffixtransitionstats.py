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
from collections import defaultdict
from trnltk.parseset.xmlbindings import UnparsableWordBinding

class SuffixTransitionProbabilityGenerator(object):
    """
    Deprecated
    @deprecated
    """

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