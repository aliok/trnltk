import pymongo

class _Dao(object):
    def __init__(self):
        db = pymongo.Connection(host='127.0.0.1')['trnltk']

        self._corpora = db['corpora']
        self._words = db['words']

        self._ensure_corpora_indexes(self._corpora)
        self._ensure_word_indexes(self._words)


    def _corpus_exists(self, corpus_name):
        """
        @type corpus_name: str or unicode
        @rtype: bool
        """
        return self._corpora.find({'corpus.name': corpus_name}).count() > 0

    def create_corpus(self, corpus_name, corpus_description):
        """
        @type corpus_name: str
        @type corpus_description: str
        @rtype: dict
        """
        corpus = {
            'name': corpus_name,
            'description': corpus_description
        }

        self._corpora.insert(corpus)

        return corpus

    def create_word(self, token, index, corpus_id):
        word = {
            "corpus_id": corpus_id,
            "index": index,
            "surface": token,
            "parsed": 0
        }

        return self._words.insert(word)

    def _ensure_corpora_indexes(self, corpus_collection):
        ##TODO: unique constraints
        pass

    def _ensure_word_indexes(self, word_collection):
        ##TODO: unique constraints
        pass
