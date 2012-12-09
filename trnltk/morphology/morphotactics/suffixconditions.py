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
from trnltk.morphology.model.morpheme import FreeTransitionSuffix, ZeroTransitionSuffix

# http://en.wikipedia.org/wiki/Specification_pattern

class Specification(object):
    def is_satisfied_by(self, obj):
        raise NotImplementedError( "Should have implemented this" )

    def __or__(self, other):
        return OrSpecification([self,other])

    def __and__(self, other):
        return AndSpecification([self, other])

    def __invert__(self):
        return NotSpecification(self)

    def __str__(self):
        raise NotImplementedError( "Should have implemented this" )

    def __repr__(self):
        raise NotImplementedError( "Should have implemented this" )

class AndSpecification(Specification):
    def __init__(self, specifications):
        self._specifications = specifications

    def is_satisfied_by(self, obj):
        for specification in self._specifications:
            if not specification.is_satisfied_by(obj):
                return False

        return True

    def __str__(self):
        return u' & '.join([unicode(c) for c in self._specifications])

    def __repr__(self):
        return self.__str__()

class OrSpecification(Specification):
    def __init__(self, specifications):
        self._specifications = specifications

    def is_satisfied_by(self, obj):
        for specification in self._specifications:
            if specification.is_satisfied_by(obj):
                return True

        return False

    def __str__(self):
        return u' | '.join([unicode(c) for c in self._specifications])

    def __repr__(self):
        return self.__str__()

class NotSpecification(Specification):
    def __init__(self, specification):
        self._wrapped = specification

    def is_satisfied_by(self, obj):
        return not self._wrapped.is_satisfied_by(obj)

    def __str__(self):
        return u'~{}'.format(unicode(self._wrapped))

    def __repr__(self):
        return self.__str__()

class AlwaysFalseSpecification(Specification):
    def is_satisfied_by(self, obj):
        return False

    def __str__(self):
        return u'False'

    def __repr__(self):
        return self.__str__()

class AlwaysTrueSpecification(Specification):
    def is_satisfied_by(self, obj):
        return True

    def __str__(self):
        return u'True'

    def __repr__(self):
        return self.__str__()




class HasSuffixFormSinceLastDerivation(Specification):
    def __init__(self, _suffix, _form_str=None):
        self._suffix = _suffix
        self._form_str = _form_str

    def is_satisfied_by(self, morpheme_container):
        if not morpheme_container:
            return False

        suffixes_since_derivation_suffix = morpheme_container.get_suffixes_since_derivation_suffix()
        if not suffixes_since_derivation_suffix:
            return False

        if self._form_str is not None:
            transitions_since_derivation_suffix = morpheme_container.get_transitions_since_derivation_suffix()
            if any([transition.suffix_form_application.suffix_form.suffix==self._suffix and transition.suffix_form_application.suffix_form.form==self._form_str
                        for transition in transitions_since_derivation_suffix]):
                return True
            else:
                return False
        else:
            return self._suffix in suffixes_since_derivation_suffix

    def __str__(self):
        if self._form_str is not None:
            return u'has_suffix_form_since_last_deriv({}[{}])'.format(self._suffix, self._form_str)
        else:
            return u'has_suffix_since_last_deriv({})'.format(self._suffix)

    def __repr__(self):
        return self.__str__()


class HasSuffixFormAsLastDerivation(Specification):
    def __init__(self, _suffix, _form_str=None):
        self._suffix = _suffix
        self._form_str = _form_str

    def is_satisfied_by(self, morpheme_container):
        if not morpheme_container:
            return False

        last_derivation_transition = morpheme_container.get_last_derivation_transition()
        if not last_derivation_transition:
            return False

        if self._form_str:
            return last_derivation_transition.suffix_form_application.suffix_form.suffix==self._suffix \
                and last_derivation_transition.suffix_form_application.suffix_form.form==self._form_str
        else:
            return last_derivation_transition.suffix_form_application.suffix_form.suffix==self._suffix

    def __str__(self):
        if self._form_str:
            return u'has_suffix_form_as_last_deriv({}[{}])'.format(self._suffix, self._form_str)
        else:
            return u'has_suffix_as_last_deriv({})'.format(self._suffix)

    def __repr__(self):
        return self.__str__()



class AppliesToRoot(Specification):
    def __init__(self, root_str):
        self._root_str = root_str

    def is_satisfied_by(self, morpheme_container):
        if not morpheme_container:
            return False
        return morpheme_container.get_root().str==self._root_str

    def __str__(self):
        return u'applies_to_root({})'.format(self._root_str)

    def __repr__(self):
        return self.__str__()



class LastSuffixGoesToState(Specification):
    def __init__(self, state_type):
        self._state_type = state_type

    def is_satisfied_by(self, morpheme_container):
        if not morpheme_container or not morpheme_container.has_transitions():
            return False

        if not morpheme_container.get_last_transition():
            return False

        return morpheme_container.get_last_transition().to_state.type==self._state_type

    def __str__(self):
        return u'suffix_goes_to({})'.format(self._state_type)

    def __repr__(self):
        return self.__str__()



