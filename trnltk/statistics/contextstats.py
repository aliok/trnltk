# coding=utf-8
from bson.code import Code
import pymongo

class WordBigramQueryBuilder(object):
    def __init__(self):
        self._query = {}
        pass

    def surface(self, str_value, syntactic_category=None):
        self._query['item_1.word.surface.value'] = str_value
        if syntactic_category:
            self._query['item_1.word.surface.syntactic_category'] = syntactic_category

        return self

    def given_surface(self, str_value, syntactic_category=None):
        self._query['item_0.word.surface.value'] = str_value
        if syntactic_category:
            self._query['item_0.word.surface.syntactic_category'] = syntactic_category

        return self

    def stem(self, str_value, syntactic_category=None):
        self._query['item_1.word.stem.value'] = str_value
        if syntactic_category:
            self._query['item_1.word.stem.syntactic_category'] = syntactic_category

        return self

    def given_stem(self, str_value, syntactic_category=None):
        self._query['item_0.word.stem.value'] = str_value
        if syntactic_category:
            self._query['item_0.word.stem.syntactic_category'] = syntactic_category

        return self

    def lemma_root(self, str_value, syntactic_category=None):
        self._query['item_1.word.lemma_root.value'] = str_value
        if syntactic_category:
            self._query['item_1.word.lemma_root.syntactic_category'] = syntactic_category

        return self

    def given_lemma_root(self, str_value, syntactic_category=None):
        self._query['item_0.word.lemma_root.value'] = str_value
        if syntactic_category:
            self._query['item_0.word.lemma_root.syntactic_category'] = syntactic_category

        return self

    def build(self):
        return self._query


class BigramContextProbabilityGenerator(object):
    def __init__(self, collection):
        self._no_context_parsing_likelihood_calculator = NoContextParsingLikelihoodCalculator(collection)
        self._context_parsing_likelihood_calculator = ContextParsingLikelihoodCalculator(collection)

    def generate(self, morpheme_container, context):
        """
        Generates the probability of a morpheme container, aka morphological parse result, with its context
        @type morpheme_container: MorphemeContainer
        @param context: List of tuples for previous words (surface, parse_results_list)
        @type context: list
        """

        #don't attempt parsing the context yet
        previous_word = context[0][0]
        surface_str = morpheme_container.get_surface_so_far()
        surface_syn_cat = morpheme_container.get_surface_syntactic_category()
        stem_str = morpheme_container.get_stem()
        stem_syn_cat = morpheme_container.get_stem_syntactic_category()
        lemma_root_str = morpheme_container.get_root().lexeme.root
        lemma_root_syn_cat = morpheme_container.get_root().lexeme.syntactic_category

        parse_results_of_previous_word = context[0][1]

        likelihood_without_parsing_context = self._no_context_parsing_likelihood_calculator.likelihood(previous_word, lemma_root_str,
            lemma_root_syn_cat,
            stem_str, stem_syn_cat, surface_str, surface_syn_cat)

        likelihood_with_parsing_context = self._context_parsing_likelihood_calculator.likelihood(parse_results_of_previous_word,
            lemma_root_str, lemma_root_syn_cat,
            stem_str, stem_syn_cat, surface_str, surface_syn_cat)

        return 0.2 * likelihood_without_parsing_context + 0.8 * likelihood_with_parsing_context


