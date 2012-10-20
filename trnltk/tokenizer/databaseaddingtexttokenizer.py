# coding=utf-8
from trnltk.tokenizer.hidden.dao import _Dao
from trnltk.tokenizer.texttokenizer import TextTokenizer



class DatabaseAddingTextTokenizer(object):
    def __init__(self):
        self._tokenizer = TextTokenizer()
        self._dao = _Dao()

    def add_to_database(self, text, corpus_name, corpus_description):
        assert text

        tokens = self._tokenizer.tokenize(text)

        if self._dao._corpus_exists(corpus_name):
            raise Exception('Corpus {} exists already.'.format(corpus_name))

        corpus = self._dao.create_corpus(corpus_name, corpus_description)

        print corpus

        corpus_id = corpus['_id']

        for index, token in enumerate(tokens):  # no batch insert for now
            self._dao.create_word(token, index, corpus_id)

        return corpus
