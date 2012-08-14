# coding=utf-8
import pymongo

class WordBigramQueryBuilder(object):
    def __init__(self):
        self._query = {}

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

    def generate(self, morpheme_container, leading_context, following_context):
        """
        Generates the probability of a morpheme container, aka morphological parse result, with its context
        @type morpheme_container: MorphemeContainer
        @param leading_context: List of tuples for leading words (surface, parse_results_list)
        @type leading_context: list
        @param following_context: List of tuples for following words (surface, parse_results_list)
        @type following_context: list
        """

        #don't attempt parsing the leading_context yet
        leading_word = leading_context[0][0]
        following_word = following_context[0][0]

        surface_str = morpheme_container.get_surface_so_far()
        surface_syn_cat = morpheme_container.get_surface_syntactic_category()
        stem_str = morpheme_container.get_stem()
        stem_syn_cat = morpheme_container.get_stem_syntactic_category()
        lemma_root_str = morpheme_container.get_root().lexeme.root
        lemma_root_syn_cat = morpheme_container.get_root().lexeme.syntactic_category

        parse_results_of_leading_word = leading_context[0][1]

        likelihood_without_parsing_leading_context = self._no_context_parsing_likelihood_calculator.likelihood(leading_word, lemma_root_str,
            lemma_root_syn_cat,
            stem_str, stem_syn_cat, surface_str, surface_syn_cat)

        likelihood_with_parsing_leading_context = self._context_parsing_likelihood_calculator.likelihood(parse_results_of_leading_word,
            lemma_root_str, lemma_root_syn_cat,
            stem_str, stem_syn_cat, surface_str, surface_syn_cat)

        return 0.2 * likelihood_without_parsing_leading_context + 0.8 * likelihood_with_parsing_leading_context


class NoContextParsingLikelihoodCalculator(object):
    def __init__(self, collection):
        self.collection = collection

    def _count_given_leading_word(self, leading_word):
        self.collection.ensure_index([
            ("item_0.word.surface.value", pymongo.ASCENDING)
        ], name="leading_surface_index", drop_dups=True)

        query_given_leading_word = WordBigramQueryBuilder().given_surface(leading_word).build()
        count_given_leading_word = float(self.collection.find(query_given_leading_word).count())
        return count_given_leading_word

    def _count_surface_given_leading_word(self, leading_word, surface_str, surface_syntactic_category):
        self.collection.ensure_index([
            ("item_0.word.surface.value", pymongo.ASCENDING),
            ("item_1.word.surface.value", pymongo.ASCENDING),
            ("item_1.word.surface.syntactic_category", pymongo.ASCENDING),
        ], name="word_surface_index", drop_dups=True)

        query_surface_given_leading_word = WordBigramQueryBuilder().surface(surface_str, surface_syntactic_category).given_surface(leading_word).build()
        count_surface_given_leading_word = float(self.collection.find(query_surface_given_leading_word).count())
        return count_surface_given_leading_word

    def _count_stem_given_leading_word(self, leading_word, stem_str, stem_syntactic_category):
        self.collection.ensure_index([
            ("item_0.word.surface.value", pymongo.ASCENDING),
            ("item_1.word.stem.value", pymongo.ASCENDING),
            ("item_1.word.stem.syntactic_category", pymongo.ASCENDING),
        ], name="word_stem_index", drop_dups=True)

        query_stem_given_leading_word = WordBigramQueryBuilder().stem(stem_str, stem_syntactic_category).given_surface(leading_word).build()
        count_stem_given_leading_word = float(self.collection.find(query_stem_given_leading_word).count())
        return count_stem_given_leading_word

    def _count_lexeme_given_leading_word(self, leading_word, lemma_root_str, lemma_root_syntactic_category):
        self.collection.ensure_index([
            ("item_0.word.surface.value", pymongo.ASCENDING),
            ("item_1.word.lemma_root.value", pymongo.ASCENDING),
            ("item_1.word.lemma_root.syntactic_category", pymongo.ASCENDING),
        ], name="word_lemma_root_index", drop_dups=True)

        query_lexeme_given_leading_word = WordBigramQueryBuilder().lemma_root(lemma_root_str, lemma_root_syntactic_category).given_surface(leading_word).build()
        count_lexeme_given_leading_word = float(self.collection.find(query_lexeme_given_leading_word).count())
        return count_lexeme_given_leading_word

    def likelihood(self, leading_word, lemma_root_str, lemma_root_syn_cat, stem_str, stem_syn_cat, surface_str, surface_syn_cat):
        count_given_leading_word = self._count_given_leading_word(leading_word)
        count_surface_given_leading_word = self._count_surface_given_leading_word(leading_word, surface_str, surface_syn_cat)
        count_stem_given_leading_word = self._count_stem_given_leading_word(leading_word, stem_str, stem_syn_cat)
        count_lexeme_given_leading_word = self._count_lexeme_given_leading_word(leading_word, lemma_root_str, lemma_root_syn_cat)

        # P(surface + surface_syn_cat | leading word)
        p_surface_given_leading_word = count_surface_given_leading_word / count_given_leading_word if count_given_leading_word else 0.0

        # P(stem + stem_syn_cat | leading word)
        p_stem_given_leading_word = count_stem_given_leading_word / count_given_leading_word if count_given_leading_word else 0.0

        # P(lexeme + lexeme_syn_cat | leading word)
        p_lexeme_given_leading_word = count_lexeme_given_leading_word / count_given_leading_word if count_given_leading_word else 0.0

        #attempt parsing the context words
        return 0.55 * p_surface_given_leading_word + 0.3 * p_stem_given_leading_word + 0.15 * p_lexeme_given_leading_word


