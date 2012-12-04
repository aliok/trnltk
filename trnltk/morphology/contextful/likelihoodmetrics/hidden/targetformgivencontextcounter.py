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
from trnltk.morphology.contextful.likelihoodmetrics.hidden.query import QueryExecutionContextBuilder, QueryExecutor, WordNGramQueryContainer, CachingQueryExecutionContext, CachingQueryExecutor, InMemoryCachingQueryExecutor

class TargetFormGivenContextCounter(object):
    def __init__(self, collection_map):
        self._collection_map = collection_map

    def _count_target_form_given_context(self, target, context, target_comes_after, target_appender, context_appender):
        query_container = WordNGramQueryContainer(len(context) + 1) if target_appender else WordNGramQueryContainer(len(context))
        params = []

        if target_appender:
            target_appender.append(target, query_container, params)
        for context_item in context:
            context_appender.append(context_item, query_container, params)

        return self._find_count_for_query(params, query_container, target_comes_after)

    def _find_count_for_query(self, params, query_container, target_comes_after):
        query_execution_context = QueryExecutionContextBuilder(self._collection_map).create_context(query_container, target_comes_after)
        return QueryExecutor().query_execution_context(query_execution_context).params(*params).count()

class CachingTargetFormGivenContextCounter(TargetFormGivenContextCounter):
    def __init__(self, collection_map, query_cache_collection):
        super(CachingTargetFormGivenContextCounter, self).__init__(collection_map)
        self._query_cache_collection = query_cache_collection
        # TODO: how about an index for query_cache_collection?

    def _find_count_for_query(self, params, query_container, target_comes_after):
        query_execution_context = QueryExecutionContextBuilder(self._collection_map).create_context(query_container, target_comes_after)
        caching_query_execution_context = CachingQueryExecutionContext(query_execution_context.keys, query_execution_context.collection, self._query_cache_collection)
        return CachingQueryExecutor().query_execution_context(caching_query_execution_context).params(*params).count()

class InMemoryCachingTargetFormGivenContextCounter(TargetFormGivenContextCounter):
    def __init__(self, collection_map):
        super(InMemoryCachingTargetFormGivenContextCounter, self).__init__(collection_map)

    def _find_count_for_query(self, params, query_container, target_comes_after):
        query_execution_context = QueryExecutionContextBuilder(self._collection_map).create_context(query_container, target_comes_after)
        return InMemoryCachingQueryExecutor().query_execution_context(query_execution_context).params(*params).count()