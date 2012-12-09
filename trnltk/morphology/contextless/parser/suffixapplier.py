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
import logging
from trnltk.morphology.model import formatter
from trnltk.morphology.model.graphmodel import State
from trnltk.morphology.model.morpheme import SuffixFormApplication
from trnltk.morphology.phonetics.phonetics import Phonetics

logger = logging.getLogger('suffixapplier')

def try_suffix(morpheme_container, suffix, to_state, word):

    if not transition_allowed_for_suffix(morpheme_container, suffix):
        return None

    new_candidates = []

    if logger.isEnabledFor(logging.DEBUG):
        logger.debug('    Gonna try %d suffix forms : "%s"', len(suffix.suffix_forms), suffix.suffix_forms)

    for suffix_form in suffix.suffix_forms:
        logger.debug('     Gonna try suffix form "%s".', suffix_form)

        new_morpheme_container = try_suffix_form(morpheme_container, suffix_form, to_state, word)
        if new_morpheme_container:
            new_candidates.append(new_morpheme_container)

    return new_candidates

def transition_allowed_for_suffix(morpheme_container, suffix):
    if suffix.group and suffix.group in morpheme_container.get_suffix_groups_since_last_derivation():
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('    Another suffix is already added on the same group(%s) since last derivation, skipping suffix.', suffix.group)
            logger.debug('    Groups since last derivation are : %s', morpheme_container.get_suffix_groups_since_last_derivation())
        return False

    if not suffix.allow_repetition and morpheme_container.get_last_derivation_suffix() and morpheme_container.get_last_derivation_suffix()==suffix:
        logger.debug('    The last derivation suffix is same with the suffix, skipping.')
        return False

    return True

def try_suffix_form(morpheme_container, suffix_form, to_state, word):
    state_before_suffix_form_application = morpheme_container.get_last_state()

    if not transition_allowed_for_suffix_form(morpheme_container, suffix_form):
        return None

    so_far = morpheme_container.get_surface_so_far()
    morpheme_container_lexeme_attributes = morpheme_container.get_lexeme_attributes()

    morpheme_container_phonetic_attributes = morpheme_container.get_phonetic_attributes()

    modified_word, fitting_suffix_form = Phonetics.apply(so_far, morpheme_container_phonetic_attributes, suffix_form.form, morpheme_container_lexeme_attributes)
    applied_str =  modified_word + fitting_suffix_form
    if Phonetics.application_matches(word, applied_str, to_state.name!='VERB_ROOT'):
        actual_suffix_form_str = word[len(so_far):len(applied_str)]
        logger.debug('      Word "%s" starts with applied str "%s" (%s), adding to current morpheme container', word, applied_str, actual_suffix_form_str)
        clone = morpheme_container.clone()
        clone.add_transition(SuffixFormApplication(suffix_form, actual_suffix_form_str, fitting_suffix_form), to_state)

        if morpheme_container.has_transitions() and morpheme_container.get_last_transition().suffix_form_application.suffix_form.postcondition and not morpheme_container.get_last_transition().suffix_form_application.suffix_form.postcondition.is_satisfied_by(clone):
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug('      Suffix does not satisfy the postcondition "%s" of last transition suffix form "%s", skipping.', morpheme_container.get_last_transition().suffix_form_application.suffix_form.postcondition, formatter.format_transition(clone.get_last_transition()))
            return None

        if morpheme_container.has_transitions() and state_before_suffix_form_application.type==State.DERIVATIONAL:
            logger.debug('      Suffix is derivative, checking the post derivation conditions of suffixes from previous derivation.')
            for transition in morpheme_container.get_transitions_from_derivation_suffix():
                application_suffix_form = transition.suffix_form_application.suffix_form
                if application_suffix_form.post_derivation_condition:
                    matches = application_suffix_form.post_derivation_condition.is_satisfied_by(clone)
                    if not matches:
                        logger.debug('      Post derivation condition "%s" of suffix "%s" is not satisfied, skipping.', application_suffix_form.post_derivation_condition, application_suffix_form.suffix)
                        return None

        return clone

    else:
        logger.debug('      Word "%s" does not start with applied str "%s" (%s), skipping', word, applied_str, applied_str)
        return None

def transition_allowed_for_suffix_form(morpheme_container, suffix_form):
    if suffix_form.precondition and not suffix_form.precondition.is_satisfied_by(morpheme_container):
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('      Precondition "%s" of suffix form "%s" is not satisfied with transitions %s, skipping.', suffix_form.form, suffix_form.precondition, morpheme_container)
        return False

    if suffix_form.form and not Phonetics.expectations_satisfied(morpheme_container.get_phonetic_expectations(), suffix_form.form):
        logger.debug('      Suffix form "%s" does not satisfy phonetic expectations %s, skipping.', suffix_form.form, morpheme_container.get_phonetic_expectations())
        return False

    if not Phonetics.is_suffix_form_applicable(morpheme_container.get_surface_so_far(), suffix_form.form):
        logger.debug('      Suffix form "%s" is not phonetically applicable to "%s", skipping.', suffix_form.form, morpheme_container.get_surface_so_far())
        return False

    return True