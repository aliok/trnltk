import re
from trnltk.stem.stemgenerator import NumeralStem, AbbreviationStem, ProperNounStem

class WordStemFinder(object):
    def __init__(self, stem_root_map):
        self.stem_root_map = stem_root_map

    def find_stem_for_partial_input(self, partial_input):
        if self.stem_root_map.has_key(partial_input):
            return self.stem_root_map[partial_input][:]
        else:
            return []

class NumeralStemFinder(object):
    NUMBER_REGEXES = [re.compile(u'^[-+]?\d+(,\d)?\d*$'), re.compile(u'^[-+]?(\d{1,3}\.)+\d{3}(,\d)?\d*$')]

    def find_stem_for_partial_input(self, partial_input):
        for regex in self.NUMBER_REGEXES:
            if regex.match(partial_input):
                return [NumeralStem(partial_input)]

        return []

class ProperNounFromApostropheStemFinder(object):
    APOSTROPHE = u"'"

    def find_stem_for_partial_input(self, partial_input):
        if partial_input.endswith(self.APOSTROPHE):
            proper_noun_candidate = partial_input[:-1]
            if proper_noun_candidate.isupper():
                return [AbbreviationStem(partial_input[:-1])]
            elif proper_noun_candidate[0].isupper():
                return [ProperNounStem(partial_input[:-1])]

        return []

class ProperNounWithoutApostropheStemFinder(object):
    APOSTROPHE = u"'"

    def find_stem_for_partial_input(self, partial_input):
        if not partial_input[0].isalpha() or not partial_input[0].isupper() or self.APOSTROPHE in partial_input:
            return []

        # TODO: might be a known proper noun like "Turkce" or "Istanbul". no support for them yet

        # TODO: might be a known proper noun with implicit P3sg. like : Eminonu, Kusadasi.
        # it is important since :
        # 1. Ankara'_y_a but Eminonu'_n_e
        # 2: P3sg doesn't apply to these words: onun Kusadasi, onun Eminonu
        # 3. Possessions are applied to 'root' : benim Kusadam etc. SKIP this case!

        return [ProperNounStem(partial_input)]