class NoContextParsingLikelihoodCalculator(object):
    def __init__(self, collection):
        self.collection = collection

    def _count_given_previous_word(self, previous_word):
        self.collection.ensure_index([
            ("item_0.word.surface.value", pymongo.ASCENDING)
        ], name="previous_surface_index", drop_dups=True)

        query_given_previous_word = WordBigramQueryBuilder().given_surface(previous_word).build()
        count_given_previous_word = float(self.collection.find(query_given_previous_word).count())
        return count_given_previous_word

    def _count_surface_given_previous_word(self, previous_word, surface_str, surface_syntactic_category):
        self.collection.ensure_index([
            ("item_0.word.surface.value", pymongo.ASCENDING),
            ("item_1.word.surface.value", pymongo.ASCENDING),
            ("item_1.word.surface.syntactic_category", pymongo.ASCENDING),
        ], name="word_surface_index", drop_dups=True)

        query_surface_given_previous_word = WordBigramQueryBuilder().surface(surface_str, surface_syntactic_category).given_surface(previous_word).build()
        count_surface_given_previous_word = float(self.collection.find(query_surface_given_previous_word).count())
        return count_surface_given_previous_word

    def _count_stem_given_previous_word(self, previous_word, stem_str, stem_syntactic_category):
        self.collection.ensure_index([
            ("item_0.word.surface.value", pymongo.ASCENDING),
            ("item_1.word.stem.value", pymongo.ASCENDING),
            ("item_1.word.stem.syntactic_category", pymongo.ASCENDING),
        ], name="word_stem_index", drop_dups=True)

        query_stem_given_previous_word = WordBigramQueryBuilder().stem(stem_str, stem_syntactic_category).given_surface(previous_word).build()
        count_stem_given_previous_word = float(self.collection.find(query_stem_given_previous_word).count())
        return count_stem_given_previous_word

    def _count_lexeme_given_previous_word(self, previous_word, lemma_root_str, lemma_root_syntactic_category):
        self.collection.ensure_index([
            ("item_0.word.surface.value", pymongo.ASCENDING),
            ("item_1.word.lemma_root.value", pymongo.ASCENDING),
            ("item_1.word.lemma_root.syntactic_category", pymongo.ASCENDING),
        ], name="word_lemma_root_index", drop_dups=True)

        query_lexeme_given_previous_word = WordBigramQueryBuilder().lemma_root(lemma_root_str, lemma_root_syntactic_category).given_surface(previous_word).build()
        count_lexeme_given_previous_word = float(self.collection.find(query_lexeme_given_previous_word).count())
        return count_lexeme_given_previous_word

    def likelihood(self, previous_word, lemma_root_str, lemma_root_syn_cat, stem_str, stem_syn_cat, surface_str, surface_syn_cat):
        count_given_previous_word = self._count_given_previous_word(previous_word)
        count_surface_given_previous_word = self._count_surface_given_previous_word(previous_word, surface_str, surface_syn_cat)
        count_stem_given_previous_word = self._count_stem_given_previous_word(previous_word, stem_str, stem_syn_cat)
        count_lexeme_given_previous_word = self._count_lexeme_given_previous_word(previous_word, lemma_root_str, lemma_root_syn_cat)

        # P(surface + surface_syn_cat | previous word)
        p_surface_given_previous_word = count_surface_given_previous_word / count_given_previous_word if count_given_previous_word else 0.0

        # P(stem + stem_syn_cat | previous word)
        p_stem_given_previous_word = count_stem_given_previous_word / count_given_previous_word if count_given_previous_word else 0.0

        # P(lexeme + lexeme_syn_cat | previous word)
        p_lexeme_given_previous_word = count_lexeme_given_previous_word / count_given_previous_word if count_given_previous_word else 0.0

        #attempt parsing the context words
        return 0.55 * p_surface_given_previous_word + 0.3 * p_stem_given_previous_word + 0.15 * p_lexeme_given_previous_word


