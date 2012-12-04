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

            id_of_first_word = self.dbmanager.find_id_of_first_word_in_corpus(corpus_id)
            number_of_words = self.dbmanager.count_all(corpus_id)
            number_of_nonparsed_words = self.dbmanager.count_all_nonparsed(corpus_id)

            parse_percent = 100.0 - (float(number_of_nonparsed_words) / float(number_of_words) * 100.0)
            self.index_view.add_corpus(corpus, id_of_first_word, number_of_words, parse_percent)
