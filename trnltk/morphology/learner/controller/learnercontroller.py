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
from trnltk.morphology.contextful.likelihoodmetrics.wordformcollocation.parsecontext import MockMorphemeContainerBuilder
from trnltk.morphology.model import formatter

class LearnerController(object):
    WORD_COUNT_TO_SHOW_IN_CONTEXT = 6
    WORD_COUNT_TO_USE_AS_PARSE_CONTEXT = 2

    def __init__(self, learnerview, dbmanager, sessionmanager, contextful_morphological_parser, parse_context_creator):
        """
        @type learnerview: LearnerView
        @type dbmanager : DbManager
        @type sessionmanager : SessionManager
        @type contextful_morphological_parser : ContextfulMorphologicalParser
        @type parse_context_creator : ParseContextCreator
        """
        self.learnerview = learnerview
        self.dbmanager = dbmanager
        self.sessionmanager = sessionmanager
        self.contextful_morphological_parser = contextful_morphological_parser
        self.parse_context_creator = parse_context_creator



    def go_to_word(self, word_id):
        """
        @type word_id: ObjectId
        """
        assert LearnerController.WORD_COUNT_TO_SHOW_IN_CONTEXT >= LearnerController.WORD_COUNT_TO_USE_AS_PARSE_CONTEXT

        assert word_id

        self.sessionmanager.delete_parse_results()

        # find and set new word in view
        word = self.dbmanager.get_word(word_id)
        assert word
        self.learnerview.set_current_word(word)

        word_index = word['index']
        corpus_id = word['corpus_id']

        # set corpus id in the view
        self.learnerview.set_corpus_id(corpus_id)

        # find and set contexts (to be shown) in view
        leading_start_index_to_show = word_index - LearnerController.WORD_COUNT_TO_SHOW_IN_CONTEXT
        leading_end_index_to_show = word_index - 1

        following_start_index_to_show = word_index + 1
        following_end_index_to_show = word_index + LearnerController.WORD_COUNT_TO_SHOW_IN_CONTEXT

        leading_words = self.dbmanager.get_words_in_range(corpus_id, leading_start_index_to_show, leading_end_index_to_show)
        following_words = self.dbmanager.get_words_in_range(corpus_id, following_start_index_to_show, following_end_index_to_show)

        self.learnerview.set_leading_words(leading_words)
        self.learnerview.set_following_words(following_words)


        # set counts and indices of the new word within counts in view
        all_nonparsed_count = self.dbmanager.count_all_nonparsed(corpus_id)
        prior_nonparsed_count = self.dbmanager.count_nonparsed_prior_to_index(corpus_id, word_index)

        all_count = self.dbmanager.count_all(corpus_id)

        if not word['parsed']:
            self.learnerview.set_all_nonparsed_count(all_nonparsed_count)
            self.learnerview.set_prior_nonparsed_count(prior_nonparsed_count)

        self.learnerview.set_all_count(all_count)


        # find previous and next nonparsed words and set the stuff on the ui
        previous_nonparsed_word = self.dbmanager.find_previous_nonparsed_word(corpus_id, word_index)
        next_nonparsed_word = self.dbmanager.find_next_nonparsed_word(corpus_id, word_index)

        if previous_nonparsed_word:
            self.learnerview.set_previous_nonparsed_word(previous_nonparsed_word)
        if next_nonparsed_word:
            self.learnerview.set_next_nonparsed_word(next_nonparsed_word)

        next_word = self.dbmanager.find_next_word(corpus_id, word)
        if next_word:
            self.learnerview.set_next_word(next_word)


        # find parse context words
        leading_parse_context_words = leading_words[-LearnerController.WORD_COUNT_TO_USE_AS_PARSE_CONTEXT:] if len(leading_words) >=LearnerController.WORD_COUNT_TO_USE_AS_PARSE_CONTEXT else leading_words[:]
        following_parse_context_words = following_words[:LearnerController.WORD_COUNT_TO_USE_AS_PARSE_CONTEXT] if len(following_words) >= LearnerController.WORD_COUNT_TO_USE_AS_PARSE_CONTEXT else following_words[:]

        leading_parse_context = self.parse_context_creator.create(leading_parse_context_words)
        following_parse_context = self.parse_context_creator.create(following_parse_context_words)

        # parse and set parse results in view
        parse_results_with_likelihoods = []

        calculation_context = {}
        parse_results = self.contextful_morphological_parser.parse_with_likelihoods(word['surface'], leading_parse_context, following_parse_context, calculation_context)
        if not parse_results:
            return

        for parse_result_index, (parse_result, likelihood) in enumerate(parse_results):
            parse_results_with_likelihoods.append((parse_result, likelihood, calculation_context[parse_result_index]))

        total_likelihood = sum([t[1] for t in parse_results_with_likelihoods])

        # sort by likelihood then "shortness"
        parse_results_with_likelihoods = sorted(parse_results_with_likelihoods, key=lambda tup : (tup[1], -len(tup[0].get_transitions())), reverse=True)

        for parse_result, likelihood_value, calculation_context in parse_results_with_likelihoods:
            uuid_for_parse_result = self.sessionmanager.put_parse_result_in_session(parse_result, calculation_context)
            likelihood_percent = likelihood_value / total_likelihood * 100.0 if total_likelihood > 0.0 else 0.0
            is_correct_parse_result = word['parsed'] and formatter.format_morpheme_container_for_parseset(parse_result)==word['parse_result']
            self.learnerview.add_parse_result(uuid_for_parse_result, parse_result, likelihood_value, likelihood_percent, is_correct_parse_result, calculation_context)


class ParseContextCreator(object):
    def __init__(self, morphological_parser):
        self.morphological_parser = morphological_parser

    def create(self, parse_context_words):
        return [self._build_parse_context_item_from_word(parse_context_word) for parse_context_word in parse_context_words]

    def _build_parse_context_item_from_word(self, parse_context_word):
        if parse_context_word['parsed']:
            return [
                MockMorphemeContainerBuilder(
                    parse_context_word.get('parse_result'),
                    parse_context_word['surface'],
                    parse_context_word['surface_syntactic_category'],
                    parse_context_word['surface_secondary_syntactic_category']
                )\
                .stem(
                    parse_context_word['stem'],
                    parse_context_word['stem_syntactic_category'],
                    parse_context_word['stem_secondary_syntactic_category'],
                ).lexeme(
                    parse_context_word['lemma_root'],
                    parse_context_word['lemma_root_syntactic_category'],
                    parse_context_word['lemma_root_secondary_syntactic_category']
                )\
                .build()
            ]

        else:
            return self.morphological_parser.parse(parse_context_word['surface'])
