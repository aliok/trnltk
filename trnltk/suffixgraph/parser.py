# coding=utf-8
import logging
from trnltk.stem.dictionaryitem import  PrimaryPosition, RootAttribute
from trnltk.suffixgraph.stem import get_default_stem_state
from trnltk.suffixgraph.suffixapplier import *
from trnltk.suffixgraph.suffixgraph import *
from trnltk.suffixgraph.token import ParseToken

logger = logging.getLogger('parser')

class Parser:
    def __init__(self, stems, predefined_paths):
        self.stems = stems
        self.predefined_paths = predefined_paths or []

    def parse(self, input):
        logger.debug('\n\n-------------Parsing word "%s"', input)

        candidates = []
        for i in range(1, len(input)+1):
            stem_candidate = input[:i]

            dictionary_stems = []
            for stem in self.stems:
                if stem.root==stem_candidate:
                    dictionary_stems.append(stem)

            if logger.isEnabledFor(logging.DEBUG):
                logger.debug('Found %d stem candidates for stem part "%s":', len(dictionary_stems), stem_candidate)
                for stem in dictionary_stems:
                    logger.debug('\t %s', stem)

            for stem in dictionary_stems:
                if self.predefined_paths.has_paths(stem):
                    predefined_tokens = self.predefined_paths.get_paths(stem)
                    logger.debug('Found predefined tokens for stem candidate "%s" : %s', stem, predefined_tokens)
                    for token in predefined_tokens:
                        if input.startswith(token.so_far):
                            logger.debug('Predefined token is applicable %s', token)
                            clone = token.clone()
                            clone.rest_str = input[len(token.so_far):]
                            candidates.append(clone)
                        else:
                            logger.debug('Predefined token is not applicable, skipping %s', token)
                else:
                    token = ParseToken(stem, get_default_stem_state(stem), input[len(stem_candidate):])
                    candidates.append(token)

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('Found %d candidate tokens :', len(candidates))
            for c in candidates:
                logger.debug('\t %s', c)

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
        state_applicable_suffixes = get_applicable_suffixes_of_state_for_token(from_state, token)
        logger.debug('  Found applicable suffixes for token from state %s: %s', from_state, state_applicable_suffixes)

        for (suffix, to_state) in state_applicable_suffixes:
            logger.debug('   Going to try suffix %s to state %s', suffix, to_state)

            new_tokens_for_suffix = try_suffix(token, suffix, to_state, word)
            if new_tokens_for_suffix:
                new_candidates.extend(new_tokens_for_suffix)

        return new_candidates

    def _apply_required_transitions_to_stem_candidates(self, candidates, word):
        new_candidates = []
        for candidate in candidates:
            if candidate.stem.dictionary_item.primary_position==PrimaryPosition.VERB:
                if RootAttribute.ProgressiveVowelDrop in candidate.stem.dictionary_item.attributes and len(candidate.stem.root)==len(candidate.stem.dictionary_item.root)-1:
                    # apply Positive + Progressive 'Iyor'

                    # apply Positive
                    if not transition_allowed_for_suffix(candidate, Positive):
                        raise Exception('There is a progressive vowel drop, but suffix "{}" cannot be applied to {}'.format(Positive, candidate))

                    clone = try_suffix_form(candidate, Positive.suffix_forms[0], VERB_WITH_POLARITY, word)    ##TODO
                    if not clone:
                        logger.debug('There is a progressive vowel drop, but suffix form "{}" cannot be applied to {}'.format(Positive.suffix_forms[0], candidate))
                        continue

                    # apply Progressive 'Iyor'
                    if not transition_allowed_for_suffix(clone, Progressive):
                        raise Exception('There is a progressive vowel drop, but suffix "{}" cannot be applied to {}'.format(Progressive, candidate))

                    clone = try_suffix_form(clone, Progressive.suffix_forms[0], VERB_WITH_TENSE, word)    ##TODO
                    if not clone:
                        logger.debug('There is a progressive vowel drop, but suffix form "{}" cannot be applied to {}'.format(Progressive.suffix_forms[0], candidate))
                        continue

                    new_candidates.append(clone)
                else:
                    new_candidates.append(candidate)
            else:
                new_candidates.append(candidate)

        return new_candidates