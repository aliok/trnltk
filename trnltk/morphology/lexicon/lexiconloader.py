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
import codecs
from trnltk.morphology.phonetics.alphabet import TurkishAlphabet
from trnltk.morphology.model.lexeme import Lexeme, SyntacticCategory, SecondarySyntacticCategory, LexemeAttribute

class LexiconLoader(object):

    @classmethod
    def load_from_file(cls, file_path):
        lexemes = set()

        with codecs.open(file_path, mode='r', encoding='utf-8') as dictionary_file:
            lexemes = cls.load_from_lines(dictionary_file)

        return lexemes

    @classmethod
    def load_from_lines(cls, lines):
        lexemes = set()

        for line in lines:
            line = line.strip()
            if line.startswith('#'):
                continue

            try:
                lexeme = cls._crate_lexeme_from_line(line)
                cls._set_category_and_lemma(lexeme)
                cls._infer_morphemic_attributes(lexeme)
                if lexeme.attributes:
                    lexeme.attributes = set(lexeme.attributes)
            except:
                print 'Error in line: ', line
                raise
            lexemes.add(lexeme)

        return lexemes

    @classmethod
    def _crate_lexeme_from_line(cls, line):
        syntactic_category = None
        secondary_syntactic_category = None
        attributes = {}

        (str_root, str_meta) = line.split('[') if '[' in line else (line, None)

        str_root = str_root.strip()
        lemma = root = str_root

        str_meta = str_meta.strip() if str_meta else None
        assert str_meta is None or '[' not in str_meta

        str_meta = str_meta[:-1].strip() if str_meta else None
        assert str_meta is None or ']' not in str_meta

        if str_meta:
            str_metas = str_meta.split(';')
            for str_meta_part in str_metas:
                str_meta_part = str_meta_part.strip()
                if str_meta_part.startswith('P:'):
                    (syntactic_category, secondary_syntactic_category) = str_meta_part[len('P:'):].split(',') if ',' in str_meta_part else (str_meta_part[len('P:'):], None)
                    syntactic_category = syntactic_category.strip() if syntactic_category else None
                    secondary_syntactic_category = secondary_syntactic_category.strip() if secondary_syntactic_category else None
                elif str_meta_part.startswith('A:'):
                    str_attributes = str_meta_part[len('A:'):]
                    attributes = set(str_attributes.split(','))
                    attributes = set([a.strip() for a in attributes])
                elif str_meta_part.startswith('R:'):
                    root = str_meta_part[len('R:'):]
                elif str_meta_part.startswith('S:'):
                    pass
                else:
                    raise Exception('Unable to parse line' + line)

        return Lexeme(lemma, root, syntactic_category, secondary_syntactic_category, attributes or None)

    @classmethod
    def _set_category_and_lemma(cls, lexeme):
        item_root = lexeme.root

        if item_root[0].isupper():
            lexeme.syntactic_category = SyntacticCategory.NOUN
            lexeme.secondary_syntactic_category = SecondarySyntacticCategory.PROPER_NOUN

        elif not lexeme.syntactic_category and not lexeme.secondary_syntactic_category:
            if item_root.endswith(u'mak') or item_root.endswith(u'mek'):
                lexeme.syntactic_category = SyntacticCategory.VERB
                lexeme.root = item_root[:-3]
            else:
                lexeme.syntactic_category = SyntacticCategory.NOUN

    @classmethod
    def _infer_morphemic_attributes(cls, lexeme):
        """
        @type lexeme: Lexeme
        """
        item_root = lexeme.root
        root_vowel_count = cls._vowel_count(item_root)
        last_letter = TurkishAlphabet.get_letter_for_char(item_root[-1])

        if lexeme.syntactic_category==SyntacticCategory.VERB:
            if last_letter.vowel:
                lexeme.attributes.add(LexemeAttribute.ProgressiveVowelDrop)
                lexeme.attributes.add(LexemeAttribute.Passive_In)

            if root_vowel_count>1 and LexemeAttribute.Aorist_A not in lexeme.attributes:
                lexeme.attributes.add(LexemeAttribute.Aorist_I)

            if root_vowel_count==1 and LexemeAttribute.Aorist_I not in lexeme.attributes:
                lexeme.attributes.add(LexemeAttribute.Aorist_A)

            if last_letter==TurkishAlphabet.L_l:
                lexeme.attributes.add(LexemeAttribute.Passive_In)

            if all(a not in lexeme.attributes for a in LexemeAttribute.CAUSATIVES):
                if last_letter.vowel or (last_letter in [TurkishAlphabet.L_l, TurkishAlphabet.L_r]) and root_vowel_count>1:
                    lexeme.attributes.add(LexemeAttribute.Causative_t)
                elif last_letter==TurkishAlphabet.L_t and root_vowel_count<2:
                    lexeme.attributes.add(LexemeAttribute.Causative_Ir)
                else:
                    lexeme.attributes.add(LexemeAttribute.Causative_dIr)

            if LexemeAttribute.ProgressiveVowelDrop in lexeme.attributes:
                lexeme.attributes.add(LexemeAttribute.NoVoicing)

            if LexemeAttribute.Voicing not in lexeme.attributes and LexemeAttribute.NoVoicing not in lexeme.attributes:
                lexeme.attributes.add(LexemeAttribute.NoVoicing)

        elif lexeme.syntactic_category==SyntacticCategory.NOUN and LexemeAttribute.CompoundP3sg in lexeme.attributes:
            if LexemeAttribute.VoicingOpt in lexeme.attributes:
                if LexemeAttribute.Voicing in lexeme.attributes:
                    lexeme.attributes.remove(LexemeAttribute.Voicing)
                if LexemeAttribute.NoVoicing in lexeme.attributes:
                    lexeme.attributes.remove(LexemeAttribute.NoVoicing)
            elif LexemeAttribute.Voicing not in lexeme.attributes:
                lexeme.attributes.add(LexemeAttribute.NoVoicing)

        elif lexeme.syntactic_category in [SyntacticCategory.NOUN, SyntacticCategory.ADJECTIVE]:
            if LexemeAttribute.VoicingOpt in lexeme.attributes:
                if LexemeAttribute.Voicing in lexeme.attributes:
                    lexeme.attributes.remove(LexemeAttribute.Voicing)
                if LexemeAttribute.NoVoicing in lexeme.attributes:
                    lexeme.attributes.remove(LexemeAttribute.NoVoicing)
            else:
                if root_vowel_count>1 and last_letter.voiceless and not last_letter.continuant and LexemeAttribute.NoVoicing not in lexeme.attributes \
                and LexemeAttribute.InverseHarmony not in lexeme.attributes:
                    lexeme.attributes.add(LexemeAttribute.Voicing)
                elif item_root.endswith('nk') or item_root.endswith('og') or item_root.endswith('rt'):
                    lexeme.attributes.add(LexemeAttribute.Voicing)
                elif LexemeAttribute.Voicing not in lexeme.attributes:
                    lexeme.attributes.add(LexemeAttribute.NoVoicing)

    @classmethod
    def _vowel_count(cls, seq):
        vowel_count = 0
        for c in seq:
            if TurkishAlphabet.get_letter_for_char(c).vowel:
                vowel_count += 1

        return vowel_count
