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
