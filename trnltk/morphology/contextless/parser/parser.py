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
import logging
from trnltk.morphology.model import formatter
from trnltk.morphology.model.lexeme import  SyntacticCategory, LexemeAttribute
from trnltk.morphology.contextless.parser.suffixapplier import *
from trnltk.morphology.model.morphemecontainer import MorphemeContainer
from trnltk.morphology.phonetics.alphabet import TurkishAlphabet

logger = logging.getLogger('parser')

class ContextlessMorphologicalParser(object):
    def __init__(self, suffix_graph, predefined_paths, root_finders):
        self._suffix_graph = suffix_graph
        self._predefined_paths = predefined_paths
        self._root_finders = root_finders


    def parse(self, input):
        logger.debug('\n\n-------------Parsing word "%s"', input)

        candidates = self._find_initial_parse_morpheme_containers(input)

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('Found %d candidate morpheme containers :', len(candidates))
            for c in candidates:
                logger.debug('\t %s', c)

        logger.debug('Applying required _transitions to lexeme candidates')
        candidates = self._apply_required_transitions_to_lexeme_candidates(candidates, input)

        results = []
        new_candidates = self._traverse_candidates(candidates, results, input)
        if new_candidates:
            raise Exception('There are still parse morpheme containers to traverse, but traversing is finished : {}'.format(new_candidates))
        return results

    def _find_initial_parse_morpheme_containers(self, input):
        candidates = []

        for i in range(1, len(input) + 1):
            partial_input = input[:i]

            roots_from_lexicon = self._find_roots_for_partial_input(partial_input, input)

            if logger.isEnabledFor(logging.DEBUG):
                logger.debug('Found %d root candidates for partial input "%s":', len(roots_from_lexicon), partial_input)
                for root in roots_from_lexicon:
                    logger.debug('\t %s', root)

            for root in roots_from_lexicon:
                if self._predefined_paths and self._predefined_paths.has_paths(root):
                    predefined_morpheme_containers = self._predefined_paths.get_paths(root)
                    if logger.isEnabledFor(logging.DEBUG):
                        logger.debug('Found predefined morpheme containers for root candidate "%s" : %s', root, predefined_morpheme_containers)
                    for predefined_morpheme_container in predefined_morpheme_containers:
                        if input.startswith(predefined_morpheme_container.get_surface_so_far()):
                            logger.debug('Predefined morpheme_container is applicable %s', predefined_morpheme_container)
                            clone = predefined_morpheme_container.clone()
                            clone.set_remaining_surface(input[len(predefined_morpheme_container.get_surface_so_far()):])
                            candidates.append(clone)
                        else:
                            logger.debug('Predefined morpheme container is not applicable, skipping %s', predefined_morpheme_container)
                else:
                    morpheme_container = MorphemeContainer(root, self._suffix_graph.get_default_root_state(root), input[len(root.str):])
                    candidates.append(morpheme_container)

        return candidates

    def _find_roots_for_partial_input(self, partial_input, input):
        roots = []
        for root_finder in self._root_finders:
            roots.extend(root_finder.find_roots_for_partial_input(partial_input, input))
        return roots

    def _traverse_candidates(self, candidates, results, word):
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('Gonna traverse %d candidates:', len(candidates))
            for c in candidates:
                logger.debug('\t%s', c)

        new_candidates = []
        for morpheme_container in candidates:
            logger.debug(' Traversing candidate: %s', morpheme_container)

            morpheme_containers_for_candidate = self._traverse_candidate(morpheme_container, word)
            for morpheme_container_for_candidate in morpheme_containers_for_candidate:
                if morpheme_container_for_candidate.get_last_state().type==State.TERMINAL:
                    if not morpheme_container_for_candidate.get_remaining_surface():
                        results.append(morpheme_container_for_candidate)
                        if logger.isEnabledFor(logging.DEBUG):
                            logger.debug("Found a terminal result --------------------->")
                            logger.debug(morpheme_container_for_candidate)
                            logger.debug(formatter.format_morpheme_container_for_tests(morpheme_container_for_candidate))
                    else:
                        if logger.isEnabledFor(logging.DEBUG):
                            logger.debug("Found a morpheme container with terminal state, but there is still something to parse. Remaining:%s MorphemeContainer:%s", morpheme_container_for_candidate.get_remaining_surface(), morpheme_container_for_candidate)
                else:
                    new_candidates.append(morpheme_container_for_candidate)

        if new_candidates:
            new_candidates = self._traverse_candidates(new_candidates, results, word)

        return new_candidates

    def _traverse_candidate(self, morpheme_container, word):
        if morpheme_container.get_last_state().type==State.TERMINAL:
            return [morpheme_container]

        new_candidates = []

        from_state = morpheme_container.get_last_state()
        state_applicable_suffixes = self.get_applicable_suffixes_of_state_for_morpheme_container(from_state, morpheme_container)
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('  Found applicable suffixes for morpheme_container from state %s: %s', from_state, state_applicable_suffixes)

        for (suffix, to_state) in state_applicable_suffixes:
            logger.debug('   Going to try suffix %s to state %s', suffix, to_state)

            new_morpheme_containers_for_suffix = try_suffix(morpheme_container, suffix, to_state, word)
            if new_morpheme_containers_for_suffix:
                new_candidates.extend(new_morpheme_containers_for_suffix)

        return new_candidates

    def get_applicable_suffixes_of_state_for_morpheme_container(self, from_state, morpheme_container):
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('  Finding applicable suffixes for morpheme_container from state %s: %s', from_state, morpheme_container)
            logger.debug('   Found outputs %s', from_state.outputs)

        # filter out suffixes which are already added since last derivation
        state_applicable_suffixes = filter(lambda t: t[0] not in morpheme_container.get_suffixes_since_derivation_suffix(), from_state.outputs)
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('   Filtered out the applied suffixes since last derivation %s : %s', morpheme_container.get_suffixes_since_derivation_suffix(),  state_applicable_suffixes)

        # filter out suffixes if one of the suffixes of whose group is already added since last derivation
        state_applicable_suffixes = filter(lambda t: True if not t[0].group else t[0].group not in morpheme_container.get_suffix_groups_since_last_derivation(), state_applicable_suffixes)
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('   Filtered out the suffixes that has one applied in their groups: %s', state_applicable_suffixes)

        return state_applicable_suffixes

    def _apply_required_transitions_to_lexeme_candidates(self, candidates, word):
        new_candidates = []
        for candidate in candidates:
            if candidate.get_root().lexeme.syntactic_category==SyntacticCategory.VERB:
                if LexemeAttribute.ProgressiveVowelDrop in candidate.get_root().lexeme.attributes and len(candidate.get_root().str)==len(candidate.get_root().lexeme.root)-1:
                    # apply Positive + Progressive 'Iyor'
                    Positive = self._suffix_graph.get_suffix(u'Pos')
                    Progressive = self._suffix_graph.get_suffix(u'Prog')

                    # apply Positive
                    if not transition_allowed_for_suffix(candidate, Positive):
                        raise Exception('There is a progressive vowel drop, but suffix "{}" cannot be applied to {}'.format(Positive, candidate))

                    clone = try_suffix_form(candidate, Positive.get_suffix_form(u''), self._suffix_graph.get_state(u'VERB_WITH_POLARITY'), word)
                    if not clone:
                        if logger.isEnabledFor(logging.DEBUG):
                            logger.debug('There is a progressive vowel drop, but suffix form "{}" cannot be applied to {}'.format(Positive.suffix_forms[0], candidate))
                        continue

                    # apply Progressive 'Iyor'
                    if not transition_allowed_for_suffix(clone, Progressive):
                        raise Exception('There is a progressive vowel drop, but suffix "{}" cannot be applied to {}'.format(Progressive, candidate))

                    clone = try_suffix_form(clone, Progressive.get_suffix_form(u'Iyor'), self._suffix_graph.get_state(u'VERB_WITH_TENSE'), word)
                    if not clone:
                        if logger.isEnabledFor(logging.DEBUG):
                            logger.debug('There is a progressive vowel drop, but suffix form "{}" cannot be applied to {}'.format(Progressive.suffix_forms[0], candidate))
                        continue

                    new_candidates.append(clone)
                else:
                    new_candidates.append(candidate)
            else:
                new_candidates.append(candidate)

        return new_candidates

class UpperCaseSupportingContextlessMorphologicalParser(ContextlessMorphologicalParser):
    def __init__(self, suffix_graph, predefined_paths, root_finders):
        super(UpperCaseSupportingContextlessMorphologicalParser, self).__init__(suffix_graph, predefined_paths, root_finders)

    def parse(self, input):
        parse_results = super(UpperCaseSupportingContextlessMorphologicalParser, self).parse(input)
        if input[0].isupper():
            parse_results += super(UpperCaseSupportingContextlessMorphologicalParser, self).parse(TurkishAlphabet.lower(input[0]) + input[1:])

        return parse_results
