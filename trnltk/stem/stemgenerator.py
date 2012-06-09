import copy
from trnltk.phonetics.alphabet import TurkishAlphabet
from trnltk.stem.dictionaryitem import RootAttribute, PrimaryPosition
from trnltk.phonetics.phonetics import Phonetics, PhoneticExpectation, PhoneticAttributes

class Stem:
    def __init__(self, root, dictionary_item, phonetic_expectations, phonetic_attributes):
        self.root = root
        self.dictionary_item = dictionary_item
        self.phonetic_expectations = phonetic_expectations if phonetic_attributes else []
        self.phonetic_attributes = phonetic_attributes if phonetic_attributes else []

    def __eq__(self, other):
        return self.root==other.root and self.dictionary_item==other.dictionary_item \
            and self.phonetic_expectations==other.phonetic_expectations \
            and self.phonetic_attributes==other.phonetic_attributes

    def __hash__(self):
        return hash((self.root,
                     tuple(sorted(self.phonetic_expectations or [])),
                     tuple(sorted(self.phonetic_attributes or []))
            ))

    def __str__(self):
        return u'{}({}) PH_ATTR:{} PH_EXPC:{}'.format(repr(self.root), self.dictionary_item, self.phonetic_attributes, self.phonetic_expectations)

    def __repr__(self):
        return self.__str__()

    def _clone(self):
        return Stem(
            self.root,
            self.dictionary_item,
            copy.copy(self.phonetic_expectations) if self.phonetic_expectations else None,
            copy.copy(self.phonetic_attributes) if self.phonetic_attributes else None)

