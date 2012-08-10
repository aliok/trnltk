# coding=utf-8
from bson.code import Code
import os
import unittest
from xml.dom.minidom import parse
from hamcrest.core.assert_that import assert_that
import pymongo
from trnltk.ngrams.ngramgenerators import LexemeNGramGenerator
from trnltk.parseset.xmlbindings import ParseSetBinding, UnparsableWordBinding, WordBinding, SentenceBinding, RootBinding
from hamcrest import *

class LexemeTrigramMongodbGeneratorTest(unittest.TestCase):
    BULK_INSERT_SIZE = 500

    @classmethod
    def setUpClass(cls):
        super(LexemeTrigramMongodbGeneratorTest, cls).setUpClass()
        connection = pymongo.Connection()
        cls.db = connection['trnltk']

    def test_create_ngrams_for_parseset_001(self):
        self._create_trigrams_for_parseset_n("001")

    def test_create_ngrams_for_parseset_002(self):
        self._create_trigrams_for_parseset_n("002")

    def test_create_ngrams_for_parseset_003(self):
        self._create_trigrams_for_parseset_n("003")

    def test_create_ngrams_for_parseset_004(self):
        self._create_trigrams_for_parseset_n("004")

    def test_create_ngrams_for_parseset_005(self):
        self._create_trigrams_for_parseset_n("005")

    def test_create_ngrams_for_parseset_999(self):
        self._create_trigrams_for_parseset_n("999")


    def _create_trigrams_for_parseset_n(self, parseset_index):
        print "Parsing parse set {} and generating trigrams with occurrence counts".format(parseset_index)

        dom = parse(os.path.join(os.path.dirname(__file__), '../../testresources/parsesets/parseset{}.xml'.format(parseset_index)))
        parseset = ParseSetBinding.build(dom.getElementsByTagName("parseset")[0])

        print "Found {} sentences".format(len(parseset.sentences))
        print "Found {} words".format(len([word for sentence in parseset.sentences for word in sentence.words]))
        print "Found {} parsable words".format(
            len(filter(lambda word: not isinstance(word, UnparsableWordBinding), [word for sentence in parseset.sentences for word in sentence.words])))

        generator = LexemeNGramGenerator(3)

        collection = self.db['lexemeTrigrams{}'.format(parseset_index)]

        # delete everything in the collection
        collection.remove({})


        # creating this compound index creates indexes : (a) (a,b) (a,b,c)
        collection.ensure_index([('item_0', pymongo.ASCENDING), ('item_1', pymongo.ASCENDING), ('item_2', pymongo.ASCENDING)])
        # creating this compound index creates indexes : (b) (b,c)
        collection.ensure_index([('item_1', pymongo.ASCENDING), ('item_2', pymongo.ASCENDING)])
        # creating this          index creates indexes : (c)
        collection.ensure_index([('item_2', pymongo.ASCENDING)])

        bulk_insert_buffer = []
        for trigram in generator.iter_ngrams(parseset.sentences):
            entity = {
                'item_0': {'value': trigram[0][0], 'category': trigram[0][1]},
                'item_1': {'value': trigram[1][0], 'category': trigram[1][1]},
                'item_2': {'value': trigram[2][0], 'category': trigram[2][1]}
            }
            bulk_insert_buffer.append(entity)
            if len(bulk_insert_buffer) % self.BULK_INSERT_SIZE == 0:
                collection.insert(bulk_insert_buffer)
                bulk_insert_buffer = []

        collection.insert(bulk_insert_buffer)

        trigram_count = collection.count()
        print "Generated {} trigrams".format(trigram_count)

        print "{} are distinct trigrams".format(self._calculate_distinct_trigrams(collection))
        print "{} distinct trigrams have more than one occurrence".format(self._calculate_distinct_trigrams_with_multiple_occurrences(collection))



    @classmethod
    def _calculate_distinct_trigrams(cls, collection):
        mapper = Code("""
            function(){
                emit({
                    a:this.item_0.value,    b:this.item_1.value,    c:this.item_2.value,
                    d:this.item_0.category, d:this.item_1.category, f:this.item_2.category,
                }, {count: 1});
            }
        """)

        reducer = Code("""
            function(key,values){
                var total = 0;
                for (var i = 0; i < values.length; i++) {
                    total += values[i].count
                }

                return {count:total};
            }
        """)

        result = collection.map_reduce(mapper, reducer, "_temporary")

        return result.count()

    @classmethod
    def _calculate_distinct_trigrams_with_multiple_occurrences(cls, collection):
        mapper = Code("""
            function(){
                emit({
                    a:this.item_0.value,    b:this.item_1.value,    c:this.item_2.value,
                    d:this.item_0.category, d:this.item_1.category, f:this.item_2.category,
                }, {count: 1});
            }
        """)

        reducer = Code("""
            function(key,values){
                var total = 0;
                for (var i = 0; i < values.length; i++) {
                    total += values[i].count
                }

                return {count:total};
            }
        """)

        result = collection.map_reduce(mapper, reducer, "_temporary")

        return result.find({"value.count" : {"$gt" : 1}}).count()


