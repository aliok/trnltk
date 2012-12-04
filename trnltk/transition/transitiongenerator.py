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