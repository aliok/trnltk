class CorpusCreatorController(object):
    def __init__(self, corpus_creator_view, dbmanager, tokenizer):
        """
        @type corpus_creator_view: CorpusCreatorView
        @type dbmanager: DbManager
        @type tokenizer: TextTokenizer
        """
        self.corpus_creator_view = corpus_creator_view
        self.dbmanager = dbmanager
        self.tokenizer = tokenizer

    def create_corpus(self, corpus_name, corpus_desc, corpus_content):
        try:
            self.corpus_creator_view.set_corpus_name(corpus_name)

            if self.dbmanager.is_corpus_with_name_exist(corpus_name):
                self.corpus_creator_view.set_corpus_name_not_unique()
                return

            corpus_id = self.dbmanager.create_corpus(corpus_name, corpus_desc)

            tokens = self.tokenizer.tokenize(corpus_content)

            for index, token in enumerate(tokens):  # no batch insert for now
                self.dbmanager.create_word(token, corpus_id, index)

            self.corpus_creator_view.set_success()
        except Exception as e:
            self.corpus_creator_view.set_error(str(e))