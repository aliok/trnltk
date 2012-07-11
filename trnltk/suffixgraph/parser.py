# coding=utf-8
import logging
from trnltk.stem.dictionaryitem import  PrimaryPosition, RootAttribute
from trnltk.suffixgraph.suffixapplier import *
from trnltk.suffixgraph.token import ParseToken

logger = logging.getLogger('parser')

class WordStemFinder:
    def __init__(self, stem_root_map):
        self.stem_root_map = stem_root_map

    def find_stem_for_partial_input(self, partial_input):
        if self.stem_root_map.has_key(partial_input):
            return self.stem_root_map[partial_input][:]
        else:
            return []

class NumeralStemFinder:
    def find_stem_for_partial_input(self, partial_input):
        return []

class Parser:
    def __init__(self, suffix_graph, predefined_paths, stem_finders):
        self._suffix_graph = suffix_graph
        self._predefined_paths = predefined_paths or []
        self._stem_finders = stem_finders


    def parse(self, input):
        logger.debug('\n\n-------------Parsing word "%s"', input)

        candidates = self._find_initial_parse_tokens(input)

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

    def _find_initial_parse_tokens(self, input):
        candidates = []

        for i in range(1, len(input) + 1):
            partial_input = input[:i]

            dictionary_stems = self._find_stems_for_partial_input(partial_input)

            if logger.isEnabledFor(logging.DEBUG):
                logger.debug('Found %d stem candidates for partial input "%s":', len(dictionary_stems), partial_input)
                for stem in dictionary_stems:
                    logger.debug('\t %s', stem)

            for stem in dictionary_stems:
                if self._predefined_paths.has_paths(stem):
                    predefined_tokens = self._predefined_paths.get_paths(stem)
                    logger.debug('Found predefined tokens for stem candidate "%s" : %s', stem, predefined_tokens)
                    for predefined_token in predefined_tokens:
                        if input.startswith(predefined_token.so_far):
                            logger.debug('Predefined token is is_suffix_form_applicable %s', predefined_token)
                            clone = predefined_token.clone()
                            clone.rest_str = input[len(predefined_token.so_far):]
                            candidates.append(clone)
                        else:
                            logger.debug('Predefined token is not is_suffix_form_applicable, skipping %s', predefined_token)
                else:
                    predefined_token = ParseToken(stem, self._suffix_graph.get_default_stem_state(stem), input[len(partial_input):])
                    candidates.append(predefined_token)

        return candidates

    def _find_stems_for_partial_input(self, partial_input):
        stems = []
        for stem_finder in self._stem_finders:
            stems.extend(stem_finder.find_stem_for_partial_input(partial_input))
        return stems

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
        state_applicable_suffixes = self.get_applicable_suffixes_of_state_for_token(from_state, token)
        logger.debug('  Found is_suffix_form_applicable suffixes for token from state %s: %s', from_state, state_applicable_suffixes)

        for (suffix, to_state) in state_applicable_suffixes:
            logger.debug('   Going to try suffix %s to state %s', suffix, to_state)

            new_tokens_for_suffix = try_suffix(token, suffix, to_state, word)
            if new_tokens_for_suffix:
                new_candidates.extend(new_tokens_for_suffix)

        return new_candidates

    def get_applicable_suffixes_of_state_for_token(self, from_state, token):
        logger.debug('  Finding is_suffix_form_applicable suffixes for token from state %s: %s', from_state, token)
        logger.debug('   Found outputs %s', from_state.outputs)

        # filter out suffixes which are already added since last derivation
        state_applicable_suffixes = filter(lambda t: t[0] not in token.get_suffixes_since_derivation_suffix(), from_state.outputs)
        logger.debug('   Filtered out the applied suffixes since last derivation %s : %s', token.get_suffixes_since_derivation_suffix(),  state_applicable_suffixes)

        # filter out suffixes if one of the suffixes of whose group is already added since last derivation
        state_applicable_suffixes = filter(lambda t: True if not t[0].group else t[0].group not in token.get_suffix_groups_since_last_derivation(), state_applicable_suffixes)
        logger.debug('   Filtered out the suffixes that has one applied in their groups: %s', state_applicable_suffixes)

        return state_applicable_suffixes

    def _apply_required_transitions_to_stem_candidates(self, candidates, word):
        new_candidates = []
        for candidate in candidates:
            if candidate.stem.dictionary_item.primary_position==PrimaryPosition.VERB:
                if RootAttribute.ProgressiveVowelDrop in candidate.stem.dictionary_item.attributes and len(candidate.stem.root)==len(candidate.stem.dictionary_item.root)-1:
                    # apply Positive + Progressive 'Iyor'
                    Positive = self._suffix_graph.Positive
                    Progressive = self._suffix_graph.Progressive

                    # apply Positive
                    if not transition_allowed_for_suffix(candidate, Positive):
                        raise Exception('There is a progressive vowel drop, but suffix "{}" cannot be applied to {}'.format(Positive, candidate))

                    clone = try_suffix_form(candidate, Positive.get_suffix_form(u''), self._suffix_graph.VERB_WITH_POLARITY, word)
                    if not clone:
                        logger.debug('There is a progressive vowel drop, but suffix form "{}" cannot be applied to {}'.format(Positive.suffix_forms[0], candidate))
                        continue

                    # apply Progressive 'Iyor'
                    if not transition_allowed_for_suffix(clone, Progressive):
                        raise Exception('There is a progressive vowel drop, but suffix "{}" cannot be applied to {}'.format(Progressive, candidate))

                    clone = try_suffix_form(clone, Progressive.get_suffix_form(u'Iyor'), self._suffix_graph.VERB_WITH_TENSE, word)
                    if not clone:
                        logger.debug('There is a progressive vowel drop, but suffix form "{}" cannot be applied to {}'.format(Progressive.suffix_forms[0], candidate))
                        continue

                    new_candidates.append(clone)
                else:
                    new_candidates.append(candidate)
            else:
                new_candidates.append(candidate)

        return new_candidates