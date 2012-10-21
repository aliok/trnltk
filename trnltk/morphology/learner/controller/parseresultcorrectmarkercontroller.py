from trnltk.morphology.model import formatter
from trnltk.morphology.phonetics.alphabet import TurkishAlphabet

class ParseResultCorrectMarkerController(object):
    def __init__(self, dbmanager):
        """
        @type dbmanager: DbManager
        """
        self.dbmanager = dbmanager

    def save_parse_result_for_word(self, corpus_id, word_index, parse_result):
        """
        @type corpus_id: ObjectId
        @type word_index: int
        @type parse_result: MorphemeContainer
        """
        word = self.dbmanager.get_word(corpus_id, word_index)
        if not word:
            raise Exception("Word not found for setting the correct parse result! {} {}".format(corpus_id, word_index))

        # check if the parse result belongs to the word in given index
        assert word['surface'] == parse_result.get_surface() or TurkishAlphabet.lower(word['surface']) == parse_result.get_surface()

        self.dbmanager.set_parse_result_for_word(word, formatter.format_morpheme_container_for_parseset(parse_result), parse_result)