class StemGenerator:
    _modifiers = {
        RootAttribute.Doubling,
        RootAttribute.LastVowelDrop,
        RootAttribute.ProgressiveVowelDrop,
        RootAttribute.InverseHarmony,
        RootAttribute.Voicing,
        RootAttribute.VoicingOpt,
        RootAttribute.StemChange,
        RootAttribute.CompoundP3sg
    }

    @classmethod
    def generate(cls, dictionary_item):
        if any(x in dictionary_item.attributes for x in StemGenerator._modifiers):
            return StemGenerator._generate_modified_root_nodes(dictionary_item)
        else:
            phonetic_attributes = Phonetics.calculate_phonetic_attributes(dictionary_item.root)
            stem = Stem(dictionary_item.root, dictionary_item, None, phonetic_attributes)
            return [stem]

    @classmethod
    def _generate_modified_root_nodes(cls, dictionary_item):
        if RootAttribute.StemChange in dictionary_item.attributes:
            special_stems = cls._handle_special_stems(dictionary_item)
            if special_stems:
                return special_stems

        if RootAttribute.CompoundP3sg in dictionary_item.attributes: ##TODO:
            return cls._handle_p3sg_compounds(dictionary_item)

        modified_seq = dictionary_item.root

        original_attributes = Phonetics.calculate_phonetic_attributes(dictionary_item.root)
        modified_attributes = Phonetics.calculate_phonetic_attributes(dictionary_item.root)
        original_phonetic_expectations = set()
        modified_phonetic_expectations = set()

        if RootAttribute.Voicing in dictionary_item.attributes or RootAttribute.VoicingOpt in dictionary_item.attributes:
            last_letter = TurkishAlphabet.get_letter_for_char(modified_seq[-1])
            modified_letter = TurkishAlphabet.voice(last_letter)
            assert modified_letter is not None
            if dictionary_item.lemma.endswith("nk"):
                modified_letter = TurkishAlphabet.L_g
            modified_seq = modified_seq[:-1] + modified_letter.char_value
            if PhoneticAttributes.LastLetterVoicelessStop in modified_attributes:
                modified_attributes.remove(PhoneticAttributes.LastLetterVoicelessStop)
            if RootAttribute.VoicingOpt not in dictionary_item.attributes:
                original_phonetic_expectations.add(PhoneticExpectation.ConsonantStart)
            modified_phonetic_expectations.add(PhoneticExpectation.VowelStart)

        if RootAttribute.Doubling in dictionary_item.attributes:
            modified_seq = modified_seq + modified_seq[-1]
            original_phonetic_expectations.add(PhoneticExpectation.ConsonantStart)
            modified_phonetic_expectations.add(PhoneticExpectation.VowelStart)

        if RootAttribute.LastVowelDrop in dictionary_item.attributes:
            modified_seq = modified_seq[:-2] + modified_seq[-1]
            if dictionary_item.primary_position!=PrimaryPosition.VERB:
                original_phonetic_expectations.add(PhoneticExpectation.ConsonantStart)
            modified_phonetic_expectations.add(PhoneticExpectation.VowelStart)

        if RootAttribute.InverseHarmony in dictionary_item.attributes:
            original_attributes.add(PhoneticAttributes.LastVowelFrontal)
            if PhoneticAttributes.LastVowelBack in original_attributes:
                original_attributes.remove(PhoneticAttributes.LastVowelBack)
            modified_attributes.add(PhoneticAttributes.LastVowelFrontal)
            if PhoneticAttributes.LastVowelBack in modified_attributes:
                modified_attributes.remove(PhoneticAttributes.LastVowelBack)

        if RootAttribute.ProgressiveVowelDrop in dictionary_item.attributes:
            modified_seq = modified_seq[:-1]
            if StemGenerator._has_vowel(modified_seq):
                modified_attributes = Phonetics.calculate_phonetic_attributes(modified_seq)
            modified_phonetic_expectations.add(PhoneticExpectation.VowelStart)


        original_phonetic_expectations = original_phonetic_expectations or None
        modified_phonetic_expectations = modified_phonetic_expectations or None

        original = Stem(dictionary_item.root, dictionary_item, original_phonetic_expectations, original_attributes)
        modified = Stem(modified_seq, dictionary_item, modified_phonetic_expectations, modified_attributes)

        if original==modified:
            return [original]
        else:
            return [original, modified]

    @classmethod
    def _handle_special_stems(cls, dictionary_item):
        ##TODO: de-ye
        if dictionary_item.lemma==u'ben':
            dictionary_item.attributes.remove(RootAttribute.StemChange)
            stem_ben = Stem(u'ben', dictionary_item, [], Phonetics.calculate_phonetic_attributes(u'ben'))
            stem_ban = Stem(u'ban', dictionary_item, [], Phonetics.calculate_phonetic_attributes(u'ban'))
            return [stem_ben, stem_ban]
        elif dictionary_item.lemma==u'sen':
            dictionary_item.attributes.remove(RootAttribute.StemChange)
            stem_sen = Stem(u'sen', dictionary_item, [], Phonetics.calculate_phonetic_attributes(u'ben'))
            stem_san = Stem(u'san', dictionary_item, [], Phonetics.calculate_phonetic_attributes(u'ban'))
            return [stem_sen, stem_san]
        elif dictionary_item.lemma==u'demek':
            return None
        elif dictionary_item.lemma==u'yemek':
            return None
        else:
            raise Exception('Unhandled stem change : {} !'.format(dictionary_item))

    @classmethod
    def _handle_p3sg_compounds(cls, dictionary_item):
        return []

    @classmethod
    def _has_vowel(cls, seq):
        for s in seq:
            if TurkishAlphabet.get_letter_for_char(s).vowel:
                return True

        return False


class CircumflexConvertingStemGenerator:
    Circumflex_Letters_Map = {
        TurkishAlphabet.L_ac.char_value : TurkishAlphabet.L_a.char_value,
        TurkishAlphabet.L_ic.char_value : TurkishAlphabet.L_i.char_value,
        TurkishAlphabet.L_uc.char_value : TurkishAlphabet.L_u.char_value,
        TurkishAlphabet.L_ac.upper_case_char_value : TurkishAlphabet.L_a.upper_case_char_value,
        TurkishAlphabet.L_ic.upper_case_char_value : TurkishAlphabet.L_i.upper_case_char_value,
        TurkishAlphabet.L_uc.upper_case_char_value : TurkishAlphabet.L_u.upper_case_char_value
    }

    Circumflex_Chars = Circumflex_Letters_Map.keys()

    @classmethod
    def generate(cls, dictionary_item):
        stems = []
        stems_with_circumflexes = StemGenerator.generate(dictionary_item)
        stems.extend(stems_with_circumflexes)

        if any(c in dictionary_item.root for c in cls.Circumflex_Chars):
            for stem in stems_with_circumflexes:
                stem_without_circumflex = stem._clone()
                root = stem.root
                for (circumflex_char, converted_char) in cls.Circumflex_Letters_Map.iteritems():
                    root = root.replace(circumflex_char, converted_char)

                stem_without_circumflex.root = root

                stems.append(stem_without_circumflex)


        return stems