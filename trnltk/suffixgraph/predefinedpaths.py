# coding=utf-8
from trnltk.stem.dictionaryitem import SecondaryPosition, PrimaryPosition
from trnltk.suffixgraph.stem import get_default_stem_state
from trnltk.suffixgraph.suffixapplier import *
from trnltk.suffixgraph.token import *
from trnltk.suffixgraph.suffixgraph import *

class PredefinedPaths():
    def __init__(self, stems):
        self._stems = stems
        self.token_map = None

    def _find_stem(self, stem_str, primary_position, secondary_position):
        for stem in self._stems:
            if stem.root == stem_str and stem.dictionary_item.primary_position == primary_position and stem.dictionary_item.secondary_position == secondary_position:
                return stem

        raise Exception('Unable to find stem {}+{}+{}'.format(stem_str, primary_position, secondary_position))


    def _add_transition(self, token, suffix_form_application_str, suffix, to_state, whole_word):
        suffix_form = SuffixForm(suffix_form_application_str)
        suffix_form.suffix = suffix
        new_token = try_suffix_form(token, suffix_form, to_state, whole_word)
        if not new_token:
            raise Exception('Unable to add transition {} {} {} {} {}'.format(token, suffix_form_application_str, suffix, to_state, whole_word))
        return new_token

    def _find_to_state(self, state, suffix):
        for (out_suffix, out_state) in state.outputs:
            if out_suffix == suffix:
                return out_state

        raise Exception('Unable to find output state for {} {}'.format(state, suffix))


    def _follow_path(self, stem, path_edges):
        token = ParseToken(stem, get_default_stem_state(stem), u'')
        for path_edge in path_edges:
            suffix = None
            suffix_form_application_str = None

            if isinstance(path_edge, tuple):
                suffix = path_edge[0]
                suffix_form_application_str = path_edge[1] if len(path_edge) > 1 else u''
            else:
                suffix = path_edge
                suffix_form_application_str = u''

            path_result = token.so_far + suffix_form_application_str
            to_state = self._find_to_state(token.get_last_state(), suffix)

            token = self._add_transition(token, suffix_form_application_str, suffix, to_state, path_result)

        return token

    def _add_token(self, stem, path_tuples):
        token = self._follow_path(stem, path_tuples)

        if not self.token_map.has_key(stem):
            self.token_map[stem] = []

        self.token_map[stem].append(token)

    def has_paths(self, stem):
        if not self.token_map:
            raise Exception("Predefined paths are not yet created. Maybe you forgot to run 'create_predefined_paths' ?")

        return self.token_map.has_key(stem)

    def get_paths(self, stem):
        if not self.token_map:
            raise Exception("Predefined paths are not yet created. Maybe you forgot to run 'create_predefined_paths' ?")

        return self.token_map[stem]

    def create_predefined_paths(self):
        self.token_map = {}

        self._create_predefined_path_of_ben()
        self._create_predefined_path_of_sen()
        self._create_predefined_path_of_o_pron_pers()
        self._create_predefined_path_of_biz()
        self._create_predefined_path_of_siz()
        self._create_predefined_path_of_onlar_pron_pers()

        self._create_predefined_path_of_bu_pron_demons()
        self._create_predefined_path_of_su_pron_demons()
        self._create_predefined_path_of_o_pron_demons()
        self._create_predefined_path_of_bunlar_pron_demons()
        self._create_predefined_path_of_sunlar_pron_demons()
        self._create_predefined_path_of_onlar_pron_demons()


    def _create_predefined_path_of_ben(self):
        stem_ben = self._find_stem(u'ben', PrimaryPosition.PRONOUN, SecondaryPosition.PERSONAL)
        stem_ban = self._find_stem(u'ban', PrimaryPosition.PRONOUN, SecondaryPosition.PERSONAL)

        self._add_token(stem_ben, [A1Sg_Pron, Pnon_Pron, Nom_Pron])
        self._add_token(stem_ben, [A1Sg_Pron, Pnon_Pron, (Acc_Pron, u'i')])
        self._add_token(stem_ban, [A1Sg_Pron, Pnon_Pron, (Dat_Pron, u'a')])
        self._add_token(stem_ben, [A1Sg_Pron, Pnon_Pron, (Loc_Pron, u'de')])
        self._add_token(stem_ben, [A1Sg_Pron, Pnon_Pron, (Abl_Pron, u'den')])
        self._add_token(stem_ben, [A1Sg_Pron, Pnon_Pron, (Ins_Pron, u'le')])
        self._add_token(stem_ben, [A1Sg_Pron, Pnon_Pron, (Ins_Pron, u'imle')])
        self._add_token(stem_ben, [A1Sg_Pron, Pnon_Pron, (Gen_Pron, u'im')])

        self._add_token(stem_ben, [A1Sg_Pron, Pnon_Pron, Nom_Pron_Deriv])

    def _create_predefined_path_of_sen(self):
        stem_sen = self._find_stem(u'sen', PrimaryPosition.PRONOUN, SecondaryPosition.PERSONAL)
        stem_san = self._find_stem(u'san', PrimaryPosition.PRONOUN, SecondaryPosition.PERSONAL)

        self._add_token(stem_sen, [A2Sg_Pron, Pnon_Pron, Nom_Pron])
        self._add_token(stem_sen, [A2Sg_Pron, Pnon_Pron, (Acc_Pron, u'i')])
        self._add_token(stem_san, [A2Sg_Pron, Pnon_Pron, (Dat_Pron, u'a')])
        self._add_token(stem_sen, [A2Sg_Pron, Pnon_Pron, (Loc_Pron, u'de')])
        self._add_token(stem_sen, [A2Sg_Pron, Pnon_Pron, (Abl_Pron, u'den')])
        self._add_token(stem_sen, [A2Sg_Pron, Pnon_Pron, (Ins_Pron, u'le')])
        self._add_token(stem_sen, [A2Sg_Pron, Pnon_Pron, (Ins_Pron, u'inle')])
        self._add_token(stem_sen, [A2Sg_Pron, Pnon_Pron, (Gen_Pron, u'in')])

        self._add_token(stem_sen, [A2Sg_Pron, Pnon_Pron, Nom_Pron_Deriv])

    def _create_predefined_path_of_o_pron_pers(self):
        stem_o = self._find_stem(u'o', PrimaryPosition.PRONOUN, SecondaryPosition.PERSONAL)

        self._add_token(stem_o, [A3Sg_Pron, Pnon_Pron, Nom_Pron])
        self._add_token(stem_o, [A3Sg_Pron, Pnon_Pron, (Acc_Pron, u'nu')])
        self._add_token(stem_o, [A3Sg_Pron, Pnon_Pron, (Dat_Pron, u'na')])
        self._add_token(stem_o, [A3Sg_Pron, Pnon_Pron, (Loc_Pron, u'nda')])
        self._add_token(stem_o, [A3Sg_Pron, Pnon_Pron, (Abl_Pron, u'ndan')])
        self._add_token(stem_o, [A3Sg_Pron, Pnon_Pron, (Ins_Pron, u'nla')])
        self._add_token(stem_o, [A3Sg_Pron, Pnon_Pron, (Ins_Pron, u'nunla')])
        self._add_token(stem_o, [A3Sg_Pron, Pnon_Pron, (Gen_Pron, u'nun')])

        self._add_token(stem_o, [A3Sg_Pron, Pnon_Pron, Nom_Pron_Deriv])

    def _create_predefined_path_of_biz(self):
        stem_biz = self._find_stem(u'biz', PrimaryPosition.PRONOUN, SecondaryPosition.PERSONAL)

        self._add_token(stem_biz, [A1Pl_Pron, Pnon_Pron, Nom_Pron])
        self._add_token(stem_biz, [A1Pl_Pron, Pnon_Pron, (Acc_Pron, u'i')])
        self._add_token(stem_biz, [A1Pl_Pron, Pnon_Pron, (Dat_Pron, u'e')])
        self._add_token(stem_biz, [A1Pl_Pron, Pnon_Pron, (Loc_Pron, u'de')])
        self._add_token(stem_biz, [A1Pl_Pron, Pnon_Pron, (Abl_Pron, u'den')])
        self._add_token(stem_biz, [A1Pl_Pron, Pnon_Pron, (Ins_Pron, u'le')])
        self._add_token(stem_biz, [A1Pl_Pron, Pnon_Pron, (Ins_Pron, u'imle')])
        self._add_token(stem_biz, [A1Pl_Pron, Pnon_Pron, (Gen_Pron, u'im')])

        self._add_token(stem_biz, [A1Pl_Pron, Pnon_Pron, Nom_Pron_Deriv])

        self._add_token(stem_biz, [(A1Pl_Pron, u'ler'), Pnon_Pron, Nom_Pron])
        self._add_token(stem_biz, [(A1Pl_Pron, u'ler'), Pnon_Pron, (Acc_Pron, u'i')])
        self._add_token(stem_biz, [(A1Pl_Pron, u'ler'), Pnon_Pron, (Dat_Pron, u'e')])
        self._add_token(stem_biz, [(A1Pl_Pron, u'ler'), Pnon_Pron, (Loc_Pron, u'de')])
        self._add_token(stem_biz, [(A1Pl_Pron, u'ler'), Pnon_Pron, (Abl_Pron, u'den')])
        self._add_token(stem_biz, [(A1Pl_Pron, u'ler'), Pnon_Pron, (Ins_Pron, u'le')])
        self._add_token(stem_biz, [(A1Pl_Pron, u'ler'), Pnon_Pron, (Gen_Pron, u'in')])

        self._add_token(stem_biz, [(A1Pl_Pron, u'ler'), Pnon_Pron, Nom_Pron_Deriv])

    def _create_predefined_path_of_siz(self):
        stem_siz = self._find_stem(u'siz', PrimaryPosition.PRONOUN, SecondaryPosition.PERSONAL)

        self._add_token(stem_siz, [A2Pl_Pron, Pnon_Pron, Nom_Pron])
        self._add_token(stem_siz, [A2Pl_Pron, Pnon_Pron, (Acc_Pron, u'i')])
        self._add_token(stem_siz, [A2Pl_Pron, Pnon_Pron, (Dat_Pron, u'e')])
        self._add_token(stem_siz, [A2Pl_Pron, Pnon_Pron, (Loc_Pron, u'de')])
        self._add_token(stem_siz, [A2Pl_Pron, Pnon_Pron, (Abl_Pron, u'den')])
        self._add_token(stem_siz, [A2Pl_Pron, Pnon_Pron, (Ins_Pron, u'le')])
        self._add_token(stem_siz, [A2Pl_Pron, Pnon_Pron, (Ins_Pron, u'inle')])
        self._add_token(stem_siz, [A2Pl_Pron, Pnon_Pron, (Gen_Pron, u'in')])

        self._add_token(stem_siz, [A2Pl_Pron, Pnon_Pron, Nom_Pron_Deriv])

        self._add_token(stem_siz, [(A2Pl_Pron, u'ler'), Pnon_Pron, Nom_Pron])
        self._add_token(stem_siz, [(A2Pl_Pron, u'ler'), Pnon_Pron, (Acc_Pron, u'i')])
        self._add_token(stem_siz, [(A2Pl_Pron, u'ler'), Pnon_Pron, (Dat_Pron, u'e')])
        self._add_token(stem_siz, [(A2Pl_Pron, u'ler'), Pnon_Pron, (Loc_Pron, u'de')])
        self._add_token(stem_siz, [(A2Pl_Pron, u'ler'), Pnon_Pron, (Abl_Pron, u'den')])
        self._add_token(stem_siz, [(A2Pl_Pron, u'ler'), Pnon_Pron, (Ins_Pron, u'le')])
        self._add_token(stem_siz, [(A2Pl_Pron, u'ler'), Pnon_Pron, (Gen_Pron, u'in')])

        self._add_token(stem_siz, [(A2Pl_Pron, u'ler'), Pnon_Pron, Nom_Pron_Deriv])

    def _create_predefined_path_of_onlar_pron_pers(self):
        stem_o = self._find_stem(u'o', PrimaryPosition.PRONOUN, SecondaryPosition.PERSONAL)

        self._add_token(stem_o, [(A3Pl_Pron, 'nlar'), Pnon_Pron, Nom_Pron])
        self._add_token(stem_o, [(A3Pl_Pron, 'nlar'), Pnon_Pron, (Acc_Pron, u'ı')])
        self._add_token(stem_o, [(A3Pl_Pron, 'nlar'), Pnon_Pron, (Dat_Pron, u'a')])
        self._add_token(stem_o, [(A3Pl_Pron, 'nlar'), Pnon_Pron, (Loc_Pron, u'da')])
        self._add_token(stem_o, [(A3Pl_Pron, 'nlar'), Pnon_Pron, (Abl_Pron, u'dan')])
        self._add_token(stem_o, [(A3Pl_Pron, 'nlar'), Pnon_Pron, (Ins_Pron, u'la')])
        self._add_token(stem_o, [(A3Pl_Pron, 'nlar'), Pnon_Pron, (Gen_Pron, u'ın')])

        self._add_token(stem_o, [(A3Pl_Pron, 'nlar'), Pnon_Pron, Nom_Pron_Deriv])

    def _create_predefined_path_of_bu_pron_demons(self):
        stem_bu = self._find_stem(u'bu', PrimaryPosition.PRONOUN, SecondaryPosition.DEMONSTRATIVE)

        self._add_token(stem_bu, [A3Sg_Pron, Pnon_Pron, Nom_Pron])
        self._add_token(stem_bu, [A3Sg_Pron, Pnon_Pron, (Acc_Pron, u'nu')])
        self._add_token(stem_bu, [A3Sg_Pron, Pnon_Pron, (Dat_Pron, u'na')])
        self._add_token(stem_bu, [A3Sg_Pron, Pnon_Pron, (Loc_Pron, u'nda')])
        self._add_token(stem_bu, [A3Sg_Pron, Pnon_Pron, (Abl_Pron, u'ndan')])
        self._add_token(stem_bu, [A3Sg_Pron, Pnon_Pron, (Ins_Pron, u'nla')])
        self._add_token(stem_bu, [A3Sg_Pron, Pnon_Pron, (Ins_Pron, u'nunla')])
        self._add_token(stem_bu, [A3Sg_Pron, Pnon_Pron, (Gen_Pron, u'nun')])

        self._add_token(stem_bu, [A3Sg_Pron, Pnon_Pron, Nom_Pron_Deriv])

    def _create_predefined_path_of_su_pron_demons(self):
        stem_su = self._find_stem(u'şu', PrimaryPosition.PRONOUN, SecondaryPosition.DEMONSTRATIVE)

        self._add_token(stem_su, [A3Sg_Pron, Pnon_Pron, Nom_Pron])
        self._add_token(stem_su, [A3Sg_Pron, Pnon_Pron, (Acc_Pron, u'nu')])
        self._add_token(stem_su, [A3Sg_Pron, Pnon_Pron, (Dat_Pron, u'na')])
        self._add_token(stem_su, [A3Sg_Pron, Pnon_Pron, (Loc_Pron, u'nda')])
        self._add_token(stem_su, [A3Sg_Pron, Pnon_Pron, (Abl_Pron, u'ndan')])
        self._add_token(stem_su, [A3Sg_Pron, Pnon_Pron, (Ins_Pron, u'nla')])
        self._add_token(stem_su, [A3Sg_Pron, Pnon_Pron, (Ins_Pron, u'nunla')])
        self._add_token(stem_su, [A3Sg_Pron, Pnon_Pron, (Gen_Pron, u'nun')])

        self._add_token(stem_su, [A3Sg_Pron, Pnon_Pron, Nom_Pron_Deriv])

    def _create_predefined_path_of_o_pron_demons(self):
        stem_o = self._find_stem(u'o', PrimaryPosition.PRONOUN, SecondaryPosition.DEMONSTRATIVE)

        self._add_token(stem_o, [A3Sg_Pron, Pnon_Pron, Nom_Pron])
        self._add_token(stem_o, [A3Sg_Pron, Pnon_Pron, (Acc_Pron, u'nu')])
        self._add_token(stem_o, [A3Sg_Pron, Pnon_Pron, (Dat_Pron, u'na')])
        self._add_token(stem_o, [A3Sg_Pron, Pnon_Pron, (Loc_Pron, u'nda')])
        self._add_token(stem_o, [A3Sg_Pron, Pnon_Pron, (Abl_Pron, u'ndan')])
        self._add_token(stem_o, [A3Sg_Pron, Pnon_Pron, (Ins_Pron, u'nla')])
        self._add_token(stem_o, [A3Sg_Pron, Pnon_Pron, (Ins_Pron, u'nunla')])
        self._add_token(stem_o, [A3Sg_Pron, Pnon_Pron, (Gen_Pron, u'nun')])

        self._add_token(stem_o, [A3Sg_Pron, Pnon_Pron, Nom_Pron_Deriv])

    def _create_predefined_path_of_bunlar_pron_demons(self):
        stem_bu = self._find_stem(u'bu', PrimaryPosition.PRONOUN, SecondaryPosition.DEMONSTRATIVE)

        self._add_token(stem_bu, [(A3Pl_Pron, 'nlar'), Pnon_Pron, Nom_Pron])
        self._add_token(stem_bu, [(A3Pl_Pron, 'nlar'), Pnon_Pron, (Acc_Pron, u'ı')])
        self._add_token(stem_bu, [(A3Pl_Pron, 'nlar'), Pnon_Pron, (Dat_Pron, u'a')])
        self._add_token(stem_bu, [(A3Pl_Pron, 'nlar'), Pnon_Pron, (Loc_Pron, u'da')])
        self._add_token(stem_bu, [(A3Pl_Pron, 'nlar'), Pnon_Pron, (Abl_Pron, u'dan')])
        self._add_token(stem_bu, [(A3Pl_Pron, 'nlar'), Pnon_Pron, (Ins_Pron, u'la')])
        self._add_token(stem_bu, [(A3Pl_Pron, 'nlar'), Pnon_Pron, (Gen_Pron, u'ın')])

        self._add_token(stem_bu, [(A3Pl_Pron, 'nlar'), Pnon_Pron, Nom_Pron_Deriv])

    def _create_predefined_path_of_sunlar_pron_demons(self):
        stem_su = self._find_stem(u'şu', PrimaryPosition.PRONOUN, SecondaryPosition.DEMONSTRATIVE)

        self._add_token(stem_su, [(A3Pl_Pron, 'nlar'), Pnon_Pron, Nom_Pron])
        self._add_token(stem_su, [(A3Pl_Pron, 'nlar'), Pnon_Pron, (Acc_Pron, u'ı')])
        self._add_token(stem_su, [(A3Pl_Pron, 'nlar'), Pnon_Pron, (Dat_Pron, u'a')])
        self._add_token(stem_su, [(A3Pl_Pron, 'nlar'), Pnon_Pron, (Loc_Pron, u'da')])
        self._add_token(stem_su, [(A3Pl_Pron, 'nlar'), Pnon_Pron, (Abl_Pron, u'dan')])
        self._add_token(stem_su, [(A3Pl_Pron, 'nlar'), Pnon_Pron, (Ins_Pron, u'la')])
        self._add_token(stem_su, [(A3Pl_Pron, 'nlar'), Pnon_Pron, (Gen_Pron, u'ın')])

        self._add_token(stem_su, [(A3Pl_Pron, 'nlar'), Pnon_Pron, Nom_Pron_Deriv])

    def _create_predefined_path_of_onlar_pron_demons(self):
        stem_o = self._find_stem(u'o', PrimaryPosition.PRONOUN, SecondaryPosition.DEMONSTRATIVE)

        self._add_token(stem_o, [(A3Pl_Pron, 'nlar'), Pnon_Pron, Nom_Pron])
        self._add_token(stem_o, [(A3Pl_Pron, 'nlar'), Pnon_Pron, (Acc_Pron, u'ı')])
        self._add_token(stem_o, [(A3Pl_Pron, 'nlar'), Pnon_Pron, (Dat_Pron, u'a')])
        self._add_token(stem_o, [(A3Pl_Pron, 'nlar'), Pnon_Pron, (Loc_Pron, u'da')])
        self._add_token(stem_o, [(A3Pl_Pron, 'nlar'), Pnon_Pron, (Abl_Pron, u'dan')])
        self._add_token(stem_o, [(A3Pl_Pron, 'nlar'), Pnon_Pron, (Ins_Pron, u'la')])
        self._add_token(stem_o, [(A3Pl_Pron, 'nlar'), Pnon_Pron, (Gen_Pron, u'ın')])

        self._add_token(stem_o, [(A3Pl_Pron, 'nlar'), Pnon_Pron, Nom_Pron_Deriv])