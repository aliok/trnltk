from trnltk.stem.dictionaryitem import PrimaryPosition, SecondaryPosition
from trnltk.stem.stemgenerator import CircumflexConvertingStemGenerator
from trnltk.suffixgraph.suffixgraphmodel import FreeTransitionSuffix

def format_parse_token_as_parseset_format(result):
    """
    @return kitap+Noun+A3sg+Pnon+Acc for word 'kitaba'
    """
    root = result.get_stem().dictionary_item.root
    secondary_position_str = result.get_stem().dictionary_item.secondary_position

#    ##TODO: skip some secondary positions for now...
    if result.get_stem().dictionary_item.primary_position == PrimaryPosition.NOUN:
        if result.get_stem().dictionary_item.secondary_position == SecondaryPosition.TIME:
            secondary_position_str = None
    elif result.get_stem().dictionary_item.primary_position == PrimaryPosition.ADVERB:
        if result.get_stem().dictionary_item.secondary_position == SecondaryPosition.QUESTION:
            secondary_position_str = None
        elif result.get_stem().dictionary_item.secondary_position == SecondaryPosition.TIME:
            secondary_position_str = None
    elif result.get_stem().dictionary_item.primary_position == PrimaryPosition.ADJECTIVE:
        if result.get_stem().dictionary_item.secondary_position == SecondaryPosition.QUESTION:
            secondary_position_str = None

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
        if not secondary_position_str:
            return u'({},"{}+{}")'.format(1, root, result.get_stem_state().pretty_name)
        else:
            return u'({},"{}+{}+{}")'.format(1, root, result.get_stem_state().pretty_name, secondary_position_str)

    return_value = None

    if not secondary_position_str:
        return_value = u'({},"{}+{}")'.format(1, root, result.get_stem_state().pretty_name)
    else:
        return_value = u'({},"{}+{}+{}")'.format(1, root, result.get_stem_state().pretty_name, secondary_position_str)

    if not groups[0]:
        if not secondary_position_str:
            return_value = u'({},"{}+{}")'.format(1, root, result.get_stem_state().pretty_name)
        else:
            return_value = u'({},"{}+{}+{}")'.format(1, root, result.get_stem_state().pretty_name, secondary_position_str)
    else:
        if not secondary_position_str:
            return_value = u'({},"{}+{}+{}")'.format(1, root, result.get_stem_state().pretty_name, u'+'.join(groups[0]))
        else:
            return_value = u'({},"{}+{}+{}+{}")'.format(1, root, result.get_stem_state().pretty_name, secondary_position_str, u'+'.join(groups[0]))

    for i in range(1, len(groups)):
        group = groups[i]
        return_value += u'({},"{}")'.format(i + 1, u'+'.join(group))

    ##TODO:
    if any(c in CircumflexConvertingStemGenerator.Circumflex_Chars for c in return_value):
        for (cir, pla) in CircumflexConvertingStemGenerator.Circumflex_Letters_Map.iteritems():
            return_value = return_value.replace(cir, pla)

    ##TODO:
    if u'+Apos' in return_value:
        return_value = return_value.replace(u'+Apos', u'')

    return return_value