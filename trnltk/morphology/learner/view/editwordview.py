class EditWordView(object):
    def __init__(self):
        self._context = {}

    def get_template_context(self):
        return self._context

    def set_current_word(self, word):
        self._context['current_word_id'] = word['_id']
        self._context['current_surface'] = word['surface']

    def set_next_word_id(self, next_word_id):
        self._context['next_word_id'] = next_word_id
