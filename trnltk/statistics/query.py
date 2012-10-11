# coding=utf-8
import logging
import pymongo

logger = logging.getLogger('query')

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
        self._n = n
        self._target_item = None
        self._given_items = []

    def _add_given(self, type, include_syntactic_category=False):
        self._given_items.append(WordNGramQueryContainerItem(type, include_syntactic_category))
        return self

    def _add_target(self, type, include_syntactic_category=False):
        if self._target_item:
            raise Exception("Target item is already set!")
        self._target_item = WordNGramQueryContainerItem(type, include_syntactic_category)
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

    def create_context(self, target_comes_after):
        assert self._n == (1 if self._target_item else 0) + len(self._given_items)

        index_name = "word{}GramIdx".format(self._n)
        keys = []

        target_item_index = self._n - 1 if target_comes_after else 0
        item_index_range = range(0, target_item_index) if target_comes_after else range(1, self._n)

        if not self._target_item:
            target_item_index = -1
            item_index_range = range(0, self._n)

        if self._target_item:
            target_item_index_part, target_item_keys = self._build_key(self._target_item, target_item_index)
            keys.extend(target_item_keys)
            index_name += target_item_index_part

        for index, item in enumerate(self._given_items):
            item_index = item_index_range[index]
            item = self._given_items[index]
            item_index_part, item_keys = self._build_key(item, item_index)
            keys.extend(item_keys)
            index_name += item_index_part

        return index_name, keys

    def _build_key(self, query_item, index):
        index_part = "_{}_{}".format(index, query_item.str_type)
        keys = ["item_{}.word.{}.value".format(index, query_item.str_type)]
        if query_item.include_syntactic_category:
            keys.append("item_{}.word.{}.syntactic_category".format(index, query_item.str_type))
            index_part += "_cat"
        return index_part, keys


class QueryExecutionContext(object):
    def __init__(self, keys, collection):
        self.keys = keys
        self.collection = collection


class QueryBuilder(object):
    def __init__(self, collection_map):
        self._collection_map = collection_map

    def build_query(self, query_container, target_comes_after):
        index_name, keys = query_container.create_context(target_comes_after)
        collection = self._collection_map[query_container._n]

        index_keys = [(key, pymongo.ASCENDING) for key in keys]
        logger.log(logging.DEBUG, u'Creating index {} with keys: {}'.format(index_name, index_keys))
        created_index_name = collection.ensure_index(index_keys, name=index_name, drop_dups=True)
        if created_index_name:
            logger.log(logging.DEBUG, u'\tCreated index with name : ' + str(created_index_name))
        else:
            logger.log(logging.DEBUG, u'\tIndex already exists')

        return QueryExecutionContext(keys, collection)


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