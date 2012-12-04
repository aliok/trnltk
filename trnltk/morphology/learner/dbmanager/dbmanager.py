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
import pymongo

class DbManager(object):
    def __init__(self, connection):
        db = connection['trnltk']

        self.corpus_collection = db['corpora']
        self.word_collection = db['words']

    def build_indexes(self):
        self.corpus_collection.ensure_index([('name', pymongo.ASCENDING)], unique=True)

        self.word_collection.ensure_index([('corpus_id', pymongo.ASCENDING), ('index', pymongo.ASCENDING)], unique=True)
        self.word_collection.ensure_index([('corpus_id', pymongo.ASCENDING), ('parsed', pymongo.ASCENDING), ('index', pymongo.ASCENDING)])

    def find_next_nonparsed_word(self, corpus_id, word_start_index):
        assert corpus_id and word_start_index is not None

        query = {
            'corpus_id': corpus_id,
            'parsed': 0,
            'index': {"$gt": word_start_index}
        }

        cursor = self.word_collection.find(query).sort('index', pymongo.ASCENDING).limit(1)

        count = cursor.count(with_limit_and_skip=True)
        assert count <= 1

        if count:
            return cursor[0]
        else:
            return None

    def find_previous_nonparsed_word(self, corpus_id, word_end_index):
        assert corpus_id and word_end_index is not None

        query = {
            'corpus_id': corpus_id,
            'parsed': 0,
            'index': {"$lt": word_end_index}
        }

        cursor = self.word_collection.find(query).sort('index', pymongo.DESCENDING).limit(1)

        count = cursor.count(with_limit_and_skip=True)
        assert count <= 1

        if count:
            return cursor[0]
        else:
            return None

    def get_words_in_range(self, corpus_id, start_index, end_index):
        assert corpus_id and start_index is not None and end_index is not None

        query = {
            'corpus_id': corpus_id,
            'index': {"$gte": start_index, "$lte": end_index}
        }

        return [word for word in self.word_collection.find(query).sort('index', pymongo.ASCENDING)]

    def get_word_by_index(self, corpus_id, word_index):
        assert corpus_id and word_index is not None

        query = {
            'corpus_id': corpus_id,
            'index': word_index
        }

        return self.word_collection.find_one(query)

    def count_all_nonparsed(self, corpus_id):
        assert corpus_id

        query = {
            'corpus_id': corpus_id,
            'parsed': 0
        }

        return self.word_collection.find(query).count()

    def count_nonparsed_prior_to_index(self, corpus_id, index):
        assert corpus_id and index is not None

        query = {
            'corpus_id': corpus_id,
            'parsed': 0,
            'index': {"$lt": index}
        }

        return self.word_collection.find(query).count()

    def count_all(self, corpus_id):
        assert corpus_id

        query = {
            'corpus_id': corpus_id
        }

        return self.word_collection.find(query).count()

    def get_word(self, word_id):
        """
        @type word_id: ObjectId
        """
        assert word_id

        return self.word_collection.find_one(word_id)

    def get_all_corpora(self):
        """
        @rtype: Cursor
        """
        return self.corpus_collection.find()

    def is_corpus_with_name_exist(self, corpus_name):
        return self.corpus_collection.find({'name': corpus_name}).count() > 0

    def create_corpus(self, corpus_name, corpus_desc):
        """
        @type corpus_name: str
        @type corpus_desc: str
        @rtype: ObjectId
        """
        corpus = {
            'name': corpus_name,
            'description': corpus_desc
        }

        self.corpus_collection.insert(corpus)

        return corpus['_id']

    def create_word(self, token, corpus_id, index):
        """
        @type token: str or unicode
        @type corpus_id: ObjectId
        @type index: int
        @type: dict
        """
        word = {
            "corpus_id": corpus_id,
            "index": index,
            "surface": token,
            "parsed": 0
        }

        return self.word_collection.insert(word)

    def set_parse_result_for_word(self, word, str_parse_result, parse_result):
        """
        @type word: mongo db document
        @type str_parse_result: str or unicode
        @type parse_result: MorphemeContainer
        """
        word['parsed'] = 1
        word['parse_result'] = str_parse_result

        #word['surface'] = parse_result.get_surface()       DON'T CHANGE THE SURFACE!
        word['surface_syntactic_category'] = parse_result.get_surface_syntactic_category()
        word['surface_secondary_syntactic_category'] = parse_result.get_surface_secondary_syntactic_category()

        word['stem'] = parse_result.get_stem()
        word['stem_syntactic_category'] = parse_result.get_stem_syntactic_category()
        word['stem_secondary_syntactic_category'] = parse_result.get_stem_secondary_syntactic_category()

        word['lemma_root'] = parse_result.get_lemma_root()
        word['lemma_root_syntactic_category'] = parse_result.get_lemma_root_syntactic_category()
        word['lemma_root_secondary_syntactic_category'] = parse_result.get_lemma_root_secondary_syntactic_category()

        self.word_collection.save(word)

    def find_id_of_first_word_in_corpus(self, corpus_id):
        val = self.word_collection.find_one({'corpus_id': corpus_id, 'index': 0}, {'_id': True})
        if val and val['_id']:
            return val['_id']
        else:
            raise Exception('Corpus {} doesnt have a word with index 0.'.format(corpus_id))

    def insert_word_at_index(self, corpus_id, surface, index):
        # super bad implementation, but nvm...

        self.increase_word_indexes(corpus_id, index)
        self.create_word(surface, corpus_id, index)

    def delete_word(self, word):
        # super bad implementation, same with method 'insert_word_at_index'
        corpus_id = word['corpus_id']
        word_index = word['index']

        last_index = self.count_all(corpus_id) - 1

        self.word_collection.remove(word)
        self.decrease_word_indexes(corpus_id, word_index + 1, last_index + 1)

    def increase_word_indexes(self, corpus_id, index):
        # super bad implementation, but nvm...
        last_index = self.count_all(corpus_id) - 1
        for i in range(last_index, index - 1, -1):
            word_by_index = self.get_word_by_index(corpus_id, i)
            if not word_by_index:
                # this stupid implementation of splitting and word indexes require indexes to be contiguous
                raise Exception('No word found for index {}!'.format(i))
            word_by_index['index'] = i + 1
            self.word_collection.save(word_by_index)

    def decrease_word_indexes(self, corpus_id, from_index, to_index):
        # super bad implementation, but nvm...
        for i in range(from_index, to_index, 1):
            word_by_index = self.get_word_by_index(corpus_id, i)
            if not word_by_index:
                # this stupid implementation of splitting and word indexes require indexes to be contiguous
                raise Exception('No word found for index {}!'.format(i))
            word_by_index['index'] = i - 1
            self.word_collection.save(word_by_index)


    def update_word(self, word, surface_first_part):
        word['surface'] = surface_first_part       #update the surface
        word['parsed'] = 0

        if word.get('parse_result') is not None:
            del word['parse_result']

        if word.get('surface_syntactic_category') is not None:
            del word['surface_syntactic_category']
        if word.get('surface_secondary_syntactic_category') is not None:
            del word['surface_secondary_syntactic_category']

        if word.get('stem') is not None:
            del word['stem']
        if word.get('stem_syntactic_category') is not None:
            del word['stem_syntactic_category']
        if word.get('stem_secondary_syntactic_category') is not None:
            del word['stem_secondary_syntactic_category']

        if word.get('lemma_root') is not None:
            del word['lemma_root']
        if word.get('lemma_root_syntactic_category') is not None:
            del word['lemma_root_syntactic_category']
        if word.get('lemma_root_secondary_syntactic_category') is not None:
            del word['lemma_root_secondary_syntactic_category']

        self.word_collection.save(word)

    def find_next_word(self, corpus_id, word):
        val = self.get_word_by_index(corpus_id, word['index'] + 1)
        if val:
            return val
        else:
            return self.get_word(self.find_id_of_first_word_in_corpus(corpus_id))

    def delete_corpus(self, corpus_id):
        self.corpus_collection.remove(corpus_id)

    def get_corpus(self, corpus_id):
        return self.corpus_collection.find_one(corpus_id)

    def get_words_of_corpus(self, corpus_id):
        query = {
            'corpus_id': corpus_id
        }
        return self.word_collection.find(query)
