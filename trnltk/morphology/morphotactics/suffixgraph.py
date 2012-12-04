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
from trnltk.morphology.model.graphmodel import State
from trnltk.morphology.model.morpheme import Suffix, ZeroTransitionSuffix, FreeTransitionSuffix

class EmptySuffixGraph(object):
    def __init__(self):
        pass

    def initialize(self):
        self.register_states()
        self.register_suffixes()
        self.create_suffix_edges()

    def register_states(self):
        pass

    def get_default_root_state(self, root):
        return None

    def _find_default_root_state(self, root):
        return None

    def register_suffixes(self):
        pass

    def create_suffix_edges(self):
        pass

    def get_all_states(self):
        return None

    def find_state(self, name):
        return None

    def get_state(self, name):
        return None

    def find_suffix(self, name):
        return None

    def get_suffix(self, name):
        return None


class SuffixGraphDecorator(EmptySuffixGraph):
    def __init__(self, decorated):
        EmptySuffixGraph.__init__(self)
        self._decorated = decorated

        self.all_states = dict()
        self.all_suffixes = dict()

    def initialize(self):
        self._decorated.initialize()

        self.register_states()
        self.register_suffixes()
        self.create_suffix_edges()

    def get_default_root_state(self, root):
        state = self._find_default_root_state(root)
        if not state:
            raise Exception(u'Unable to find default root state for root {}'.format(str(root)))
        else:
            return state

    def _find_default_root_state(self, root):
        return self._decorated._find_default_root_state(root)

    def get_all_states(self):
        return (self._decorated.get_all_states() or []) + self.all_states.values()

    def find_state(self, name):
        state_from_decorated = self._decorated.find_state(name)
        state_from_self = self.all_states[name] if self.all_states.has_key(name) else None
        if state_from_decorated and state_from_self:
            raise Exception(u'State {} is found in decorated and self!'.format(name))
        else:
            return state_from_decorated or state_from_self

    def get_state(self, name):
        state = self.find_state(name)
        if not state:
            raise Exception(u'State {} not found'.format(name))
        else:
            return state

    def find_suffix(self, name):
        suffix_from_decorated = self._decorated.find_suffix(name)
        suffix_from_self = self.all_suffixes[name] if self.all_suffixes.has_key(name) else None
        if suffix_from_decorated and suffix_from_self:
            raise Exception(u'Suffix {} is found in decorated and self!'.format(name))
        else:
            return suffix_from_decorated or suffix_from_self

    def get_suffix(self, name):
        suffix = self.find_suffix(name)
        if not suffix:
            raise Exception(u'Suffix {} not found'.format(name))
        else:
            return suffix

    def _register_state(self, state_name, state_type, syntactic_category):
        if self.find_state(state_name):
            raise Exception(u'State {} already exists in decorated or self!'.format(state_name))

        assert not self.all_states.has_key(state_name)
        state = State(state_name, state_type, syntactic_category)
        self.all_states[state_name] = state
        return state

    def _register_suffix(self, name, group=None, pretty_name=None, allow_repetition=False):
        suffix = Suffix(name, group, pretty_name, allow_repetition)
        return self.__put_suffix(name, suffix)

    def _register_zero_transition_suffix(self, name):
        suffix = ZeroTransitionSuffix(name)
        return self.__put_suffix(name, suffix)

    def _register_free_transition_suffix(self, name):
        suffix = FreeTransitionSuffix(name)
        return self.__put_suffix(name, suffix)

    def __put_suffix(self, name, suffix):
        if self.find_suffix(name):
            raise Exception(u'Suffix {} already exists in decorated or self!'.format(name))
        self.all_suffixes[name] = suffix
        return suffix
