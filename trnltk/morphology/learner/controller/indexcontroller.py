class IndexController(object):
    def __init__(self, index_view, dbmanager):
        """
        @type index_view: IndexView
        @type dbmanager: DbManager
        """
        self.index_view = index_view
        self.dbmanager = dbmanager

    def go_home(self):
        corpora_cursor = self.dbmanager.get_all_corpora()
        for corpus in corpora_cursor:
            corpus_id = corpus['_id']
            number_of_words = self.dbmanager.count_all(corpus_id)
            number_of_nonparsed_words = self.dbmanager.count_all_nonparsed(corpus_id)
            parse_percent = 100.0 - (float(number_of_nonparsed_words) / float(number_of_words) * 100.0)
            self.index_view.add_corpus(corpus, number_of_words, parse_percent)
