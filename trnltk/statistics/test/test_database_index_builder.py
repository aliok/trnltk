# coding=utf-8
"""
There is no verification -yet- in test of this class.
The tests are there for making sure there is no run time exceptions
"""
import unittest
import pymongo
from trnltk.statistics.contextstats import   ContextWordAppender, ParseResultSurfaceAppender, ParseResultStemAppender, ParseResultLemmaRootAppender
from trnltk.statistics.query import  DatabaseIndexBuilder

class DatabaseIndexBuilderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(DatabaseIndexBuilderTest, cls).setUpClass()

        mongodb_connection = pymongo.Connection(host='127.0.0.1')

        cls.collection_map_for_N_1 = {
            1: mongodb_connection['trnltk']['wordUnigramsIndexBuilderTest']
        }

        cls.collection_map_for_N_2 = {
            1: mongodb_connection['trnltk']['wordUnigramsIndexBuilderTest'],
            2: mongodb_connection['trnltk']['wordBigramsIndexBuilderTest']
        }

        cls.collection_map_for_N_3 = {
            1: mongodb_connection['trnltk']['wordUnigramsIndexBuilderTest'],
            2: mongodb_connection['trnltk']['wordBigramsIndexBuilderTest'],
            3: mongodb_connection['trnltk']['wordTrigramsIndexBuilderTest']
        }

        context_word_appender = ContextWordAppender()
        target_surface_syn_cat_appender = ParseResultSurfaceAppender(True, True)
        target_stem_syn_cat_appender = ParseResultStemAppender(True, True)
        target_lemma_root_syn_cat_appender = ParseResultLemmaRootAppender(True, True)

        context_surface_syn_cat_appender = ParseResultSurfaceAppender(True, False)
        context_stem_syn_cat_appender = ParseResultStemAppender(True, False)
        context_lemma_root_syn_cat_appender = ParseResultLemmaRootAppender(True, False)

        cls.context_parsing_appender_matrix_ROW1 = [
            (target_surface_syn_cat_appender, context_surface_syn_cat_appender),
            (target_surface_syn_cat_appender, context_stem_syn_cat_appender),
            (target_surface_syn_cat_appender, context_lemma_root_syn_cat_appender)
        ]

        cls.context_parsing_appender_matrix_ROW2 = [
            (target_stem_syn_cat_appender, context_surface_syn_cat_appender),
            (target_stem_syn_cat_appender, context_stem_syn_cat_appender),
            (target_stem_syn_cat_appender, context_lemma_root_syn_cat_appender)
        ]

        cls.context_parsing_appender_matrix_ROW3 = [
            (target_lemma_root_syn_cat_appender, context_surface_syn_cat_appender),
            (target_lemma_root_syn_cat_appender, context_stem_syn_cat_appender),
            (target_lemma_root_syn_cat_appender, context_lemma_root_syn_cat_appender)
        ]

        cls.non_context_parsing_appender_matrix = [
            (context_word_appender,),
            (target_surface_syn_cat_appender, context_word_appender),
            (target_stem_syn_cat_appender, context_word_appender),
            (target_lemma_root_syn_cat_appender, context_word_appender)
        ]

        for collection in cls.collection_map_for_N_3.itervalues():
            collection.drop()

    def test_create_context_parsing_appender_index_for_unigram_collection(self):
        index_builder = DatabaseIndexBuilder(self.collection_map_for_N_1)

        index_builder.create_indexes(self.context_parsing_appender_matrix_ROW1)
        index_builder.create_indexes(self.context_parsing_appender_matrix_ROW2)
        index_builder.create_indexes(self.context_parsing_appender_matrix_ROW3)

    def test_create_context_parsing_appender_index_for_bigram_collection(self):
        index_builder = DatabaseIndexBuilder(self.collection_map_for_N_2)

        index_builder.create_indexes(self.context_parsing_appender_matrix_ROW1)
        index_builder.create_indexes(self.context_parsing_appender_matrix_ROW2)
        index_builder.create_indexes(self.context_parsing_appender_matrix_ROW3)

    def test_create_context_parsing_appender_index_for_trigram_collection(self):
        index_builder = DatabaseIndexBuilder(self.collection_map_for_N_3)

        index_builder.create_indexes(self.context_parsing_appender_matrix_ROW1)
        index_builder.create_indexes(self.context_parsing_appender_matrix_ROW2)
        index_builder.create_indexes(self.context_parsing_appender_matrix_ROW3)



    def test_create_noncontext_parsing_appender_index_for_unigram_collection(self):
        index_builder = DatabaseIndexBuilder(self.collection_map_for_N_1)

        index_builder.create_indexes(self.non_context_parsing_appender_matrix)

    def test_create_noncontext_parsing_appender_index_for_bigram_collection(self):
        index_builder = DatabaseIndexBuilder(self.collection_map_for_N_2)

        index_builder.create_indexes(self.non_context_parsing_appender_matrix)

    def test_create_noncontext_parsing_appender_index_for_trigram_collection(self):
        index_builder = DatabaseIndexBuilder(self.collection_map_for_N_3)

        index_builder.create_indexes(self.non_context_parsing_appender_matrix)


if __name__ == '__main__':
    unittest.main()
