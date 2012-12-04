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
class EditWordController(object):
    def __init__(self, edit_word_view, dbmanager):
        """
        @type edit_word_view: EditWordView
        @type dbmanager : DbManager
        """
        self.edit_word_view = edit_word_view
        self.dbmanager = dbmanager

    def go_to_word(self, word_id, next_word_id):
        """
        @type word_id: ObjectId
        """
        assert word_id and next_word_id

        # find and set new word in view
        word = self.dbmanager.get_word(word_id)
        assert word
        self.edit_word_view.set_current_word(word)
        self.edit_word_view.set_next_word_id(next_word_id)

    def update_word(self, word_id, surface_first_part, surface_second_part):
        """
        @type word_id: ObjectId
        """
        assert word_id

        # find new word
        word = self.dbmanager.get_word(word_id)
        assert word

        if surface_first_part:
            surface_first_part = surface_first_part.strip()

        if surface_second_part:
            surface_second_part = surface_second_part.strip()

        if surface_first_part and surface_second_part:
            word_index = word['index']
            self.dbmanager.update_word(word, surface_first_part)
            self.dbmanager.insert_word_at_index(word['corpus_id'], surface_second_part, word_index + 1)
        elif surface_first_part:
            self.dbmanager.update_word(word, surface_first_part)
        elif surface_second_part:
            self.dbmanager.update_word(word, surface_second_part)
        else:
            raise Exception('You have to provide at least one part')

    def delete_word(self, word_id):
        word = self.dbmanager.get_word(word_id)
        assert word
        corpus_id = word['corpus_id']

        self.dbmanager.delete_word(word)
        corpus_length = self.dbmanager.count_all(corpus_id)
        if not corpus_length:
            self.dbmanager.delete_corpus(corpus_id)
            return False
        else:
            return True