class ContextParsingLikelihoodCalculator(object):
    def __init__(self, collection):
        self.collection = collection

    def _count_given_previous_surface(self, previous_surface_str, previous_surface_syn_cat):
        self.collection.ensure_index([
            ("item_0.word.surface.value", pymongo.ASCENDING),
            ("item_0.word.surface.syntactic_category", pymongo.ASCENDING)
        ], name="surface_surface_index", drop_dups=True)

        query_given_previous_surface = WordBigramQueryBuilder().given_surface(previous_surface_str, previous_surface_syn_cat).build()
        count_given_previous_surface = float(self.collection.find(query_given_previous_surface).count())
        return count_given_previous_surface

    def _count_surface_given_previous_surface(self, previous_surface_str, previous_surface_syn_cat, surface_str, surface_syntactic_category):
        self.collection.ensure_index([
            ("item_0.word.surface.value", pymongo.ASCENDING),
            ("item_0.word.surface.syntactic_category", pymongo.ASCENDING),
            ("item_1.word.surface.value", pymongo.ASCENDING),
            ("item_1.word.surface.syntactic_category", pymongo.ASCENDING),
        ], name="surface_surface_index", drop_dups=True)

        query_surface_given_previous_surface = WordBigramQueryBuilder().surface(surface_str, surface_syntactic_category).given_surface(previous_surface_str, previous_surface_syn_cat).build()
        count_surface_given_previous_surface = float(self.collection.find(query_surface_given_previous_surface).count())
        return count_surface_given_previous_surface

    def _count_stem_given_previous_surface(self, previous_surface_str, previous_surface_syn_cat, stem_str, stem_syntactic_category):
        self.collection.ensure_index([
            ("item_0.word.surface.value", pymongo.ASCENDING),
            ("item_0.word.surface.syntactic_category", pymongo.ASCENDING),
            ("item_1.word.stem.value", pymongo.ASCENDING),
            ("item_1.word.stem.syntactic_category", pymongo.ASCENDING),
        ], name="surface_stem_index", drop_dups=True)

        query_stem_given_previous_surface = WordBigramQueryBuilder().stem(stem_str, stem_syntactic_category).given_surface(previous_surface_str, previous_surface_syn_cat).build()
        count_stem_given_previous_surface = float(self.collection.find(query_stem_given_previous_surface).count())
        return count_stem_given_previous_surface

    def _count_lexeme_given_previous_surface(self, previous_surface_str, previous_surface_syn_cat, lemma_root_str, lemma_root_syntactic_category):
        self.collection.ensure_index([
            ("item_0.word.surface.value", pymongo.ASCENDING),
            ("item_0.word.surface.syntactic_category", pymongo.ASCENDING),
            ("item_1.word.lemma_root.value", pymongo.ASCENDING),
            ("item_1.word.lemma_root.syntactic_category", pymongo.ASCENDING),
        ], name="surface_lemma_root_index", drop_dups=True)

        query_lexeme_given_previous_surface = WordBigramQueryBuilder().lemma_root(lemma_root_str, lemma_root_syntactic_category).given_surface(previous_surface_str, previous_surface_syn_cat).build()
        count_lexeme_given_previous_surface = float(self.collection.find(query_lexeme_given_previous_surface).count())
        return count_lexeme_given_previous_surface


    def _count_given_previous_stem(self, previous_stem_str, previous_stem_syn_cat):
        self.collection.ensure_index([
            ("item_0.word.stem.value", pymongo.ASCENDING),
            ("item_0.word.stem.syntactic_category", pymongo.ASCENDING)
        ], name="stem_surface_index", drop_dups=True)

        query_given_previous_stem = WordBigramQueryBuilder().given_stem(previous_stem_str, previous_stem_syn_cat).build()
        count_given_previous_stem = float(self.collection.find(query_given_previous_stem).count())
        return count_given_previous_stem

    def _count_surface_given_previous_stem(self, previous_stem_str, previous_stem_syn_cat, surface_str, surface_syntactic_category):
        self.collection.ensure_index([
            ("item_0.word.stem.value", pymongo.ASCENDING),
            ("item_0.word.stem.syntactic_category", pymongo.ASCENDING),
            ("item_1.word.surface.value", pymongo.ASCENDING),
            ("item_1.word.surface.syntactic_category", pymongo.ASCENDING),
        ], name="stem_surface_index", drop_dups=True)

        query_surface_given_previous_stem = WordBigramQueryBuilder().surface(surface_str, surface_syntactic_category).given_stem(previous_stem_str, previous_stem_syn_cat).build()
        count_surface_given_previous_stem = float(self.collection.find(query_surface_given_previous_stem).count())
        return count_surface_given_previous_stem

    def _count_stem_given_previous_stem(self, previous_stem_str, previous_stem_syn_cat, stem_str, stem_syntactic_category):
        self.collection.ensure_index([
            ("item_0.word.stem.value", pymongo.ASCENDING),
            ("item_0.word.stem.syntactic_category", pymongo.ASCENDING),
            ("item_1.word.stem.value", pymongo.ASCENDING),
            ("item_1.word.stem.syntactic_category", pymongo.ASCENDING),
        ], name="stem_stem_index", drop_dups=True)

        query_stem_given_previous_stem = WordBigramQueryBuilder().stem(stem_str, stem_syntactic_category).given_stem(previous_stem_str, previous_stem_syn_cat).build()
        count_stem_given_previous_stem = float(self.collection.find(query_stem_given_previous_stem).count())
        return count_stem_given_previous_stem

    def _count_lexeme_given_previous_stem(self, previous_stem_str, previous_stem_syn_cat, lemma_root_str, lemma_root_syntactic_category):
        self.collection.ensure_index([
            ("item_0.word.stem.value", pymongo.ASCENDING),
            ("item_0.word.stem.syntactic_category", pymongo.ASCENDING),
            ("item_1.word.lemma_root.value", pymongo.ASCENDING),
            ("item_1.word.lemma_root.syntactic_category", pymongo.ASCENDING),
        ], name="stem_lemma_root_index", drop_dups=True)

        query_lexeme_given_previous_stem = WordBigramQueryBuilder().lemma_root(lemma_root_str, lemma_root_syntactic_category).given_stem(previous_stem_str, previous_stem_syn_cat).build()
        count_lexeme_given_previous_stem = float(self.collection.find(query_lexeme_given_previous_stem).count())
        return count_lexeme_given_previous_stem


    def _count_given_previous_lexeme(self, previous_lemma_root_str, previous_lemma_root_syn_cat):
        self.collection.ensure_index([
            ("item_0.word.lemma_root.value", pymongo.ASCENDING),
            ("item_0.word.lemma_root.syntactic_category", pymongo.ASCENDING)
        ], name="lemma_root_surface_index", drop_dups=True)

        query_given_previous_lexeme = WordBigramQueryBuilder().given_lemma_root(previous_lemma_root_str, previous_lemma_root_syn_cat).build()
        count_given_previous_lexeme = float(self.collection.find(query_given_previous_lexeme).count())
        return count_given_previous_lexeme

    def _count_surface_given_previous_lexeme(self, previous_lemma_root_str, previous_lemma_root_syn_cat, surface_str, surface_syntactic_category):
        self.collection.ensure_index([
            ("item_0.word.lemma_root.value", pymongo.ASCENDING),
            ("item_0.word.lemma_root.syntactic_category", pymongo.ASCENDING),
            ("item_1.word.surface.value", pymongo.ASCENDING),
            ("item_1.word.surface.syntactic_category", pymongo.ASCENDING),
        ], name="lemma_root_surface_index", drop_dups=True)

        query_surface_given_previous_lexeme = WordBigramQueryBuilder().surface(surface_str, surface_syntactic_category).given_lemma_root(previous_lemma_root_str, previous_lemma_root_syn_cat).build()
        count_surface_given_previous_lexeme = float(self.collection.find(query_surface_given_previous_lexeme).count())
        return count_surface_given_previous_lexeme

    def _count_stem_given_previous_lexeme(self, previous_lemma_root_str, previous_lemma_root_syn_cat, stem_str, stem_syntactic_category):
        self.collection.ensure_index([
            ("item_0.word.lemma_root.value", pymongo.ASCENDING),
            ("item_0.word.lemma_root.syntactic_category", pymongo.ASCENDING),
            ("item_1.word.stem.value", pymongo.ASCENDING),
            ("item_1.word.stem.syntactic_category", pymongo.ASCENDING),
        ], name="lemma_root_stem_index", drop_dups=True)

        query_stem_given_previous_lexeme = WordBigramQueryBuilder().stem(stem_str, stem_syntactic_category).given_lemma_root(previous_lemma_root_str, previous_lemma_root_syn_cat).build()
        count_stem_given_previous_lexeme = float(self.collection.find(query_stem_given_previous_lexeme).count())
        return count_stem_given_previous_lexeme

    def _count_lexeme_given_previous_lexeme(self, previous_lemma_root_str, previous_lemma_root_syn_cat, lemma_root_str, lemma_root_syntactic_category):
        self.collection.ensure_index([
            ("item_0.word.lemma_root.value", pymongo.ASCENDING),
            ("item_0.word.lemma_root.syntactic_category", pymongo.ASCENDING),
            ("item_1.word.lemma_root.value", pymongo.ASCENDING),
            ("item_1.word.lemma_root.syntactic_category", pymongo.ASCENDING),
        ], name="lemma_root_lemma_root_index", drop_dups=True)

        query_lexeme_given_previous_lexeme = WordBigramQueryBuilder().lemma_root(lemma_root_str, lemma_root_syntactic_category).given_lemma_root(previous_lemma_root_str, previous_lemma_root_syn_cat).build()
        count_lexeme_given_previous_lexeme = float(self.collection.find(query_lexeme_given_previous_lexeme).count())
        return count_lexeme_given_previous_lexeme


    def _p_word_given_previous_surface(self, morpheme_container, surface_str, surface_syn_cat, stem_str, stem_syn_cat, lemma_root_str, lemma_root_syn_cat):

        previous_surface_str = morpheme_container.get_surface_so_far()
        previous_surface_syn_cat = morpheme_container.get_surface_syntactic_category()

        count_given_previous_surface = self._count_given_previous_surface(previous_surface_str, previous_surface_syn_cat)
        count_surface_given_previous_surface = self._count_surface_given_previous_surface(previous_surface_str, previous_surface_syn_cat, surface_str, surface_syn_cat)
        count_stem_given_previous_surface = self._count_stem_given_previous_surface(previous_surface_str, previous_surface_syn_cat, stem_str, stem_syn_cat)
        count_lexeme_given_previous_surface = self._count_lexeme_given_previous_surface(previous_surface_str, previous_surface_syn_cat, lemma_root_str, lemma_root_syn_cat)

        # P(surface + surface_syn_cat | previous surface + syn_cat)
        p_surface_given_previous_surface = count_surface_given_previous_surface / count_given_previous_surface if count_given_previous_surface else 0.0

        # P(stem + stem_syn_cat | previous surface + syn_cat)
        p_stem_given_previous_surface = count_stem_given_previous_surface / count_given_previous_surface if count_given_previous_surface else 0.0

        # P(lexeme + lexeme_syn_cat | previous surface + syn_cat)
        p_lexeme_given_previous_surface = count_lexeme_given_previous_surface / count_given_previous_surface if count_given_previous_surface else 0.0

        p_word_with_previous_surface = 0.55 * p_surface_given_previous_surface + 0.3 * p_stem_given_previous_surface + 0.15 * p_lexeme_given_previous_surface

        return p_word_with_previous_surface

    def _p_word_given_previous_stem(self, morpheme_container, surface_str, surface_syn_cat, stem_str, stem_syn_cat, lemma_root_str, lemma_root_syn_cat):

        previous_stem_str = morpheme_container.get_stem()
        previous_stem_syn_cat = morpheme_container.get_stem_syntactic_category()

        count_given_previous_stem = self._count_given_previous_stem(previous_stem_str, previous_stem_syn_cat)
        count_surface_given_previous_stem = self._count_surface_given_previous_stem(previous_stem_str, previous_stem_syn_cat, surface_str, surface_syn_cat)
        count_stem_given_previous_stem = self._count_stem_given_previous_stem(previous_stem_str, previous_stem_syn_cat, stem_str, stem_syn_cat)
        count_lexeme_given_previous_stem = self._count_lexeme_given_previous_stem(previous_stem_str, previous_stem_syn_cat, lemma_root_str, lemma_root_syn_cat)

        # P(surface + surface_syn_cat | previous stem + syn_cat)
        p_surface_given_previous_stem = count_surface_given_previous_stem / count_given_previous_stem if count_given_previous_stem else 0.0

        # P(stem + stem_syn_cat | previous stem + syn_cat)
        p_stem_given_previous_stem = count_stem_given_previous_stem / count_given_previous_stem if count_given_previous_stem else 0.0

        # P(lexeme + lexeme_syn_cat | previous stem + syn_cat)
        p_lexeme_given_previous_stem = count_lexeme_given_previous_stem / count_given_previous_stem if count_given_previous_stem else 0.0

        p_word_with_previous_stem = 0.55 * p_surface_given_previous_stem + 0.3 * p_stem_given_previous_stem + 0.15 * p_lexeme_given_previous_stem

        return p_word_with_previous_stem

    def _p_word_given_previous_lexeme(self, morpheme_container, surface_str, surface_syn_cat, stem_str, stem_syn_cat, lemma_root_str, lemma_root_syn_cat):

        previous_lemma_root_str = morpheme_container.get_root().lexeme.root
        previous_lemma_root_syn_cat = morpheme_container.get_root().lexeme.syntactic_category

        count_given_previous_lexeme = self._count_given_previous_lexeme(previous_lemma_root_str, previous_lemma_root_syn_cat)
        count_surface_given_previous_lexeme = self._count_surface_given_previous_lexeme(previous_lemma_root_str, previous_lemma_root_syn_cat, surface_str, surface_syn_cat)
        count_stem_given_previous_lexeme = self._count_stem_given_previous_lexeme(previous_lemma_root_str, previous_lemma_root_syn_cat, stem_str, stem_syn_cat)
        count_lexeme_given_previous_lexeme = self._count_lexeme_given_previous_lexeme(previous_lemma_root_str, previous_lemma_root_syn_cat, lemma_root_str, lemma_root_syn_cat)

        # P(surface + surface_syn_cat | previous lemma + syn_cat)
        p_surface_given_previous_lexeme = count_surface_given_previous_lexeme / count_given_previous_lexeme if count_given_previous_lexeme else 0.0

        # P(stem + stem_syn_cat | previous lemma + syn_cat)
        p_stem_given_previous_lexeme = count_stem_given_previous_lexeme / count_given_previous_lexeme if count_given_previous_lexeme else 0.0

        # P(lexeme + lexeme_syn_cat | previous lemma + syn_cat)
        p_lexeme_given_previous_lexeme = count_lexeme_given_previous_lexeme / count_given_previous_lexeme if count_given_previous_lexeme else 0.0

        p_word_with_previous_lexeme = 0.55 * p_surface_given_previous_lexeme + 0.3 * p_stem_given_previous_lexeme + 0.15 * p_lexeme_given_previous_lexeme

        return p_word_with_previous_lexeme

    def likelihood(self, parse_results_of_previous_word, lemma_root_str, lemma_root_syn_cat, stem_str, stem_syn_cat, surface_str, surface_syn_cat):
        total = 0.0

        for morpheme_container in parse_results_of_previous_word:
            p_word_given_previous_surface = self._p_word_given_previous_surface(morpheme_container, surface_str, surface_syn_cat, stem_str, stem_syn_cat, lemma_root_str, lemma_root_syn_cat)
            p_word_given_previous_stem = self._p_word_given_previous_stem(morpheme_container, surface_str, surface_syn_cat, stem_str, stem_syn_cat, lemma_root_str, lemma_root_syn_cat)
            p_word_given_previous_lexeme = self._p_word_given_previous_lexeme(morpheme_container, surface_str, surface_syn_cat, stem_str, stem_syn_cat, lemma_root_str, lemma_root_syn_cat)

            total += 0.55 * p_word_given_previous_surface + 0.3 * p_word_given_previous_stem + 0.15 * p_word_given_previous_lexeme


        return total / float(len(parse_results_of_previous_word))