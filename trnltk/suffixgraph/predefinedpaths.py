# coding=utf-8
from trnltk.stem.dictionaryitem import SecondarySyntacticCategory, SyntacticCategory
from trnltk.parser.suffixapplier import *
from trnltk.parser.token import *
from trnltk.suffixgraph.suffixgraph import *

class PredefinedPaths(object):
    def __init__(self, stem_root_map, suffix_graph):
        self._stem_root_map = stem_root_map
        self.suffix_graph = suffix_graph
        self.token_map = {}

    def _find_stem(self, stem_str, syntactic_category, secondary_syntactic_category):
        if self._stem_root_map.has_key(stem_str):
            stems_for_stem_str = self._stem_root_map[stem_str]
            for stem in stems_for_stem_str:
                if stem.dictionary_item.syntactic_category == syntactic_category and stem.dictionary_item.secondary_syntactic_category == secondary_syntactic_category:
                    return stem

        raise Exception(u'Unable to find _stem {}+{}+{}'.format(stem_str, syntactic_category, secondary_syntactic_category))


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

        raise Exception(u'Unable to find output state for {} {}'.format(state, suffix))


    def _follow_path(self, stem, path_edges):
        token = ParseToken(stem, self.suffix_graph.get_default_stem_state(stem), u'')
        for path_edge in path_edges:
            suffix = None
            suffix_form_application_str = None

            if isinstance(path_edge, tuple):
                suffix = path_edge[0]
                suffix_form_application_str = path_edge[1] if len(path_edge) > 1 else u''
            else:
                suffix = path_edge
                suffix_form_application_str = u''

            path_result = token.get_so_far() + suffix_form_application_str
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
            raise Exception(u"Predefined paths are not yet created. Maybe you forgot to run 'create_predefined_paths' ?")

        return self.token_map.has_key(stem)

    def get_paths(self, stem):
        if not self.token_map:
            raise Exception("Predefined paths are not yet created. Maybe you forgot to run 'create_predefined_paths' ?")

        return self.token_map[stem]

    def create_predefined_paths(self):
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

        self._create_predefined_path_of_kendi()
        self._create_predefined_path_of_hepsi()

        self._create_predefined_path_of_question_particles()

        self._create_predefined_path_of_ora()

    def _create_predefined_path_of_ben(self):
        stem_ben = self._find_stem(u'ben', SyntacticCategory.PRONOUN, SecondarySyntacticCategory.PERSONAL)
        stem_ban = self._find_stem(u'ban', SyntacticCategory.PRONOUN, SecondarySyntacticCategory.PERSONAL)

        self._add_token(stem_ben, [self.suffix_graph.A1Sg_Pron, self.suffix_graph.Pnon_Pron,  self.suffix_graph.Nom_Pron])
        self._add_token(stem_ben, [self.suffix_graph.A1Sg_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Acc_Pron,    u'i')])
        self._add_token(stem_ban, [self.suffix_graph.A1Sg_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Dat_Pron,    u'a')])
        self._add_token(stem_ben, [self.suffix_graph.A1Sg_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Loc_Pron,    u'de')])
        self._add_token(stem_ben, [self.suffix_graph.A1Sg_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Abl_Pron,    u'den')])
        self._add_token(stem_ben, [self.suffix_graph.A1Sg_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Ins_Pron,    u'le')])
        self._add_token(stem_ben, [self.suffix_graph.A1Sg_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Ins_Pron,    u'imle')])
        self._add_token(stem_ben, [self.suffix_graph.A1Sg_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Gen_Pron,    u'im')])
        self._add_token(stem_ben, [self.suffix_graph.A1Sg_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.AccordingTo, u'ce')])

        self._add_token(stem_ben, [self.suffix_graph.A1Sg_Pron, self.suffix_graph.Pnon_Pron, self.suffix_graph.Nom_Pron_Deriv])

    def _create_predefined_path_of_sen(self):
        stem_sen = self._find_stem(u'sen', SyntacticCategory.PRONOUN, SecondarySyntacticCategory.PERSONAL)
        stem_san = self._find_stem(u'san', SyntacticCategory.PRONOUN, SecondarySyntacticCategory.PERSONAL)

        self._add_token(stem_sen, [self.suffix_graph.A2Sg_Pron, self.suffix_graph.Pnon_Pron,  self.suffix_graph.Nom_Pron])
        self._add_token(stem_sen, [self.suffix_graph.A2Sg_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Acc_Pron,    u'i')])
        self._add_token(stem_san, [self.suffix_graph.A2Sg_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Dat_Pron,    u'a')])
        self._add_token(stem_sen, [self.suffix_graph.A2Sg_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Loc_Pron,    u'de')])
        self._add_token(stem_sen, [self.suffix_graph.A2Sg_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Abl_Pron,    u'den')])
        self._add_token(stem_sen, [self.suffix_graph.A2Sg_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Ins_Pron,    u'le')])
        self._add_token(stem_sen, [self.suffix_graph.A2Sg_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Ins_Pron,    u'inle')])
        self._add_token(stem_sen, [self.suffix_graph.A2Sg_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Gen_Pron,    u'in')])
        self._add_token(stem_sen, [self.suffix_graph.A2Sg_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.AccordingTo, u'ce')])

        self._add_token(stem_sen, [self.suffix_graph.A2Sg_Pron, self.suffix_graph.Pnon_Pron, self.suffix_graph.Nom_Pron_Deriv])

    def _create_predefined_path_of_o_pron_pers(self):
        stem_o = self._find_stem(u'o', SyntacticCategory.PRONOUN, SecondarySyntacticCategory.PERSONAL)

        self._add_token(stem_o, [self.suffix_graph.A3Sg_Pron, self.suffix_graph.Pnon_Pron,  self.suffix_graph.Nom_Pron])
        self._add_token(stem_o, [self.suffix_graph.A3Sg_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Acc_Pron,    u'nu')])
        self._add_token(stem_o, [self.suffix_graph.A3Sg_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Dat_Pron,    u'na')])
        self._add_token(stem_o, [self.suffix_graph.A3Sg_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Loc_Pron,    u'nda')])
        self._add_token(stem_o, [self.suffix_graph.A3Sg_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Abl_Pron,    u'ndan')])
        self._add_token(stem_o, [self.suffix_graph.A3Sg_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Ins_Pron,    u'nla')])
        self._add_token(stem_o, [self.suffix_graph.A3Sg_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Ins_Pron,    u'nunla')])
        self._add_token(stem_o, [self.suffix_graph.A3Sg_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Gen_Pron,    u'nun')])
        self._add_token(stem_o, [self.suffix_graph.A3Sg_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.AccordingTo, u'nca')])

        self._add_token(stem_o, [self.suffix_graph.A3Sg_Pron, self.suffix_graph.Pnon_Pron,  self.suffix_graph.Nom_Pron_Deriv])

    def _create_predefined_path_of_biz(self):
        stem_biz = self._find_stem(u'biz', SyntacticCategory.PRONOUN, SecondarySyntacticCategory.PERSONAL)

        self._add_token(stem_biz, [self.suffix_graph.A1Pl_Pron, self.suffix_graph.Pnon_Pron,  self.suffix_graph.Nom_Pron])
        self._add_token(stem_biz, [self.suffix_graph.A1Pl_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Acc_Pron,    u'i')])
        self._add_token(stem_biz, [self.suffix_graph.A1Pl_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Dat_Pron,    u'e')])
        self._add_token(stem_biz, [self.suffix_graph.A1Pl_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Loc_Pron,    u'de')])
        self._add_token(stem_biz, [self.suffix_graph.A1Pl_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Abl_Pron,    u'den')])
        self._add_token(stem_biz, [self.suffix_graph.A1Pl_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Ins_Pron,    u'le')])
        self._add_token(stem_biz, [self.suffix_graph.A1Pl_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Ins_Pron,    u'imle')])
        self._add_token(stem_biz, [self.suffix_graph.A1Pl_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Gen_Pron,    u'im')])
        self._add_token(stem_biz, [self.suffix_graph.A1Pl_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.AccordingTo, u'ce')])

        self._add_token(stem_biz, [self.suffix_graph.A1Pl_Pron, self.suffix_graph.Pnon_Pron, self.suffix_graph.Nom_Pron_Deriv])

        self._add_token(stem_biz, [(self.suffix_graph.A1Pl_Pron, u'ler'), self.suffix_graph.Pnon_Pron,  self.suffix_graph.Nom_Pron])
        self._add_token(stem_biz, [(self.suffix_graph.A1Pl_Pron, u'ler'), self.suffix_graph.Pnon_Pron, (self.suffix_graph.Acc_Pron,    u'i')])
        self._add_token(stem_biz, [(self.suffix_graph.A1Pl_Pron, u'ler'), self.suffix_graph.Pnon_Pron, (self.suffix_graph.Dat_Pron,    u'e')])
        self._add_token(stem_biz, [(self.suffix_graph.A1Pl_Pron, u'ler'), self.suffix_graph.Pnon_Pron, (self.suffix_graph.Loc_Pron,    u'de')])
        self._add_token(stem_biz, [(self.suffix_graph.A1Pl_Pron, u'ler'), self.suffix_graph.Pnon_Pron, (self.suffix_graph.Abl_Pron,    u'den')])
        self._add_token(stem_biz, [(self.suffix_graph.A1Pl_Pron, u'ler'), self.suffix_graph.Pnon_Pron, (self.suffix_graph.Ins_Pron,    u'le')])
        self._add_token(stem_biz, [(self.suffix_graph.A1Pl_Pron, u'ler'), self.suffix_graph.Pnon_Pron, (self.suffix_graph.Gen_Pron,    u'in')])
        self._add_token(stem_biz, [(self.suffix_graph.A1Pl_Pron, u'ler'), self.suffix_graph.Pnon_Pron, (self.suffix_graph.AccordingTo, u'ce')])

        self._add_token(stem_biz, [(self.suffix_graph.A1Pl_Pron, u'ler'), self.suffix_graph.Pnon_Pron, self.suffix_graph.Nom_Pron_Deriv])

    def _create_predefined_path_of_siz(self):
        stem_siz = self._find_stem(u'siz', SyntacticCategory.PRONOUN, SecondarySyntacticCategory.PERSONAL)

        self._add_token(stem_siz, [self.suffix_graph.A2Pl_Pron, self.suffix_graph.Pnon_Pron,  self.suffix_graph.Nom_Pron])
        self._add_token(stem_siz, [self.suffix_graph.A2Pl_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Acc_Pron,    u'i')])
        self._add_token(stem_siz, [self.suffix_graph.A2Pl_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Dat_Pron,    u'e')])
        self._add_token(stem_siz, [self.suffix_graph.A2Pl_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Loc_Pron,    u'de')])
        self._add_token(stem_siz, [self.suffix_graph.A2Pl_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Abl_Pron,    u'den')])
        self._add_token(stem_siz, [self.suffix_graph.A2Pl_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Ins_Pron,    u'le')])
        self._add_token(stem_siz, [self.suffix_graph.A2Pl_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Ins_Pron,    u'inle')])
        self._add_token(stem_siz, [self.suffix_graph.A2Pl_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Gen_Pron,    u'in')])
        self._add_token(stem_siz, [self.suffix_graph.A2Pl_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.AccordingTo, u'ce')])

        self._add_token(stem_siz, [self.suffix_graph.A2Pl_Pron, self.suffix_graph.Pnon_Pron, self.suffix_graph.Nom_Pron_Deriv])

        self._add_token(stem_siz, [(self.suffix_graph.A2Pl_Pron, u'ler'), self.suffix_graph.Pnon_Pron,  self.suffix_graph.Nom_Pron])
        self._add_token(stem_siz, [(self.suffix_graph.A2Pl_Pron, u'ler'), self.suffix_graph.Pnon_Pron, (self.suffix_graph.Acc_Pron,    u'i')])
        self._add_token(stem_siz, [(self.suffix_graph.A2Pl_Pron, u'ler'), self.suffix_graph.Pnon_Pron, (self.suffix_graph.Dat_Pron,    u'e')])
        self._add_token(stem_siz, [(self.suffix_graph.A2Pl_Pron, u'ler'), self.suffix_graph.Pnon_Pron, (self.suffix_graph.Loc_Pron,    u'de')])
        self._add_token(stem_siz, [(self.suffix_graph.A2Pl_Pron, u'ler'), self.suffix_graph.Pnon_Pron, (self.suffix_graph.Abl_Pron,    u'den')])
        self._add_token(stem_siz, [(self.suffix_graph.A2Pl_Pron, u'ler'), self.suffix_graph.Pnon_Pron, (self.suffix_graph.Ins_Pron,    u'le')])
        self._add_token(stem_siz, [(self.suffix_graph.A2Pl_Pron, u'ler'), self.suffix_graph.Pnon_Pron, (self.suffix_graph.Gen_Pron,    u'in')])
        self._add_token(stem_siz, [(self.suffix_graph.A2Pl_Pron, u'ler'), self.suffix_graph.Pnon_Pron, (self.suffix_graph.AccordingTo, u'ce')])

        self._add_token(stem_siz, [(self.suffix_graph.A2Pl_Pron, u'ler'), self.suffix_graph.Pnon_Pron, self.suffix_graph.Nom_Pron_Deriv])

    def _create_predefined_path_of_onlar_pron_pers(self):
        stem_o = self._find_stem(u'o', SyntacticCategory.PRONOUN, SecondarySyntacticCategory.PERSONAL)

        self._add_token(stem_o, [(self.suffix_graph.A3Pl_Pron, 'nlar'), self.suffix_graph.Pnon_Pron,  self.suffix_graph.Nom_Pron])
        self._add_token(stem_o, [(self.suffix_graph.A3Pl_Pron, 'nlar'), self.suffix_graph.Pnon_Pron, (self.suffix_graph.Acc_Pron,    u'ı')])
        self._add_token(stem_o, [(self.suffix_graph.A3Pl_Pron, 'nlar'), self.suffix_graph.Pnon_Pron, (self.suffix_graph.Dat_Pron,    u'a')])
        self._add_token(stem_o, [(self.suffix_graph.A3Pl_Pron, 'nlar'), self.suffix_graph.Pnon_Pron, (self.suffix_graph.Loc_Pron,    u'da')])
        self._add_token(stem_o, [(self.suffix_graph.A3Pl_Pron, 'nlar'), self.suffix_graph.Pnon_Pron, (self.suffix_graph.Abl_Pron,    u'dan')])
        self._add_token(stem_o, [(self.suffix_graph.A3Pl_Pron, 'nlar'), self.suffix_graph.Pnon_Pron, (self.suffix_graph.Ins_Pron,    u'la')])
        self._add_token(stem_o, [(self.suffix_graph.A3Pl_Pron, 'nlar'), self.suffix_graph.Pnon_Pron, (self.suffix_graph.Gen_Pron,    u'ın')])
        self._add_token(stem_o, [(self.suffix_graph.A3Pl_Pron, 'nlar'), self.suffix_graph.Pnon_Pron, (self.suffix_graph.AccordingTo, u'ca')])

        self._add_token(stem_o, [(self.suffix_graph.A3Pl_Pron, 'nlar'), self.suffix_graph.Pnon_Pron,  self.suffix_graph.Nom_Pron_Deriv])

    def _create_predefined_path_of_bu_pron_demons(self):
        stem_bu = self._find_stem(u'bu', SyntacticCategory.PRONOUN, SecondarySyntacticCategory.DEMONSTRATIVE)

        self._add_token(stem_bu, [self.suffix_graph.A3Sg_Pron, self.suffix_graph.Pnon_Pron,  self.suffix_graph.Nom_Pron])
        self._add_token(stem_bu, [self.suffix_graph.A3Sg_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Acc_Pron, u'nu')])
        self._add_token(stem_bu, [self.suffix_graph.A3Sg_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Dat_Pron, u'na')])
        self._add_token(stem_bu, [self.suffix_graph.A3Sg_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Loc_Pron, u'nda')])
        self._add_token(stem_bu, [self.suffix_graph.A3Sg_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Abl_Pron, u'ndan')])
        self._add_token(stem_bu, [self.suffix_graph.A3Sg_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Ins_Pron, u'nla')])
        self._add_token(stem_bu, [self.suffix_graph.A3Sg_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Ins_Pron, u'nunla')])
        self._add_token(stem_bu, [self.suffix_graph.A3Sg_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Gen_Pron, u'nun')])

        self._add_token(stem_bu, [self.suffix_graph.A3Sg_Pron, self.suffix_graph.Pnon_Pron,  self.suffix_graph.Nom_Pron_Deriv])

    def _create_predefined_path_of_su_pron_demons(self):
        stem_su = self._find_stem(u'şu', SyntacticCategory.PRONOUN, SecondarySyntacticCategory.DEMONSTRATIVE)

        self._add_token(stem_su, [self.suffix_graph.A3Sg_Pron, self.suffix_graph.Pnon_Pron,  self.suffix_graph.Nom_Pron])
        self._add_token(stem_su, [self.suffix_graph.A3Sg_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Acc_Pron, u'nu')])
        self._add_token(stem_su, [self.suffix_graph.A3Sg_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Dat_Pron, u'na')])
        self._add_token(stem_su, [self.suffix_graph.A3Sg_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Loc_Pron, u'nda')])
        self._add_token(stem_su, [self.suffix_graph.A3Sg_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Abl_Pron, u'ndan')])
        self._add_token(stem_su, [self.suffix_graph.A3Sg_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Ins_Pron, u'nla')])
        self._add_token(stem_su, [self.suffix_graph.A3Sg_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Ins_Pron, u'nunla')])
        self._add_token(stem_su, [self.suffix_graph.A3Sg_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Gen_Pron, u'nun')])

        self._add_token(stem_su, [self.suffix_graph.A3Sg_Pron, self.suffix_graph.Pnon_Pron,  self.suffix_graph.Nom_Pron_Deriv])

    def _create_predefined_path_of_o_pron_demons(self):
        stem_o = self._find_stem(u'o', SyntacticCategory.PRONOUN, SecondarySyntacticCategory.DEMONSTRATIVE)

        self._add_token(stem_o, [self.suffix_graph.A3Sg_Pron, self.suffix_graph.Pnon_Pron, self.suffix_graph.Nom_Pron])
        self._add_token(stem_o, [self.suffix_graph.A3Sg_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Acc_Pron, u'nu')])
        self._add_token(stem_o, [self.suffix_graph.A3Sg_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Dat_Pron, u'na')])
        self._add_token(stem_o, [self.suffix_graph.A3Sg_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Loc_Pron, u'nda')])
        self._add_token(stem_o, [self.suffix_graph.A3Sg_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Abl_Pron, u'ndan')])
        self._add_token(stem_o, [self.suffix_graph.A3Sg_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Ins_Pron, u'nla')])
        self._add_token(stem_o, [self.suffix_graph.A3Sg_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Ins_Pron, u'nunla')])
        self._add_token(stem_o, [self.suffix_graph.A3Sg_Pron, self.suffix_graph.Pnon_Pron, (self.suffix_graph.Gen_Pron, u'nun')])

        self._add_token(stem_o, [self.suffix_graph.A3Sg_Pron, self.suffix_graph.Pnon_Pron, self.suffix_graph.Nom_Pron_Deriv])

    def _create_predefined_path_of_bunlar_pron_demons(self):
        stem_bu = self._find_stem(u'bu', SyntacticCategory.PRONOUN, SecondarySyntacticCategory.DEMONSTRATIVE)

        self._add_token(stem_bu, [(self.suffix_graph.A3Pl_Pron, 'nlar'), self.suffix_graph.Pnon_Pron, self.suffix_graph.Nom_Pron])
        self._add_token(stem_bu, [(self.suffix_graph.A3Pl_Pron, 'nlar'), self.suffix_graph.Pnon_Pron, (self.suffix_graph.Acc_Pron, u'ı')])
        self._add_token(stem_bu, [(self.suffix_graph.A3Pl_Pron, 'nlar'), self.suffix_graph.Pnon_Pron, (self.suffix_graph.Dat_Pron, u'a')])
        self._add_token(stem_bu, [(self.suffix_graph.A3Pl_Pron, 'nlar'), self.suffix_graph.Pnon_Pron, (self.suffix_graph.Loc_Pron, u'da')])
        self._add_token(stem_bu, [(self.suffix_graph.A3Pl_Pron, 'nlar'), self.suffix_graph.Pnon_Pron, (self.suffix_graph.Abl_Pron, u'dan')])
        self._add_token(stem_bu, [(self.suffix_graph.A3Pl_Pron, 'nlar'), self.suffix_graph.Pnon_Pron, (self.suffix_graph.Ins_Pron, u'la')])
        self._add_token(stem_bu, [(self.suffix_graph.A3Pl_Pron, 'nlar'), self.suffix_graph.Pnon_Pron, (self.suffix_graph.Gen_Pron, u'ın')])

        self._add_token(stem_bu, [(self.suffix_graph.A3Pl_Pron, 'nlar'), self.suffix_graph.Pnon_Pron, self.suffix_graph.Nom_Pron_Deriv])

    def _create_predefined_path_of_sunlar_pron_demons(self):
        stem_su = self._find_stem(u'şu', SyntacticCategory.PRONOUN, SecondarySyntacticCategory.DEMONSTRATIVE)

        self._add_token(stem_su, [(self.suffix_graph.A3Pl_Pron, 'nlar'), self.suffix_graph.Pnon_Pron, self.suffix_graph.Nom_Pron])
        self._add_token(stem_su, [(self.suffix_graph.A3Pl_Pron, 'nlar'), self.suffix_graph.Pnon_Pron, (self.suffix_graph.Acc_Pron, u'ı')])
        self._add_token(stem_su, [(self.suffix_graph.A3Pl_Pron, 'nlar'), self.suffix_graph.Pnon_Pron, (self.suffix_graph.Dat_Pron, u'a')])
        self._add_token(stem_su, [(self.suffix_graph.A3Pl_Pron, 'nlar'), self.suffix_graph.Pnon_Pron, (self.suffix_graph.Loc_Pron, u'da')])
        self._add_token(stem_su, [(self.suffix_graph.A3Pl_Pron, 'nlar'), self.suffix_graph.Pnon_Pron, (self.suffix_graph.Abl_Pron, u'dan')])
        self._add_token(stem_su, [(self.suffix_graph.A3Pl_Pron, 'nlar'), self.suffix_graph.Pnon_Pron, (self.suffix_graph.Ins_Pron, u'la')])
        self._add_token(stem_su, [(self.suffix_graph.A3Pl_Pron, 'nlar'), self.suffix_graph.Pnon_Pron, (self.suffix_graph.Gen_Pron, u'ın')])

        self._add_token(stem_su, [(self.suffix_graph.A3Pl_Pron, 'nlar'), self.suffix_graph.Pnon_Pron, self.suffix_graph.Nom_Pron_Deriv])

    def _create_predefined_path_of_onlar_pron_demons(self):
        stem_o = self._find_stem(u'o', SyntacticCategory.PRONOUN, SecondarySyntacticCategory.DEMONSTRATIVE)

        self._add_token(stem_o, [(self.suffix_graph.A3Pl_Pron, 'nlar'), self.suffix_graph.Pnon_Pron, self.suffix_graph.Nom_Pron])
        self._add_token(stem_o, [(self.suffix_graph.A3Pl_Pron, 'nlar'), self.suffix_graph.Pnon_Pron, (self.suffix_graph.Acc_Pron, u'ı')])
        self._add_token(stem_o, [(self.suffix_graph.A3Pl_Pron, 'nlar'), self.suffix_graph.Pnon_Pron, (self.suffix_graph.Dat_Pron, u'a')])
        self._add_token(stem_o, [(self.suffix_graph.A3Pl_Pron, 'nlar'), self.suffix_graph.Pnon_Pron, (self.suffix_graph.Loc_Pron, u'da')])
        self._add_token(stem_o, [(self.suffix_graph.A3Pl_Pron, 'nlar'), self.suffix_graph.Pnon_Pron, (self.suffix_graph.Abl_Pron, u'dan')])
        self._add_token(stem_o, [(self.suffix_graph.A3Pl_Pron, 'nlar'), self.suffix_graph.Pnon_Pron, (self.suffix_graph.Ins_Pron, u'la')])
        self._add_token(stem_o, [(self.suffix_graph.A3Pl_Pron, 'nlar'), self.suffix_graph.Pnon_Pron, (self.suffix_graph.Gen_Pron, u'ın')])

        self._add_token(stem_o, [(self.suffix_graph.A3Pl_Pron, 'nlar'), self.suffix_graph.Pnon_Pron, self.suffix_graph.Nom_Pron_Deriv])

    def _create_predefined_path_of_kendi(self):
        stem_kendi = self._find_stem(u'kendi', SyntacticCategory.PRONOUN, SecondarySyntacticCategory.REFLEXIVE)

        ##### A1Sg
        self._add_token(stem_kendi, [self.suffix_graph.A1Sg_Pron, (self.suffix_graph.P1Sg_Pron,'m'), self.suffix_graph.Nom_Pron])
        self._add_token(stem_kendi, [self.suffix_graph.A1Sg_Pron, (self.suffix_graph.P1Sg_Pron,'m'), (self.suffix_graph.Acc_Pron, u'i')])
        self._add_token(stem_kendi, [self.suffix_graph.A1Sg_Pron, (self.suffix_graph.P1Sg_Pron,'m'), (self.suffix_graph.Dat_Pron, u'e')])
        self._add_token(stem_kendi, [self.suffix_graph.A1Sg_Pron, (self.suffix_graph.P1Sg_Pron,'m'), (self.suffix_graph.Loc_Pron, u'de')])
        self._add_token(stem_kendi, [self.suffix_graph.A1Sg_Pron, (self.suffix_graph.P1Sg_Pron,'m'), (self.suffix_graph.Abl_Pron, u'den')])
        self._add_token(stem_kendi, [self.suffix_graph.A1Sg_Pron, (self.suffix_graph.P1Sg_Pron,'m'), (self.suffix_graph.Ins_Pron, u'le')])
        self._add_token(stem_kendi, [self.suffix_graph.A1Sg_Pron, (self.suffix_graph.P1Sg_Pron,'m'), (self.suffix_graph.Gen_Pron, u'in')])

        self._add_token(stem_kendi, [self.suffix_graph.A1Sg_Pron, (self.suffix_graph.P1Sg_Pron,'m'), self.suffix_graph.Nom_Pron_Deriv])

        ##### A2Sg
        self._add_token(stem_kendi, [self.suffix_graph.A2Sg_Pron, (self.suffix_graph.P2Sg_Pron,'n'), self.suffix_graph.Nom_Pron])
        self._add_token(stem_kendi, [self.suffix_graph.A2Sg_Pron, (self.suffix_graph.P2Sg_Pron,'n'), (self.suffix_graph.Acc_Pron, u'i')])
        self._add_token(stem_kendi, [self.suffix_graph.A2Sg_Pron, (self.suffix_graph.P2Sg_Pron,'n'), (self.suffix_graph.Dat_Pron, u'e')])
        self._add_token(stem_kendi, [self.suffix_graph.A2Sg_Pron, (self.suffix_graph.P2Sg_Pron,'n'), (self.suffix_graph.Loc_Pron, u'de')])
        self._add_token(stem_kendi, [self.suffix_graph.A2Sg_Pron, (self.suffix_graph.P2Sg_Pron,'n'), (self.suffix_graph.Abl_Pron, u'den')])
        self._add_token(stem_kendi, [self.suffix_graph.A2Sg_Pron, (self.suffix_graph.P2Sg_Pron,'n'), (self.suffix_graph.Ins_Pron, u'le')])
        self._add_token(stem_kendi, [self.suffix_graph.A2Sg_Pron, (self.suffix_graph.P2Sg_Pron,'n'), (self.suffix_graph.Gen_Pron, u'in')])

        self._add_token(stem_kendi, [self.suffix_graph.A2Sg_Pron, (self.suffix_graph.P2Sg_Pron,'n'), self.suffix_graph.Nom_Pron_Deriv])

        ##### A3Sg
        self._add_token(stem_kendi, [self.suffix_graph.A3Sg_Pron, self.suffix_graph.P3Sg_Pron, self.suffix_graph.Nom_Pron])
        self._add_token(stem_kendi, [self.suffix_graph.A3Sg_Pron, self.suffix_graph.P3Sg_Pron, (self.suffix_graph.Acc_Pron, u'ni')])
        self._add_token(stem_kendi, [self.suffix_graph.A3Sg_Pron, self.suffix_graph.P3Sg_Pron, (self.suffix_graph.Dat_Pron, u'ne')])
        self._add_token(stem_kendi, [self.suffix_graph.A3Sg_Pron, self.suffix_graph.P3Sg_Pron, (self.suffix_graph.Loc_Pron, u'nde')])
        self._add_token(stem_kendi, [self.suffix_graph.A3Sg_Pron, self.suffix_graph.P3Sg_Pron, (self.suffix_graph.Abl_Pron, u'nden')])
        self._add_token(stem_kendi, [self.suffix_graph.A3Sg_Pron, self.suffix_graph.P3Sg_Pron, (self.suffix_graph.Ins_Pron, u'yle')])
        self._add_token(stem_kendi, [self.suffix_graph.A3Sg_Pron, self.suffix_graph.P3Sg_Pron, (self.suffix_graph.Gen_Pron, u'nin')])

        self._add_token(stem_kendi, [self.suffix_graph.A3Sg_Pron, self.suffix_graph.P3Sg_Pron, self.suffix_graph.Nom_Pron_Deriv])

        self._add_token(stem_kendi, [self.suffix_graph.A3Sg_Pron, (self.suffix_graph.P3Sg_Pron,'si'), self.suffix_graph.Nom_Pron])
        self._add_token(stem_kendi, [self.suffix_graph.A3Sg_Pron, (self.suffix_graph.P3Sg_Pron,'si'), (self.suffix_graph.Acc_Pron, u'ni')])
        self._add_token(stem_kendi, [self.suffix_graph.A3Sg_Pron, (self.suffix_graph.P3Sg_Pron,'si'), (self.suffix_graph.Dat_Pron, u'ne')])
        self._add_token(stem_kendi, [self.suffix_graph.A3Sg_Pron, (self.suffix_graph.P3Sg_Pron,'si'), (self.suffix_graph.Loc_Pron, u'nde')])
        self._add_token(stem_kendi, [self.suffix_graph.A3Sg_Pron, (self.suffix_graph.P3Sg_Pron,'si'), (self.suffix_graph.Abl_Pron, u'nden')])
        self._add_token(stem_kendi, [self.suffix_graph.A3Sg_Pron, (self.suffix_graph.P3Sg_Pron,'si'), (self.suffix_graph.Ins_Pron, u'yle')])
        self._add_token(stem_kendi, [self.suffix_graph.A3Sg_Pron, (self.suffix_graph.P3Sg_Pron,'si'), (self.suffix_graph.Gen_Pron, u'nin')])

        self._add_token(stem_kendi, [self.suffix_graph.A3Sg_Pron, (self.suffix_graph.P3Sg_Pron,'si'), self.suffix_graph.Nom_Pron_Deriv])


        ##### A1pl
        self._add_token(stem_kendi, [self.suffix_graph.A1Pl_Pron, (self.suffix_graph.P1Pl_Pron,'miz'), self.suffix_graph.Nom_Pron])
        self._add_token(stem_kendi, [self.suffix_graph.A1Pl_Pron, (self.suffix_graph.P1Pl_Pron,'miz'), (self.suffix_graph.Acc_Pron, u'i')])
        self._add_token(stem_kendi, [self.suffix_graph.A1Pl_Pron, (self.suffix_graph.P1Pl_Pron,'miz'), (self.suffix_graph.Dat_Pron, u'e')])
        self._add_token(stem_kendi, [self.suffix_graph.A1Pl_Pron, (self.suffix_graph.P1Pl_Pron,'miz'), (self.suffix_graph.Loc_Pron, u'de')])
        self._add_token(stem_kendi, [self.suffix_graph.A1Pl_Pron, (self.suffix_graph.P1Pl_Pron,'miz'), (self.suffix_graph.Abl_Pron, u'den')])
        self._add_token(stem_kendi, [self.suffix_graph.A1Pl_Pron, (self.suffix_graph.P1Pl_Pron,'miz'), (self.suffix_graph.Ins_Pron, u'le')])
        self._add_token(stem_kendi, [self.suffix_graph.A1Pl_Pron, (self.suffix_graph.P1Pl_Pron,'miz'), (self.suffix_graph.Gen_Pron, u'in')])

        self._add_token(stem_kendi, [self.suffix_graph.A1Pl_Pron, (self.suffix_graph.P1Pl_Pron,'miz'), self.suffix_graph.Nom_Pron_Deriv])

        self._add_token(stem_kendi, [(self.suffix_graph.A1Pl_Pron,'ler'), (self.suffix_graph.P1Pl_Pron,'imiz'), self.suffix_graph.Nom_Pron])
        self._add_token(stem_kendi, [(self.suffix_graph.A1Pl_Pron,'ler'), (self.suffix_graph.P1Pl_Pron,'imiz'), (self.suffix_graph.Acc_Pron, u'i')])
        self._add_token(stem_kendi, [(self.suffix_graph.A1Pl_Pron,'ler'), (self.suffix_graph.P1Pl_Pron,'imiz'), (self.suffix_graph.Dat_Pron, u'e')])
        self._add_token(stem_kendi, [(self.suffix_graph.A1Pl_Pron,'ler'), (self.suffix_graph.P1Pl_Pron,'imiz'), (self.suffix_graph.Loc_Pron, u'de')])
        self._add_token(stem_kendi, [(self.suffix_graph.A1Pl_Pron,'ler'), (self.suffix_graph.P1Pl_Pron,'imiz'), (self.suffix_graph.Abl_Pron, u'den')])
        self._add_token(stem_kendi, [(self.suffix_graph.A1Pl_Pron,'ler'), (self.suffix_graph.P1Pl_Pron,'imiz'), (self.suffix_graph.Ins_Pron, u'le')])
        self._add_token(stem_kendi, [(self.suffix_graph.A1Pl_Pron,'ler'), (self.suffix_graph.P1Pl_Pron,'imiz'), (self.suffix_graph.Gen_Pron, u'in')])

        self._add_token(stem_kendi, [(self.suffix_graph.A1Pl_Pron,'ler'), (self.suffix_graph.P1Pl_Pron,'imiz'), self.suffix_graph.Nom_Pron_Deriv])

        ##### A2pl
        self._add_token(stem_kendi, [self.suffix_graph.A2Pl_Pron, (self.suffix_graph.P2Pl_Pron,'niz'), self.suffix_graph.Nom_Pron])
        self._add_token(stem_kendi, [self.suffix_graph.A2Pl_Pron, (self.suffix_graph.P2Pl_Pron,'niz'), (self.suffix_graph.Acc_Pron, u'i')])
        self._add_token(stem_kendi, [self.suffix_graph.A2Pl_Pron, (self.suffix_graph.P2Pl_Pron,'niz'), (self.suffix_graph.Dat_Pron, u'e')])
        self._add_token(stem_kendi, [self.suffix_graph.A2Pl_Pron, (self.suffix_graph.P2Pl_Pron,'niz'), (self.suffix_graph.Loc_Pron, u'de')])
        self._add_token(stem_kendi, [self.suffix_graph.A2Pl_Pron, (self.suffix_graph.P2Pl_Pron,'niz'), (self.suffix_graph.Abl_Pron, u'den')])
        self._add_token(stem_kendi, [self.suffix_graph.A2Pl_Pron, (self.suffix_graph.P2Pl_Pron,'niz'), (self.suffix_graph.Ins_Pron, u'le')])
        self._add_token(stem_kendi, [self.suffix_graph.A2Pl_Pron, (self.suffix_graph.P2Pl_Pron,'niz'), (self.suffix_graph.Gen_Pron, u'in')])

        self._add_token(stem_kendi, [self.suffix_graph.A2Pl_Pron, (self.suffix_graph.P2Pl_Pron,'niz'), self.suffix_graph.Nom_Pron_Deriv])

        self._add_token(stem_kendi, [(self.suffix_graph.A2Pl_Pron,'ler'), (self.suffix_graph.P2Pl_Pron,'iniz'), self.suffix_graph.Nom_Pron])
        self._add_token(stem_kendi, [(self.suffix_graph.A2Pl_Pron,'ler'), (self.suffix_graph.P2Pl_Pron,'iniz'), (self.suffix_graph.Acc_Pron, u'i')])
        self._add_token(stem_kendi, [(self.suffix_graph.A2Pl_Pron,'ler'), (self.suffix_graph.P2Pl_Pron,'iniz'), (self.suffix_graph.Dat_Pron, u'e')])
        self._add_token(stem_kendi, [(self.suffix_graph.A2Pl_Pron,'ler'), (self.suffix_graph.P2Pl_Pron,'iniz'), (self.suffix_graph.Loc_Pron, u'de')])
        self._add_token(stem_kendi, [(self.suffix_graph.A2Pl_Pron,'ler'), (self.suffix_graph.P2Pl_Pron,'iniz'), (self.suffix_graph.Abl_Pron, u'den')])
        self._add_token(stem_kendi, [(self.suffix_graph.A2Pl_Pron,'ler'), (self.suffix_graph.P2Pl_Pron,'iniz'), (self.suffix_graph.Ins_Pron, u'le')])
        self._add_token(stem_kendi, [(self.suffix_graph.A2Pl_Pron,'ler'), (self.suffix_graph.P2Pl_Pron,'iniz'), (self.suffix_graph.Gen_Pron, u'in')])

        self._add_token(stem_kendi, [(self.suffix_graph.A2Pl_Pron,'ler'), (self.suffix_graph.P2Pl_Pron,'iniz'), self.suffix_graph.Nom_Pron_Deriv])

        ##### A3pl
        self._add_token(stem_kendi, [(self.suffix_graph.A3Pl_Pron,'leri'), self.suffix_graph.P3Pl_Pron, self.suffix_graph.Nom_Pron])
        self._add_token(stem_kendi, [(self.suffix_graph.A3Pl_Pron,'leri'), self.suffix_graph.P3Pl_Pron, (self.suffix_graph.Acc_Pron, u'ni')])
        self._add_token(stem_kendi, [(self.suffix_graph.A3Pl_Pron,'leri'), self.suffix_graph.P3Pl_Pron, (self.suffix_graph.Dat_Pron, u'ne')])
        self._add_token(stem_kendi, [(self.suffix_graph.A3Pl_Pron,'leri'), self.suffix_graph.P3Pl_Pron, (self.suffix_graph.Loc_Pron, u'nde')])
        self._add_token(stem_kendi, [(self.suffix_graph.A3Pl_Pron,'leri'), self.suffix_graph.P3Pl_Pron, (self.suffix_graph.Abl_Pron, u'nden')])
        self._add_token(stem_kendi, [(self.suffix_graph.A3Pl_Pron,'leri'), self.suffix_graph.P3Pl_Pron, (self.suffix_graph.Ins_Pron, u'yle')])
        self._add_token(stem_kendi, [(self.suffix_graph.A3Pl_Pron,'leri'), self.suffix_graph.P3Pl_Pron, (self.suffix_graph.Gen_Pron, u'nin')])

        self._add_token(stem_kendi, [(self.suffix_graph.A3Pl_Pron,'leri'), self.suffix_graph.P3Pl_Pron, self.suffix_graph.Nom_Pron_Deriv])

    def _create_predefined_path_of_hepsi(self):
        stem_hep = self._find_stem(u'hep', SyntacticCategory.PRONOUN, None)
        stem_hepsi = self._find_stem(u'hepsi', SyntacticCategory.PRONOUN, None)

        ##### No A1Sg

        ##### No A2Sg

        ##### No A3Sg

        ##### A1pl
        self._add_token(stem_hep, [self.suffix_graph.A1Pl_Pron, (self.suffix_graph.P1Pl_Pron,'imiz'), self.suffix_graph.Nom_Pron])
        self._add_token(stem_hep, [self.suffix_graph.A1Pl_Pron, (self.suffix_graph.P1Pl_Pron,'imiz'), (self.suffix_graph.Acc_Pron,    u'i')])
        self._add_token(stem_hep, [self.suffix_graph.A1Pl_Pron, (self.suffix_graph.P1Pl_Pron,'imiz'), (self.suffix_graph.Dat_Pron,    u'e')])
        self._add_token(stem_hep, [self.suffix_graph.A1Pl_Pron, (self.suffix_graph.P1Pl_Pron,'imiz'), (self.suffix_graph.Loc_Pron,    u'de')])
        self._add_token(stem_hep, [self.suffix_graph.A1Pl_Pron, (self.suffix_graph.P1Pl_Pron,'imiz'), (self.suffix_graph.Abl_Pron,    u'den')])
        self._add_token(stem_hep, [self.suffix_graph.A1Pl_Pron, (self.suffix_graph.P1Pl_Pron,'imiz'), (self.suffix_graph.Ins_Pron,    u'le')])
        self._add_token(stem_hep, [self.suffix_graph.A1Pl_Pron, (self.suffix_graph.P1Pl_Pron,'imiz'), (self.suffix_graph.Gen_Pron,    u'in')])
        self._add_token(stem_hep, [self.suffix_graph.A1Pl_Pron, (self.suffix_graph.P1Pl_Pron,'imiz'), (self.suffix_graph.AccordingTo, u'ce')])

        self._add_token(stem_hep, [self.suffix_graph.A1Pl_Pron, (self.suffix_graph.P1Pl_Pron,'imiz'), self.suffix_graph.Nom_Pron_Deriv])

        ##### A2pl
        self._add_token(stem_hep, [self.suffix_graph.A2Pl_Pron, (self.suffix_graph.P2Pl_Pron,'iniz'), self.suffix_graph.Nom_Pron])
        self._add_token(stem_hep, [self.suffix_graph.A2Pl_Pron, (self.suffix_graph.P2Pl_Pron,'iniz'), (self.suffix_graph.Acc_Pron,    u'i')])
        self._add_token(stem_hep, [self.suffix_graph.A2Pl_Pron, (self.suffix_graph.P2Pl_Pron,'iniz'), (self.suffix_graph.Dat_Pron,    u'e')])
        self._add_token(stem_hep, [self.suffix_graph.A2Pl_Pron, (self.suffix_graph.P2Pl_Pron,'iniz'), (self.suffix_graph.Loc_Pron,    u'de')])
        self._add_token(stem_hep, [self.suffix_graph.A2Pl_Pron, (self.suffix_graph.P2Pl_Pron,'iniz'), (self.suffix_graph.Abl_Pron,    u'den')])
        self._add_token(stem_hep, [self.suffix_graph.A2Pl_Pron, (self.suffix_graph.P2Pl_Pron,'iniz'), (self.suffix_graph.Ins_Pron,    u'le')])
        self._add_token(stem_hep, [self.suffix_graph.A2Pl_Pron, (self.suffix_graph.P2Pl_Pron,'iniz'), (self.suffix_graph.Gen_Pron,    u'in')])
        self._add_token(stem_hep, [self.suffix_graph.A2Pl_Pron, (self.suffix_graph.P2Pl_Pron,'iniz'), (self.suffix_graph.AccordingTo, u'ce')])

        self._add_token(stem_hep, [self.suffix_graph.A2Pl_Pron, (self.suffix_graph.P2Pl_Pron,'iniz'), self.suffix_graph.Nom_Pron_Deriv])

        ##### A3pl

        self._add_token(stem_hepsi, [self.suffix_graph.A3Pl_Pron, self.suffix_graph.P3Pl_Pron, self.suffix_graph.Nom_Pron])
        self._add_token(stem_hepsi, [self.suffix_graph.A3Pl_Pron, self.suffix_graph.P3Pl_Pron, (self.suffix_graph.Acc_Pron,    u'ni')])
        self._add_token(stem_hepsi, [self.suffix_graph.A3Pl_Pron, self.suffix_graph.P3Pl_Pron, (self.suffix_graph.Dat_Pron,    u'ne')])
        self._add_token(stem_hepsi, [self.suffix_graph.A3Pl_Pron, self.suffix_graph.P3Pl_Pron, (self.suffix_graph.Loc_Pron,    u'nde')])
        self._add_token(stem_hepsi, [self.suffix_graph.A3Pl_Pron, self.suffix_graph.P3Pl_Pron, (self.suffix_graph.Abl_Pron,    u'nden')])
        self._add_token(stem_hepsi, [self.suffix_graph.A3Pl_Pron, self.suffix_graph.P3Pl_Pron, (self.suffix_graph.Ins_Pron,    u'yle')])
        self._add_token(stem_hepsi, [self.suffix_graph.A3Pl_Pron, self.suffix_graph.P3Pl_Pron, (self.suffix_graph.Gen_Pron,    u'nin')])
        self._add_token(stem_hepsi, [self.suffix_graph.A3Pl_Pron, self.suffix_graph.P3Pl_Pron, (self.suffix_graph.AccordingTo, u'nce')])

        self._add_token(stem_hepsi, [self.suffix_graph.A3Pl_Pron, self.suffix_graph.P3Pl_Pron, self.suffix_graph.Nom_Pron_Deriv])

    def _create_predefined_path_of_question_particles(self):
        stem_mii = self._find_stem(u'mı', SyntacticCategory.QUESTION, None)
        stem_mi  = self._find_stem(u'mi', SyntacticCategory.QUESTION, None)
        stem_mu  = self._find_stem(u'mu', SyntacticCategory.QUESTION, None)
        stem_muu = self._find_stem(u'mü', SyntacticCategory.QUESTION, None)

        ##### Pres
        self._add_token(stem_mii, [self.suffix_graph.Pres_Ques, (self.suffix_graph.A1Sg_Ques,u'yım')])
        self._add_token(stem_mii, [self.suffix_graph.Pres_Ques, (self.suffix_graph.A2Sg_Ques,u'sın')])
        self._add_token(stem_mii, [self.suffix_graph.Pres_Ques, (self.suffix_graph.A3Sg_Ques,u'')])
        self._add_token(stem_mii, [self.suffix_graph.Pres_Ques, (self.suffix_graph.A1Pl_Ques,u'yız')])
        self._add_token(stem_mii, [self.suffix_graph.Pres_Ques, (self.suffix_graph.A2Pl_Ques,u'sınız')])
        self._add_token(stem_mii, [self.suffix_graph.Pres_Ques, (self.suffix_graph.A3Pl_Ques,u'lar')])

        self._add_token(stem_mi , [self.suffix_graph.Pres_Ques, (self.suffix_graph.A1Sg_Ques,u'yim')])
        self._add_token(stem_mi , [self.suffix_graph.Pres_Ques, (self.suffix_graph.A2Sg_Ques,u'sin')])
        self._add_token(stem_mi , [self.suffix_graph.Pres_Ques, (self.suffix_graph.A3Sg_Ques,u'')])
        self._add_token(stem_mi , [self.suffix_graph.Pres_Ques, (self.suffix_graph.A1Pl_Ques,u'yiz')])
        self._add_token(stem_mi , [self.suffix_graph.Pres_Ques, (self.suffix_graph.A2Pl_Ques,u'siniz')])
        self._add_token(stem_mi , [self.suffix_graph.Pres_Ques, (self.suffix_graph.A3Pl_Ques,u'ler')])

        self._add_token(stem_mu , [self.suffix_graph.Pres_Ques, (self.suffix_graph.A1Sg_Ques,u'yum')])
        self._add_token(stem_mu , [self.suffix_graph.Pres_Ques, (self.suffix_graph.A2Sg_Ques,u'sun')])
        self._add_token(stem_mu , [self.suffix_graph.Pres_Ques, (self.suffix_graph.A3Sg_Ques,u'')])
        self._add_token(stem_mu , [self.suffix_graph.Pres_Ques, (self.suffix_graph.A1Pl_Ques,u'yuz')])
        self._add_token(stem_mu , [self.suffix_graph.Pres_Ques, (self.suffix_graph.A2Pl_Ques,u'sunuz')])
        self._add_token(stem_mu , [self.suffix_graph.Pres_Ques, (self.suffix_graph.A3Pl_Ques,u'lar')])

        self._add_token(stem_muu, [self.suffix_graph.Pres_Ques, (self.suffix_graph.A1Sg_Ques,u'yüm')])
        self._add_token(stem_muu, [self.suffix_graph.Pres_Ques, (self.suffix_graph.A2Sg_Ques,u'sün')])
        self._add_token(stem_muu, [self.suffix_graph.Pres_Ques, (self.suffix_graph.A3Sg_Ques,u'')])
        self._add_token(stem_muu, [self.suffix_graph.Pres_Ques, (self.suffix_graph.A1Pl_Ques,u'yüz')])
        self._add_token(stem_muu, [self.suffix_graph.Pres_Ques, (self.suffix_graph.A2Pl_Ques,u'sünüz')])
        self._add_token(stem_muu, [self.suffix_graph.Pres_Ques, (self.suffix_graph.A3Pl_Ques,u'ler')])

        ##### Past
        self._add_token(stem_mii, [(self.suffix_graph.Past_Ques,u'ydı'), (self.suffix_graph.A1Sg_Ques,u'm')])
        self._add_token(stem_mii, [(self.suffix_graph.Past_Ques,u'ydı'), (self.suffix_graph.A2Sg_Ques,u'n')])
        self._add_token(stem_mii, [(self.suffix_graph.Past_Ques,u'ydı'), (self.suffix_graph.A3Sg_Ques,u'')])
        self._add_token(stem_mii, [(self.suffix_graph.Past_Ques,u'ydı'), (self.suffix_graph.A1Pl_Ques,u'k')])
        self._add_token(stem_mii, [(self.suffix_graph.Past_Ques,u'ydı'), (self.suffix_graph.A2Pl_Ques,u'nız')])
        self._add_token(stem_mii, [(self.suffix_graph.Past_Ques,u'ydı'), (self.suffix_graph.A3Pl_Ques,u'lar')])

        self._add_token(stem_mi , [(self.suffix_graph.Past_Ques,u'ydi'), (self.suffix_graph.A1Sg_Ques,u'm')])
        self._add_token(stem_mi , [(self.suffix_graph.Past_Ques,u'ydi'), (self.suffix_graph.A2Sg_Ques,u'n')])
        self._add_token(stem_mi , [(self.suffix_graph.Past_Ques,u'ydi'), (self.suffix_graph.A3Sg_Ques,u'')])
        self._add_token(stem_mi , [(self.suffix_graph.Past_Ques,u'ydi'), (self.suffix_graph.A1Pl_Ques,u'k')])
        self._add_token(stem_mi , [(self.suffix_graph.Past_Ques,u'ydi'), (self.suffix_graph.A2Pl_Ques,u'niz')])
        self._add_token(stem_mi , [(self.suffix_graph.Past_Ques,u'ydi'), (self.suffix_graph.A3Pl_Ques,u'ler')])

        self._add_token(stem_mu , [(self.suffix_graph.Past_Ques,u'ydu'), (self.suffix_graph.A1Sg_Ques,u'm')])
        self._add_token(stem_mu , [(self.suffix_graph.Past_Ques,u'ydu'), (self.suffix_graph.A2Sg_Ques,u'n')])
        self._add_token(stem_mu , [(self.suffix_graph.Past_Ques,u'ydu'), (self.suffix_graph.A3Sg_Ques,u'')])
        self._add_token(stem_mu , [(self.suffix_graph.Past_Ques,u'ydu'), (self.suffix_graph.A1Pl_Ques,u'k')])
        self._add_token(stem_mu , [(self.suffix_graph.Past_Ques,u'ydu'), (self.suffix_graph.A2Pl_Ques,u'nuz')])
        self._add_token(stem_mu , [(self.suffix_graph.Past_Ques,u'ydu'), (self.suffix_graph.A3Pl_Ques,u'lar')])

        self._add_token(stem_muu, [(self.suffix_graph.Past_Ques,u'ydü'), (self.suffix_graph.A1Sg_Ques,u'm')])
        self._add_token(stem_muu, [(self.suffix_graph.Past_Ques,u'ydü'), (self.suffix_graph.A2Sg_Ques,u'n')])
        self._add_token(stem_muu, [(self.suffix_graph.Past_Ques,u'ydü'), (self.suffix_graph.A3Sg_Ques,u'')])
        self._add_token(stem_muu, [(self.suffix_graph.Past_Ques,u'ydü'), (self.suffix_graph.A1Pl_Ques,u'k')])
        self._add_token(stem_muu, [(self.suffix_graph.Past_Ques,u'ydü'), (self.suffix_graph.A2Pl_Ques,u'nüz')])
        self._add_token(stem_muu, [(self.suffix_graph.Past_Ques,u'ydü'), (self.suffix_graph.A3Pl_Ques,u'ler')])

        ##### Narr
        self._add_token(stem_mii, [(self.suffix_graph.Past_Ques,u'ymış'), (self.suffix_graph.A1Sg_Ques,u'ım')])
        self._add_token(stem_mii, [(self.suffix_graph.Past_Ques,u'ymış'), (self.suffix_graph.A2Sg_Ques,u'sın')])
        self._add_token(stem_mii, [(self.suffix_graph.Past_Ques,u'ymış'), (self.suffix_graph.A3Sg_Ques,u'')])
        self._add_token(stem_mii, [(self.suffix_graph.Past_Ques,u'ymış'), (self.suffix_graph.A1Pl_Ques,u'ız')])
        self._add_token(stem_mii, [(self.suffix_graph.Past_Ques,u'ymış'), (self.suffix_graph.A2Pl_Ques,u'sınız')])
        self._add_token(stem_mii, [(self.suffix_graph.Past_Ques,u'ymış'), (self.suffix_graph.A3Pl_Ques,u'lar')])

        self._add_token(stem_mi , [(self.suffix_graph.Past_Ques,u'ymiş'), (self.suffix_graph.A1Sg_Ques,u'im')])
        self._add_token(stem_mi , [(self.suffix_graph.Past_Ques,u'ymiş'), (self.suffix_graph.A2Sg_Ques,u'sin')])
        self._add_token(stem_mi , [(self.suffix_graph.Past_Ques,u'ymiş'), (self.suffix_graph.A3Sg_Ques,u'')])
        self._add_token(stem_mi , [(self.suffix_graph.Past_Ques,u'ymiş'), (self.suffix_graph.A1Pl_Ques,u'iz')])
        self._add_token(stem_mi , [(self.suffix_graph.Past_Ques,u'ymiş'), (self.suffix_graph.A2Pl_Ques,u'siniz')])
        self._add_token(stem_mi , [(self.suffix_graph.Past_Ques,u'ymiş'), (self.suffix_graph.A3Pl_Ques,u'ler')])

        self._add_token(stem_mu , [(self.suffix_graph.Past_Ques,u'ymuş'), (self.suffix_graph.A1Sg_Ques,u'um')])
        self._add_token(stem_mu , [(self.suffix_graph.Past_Ques,u'ymuş'), (self.suffix_graph.A2Sg_Ques,u'sun')])
        self._add_token(stem_mu , [(self.suffix_graph.Past_Ques,u'ymuş'), (self.suffix_graph.A3Sg_Ques,u'')])
        self._add_token(stem_mu , [(self.suffix_graph.Past_Ques,u'ymuş'), (self.suffix_graph.A1Pl_Ques,u'uz')])
        self._add_token(stem_mu , [(self.suffix_graph.Past_Ques,u'ymuş'), (self.suffix_graph.A2Pl_Ques,u'sunuz')])
        self._add_token(stem_mu , [(self.suffix_graph.Past_Ques,u'ymuş'), (self.suffix_graph.A3Pl_Ques,u'lar')])

        self._add_token(stem_muu, [(self.suffix_graph.Past_Ques,u'ymüş'), (self.suffix_graph.A1Sg_Ques,u'üm')])
        self._add_token(stem_muu, [(self.suffix_graph.Past_Ques,u'ymüş'), (self.suffix_graph.A2Sg_Ques,u'sün')])
        self._add_token(stem_muu, [(self.suffix_graph.Past_Ques,u'ymüş'), (self.suffix_graph.A3Sg_Ques,u'')])
        self._add_token(stem_muu, [(self.suffix_graph.Past_Ques,u'ymüş'), (self.suffix_graph.A1Pl_Ques,u'üz')])
        self._add_token(stem_muu, [(self.suffix_graph.Past_Ques,u'ymüş'), (self.suffix_graph.A2Pl_Ques,u'sünüz')])
        self._add_token(stem_muu, [(self.suffix_graph.Past_Ques,u'ymüş'), (self.suffix_graph.A3Pl_Ques,u'ler')])

    def _create_predefined_path_of_ora(self):
        stem_or = self._find_stem(u'or', SyntacticCategory.NOUN, None)

        # define predefined paths for "orda" and "ordan"

        self._add_token(stem_or, [self.suffix_graph.A3Sg_Noun, self.suffix_graph.Pnon_Noun, (self.suffix_graph.Loc_Noun,'da')])
        self._add_token(stem_or, [self.suffix_graph.A3Sg_Noun, self.suffix_graph.Pnon_Noun, (self.suffix_graph.Abl_Noun,'dan')])
