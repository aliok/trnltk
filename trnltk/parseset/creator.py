from trnltk.parser import formatter
from trnltk.parseset.xmlbindings import *
from trnltk.suffixgraph.suffixgraphmodel import FreeTransitionSuffix

class ParseSetCreator(object):
    def create_word_binding_from_token(self, word_str, token):
        assert word_str == token.get_so_far()

        root = token.get_stem().root
        lemma = token.get_stem().dictionary_item.lemma
        lemma_root = token.get_stem().dictionary_item.root
        stem_syntactic_category = token.get_stem().dictionary_item.syntactic_category
        stem_secondary_syntactic_category = token.get_stem().dictionary_item.secondary_syntactic_category
        stem = StemBinding(root, lemma, lemma_root, stem_syntactic_category, stem_secondary_syntactic_category)

        word_syntactic_category = stem_syntactic_category
        word_secondary_syntactic_category = stem_secondary_syntactic_category

        if token.has_transitions():
            last_derivation_transition = token.get_last_derivation_transition()
            if last_derivation_transition:
                word_syntactic_category = last_derivation_transition.to_state.syntactic_category
                word_secondary_syntactic_category = None

        word_str = token.get_so_far()
        parse_result = formatter.format_parse_token_for_parseset(token)
        word = WordBinding(word_str, parse_result, stem, word_syntactic_category, word_secondary_syntactic_category)

        if token.get_transitions():
            so_far = root
            for transition in token.get_transitions():
                if isinstance(transition.suffix_form_application.suffix_form.suffix, FreeTransitionSuffix):
                    continue

                suffix_name = transition.suffix_form_application.suffix_form.suffix.name
                suffix_pretty_name = transition.suffix_form_application.suffix_form.suffix.pretty_name
                suffix_form = transition.suffix_form_application.suffix_form.form
                suffix_application = transition.suffix_form_application.fitting_suffix_form
                suffix_actual_application = transition.suffix_form_application.actual_suffix_form
                word_with_suffix_application = None
                if (so_far + suffix_actual_application)==root:
                    word_with_suffix_application = token.get_stem().dictionary_item.root + suffix_application
                else:
                    word_with_suffix_application = so_far + suffix_application
                so_far += suffix_actual_application
                if transition.is_derivational():
                    suffix = DerivationalSuffixBinding(suffix_name, suffix_pretty_name, suffix_form, suffix_application, suffix_actual_application, word_with_suffix_application, so_far, transition.to_state.syntactic_category)
                    word.suffixes.append(suffix)
                else:
                    suffix = InflectionalSuffixBinding(suffix_name, suffix_pretty_name, suffix_form, suffix_application, suffix_actual_application, word_with_suffix_application, so_far, transition.to_state.syntactic_category)
                    word.suffixes.append(suffix)
        return word

    def create_sentence_binding_from_tokens(self, tokens):
        sentence = SentenceBinding()

        for (word_str, token) in tokens:
            if not token:
                sentence.words.append(UnparsableWordBinding(word_str))
            else:
                if token.get_remaining():
                    raise Exception(u'Token is not terminal : {}'.format(token))

                word = self.create_word_binding_from_token(word_str, token)
                sentence.words.append(word)

        return sentence