from trnltk.ngrams.ngramgenerator import NGramGenerator

class LexemeNGramGenerator(NGramGenerator):
    def __init__(self, n):
        extractor = lambda word_binding: (word_binding.root.lemma_root, word_binding.root.syntactic_category)
        super(LexemeNGramGenerator, self).__init__(n, extractor, ("<s>", "<s>"), ("</s>", "</s>"))

class StemNGramGenerator(NGramGenerator):
    def __init__(self, n):
        extractor = lambda word_binding: word_binding.root.str
        super(StemNGramGenerator, self).__init__(n, extractor, "<s>", "</s>")

