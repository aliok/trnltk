import codecs
import os

def write_proper_nouns():
    dictionary_file = os.path.join(os.path.dirname(__file__), '../resources/master_dictionary.txt')
    for line in open(dictionary_file):
        line = line.strip()
        if line.startswith('#'):
            continue
        elif line[0].isupper():
            print line

def remove_proper_nouns():
    dictionary_file = os.path.join(os.path.dirname(__file__), '../resources/master_dictionary.txt')
    out_file = os.path.join(os.path.dirname(__file__), '../resources/new_master_dictionary.txt')
    with open(dictionary_file) as src:
        with codecs.open(out_file, 'w', encoding='utf-8') as out:
            for line in src:
                line = line.strip()
                if line.startswith('#'):
                    continue
                elif line[0].isupper():
                    print line
                else:
                    out.write(line.decode('utf-8'))
                    out.write('\n')

if __name__ == '__main__':
    #write_proper_nouns()
    remove_proper_nouns()