# coding=utf-8
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
import unittest
from hamcrest import *
from mockito import *
from trnltk.morphology.morphotactics.suffixgraph import SuffixGraphDecorator

class SuffixGraphTest(unittest.TestCase):
    def setUp(self):
        self.root1 = mock()
        self.state1 = mock()
        self.state2 = mock()
        self.state3 = mock()

        self.suffix1 = mock()
        self.suffix2 = mock()

        self.suffix_group1 = mock()

        self.suffix_group1.suffixes = []

        self.decorated = mock()
        self.decorator = SuffixGraphDecorator(self.decorated)

    def test_initialize(self):
        self.decorator.initialize()

        verify(self.decorated).initialize()

    def test_should_get_default_root_state_when_there_is_one(self):
        when(self.decorated)._find_default_root_state(self.root1).thenReturn(self.state1)

        assert_that(self.decorator.get_default_root_state(self.root1), same_instance(self.state1))
        verify(self.decorated)._find_default_root_state(self.root1)

    def test_should_get_default_root_state_when_there_is_not_one(self):
        when(self.decorated)._find_default_root_state(self.root1).thenReturn(None)

        try:
            self.decorator.get_default_root_state(self.root1)
            self.fail("Should've raised an exception when there is no default state found")
        except Exception:
            pass

        verify(self.decorated)._find_default_root_state(self.root1)

    def test_should_get_all_states_when_decorated_has_a_state(self):
        when(self.decorated).get_all_states().thenReturn([self.state1])
        self.decorator.all_states = {'A': self.state2, 'B': self.state3}

        assert_that(self.decorator.get_all_states(), equal_to([self.state1, self.state2, self.state3]))

        verify(self.decorated).get_all_states()

    def test_should_get_all_states_when_decorated_doesnt_have_a_state(self):
        when(self.decorated).get_all_states().thenReturn(None)
        self.decorator.all_states = {'A': self.state1, 'B': self.state2}

        assert_that(self.decorator.get_all_states(), equal_to([self.state1, self.state2]))

        verify(self.decorated).get_all_states()

    def test_should_not_find_state_when_it_doesnt_exist_at_all(self):
        when(self.decorated).find_state('STATE_NAME').thenReturn(None)
        self.decorator.all_states = {}

        assert_that(not self.decorator.find_state('STATE_NAME'))
        verify(self.decorated).find_state('STATE_NAME')

    def test_should_find_state_when_it_is_registered_in_decorated(self):
        when(self.decorated).find_state('STATE_NAME').thenReturn(self.state1)
        self.decorator.all_states = {}

        assert_that(self.decorator.find_state('STATE_NAME'), equal_to(self.state1))
        verify(self.decorated).find_state('STATE_NAME')

    def test_should_find_state_when_it_is_registered_in_decorator(self):
        when(self.decorated).find_state('STATE_NAME').thenReturn(None)
        self.decorator.all_states = {'STATE_NAME': self.state1}

        assert_that(self.decorator.find_state('STATE_NAME'), equal_to(self.state1))
        verify(self.decorated).find_state('STATE_NAME')

    def test_should_not_find_state_when_it_is_registered_in_decorated_and_decorator(self):
        when(self.decorated).find_state('STATE_NAME').thenReturn(self.state1)
        self.decorator.all_states = {'STATE_NAME': self.state2}

        try:
            self.decorator.find_state('STATE_NAME')
            self.fail("Should've raised an exception, since found state is ambiguous")
        except Exception:
            pass

        verify(self.decorated).find_state('STATE_NAME')

    def test_should_not_find_suffix_when_it_doesnt_exist_at_all(self):
        when(self.decorated).find_suffix('SUFFIX_NAME').thenReturn(None)
        self.decorator.all_suffixes = {}

        assert_that(not self.decorator.find_suffix('SUFFIX_NAME'))
        verify(self.decorated).find_suffix('SUFFIX_NAME')

    def test_should_find_suffix_when_it_is_registered_in_decorated(self):
        when(self.decorated).find_suffix('SUFFIX_NAME').thenReturn(self.suffix1)
        self.decorator.all_suffixes = {}

        assert_that(self.decorator.find_suffix('SUFFIX_NAME'), equal_to(self.suffix1))
        verify(self.decorated).find_suffix('SUFFIX_NAME')

    def test_should_find_suffix_when_it_is_registered_in_decorator(self):
        when(self.decorated).find_suffix('SUFFIX_NAME').thenReturn(None)
        self.decorator.all_suffixes = {'SUFFIX_NAME': self.suffix1}

        assert_that(self.decorator.find_suffix('SUFFIX_NAME'), equal_to(self.suffix1))
        verify(self.decorated).find_suffix('SUFFIX_NAME')

    def test_should_not_find_suffix_when_it_is_registered_in_decorated_and_decorator(self):
        when(self.decorated).find_suffix('SUFFIX_NAME').thenReturn(self.suffix1)
        self.decorator.all_suffixes = {'SUFFIX_NAME': self.suffix2}

        try:
            self.decorator.find_suffix('SUFFIX_NAME')
            self.fail("Should've raised an exception, since found suffix is ambiguous")
        except Exception:
            pass

        verify(self.decorated).find_suffix('SUFFIX_NAME')

    def test_should_register_a_state(self):
        when(self.decorated).find_state('STATE_NAME').thenReturn(None)
        self.decorator.all_states = {}

        self.decorator._register_state('STATE_NAME', 'STATE_TYPE', 'STATE_SYN_CAT')

        verify(self.decorated).find_state('STATE_NAME')
        assert_that(self.decorator.all_states, has_length(1))
        assert_that(self.decorator.all_states['STATE_NAME'].name, equal_to('STATE_NAME'))
        assert_that(self.decorator.all_states['STATE_NAME'].type, equal_to('STATE_TYPE'))
        assert_that(self.decorator.all_states['STATE_NAME'].syntactic_category, equal_to('STATE_SYN_CAT'))

    def test_should_not_register_a_state_when_it_exists_in_decorated(self):
        when(self.decorated).find_state('STATE_NAME').thenReturn(self.state1)
        self.decorator.all_states = {}

        try:
            self.decorator._register_state('STATE_NAME', 'STATE_TYPE', 'STATE_SYN_CAT')
            self.fail("Should've raised an exception, since the state is already registered in decorated")
        except Exception:
            pass

        verify(self.decorated).find_state('STATE_NAME')
        assert_that(self.decorator.all_states, has_length(0))

    def test_should_not_register_a_state_when_it_exists_in_decorator(self):
        when(self.decorated).find_state('STATE_NAME').thenReturn(None)
        self.decorator.all_states = {'STATE_NAME': self.state1}

        try:
            self.decorator._register_state('STATE_NAME', 'STATE_TYPE', 'STATE_SYN_CAT')
            self.fail("Should've raised an exception, since the state is already registered in decorator")
        except Exception:
            pass

        verify(self.decorated).find_state('STATE_NAME')
        assert_that(self.decorator.all_states, has_length(1))

    def test_should_register_a_suffix(self):
        when(self.decorated).find_suffix('SUFFIX_NAME').thenReturn(None)
        self.decorator.all_suffixes = {}

        self.decorator._register_suffix('SUFFIX_NAME', self.suffix_group1, 'SUFFIX_NAME_PRETTY', True)

        verify(self.decorated).find_suffix('SUFFIX_NAME')
        assert_that(self.decorator.all_suffixes, has_length(1))
        assert_that(self.decorator.all_suffixes['SUFFIX_NAME'].name, equal_to('SUFFIX_NAME'))
        assert_that(self.decorator.all_suffixes['SUFFIX_NAME'].group, same_instance(self.suffix_group1))
        assert_that(self.decorator.all_suffixes['SUFFIX_NAME'].pretty_name, equal_to('SUFFIX_NAME_PRETTY'))
        assert_that(self.decorator.all_suffixes['SUFFIX_NAME'].allow_repetition)

    def test_should_not_register_a_suffix_when_it_exists_in_decorated(self):
        when(self.decorated).find_suffix('SUFFIX_NAME').thenReturn(self.suffix1)
        self.decorator.all_suffixes = {}

        try:
            self.decorator._register_suffix('SUFFIX_NAME', self.suffix_group1, 'SUFFIX_NAME_PRETTY', True)
            self.fail("Should've raised an exception, since the suffix is already registered in decorated")
        except Exception:
            pass

        verify(self.decorated).find_suffix('SUFFIX_NAME')
        assert_that(self.decorator.all_suffixes, has_length(0))

    def test_should_not_register_a_suffix_when_it_exists_in_decorator(self):
        when(self.decorated).find_suffix('SUFFIX_NAME').thenReturn(None)
        self.decorator.all_suffixes = {'SUFFIX_NAME': self.suffix1}

        try:
            self.decorator._register_suffix('SUFFIX_NAME', self.suffix_group1, 'SUFFIX_NAME_PRETTY', True)
            self.fail("Should've raised an exception, since the suffix is already registered in decorator")
        except Exception:
            pass

        verify(self.decorated).find_suffix('SUFFIX_NAME')
        assert_that(self.decorator.all_suffixes, has_length(1))
        assert_that(self.decorator.all_suffixes, equal_to({'SUFFIX_NAME': self.suffix1}))

if __name__ == '__main__':
    unittest.main()