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