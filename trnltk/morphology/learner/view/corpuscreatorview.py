class CorpusCreatorView(object):
    def __init__(self):
        self._context = {}

    def get_template_context(self):
        return self._context

    def set_corpus_name(self, corpus_name):
        self._context['corpus_name'] = corpus_name

    def set_corpus_name_not_unique(self):
        self.set_error("Please select a unique corpus name. Provided name already exists.")

    def set_success(self):
        self._context['error_occurred'] = False

    def set_error(self, param):
        self._context['error_occurred'] = True
        self._context['error_msg'] = param