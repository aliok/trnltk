from trnltk.ngrams.ngramgenerator import NGramGenerator
from trnltk.parseset.xmlbindings import DerivationalSuffixBinding

class LexemeNGramGenerator(NGramGenerator):
    def __init__(self, n):
        extractor = lambda word_binding: (word_binding.root.lemma_root, word_binding.root.syntactic_category)
        super(LexemeNGramGenerator, self).__init__(n, extractor, ("<s>", "<s>"), ("</s>", "</s>"))

class StemNGramGenerator(NGramGenerator):
    def __init__(self, n):
        extractor = self._get_stem
        super(StemNGramGenerator, self).__init__(n, extractor, "<s>", "</s>")

    @classmethod
    def _get_stem(cls, word_binding):
        """
        Returns the stem of the surface. For example, stem of "kitapcilar" is "kitapci".
        So, the finding process is basically removing the inflections at the end, until there is a derivation.
        @type word_binding: WordBinding
        """
        if not word_binding.suffixes:
            return word_binding.str


        indexes_of_derivational_suffixes = [i for i in range(len(word_binding.suffixes)) if isinstance(word_binding.suffixes[i], DerivationalSuffixBinding)]
        if indexes_of_derivational_suffixes:
            index_of_last_derivational_suffix = indexes_of_derivational_suffixes[-1]
            return word_binding.suffixes[index_of_last_derivational_suffix].word
        else:
            return word_binding.str
