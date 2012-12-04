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
from trnltk.morphology.model.lexeme import SyntacticCategory, SecondarySyntacticCategory
from trnltk.morphology.lexicon.rootgenerator import CircumflexConvertingRootGenerator
from trnltk.morphology.model.morpheme import FreeTransitionSuffix

def format_morpheme_container_for_parseset(result, add_space=False):
    """
    @return kitap+Noun+A3sg+Pnon+Dat for word 'kitaba'
    """
    returnValue = u'{}+{}'.format(result.get_root().lexeme.root, result.get_root_state().pretty_name)
    if result.get_root().lexeme.secondary_syntactic_category:
        returnValue += u'+{}'.format(result.get_root().lexeme.secondary_syntactic_category)

    if result.has_transitions():
        non_free_transitions = filter(lambda t: not isinstance(t.suffix_form_application.suffix_form.suffix, FreeTransitionSuffix), result.get_transitions())
        if non_free_transitions:
            if add_space:
                returnValue = returnValue + u' + ' + u' + '.join([format_transition(t, False) for t in non_free_transitions])
            else:
                returnValue = returnValue + u'+' + u'+'.join([format_transition(t, False) for t in non_free_transitions])

    return returnValue

def format_morpheme_container_for_tests(result):
    """
    @return kitab(kitap)+Noun+A3sg+Pnon+Dat(+yA[a]) for word 'kitaba'
    """
    returnValue = u'{}({})+{}'.format(result.get_root().str, result.get_root().lexeme.lemma, result.get_root_state().pretty_name)
    if result.get_root().lexeme.secondary_syntactic_category:
        returnValue += u'+{}'.format(result.get_root().lexeme.secondary_syntactic_category)

    if result.has_transitions():
        non_free_transitions = filter(lambda t: not isinstance(t.suffix_form_application.suffix_form.suffix, FreeTransitionSuffix), result.get_transitions())
        if non_free_transitions:
            returnValue = returnValue + u'+' + u'+'.join([format_transition(t, True) for t in non_free_transitions])

    return returnValue

def format_transition(transition, includeForm=True):
    returnVal = u''
    if transition.is_derivational():
        returnVal = transition.to_state.pretty_name + '+'

    if includeForm and transition.suffix_form_application.actual_suffix_form and transition.suffix_form_application.actual_suffix_form.isalnum():
        returnVal += u'{}({}[{}])'.format(transition.suffix_form_application.suffix_form.suffix.pretty_name,
            transition.suffix_form_application.suffix_form.form, transition.suffix_form_application.actual_suffix_form)
    else:
        returnVal += u'{}'.format(transition.suffix_form_application.suffix_form.suffix.pretty_name)

    return returnVal

def format_morpheme_container_for_simple_parseset(result):
    """
    @return (1,"kitap+Noun+A3sg+Pnon+Dat") for word 'kitaba'
    """
    root = result.get_root().lexeme.root
    secondary_syntactic_category_str = result.get_root().lexeme.secondary_syntactic_category

    #    ##TODO: skip some secondary categories for now...
#    if result.get_root().lexeme.syntactic_category == SyntacticCategory.NOUN:
#        if result.get_root().lexeme.secondary_syntactic_category == SecondarySyntacticCategory.TIME:
#            secondary_syntactic_category_str = None
#    elif result.get_root().lexeme.syntactic_category == SyntacticCategory.ADVERB:
    if result.get_root().lexeme.syntactic_category == SyntacticCategory.ADVERB:
        if result.get_root().lexeme.secondary_syntactic_category == SecondarySyntacticCategory.QUESTION:
            secondary_syntactic_category_str = None
        elif result.get_root().lexeme.secondary_syntactic_category == SecondarySyntacticCategory.TIME:
            secondary_syntactic_category_str = None
    elif result.get_root().lexeme.syntactic_category == SyntacticCategory.ADJECTIVE:
        if result.get_root().lexeme.secondary_syntactic_category == SecondarySyntacticCategory.QUESTION:
            secondary_syntactic_category_str = None

    groups = []
    current_group = []
    for transition in result.get_transitions():
        if transition.is_derivational():
            groups.append(current_group)
            current_group = [transition.to_state.pretty_name]
        else:
            pass

        if isinstance(transition.suffix_form_application.suffix_form.suffix, FreeTransitionSuffix):
            continue
        else:
            current_group.append(transition.suffix_form_application.suffix_form.suffix.pretty_name)

    groups.append(current_group)

    if not groups:
        if not secondary_syntactic_category_str:
            return u'({},"{}+{}")'.format(1, root, result.get_root_state().pretty_name)
        else:
            return u'({},"{}+{}+{}")'.format(1, root, result.get_root_state().pretty_name, secondary_syntactic_category_str)

    return_value = None

    if not secondary_syntactic_category_str:
        return_value = u'({},"{}+{}")'.format(1, root, result.get_root_state().pretty_name)
    else:
        return_value = u'({},"{}+{}+{}")'.format(1, root, result.get_root_state().pretty_name, secondary_syntactic_category_str)

    if not groups[0]:
        if not secondary_syntactic_category_str:
            return_value = u'({},"{}+{}")'.format(1, root, result.get_root_state().pretty_name)
        else:
            return_value = u'({},"{}+{}+{}")'.format(1, root, result.get_root_state().pretty_name, secondary_syntactic_category_str)
    else:
        if not secondary_syntactic_category_str:
            return_value = u'({},"{}+{}+{}")'.format(1, root, result.get_root_state().pretty_name, u'+'.join(groups[0]))
        else:
            return_value = u'({},"{}+{}+{}+{}")'.format(1, root, result.get_root_state().pretty_name, secondary_syntactic_category_str, u'+'.join(groups[0]))

    for i in range(1, len(groups)):
        group = groups[i]
        return_value += u'({},"{}")'.format(i + 1, u'+'.join(group))

    ##TODO:
    if any(c in CircumflexConvertingRootGenerator.Circumflex_Chars for c in return_value):
        for (cir, pla) in CircumflexConvertingRootGenerator.Circumflex_Letters_Map.iteritems():
            return_value = return_value.replace(cir, pla)

    ##TODO:
    if u'+Apos' in return_value:
        return_value = return_value.replace(u'+Apos', u'')

    return return_value


def format_morpheme_container_for_simple_parseset_without_suffixes(result):
    """
    @type result MorphemeContainer
    @return "kitaplasti+Verb[kitaplas(kitap+Noun)+Verb]" for word 'kitaplasti'
    """

    return u"{}+{}[{}({}+{})+{}]".format(result.get_surface(), result.get_surface_syntactic_category(), result.get_stem(), result.get_stem_syntactic_category(), result.get_lemma_root(), result.get_lemma_root_syntactic_category())