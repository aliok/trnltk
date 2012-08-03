from trnltk.morphology.phonetics.alphabet import TurkishAlphabet
from trnltk.morphology.lexiconmodel.lexeme import RootAttribute, SyntacticCategory
from trnltk.morphology.phonetics.phonetics import Phonetics, PhoneticExpectation, PhoneticAttributes
from trnltk.morphology.lexiconmodel.root import Root

class RootGenerator(object):
    _modifiers = {
        RootAttribute.Doubling,
        RootAttribute.LastVowelDrop,
        RootAttribute.ProgressiveVowelDrop,
        RootAttribute.InverseHarmony,
        RootAttribute.Voicing,
        RootAttribute.VoicingOpt,
        RootAttribute.StemChange
    }

    @classmethod
    def generate(cls, lexeme):
        if any(x in lexeme.attributes for x in RootGenerator._modifiers):
            return RootGenerator._generate_modified_root_nodes(lexeme)
        else:
            phonetic_attributes = Phonetics.calculate_phonetic_attributes_of_plain_sequence(lexeme.root)
            root = Root(lexeme.root, lexeme, None, phonetic_attributes)
            return [root]

    @classmethod
    def _generate_modified_root_nodes(cls, lexeme):
        if RootAttribute.StemChange in lexeme.attributes:
            special_roots = cls._handle_special_roots(lexeme)
            if special_roots:
                return special_roots

        modified_seq = lexeme.root

        original_attributes = Phonetics.calculate_phonetic_attributes_of_plain_sequence(lexeme.root)
        modified_attributes = Phonetics.calculate_phonetic_attributes_of_plain_sequence(lexeme.root)
        original_phonetic_expectations = set()
        modified_phonetic_expectations = set()

        if RootAttribute.Voicing in lexeme.attributes or RootAttribute.VoicingOpt in lexeme.attributes:
            last_letter = TurkishAlphabet.get_letter_for_char(modified_seq[-1])
            modified_letter = TurkishAlphabet.voice(last_letter)
            assert modified_letter is not None
            if lexeme.lemma.endswith("nk"):
                modified_letter = TurkishAlphabet.L_g
            modified_seq = modified_seq[:-1] + modified_letter.char_value
            if PhoneticAttributes.LastLetterVoicelessStop in modified_attributes:
                modified_attributes.remove(PhoneticAttributes.LastLetterVoicelessStop)
            if RootAttribute.VoicingOpt not in lexeme.attributes:
                original_phonetic_expectations.add(PhoneticExpectation.ConsonantStart)
            modified_phonetic_expectations.add(PhoneticExpectation.VowelStart)

        if RootAttribute.Doubling in lexeme.attributes:
            modified_seq = modified_seq + modified_seq[-1]
            original_phonetic_expectations.add(PhoneticExpectation.ConsonantStart)
            modified_phonetic_expectations.add(PhoneticExpectation.VowelStart)

        if RootAttribute.LastVowelDrop in lexeme.attributes:
            modified_seq = modified_seq[:-2] + modified_seq[-1]
            if lexeme.syntactic_category!=SyntacticCategory.VERB:
                original_phonetic_expectations.add(PhoneticExpectation.ConsonantStart)
            modified_phonetic_expectations.add(PhoneticExpectation.VowelStart)

        if RootAttribute.InverseHarmony in lexeme.attributes:
            original_attributes.add(PhoneticAttributes.LastVowelFrontal)
            if PhoneticAttributes.LastVowelBack in original_attributes:
                original_attributes.remove(PhoneticAttributes.LastVowelBack)
            modified_attributes.add(PhoneticAttributes.LastVowelFrontal)
            if PhoneticAttributes.LastVowelBack in modified_attributes:
                modified_attributes.remove(PhoneticAttributes.LastVowelBack)

        if RootAttribute.ProgressiveVowelDrop in lexeme.attributes:
            modified_seq = modified_seq[:-1]
            if RootGenerator._has_vowel(modified_seq):
                modified_attributes = Phonetics.calculate_phonetic_attributes_of_plain_sequence(modified_seq)
            modified_phonetic_expectations.add(PhoneticExpectation.VowelStart)


        original_phonetic_expectations = original_phonetic_expectations or None
        modified_phonetic_expectations = modified_phonetic_expectations or None

        original = Root(lexeme.root, lexeme, original_phonetic_expectations, original_attributes)
        modified = Root(modified_seq, lexeme, modified_phonetic_expectations, modified_attributes)

        if original==modified:
            return [original]
        else:
            return [original, modified]

    @classmethod
    def _handle_special_roots(cls, lexeme):
        lexeme.attributes.remove(RootAttribute.StemChange)

        ##TODO: de-ye
        if lexeme.lemma==u'ben':
            root_ben = Root(u'ben', lexeme, [], Phonetics.calculate_phonetic_attributes_of_plain_sequence(u'ben'))
            root_ban = Root(u'ban', lexeme, [], Phonetics.calculate_phonetic_attributes_of_plain_sequence(u'ban'))
            return [root_ben, root_ban]
        elif lexeme.lemma==u'sen':
            root_sen = Root(u'sen', lexeme, [], Phonetics.calculate_phonetic_attributes_of_plain_sequence(u'ben'))
            root_san = Root(u'san', lexeme, [], Phonetics.calculate_phonetic_attributes_of_plain_sequence(u'ban'))
            return [root_sen, root_san]
        elif lexeme.lemma==u'demek':
            return None
        elif lexeme.lemma==u'yemek':
            return None
        elif lexeme.lemma==u'hepsi':
            root_hep = Root(u'hep', lexeme, [], Phonetics.calculate_phonetic_attributes_of_plain_sequence(u'hep'))
            root_hepsi = Root(u'hepsi', lexeme, [], Phonetics.calculate_phonetic_attributes_of_plain_sequence(u'hepsi'))
            return [root_hep, root_hepsi]
        elif lexeme.lemma==u'ora':
            root_or = Root(u'or', lexeme, [], Phonetics.calculate_phonetic_attributes_of_plain_sequence(u'or'))
            root_ora = Root(u'ora', lexeme, [], Phonetics.calculate_phonetic_attributes_of_plain_sequence(u'ora'))
            return [root_or, root_ora]
        else:
            raise Exception('Unhandled stem change : {} !'.format(lexeme))

    @classmethod
    def _has_vowel(cls, seq):
        for s in seq:
            if TurkishAlphabet.get_letter_for_char(s).vowel:
                return True

        return False


class CircumflexConvertingRootGenerator(object):
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
    def generate(cls, lexeme):
        roots = []
        roots_with_circumflexes = RootGenerator.generate(lexeme)
        roots.extend(roots_with_circumflexes)

        if any(c in lexeme.root for c in cls.Circumflex_Chars):
            for root in roots_with_circumflexes:
                root_without_circumflex = root._clone()
                root = root.str
                for (circumflex_char, converted_char) in cls.Circumflex_Letters_Map.iteritems():
                    root = root.replace(circumflex_char, converted_char)

                root_without_circumflex.root = root

                roots.append(root_without_circumflex)


        return roots

class RootMapGenerator(object):
    def generate(self, all_roots):
        root_map = {}
        for root in all_roots:
            key = root.root
            if not root_map.has_key(key):
                root_map[key] = []

            root_map[key].append(root)

        return root_map