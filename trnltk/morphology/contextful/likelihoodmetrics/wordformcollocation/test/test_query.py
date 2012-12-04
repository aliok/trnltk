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
import unittest
from hamcrest import *
from mock import Mock
from trnltk.morphology.contextful.likelihoodmetrics.hidden.query import WordNGramQueryContainer, QueryExecutor, QueryExecutionContext, QueryExecutionContextBuilder, QueryExecutionIndexContextBuilder

class WordNGramQueryContainerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def test_add_criterion(self):
        self.assertRaises(AssertionError, lambda: WordNGramQueryContainer(-1))
        self.assertRaises(AssertionError, lambda: WordNGramQueryContainer(0))

        assert_that(str(WordNGramQueryContainer(1).target_surface().target_item), equal_to("(surface)"))
        assert_that(str(WordNGramQueryContainer(1).target_surface(False).target_item), equal_to("(surface)"))
        assert_that(str(WordNGramQueryContainer(1).target_surface(True).target_item), equal_to("(surface, syntactic_category)"))

        assert_that(str(WordNGramQueryContainer(2).target_surface().target_item), equal_to("(surface)"))
        assert_that(str(WordNGramQueryContainer(2).target_surface(False).target_item), equal_to("(surface)"))
        assert_that(str(WordNGramQueryContainer(2).target_surface(True).target_item), equal_to("(surface, syntactic_category)"))

        assert_that(str(WordNGramQueryContainer(2).target_surface().given_stem().target_item), equal_to("(surface)"))
        assert_that(str(WordNGramQueryContainer(2).target_surface(False).given_stem(False).target_item), equal_to("(surface)"))
        assert_that(str(WordNGramQueryContainer(2).target_surface(False).given_stem(True).target_item), equal_to("(surface)"))
        assert_that(str(WordNGramQueryContainer(2).target_surface(True).given_stem(True).target_item), equal_to("(surface, syntactic_category)"))

        assert_that(str(WordNGramQueryContainer(2).target_surface().given_items), equal_to("[]"))
        assert_that(str(WordNGramQueryContainer(2).target_surface(False).given_items), equal_to("[]"))
        assert_that(str(WordNGramQueryContainer(2).target_surface(True).given_items), equal_to("[]"))

        assert_that(str(WordNGramQueryContainer(2).target_surface().given_stem().given_items), equal_to("[(stem)]"))
        assert_that(str(WordNGramQueryContainer(2).target_surface(False).given_stem(False).given_items), equal_to("[(stem)]"))
        assert_that(str(WordNGramQueryContainer(2).target_surface(False).given_stem(True).given_items), equal_to("[(stem, syntactic_category)]"))
        assert_that(str(WordNGramQueryContainer(2).target_surface(True).given_stem(True).given_items), equal_to("[(stem, syntactic_category)]"))

        assert_that(str(WordNGramQueryContainer(2).target_surface().given_items), equal_to("[]"))
        assert_that(str(WordNGramQueryContainer(2).target_surface(False).given_items), equal_to("[]"))
        assert_that(str(WordNGramQueryContainer(2).target_surface(True).given_items), equal_to("[]"))

        assert_that(str(WordNGramQueryContainer(2).target_surface().given_stem().given_items), equal_to("[(stem)]"))
        assert_that(str(WordNGramQueryContainer(2).target_surface(False).given_stem(False).given_items), equal_to("[(stem)]"))
        assert_that(str(WordNGramQueryContainer(2).target_surface(False).given_stem(True).given_items), equal_to("[(stem, syntactic_category)]"))
        assert_that(str(WordNGramQueryContainer(2).target_surface(True).given_stem(True).given_items), equal_to("[(stem, syntactic_category)]"))



        assert_that(str(WordNGramQueryContainer(3).target_surface().given_items), equal_to("[]"))
        assert_that(str(WordNGramQueryContainer(3).target_surface(False).given_items), equal_to("[]"))
        assert_that(str(WordNGramQueryContainer(3).target_surface(True).given_items), equal_to("[]"))

        assert_that(str(WordNGramQueryContainer(3).target_surface().given_stem().given_stem().given_items), equal_to("[(stem), (stem)]"))
        assert_that(str(WordNGramQueryContainer(3).target_surface(False).given_stem(True).given_stem().given_items), equal_to("[(stem, syntactic_category), (stem)]"))
        assert_that(str(WordNGramQueryContainer(3).target_surface(False).given_stem(True).given_stem(True).given_items), equal_to("[(stem, syntactic_category), (stem, syntactic_category)]"))
        assert_that(str(WordNGramQueryContainer(3).target_surface(True).given_stem(False).given_stem(True).given_items), equal_to("[(stem), (stem, syntactic_category)]"))

class QueryExecutionContextBuilderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.unigram_collection = Mock(name="unigram_collection")
        cls.bigram_collection = Mock(name="bigram_collection")
        cls.trigram_collection = Mock(name="trigram_collection")
        cls.fourgram_collection = Mock("fourgram_collection")

        cls.collection_map = {
            1: cls.unigram_collection,
            2: cls.bigram_collection,
            3: cls.trigram_collection,
            4: cls.fourgram_collection
        }

    def test_create_context_keys_without_given(self):
        query_execution_context = QueryExecutionContextBuilder(self.collection_map).create_context(WordNGramQueryContainer(1).target_surface(False), False)
        assert_that(query_execution_context.keys, equal_to(["item_0.word.surface.value"]))
        assert_that(query_execution_context.collection, is_(self.unigram_collection))

        query_execution_context = QueryExecutionContextBuilder(self.collection_map).create_context(WordNGramQueryContainer(1).target_surface(False), True)
        assert_that(query_execution_context.keys, equal_to(["item_0.word.surface.value"]))
        assert_that(query_execution_context.collection, is_(self.unigram_collection))


        query_execution_context = QueryExecutionContextBuilder(self.collection_map).create_context(WordNGramQueryContainer(1).target_surface(True), False)
        assert_that(query_execution_context.keys, equal_to(["item_0.word.surface.value", "item_0.word.surface.syntactic_category"]))
        assert_that(query_execution_context.collection, is_(self.unigram_collection))

        query_execution_context = QueryExecutionContextBuilder(self.collection_map).create_context(WordNGramQueryContainer(1).target_surface(True), True)
        assert_that(query_execution_context.keys, equal_to(["item_0.word.surface.value", "item_0.word.surface.syntactic_category"]))
        assert_that(query_execution_context.collection, is_(self.unigram_collection))


        query_execution_context = QueryExecutionContextBuilder(self.collection_map).create_context(WordNGramQueryContainer(1).target_surface(False), False)
        assert_that(query_execution_context.keys, equal_to(["item_0.word.surface.value"]))
        assert_that(query_execution_context.collection, is_(self.unigram_collection))

        query_execution_context = QueryExecutionContextBuilder(self.collection_map).create_context(WordNGramQueryContainer(1).target_surface(False), True)
        assert_that(query_execution_context.keys, equal_to(["item_0.word.surface.value"]))
        assert_that(query_execution_context.collection, is_(self.unigram_collection))

    def test_create_context_keys_without_target(self):
        query_execution_context = QueryExecutionContextBuilder(self.collection_map).create_context(WordNGramQueryContainer(1).given_surface(False), False)
        assert_that(query_execution_context.keys, equal_to(["item_0.word.surface.value"]))
        assert_that(query_execution_context.collection, is_(self.unigram_collection))

        query_execution_context = QueryExecutionContextBuilder(self.collection_map).create_context(WordNGramQueryContainer(1).given_surface(False), True)
        assert_that(query_execution_context.keys, equal_to(["item_0.word.surface.value"]))
        assert_that(query_execution_context.collection, is_(self.unigram_collection))


        query_execution_context = QueryExecutionContextBuilder(self.collection_map).create_context(WordNGramQueryContainer(2).given_surface(True).given_surface(True), False)
        assert_that(query_execution_context.keys, equal_to(['item_0.word.surface.value', 'item_0.word.surface.syntactic_category', 'item_1.word.surface.value', 'item_1.word.surface.syntactic_category']))
        assert_that(query_execution_context.collection, is_(self.bigram_collection))

        query_execution_context = QueryExecutionContextBuilder(self.collection_map).create_context(WordNGramQueryContainer(2).given_surface(True).given_surface(False), False)
        assert_that(query_execution_context.keys, equal_to(['item_0.word.surface.value', 'item_0.word.surface.syntactic_category', 'item_1.word.surface.value']))
        assert_that(query_execution_context.collection, is_(self.bigram_collection))


        query_execution_context = QueryExecutionContextBuilder(self.collection_map).create_context(WordNGramQueryContainer(2).given_surface(False).given_surface(True), False)
        assert_that(query_execution_context.keys, equal_to(['item_0.word.surface.value', 'item_1.word.surface.value', 'item_1.word.surface.syntactic_category']))
        assert_that(query_execution_context.collection, is_(self.bigram_collection))

        query_execution_context = QueryExecutionContextBuilder(self.collection_map).create_context(WordNGramQueryContainer(2).given_surface(False).given_surface(False), True)
        assert_that(query_execution_context.keys, equal_to(['item_0.word.surface.value', 'item_1.word.surface.value']))
        assert_that(query_execution_context.collection, is_(self.bigram_collection))


    def test_create_context_keys_with_target_and_given(self):
        query_execution_context = QueryExecutionContextBuilder(self.collection_map).create_context(WordNGramQueryContainer(2).target_surface(False).given_surface(False), False)
        assert_that(query_execution_context.keys, equal_to(['item_0.word.surface.value', 'item_1.word.surface.value']))
        assert_that(query_execution_context.collection, is_(self.bigram_collection))

        query_execution_context = QueryExecutionContextBuilder(self.collection_map).create_context(WordNGramQueryContainer(2).target_surface(True ).given_surface(False), True)
        assert_that(query_execution_context.keys, equal_to(['item_1.word.surface.value', 'item_1.word.surface.syntactic_category', 'item_0.word.surface.value']))
        assert_that(query_execution_context.collection, is_(self.bigram_collection))


        query_execution_context = QueryExecutionContextBuilder(self.collection_map).create_context(WordNGramQueryContainer(2).target_surface(False).given_surface(True ), False)
        assert_that(query_execution_context.keys, equal_to(['item_0.word.surface.value', 'item_1.word.surface.value', 'item_1.word.surface.syntactic_category']))
        assert_that(query_execution_context.collection, is_(self.bigram_collection))

        query_execution_context = QueryExecutionContextBuilder(self.collection_map).create_context(WordNGramQueryContainer(2).target_surface(False).given_surface(True ), True)
        assert_that(query_execution_context.keys, equal_to(['item_1.word.surface.value', 'item_0.word.surface.value', 'item_0.word.surface.syntactic_category']))
        assert_that(query_execution_context.collection, is_(self.bigram_collection))


        query_execution_context = QueryExecutionContextBuilder(self.collection_map).create_context(WordNGramQueryContainer(3).target_surface(True ).given_surface(False).given_stem(False), False)
        assert_that(query_execution_context.keys, equal_to(['item_0.word.surface.value', 'item_0.word.surface.syntactic_category', 'item_1.word.surface.value', 'item_2.word.stem.value']))
        assert_that(query_execution_context.collection, is_(self.trigram_collection))

        query_execution_context = QueryExecutionContextBuilder(self.collection_map).create_context(WordNGramQueryContainer(3).target_surface(True ).given_surface(False).given_stem(True ), True)
        assert_that(query_execution_context.keys, equal_to(['item_2.word.surface.value', 'item_2.word.surface.syntactic_category', 'item_0.word.surface.value', 'item_1.word.stem.value', 'item_1.word.stem.syntactic_category']))
        assert_that(query_execution_context.collection, is_(self.trigram_collection))


        query_execution_context = QueryExecutionContextBuilder(self.collection_map).create_context(WordNGramQueryContainer(3).target_surface(False).given_surface(True ).given_stem(False), False)
        assert_that(query_execution_context.keys, equal_to(['item_0.word.surface.value', 'item_1.word.surface.value', 'item_1.word.surface.syntactic_category', 'item_2.word.stem.value']))
        assert_that(query_execution_context.collection, is_(self.trigram_collection))

        query_execution_context = QueryExecutionContextBuilder(self.collection_map).create_context(WordNGramQueryContainer(3).target_surface(False).given_surface(True ).given_stem(False), True)
        assert_that(query_execution_context.keys, equal_to(['item_2.word.surface.value', 'item_0.word.surface.value', 'item_0.word.surface.syntactic_category', 'item_1.word.stem.value']))
        assert_that(query_execution_context.collection, is_(self.trigram_collection))


        query_execution_context = QueryExecutionContextBuilder(self.collection_map).create_context(WordNGramQueryContainer(4).target_surface(False).given_surface(True ).given_stem(False).given_lemma_root(False), False)
        assert_that(query_execution_context.keys, equal_to(['item_0.word.surface.value', 'item_1.word.surface.value', 'item_1.word.surface.syntactic_category', 'item_2.word.stem.value', 'item_3.word.lemma_root.value']))
        assert_that(query_execution_context.collection, is_(self.fourgram_collection))

        query_execution_context = QueryExecutionContextBuilder(self.collection_map).create_context(WordNGramQueryContainer(4).target_surface(True ).given_surface(True ).given_stem(False).given_lemma_root(True), True)
        assert_that(query_execution_context.keys, equal_to(['item_3.word.surface.value', 'item_3.word.surface.syntactic_category', 'item_0.word.surface.value', 'item_0.word.surface.syntactic_category', 'item_1.word.stem.value', 'item_2.word.lemma_root.value', 'item_2.word.lemma_root.syntactic_category']))
        assert_that(query_execution_context.collection, is_(self.fourgram_collection))


class QueryExecutionIndexContextBuilderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.unigram_collection = Mock(name="unigram_collection")
        cls.bigram_collection = Mock(name="bigram_collection")
        cls.trigram_collection = Mock(name="trigram_collection")
        cls.fourgram_collection = Mock("fourgram_collection")

        cls.collection_map = {
            1: cls.unigram_collection,
            2: cls.bigram_collection,
            3: cls.trigram_collection,
            4: cls.fourgram_collection
        }

    def test_create_context_keys_and_index_without_given(self):
        query_execution_context = QueryExecutionIndexContextBuilder().create_context(self.unigram_collection, WordNGramQueryContainer(1).target_surface(False), False)
        assert_that(query_execution_context.keys, equal_to(["item_0.word.surface.value"]))
        assert_that(query_execution_context.collection, is_(self.unigram_collection))
        assert_that(query_execution_context.index_name, equal_to("word1GramIdx_0_surface"))

        query_execution_context = QueryExecutionIndexContextBuilder().create_context(self.unigram_collection, WordNGramQueryContainer(1).target_surface(False), True)
        assert_that(query_execution_context.keys, equal_to(["item_0.word.surface.value"]))
        assert_that(query_execution_context.collection, is_(self.unigram_collection))
        assert_that(query_execution_context.index_name, equal_to("word1GramIdx_0_surface"))


        query_execution_context = QueryExecutionIndexContextBuilder().create_context(self.unigram_collection, WordNGramQueryContainer(1).target_surface(True), False)
        assert_that(query_execution_context.keys, equal_to(["item_0.word.surface.value", "item_0.word.surface.syntactic_category"]))
        assert_that(query_execution_context.collection, is_(self.unigram_collection))
        assert_that(query_execution_context.index_name, equal_to("word1GramIdx_0_surface_cat"))

        query_execution_context = QueryExecutionIndexContextBuilder().create_context(self.unigram_collection, WordNGramQueryContainer(1).target_surface(True), True)
        assert_that(query_execution_context.keys, equal_to(["item_0.word.surface.value", "item_0.word.surface.syntactic_category"]))
        assert_that(query_execution_context.collection, is_(self.unigram_collection))
        assert_that(query_execution_context.index_name, equal_to("word1GramIdx_0_surface_cat"))


        query_execution_context = QueryExecutionIndexContextBuilder().create_context(self.unigram_collection, WordNGramQueryContainer(1).target_surface(False), False)
        assert_that(query_execution_context.keys, equal_to(["item_0.word.surface.value"]))
        assert_that(query_execution_context.collection, is_(self.unigram_collection))
        assert_that(query_execution_context.index_name, equal_to("word1GramIdx_0_surface"))

        query_execution_context = QueryExecutionIndexContextBuilder().create_context(self.unigram_collection, WordNGramQueryContainer(1).target_surface(False), True)
        assert_that(query_execution_context.keys, equal_to(["item_0.word.surface.value"]))
        assert_that(query_execution_context.collection, is_(self.unigram_collection))
        assert_that(query_execution_context.index_name, equal_to("word1GramIdx_0_surface"))

    def test_create_context_keys_and_index_without_target(self):
        query_execution_context = QueryExecutionIndexContextBuilder().create_context(self.unigram_collection, WordNGramQueryContainer(1).given_surface(False), False)
        assert_that(query_execution_context.keys, equal_to(["item_0.word.surface.value"]))
        assert_that(query_execution_context.collection, is_(self.unigram_collection))
        assert_that(query_execution_context.index_name, equal_to("word1GramIdx_0_surface"))

        query_execution_context = QueryExecutionIndexContextBuilder().create_context(self.unigram_collection, WordNGramQueryContainer(1).given_surface(False), True)
        assert_that(query_execution_context.keys, equal_to(["item_0.word.surface.value"]))
        assert_that(query_execution_context.collection, is_(self.unigram_collection))
        assert_that(query_execution_context.index_name, equal_to("word1GramIdx_0_surface"))


        query_execution_context = QueryExecutionIndexContextBuilder().create_context(self.bigram_collection, WordNGramQueryContainer(2).given_surface(True).given_surface(True), False)
        assert_that(query_execution_context.keys, equal_to(['item_0.word.surface.value', 'item_0.word.surface.syntactic_category', 'item_1.word.surface.value', 'item_1.word.surface.syntactic_category']))
        assert_that(query_execution_context.collection, is_(self.bigram_collection))
        assert_that(query_execution_context.index_name, equal_to("word2GramIdx_0_surface_cat_1_surface_cat"))

        query_execution_context = QueryExecutionIndexContextBuilder().create_context(self.bigram_collection, WordNGramQueryContainer(2).given_surface(True).given_surface(False), False)
        assert_that(query_execution_context.keys, equal_to(['item_0.word.surface.value', 'item_0.word.surface.syntactic_category', 'item_1.word.surface.value']))
        assert_that(query_execution_context.collection, is_(self.bigram_collection))
        assert_that(query_execution_context.index_name, equal_to("word2GramIdx_0_surface_cat_1_surface"))


        query_execution_context = QueryExecutionIndexContextBuilder().create_context(self.bigram_collection, WordNGramQueryContainer(2).given_surface(False).given_surface(True), False)
        assert_that(query_execution_context.keys, equal_to(['item_0.word.surface.value', 'item_1.word.surface.value', 'item_1.word.surface.syntactic_category']))
        assert_that(query_execution_context.collection, is_(self.bigram_collection))
        assert_that(query_execution_context.index_name, equal_to("word2GramIdx_0_surface_1_surface_cat"))

        query_execution_context = QueryExecutionIndexContextBuilder().create_context(self.bigram_collection, WordNGramQueryContainer(2).given_surface(False).given_surface(False), True)
        assert_that(query_execution_context.keys, equal_to(['item_0.word.surface.value', 'item_1.word.surface.value']))
        assert_that(query_execution_context.collection, is_(self.bigram_collection))
        assert_that(query_execution_context.index_name, equal_to("word2GramIdx_0_surface_1_surface"))


    def test_create_context_keys_and_index_with_target_and_given(self):
        query_execution_context = QueryExecutionIndexContextBuilder().create_context(self.bigram_collection, WordNGramQueryContainer(2).target_surface(False).given_surface(False), False)
        assert_that(query_execution_context.keys, equal_to(['item_0.word.surface.value', 'item_1.word.surface.value']))
        assert_that(query_execution_context.collection, is_(self.bigram_collection))
        assert_that(query_execution_context.index_name, equal_to("word2GramIdx_0_surface_1_surface"))


        query_execution_context = QueryExecutionIndexContextBuilder().create_context(self.bigram_collection, WordNGramQueryContainer(2).target_surface(True ).given_surface(False), True)
        assert_that(query_execution_context.keys, equal_to(['item_1.word.surface.value', 'item_1.word.surface.syntactic_category', 'item_0.word.surface.value']))
        assert_that(query_execution_context.collection, is_(self.bigram_collection))
        assert_that(query_execution_context.index_name, equal_to("word2GramIdx_1_surface_cat_0_surface"))


        query_execution_context = QueryExecutionIndexContextBuilder().create_context(self.bigram_collection, WordNGramQueryContainer(2).target_surface(False).given_surface(True ), False)
        assert_that(query_execution_context.keys, equal_to(['item_0.word.surface.value', 'item_1.word.surface.value', 'item_1.word.surface.syntactic_category']))
        assert_that(query_execution_context.collection, is_(self.bigram_collection))
        assert_that(query_execution_context.index_name, equal_to("word2GramIdx_0_surface_1_surface_cat"))

        query_execution_context = QueryExecutionIndexContextBuilder().create_context(self.bigram_collection, WordNGramQueryContainer(2).target_surface(False).given_surface(True ), True)
        assert_that(query_execution_context.keys, equal_to(['item_1.word.surface.value', 'item_0.word.surface.value', 'item_0.word.surface.syntactic_category']))
        assert_that(query_execution_context.collection, is_(self.bigram_collection))
        assert_that(query_execution_context.index_name, equal_to("word2GramIdx_1_surface_0_surface_cat"))


        query_execution_context = QueryExecutionIndexContextBuilder().create_context(self.trigram_collection, WordNGramQueryContainer(3).target_surface(True ).given_surface(False).given_stem(False), False)
        assert_that(query_execution_context.keys, equal_to(['item_0.word.surface.value', 'item_0.word.surface.syntactic_category', 'item_1.word.surface.value', 'item_2.word.stem.value']))
        assert_that(query_execution_context.collection, is_(self.trigram_collection))
        assert_that(query_execution_context.index_name, equal_to("word3GramIdx_0_surface_cat_1_surface_2_stem"))

        query_execution_context = QueryExecutionIndexContextBuilder().create_context(self.trigram_collection, WordNGramQueryContainer(3).target_surface(True ).given_surface(False).given_stem(True ), True)
        assert_that(query_execution_context.keys, equal_to(['item_2.word.surface.value', 'item_2.word.surface.syntactic_category', 'item_0.word.surface.value', 'item_1.word.stem.value', 'item_1.word.stem.syntactic_category']))
        assert_that(query_execution_context.collection, is_(self.trigram_collection))
        assert_that(query_execution_context.index_name, equal_to("word3GramIdx_2_surface_cat_0_surface_1_stem_cat"))


        query_execution_context = QueryExecutionIndexContextBuilder().create_context(self.trigram_collection, WordNGramQueryContainer(3).target_surface(False).given_surface(True ).given_stem(False), False)
        assert_that(query_execution_context.keys, equal_to(['item_0.word.surface.value', 'item_1.word.surface.value', 'item_1.word.surface.syntactic_category', 'item_2.word.stem.value']))
        assert_that(query_execution_context.collection, is_(self.trigram_collection))
        assert_that(query_execution_context.index_name, equal_to("word3GramIdx_0_surface_1_surface_cat_2_stem"))

        query_execution_context = QueryExecutionIndexContextBuilder().create_context(self.trigram_collection, WordNGramQueryContainer(3).target_surface(False).given_surface(True ).given_stem(False), True)
        assert_that(query_execution_context.keys, equal_to(['item_2.word.surface.value', 'item_0.word.surface.value', 'item_0.word.surface.syntactic_category', 'item_1.word.stem.value']))
        assert_that(query_execution_context.collection, is_(self.trigram_collection))
        assert_that(query_execution_context.index_name, equal_to("word3GramIdx_2_surface_0_surface_cat_1_stem"))


        query_execution_context = QueryExecutionIndexContextBuilder().create_context(self.fourgram_collection, WordNGramQueryContainer(4).target_surface(False).given_surface(True ).given_stem(False).given_lemma_root(False), False)
        assert_that(query_execution_context.keys, equal_to(['item_0.word.surface.value', 'item_1.word.surface.value', 'item_1.word.surface.syntactic_category', 'item_2.word.stem.value', 'item_3.word.lemma_root.value']))
        assert_that(query_execution_context.collection, is_(self.fourgram_collection))
        assert_that(query_execution_context.index_name, equal_to("word4GramIdx_0_surface_1_surface_cat_2_stem_3_lemma_root"))

        query_execution_context = QueryExecutionIndexContextBuilder().create_context(self.fourgram_collection, WordNGramQueryContainer(4).target_surface(True ).given_surface(True ).given_stem(False).given_lemma_root(True), True)
        assert_that(query_execution_context.keys, equal_to(['item_3.word.surface.value', 'item_3.word.surface.syntactic_category', 'item_0.word.surface.value', 'item_0.word.surface.syntactic_category', 'item_1.word.stem.value', 'item_2.word.lemma_root.value', 'item_2.word.lemma_root.syntactic_category']))
        assert_that(query_execution_context.collection, is_(self.fourgram_collection))
        assert_that(query_execution_context.index_name, equal_to("word4GramIdx_3_surface_cat_0_surface_cat_1_stem_2_lemma_root_cat"))

class QueryExecutorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def test_build_query_with_invalid_params(self):
        mock_collection = Mock()
        mock_collection.full_name = 'Mock_Collection'

        query_execution_context = QueryExecutionContext(["key1", "key2"], mock_collection)
        self.assertRaises(AssertionError, lambda : QueryExecutor().query_execution_context(query_execution_context).params()._build_query_with_params())
        self.assertRaises(AssertionError, lambda : QueryExecutor().query_execution_context(query_execution_context).params("1")._build_query_with_params())
        self.assertRaises(AssertionError, lambda : QueryExecutor().query_execution_context(query_execution_context).params("1", "2", "3")._build_query_with_params())

    def test_build_query_with_params(self):
        mock_collection = Mock()
        mock_collection.full_name = 'Mock_Collection'

        query_execution_context = QueryExecutionContext(["key1", "key2"], mock_collection)
        query_with_params = QueryExecutor().query_execution_context(query_execution_context).params("1", "2")._build_query_with_params()
        assert_that(query_with_params, has_length(2))
        assert_that(query_with_params, has_entry("key1", "1"))
        assert_that(query_with_params, has_entry("key2", "2"))


if __name__ == '__main__':
    unittest.main()
