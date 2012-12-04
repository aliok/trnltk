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
import unittest
from hamcrest.core.assert_that import assert_that
from trnltk.ngrams.ngramgenerator import NGramGenerator
from trnltk.parseset.xmlbindings import  UnparsableWordBinding, WordBinding, RootBinding
from hamcrest import *

class GenericGramGeneratorTest(unittest.TestCase):
    root1 = RootBinding("root1", "lemma1", "lemma_root1", "root_synt_cat1", None)
    root2 = RootBinding("root2", "lemma2", "lemma_root2", "root_synt_cat2", None)
    root4 = RootBinding("root4", "lemma4", "lemma_root4", "root_synt_cat4", None)
    root5 = RootBinding("root5", "lemma5", "lemma_root5", "root_synt_cat5", None)

    word1 = WordBinding("surface_1", "word1_parse_result", root1, "word1_synt_cat", None, None)
    word2 = WordBinding("surface_2", "word2_parse_result", root2, "word2_synt_cat", None, None)
    word3 = UnparsableWordBinding("surface_1")
    word4 = WordBinding("surface_4", "word4_parse_result", root4, "word4_synt_cat", None, None)
    word5 = WordBinding("surface_5", "word5_parse_result", root5, "word5_synt_cat", None, None)

    words = [word1, word2, word3, word4, word5]

    def test_create_unigrams(self):
        extractor = lambda word_binding: (word_binding.root.lemma_root, word_binding.root.syntactic_category)
        generator = NGramGenerator(1, extractor, ("<s>", "<s>"), ("</s>", "</s>"))
        ngrams = generator.get_ngrams(self.words)

        assert_that(ngrams, has_length(4))

        lexeme1 = ("lemma_root1", "root_synt_cat1")
        lexeme2 = ("lemma_root2", "root_synt_cat2")
        lexeme4 = ("lemma_root4", "root_synt_cat4")
        lexeme5 = ("lemma_root5", "root_synt_cat5")

        assert_that(ngrams, has_item(lexeme1))
        assert_that(ngrams, has_item(lexeme2))
        assert_that(ngrams, has_item(lexeme4))
        assert_that(ngrams, has_item(lexeme5))

    def test_create_bigrams(self):
        extractor = lambda word_binding: (word_binding.root.lemma_root, word_binding.root.syntactic_category)
        generator = NGramGenerator(2, extractor, ("<s>", "<s>"), ("</s>", "</s>"))
        ngrams = generator.get_ngrams(self.words)

        assert_that(ngrams, has_length(5))

        start_lexeme = ("<s>", "<s>")
        lexeme1 = ("lemma_root1", "root_synt_cat1")
        lexeme2 = ("lemma_root2", "root_synt_cat2")
        lexeme4 = ("lemma_root4", "root_synt_cat4")
        lexeme5 = ("lemma_root5", "root_synt_cat5")
        end_lexeme = ("</s>", "</s>")

        assert_that(ngrams, has_item((start_lexeme, lexeme1)))
        assert_that(ngrams, has_item((lexeme1, lexeme2)))
        assert_that(ngrams, has_item((lexeme2, lexeme4)))
        assert_that(ngrams, has_item((lexeme4, lexeme5)))
        assert_that(ngrams, has_item((lexeme5, end_lexeme)))

    def test_create_trigrams(self):
        extractor = lambda word_binding: (word_binding.root.lemma_root, word_binding.root.syntactic_category)
        generator = NGramGenerator(3, extractor, ("<s>", "<s>"), ("</s>", "</s>"))
        ngrams = generator.get_ngrams(self.words)

        assert_that(ngrams, has_length(6))

        start_lexeme = ("<s>", "<s>")
        lexeme1 = ("lemma_root1", "root_synt_cat1")
        lexeme2 = ("lemma_root2", "root_synt_cat2")
        lexeme4 = ("lemma_root4", "root_synt_cat4")
        lexeme5 = ("lemma_root5", "root_synt_cat5")
        end_lexeme = ("</s>", "</s>")

        assert_that(ngrams, has_item((start_lexeme, start_lexeme, lexeme1)))
        assert_that(ngrams, has_item((start_lexeme, lexeme1, lexeme2)))
        assert_that(ngrams, has_item((lexeme1, lexeme2, lexeme4)))
        assert_that(ngrams, has_item((lexeme2, lexeme4, lexeme5)))
        assert_that(ngrams, has_item((lexeme4, lexeme5, end_lexeme)))
        assert_that(ngrams, has_item((lexeme5, end_lexeme, end_lexeme)))


if __name__ == '__main__':
    unittest.main()

