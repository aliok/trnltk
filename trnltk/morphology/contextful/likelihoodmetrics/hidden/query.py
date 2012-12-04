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

logger = logging.getLogger('query')

class QueryExecutionContext(object):
    def __init__(self, keys, collection):
        self.keys = keys
        self.collection = collection

class QueryExecutionIndexContext(object):
    def __init__(self, keys, index_name, collection):
        self.keys = keys
        self.index_name = index_name
        self.collection = collection

class CachingQueryExecutionContext(QueryExecutionContext):
    def __init__(self, keys, collection, query_cache_collection):
        super(CachingQueryExecutionContext, self).__init__(keys, collection)
        self.query_cache_collection = query_cache_collection

class WordNGramQueryContainerItem(object):
    def __init__(self, str_type, include_syntactic_category):
        self.str_type = str_type
        self.include_syntactic_category = include_syntactic_category

    def __str__(self):
        if self.include_syntactic_category:
            return "({}, {})".format(self.str_type, "syntactic_category")
        else:
            return "({})".format(self.str_type)

    def __repr__(self):
        return self.__str__()


class WordNGramQueryContainer(object):
    def __init__(self, n):
        assert n>0
        self.n = n
        self.target_item = None
        self.given_items = []

    def _add_given(self, type, include_syntactic_category=False):
        self.given_items.append(WordNGramQueryContainerItem(type, include_syntactic_category))
        return self

    def _add_target(self, type, include_syntactic_category=False):
        if self.target_item:
            raise Exception("Target item is already set!")
        self.target_item = WordNGramQueryContainerItem(type, include_syntactic_category)
        return self

    def given_parse_result(self):
        return self._add_given('parse_result', False)

    def given_surface(self, include_syntactic_category=False):
        return self._add_given('surface', include_syntactic_category)

    def given_stem(self, include_syntactic_category=False):
        return self._add_given('stem', include_syntactic_category)

    def given_lemma_root(self, include_syntactic_category=False):
        return self._add_given('lemma_root', include_syntactic_category)

    def target_parse_result(self):
        return self._add_target('parse_result', False)

    def target_surface(self, include_syntactic_category=False):
        return self._add_target('surface', include_syntactic_category)

    def target_stem(self, include_syntactic_category=False):
        return self._add_target('stem', include_syntactic_category)

    def target_lemma_root(self, include_syntactic_category=False):
        return self._add_target('lemma_root', include_syntactic_category)


class QueryExecutionContextBuilder(object):
    def __init__(self, collection_map):
        self._collection_map = collection_map

    def create_context(self, query_container, target_comes_after):
        item_count = (1 if query_container.target_item else 0) + len(query_container.given_items)
        assert query_container.n == item_count, "n: {}, item count : {}".format(query_container.n, item_count)

        keys = []

        target_item_index = query_container.n - 1 if target_comes_after else 0
        item_index_range = range(0, target_item_index) if target_comes_after else range(1, query_container.n)

        if not query_container.target_item:
            target_item_index = -1
            item_index_range = range(0, query_container.n)

        if query_container.target_item:
            target_item_keys = self._build_key(query_container.target_item, target_item_index)
            keys.extend(target_item_keys)

        for index, item in enumerate(query_container.given_items):
            item_index = item_index_range[index]
            item = query_container.given_items[index]
            item_keys = self._build_key(item, item_index)
            keys.extend(item_keys)

        collection = self._collection_map[query_container.n]

        return QueryExecutionContext(keys, collection)

    def _build_key(self, query_item, index):
        keys = ["item_{}.word.{}.value".format(index, query_item.str_type)]
        if query_item.include_syntactic_category:
            keys.append("item_{}.word.{}.syntactic_category".format(index, query_item.str_type))
        return keys

