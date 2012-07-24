import codecs
from trnltk.phonetics.alphabet import TurkishAlphabet
from trnltk.stem.dictionaryitem import DictionaryItem, PrimaryPosition, SecondaryPosition, RootAttribute

__author__ = 'ali'

class DictionaryLoader(object):

    @classmethod
    def load_from_file(cls, file_path):
        dictionary_items = set()

        with codecs.open(file_path, mode='r', encoding='utf-8') as dictionary_file:
            dictionary_items = cls.load_from_lines(dictionary_file)

        return dictionary_items

    @classmethod
    def load_from_lines(cls, lines):
        dictionary_items = set()

        for line in lines:
            line = line.strip()
            if line.startswith('#'):
                continue

            try:
                dictionary_item = cls._crate_dictionary_item_from_line(line)
                cls._set_position_and_lemma(dictionary_item)
                cls._infer_morphemic_attributes(dictionary_item)
                if dictionary_item.attributes:
                    dictionary_item.attributes = sorted(list(set(dictionary_item.attributes)))
            except:
                print 'Error in line: ', line
                raise
            dictionary_items.add(dictionary_item)

        return dictionary_items

    @classmethod
    def _crate_dictionary_item_from_line(cls, line):
        primary_position = None
        secondary_position = None
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
                    (primary_position, secondary_position) = str_meta_part[len('P:'):].split(',') if ',' in str_meta_part else (str_meta_part[len('P:'):], None)
                    primary_position = primary_position.strip() if primary_position else None
                    secondary_position = secondary_position.strip() if secondary_position else None
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

        return DictionaryItem(lemma, root, primary_position, secondary_position, attributes or None)

    @classmethod
    def _set_position_and_lemma(cls, dictionary_item):
        item_root = dictionary_item.root

        if item_root[0].isupper():
            dictionary_item.primary_position = PrimaryPosition.NOUN
            dictionary_item.secondary_position = SecondaryPosition.PROPER_NOUN

        elif not dictionary_item.primary_position and not dictionary_item.secondary_position:
            if item_root.endswith(u'mak') or item_root.endswith(u'mek'):
                dictionary_item.primary_position = PrimaryPosition.VERB
                dictionary_item.root = item_root[:-3]
            else:
                dictionary_item.primary_position = PrimaryPosition.NOUN

    @classmethod
    def _infer_morphemic_attributes(cls, dictionary_item):
        item_root = dictionary_item.root
        root_vowel_count = cls._vowel_count(item_root)
        last_letter = TurkishAlphabet.get_letter_for_char(item_root[-1])

        if dictionary_item.primary_position==PrimaryPosition.VERB:
            if last_letter.vowel and RootAttribute.Passive_NotApplicable not in dictionary_item.attributes:
                dictionary_item.attributes.append(RootAttribute.ProgressiveVowelDrop)
                dictionary_item.attributes.append(RootAttribute.Passive_In)

            if root_vowel_count>1 and RootAttribute.Aorist_A not in dictionary_item.attributes:
                dictionary_item.attributes.append(RootAttribute.Aorist_I)

            if root_vowel_count==1 and RootAttribute.Aorist_I not in dictionary_item.attributes:
                dictionary_item.attributes.append(RootAttribute.Aorist_A)

            if last_letter==TurkishAlphabet.L_l and RootAttribute.Passive_NotApplicable not in dictionary_item.attributes:
                dictionary_item.attributes.append(RootAttribute.Passive_In)

            if all(a not in dictionary_item.attributes for a in RootAttribute.CAUSATIVES):
                if last_letter.vowel or (last_letter in [TurkishAlphabet.L_l, TurkishAlphabet.L_r]) and root_vowel_count>1:
                    dictionary_item.attributes.append(RootAttribute.Causative_t)
                elif last_letter==TurkishAlphabet.L_t and root_vowel_count<2:
                    dictionary_item.attributes.append(RootAttribute.Causative_Ir)
                else:
                    dictionary_item.attributes.append(RootAttribute.Causative_dIr)

            if RootAttribute.ProgressiveVowelDrop in dictionary_item.attributes:
                dictionary_item.attributes.append(RootAttribute.NoVoicing)

            if RootAttribute.Voicing not in dictionary_item.attributes and RootAttribute.NoVoicing not in dictionary_item.attributes:
                dictionary_item.attributes.append(RootAttribute.NoVoicing)

        elif dictionary_item.primary_position==PrimaryPosition.NOUN and RootAttribute.CompoundP3sg in dictionary_item.attributes:
            if RootAttribute.VoicingOpt in dictionary_item.attributes:
                if RootAttribute.Voicing in dictionary_item.attributes:
                    dictionary_item.attributes.remove(RootAttribute.Voicing)
                if RootAttribute.NoVoicing in dictionary_item.attributes:
                    dictionary_item.attributes.remove(RootAttribute.NoVoicing)
            elif RootAttribute.Voicing not in dictionary_item.attributes:
                dictionary_item.attributes.append(RootAttribute.NoVoicing)

        elif dictionary_item.primary_position in [PrimaryPosition.NOUN, PrimaryPosition.ADJECTIVE]:
            if RootAttribute.VoicingOpt in dictionary_item.attributes:
                if RootAttribute.Voicing in dictionary_item.attributes:
                    dictionary_item.attributes.remove(RootAttribute.Voicing)
                if RootAttribute.NoVoicing in dictionary_item.attributes:
                    dictionary_item.attributes.remove(RootAttribute.NoVoicing)
            else:
                if root_vowel_count>1 and last_letter.stop_consonant and RootAttribute.NoVoicing not in dictionary_item.attributes \
                and RootAttribute.InverseHarmony not in dictionary_item.attributes:
                    dictionary_item.attributes.append(RootAttribute.Voicing)
                elif item_root.endswith('nk') or item_root.endswith('og') or item_root.endswith('rt'):
                    dictionary_item.attributes.append(RootAttribute.Voicing)
                elif RootAttribute.Voicing not in dictionary_item.attributes:
                    dictionary_item.attributes.append(RootAttribute.NoVoicing)

    @classmethod
    def _vowel_count(cls, seq):
        vowel_count = 0
        for c in seq:
            if TurkishAlphabet.get_letter_for_char(c).vowel:
                vowel_count += 1

        return vowel_count
