import pymongo

class DbManager(object):     # TODO: what about indexes?
    def __init__(self, connection):
        db = connection['trnltk']

        self.corpus_collection = db['corpora']
        self.word_collection = db['words']

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


    def get_word(self, corpus_id, word_index):
        assert corpus_id and word_index is not None

        query = {
            'corpus_id': corpus_id,
            'parsed': 0,
            'index': word_index
        }

        return self.word_collection.find_one(query)

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
