# coding=utf-8
import logging
from trnltk.stem.dictionaryitem import  PrimaryPosition, RootAttribute
from trnltk.phonetics.phonetics import Phonetics
from trnltk.suffixgraph.suffixgraph import *

__author__ = 'ali'

logger = logging.getLogger('parser')

class SuffixFormApplication:
    def __init__(self, suffix_form, applied_suffix_form):
        self.suffix_form = suffix_form
        self.applied_suffix_form = applied_suffix_form

class Transition:
    def __init__(self, from_state, suffix_form_application, to_state):
        self.from_state = from_state
        self.suffix_form_application = suffix_form_application
        self.to_state = to_state

    def __str__(self):
        return u'{}:{}({}->{})=>{}'.format(self.from_state, self.suffix_form_application.suffix_form.suffix.name,
            self.suffix_form_application.suffix_form.form, self.suffix_form_application.applied_suffix_form, self.to_state)

    def __repr__(self):
        return repr(self.__str__())

    def to_pretty_str(self):
        returnVal = u''
        if self.from_state.type==State.DERIV:
            returnVal = self.to_state.pretty_name + '+'

        if self.suffix_form_application.applied_suffix_form:
            returnVal += u'{}({}[{}])'.format(self.suffix_form_application.suffix_form.suffix.pretty_name,
                self.suffix_form_application.suffix_form.form, self.suffix_form_application.applied_suffix_form)
        else:
            returnVal += u'{}'.format(self.suffix_form_application.suffix_form.suffix.pretty_name)

        return returnVal

class ParseToken:
    def __init__(self, stem, stem_state, rest_str):
        self.stem = stem
        self.stem_state = stem_state
        self.so_far = stem.root
        self.rest_str = rest_str
        self.transitions = []
        self.last_rank = -99999
        self.current_phonetic_expectations = stem.phonetic_expectations

    def clone(self):
        clone = ParseToken(self.stem, self.stem_state, self.rest_str)
        clone.so_far = self.so_far
        clone.transitions = []
        clone.transitions.extend(self.transitions)
        clone.last_rank = self.last_rank
        clone.current_phonetic_expectations = self.current_phonetic_expectations
        return clone

    def get_last_state(self):
        if self.transitions:
            return self.transitions[-1].to_state
        else:
            return self.stem_state

    def get_last_derivation_suffix(self):
        for transition in reversed(self.transitions):
            if transition.from_state.type==State.DERIV:
                return transition.suffix_form_application.suffix_form.suffix

        return None

    def get_suffixes_since_derivation_suffix(self):
        result = []
        for transition in reversed(self.transitions):
            if transition.from_state.type==State.DERIV:
                break
            else:
                result.append(transition.suffix_form_application.suffix_form.suffix)

        return result

    def get_attributes(self):      ##TODO: rename it!
        if self.transitions and any(t.suffix_form_application.applied_suffix_form for t in self.transitions):
            return None
        else:
            return self.stem.dictionary_item.attributes

    def add_transition(self, suffix_form_application, to_state):
        last_state = self.get_last_state()
        self.transitions.append(Transition(last_state, suffix_form_application, to_state))
        if to_state.type==State.DERIV:
            self.last_rank = -99999
        else:
            self.last_rank = suffix_form_application.suffix_form.suffix.rank

        if suffix_form_application.suffix_form.form:
            self.current_phonetic_expectations = []

    def __str__(self):
        returnValue = '{}+{}'.format(self.stem, self.stem_state)
        if self.transitions:
            returnValue = returnValue + "+" + str(self.transitions)

        return returnValue

    def __repr__(self):
        return self.__str__()

    def to_pretty_str(self):
        returnValue = u'{}({})+{}'.format(self.stem.root, self.stem.dictionary_item.lemma, self.stem_state.pretty_name)
        if self.stem.dictionary_item.secondary_position:
            returnValue += u'+{}'.format(self.stem.dictionary_item.secondary_position)

        if self.transitions:
            non_free_transitions = filter(lambda t: not isinstance(t.suffix_form_application.suffix_form.suffix, FreeTransitionSuffix), self.transitions)
            if non_free_transitions:
                returnValue = returnValue + u'+' + u'+'.join([t.to_pretty_str() for t in non_free_transitions])

        return returnValue

