"""
Copyright  2012  Ali Ok (aliokATapacheDOTorg)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
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