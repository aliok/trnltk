import codecs
from trnltk.morphology.phonetics.alphabet import TurkishAlphabet
from trnltk.morphology.lexiconmodel.lexeme import Lexeme, SyntacticCategory, SecondarySyntacticCategory, RootAttribute

__author__ = 'ali'

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
                    lexeme.attributes = sorted(list(set(lexeme.attributes)))
            except:
                print 'Error in line: ', line
                raise
            lexemes.add(lexeme)

        return lexemes

    @classmethod
    def _crate_lexeme_from_line(cls, line):
        syntactic_category = None
        secondary_syntactic_category = None
        attributes = []

        (str_root, str_meta) = line.split('[') if '[' in line else (line, None)

        str_root = str_root.strip()
        lemma = root = str_root

        str_meta = str_meta.strip() if str_meta else None
        str_meta = str_meta[:-1].strip() if str_meta else None

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
                    attributes = str_attributes.split(',')
                    attributes = [a.strip() for a in attributes]
                elif str_meta_part.startswith('R:'):
                    root = str_meta_part[len('R:'):]
                elif str_meta_part.startswith('S:'):
                    pass
                else:
                    raise Exception('Unable to parse line' + line)

                ##todo: S:rel_ki stuff is skipped

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
        item_root = lexeme.root
        root_vowel_count = cls._vowel_count(item_root)
        last_letter = TurkishAlphabet.get_letter_for_char(item_root[-1])

        if lexeme.syntactic_category==SyntacticCategory.VERB:
            if last_letter.vowel and RootAttribute.Passive_NotApplicable not in lexeme.attributes:
                lexeme.attributes.append(RootAttribute.ProgressiveVowelDrop)
                lexeme.attributes.append(RootAttribute.Passive_In)

            if root_vowel_count>1 and RootAttribute.Aorist_A not in lexeme.attributes:
                lexeme.attributes.append(RootAttribute.Aorist_I)

            if root_vowel_count==1 and RootAttribute.Aorist_I not in lexeme.attributes:
                lexeme.attributes.append(RootAttribute.Aorist_A)

            if last_letter==TurkishAlphabet.L_l and RootAttribute.Passive_NotApplicable not in lexeme.attributes:
                lexeme.attributes.append(RootAttribute.Passive_In)

            if all(a not in lexeme.attributes for a in RootAttribute.CAUSATIVES):
                if last_letter.vowel or (last_letter in [TurkishAlphabet.L_l, TurkishAlphabet.L_r]) and root_vowel_count>1:
                    lexeme.attributes.append(RootAttribute.Causative_t)
                elif last_letter==TurkishAlphabet.L_t and root_vowel_count<2:
                    lexeme.attributes.append(RootAttribute.Causative_Ir)
                else:
                    lexeme.attributes.append(RootAttribute.Causative_dIr)

            if RootAttribute.ProgressiveVowelDrop in lexeme.attributes:
                lexeme.attributes.append(RootAttribute.NoVoicing)

            if RootAttribute.Voicing not in lexeme.attributes and RootAttribute.NoVoicing not in lexeme.attributes:
                lexeme.attributes.append(RootAttribute.NoVoicing)

        elif lexeme.syntactic_category==SyntacticCategory.NOUN and RootAttribute.CompoundP3sg in lexeme.attributes:
            if RootAttribute.VoicingOpt in lexeme.attributes:
                if RootAttribute.Voicing in lexeme.attributes:
                    lexeme.attributes.remove(RootAttribute.Voicing)
                if RootAttribute.NoVoicing in lexeme.attributes:
                    lexeme.attributes.remove(RootAttribute.NoVoicing)
            elif RootAttribute.Voicing not in lexeme.attributes:
                lexeme.attributes.append(RootAttribute.NoVoicing)

        elif lexeme.syntactic_category in [SyntacticCategory.NOUN, SyntacticCategory.ADJECTIVE]:
            if RootAttribute.VoicingOpt in lexeme.attributes:
                if RootAttribute.Voicing in lexeme.attributes:
                    lexeme.attributes.remove(RootAttribute.Voicing)
                if RootAttribute.NoVoicing in lexeme.attributes:
                    lexeme.attributes.remove(RootAttribute.NoVoicing)
            else:
                if root_vowel_count>1 and last_letter.stop_consonant and RootAttribute.NoVoicing not in lexeme.attributes \
                and RootAttribute.InverseHarmony not in lexeme.attributes:
                    lexeme.attributes.append(RootAttribute.Voicing)
                elif item_root.endswith('nk') or item_root.endswith('og') or item_root.endswith('rt'):
                    lexeme.attributes.append(RootAttribute.Voicing)
                elif RootAttribute.Voicing not in lexeme.attributes:
                    lexeme.attributes.append(RootAttribute.NoVoicing)

    @classmethod
    def _vowel_count(cls, seq):
        vowel_count = 0
        for c in seq:
            if TurkishAlphabet.get_letter_for_char(c).vowel:
                vowel_count += 1

        return vowel_count