class Parser:
    def __init__(self, stems):
        self.stems = stems

    def parse(self, input):
        logger.debug('\n\n-------------Parsing word "%s"', input)

        candidates = []
        for i in range(1, len(input)+1):
            stem_candidate = input[:i]
            for stem in self.stems:
                if stem.root==stem_candidate:
                    token = ParseToken(stem, self._get_default_stem_state(stem), input[len(stem_candidate):])
                    candidates.append(token)

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('Found %d stem candidates :', len(candidates))
            for c in candidates:
                logger.debug('\t %s', c.stem)

        logger.debug('Applying required transitions to stem candidates')
        candidates = self._apply_required_transitions_to_stem_candidates(candidates, input)

        results = []
        new_candidates = self._traverse_candidates(candidates, results, input)
        if new_candidates:
            raise Exception('There are still parse tokens to traverse, but traversing is finished : {}'.format(new_candidates))
        return results

    def _traverse_candidates(self, candidates, results, word):
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('Gonna traverse %d candidates:', len(candidates))
            for c in candidates:
                logger.debug('\t%s', c)

        new_candidates = []
        for token in candidates:
            logger.debug(' Traversing candidate: %s', token)

            tokens_for_candidate = self._traverse_candidate(token, word)
            for token_for_candidate in tokens_for_candidate:
                if token_for_candidate.get_last_state().type==State.TERMINAL:
                    if not token_for_candidate.rest_str:
                        results.append(token_for_candidate)
                        logger.debug("Found a terminal result --------------------->")
                        logger.debug(token_for_candidate)
                        logger.debug(token_for_candidate.to_pretty_str())
                    else:
                        logger.debug("Found a terminal parseToken, but there is still something to parse. Remaining:%s ParseToken:%s", token_for_candidate.rest_str, token_for_candidate)
                else:
                    new_candidates.append(token_for_candidate)

        if new_candidates:
            new_candidates = self._traverse_candidates(new_candidates, results, word)

        return new_candidates

    def _traverse_candidate(self, token, word):
        if token.get_last_state().type==State.TERMINAL:
            return [token]

        new_candidates = []

        from_state = token.get_last_state()
        state_applicable_suffixes = self._get_applicable_suffixes_of_state_for_token(from_state, token)
        logger.debug('  Found applicable suffixes for token from state %s: %s', from_state, state_applicable_suffixes)

        for (suffix, to_state) in state_applicable_suffixes:
            logger.debug('   Going to try suffix %s to state %s', suffix, to_state)

            new_tokens_for_suffix = self._try_suffix(token, suffix, to_state, word)
            if new_tokens_for_suffix:
                new_candidates.extend(new_tokens_for_suffix)

        return new_candidates

    def _try_suffix(self, token, suffix, to_state, word):

        if not self._is_transition_allowed_for_suffix(token, suffix):
            return None

        new_candidates = []

        logger.debug('    Gonna try %d suffix forms : "%s"', len(suffix.suffix_forms), suffix.suffix_forms)
        for suffix_form in suffix.suffix_forms:
            logger.debug('     Gonna try suffix form "%s".', suffix_form)

            new_token = self._try_suffix_form(token, suffix_form, to_state, word)
            if new_token:
                new_candidates.append(new_token)

        return new_candidates

    def _is_transition_allowed_for_suffix(self, token, suffix):
        if suffix.group and suffix.group in self._get_suffix_groups_since_last_derivation(token):
            logger.debug('    Another suffix is already added on the same group(%s) since last derivation, skipping suffix.', suffix.group)
            logger.debug('    Groups since last derivation are : %s', self._get_suffix_groups_since_last_derivation(token))
            return False

        if token.get_last_derivation_suffix() and token.get_last_derivation_suffix()==suffix:
            logger.debug('    The last derivation suffix is same with the suffix, skipping.')
            return False

        return True

    def _try_suffix_form(self, token, suffix_form, to_state, word):
        if not self._is_transition_allowed_for_suffix_form(token, suffix_form):
            return None

        applied_str = Phonetics.apply(token.so_far, suffix_form.form, token.get_attributes())
        if Phonetics.application_matches(word, applied_str):
            applied_suffix_form = word[len(token.so_far):len(applied_str)]
            logger.debug('      Word "%s" starts with applied str "%s" (%s), adding to current token', word, applied_str, applied_suffix_form)
            clone = token.clone()
            clone.add_transition(SuffixFormApplication(suffix_form, applied_suffix_form), to_state)
            clone.so_far = applied_str
            clone.rest_str = word[len(applied_str):]

            if token.transitions and token.transitions[-1].suffix_form_application.suffix_form.postcondition and not token.transitions[-1].suffix_form_application.suffix_form.postcondition.matches(clone):
                logger.debug('      Suffix does not satisfy the postcondition "%s" of last transition suffix form "%s", skipping.', token.transitions[-1].suffix_form_application.suffix_form.postcondition, clone.transitions[-1].to_pretty_str())
                return False

            return clone

        else:
            logger.debug('      Word "%s" does not start with applied str "%s" (%s), skipping', word, applied_str, applied_str)
            return None

    def _is_transition_allowed_for_suffix_form(self, token, suffix_form):
        if suffix_form.precondition and not suffix_form.precondition.matches(token):
            logger.debug('      Precondition "%s" of suffix form "%s" is not satisfied with transitions %s, skipping.', suffix_form.form, suffix_form.precondition, token)
            return False

        if suffix_form.form and not Phonetics.expectations_satisfied(token.current_phonetic_expectations, suffix_form.form):
            logger.debug('      Suffix form "%s" does not satisfy phonetic expectations %s, skipping.', suffix_form.form, token.current_phonetic_expectations)
            return False

        if not Phonetics.applicable(token.so_far, suffix_form.form):
            logger.debug('      Suffix form "%s" is not phonetically applicable to "%s", skipping.', suffix_form.form, token.so_far)
            return False

        return True

    def _get_applicable_suffixes_of_state_for_token(self, from_state, token):
        logger.debug('  Finding applicable suffixes for token from state %s: %s', from_state, token)
        logger.debug('   Found outputs %s', from_state.outputs)

        # filter out suffixes with bigger ranks
        state_applicable_suffixes = filter(lambda t: t[0].rank >= token.last_rank, from_state.outputs)
        logger.debug('   Filtered by rank %d : %s',token.last_rank,  state_applicable_suffixes)

        # filter out suffixes which are already added since last derivation
        state_applicable_suffixes = filter(lambda t: t[0] not in token.get_suffixes_since_derivation_suffix(), state_applicable_suffixes)
        logger.debug('   Filtered out the applied suffixes since last derivation %s : %s', token.get_suffixes_since_derivation_suffix(),  state_applicable_suffixes)

        # filter out suffixes if one of the suffixes of whose group is already added since last derivation
        state_applicable_suffixes = filter(lambda t: True if not t[0].group else t[0].group not in self._get_suffix_groups_since_last_derivation(token), state_applicable_suffixes)
        logger.debug('   Filtered out the suffixes that has one applied in their groups: %s', state_applicable_suffixes)

        # sort suffixes by rank
        state_applicable_suffixes = sorted(state_applicable_suffixes, cmp=lambda x, y: cmp(x[0].rank, y[0].rank))
        logger.debug('   Sorted by rank: %s', state_applicable_suffixes)

        return state_applicable_suffixes

    def _get_suffix_groups_since_last_derivation(self, token):
        return [s.group for s in token.get_suffixes_since_derivation_suffix()]

    def _get_default_stem_state(self, stem):
        if not stem.dictionary_item.primary_position or stem.dictionary_item.primary_position==PrimaryPosition.NOUN:
            return NOUN_ROOT
        elif stem.dictionary_item.primary_position==PrimaryPosition.VERB:
            return VERB_ROOT
        elif stem.dictionary_item.primary_position==PrimaryPosition.ADVERB:
            return ADVERB_ROOT
        elif stem.dictionary_item.primary_position==PrimaryPosition.ADJECTIVE:
            return ADJECTIVE_ROOT
        elif stem.dictionary_item.primary_position==PrimaryPosition.PRONOUN:
            return PRONOUN_ROOT
        elif stem.dictionary_item.primary_position==PrimaryPosition.DETERMINER:
            return DETERMINER_ROOT_TERMINAL
        elif stem.dictionary_item.primary_position==PrimaryPosition.PUNCTUATION:
            return PUNC_ROOT_TERMINAL
        else:
            raise Exception("No stem state found!")

    def _apply_required_transitions_to_stem_candidates(self, candidates, word):
        new_candidates = []
        for candidate in candidates:
            if candidate.stem.dictionary_item.primary_position==PrimaryPosition.VERB:
                if RootAttribute.ProgressiveVowelDrop in candidate.stem.dictionary_item.attributes and len(candidate.stem.root)==len(candidate.stem.dictionary_item.root)-1:
                    # apply Positive + Progressive 'Iyor'

                    # apply Positive
                    if not self._is_transition_allowed_for_suffix(candidate, Positive):
                        raise Exception('There is a progressive vowel drop, but suffix "{}" cannot be applied to {}'.format(Positive, candidate))

                    clone = self._try_suffix_form(candidate, Positive.suffix_forms[0], VERB_WITH_POLARITY, word)    ##TODO
                    if not clone:
                        logger.debug('There is a progressive vowel drop, but suffix form "{}" cannot be applied to {}'.format(Positive.suffix_forms[0], candidate))
                        continue

                    # apply Progressive 'Iyor'
                    if not self._is_transition_allowed_for_suffix(clone, Progressive):
                        raise Exception('There is a progressive vowel drop, but suffix "{}" cannot be applied to {}'.format(Progressive, candidate))

                    clone = self._try_suffix_form(clone, Progressive.suffix_forms[0], VERB_WITH_TENSE, word)    ##TODO
                    if not clone:
                        logger.debug('There is a progressive vowel drop, but suffix form "{}" cannot be applied to {}'.format(Progressive.suffix_forms[0], candidate))
                        continue

                    new_candidates.append(clone)
                else:
                    new_candidates.append(candidate)
            else:
                new_candidates.append(candidate)

        return new_candidates