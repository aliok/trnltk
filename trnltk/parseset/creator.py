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
from trnltk.morphology.model import formatter
from trnltk.morphology.phonetics.alphabet import TurkishAlphabet
from trnltk.parseset.xmlbindings import *
from trnltk.morphology.model.morpheme import FreeTransitionSuffix

class ParseSetCreator(object):
    def create_word_binding_from_morpheme_container(self, word_str, morpheme_container):
        assert (word_str == morpheme_container.get_surface_so_far()) or (TurkishAlphabet.lower(word_str[0])+word_str[1:] == morpheme_container.get_surface_so_far())

        root_str = morpheme_container.get_root().str
        lemma = morpheme_container.get_root().lexeme.lemma
        lemma_root = morpheme_container.get_root().lexeme.root
        root_syntactic_category = morpheme_container.get_root().lexeme.syntactic_category
        root_secondary_syntactic_category = morpheme_container.get_root().lexeme.secondary_syntactic_category
        root = RootBinding(root_str, lemma, lemma_root, root_syntactic_category, root_secondary_syntactic_category)

        word_syntactic_category = morpheme_container.get_surface_syntactic_category()
        word_secondary_syntactic_category = morpheme_container.get_surface_secondary_syntactic_category()

        parse_result = formatter.format_morpheme_container_for_parseset(morpheme_container)
        word = WordBinding(word_str, parse_result, root, word_syntactic_category, word_secondary_syntactic_category)

        if morpheme_container.get_transitions():
            so_far = root_str
            for transition in morpheme_container.get_transitions():
                if isinstance(transition.suffix_form_application.suffix_form.suffix, FreeTransitionSuffix):
                    continue

                suffix_name = transition.suffix_form_application.suffix_form.suffix.name
                suffix_pretty_name = transition.suffix_form_application.suffix_form.suffix.pretty_name
                suffix_form = transition.suffix_form_application.suffix_form.form
                suffix_application = transition.suffix_form_application.fitting_suffix_form
                suffix_actual_application = transition.suffix_form_application.actual_suffix_form
                word_with_suffix_application = None
                if (so_far + suffix_actual_application)==root_str:
                    word_with_suffix_application = morpheme_container.get_root().lexeme.root + suffix_application
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

    def create_sentence_binding_from_morpheme_containers(self, morpheme_containers):
        sentence = SentenceBinding()

        for (word_str, morpheme_container) in morpheme_containers:
            if not morpheme_container:
                sentence.words.append(UnparsableWordBinding(word_str))
            else:
                if morpheme_container.get_remaining_surface():
                    raise Exception(u'Morpheme container is not in terminal state : {}'.format(morpheme_container))

                word = self.create_word_binding_from_morpheme_container(word_str, morpheme_container)
                sentence.words.append(word)

        return sentence