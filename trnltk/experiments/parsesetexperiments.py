import os

def write_apos_without_proper_nouns():
    dictionary_file = os.path.join(os.path.dirname(__file__), '../testresources/simpleparsesets/parseset999.txt')
    for line in open(dictionary_file):
        line = line.strip()
        if "'" in line and "Noun+Prop" not in line:
            print line

def write_proper_nouns_without_apos():
    dictionary_file = os.path.join(os.path.dirname(__file__), '../testresources/simpleparsesets/parseset999.txt')
    for line in open(dictionary_file):
        line = line.strip()
        if "'" not in line and "Prop" in line:
            propnoun = line[line.index('(1,"')+4:line.index('+', line.index('(1,"'))]
            word = line.split('=')[0]
            if propnoun!=word:
                print line



if __name__ == '__main__':
    #write_apos_without_proper_nouns()
    write_proper_nouns_without_apos()