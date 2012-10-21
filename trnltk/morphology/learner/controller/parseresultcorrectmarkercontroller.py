from trnltk.morphology.model import formatter
from trnltk.morphology.phonetics.alphabet import TurkishAlphabet

class ParseResultCorrectMarkerController(object):
    def __init__(self, dbmanager):
        """
        @type dbmanager: DbManager
        """
        self.dbmanager = dbmanager

    def save_parse_result_for_word(self, word_id, parse_result):
        """
        @type word_id: ObjectId
        @type parse_result: MorphemeContainer
        """
        word = self.dbmanager.get_word(word_id)
        if not word:
            raise Exception("Word not found for setting the correct parse result! {}".format(word_id))

        # check if the parse result belongs to the given word
        assert word['surface'] == parse_result.get_surface() or TurkishAlphabet.lower(word['surface']) == parse_result.get_surface()

        self.dbmanager.set_parse_result_for_word(word, formatter.format_morpheme_container_for_parseset(parse_result), parse_result)

