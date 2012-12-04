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



