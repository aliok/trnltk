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

class QueryKeyAppender(object):
    def append(self, container, query, params):
        raise NotImplementedError()

    def append_index_key(self, index_container):
        raise NotImplementedError()

class WordSurfaceAppender(QueryKeyAppender):
    def append(self, word, query, params):
        query.given_surface(False)
        params.append(word)

    def append_index_key(self, index_container):
        index_container.given_surface(False)

class WordParseResultAppender(QueryKeyAppender):
    def append(self, morpheme_container, query, params):
        query.given_parse_result()
        params.append(morpheme_container.format())

    def append_index_key(self, index_container):
        index_container.given_parse_result()

class ParseResultFormAppender(QueryKeyAppender):
    def __init__(self, add_syntactic_category, is_target):
        self.add_syntactic_category = add_syntactic_category
        self.is_target = is_target

    def append(self, target, query, params):
        raise NotImplementedError()

    def append_index_key(self, index_container):
        raise NotImplementedError()

    def get_ngram_type_item(self):
        raise NotImplementedError()


class ParseResulResultAppender(ParseResultFormAppender):
    def append(self, morpheme_container, query, params):
        if self.is_target:
            query.target_parse_result()
        else:
            query.given_parse_result()

        parse_result_str = morpheme_container.format()
        if self.add_syntactic_category:
            raise Exception('Syntactic category is not supported for parse results')
        else:
            params.append(parse_result_str)

    def append_index_key(self, index_container):
        if self.is_target:
            index_container.target_parse_result()
        else:
            index_container.given_parse_result()

    def get_ngram_type_item(self):
        return 'parse_result'


class ParseResultSurfaceAppender(ParseResultFormAppender):
    def append(self, morpheme_container, query, params):
        if self.is_target:
            if self.add_syntactic_category:
                query.target_surface(True)
            else:
                query.target_surface(False)
        else:
            if self.add_syntactic_category:
                query.given_surface(True)
            else:
                query.given_surface(False)

        surface = morpheme_container.get_surface()
        if self.add_syntactic_category:
            syntactic_category = morpheme_container.get_surface_syntactic_category()
            secondary_syntactic_category = morpheme_container.get_surface_secondary_syntactic_category()
            if secondary_syntactic_category:
                syntactic_category += u'_' + secondary_syntactic_category

            params.append(surface)
            params.append(syntactic_category)
        else:
            params.append(surface)

    def append_index_key(self, index_container):
        if self.is_target:
            if self.add_syntactic_category:
                index_container.target_surface(True)
            else:
                index_container.target_surface(False)
        else:
            if self.add_syntactic_category:
                index_container.given_surface(True)
            else:
                index_container.given_surface(False)

    def get_ngram_type_item(self):
        return 'surface'

class ParseResultStemAppender(ParseResultFormAppender):
    def append(self, morpheme_container, query, params):
        if self.is_target:
            if self.add_syntactic_category:
                query.target_stem(True)
            else:
                query.target_stem(False)
        else:
            if self.add_syntactic_category:
                query.given_stem(True)
            else:
                query.given_stem(False)

        stem = morpheme_container.get_stem()
        if self.add_syntactic_category:
            syntactic_category = morpheme_container.get_stem_syntactic_category()
            secondary_syntactic_category = morpheme_container.get_stem_secondary_syntactic_category()
            if secondary_syntactic_category:
                syntactic_category += u'_' + secondary_syntactic_category

            params.append(stem)
            params.append(syntactic_category)
        else:
            params.append(stem)

    def append_index_key(self, index_container):
        if self.is_target:
            if self.add_syntactic_category:
                index_container.target_stem(True)
            else:
                index_container.target_stem(False)
        else:
            if self.add_syntactic_category:
                index_container.given_stem(True)
            else:
                index_container.given_stem(False)

    def get_ngram_type_item(self):
        return 'stem'

class ParseResultLemmaRootAppender(ParseResultFormAppender):
    def append(self, morpheme_container, query, params):
        if self.is_target:
            if self.add_syntactic_category:
                query.target_lemma_root(True)
            else:
                query.target_lemma_root(False)
        else:
            if self.add_syntactic_category:
                query.given_lemma_root(True)
            else:
                query.given_lemma_root(False)

        lemma_root = morpheme_container.get_lemma_root()
        if self.add_syntactic_category:
            syntactic_category = morpheme_container.get_lemma_root_syntactic_category()
            secondary_syntactic_category = morpheme_container.get_lemma_root_secondary_syntactic_category()
            if secondary_syntactic_category:
                syntactic_category += u'_' + secondary_syntactic_category

            params.append(lemma_root)
            params.append(syntactic_category)
        else:
            params.append(lemma_root)

    def append_index_key(self, index_container):
        if self.is_target:
            if self.add_syntactic_category:
                index_container.target_lemma_root(True)
            else:
                index_container.target_lemma_root(False)
        else:
            if self.add_syntactic_category:
                index_container.given_lemma_root(True)
            else:
                index_container.given_lemma_root(False)

    def get_ngram_type_item(self):
        return 'lemma_root'

_word_surface_appender = _context_word_appender = WordSurfaceAppender()
_word_parse_result_appender = ParseResulResultAppender(False, False)

_target_surface_syn_cat_appender = ParseResultSurfaceAppender(True, True)
_target_stem_syn_cat_appender = ParseResultStemAppender(True, True)
_target_lemma_root_syn_cat_appender = ParseResultLemmaRootAppender(True, True)

_context_surface_syn_cat_appender = ParseResultSurfaceAppender(True, False)
_context_stem_syn_cat_appender = ParseResultStemAppender(True, False)
_context_lemma_root_syn_cat_appender = ParseResultLemmaRootAppender(True, False)