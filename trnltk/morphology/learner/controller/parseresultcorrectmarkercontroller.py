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
from trnltk.morphology.model import formatter
from trnltk.morphology.phonetics.alphabet import TurkishAlphabet

class ParseResultCorrectMarkerController(object):
    def __init__(self, dbmanager, sessionmanager):
        """
        @type dbmanager: DbManager
        @type sessionmanager: SessionManager
        """
        self.dbmanager = dbmanager
        self.sessionmanager = sessionmanager

    def save_parse_result_for_word(self, word_id, parse_result_uuid):
        """
        @type word_id: ObjectId
        @type parse_result_uuid: str or unicode
        """
        parse_result = self.sessionmanager.get_parse_result(parse_result_uuid)
        assert parse_result, "No parse result found with id {}".format(parse_result)

        word = self.dbmanager.get_word(word_id)
        if not word:
            raise Exception("Word not found for setting the correct parse result! {}".format(word_id))

        # check if the parse result belongs to the given word
        assert word['surface'] == parse_result.get_surface() or TurkishAlphabet.lower(word['surface']) == parse_result.get_surface()

        self.dbmanager.set_parse_result_for_word(word, formatter.format_morpheme_container_for_parseset(parse_result), parse_result)

