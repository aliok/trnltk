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
import pymongo
from trnltk.morphology.contextful.likelihoodmetrics.hidden.query import WordNGramQueryContainer, QueryExecutionIndexContextBuilder

logger = logging.getLogger('database')

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