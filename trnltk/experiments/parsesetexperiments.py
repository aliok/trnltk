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

def write_apostophes_without_proper_nouns(parse_set_index):
    parse_set_file_path = os.path.join(os.path.dirname(__file__), '../testresources/simpleparsesets/simpleparseset{}.txt'.format(parse_set_index))
    with codecs.open(parse_set_file_path, mode='r', encoding='utf-8') as parse_set_file:
        for line in parse_set_file:
            line = line.strip()
            if line.startswith('#'):
                continue

            if "'" in line and "Noun+Prop" not in line:
                print line


def write_proper_nouns_without_apostrophe(parse_set_index):
    parse_set_file_path = os.path.join(os.path.dirname(__file__), '../testresources/simpleparsesets/simpleparseset{}.txt'.format(parse_set_index))
    with codecs.open(parse_set_file_path, mode='r', encoding='utf-8') as parse_set_file:
        for line in parse_set_file:
            line = line.strip()
            if line.startswith('#'):
                continue

            if "'" not in line and "Prop" in line:
                propnoun = line[line.index('(1,"') + 4:line.index('+', line.index('(1,"'))]
                word = line.split('=')[0]
                if propnoun != word:
                    print line


def find_word_count(parse_set_index):
    count = 0
    parse_set_file_path = os.path.join(os.path.dirname(__file__), '../testresources/simpleparsesets/simpleparseset{}.txt'.format(parse_set_index))
    with codecs.open(parse_set_file_path, mode='r', encoding='utf-8') as parse_set_file:
        for line in parse_set_file:
            line = line.strip()
            if line.startswith('#'):
                continue

            count += 1

    print count


def print_parseset(parse_set_index, percent = 0.1):
    out = u''
    parse_set_file_path = os.path.join(os.path.dirname(__file__), '../testresources/simpleparsesets/simpleparseset{}.txt'.format(parse_set_index))
    with codecs.open(parse_set_file_path, mode='r', encoding='utf-8') as parse_set_file:
        for line in parse_set_file:
            line = line.strip()
            if line.startswith('#'):
                out += u"\n"
            else:
                word = line.split('=')[0]
                out += word + u' '

    i = int(1.0 * percent * float(len(out)))
    print i
    print len(out)
    test_data = out[0:i]

    print test_data


if __name__ == '__main__':
#    write_apostophes_without_proper_nouns("005")
#    write_proper_nouns_without_apostrophe("005")
#    find_word_count("005")
    print_parseset("005", 0.5)