class ContextParsingLikelihoodCalculator(object):
    def __init__(self, collection):
        self.collection = collection

    def _count_given_leading_surface(self, leading_surface_str, leading_surface_syn_cat):
        self.collection.ensure_index([
            ("item_0.word.surface.value", pymongo.ASCENDING),
            ("item_0.word.surface.syntactic_category", pymongo.ASCENDING)
        ], name="word_surface_index", drop_dups=True)

        query_given_leading_surface = WordBigramQueryBuilder().given_surface(leading_surface_str, leading_surface_syn_cat).build()
        count_given_leading_surface = float(self.collection.find(query_given_leading_surface).count())
        return count_given_leading_surface

    def _count_surface_given_leading_surface(self, leading_surface_str, leading_surface_syn_cat, surface_str, surface_syntactic_category):
        self.collection.ensure_index([
            ("item_0.word.surface.value", pymongo.ASCENDING),
            ("item_0.word.surface.syntactic_category", pymongo.ASCENDING),
            ("item_1.word.surface.value", pymongo.ASCENDING),
            ("item_1.word.surface.syntactic_category", pymongo.ASCENDING),
        ], name="surface_surface_index", drop_dups=True)

        query_surface_given_leading_surface = WordBigramQueryBuilder().surface(surface_str, surface_syntactic_category).given_surface(leading_surface_str,
            leading_surface_syn_cat).build()
        count_surface_given_leading_surface = float(self.collection.find(query_surface_given_leading_surface).count())
        return count_surface_given_leading_surface

    def _count_stem_given_leading_surface(self, leading_surface_str, leading_surface_syn_cat, stem_str, stem_syntactic_category):
        self.collection.ensure_index([
            ("item_0.word.surface.value", pymongo.ASCENDING),
            ("item_0.word.surface.syntactic_category", pymongo.ASCENDING),
            ("item_1.word.stem.value", pymongo.ASCENDING),
            ("item_1.word.stem.syntactic_category", pymongo.ASCENDING),
        ], name="surface_stem_index", drop_dups=True)

        query_stem_given_leading_surface = WordBigramQueryBuilder().stem(stem_str, stem_syntactic_category).given_surface(leading_surface_str,
            leading_surface_syn_cat).build()
        count_stem_given_leading_surface = float(self.collection.find(query_stem_given_leading_surface).count())
        return count_stem_given_leading_surface

    def _count_lexeme_given_leading_surface(self, leading_surface_str, leading_surface_syn_cat, lemma_root_str, lemma_root_syntactic_category):
        self.collection.ensure_index([
            ("item_0.word.surface.value", pymongo.ASCENDING),
            ("item_0.word.surface.syntactic_category", pymongo.ASCENDING),
            ("item_1.word.lemma_root.value", pymongo.ASCENDING),
            ("item_1.word.lemma_root.syntactic_category", pymongo.ASCENDING),
        ], name="surface_lemma_root_index", drop_dups=True)

        query_lexeme_given_leading_surface = WordBigramQueryBuilder().lemma_root(lemma_root_str, lemma_root_syntactic_category).given_surface(
            leading_surface_str, leading_surface_syn_cat).build()
        count_lexeme_given_leading_surface = float(self.collection.find(query_lexeme_given_leading_surface).count())
        return count_lexeme_given_leading_surface


    def _count_given_leading_stem(self, leading_stem_str, leading_stem_syn_cat):
        self.collection.ensure_index([
            ("item_0.word.stem.value", pymongo.ASCENDING),
            ("item_0.word.stem.syntactic_category", pymongo.ASCENDING)
        ], name="stem_surface_index", drop_dups=True)

        query_given_leading_stem = WordBigramQueryBuilder().given_stem(leading_stem_str, leading_stem_syn_cat).build()
        count_given_leading_stem = float(self.collection.find(query_given_leading_stem).count())
        return count_given_leading_stem

    def _count_surface_given_leading_stem(self, leading_stem_str, leading_stem_syn_cat, surface_str, surface_syntactic_category):
        self.collection.ensure_index([
            ("item_0.word.stem.value", pymongo.ASCENDING),
            ("item_0.word.stem.syntactic_category", pymongo.ASCENDING),
            ("item_1.word.surface.value", pymongo.ASCENDING),
            ("item_1.word.surface.syntactic_category", pymongo.ASCENDING),
        ], name="stem_surface_index", drop_dups=True)

        query_surface_given_leading_stem = WordBigramQueryBuilder().surface(surface_str, surface_syntactic_category).given_stem(leading_stem_str,
            leading_stem_syn_cat).build()
        count_surface_given_leading_stem = float(self.collection.find(query_surface_given_leading_stem).count())
        return count_surface_given_leading_stem

    def _count_stem_given_leading_stem(self, leading_stem_str, leading_stem_syn_cat, stem_str, stem_syntactic_category):
        self.collection.ensure_index([
            ("item_0.word.stem.value", pymongo.ASCENDING),
            ("item_0.word.stem.syntactic_category", pymongo.ASCENDING),
            ("item_1.word.stem.value", pymongo.ASCENDING),
            ("item_1.word.stem.syntactic_category", pymongo.ASCENDING),
        ], name="stem_stem_index", drop_dups=True)

        query_stem_given_leading_stem = WordBigramQueryBuilder().stem(stem_str, stem_syntactic_category).given_stem(leading_stem_str,
            leading_stem_syn_cat).build()
        count_stem_given_leading_stem = float(self.collection.find(query_stem_given_leading_stem).count())
        return count_stem_given_leading_stem

    def _count_lexeme_given_leading_stem(self, leading_stem_str, leading_stem_syn_cat, lemma_root_str, lemma_root_syntactic_category):
        self.collection.ensure_index([
            ("item_0.word.stem.value", pymongo.ASCENDING),
            ("item_0.word.stem.syntactic_category", pymongo.ASCENDING),
            ("item_1.word.lemma_root.value", pymongo.ASCENDING),
            ("item_1.word.lemma_root.syntactic_category", pymongo.ASCENDING),
        ], name="stem_lemma_root_index", drop_dups=True)

        query_lexeme_given_leading_stem = WordBigramQueryBuilder().lemma_root(lemma_root_str, lemma_root_syntactic_category).given_stem(leading_stem_str,
            leading_stem_syn_cat).build()
        count_lexeme_given_leading_stem = float(self.collection.find(query_lexeme_given_leading_stem).count())
        return count_lexeme_given_leading_stem


    def _count_given_leading_lexeme(self, leading_lemma_root_str, leading_lemma_root_syn_cat):
        self.collection.ensure_index([
            ("item_0.word.lemma_root.value", pymongo.ASCENDING),
            ("item_0.word.lemma_root.syntactic_category", pymongo.ASCENDING)
        ], name="lemma_root_surface_index", drop_dups=True)

        query_given_leading_lexeme = WordBigramQueryBuilder().given_lemma_root(leading_lemma_root_str, leading_lemma_root_syn_cat).build()
        count_given_leading_lexeme = float(self.collection.find(query_given_leading_lexeme).count())
        return count_given_leading_lexeme

    def _count_surface_given_leading_lexeme(self, leading_lemma_root_str, leading_lemma_root_syn_cat, surface_str, surface_syntactic_category):
        self.collection.ensure_index([
            ("item_0.word.lemma_root.value", pymongo.ASCENDING),
            ("item_0.word.lemma_root.syntactic_category", pymongo.ASCENDING),
            ("item_1.word.surface.value", pymongo.ASCENDING),
            ("item_1.word.surface.syntactic_category", pymongo.ASCENDING),
        ], name="lemma_root_surface_index", drop_dups=True)

        query_surface_given_leading_lexeme = WordBigramQueryBuilder().surface(surface_str, surface_syntactic_category).given_lemma_root(leading_lemma_root_str,
            leading_lemma_root_syn_cat).build()
        count_surface_given_leading_lexeme = float(self.collection.find(query_surface_given_leading_lexeme).count())
        return count_surface_given_leading_lexeme

    def _count_stem_given_leading_lexeme(self, leading_lemma_root_str, leading_lemma_root_syn_cat, stem_str, stem_syntactic_category):
        self.collection.ensure_index([
            ("item_0.word.lemma_root.value", pymongo.ASCENDING),
            ("item_0.word.lemma_root.syntactic_category", pymongo.ASCENDING),
            ("item_1.word.stem.value", pymongo.ASCENDING),
            ("item_1.word.stem.syntactic_category", pymongo.ASCENDING),
        ], name="lemma_root_stem_index", drop_dups=True)

        query_stem_given_leading_lexeme = WordBigramQueryBuilder().stem(stem_str, stem_syntactic_category).given_lemma_root(leading_lemma_root_str,
            leading_lemma_root_syn_cat).build()
        count_stem_given_leading_lexeme = float(self.collection.find(query_stem_given_leading_lexeme).count())
        return count_stem_given_leading_lexeme

    def _count_lexeme_given_leading_lexeme(self, leading_lemma_root_str, leading_lemma_root_syn_cat, lemma_root_str, lemma_root_syntactic_category):
        self.collection.ensure_index([
            ("item_0.word.lemma_root.value", pymongo.ASCENDING),
            ("item_0.word.lemma_root.syntactic_category", pymongo.ASCENDING),
            ("item_1.word.lemma_root.value", pymongo.ASCENDING),
            ("item_1.word.lemma_root.syntactic_category", pymongo.ASCENDING),
        ], name="lemma_root_lemma_root_index", drop_dups=True)

        query_lexeme_given_leading_lexeme = WordBigramQueryBuilder().lemma_root(lemma_root_str, lemma_root_syntactic_category).given_lemma_root(
            leading_lemma_root_str, leading_lemma_root_syn_cat).build()
        count_lexeme_given_leading_lexeme = float(self.collection.find(query_lexeme_given_leading_lexeme).count())
        return count_lexeme_given_leading_lexeme


    def _p_word_given_leading_surface(self, morpheme_container, surface_str, surface_syn_cat, stem_str, stem_syn_cat, lemma_root_str, lemma_root_syn_cat):
        leading_surface_str = morpheme_container.get_surface_so_far()
        leading_surface_syn_cat = morpheme_container.get_surface_syntactic_category()

        count_given_leading_surface = self._count_given_leading_surface(leading_surface_str, leading_surface_syn_cat)
        count_surface_given_leading_surface = self._count_surface_given_leading_surface(leading_surface_str, leading_surface_syn_cat, surface_str,
            surface_syn_cat)
        count_stem_given_leading_surface = self._count_stem_given_leading_surface(leading_surface_str, leading_surface_syn_cat, stem_str, stem_syn_cat)
        count_lexeme_given_leading_surface = self._count_lexeme_given_leading_surface(leading_surface_str, leading_surface_syn_cat, lemma_root_str,
            lemma_root_syn_cat)

        # P(surface + surface_syn_cat | leading surface + syn_cat)
        p_surface_given_leading_surface = count_surface_given_leading_surface / count_given_leading_surface if count_given_leading_surface else 0.0

        # P(stem + stem_syn_cat | leading surface + syn_cat)
        p_stem_given_leading_surface = count_stem_given_leading_surface / count_given_leading_surface if count_given_leading_surface else 0.0

        # P(lexeme + lexeme_syn_cat | leading surface + syn_cat)
        p_lexeme_given_leading_surface = count_lexeme_given_leading_surface / count_given_leading_surface if count_given_leading_surface else 0.0

        p_word_with_leading_surface = 0.55 * p_surface_given_leading_surface + 0.3 * p_stem_given_leading_surface + 0.15 * p_lexeme_given_leading_surface

        return p_word_with_leading_surface

    def _p_word_given_leading_stem(self, morpheme_container, surface_str, surface_syn_cat, stem_str, stem_syn_cat, lemma_root_str, lemma_root_syn_cat):
        leading_stem_str = morpheme_container.get_stem()
        leading_stem_syn_cat = morpheme_container.get_stem_syntactic_category()

        count_given_leading_stem = self._count_given_leading_stem(leading_stem_str, leading_stem_syn_cat)
        count_surface_given_leading_stem = self._count_surface_given_leading_stem(leading_stem_str, leading_stem_syn_cat, surface_str, surface_syn_cat)
        count_stem_given_leading_stem = self._count_stem_given_leading_stem(leading_stem_str, leading_stem_syn_cat, stem_str, stem_syn_cat)
        count_lexeme_given_leading_stem = self._count_lexeme_given_leading_stem(leading_stem_str, leading_stem_syn_cat, lemma_root_str, lemma_root_syn_cat)

        # P(surface + surface_syn_cat | leading stem + syn_cat)
        p_surface_given_leading_stem = count_surface_given_leading_stem / count_given_leading_stem if count_given_leading_stem else 0.0

        # P(stem + stem_syn_cat | leading stem + syn_cat)
        p_stem_given_leading_stem = count_stem_given_leading_stem / count_given_leading_stem if count_given_leading_stem else 0.0

        # P(lexeme + lexeme_syn_cat | leading stem + syn_cat)
        p_lexeme_given_leading_stem = count_lexeme_given_leading_stem / count_given_leading_stem if count_given_leading_stem else 0.0

        p_word_with_leading_stem = 0.55 * p_surface_given_leading_stem + 0.3 * p_stem_given_leading_stem + 0.15 * p_lexeme_given_leading_stem

        return p_word_with_leading_stem

    def _p_word_given_leading_lexeme(self, morpheme_container, surface_str, surface_syn_cat, stem_str, stem_syn_cat, lemma_root_str, lemma_root_syn_cat):
        leading_lemma_root_str = morpheme_container.get_root().lexeme.root
        leading_lemma_root_syn_cat = morpheme_container.get_root().lexeme.syntactic_category

        count_given_leading_lexeme = self._count_given_leading_lexeme(leading_lemma_root_str, leading_lemma_root_syn_cat)
        count_surface_given_leading_lexeme = self._count_surface_given_leading_lexeme(leading_lemma_root_str, leading_lemma_root_syn_cat, surface_str,
            surface_syn_cat)
        count_stem_given_leading_lexeme = self._count_stem_given_leading_lexeme(leading_lemma_root_str, leading_lemma_root_syn_cat, stem_str, stem_syn_cat)
        count_lexeme_given_leading_lexeme = self._count_lexeme_given_leading_lexeme(leading_lemma_root_str, leading_lemma_root_syn_cat, lemma_root_str,
            lemma_root_syn_cat)

        # P(surface + surface_syn_cat | leading lemma + syn_cat)
        p_surface_given_leading_lexeme = count_surface_given_leading_lexeme / count_given_leading_lexeme if count_given_leading_lexeme else 0.0

        # P(stem + stem_syn_cat | leading lemma + syn_cat)
        p_stem_given_leading_lexeme = count_stem_given_leading_lexeme / count_given_leading_lexeme if count_given_leading_lexeme else 0.0

        # P(lexeme + lexeme_syn_cat | leading lemma + syn_cat)
        p_lexeme_given_leading_lexeme = count_lexeme_given_leading_lexeme / count_given_leading_lexeme if count_given_leading_lexeme else 0.0

        p_word_with_leading_lexeme = 0.55 * p_surface_given_leading_lexeme + 0.3 * p_stem_given_leading_lexeme + 0.15 * p_lexeme_given_leading_lexeme

        return p_word_with_leading_lexeme

    def likelihood(self, parse_results_of_leading_word, lemma_root_str, lemma_root_syn_cat, stem_str, stem_syn_cat, surface_str, surface_syn_cat):
        total = 0.0

        for morpheme_container in parse_results_of_leading_word:
            p_word_given_leading_surface = self._p_word_given_leading_surface(morpheme_container, surface_str, surface_syn_cat, stem_str, stem_syn_cat,
                lemma_root_str, lemma_root_syn_cat)
            p_word_given_leading_stem = self._p_word_given_leading_stem(morpheme_container, surface_str, surface_syn_cat, stem_str, stem_syn_cat, lemma_root_str
                , lemma_root_syn_cat)
            p_word_given_leading_lexeme = self._p_word_given_leading_lexeme(morpheme_container, surface_str, surface_syn_cat, stem_str, stem_syn_cat,
                lemma_root_str, lemma_root_syn_cat)

            total += 0.55 * p_word_given_leading_surface + 0.3 * p_word_given_leading_stem + 0.15 * p_word_given_leading_lexeme

        return total / float(len(parse_results_of_leading_word))