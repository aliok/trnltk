# coding=utf-8

class QueryFormAppender(object):
    def append(self, container, query, params):
        raise NotImplementedError()

    def append_index_key(self, index_container):
        raise NotImplementedError()

class ContextWordAppender(QueryFormAppender):
    def append(self, context_item, query, params):
        query.given_surface(False)
        params.append(context_item)

    def append_index_key(self, index_container):
        index_container.given_surface(False)

class ParseResultFormAppender(QueryFormAppender):
    def __init__(self, add_syntactic_category, is_target):
        self.add_syntactic_category = add_syntactic_category
        self.is_target = is_target

    def append(self, target, query, params):
        raise NotImplementedError()

    def append_index_key(self, index_container):
        raise NotImplementedError()

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