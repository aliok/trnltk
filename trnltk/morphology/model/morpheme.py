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
from trnltk.morphology.model.graphmodel import State

class Suffix(object):
    def __init__(self, name, group=None, pretty_name=None, allow_repetition=False):
        """
        @type name: str or unicode
        @type group: SuffixGroup or None
        @type pretty_name: str or unicode or None
        @type allow_repetition: bool
        """
        self.name = name
        self.suffix_forms = []
        self.group = None
        self.pretty_name = pretty_name or name
        self.allow_repetition = allow_repetition

        if group:
            self.group = group
            group.suffixes.append(self)

    def add_suffix_form(self, suffix_form, precondition=None, postcondition=None, post_derivation_condition=None):
        """
        @type suffix_form: SuffixForm or str or unicode
        @type precondition: Specification or None
        @type postcondition: Specification or None
        @type post_derivation_condition: Specification or None
        """
        form = None
        if type(suffix_form) is str or type(suffix_form) is unicode:
            form = SuffixForm(suffix_form, precondition, postcondition, post_derivation_condition)
        elif type(suffix_form) is SuffixForm:
            assert precondition is None and  postcondition is None and post_derivation_condition is None
        else:
            raise Exception("Unknown type for suffixForm" + repr(suffix_form))

        form.suffix=self
        self.suffix_forms.append(form)

    def get_suffix_form(self, suffix_form_str):
        """
        @type suffix_form_str: str or unicode
        @rtype: SuffixForm
        """
        result = None
        for suffix_form in self.suffix_forms:
            if suffix_form.form==suffix_form_str:
                if result:
                    raise Exception("Multiple suffix forms found for suffix {} and form {}".format(self, suffix_form_str))
                else:
                    result = suffix_form

        return result

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.name==other.name

class FreeTransitionSuffix(Suffix):
    def __init__(self, name):
        super(FreeTransitionSuffix, self).__init__(name)
        self.add_suffix_form("")

class ZeroTransitionSuffix(Suffix):
    def __init__(self, name):
        super(ZeroTransitionSuffix, self).__init__(name, None, pretty_name="Zero")
        self.add_suffix_form("")

class SuffixForm(object):
    def __init__(self, form, precondition=None, postcondition=None, post_derivation_condition=None):
        """
        @type form: str or unicode
        @type precondition: Specification or None
        @type postcondition: Specification or None
        @type post_derivation_condition: Specification or None
        """
        self.form = form
        self.suffix = None
        self.precondition = precondition
        self.postcondition = postcondition
        self.post_derivation_condition = post_derivation_condition

    def __str__(self):
        return self.form

    def __repr__(self):
        return repr(self.form)


class SuffixFormApplication(object):
    def __init__(self, suffix_form, actual_suffix_form, fitting_suffix_form):
        """
        @type suffix_form: SuffixForm
        @type actual_suffix_form: str or unicode
        @type fitting_suffix_form: str or unicode
        """
        self.suffix_form = suffix_form
        self.actual_suffix_form = actual_suffix_form
        self.fitting_suffix_form = fitting_suffix_form

class Transition(object):
    def __init__(self, from_state, suffix_form_application, to_state):
        """
        @type from_state: State
        @type suffix_form_application: SuffixFormApplication
        @type to_state: State
        """
        self.from_state = from_state
        self.suffix_form_application = suffix_form_application
        self.to_state = to_state

    def __str__(self):
        return u'{}:{}({}->{})=>{}'.format(self.from_state, self.suffix_form_application.suffix_form.suffix.name,
            self.suffix_form_application.suffix_form.form, self.suffix_form_application.actual_suffix_form, self.to_state)

    def __repr__(self):
        return repr(self.__str__())

    def is_derivational(self):
        return self.from_state.type==State.DERIVATIONAL


class SuffixGroup(object):
    def __init__(self, name):
        self.name = name
        self.suffixes = []

    def __str__(self):
        return self.name

    def __repr__(self):
        return repr(self.name)
