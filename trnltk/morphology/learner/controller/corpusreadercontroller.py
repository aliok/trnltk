from bson.objectid import ObjectId

class CorpusReaderController():
    def __init__(self, corpus_reader_view, dbmanager):
        """
        @type corpus_reader_view: CorpusReaderView
        @type dbmanager: DbManager
        """
        self.corpus_reader_view = corpus_reader_view
        self.dbmanager = dbmanager

    def read_corpus(self, param_corpus_id):
        assert param_corpus_id

        corpus_id = ObjectId(param_corpus_id)

        corpus = self.dbmanager.get_corpus(corpus_id)

        assert corpus

        corpus_length = self.dbmanager.count_all(corpus_id)
        count_nonparsed = self.dbmanager.count_all_nonparsed(corpus_id)

        self.corpus_reader_view.set_corpus(corpus)
        self.corpus_reader_view.set_corpus_length(corpus_length)
        self.corpus_reader_view.set_count_nonparsed(count_nonparsed)

        words = self.dbmanager.get_words_of_corpus(corpus_id)

        for word in words:
            self.corpus_reader_view.add_word(word)