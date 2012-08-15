# coding=utf-8
import unittest
from hamcrest import *
from mock import Mock
from trnltk.statistics.query import WordNGramQueryContainer, QueryBuilder, QueryExecutor, QueryExecutionContext

class WordNGramQueryContainerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def test_add_criterion(self):
        self.assertRaises(AssertionError, lambda: WordNGramQueryContainer(-1))
        self.assertRaises(AssertionError, lambda: WordNGramQueryContainer(0))

        assert_that(str(WordNGramQueryContainer(1).target_surface()._target_item), equal_to("(surface)"))
        assert_that(str(WordNGramQueryContainer(1).target_surface(False)._target_item), equal_to("(surface)"))
        assert_that(str(WordNGramQueryContainer(1).target_surface(True)._target_item), equal_to("(surface, syntactic_category)"))

        assert_that(str(WordNGramQueryContainer(2).target_surface()._target_item), equal_to("(surface)"))
        assert_that(str(WordNGramQueryContainer(2).target_surface(False)._target_item), equal_to("(surface)"))
        assert_that(str(WordNGramQueryContainer(2).target_surface(True)._target_item), equal_to("(surface, syntactic_category)"))

        assert_that(str(WordNGramQueryContainer(2).target_surface().given_stem()._target_item), equal_to("(surface)"))
        assert_that(str(WordNGramQueryContainer(2).target_surface(False).given_stem(False)._target_item), equal_to("(surface)"))
        assert_that(str(WordNGramQueryContainer(2).target_surface(False).given_stem(True)._target_item), equal_to("(surface)"))
        assert_that(str(WordNGramQueryContainer(2).target_surface(True).given_stem(True)._target_item), equal_to("(surface, syntactic_category)"))

        assert_that(str(WordNGramQueryContainer(2).target_surface()._given_items), equal_to("[]"))
        assert_that(str(WordNGramQueryContainer(2).target_surface(False)._given_items), equal_to("[]"))
        assert_that(str(WordNGramQueryContainer(2).target_surface(True)._given_items), equal_to("[]"))

        assert_that(str(WordNGramQueryContainer(2).target_surface().given_stem()._given_items), equal_to("[(stem)]"))
        assert_that(str(WordNGramQueryContainer(2).target_surface(False).given_stem(False)._given_items), equal_to("[(stem)]"))
        assert_that(str(WordNGramQueryContainer(2).target_surface(False).given_stem(True)._given_items), equal_to("[(stem, syntactic_category)]"))
        assert_that(str(WordNGramQueryContainer(2).target_surface(True).given_stem(True)._given_items), equal_to("[(stem, syntactic_category)]"))

        assert_that(str(WordNGramQueryContainer(2).target_surface()._given_items), equal_to("[]"))
        assert_that(str(WordNGramQueryContainer(2).target_surface(False)._given_items), equal_to("[]"))
        assert_that(str(WordNGramQueryContainer(2).target_surface(True)._given_items), equal_to("[]"))

        assert_that(str(WordNGramQueryContainer(2).target_surface().given_stem()._given_items), equal_to("[(stem)]"))
        assert_that(str(WordNGramQueryContainer(2).target_surface(False).given_stem(False)._given_items), equal_to("[(stem)]"))
        assert_that(str(WordNGramQueryContainer(2).target_surface(False).given_stem(True)._given_items), equal_to("[(stem, syntactic_category)]"))
        assert_that(str(WordNGramQueryContainer(2).target_surface(True).given_stem(True)._given_items), equal_to("[(stem, syntactic_category)]"))



        assert_that(str(WordNGramQueryContainer(3).target_surface()._given_items), equal_to("[]"))
        assert_that(str(WordNGramQueryContainer(3).target_surface(False)._given_items), equal_to("[]"))
        assert_that(str(WordNGramQueryContainer(3).target_surface(True)._given_items), equal_to("[]"))

        assert_that(str(WordNGramQueryContainer(3).target_surface().given_stem().given_stem()._given_items), equal_to("[(stem), (stem)]"))
        assert_that(str(WordNGramQueryContainer(3).target_surface(False).given_stem(True).given_stem()._given_items), equal_to("[(stem, syntactic_category), (stem)]"))
        assert_that(str(WordNGramQueryContainer(3).target_surface(False).given_stem(True).given_stem(True)._given_items), equal_to("[(stem, syntactic_category), (stem, syntactic_category)]"))
        assert_that(str(WordNGramQueryContainer(3).target_surface(True).given_stem(False).given_stem(True)._given_items), equal_to("[(stem), (stem, syntactic_category)]"))

    def test_create_context_index_name_without_given(self):
        assert_that(WordNGramQueryContainer(1).target_surface(False).create_context(False)[0], equal_to("word1GramIdx_0_surface"))
        assert_that(WordNGramQueryContainer(1).target_surface(False).create_context(True )[0], equal_to("word1GramIdx_0_surface"))

        assert_that(WordNGramQueryContainer(1).target_surface(True ).create_context(False)[0], equal_to("word1GramIdx_0_surface_cat"))
        assert_that(WordNGramQueryContainer(1).target_surface(True ).create_context(True )[0], equal_to("word1GramIdx_0_surface_cat"))

        assert_that(WordNGramQueryContainer(1).target_surface(False).create_context(False)[0], equal_to("word1GramIdx_0_surface"))
        assert_that(WordNGramQueryContainer(1).target_surface(False).create_context(True )[0], equal_to("word1GramIdx_0_surface"))

    def test_create_context_index_name_without_target(self):
        assert_that(WordNGramQueryContainer(1).given_surface(False).create_context(False)[0], equal_to("word1GramIdx_0_surface"))
        assert_that(WordNGramQueryContainer(1).given_surface(False).create_context(True )[0], equal_to("word1GramIdx_0_surface"))

        assert_that(WordNGramQueryContainer(2).given_surface(True ).given_surface(True ).create_context(False)[0], equal_to("word2GramIdx_0_surface_cat_1_surface_cat"))
        assert_that(WordNGramQueryContainer(2).given_surface(True ).given_surface(False).create_context(True )[0], equal_to("word2GramIdx_0_surface_cat_1_surface"))

        assert_that(WordNGramQueryContainer(3).given_surface(True ).given_surface(False).given_surface(True ).create_context(False)[0], equal_to("word3GramIdx_0_surface_cat_1_surface_2_surface_cat"))
        assert_that(WordNGramQueryContainer(3).given_surface(True ).given_surface(False).given_surface(False).create_context(True )[0], equal_to("word3GramIdx_0_surface_cat_1_surface_2_surface"))

    def test_create_context_index_name_with_target_and_given(self):
        assert_that(WordNGramQueryContainer(2).target_surface(False).given_surface(False).create_context(False)[0], equal_to("word2GramIdx_0_surface_1_surface"))
        assert_that(WordNGramQueryContainer(2).target_surface(True ).given_surface(False).create_context(True )[0], equal_to("word2GramIdx_1_surface_cat_0_surface"))

        assert_that(WordNGramQueryContainer(2).target_surface(False).given_surface(True ).create_context(False)[0], equal_to("word2GramIdx_0_surface_1_surface_cat"))
        assert_that(WordNGramQueryContainer(2).target_surface(False).given_surface(True ).create_context(True )[0], equal_to("word2GramIdx_1_surface_0_surface_cat"))

        assert_that(WordNGramQueryContainer(3).target_surface(True ).given_surface(False).given_stem(False).create_context(False)[0], equal_to("word3GramIdx_0_surface_cat_1_surface_2_stem"))
        assert_that(WordNGramQueryContainer(3).target_surface(True ).given_surface(False).given_stem(True ).create_context(True )[0], equal_to("word3GramIdx_2_surface_cat_0_surface_1_stem_cat"))

        assert_that(WordNGramQueryContainer(3).target_surface(False).given_surface(True ).given_stem(False).create_context(False)[0], equal_to("word3GramIdx_0_surface_1_surface_cat_2_stem"))
        assert_that(WordNGramQueryContainer(3).target_surface(False).given_surface(True ).given_stem(False).create_context(True )[0], equal_to("word3GramIdx_2_surface_0_surface_cat_1_stem"))

        assert_that(WordNGramQueryContainer(4).target_surface(False).given_surface(True ).given_stem(False).given_lemma_root(False).create_context(False)[0], equal_to("word4GramIdx_0_surface_1_surface_cat_2_stem_3_lemma_root"))
        assert_that(WordNGramQueryContainer(4).target_surface(True ).given_surface(True ).given_stem(False).given_lemma_root(True).create_context(True )[0], equal_to("word4GramIdx_3_surface_cat_0_surface_cat_1_stem_2_lemma_root_cat"))

    def test_create_context_keys_without_given(self):
        assert_that(WordNGramQueryContainer(1).target_surface(False).create_context(False)[1], equal_to(['item_0.word.surface.value']))
        assert_that(WordNGramQueryContainer(1).target_surface(False).create_context(True )[1], equal_to(['item_0.word.surface.value']))

        assert_that(WordNGramQueryContainer(1).target_surface(True ).create_context(False)[1], equal_to(['item_0.word.surface.value', 'item_0.word.surface.syntactic_category']))
        assert_that(WordNGramQueryContainer(1).target_surface(True ).create_context(True )[1], equal_to(['item_0.word.surface.value', 'item_0.word.surface.syntactic_category']))

        assert_that(WordNGramQueryContainer(1).target_surface(False).create_context(False)[1], equal_to(['item_0.word.surface.value']))
        assert_that(WordNGramQueryContainer(1).target_surface(False).create_context(True )[1], equal_to(['item_0.word.surface.value']))

    def test_create_context_keys_without_target(self):
        assert_that(WordNGramQueryContainer(1).given_surface(False).create_context(False)[1], equal_to(['item_0.word.surface.value']))
        assert_that(WordNGramQueryContainer(1).given_surface(False).create_context(True )[1], equal_to(['item_0.word.surface.value']))

        assert_that(WordNGramQueryContainer(2).given_surface(True ).given_surface(True ).create_context(False)[1], equal_to(['item_0.word.surface.value', 'item_0.word.surface.syntactic_category', 'item_1.word.surface.value', 'item_1.word.surface.syntactic_category']))
        assert_that(WordNGramQueryContainer(2).given_surface(True ).given_surface(False).create_context(True )[1], equal_to(['item_0.word.surface.value', 'item_0.word.surface.syntactic_category', 'item_1.word.surface.value']))

        assert_that(WordNGramQueryContainer(3).given_surface(True ).given_surface(False).given_surface(True ).create_context(False)[1], equal_to(['item_0.word.surface.value', 'item_0.word.surface.syntactic_category', 'item_1.word.surface.value', 'item_2.word.surface.value', 'item_2.word.surface.syntactic_category']))
        assert_that(WordNGramQueryContainer(3).given_surface(True ).given_surface(False).given_surface(False).create_context(True )[1], equal_to(['item_0.word.surface.value', 'item_0.word.surface.syntactic_category', 'item_1.word.surface.value', 'item_2.word.surface.value']))

    def test_create_context_index_name_with_target_and_given(self):
        assert_that(str(WordNGramQueryContainer(2).target_surface(False).given_surface(False).create_context(False)[1]), equal_to("['item_0.word.surface.value', 'item_1.word.surface.value']"))
        assert_that(str(WordNGramQueryContainer(2).target_surface(True ).given_surface(False).create_context(True )[1]), equal_to("['item_1.word.surface.value', 'item_1.word.surface.syntactic_category', 'item_0.word.surface.value']"))

        assert_that(str(WordNGramQueryContainer(2).target_surface(False).given_surface(True ).create_context(False)[1]), equal_to("['item_0.word.surface.value', 'item_1.word.surface.value', 'item_1.word.surface.syntactic_category']"))
        assert_that(str(WordNGramQueryContainer(2).target_surface(False).given_surface(True ).create_context(True )[1]), equal_to("['item_1.word.surface.value', 'item_0.word.surface.value', 'item_0.word.surface.syntactic_category']"))

        assert_that(str(WordNGramQueryContainer(3).target_surface(True ).given_surface(False).given_stem(False).create_context(False)[1]), equal_to("['item_0.word.surface.value', 'item_0.word.surface.syntactic_category', 'item_1.word.surface.value', 'item_2.word.stem.value']"))
        assert_that(str(WordNGramQueryContainer(3).target_surface(True ).given_surface(False).given_stem(True ).create_context(True )[1]), equal_to("['item_2.word.surface.value', 'item_2.word.surface.syntactic_category', 'item_0.word.surface.value', 'item_1.word.stem.value', 'item_1.word.stem.syntactic_category']"))

        assert_that(str(WordNGramQueryContainer(3).target_surface(False).given_surface(True ).given_stem(False).create_context(False)[1]), equal_to("['item_0.word.surface.value', 'item_1.word.surface.value', 'item_1.word.surface.syntactic_category', 'item_2.word.stem.value']"))
        assert_that(str(WordNGramQueryContainer(3).target_surface(False).given_surface(True ).given_stem(False).create_context(True )[1]), equal_to("['item_2.word.surface.value', 'item_0.word.surface.value', 'item_0.word.surface.syntactic_category', 'item_1.word.stem.value']"))

        assert_that(str(WordNGramQueryContainer(4).target_surface(False).given_surface(True ).given_stem(False).given_lemma_root(False).create_context(False)[1]), equal_to("['item_0.word.surface.value', 'item_1.word.surface.value', 'item_1.word.surface.syntactic_category', 'item_2.word.stem.value', 'item_3.word.lemma_root.value']"))
        assert_that(str(WordNGramQueryContainer(4).target_surface(True ).given_surface(True ).given_stem(False).given_lemma_root(True).create_context(True )[1]), equal_to("['item_3.word.surface.value', 'item_3.word.surface.syntactic_category', 'item_0.word.surface.value', 'item_0.word.surface.syntactic_category', 'item_1.word.stem.value', 'item_2.word.lemma_root.value', 'item_2.word.lemma_root.syntactic_category']"))

