import re
from trnltk.morphology.lexiconmodel.root import NumeralRoot, AbbreviationRoot, ProperNounRoot

class LexemeFinder(object):
    def find_lexeme_for_partial_input(self, partial_input):
        raise NotImplementedError()

class WordLexemeFinder(LexemeFinder):
    def __init__(self, lexeme_map):
        self.lexeme_map = lexeme_map

    def find_lexeme_for_partial_input(self, partial_input):
        if self.lexeme_map.has_key(partial_input):
            return self.lexeme_map[partial_input][:]
        else:
            return []

class NumeralLexemeFinder(LexemeFinder):
    NUMBER_REGEXES = [re.compile(u'^[-+]?\d+(,\d)?\d*$'), re.compile(u'^[-+]?(\d{1,3}\.)+\d{3}(,\d)?\d*$')]

    def find_lexeme_for_partial_input(self, partial_input):
        for regex in self.NUMBER_REGEXES:
            if regex.match(partial_input):
                return [NumeralRoot(partial_input)]

        return []

class ProperNounFromApostropheLexemeFinder(LexemeFinder):
    APOSTROPHE = u"'"

    def find_lexeme_for_partial_input(self, partial_input):
        if partial_input.endswith(self.APOSTROPHE):
            proper_noun_candidate = partial_input[:-1]
            if proper_noun_candidate.isupper():
                return [AbbreviationRoot(partial_input[:-1])]
            elif proper_noun_candidate[0].isupper():
                return [ProperNounRoot(partial_input[:-1])]

        return []

class ProperNounWithoutApostropheLexemeFinder(LexemeFinder):
    APOSTROPHE = u"'"

    def find_lexeme_for_partial_input(self, partial_input):
        if not partial_input[0].isalpha() or not partial_input[0].isupper() or self.APOSTROPHE in partial_input:
            return []

        # TODO: might be a known proper noun like "Turkce" or "Istanbul". no support for them yet

        # TODO: might be a known proper noun with implicit P3sg. like : Eminonu, Kusadasi.
        # it is important since :
        # 1. Ankara'_y_a but Eminonu'_n_e
        # 2: P3sg doesn't apply to these words: onun Kusadasi, onun Eminonu
        # 3. Possessions are applied to 'root' : benim Kusadam etc. SKIP this case!

        return [ProperNounRoot(partial_input)]