class HasLexemeAttributes(Specification):
    def __init__(self, lexeme_attrs):
        self._lexeme_attrs = lexeme_attrs

    def is_satisfied_by(self, morpheme_container):
        if not morpheme_container:
            return False

        transitions = morpheme_container.get_transitions()
        transitions = filter(lambda transition : not isinstance(transition.suffix_form_application.suffix_form.suffix, FreeTransitionSuffix), transitions)
        transitions = filter(lambda transition : not isinstance(transition.suffix_form_application.suffix_form.suffix, ZeroTransitionSuffix), transitions)
        transitions = filter(lambda transition : transition.suffix_form_application.actual_suffix_form, transitions)

        if transitions:
            return True

        if not morpheme_container.get_root().lexeme.attributes:
            return False

        return all(r in morpheme_container.get_root().lexeme.attributes for r in self._lexeme_attrs)

    def __str__(self):
        return u'has_lexeme_attributes({})'.format(self._lexeme_attrs)

    def __repr__(self):
        return self.__str__()


class DoesntHaveLexemeAttributes(Specification):
    def __init__(self, lexeme_attrs):
        self._lexeme_attrs = lexeme_attrs

    def is_satisfied_by(self, morpheme_container):
        if not morpheme_container:
            return False

        transitions = morpheme_container.get_transitions()
        transitions = filter(lambda transition : not isinstance(transition.suffix_form_application.suffix_form.suffix, FreeTransitionSuffix), transitions)
        transitions = filter(lambda transition : not isinstance(transition.suffix_form_application.suffix_form.suffix, ZeroTransitionSuffix), transitions)
        transitions = filter(lambda transition : transition.suffix_form_application.actual_suffix_form, transitions)

        if transitions:
            return True

        if not morpheme_container.get_root().lexeme.attributes:
            return True

        return not any(r in morpheme_container.get_root().lexeme.attributes for r in self._lexeme_attrs)

    def __str__(self):
        return u'doesnt_have_lexeme_attributes({})'.format(self._lexeme_attrs)

    def __repr__(self):
        return self.__str__()


class RootHasSecondarySyntacticCategory(Specification):
    def __init__(self, secondary_syntactic_category):
            self._secondary_syntactic_category = secondary_syntactic_category

    def is_satisfied_by(self, morpheme_container):
        if not morpheme_container:
            return False
        return morpheme_container.get_root().lexeme.secondary_syntactic_category==self._secondary_syntactic_category

    def __str__(self):
        return u'root_has_secondary_syntactic_category({})'.format(self._secondary_syntactic_category)

    def __repr__(self):
        return self.__str__()

class HasLastNonBlankDerivation(Specification):
    def __init__(self, _suffix, _form_str=None):
        self._suffix = _suffix
        self._form_str = _form_str

    def is_satisfied_by(self, morpheme_container):
        """
        @type morpheme_container : MorphemeContainer
        @return:
        """
        if not morpheme_container:
            return False

        last_non_blank_derivation = morpheme_container.get_last_non_blank_derivation()
        if not last_non_blank_derivation:
            return False

#        print "For", morpheme_container, "result is", last_non_blank_derivation

        if self._form_str is not None:
            return self._suffix == last_non_blank_derivation.suffix_form_application.suffix_form.suffix and \
                   self._form_str == last_non_blank_derivation.suffix_form_application.suffix_form.form
        else:
            return self._suffix==last_non_blank_derivation.suffix_form_application.suffix_form.suffix

    def __str__(self):
        if self._form_str is not None:
            return u'has_last_non_blank_derivation({}[{}])'.format(self._suffix, self._form_str)
        else:
            return u'has_last_non_blank_derivation({})'.format(self._suffix)

    def __repr__(self):
        return self.__str__()

########### preconditions
def doesnt(condition):
    return ~condition

def comes_after(suffix, form_str=None):
    return HasSuffixFormSinceLastDerivation(suffix, form_str)

def comes_after_derivation(suffix, form_str=None):
    return HasSuffixFormAsLastDerivation(suffix, form_str)

def doesnt_come_after(suffix, form_str=None):
    return doesnt(comes_after(suffix, form_str))

def doesnt_come_after_derivation(suffix, form_str=None):
    return doesnt(comes_after_derivation(suffix, form_str))

def applies_to_root(root_str):
    return AppliesToRoot(root_str)

def root_has_secondary_syntactic_category(secondary_syntactic_category):
    return RootHasSecondarySyntacticCategory(secondary_syntactic_category)

def has_lexeme_attributes(lexeme_attrs):
    return HasLexemeAttributes(lexeme_attrs)

def has_lexeme_attribute(lexeme_attr):
    return has_lexeme_attributes([lexeme_attr])

def doesnt_have_lexeme_attributes(lexeme_attrs):
    return DoesntHaveLexemeAttributes(lexeme_attrs)

def doesnt_have_lexeme_attribute(lexeme_attr):
    return doesnt_have_lexeme_attributes([lexeme_attr])

def comes_after_last_non_blank_derivation(suffix, form_str=None):
    return HasLastNonBlankDerivation(suffix, form_str)

########### postconditions
def followed_by(suffix, form_str=None):
    return HasSuffixFormSinceLastDerivation(suffix, form_str)

def followed_by_one_from_group(suffix_group):
    condition = AlwaysFalseSpecification()

    for suffix in suffix_group.suffixes:
        condition = condition | followed_by(suffix)

    return condition

def followed_by_derivation(suffix, form_str=None):
    return HasSuffixFormAsLastDerivation(suffix, form_str)

def followed_by_suffix_goes_to(state_type):
    return LastSuffixGoesToState(state_type)