class QueryBuilderTest(unittest.TestCase):
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

        cls.query_builder = QueryBuilder(cls.collection_map)

    def test_build_query_for_unigram(self):
        mock_query_container = Mock()
        mock_query_container._n = 1
        mock_query_container.create_context.return_value = ("idx_name", ["key1", "key2"])

        query_execution_context = self.query_builder.build_query(mock_query_container, True)

        assert_that(query_execution_context.keys, equal_to(["key1", "key2"]))
        assert_that(query_execution_context.collection, is_(self.unigram_collection))

        self.unigram_collection.ensure_index.assert_called_with([('key1', 1), ('key2', 1)], drop_dups=True, name='idx_name')

    def test_build_query_for_bigram(self):
        mock_query_container = Mock()
        mock_query_container._n = 2
        mock_query_container.create_context.return_value = ("idx_name", ["key1", "key2"])

        query_execution_context = self.query_builder.build_query(mock_query_container, True)

        assert_that(query_execution_context.keys, equal_to(["key1", "key2"]))
        assert_that(query_execution_context.collection, is_(self.bigram_collection))

        self.bigram_collection.ensure_index.assert_called_with([('key1', 1), ('key2', 1)], drop_dups=True, name='idx_name')

    def test_build_query_for_trigram(self):
        mock_query_container = Mock()
        mock_query_container._n = 3
        mock_query_container.create_context.return_value = ("idx_name", ["key1", "key2"])

        query_execution_context = self.query_builder.build_query(mock_query_container, True)

        assert_that(query_execution_context.keys, equal_to(["key1", "key2"]))
        assert_that(query_execution_context.collection, is_(self.trigram_collection))

        self.trigram_collection.ensure_index.assert_called_with([('key1', 1), ('key2', 1)], drop_dups=True, name='idx_name')

class QueryExecutorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def test_build_query_with_invalid_params(self):
        query_execution_context = QueryExecutionContext(["key1", "key2"], None)
        self.assertRaises(AssertionError, lambda : QueryExecutor().query_execution_context(query_execution_context).params()._build_query_with_params())
        self.assertRaises(AssertionError, lambda : QueryExecutor().query_execution_context(query_execution_context).params("1")._build_query_with_params())
        self.assertRaises(AssertionError, lambda : QueryExecutor().query_execution_context(query_execution_context).params("1", "2", "3")._build_query_with_params())

    def test_build_query_with_params(self):
        query_execution_context = QueryExecutionContext(["key1", "key2"], None)
        query_with_params = QueryExecutor().query_execution_context(query_execution_context).params("1", "2")._build_query_with_params()
        assert_that(query_with_params, has_length(2))
        assert_that(query_with_params, has_entry("key1", "1"))
        assert_that(query_with_params, has_entry("key2", "2"))


if __name__ == '__main__':
    unittest.main()
