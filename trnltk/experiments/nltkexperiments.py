from nltk.corpus import gutenberg
from nltk.text import Text

def doit():
    moby = Text(gutenberg.words('melville-moby_dick.txt'))
    moby.concordance('fight')


if __name__ == '__main__':
    doit()