# coding=utf-8
import logging
import pymongo

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

    def given_surface(self, include_syntactic_category=False):
        return self._add_given('surface', include_syntactic_category)

    def given_stem(self, include_syntactic_category=False):
        return self._add_given('stem', include_syntactic_category)

    def given_lemma_root(self, include_syntactic_category=False):
        return self._add_given('lemma_root', include_syntactic_category)

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


class DatabaseIndexBuilder(object):
    def __init__(self, collection_map):
        self._collection_map = collection_map

    def create_indexes(self, appender_matrix):
        for appender_tuple in appender_matrix:
            target_appender, context_appender = None, None

            if len(appender_tuple)>1:
                target_appender, context_appender = appender_tuple
            else:
                context_appender = appender_tuple[0]

            for key_index in range(0, len(self._collection_map.keys())):

                n = sorted(list(self._collection_map.keys()))[key_index]
                collection = self._collection_map[n]

                if n>1:
                    smaller_collection = self._collection_map[n-1]
                    smaller_index_container = WordNGramQueryContainer(n-1)

                    self._create_container_and_index(smaller_collection, smaller_index_container, n-1, None, context_appender)

                index_container = WordNGramQueryContainer(n)
                self._create_container_and_index(collection, index_container, n, target_appender, context_appender)



    def _create_container_and_index(self, collection, index_container, n, target_appender, context_appender):
        if target_appender:
            target_appender.append_index_key(index_container)
        else:
            n +=1

        for i in range(0, n-1):
            context_appender.append_index_key(index_container)

        self._create_index_from_container(collection, index_container, True)
        self._create_index_from_container(collection, index_container, False)


    def _create_index_from_container(self, collection, index_container, target_comes_after):
        query_execution_index_context = QueryExecutionIndexContextBuilder().create_context(collection, index_container, target_comes_after)
        index_name, keys = query_execution_index_context.index_name, query_execution_index_context.keys

        index_keys = [(key, pymongo.ASCENDING) for key in keys]
        logger.log(logging.DEBUG, u'Creating index {} on collection {} with keys: {}'.format(index_name, collection.name, index_keys))
        # pymongo caches the index creation requests, so it is safe to request the same for multiple times
        collection.ensure_index(index_keys, name=index_name)


class QueryCacheCollectionCreator(object):
    def __init__(self, database):
        self.database = database

    def build(self, drop=False, collection_name='ngramQueryCache', size=100000, max=1000):
        exists = collection_name in self.database.collection_names()
        if drop and exists:
            self.database.drop_collection(collection_name)

        query_cache_collection = None
        if not exists:
            query_cache_collection = self.database.create_collection(collection_name, capped=True, size=100000, max=1000)   # max N documents!
        else:
            query_cache_collection = self.database[collection_name]

        query_cache_collection.ensure_index([('query', pymongo.ASCENDING)], unique=True)

        return query_cache_collection