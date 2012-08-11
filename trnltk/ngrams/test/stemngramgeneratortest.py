# coding=utf-8
from bson.code import Code
import os
import unittest
from xml.dom.minidom import parse
from hamcrest.core.assert_that import assert_that
import pymongo
from trnltk.ngrams.ngramgenerators import  StemNGramGenerator
from trnltk.parseset.xmlbindings import ParseSetBinding, UnparsableWordBinding, WordBinding, SentenceBinding, RootBinding, InflectionalSuffixBinding, DerivationalSuffixBinding
from hamcrest import *

class StemTrigramMongodbGeneratorTest(unittest.TestCase):
    BULK_INSERT_SIZE = 500

    @classmethod
    def setUpClass(cls):
        super(StemTrigramMongodbGeneratorTest, cls).setUpClass()
        connection = pymongo.Connection()
        cls.db = connection['trnltk']

    def test_create_trigrams_for_parseset_001(self):
        self._create_trigrams_for_parseset_n("001")

    def test_create_trigrams_for_parseset_002(self):
        self._create_trigrams_for_parseset_n("002")

    def test_create_trigrams_for_parseset_003(self):
        self._create_trigrams_for_parseset_n("003")

    def test_create_trigrams_for_parseset_004(self):
        self._create_trigrams_for_parseset_n("004")

    def test_create_trigrams_for_parseset_005(self):
        self._create_trigrams_for_parseset_n("005")

    def test_create_trigrams_for_parseset_999(self):
        self._create_trigrams_for_parseset_n("999")


    def _create_trigrams_for_parseset_n(self, parseset_index):
        print "Parsing parse set {} and generating trigrams with occurrence counts".format(parseset_index)

        dom = parse(os.path.join(os.path.dirname(__file__), '../../testresources/parsesets/parseset{}.xml'.format(parseset_index)))
        parseset = ParseSetBinding.build(dom.getElementsByTagName("parseset")[0])

        print "Found {} sentences".format(len(parseset.sentences))
        print "Found {} words".format(len([word for sentence in parseset.sentences for word in sentence.words]))
        print "Found {} parsable words".format(
            len(filter(lambda word: not isinstance(word, UnparsableWordBinding), [word for sentence in parseset.sentences for word in sentence.words])))

        generator = StemNGramGenerator(3)

        collection = self.db['stemTrigrams{}'.format(parseset_index)]

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
                'item_0': trigram[0],
                'item_1': trigram[1],
                'item_2': trigram[2]
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
                    a:this.item_0, b:this.item_1, c:this.item_2
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
                    a:this.item_0, b:this.item_1, c:this.item_2
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


class StemNGramGeneratorTest(unittest.TestCase):
    root1 = RootBinding("root1", "lemma1", "lemma_root1", "root_synt_cat1", None)
    root2 = RootBinding("root2", "lemma2", "lemma_root2", "root_synt_cat2", None)
    root4 = RootBinding("root4", "lemma4", "lemma_root4", "root_synt_cat4", None)
    root5 = RootBinding("root5", "lemma5", "lemma_root5", "root_synt_cat5", None)

    suffix_a = InflectionalSuffixBinding("suffix_a", "suffix_a", "form_a", "appl_a", "actual_a", "word_a", "matched_word_a", "suffix_a_syn_cat")
    suffix_b = DerivationalSuffixBinding("suffix_b", "suffix_b", "form_b", "appl_b", "actual_b", "word_b", "matched_word_b", "suffix_b_syn_cat")
    suffix_c = InflectionalSuffixBinding("suffix_c", "suffix_c", "form_c", "appl_c", "actual_c", "word_c", "matched_word_c", "suffix_c_syn_cat")

    suffixes1 = [suffix_a, suffix_b, suffix_c]
    suffixes2 = [suffix_a, suffix_b]
    suffixes4 = [suffix_a]

    word1 = WordBinding("surface_1", "word1_parse_result", root1, "word1_synt_cat", None, suffixes1)
    word2 = WordBinding("surface_2", "word2_parse_result", root2, "word2_synt_cat", None, suffixes2)
    word3 = UnparsableWordBinding("surface_1")
    word4 = WordBinding("surface_4", "word4_parse_result", root4, "word4_synt_cat", None, suffixes4)
    word5 = WordBinding("surface_5", "word5_parse_result", root5, "word5_synt_cat", None, None)

    sentence = SentenceBinding()
    sentence.words = [word1, word2, word3, word4, word5]

    def test_create_bigrams(self):
        generator = StemNGramGenerator(2)
        ngrams = generator.get_ngrams([self.sentence])

        assert_that(ngrams, has_length(5))

        assert_that(ngrams, has_item(("<s>", "word_b")))
        assert_that(ngrams, has_item(("word_b", "word_b")))
        assert_that(ngrams, has_item(("word_b", "surface_4")))
        assert_that(ngrams, has_item(("surface_4", "surface_5")))
        assert_that(ngrams, has_item(("surface_5", "</s>")))

    def test_create_trigrams(self):
        generator = StemNGramGenerator(3)
        ngrams = generator.get_ngrams([self.sentence])

        assert_that(ngrams, has_length(6))

        assert_that(ngrams, has_item(("<s>", "<s>", "word_b")))
        assert_that(ngrams, has_item(("<s>", "word_b", "word_b")))
        assert_that(ngrams, has_item(("word_b", "word_b", "surface_4")))
        assert_that(ngrams, has_item(("word_b", "surface_4", "surface_5")))
        assert_that(ngrams, has_item(("surface_4", "surface_5", "</s>")))
        assert_that(ngrams, has_item(("surface_5", "</s>", "</s>")))


if __name__ == '__main__':
    unittest.main()

