class CorpusReaderView(object):
    def __init__(self):
        self._context = {}

    def get_template_context(self):
        return self._context

    def set_corpus(self, corpus):
        self._context['corpus_name'] = corpus['name']
        self._context['corpus_description'] = corpus['description']

    def set_corpus_length(self, corpus_length):
        self._context['corpus_length'] = corpus_length

    def set_count_nonparsed(self, count_nonparsed):
        self._context['count_nonparsed'] = count_nonparsed

    def add_word(self, word):
        if not 'words' in self._context:
            self._context['words'] = []

        self._context['words'].append(word)