class LexemeNGramGeneratorTest(unittest.TestCase):
    root1 = RootBinding("root1", "lemma1", "lemma_root1", "root_synt_cat1", None)
    root2 = RootBinding("root2", "lemma2", "lemma_root2", "root_synt_cat2", None)
    root4 = RootBinding("root4", "lemma4", "lemma_root4", "root_synt_cat4", None)
    root5 = RootBinding("root5", "lemma5", "lemma_root5", "root_synt_cat5", None)

    word1 = WordBinding("surface_1", "word1_parse_result", root1, "word1_synt_cat", None, None)
    word2 = WordBinding("surface_2", "word2_parse_result", root2, "word2_synt_cat", None, None)
    word3 = UnparsableWordBinding("surface_1")
    word4 = WordBinding("surface_4", "word4_parse_result", root4, "word4_synt_cat", None, None)
    word5 = WordBinding("surface_5", "word5_parse_result", root5, "word5_synt_cat", None, None)

    sentence = SentenceBinding()
    sentence.words = [word1, word2, word3, word4, word5]

    def test_create_bigrams(self):
        generator = LexemeNGramGenerator(2)
        ngrams = generator.get_ngrams([self.sentence])

        assert_that(ngrams, has_length(5))

        start_lexeme = ("<s>", "<s>")
        lexeme1 = ("lemma_root1", "root_synt_cat1")
        lexeme2 = ("lemma_root2", "root_synt_cat2")
        lexeme4 = ("lemma_root4", "root_synt_cat4")
        lexeme5 = ("lemma_root5", "root_synt_cat5")
        end_lexeme = ("</s>", "</s>")

        assert_that(ngrams, has_item((start_lexeme, lexeme1)))
        assert_that(ngrams, has_item((lexeme1, lexeme2)))
        assert_that(ngrams, has_item((lexeme2, lexeme4)))
        assert_that(ngrams, has_item((lexeme4, lexeme5)))
        assert_that(ngrams, has_item((lexeme5, end_lexeme)))

    def test_create_trigrams(self):
        generator = LexemeNGramGenerator(3)
        ngrams = generator.get_ngrams([self.sentence])

        assert_that(ngrams, has_length(6))

        start_lexeme = ("<s>", "<s>")
        lexeme1 = ("lemma_root1", "root_synt_cat1")
        lexeme2 = ("lemma_root2", "root_synt_cat2")
        lexeme4 = ("lemma_root4", "root_synt_cat4")
        lexeme5 = ("lemma_root5", "root_synt_cat5")
        end_lexeme = ("</s>", "</s>")

        assert_that(ngrams, has_item((start_lexeme, start_lexeme, lexeme1)))
        assert_that(ngrams, has_item((start_lexeme, lexeme1, lexeme2)))
        assert_that(ngrams, has_item((lexeme1, lexeme2, lexeme4)))
        assert_that(ngrams, has_item((lexeme2, lexeme4, lexeme5)))
        assert_that(ngrams, has_item((lexeme4, lexeme5, end_lexeme)))
        assert_that(ngrams, has_item((lexeme5, end_lexeme, end_lexeme)))


if __name__ == '__main__':
    unittest.main()

