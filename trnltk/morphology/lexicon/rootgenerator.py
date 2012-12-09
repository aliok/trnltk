# coding=utf-8
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
from trnltk.morphology.phonetics.alphabet import TurkishAlphabet
from trnltk.morphology.model.lexeme import LexemeAttribute, SyntacticCategory
from trnltk.morphology.phonetics.phonetics import Phonetics, PhoneticExpectation, PhoneticAttributes
from trnltk.morphology.model.root import Root

class RootGenerator(object):
    _modifiers = {
        LexemeAttribute.Doubling,
        LexemeAttribute.LastVowelDrop,
        LexemeAttribute.ProgressiveVowelDrop,
        LexemeAttribute.InverseHarmony,
        LexemeAttribute.Voicing,
        LexemeAttribute.VoicingOpt,
        LexemeAttribute.RootChange
    }

    @classmethod
    def generate(cls, lexeme):
        if any(x in lexeme.attributes for x in RootGenerator._modifiers):
            try:
                return RootGenerator._generate_modified_root_nodes(lexeme)
            except:
                print u'Error generating roots for lexeme : {}'.format(lexeme)
                raise
        else:
            phonetic_attributes = Phonetics.calculate_phonetic_attributes_of_plain_sequence(lexeme.root)
            root = Root(lexeme.root, lexeme, None, phonetic_attributes)
            return [root]

    @classmethod
    def _generate_modified_root_nodes(cls, lexeme):
        if LexemeAttribute.RootChange in lexeme.attributes:
            special_roots = cls._handle_special_roots(lexeme)
            if special_roots:
                return special_roots

        modified_seq = lexeme.root

        original_attributes = Phonetics.calculate_phonetic_attributes_of_plain_sequence(lexeme.root)
        modified_attributes = Phonetics.calculate_phonetic_attributes_of_plain_sequence(lexeme.root)
        original_phonetic_expectations = set()
        modified_phonetic_expectations = set()

        if LexemeAttribute.Voicing in lexeme.attributes or LexemeAttribute.VoicingOpt in lexeme.attributes:
            last_letter = TurkishAlphabet.get_letter_for_char(modified_seq[-1])
            modified_letter = TurkishAlphabet.voice(last_letter)
            assert modified_letter is not None
            if lexeme.lemma.endswith(u"nk"):
                modified_letter = TurkishAlphabet.L_g
            modified_seq = modified_seq[:-1] + modified_letter.char_value
            if PhoneticAttributes.LastLetterVoicelessStop in modified_attributes:
                modified_attributes.remove(PhoneticAttributes.LastLetterVoicelessStop)
            if modified_letter.continuant:
                if PhoneticAttributes.LastLetterNotContinuant in modified_attributes :
                    modified_attributes.remove(PhoneticAttributes.LastLetterNotContinuant)
                modified_attributes.add(PhoneticAttributes.LastLetterContinuant)
            else:
                if PhoneticAttributes.LastLetterContinuant in modified_attributes:
                    modified_attributes.remove(PhoneticAttributes.LastLetterContinuant)
                modified_attributes.add(PhoneticAttributes.LastLetterNotContinuant)
            if LexemeAttribute.VoicingOpt not in lexeme.attributes:
                original_phonetic_expectations.add(PhoneticExpectation.ConsonantStart)
            modified_phonetic_expectations.add(PhoneticExpectation.VowelStart)

        if LexemeAttribute.Doubling in lexeme.attributes:
            modified_seq = modified_seq + modified_seq[-1]
            original_phonetic_expectations.add(PhoneticExpectation.ConsonantStart)
            modified_phonetic_expectations.add(PhoneticExpectation.VowelStart)

        if LexemeAttribute.LastVowelDrop in lexeme.attributes:
            modified_seq = modified_seq[:-2] + modified_seq[-1]
            if lexeme.syntactic_category!=SyntacticCategory.VERB:
                original_phonetic_expectations.add(PhoneticExpectation.ConsonantStart)
            modified_phonetic_expectations.add(PhoneticExpectation.VowelStart)

        if LexemeAttribute.InverseHarmony in lexeme.attributes:
            original_attributes.add(PhoneticAttributes.LastVowelFrontal)
            if PhoneticAttributes.LastVowelBack in original_attributes:
                original_attributes.remove(PhoneticAttributes.LastVowelBack)
            modified_attributes.add(PhoneticAttributes.LastVowelFrontal)
            if PhoneticAttributes.LastVowelBack in modified_attributes:
                modified_attributes.remove(PhoneticAttributes.LastVowelBack)

        if LexemeAttribute.ProgressiveVowelDrop in lexeme.attributes:
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
        lexeme.attributes.remove(LexemeAttribute.RootChange)

        if lexeme.lemma==u'ben':
            root_ben = Root(u'ben', lexeme, None, Phonetics.calculate_phonetic_attributes_of_plain_sequence(u'ben'))
            root_ban = Root(u'ban', lexeme, None, Phonetics.calculate_phonetic_attributes_of_plain_sequence(u'ban'))
            return [root_ben, root_ban]
        elif lexeme.lemma==u'sen':
            root_sen = Root(u'sen', lexeme, None, Phonetics.calculate_phonetic_attributes_of_plain_sequence(u'ben'))
            root_san = Root(u'san', lexeme, None, Phonetics.calculate_phonetic_attributes_of_plain_sequence(u'ban'))
            return [root_sen, root_san]
        elif lexeme.lemma==u'demek':
            root_di = Root(u'di', lexeme, None, Phonetics.calculate_phonetic_attributes_of_plain_sequence(u'di'))
            root_de = Root(u'de', lexeme, None, Phonetics.calculate_phonetic_attributes_of_plain_sequence(u'de'))
            return [root_di, root_de]
        elif lexeme.lemma==u'yemek':
            root_yi = Root(u'yi', lexeme, None, Phonetics.calculate_phonetic_attributes_of_plain_sequence(u'yi'))
            root_ye = Root(u'ye', lexeme, None, Phonetics.calculate_phonetic_attributes_of_plain_sequence(u'ye'))
            return [root_yi, root_ye]
        elif lexeme.lemma==u'hepsi':
            root_hep = Root(u'hep', lexeme, None, Phonetics.calculate_phonetic_attributes_of_plain_sequence(u'hep'))
            root_hepsi = Root(u'hepsi', lexeme, None, Phonetics.calculate_phonetic_attributes_of_plain_sequence(u'hepsi'))
            return [root_hep, root_hepsi]
        elif lexeme.lemma==u'ora':
            root_or = Root(u'or', lexeme, None, Phonetics.calculate_phonetic_attributes_of_plain_sequence(u'or'))
            root_ora = Root(u'ora', lexeme, None, Phonetics.calculate_phonetic_attributes_of_plain_sequence(u'ora'))
            return [root_or, root_ora]
        elif lexeme.lemma==u'bura':
            root_bur = Root(u'bur', lexeme, None, Phonetics.calculate_phonetic_attributes_of_plain_sequence(u'bur'))
            root_bura = Root(u'bura', lexeme, None, Phonetics.calculate_phonetic_attributes_of_plain_sequence(u'bura'))
            return [root_bur, root_bura]
        elif lexeme.lemma==u'şura':
            root_sur = Root(u'şur', lexeme, None, Phonetics.calculate_phonetic_attributes_of_plain_sequence(u'şur'))
            root_sura = Root(u'şura', lexeme, None, Phonetics.calculate_phonetic_attributes_of_plain_sequence(u'şura'))
            return [root_sur, root_sura]
        elif lexeme.lemma==u'nere':
            root_ner = Root(u'ner', lexeme, None, Phonetics.calculate_phonetic_attributes_of_plain_sequence(u'ner'))
            root_nere = Root(u'nere', lexeme, None, Phonetics.calculate_phonetic_attributes_of_plain_sequence(u'nere'))
            return [root_ner, root_nere]
        elif lexeme.lemma==u'nere':
            root_ner = Root(u'ner', lexeme, None, Phonetics.calculate_phonetic_attributes_of_plain_sequence(u'ner'))
            root_nere = Root(u'nere', lexeme, None, Phonetics.calculate_phonetic_attributes_of_plain_sequence(u'nere'))
            return [root_ner, root_nere]
        elif lexeme.lemma==u'içeri':
            root_icer = Root(u'içer', lexeme, None, Phonetics.calculate_phonetic_attributes_of_plain_sequence(u'içer'))
            root_iceri = Root(u'içeri', lexeme, None, Phonetics.calculate_phonetic_attributes_of_plain_sequence(u'içeri'))
            return [root_icer, root_iceri]
        elif lexeme.lemma==u'dışarı':
            root_disar = Root(u'dışar', lexeme, None, Phonetics.calculate_phonetic_attributes_of_plain_sequence(u'dışar'))
            root_disari = Root(u'dışarı', lexeme, None, Phonetics.calculate_phonetic_attributes_of_plain_sequence(u'dışarı'))
            return [root_disar, root_disari]
        elif lexeme.lemma==u'birbiri':
            root_birbir = Root(u'birbir', lexeme, None, Phonetics.calculate_phonetic_attributes_of_plain_sequence(u'birbir'))
            root_birbiri = Root(u'birbiri', lexeme, None, Phonetics.calculate_phonetic_attributes_of_plain_sequence(u'birbiri'))
            return [root_birbir, root_birbiri]
        else:
            raise Exception('Unhandled root change : {} !'.format(lexeme))

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
                root_str = root.str
                for (circumflex_char, converted_char) in cls.Circumflex_Letters_Map.iteritems():
                    root_str = root_str.replace(circumflex_char, converted_char)

                root_without_circumflex.str = root_str

                roots.append(root_without_circumflex)


        return roots

class RootMapGenerator(object):
    def generate(self, all_roots):
        root_map = {}
        for root in all_roots:
            key = root.str
            if not root_map.has_key(key):
                root_map[key] = []

            root_map[key].append(root)

        return root_map