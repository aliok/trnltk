class IndexView(object):
    def __init__(self):
        self._context = {}

    def get_template_context(self):
        return self._context

    def add_corpus(self, corpus, id_of_first_word, number_of_words, parse_percent):
        corpora = self._context.get('corpora') or []

        corpus_container = {
            'id' : corpus['_id'],
            'name' : corpus['name'],
            'description' : corpus['description'],
            'id_of_first_word' : id_of_first_word,
            'word_count' : number_of_words,
            'parse_percent' : parse_percent
        }

        corpora.append(corpus_container)

        self._context['corpora'] = corpora