class QueryExecutionIndexContextBuilder(object):
    def __init__(self):
        pass

    def create_context(self, collection, query_container, target_comes_after):
        item_count = (1 if query_container.target_item else 0) + len(query_container.given_items)
        assert query_container.n == item_count, "n: {}, item count : {}".format(query_container.n, item_count)

        index_name = "word{}GramIdx".format(query_container.n)
        keys = []

        target_item_index = query_container.n - 1 if target_comes_after else 0
        item_index_range = range(0, target_item_index) if target_comes_after else range(1, query_container.n)

        if not query_container.target_item:
            target_item_index = -1
            item_index_range = range(0, query_container.n)

        if query_container.target_item:
            target_item_index_part, target_item_keys = self._build_key(query_container.target_item, target_item_index)
            keys.extend(target_item_keys)
            index_name += target_item_index_part

        for index, item in enumerate(query_container.given_items):
            item_index = item_index_range[index]
            item = query_container.given_items[index]
            item_index_part, item_keys = self._build_key(item, item_index)
            keys.extend(item_keys)
            index_name += item_index_part

        return QueryExecutionIndexContext(keys, index_name, collection)

    def _build_key(self, query_item, index):
        index_part = "_{}_{}".format(index, query_item.str_type)
        keys = ["item_{}.word.{}.value".format(index, query_item.str_type)]
        if query_item.include_syntactic_category:
            keys.append("item_{}.word.{}.syntactic_category".format(index, query_item.str_type))
            index_part += "_cat"
        return index_part, keys

class QueryExecutor(object):
    def __init__(self):
        self._query_execution_context = None
        self._params = None

    def query_execution_context(self, query_execution_context):
        self._query_execution_context = query_execution_context
        return self

    def params(self, *args):
        self._params = list(args)
        return  self

    def find(self):
        query_with_params = self._build_query_with_params()
        return self._query_execution_context.collection.find(query_with_params)

    def count(self):
        count = float(self.find().count())
        logger.log(logging.DEBUG, u'\tFound {} results \n'.format(count))
        return count

    def _build_query_with_params(self):
        assert len(self._params)==len(self._query_execution_context.keys)
        mongo_query = {}
        for index, param in enumerate(self._params):
            mongo_query[self._query_execution_context.keys[index]] = param

        if logger.isEnabledFor(logging.DEBUG):
            logger.log(logging.DEBUG, u'Using collection ' + self._query_execution_context.collection.full_name)
            logger.log(logging.DEBUG, u'\tRunning query : ' + unicode(mongo_query))
        return mongo_query

class CachingQueryExecutor(QueryExecutor):
    def query_execution_context(self, query_execution_context):
        """
        @type query_execution_context: CachingQueryExecutionContext
        """
        assert isinstance(query_execution_context, CachingQueryExecutionContext)
        self._query_execution_context = query_execution_context
        return self

    def count(self):
        query_with_params = self._build_query_with_params()
        query_cache_collection = self._query_execution_context.query_cache_collection
        query_str = str(query_with_params)
        cached_count = query_cache_collection.find_one({'query': query_str}, fields=['count'])

        if cached_count and cached_count['count'] is not None:
            logger.log(logging.DEBUG, u'\tFound query in the cache, returning result {}'.format(cached_count['count']))
            return cached_count['count']
        else:
            count = self._query_execution_context.collection.find(query_with_params).count()
            logger.log(logging.DEBUG, u'\tPutting query into the cache, with result {}'.format(count))
            query_cache_collection.insert({'query' : query_str, 'count' : count})
            return count

class InMemoryCachingQueryExecutor(QueryExecutor):
    query_cache = {}

    def count(self):
        query_with_params = self._build_query_with_params()

        query_str = str(query_with_params)
        cached_count = InMemoryCachingQueryExecutor.query_cache.get(query_str)

        if cached_count is not None:
            logger.log(logging.DEBUG, u'\tFound query in the cache, returning result {}'.format(cached_count))
            return cached_count
        else:
            count = self._query_execution_context.collection.find(query_with_params).count()
            logger.log(logging.DEBUG, u'\tPutting query into the cache, with result {}'.format(count))
            InMemoryCachingQueryExecutor.query_cache[query_str] = count
            return count