from trnltk.stem.dictionaryitem import PrimaryPosition
from trnltk.suffixgraph.suffixgraph import *

def get_default_stem_state(stem):
    if not stem.dictionary_item.primary_position or stem.dictionary_item.primary_position==PrimaryPosition.NOUN:
        return NOUN_ROOT
    elif stem.dictionary_item.primary_position==PrimaryPosition.VERB:
        return VERB_ROOT
    elif stem.dictionary_item.primary_position==PrimaryPosition.ADVERB:
        return ADVERB_ROOT
    elif stem.dictionary_item.primary_position==PrimaryPosition.ADJECTIVE:
        return ADJECTIVE_ROOT
    elif stem.dictionary_item.primary_position==PrimaryPosition.PRONOUN:
        return PRONOUN_ROOT
    elif stem.dictionary_item.primary_position==PrimaryPosition.DETERMINER:
        return DETERMINER_ROOT_TERMINAL
    elif stem.dictionary_item.primary_position==PrimaryPosition.INTERJECTION:
        return INTERJECTION_ROOT_TERMINAL
    elif stem.dictionary_item.primary_position==PrimaryPosition.CONJUNCTION:
        return CONJUNCTION_ROOT_TERMINAL
    elif stem.dictionary_item.primary_position==PrimaryPosition.NUMERAL:
        return NUMERAL_ROOT
    elif stem.dictionary_item.primary_position==PrimaryPosition.PUNCTUATION:
        return PUNC_ROOT_TERMINAL
    else:
        raise Exception("No stem state found!")