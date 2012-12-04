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
from bson.code import Code
import os
import unittest
from xml.dom.minidom import parse
import pymongo
from trnltk.ngrams.ngramgenerator import  WordNGramGenerator, WordUnigramWithParseResultGenerator
from trnltk.parseset.xmlbindings import ParseSetBinding, UnparsableWordBinding

def _count_distinct_ngrams(collection, keys, filter_criteria):
    mapper = Code("""
            function(){
                emit({
                    """ + keys + """
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

    if filter_criteria:
        result = result.find(filter_criteria)

    return result.count()

class WordUnigramMongodbGeneratorTest(unittest.TestCase):
    BULK_INSERT_SIZE = 500

    @classmethod
    def setUpClass(cls):
        super(WordUnigramMongodbGeneratorTest, cls).setUpClass()
        connection = pymongo.Connection(host="127.0.0.1")
        cls.db = connection['trnltk']

    def test_create_unigrams_for_parseset_001(self):
        self._create_unigrams_for_parseset_n("001")

    def test_create_unigrams_for_parseset_002(self):
        self._create_unigrams_for_parseset_n("002")

    def test_create_unigrams_for_parseset_003(self):
        self._create_unigrams_for_parseset_n("003")

    def test_create_unigrams_for_parseset_004(self):
        self._create_unigrams_for_parseset_n("004")

    def test_create_unigrams_for_parseset_005(self):
        self._create_unigrams_for_parseset_n("005")

    def test_create_unigrams_for_parseset_999(self):
        self._create_unigrams_for_parseset_n("999")


    def test_inspect_unigrams_for_parseset_001(self):
        self._inspect_unigrams_for_parseset_n("001")

    def test_inspect_unigrams_for_parseset_002(self):
        self._inspect_unigrams_for_parseset_n("002")

    def test_inspect_unigrams_for_parseset_003(self):
        self._inspect_unigrams_for_parseset_n("003")

    def test_inspect_unigrams_for_parseset_004(self):
        self._inspect_unigrams_for_parseset_n("004")

    def test_inspect_unigrams_for_parseset_005(self):
        self._inspect_unigrams_for_parseset_n("005")

    def test_inspect_unigrams_for_parseset_999(self):
        self._inspect_unigrams_for_parseset_n("999")

    def _create_unigrams_for_parseset_n(self, parseset_index):
        print "Parsing parse set {} and generating unigrams with occurrence counts".format(parseset_index)

        dom = parse(os.path.join(os.path.dirname(__file__), '../../testresources/parsesets/parseset{}.xml'.format(parseset_index)))
        parseset = ParseSetBinding.build(dom.getElementsByTagName("parseset")[0])

        print "Found {} sentences".format(len(parseset.sentences))
        words = [word for sentence in parseset.sentences for word in sentence.words]
        print "Found {} words".format(len(words))
        print "Found {} parsable words".format(
            len(filter(lambda word: not isinstance(word, UnparsableWordBinding), words)))

        generator = WordNGramGenerator(1)

        collection = self.db['wordUnigrams{}'.format(parseset_index)]

        # delete everything in the collection
        collection.remove({})

        bulk_insert_buffer = []
        for unigram in generator.iter_ngrams(words):
            entity = {
                'item_0': unigram
            }
            bulk_insert_buffer.append(entity)
            if len(bulk_insert_buffer) % self.BULK_INSERT_SIZE == 0:
                collection.insert(bulk_insert_buffer)
                bulk_insert_buffer = []

        collection.insert(bulk_insert_buffer)

        self._inspect_unigrams_for_parseset_n(parseset_index)


    def _inspect_unigrams_for_parseset_n(self, parseset_index):
        collection = self.db['wordUnigrams{}'.format(parseset_index)]

        unigram_count = collection.count()
        print "Found {} unigrams".format(unigram_count)

        distinct_surface_unigram_count = self._count_distinct_surface_unigrams(collection)
        print "Found {} distinct surface unigrams".format(distinct_surface_unigram_count)

        distinct_surface_unigram_with_multiple_occurrences_count = self._count_distinct_surface_unigrams_with_multiple_occurrences(collection)
        print "Found {} distinct surface unigrams with multiple occurrences".format(distinct_surface_unigram_with_multiple_occurrences_count)

        distinct_stem_unigram_count = self._count_distinct_stem_unigrams(collection)
        print "Found {} distinct stem unigrams".format(distinct_stem_unigram_count)

        distinct_stem_unigram_with_multiple_occurrences_count = self._count_distinct_stem_unigrams_with_multiple_occurrences(collection)
        print "Found {} distinct stem unigrams with multiple occurrences".format(distinct_stem_unigram_with_multiple_occurrences_count)

        distinct_lexeme_unigram_count = self._count_distinct_lexeme_unigrams(collection)
        print "Found {} distinct lexeme unigrams".format(distinct_lexeme_unigram_count)

        distinct_lexeme_unigram_with_multiple_occurrences_count = self._count_distinct_lexeme_unigrams_with_multiple_occurrences(collection)
        print "Found {} distinct lexeme unigrams with multiple occurrences".format(distinct_lexeme_unigram_with_multiple_occurrences_count)

    @classmethod
    def _count_distinct_surface_unigrams(cls, collection):
        keys = "a:this.item_0.word.surface.value,                 b:this.item_0.word.surface.syntactic_category"
        filter_criteria = None
        return _count_distinct_ngrams(collection, keys, filter_criteria)

    @classmethod
    def _count_distinct_surface_unigrams_with_multiple_occurrences(cls, collection):
        keys = "a:this.item_0.word.surface.value,                 b:this.item_0.word.surface.syntactic_category"
        filter_criteria = {"value.count": {"$gt": 1}}
        return _count_distinct_ngrams(collection, keys, filter_criteria)

    @classmethod
    def _count_distinct_stem_unigrams(cls, collection):
        keys = "a:this.item_0.word.stem.value,                 b:this.item_0.word.stem.syntactic_category"
        filter_criteria = None
        return _count_distinct_ngrams(collection, keys, filter_criteria)

    @classmethod
    def _count_distinct_stem_unigrams_with_multiple_occurrences(cls, collection):
        keys = "a:this.item_0.word.stem.value,                 b:this.item_0.word.stem.syntactic_category"
        filter_criteria = {"value.count": {"$gt": 1}}
        return _count_distinct_ngrams(collection, keys, filter_criteria)

    @classmethod
    def _count_distinct_lexeme_unigrams(cls, collection):
        keys = "a:this.item_0.word.lemma_root.value,                 b:this.item_0.word.lemma_root.syntactic_category"
        filter_criteria = None
        return _count_distinct_ngrams(collection, keys, filter_criteria)

    @classmethod
    def _count_distinct_lexeme_unigrams_with_multiple_occurrences(cls, collection):
        keys = "a:this.item_0.word.lemma_root.value,                 b:this.item_0.word.lemma_root.syntactic_category"
        filter_criteria = {"value.count": {"$gt": 1}}
        return _count_distinct_ngrams(collection, keys, filter_criteria)

class WordBigramMongodbGeneratorTest(unittest.TestCase):
    BULK_INSERT_SIZE = 500

    @classmethod
    def setUpClass(cls):
        super(WordBigramMongodbGeneratorTest, cls).setUpClass()
        connection = pymongo.Connection(host="127.0.0.1")
        cls.db = connection['trnltk']

    def test_create_bigrams_for_parseset_001(self):
        self._create_bigrams_for_parseset_n("001")

    def test_create_bigrams_for_parseset_002(self):
        self._create_bigrams_for_parseset_n("002")

    def test_create_bigrams_for_parseset_003(self):
        self._create_bigrams_for_parseset_n("003")

    def test_create_bigrams_for_parseset_004(self):
        self._create_bigrams_for_parseset_n("004")

    def test_create_bigrams_for_parseset_005(self):
        self._create_bigrams_for_parseset_n("005")

    def test_create_bigrams_for_parseset_999(self):
        self._create_bigrams_for_parseset_n("999")


    def test_inspect_bigrams_for_parseset_001(self):
        self._inspect_bigrams_for_parseset_n("001")

    def test_inspect_bigrams_for_parseset_002(self):
        self._inspect_bigrams_for_parseset_n("002")

    def test_inspect_bigrams_for_parseset_003(self):
        self._inspect_bigrams_for_parseset_n("003")

    def test_inspect_bigrams_for_parseset_004(self):
        self._inspect_bigrams_for_parseset_n("004")

    def test_inspect_bigrams_for_parseset_005(self):
        self._inspect_bigrams_for_parseset_n("005")

    def test_inspect_bigrams_for_parseset_999(self):
        self._inspect_bigrams_for_parseset_n("999")


    def _create_bigrams_for_parseset_n(self, parseset_index):
        print "Parsing parse set {} and generating bigrams with occurrence counts".format(parseset_index)

        dom = parse(os.path.join(os.path.dirname(__file__), '../../testresources/parsesets/parseset{}.xml'.format(parseset_index)))
        parseset = ParseSetBinding.build(dom.getElementsByTagName("parseset")[0])

        print "Found {} sentences".format(len(parseset.sentences))
        words = [word for sentence in parseset.sentences for word in sentence.words]
        print "Found {} words".format(len(words))
        print "Found {} parsable words".format(
            len(filter(lambda word: not isinstance(word, UnparsableWordBinding), words)))

        generator = WordNGramGenerator(2)

        collection = self.db['wordBigrams{}'.format(parseset_index)]

        # delete everything in the collection
        collection.remove({})

        bulk_insert_buffer = []
        for bigram in generator.iter_ngrams(words):
            entity = {
                'item_0': bigram[0],
                'item_1': bigram[1]
            }
            bulk_insert_buffer.append(entity)
            if len(bulk_insert_buffer) % self.BULK_INSERT_SIZE == 0:
                collection.insert(bulk_insert_buffer)
                bulk_insert_buffer = []

        collection.insert(bulk_insert_buffer)

        self._inspect_bigrams_for_parseset_n(parseset_index)

    def _inspect_bigrams_for_parseset_n(self, parseset_index):
        collection = self.db['wordBigrams{}'.format(parseset_index)]

        bigram_count = collection.count()
        print "Found {} bigrams".format(bigram_count)

        print "Found {} distinct surface-surface bigrams".format(self._calculate_distinct_surface_surface_bigrams(collection))
        print "Found {} distinct surface-surface bigrams with multiple occurrences".format(self._calculate_distinct_surface_surface_bigrams_with_multiple_occurrences(collection))
        print "Found {} distinct surface-stem bigrams".format(self._calculate_distinct_surface_stem_bigrams(collection))
        print "Found {} distinct surface-stem bigrams with multiple occurrences".format(self._calculate_distinct_surface_stem_bigrams_with_multiple_occurrences(collection))
        print "Found {} distinct surface-lexeme bigrams".format(self._calculate_distinct_surface_lexeme_bigrams(collection))
        print "Found {} distinct surface-lexeme bigrams with multiple occurrences".format(self._calculate_distinct_surface_lexeme_bigrams_with_multiple_occurrences(collection))

        print "Found {} distinct stem-surface bigrams".format(self._calculate_distinct_stem_surface_bigrams(collection))
        print "Found {} distinct stem-surface bigrams with multiple occurrences".format(self._calculate_distinct_stem_surface_bigrams_with_multiple_occurrences(collection))
        print "Found {} distinct stem-stem bigrams".format(self._calculate_distinct_stem_stem_bigrams(collection))
        print "Found {} distinct stem-stem bigrams with multiple occurrences".format(self._calculate_distinct_stem_stem_bigrams_with_multiple_occurrences(collection))
        print "Found {} distinct stem-lexeme bigrams".format(self._calculate_distinct_stem_lexeme_bigrams(collection))
        print "Found {} distinct stem-lexeme bigrams with multiple occurrences".format(self._calculate_distinct_stem_lexeme_bigrams_with_multiple_occurrences(collection))

        print "Found {} distinct lexeme-surface bigrams".format(self._calculate_distinct_lexeme_surface_bigrams(collection))
        print "Found {} distinct lexeme-surface bigrams with multiple occurrences".format(self._calculate_distinct_lexeme_surface_bigrams_with_multiple_occurrences(collection))
        print "Found {} distinct lexeme-stem bigrams".format(self._calculate_distinct_lexeme_stem_bigrams(collection))
        print "Found {} distinct lexeme-stem bigrams with multiple occurrences".format(self._calculate_distinct_lexeme_stem_bigrams_with_multiple_occurrences(collection))
        print "Found {} distinct lexeme-lexeme bigrams".format(self._calculate_distinct_lexeme_lexeme_bigrams(collection))
        print "Found {} distinct lexeme-lexeme bigrams with multiple occurrences".format(self._calculate_distinct_lexeme_lexeme_bigrams_with_multiple_occurrences(collection))

    ####################################################################

    @classmethod
    def _calculate_distinct_surface_surface_bigrams(cls, collection):
        keys = """
        a:this.item_0.word.surface.value,                 b:this.item_1.word.surface.value,
        c:this.item_0.word.surface.syntactic_category,    d:this.item_1.word.surface.syntactic_category
        """
        filter_criteria = None
        return _count_distinct_ngrams(collection, keys, filter_criteria)

    @classmethod
    def _calculate_distinct_surface_surface_bigrams_with_multiple_occurrences(cls, collection):
        keys = """
        a:this.item_0.word.surface.value,                 b:this.item_1.word.surface.value,
        c:this.item_0.word.surface.syntactic_category,    d:this.item_1.word.surface.syntactic_category
        """
        filter_criteria = {"value.count": {"$gt": 1}}
        return _count_distinct_ngrams(collection, keys, filter_criteria)

    @classmethod
    def _calculate_distinct_surface_stem_bigrams(cls, collection):
        keys = """
        a:this.item_0.word.surface.value,                 b:this.item_1.word.stem.value,
        c:this.item_0.word.surface.syntactic_category,    d:this.item_1.word.stem.syntactic_category
        """
        filter_criteria = None
        return _count_distinct_ngrams(collection, keys, filter_criteria)

    @classmethod
    def _calculate_distinct_surface_stem_bigrams_with_multiple_occurrences(cls, collection):
        keys = """
        a:this.item_0.word.surface.value,                 b:this.item_1.word.stem.value,
        c:this.item_0.word.surface.syntactic_category,    d:this.item_1.word.stem.syntactic_category
        """
        filter_criteria = {"value.count": {"$gt": 1}}
        return _count_distinct_ngrams(collection, keys, filter_criteria)

    @classmethod
    def _calculate_distinct_surface_lexeme_bigrams(cls, collection):
        keys = """
        a:this.item_0.word.surface.value,                 b:this.item_1.word.lemma_root.value,
        c:this.item_0.word.surface.syntactic_category,    d:this.item_1.word.lemma_root.syntactic_category
        """
        filter_criteria = None
        return _count_distinct_ngrams(collection, keys, filter_criteria)

    @classmethod
    def _calculate_distinct_surface_lexeme_bigrams_with_multiple_occurrences(cls, collection):
        keys = """
        a:this.item_0.word.surface.value,                 b:this.item_1.word.lemma_root.value,
        c:this.item_0.word.surface.syntactic_category,    d:this.item_1.word.lemma_root.syntactic_category
        """
        filter_criteria = {"value.count": {"$gt": 1}}
        return _count_distinct_ngrams(collection, keys, filter_criteria)

    ####################################################################

    @classmethod
    def _calculate_distinct_stem_surface_bigrams(cls, collection):
        keys = """
        a:this.item_0.word.stem.value,                 b:this.item_1.word.surface.value,
        c:this.item_0.word.stem.syntactic_category,    d:this.item_1.word.surface.syntactic_category
        """
        filter_criteria = None
        return _count_distinct_ngrams(collection, keys, filter_criteria)

    @classmethod
    def _calculate_distinct_stem_surface_bigrams_with_multiple_occurrences(cls, collection):
        keys = """
        a:this.item_0.word.stem.value,                 b:this.item_1.word.surface.value,
        c:this.item_0.word.stem.syntactic_category,    d:this.item_1.word.surface.syntactic_category
        """
        filter_criteria = {"value.count": {"$gt": 1}}
        return _count_distinct_ngrams(collection, keys, filter_criteria)

    @classmethod
    def _calculate_distinct_stem_stem_bigrams(cls, collection):
        keys = """
        a:this.item_0.word.stem.value,                 b:this.item_1.word.stem.value,
        c:this.item_0.word.stem.syntactic_category,    d:this.item_1.word.stem.syntactic_category
        """
        filter_criteria = None
        return _count_distinct_ngrams(collection, keys, filter_criteria)

    @classmethod
    def _calculate_distinct_stem_stem_bigrams_with_multiple_occurrences(cls, collection):
        keys = """
        a:this.item_0.word.stem.value,                 b:this.item_1.word.stem.value,
        c:this.item_0.word.stem.syntactic_category,    d:this.item_1.word.stem.syntactic_category
        """
        filter_criteria = {"value.count": {"$gt": 1}}
        return _count_distinct_ngrams(collection, keys, filter_criteria)

    @classmethod
    def _calculate_distinct_stem_lexeme_bigrams(cls, collection):
        keys = """
        a:this.item_0.word.stem.value,                 b:this.item_1.word.lemma_root.value,
        c:this.item_0.word.stem.syntactic_category,    d:this.item_1.word.lemma_root.syntactic_category
        """
        filter_criteria = None
        return _count_distinct_ngrams(collection, keys, filter_criteria)

    @classmethod
    def _calculate_distinct_stem_lexeme_bigrams_with_multiple_occurrences(cls, collection):
        keys = """
        a:this.item_0.word.stem.value,                 b:this.item_1.word.lemma_root.value,
        c:this.item_0.word.stem.syntactic_category,    d:this.item_1.word.lemma_root.syntactic_category
        """
        filter_criteria = {"value.count": {"$gt": 1}}
        return _count_distinct_ngrams(collection, keys, filter_criteria)

    ####################################################################

    @classmethod
    def _calculate_distinct_lexeme_surface_bigrams(cls, collection):
        keys = """
        a:this.item_0.word.lemma_root.value,                 b:this.item_1.word.surface.value,
        c:this.item_0.word.lemma_root.syntactic_category,    d:this.item_1.word.surface.syntactic_category
        """
        filter_criteria = None
        return _count_distinct_ngrams(collection, keys, filter_criteria)

    @classmethod
    def _calculate_distinct_lexeme_surface_bigrams_with_multiple_occurrences(cls, collection):
        keys = """
        a:this.item_0.word.lemma_root.value,                 b:this.item_1.word.surface.value,
        c:this.item_0.word.lemma_root.syntactic_category,    d:this.item_1.word.surface.syntactic_category
        """
        filter_criteria = {"value.count": {"$gt": 1}}
        return _count_distinct_ngrams(collection, keys, filter_criteria)

    @classmethod
    def _calculate_distinct_lexeme_stem_bigrams(cls, collection):
        keys = """
        a:this.item_0.word.lemma_root.value,                 b:this.item_1.word.stem.value,
        c:this.item_0.word.lemma_root.syntactic_category,    d:this.item_1.word.stem.syntactic_category
        """
        filter_criteria = None
        return _count_distinct_ngrams(collection, keys, filter_criteria)

    @classmethod
    def _calculate_distinct_lexeme_stem_bigrams_with_multiple_occurrences(cls, collection):
        keys = """
        a:this.item_0.word.lemma_root.value,                 b:this.item_1.word.stem.value,
        c:this.item_0.word.lemma_root.syntactic_category,    d:this.item_1.word.stem.syntactic_category
        """
        filter_criteria = {"value.count": {"$gt": 1}}
        return _count_distinct_ngrams(collection, keys, filter_criteria)

    @classmethod
    def _calculate_distinct_lexeme_lexeme_bigrams(cls, collection):
        keys = """
        a:this.item_0.word.lemma_root.value,                 b:this.item_1.word.lemma_root.value,
        c:this.item_0.word.lemma_root.syntactic_category,    d:this.item_1.word.lemma_root.syntactic_category
        """
        filter_criteria = None
        return _count_distinct_ngrams(collection, keys, filter_criteria)

    @classmethod
    def _calculate_distinct_lexeme_lexeme_bigrams_with_multiple_occurrences(cls, collection):
        keys = """
        a:this.item_0.word.lemma_root.value,                 b:this.item_1.word.lemma_root.value,
        c:this.item_0.word.lemma_root.syntactic_category,    d:this.item_1.word.lemma_root.syntactic_category
        """
        filter_criteria = {"value.count": {"$gt": 1}}
        return _count_distinct_ngrams(collection, keys, filter_criteria)



class WordTrigramMongodbGeneratorTest(unittest.TestCase):
    BULK_INSERT_SIZE = 500

    @classmethod
    def setUpClass(cls):
        super(WordTrigramMongodbGeneratorTest, cls).setUpClass()
        connection = pymongo.Connection(host="127.0.0.1")
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
        words = [word for sentence in parseset.sentences for word in sentence.words]
        print "Found {} words".format(len(words))
        print "Found {} parsable words".format(
            len(filter(lambda word: not isinstance(word, UnparsableWordBinding), words)))

        generator = WordNGramGenerator(3)

        collection = self.db['wordTrigrams{}'.format(parseset_index)]

        # delete everything in the collection
        collection.remove({})

        bulk_insert_buffer = []
        for trigram in generator.iter_ngrams(words):
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

class WordUnigramWithParseResultGeneratorMongodbTest(unittest.TestCase):
    BULK_INSERT_SIZE = 500

    @classmethod
    def setUpClass(cls):
        super(WordUnigramWithParseResultGeneratorMongodbTest, cls).setUpClass()
        connection = pymongo.Connection(host="127.0.0.1")
        cls.db = connection['trnltk']

    def test_create_unigrams_for_parseset_001(self):
        self._create_unigrams_for_parseset_n("001")

    def test_create_unigrams_for_parseset_002(self):
        self._create_unigrams_for_parseset_n("002")

    def test_create_unigrams_for_parseset_003(self):
        self._create_unigrams_for_parseset_n("003")

    def test_create_unigrams_for_parseset_004(self):
        self._create_unigrams_for_parseset_n("004")

    def test_create_unigrams_for_parseset_005(self):
        self._create_unigrams_for_parseset_n("005")

    def test_create_unigrams_for_parseset_999(self):
        self._create_unigrams_for_parseset_n("999")


    def test_inspect_unigrams_for_parseset_001(self):
        self._inspect_unigrams_for_parseset_n("001")

    def test_inspect_unigrams_for_parseset_002(self):
        self._inspect_unigrams_for_parseset_n("002")

    def test_inspect_unigrams_for_parseset_003(self):
        self._inspect_unigrams_for_parseset_n("003")

    def test_inspect_unigrams_for_parseset_004(self):
        self._inspect_unigrams_for_parseset_n("004")

    def test_inspect_unigrams_for_parseset_005(self):
        self._inspect_unigrams_for_parseset_n("005")

    def test_inspect_unigrams_for_parseset_999(self):
        self._inspect_unigrams_for_parseset_n("999")

    def _create_unigrams_for_parseset_n(self, parseset_index):
        print "Parsing parse set {} and generating unigrams with occurrence counts and parse results".format(parseset_index)

        dom = parse(os.path.join(os.path.dirname(__file__), '../../testresources/parsesets/parseset{}.xml'.format(parseset_index)))
        parseset = ParseSetBinding.build(dom.getElementsByTagName("parseset")[0])

        print "Found {} sentences".format(len(parseset.sentences))
        words = [word for sentence in parseset.sentences for word in sentence.words]
        print "Found {} words".format(len(words))
        print "Found {} parsable words".format(
            len(filter(lambda word: not isinstance(word, UnparsableWordBinding), words)))

        generator = WordUnigramWithParseResultGenerator()

        collection = self.db['wordUnigrams{}'.format(parseset_index)]

        # delete everything in the collection
        collection.remove({})

        bulk_insert_buffer = []
        for unigram in generator.iter_ngrams(words):
            entity = {
                'item_0': unigram
            }
            bulk_insert_buffer.append(entity)
            if len(bulk_insert_buffer) % self.BULK_INSERT_SIZE == 0:
                collection.insert(bulk_insert_buffer)
                bulk_insert_buffer = []

        collection.insert(bulk_insert_buffer)

        self._inspect_unigrams_for_parseset_n(parseset_index)

    def _inspect_unigrams_for_parseset_n(self, parseset_index):
        collection = self.db['wordUnigrams{}'.format(parseset_index)]

        unigram_count = collection.count()
        print "Found {} unigrams".format(unigram_count)

        distinct_surface_unigram_count = self._count_distinct_surface_unigrams(collection)
        print "Found {} distinct surface unigrams".format(distinct_surface_unigram_count)

        distinct_surface_unigram_with_multiple_occurrences_count = self._count_distinct_surface_unigrams_with_multiple_occurrences(collection)
        print "Found {} distinct surface unigrams with multiple occurrences".format(distinct_surface_unigram_with_multiple_occurrences_count)

        distinct_stem_unigram_count = self._count_distinct_stem_unigrams(collection)
        print "Found {} distinct stem unigrams".format(distinct_stem_unigram_count)

        distinct_stem_unigram_with_multiple_occurrences_count = self._count_distinct_stem_unigrams_with_multiple_occurrences(collection)
        print "Found {} distinct stem unigrams with multiple occurrences".format(distinct_stem_unigram_with_multiple_occurrences_count)

        distinct_lexeme_unigram_count = self._count_distinct_lexeme_unigrams(collection)
        print "Found {} distinct lexeme unigrams".format(distinct_lexeme_unigram_count)

        distinct_lexeme_unigram_with_multiple_occurrences_count = self._count_distinct_lexeme_unigrams_with_multiple_occurrences(collection)
        print "Found {} distinct lexeme unigrams with multiple occurrences".format(distinct_lexeme_unigram_with_multiple_occurrences_count)

    @classmethod
    def _count_distinct_surface_unigrams(cls, collection):
        keys = "a:this.item_0.word.surface.value,                 b:this.item_0.word.surface.syntactic_category"
        filter_criteria = None
        return _count_distinct_ngrams(collection, keys, filter_criteria)

    @classmethod
    def _count_distinct_surface_unigrams_with_multiple_occurrences(cls, collection):
        keys = "a:this.item_0.word.surface.value,                 b:this.item_0.word.surface.syntactic_category"
        filter_criteria = {"value.count": {"$gt": 1}}
        return _count_distinct_ngrams(collection, keys, filter_criteria)

    @classmethod
    def _count_distinct_stem_unigrams(cls, collection):
        keys = "a:this.item_0.word.stem.value,                 b:this.item_0.word.stem.syntactic_category"
        filter_criteria = None
        return _count_distinct_ngrams(collection, keys, filter_criteria)

    @classmethod
    def _count_distinct_stem_unigrams_with_multiple_occurrences(cls, collection):
        keys = "a:this.item_0.word.stem.value,                 b:this.item_0.word.stem.syntactic_category"
        filter_criteria = {"value.count": {"$gt": 1}}
        return _count_distinct_ngrams(collection, keys, filter_criteria)

    @classmethod
    def _count_distinct_lexeme_unigrams(cls, collection):
        keys = "a:this.item_0.word.lemma_root.value,                 b:this.item_0.word.lemma_root.syntactic_category"
        filter_criteria = None
        return _count_distinct_ngrams(collection, keys, filter_criteria)

    @classmethod
    def _count_distinct_lexeme_unigrams_with_multiple_occurrences(cls, collection):
        keys = "a:this.item_0.word.lemma_root.value,                 b:this.item_0.word.lemma_root.syntactic_category"
        filter_criteria = {"value.count": {"$gt": 1}}
        return _count_distinct_ngrams(collection, keys, filter_criteria)

if __name__ == '__main__':
    unittest.main()

