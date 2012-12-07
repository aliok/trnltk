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
import codecs
import os

def print_proper_nouns():
    dictionary_file_path = os.path.join(os.path.dirname(__file__), '../resources/master_dictionary.txt')
    with codecs.open(dictionary_file_path, mode='r', encoding='utf-8') as parse_set_file:
        for line in parse_set_file:
            line = line.strip()
            if line.startswith('#'):
                continue
            elif line[0].isupper():
                print line


def remove_proper_nouns():
    out_file = os.path.join(os.path.dirname(__file__), '../resources/new_master_dictionary.txt')
    dictionary_file = os.path.join(os.path.dirname(__file__), '../resources/master_dictionary.txt')
    with codecs.open(dictionary_file, 'r', 'utf-8') as src:
        with codecs.open(out_file, 'w', encoding='utf-8') as out:
            for line in src:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                elif line[0].isupper():
                    print line
                else:
                    out.write(line)
                    out.write('\n')


def test_Turkish_char_sorting():
    import locale

    locale.setlocale(locale.LC_ALL, 'tr_TR.UTF-8')

    chars = u'''abcçdefgğhıijklmnoöprsştuüvyzqwxâîûABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZQWXÂÎÛ.,?!'"/+-(){}%;:àèïÄÏÿ'''

    chars = sorted(chars, cmp=locale.strcoll)
    chars = u''.join(chars)

    print chars

def generate_sorted_dictionary():
    import locale

    locale.setlocale(locale.LC_ALL, 'tr_TR.UTF-8')

    header = '''
        #
        # Copyright  2012  Zemberek3 Developers <http://code.google.com/p/zemberek3/> (Original work)
        # Copyright  2012  Ali Ok (aliokATapacheDOTorg) (Derivative work)
        #
        # Licensed under the Apache License, Version 2.0 (the "License");
        # you may not use this file except in compliance with the License.
        # You may obtain a copy of the License at
        #
        #    http://www.apache.org/licenses/LICENSE-2.0
        #
        # Unless required by applicable law or agreed to in writing, software
        # distributed under the License is distributed on an "AS IS" BASIS,
        # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
        # See the License for the specific language governing permissions and
        # limitations under the License.
        #
    '''

    header = header.strip()
    header = u'\n'.join([l.strip() for l in header.splitlines()])

    dictionary_file = os.path.join(os.path.dirname(__file__), '../resources/master_dictionary.txt')
    out_file = os.path.join(os.path.dirname(__file__), '../resources/new_master_dictionary.txt')

    src_lines = []

    with codecs.open(dictionary_file, 'r', 'utf-8') as src:
        for line in src:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            # need to make "a [P:xxx]" come before "a"
            # thus sort by lemma root, not the whole line
            lemma_root = line[:line.index('[')] if '[' in line else line
            lemma_root = lemma_root.strip()

            src_lines.append((lemma_root, line))

    src_lines = sorted(src_lines, cmp=locale.strcoll, key=lambda tup: tup[0])

    with codecs.open(out_file, 'w', encoding='utf-8') as out:
        out.write(header)
        out.write('\n')
        for line in src_lines:
            out.write(line[1])
            out.write('\n')




if __name__ == '__main__':
#    print_proper_nouns()
#    remove_proper_nouns()
#    test_Turkish_char_sorting()
    generate_sorted_dictionary()