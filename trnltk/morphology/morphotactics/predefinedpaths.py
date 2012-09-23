# coding=utf-8
from trnltk.morphology.model.lexeme import SecondarySyntacticCategory, SyntacticCategory
from trnltk.morphology.contextfree.parser.suffixapplier import *
from trnltk.morphology.morphotactics.suffixgraph import *

class PredefinedPaths(object):
    def __init__(self, root_map, suffix_graph):
        self._root_map = root_map
        self._suffix_graph = suffix_graph
        self._morpheme_container_map = {}

    def _find_root(self, root_str, syntactic_category, secondary_syntactic_category):
        if self._root_map.has_key(root_str):
            roots_for_root_str = self._root_map[root_str]
            for root in roots_for_root_str:
                if root.lexeme.syntactic_category == syntactic_category and root.lexeme.secondary_syntactic_category == secondary_syntactic_category:
                    return root

        raise Exception(u'Unable to find _root {}+{}+{}'.format(root_str, syntactic_category, secondary_syntactic_category))


    def _add_transition(self, morpheme_container, suffix_form_application_str, suffix, to_state, whole_word):
        suffix_form = SuffixForm(suffix_form_application_str)
        suffix_form.suffix = suffix
        new_morpheme_container = try_suffix_form(morpheme_container, suffix_form, to_state, whole_word)
        if not new_morpheme_container:
            raise Exception('Unable to add transition {} {} {} {} {}'.format(morpheme_container, suffix_form_application_str, suffix, to_state, whole_word))
        return new_morpheme_container

    def _find_to_state(self, state, suffix):
        for (out_suffix, out_state) in state.outputs:
            if out_suffix == suffix:
                return out_state

        raise Exception(u'Unable to find output state for {} {}'.format(state, suffix))


    def _follow_path(self, root, path_edges):
        morpheme_container = MorphemeContainer(root, self._suffix_graph.get_default_root_state(root), u'')
        for path_edge in path_edges:
            suffix = None
            suffix_form_application_str = None

            if isinstance(path_edge, tuple):
                suffix = path_edge[0]
                suffix_form_application_str = path_edge[1] if len(path_edge) > 1 else u''
            else:
                suffix = path_edge
                suffix_form_application_str = u''

            path_result = morpheme_container.get_surface_so_far() + suffix_form_application_str
            to_state = self._find_to_state(morpheme_container.get_last_state(), suffix)

            morpheme_container = self._add_transition(morpheme_container, suffix_form_application_str, suffix, to_state, path_result)

        return morpheme_container

    def _add_morpheme_container(self, root, path_tuples):
        morpheme_container = self._follow_path(root, path_tuples)

        if not self._morpheme_container_map.has_key(root):
            self._morpheme_container_map[root] = []

        self._morpheme_container_map[root].append(morpheme_container)

    def has_paths(self, lexeme):
        if not self._morpheme_container_map:
            raise Exception(u"Predefined paths are not yet created. Maybe you forgot to run 'create_predefined_paths' ?")

        return self._morpheme_container_map.has_key(lexeme)

    def get_paths(self, lexeme):
        if not self._morpheme_container_map:
            raise Exception("Predefined paths are not yet created. Maybe you forgot to run 'create_predefined_paths' ?")

        return self._morpheme_container_map[lexeme]

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
        self._create_predefined_path_of_herkes()

        self._create_predefined_path_of_question_particles()

        self._create_predefined_path_of_ora()

        self._create_predefined_path_of_bazilari_bazisi()
        self._create_predefined_path_of_kimileri_kimisi_kimi()
        self._create_predefined_path_of_birileri_birisi_biri()
        self._create_predefined_path_of_birbiri()
        self._create_predefined_path_of_cogu_bircogu_coklari_bircoklari()
        self._create_predefined_path_of_birkaci()

    def _create_predefined_path_of_ben(self):
        root_ben = self._find_root(u'ben', SyntacticCategory.PRONOUN, SecondarySyntacticCategory.PERSONAL)
        root_ban = self._find_root(u'ban', SyntacticCategory.PRONOUN, SecondarySyntacticCategory.PERSONAL)

        self._add_morpheme_container(root_ben, [self._suffix_graph.A1Sg_Pron, self._suffix_graph.Pnon_Pron,  self._suffix_graph.Nom_Pron])
        self._add_morpheme_container(root_ben, [self._suffix_graph.A1Sg_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Acc_Pron,    u'i')])
        self._add_morpheme_container(root_ban, [self._suffix_graph.A1Sg_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Dat_Pron,    u'a')])
        self._add_morpheme_container(root_ben, [self._suffix_graph.A1Sg_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Loc_Pron,    u'de')])
        self._add_morpheme_container(root_ben, [self._suffix_graph.A1Sg_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Abl_Pron,    u'den')])
        self._add_morpheme_container(root_ben, [self._suffix_graph.A1Sg_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Ins_Pron,    u'le')])
        self._add_morpheme_container(root_ben, [self._suffix_graph.A1Sg_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Ins_Pron,    u'imle')])
        self._add_morpheme_container(root_ben, [self._suffix_graph.A1Sg_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Gen_Pron,    u'im')])
        self._add_morpheme_container(root_ben, [self._suffix_graph.A1Sg_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.AccordingTo, u'ce')])

        self._add_morpheme_container(root_ben, [self._suffix_graph.A1Sg_Pron, self._suffix_graph.Pnon_Pron, self._suffix_graph.Nom_Pron_Deriv])

    def _create_predefined_path_of_sen(self):
        root_sen = self._find_root(u'sen', SyntacticCategory.PRONOUN, SecondarySyntacticCategory.PERSONAL)
        root_san = self._find_root(u'san', SyntacticCategory.PRONOUN, SecondarySyntacticCategory.PERSONAL)

        self._add_morpheme_container(root_sen, [self._suffix_graph.A2Sg_Pron, self._suffix_graph.Pnon_Pron,  self._suffix_graph.Nom_Pron])
        self._add_morpheme_container(root_sen, [self._suffix_graph.A2Sg_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Acc_Pron,    u'i')])
        self._add_morpheme_container(root_san, [self._suffix_graph.A2Sg_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Dat_Pron,    u'a')])
        self._add_morpheme_container(root_sen, [self._suffix_graph.A2Sg_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Loc_Pron,    u'de')])
        self._add_morpheme_container(root_sen, [self._suffix_graph.A2Sg_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Abl_Pron,    u'den')])
        self._add_morpheme_container(root_sen, [self._suffix_graph.A2Sg_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Ins_Pron,    u'le')])
        self._add_morpheme_container(root_sen, [self._suffix_graph.A2Sg_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Ins_Pron,    u'inle')])
        self._add_morpheme_container(root_sen, [self._suffix_graph.A2Sg_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Gen_Pron,    u'in')])
        self._add_morpheme_container(root_sen, [self._suffix_graph.A2Sg_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.AccordingTo, u'ce')])

        self._add_morpheme_container(root_sen, [self._suffix_graph.A2Sg_Pron, self._suffix_graph.Pnon_Pron, self._suffix_graph.Nom_Pron_Deriv])

    def _create_predefined_path_of_o_pron_pers(self):
        root_o = self._find_root(u'o', SyntacticCategory.PRONOUN, SecondarySyntacticCategory.PERSONAL)

        self._add_morpheme_container(root_o, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.Pnon_Pron,  self._suffix_graph.Nom_Pron])
        self._add_morpheme_container(root_o, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Acc_Pron,    u'nu')])
        self._add_morpheme_container(root_o, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Dat_Pron,    u'na')])
        self._add_morpheme_container(root_o, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Loc_Pron,    u'nda')])
        self._add_morpheme_container(root_o, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Abl_Pron,    u'ndan')])
        self._add_morpheme_container(root_o, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Ins_Pron,    u'nla')])
        self._add_morpheme_container(root_o, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Ins_Pron,    u'nunla')])
        self._add_morpheme_container(root_o, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Gen_Pron,    u'nun')])
        self._add_morpheme_container(root_o, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.AccordingTo, u'nca')])

        self._add_morpheme_container(root_o, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.Pnon_Pron,  self._suffix_graph.Nom_Pron_Deriv])

    def _create_predefined_path_of_biz(self):
        root_biz = self._find_root(u'biz', SyntacticCategory.PRONOUN, SecondarySyntacticCategory.PERSONAL)

        self._add_morpheme_container(root_biz, [self._suffix_graph.A1Pl_Pron, self._suffix_graph.Pnon_Pron,  self._suffix_graph.Nom_Pron])
        self._add_morpheme_container(root_biz, [self._suffix_graph.A1Pl_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Acc_Pron,    u'i')])
        self._add_morpheme_container(root_biz, [self._suffix_graph.A1Pl_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Dat_Pron,    u'e')])
        self._add_morpheme_container(root_biz, [self._suffix_graph.A1Pl_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Loc_Pron,    u'de')])
        self._add_morpheme_container(root_biz, [self._suffix_graph.A1Pl_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Abl_Pron,    u'den')])
        self._add_morpheme_container(root_biz, [self._suffix_graph.A1Pl_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Ins_Pron,    u'le')])
        self._add_morpheme_container(root_biz, [self._suffix_graph.A1Pl_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Ins_Pron,    u'imle')])
        self._add_morpheme_container(root_biz, [self._suffix_graph.A1Pl_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Gen_Pron,    u'im')])
        self._add_morpheme_container(root_biz, [self._suffix_graph.A1Pl_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.AccordingTo, u'ce')])

        self._add_morpheme_container(root_biz, [self._suffix_graph.A1Pl_Pron, self._suffix_graph.Pnon_Pron, self._suffix_graph.Nom_Pron_Deriv])

        self._add_morpheme_container(root_biz, [(self._suffix_graph.A1Pl_Pron, u'ler'), self._suffix_graph.Pnon_Pron,  self._suffix_graph.Nom_Pron])
        self._add_morpheme_container(root_biz, [(self._suffix_graph.A1Pl_Pron, u'ler'), self._suffix_graph.Pnon_Pron, (self._suffix_graph.Acc_Pron,    u'i')])
        self._add_morpheme_container(root_biz, [(self._suffix_graph.A1Pl_Pron, u'ler'), self._suffix_graph.Pnon_Pron, (self._suffix_graph.Dat_Pron,    u'e')])
        self._add_morpheme_container(root_biz, [(self._suffix_graph.A1Pl_Pron, u'ler'), self._suffix_graph.Pnon_Pron, (self._suffix_graph.Loc_Pron,    u'de')])
        self._add_morpheme_container(root_biz, [(self._suffix_graph.A1Pl_Pron, u'ler'), self._suffix_graph.Pnon_Pron, (self._suffix_graph.Abl_Pron,    u'den')])
        self._add_morpheme_container(root_biz, [(self._suffix_graph.A1Pl_Pron, u'ler'), self._suffix_graph.Pnon_Pron, (self._suffix_graph.Ins_Pron,    u'le')])
        self._add_morpheme_container(root_biz, [(self._suffix_graph.A1Pl_Pron, u'ler'), self._suffix_graph.Pnon_Pron, (self._suffix_graph.Gen_Pron,    u'in')])
        self._add_morpheme_container(root_biz, [(self._suffix_graph.A1Pl_Pron, u'ler'), self._suffix_graph.Pnon_Pron, (self._suffix_graph.AccordingTo, u'ce')])

        self._add_morpheme_container(root_biz, [(self._suffix_graph.A1Pl_Pron, u'ler'), self._suffix_graph.Pnon_Pron, self._suffix_graph.Nom_Pron_Deriv])

    def _create_predefined_path_of_siz(self):
        root_siz = self._find_root(u'siz', SyntacticCategory.PRONOUN, SecondarySyntacticCategory.PERSONAL)

        self._add_morpheme_container(root_siz, [self._suffix_graph.A2Pl_Pron, self._suffix_graph.Pnon_Pron,  self._suffix_graph.Nom_Pron])
        self._add_morpheme_container(root_siz, [self._suffix_graph.A2Pl_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Acc_Pron,    u'i')])
        self._add_morpheme_container(root_siz, [self._suffix_graph.A2Pl_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Dat_Pron,    u'e')])
        self._add_morpheme_container(root_siz, [self._suffix_graph.A2Pl_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Loc_Pron,    u'de')])
        self._add_morpheme_container(root_siz, [self._suffix_graph.A2Pl_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Abl_Pron,    u'den')])
        self._add_morpheme_container(root_siz, [self._suffix_graph.A2Pl_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Ins_Pron,    u'le')])
        self._add_morpheme_container(root_siz, [self._suffix_graph.A2Pl_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Ins_Pron,    u'inle')])
        self._add_morpheme_container(root_siz, [self._suffix_graph.A2Pl_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Gen_Pron,    u'in')])
        self._add_morpheme_container(root_siz, [self._suffix_graph.A2Pl_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.AccordingTo, u'ce')])

        self._add_morpheme_container(root_siz, [self._suffix_graph.A2Pl_Pron, self._suffix_graph.Pnon_Pron, self._suffix_graph.Nom_Pron_Deriv])

        self._add_morpheme_container(root_siz, [(self._suffix_graph.A2Pl_Pron, u'ler'), self._suffix_graph.Pnon_Pron,  self._suffix_graph.Nom_Pron])
        self._add_morpheme_container(root_siz, [(self._suffix_graph.A2Pl_Pron, u'ler'), self._suffix_graph.Pnon_Pron, (self._suffix_graph.Acc_Pron,    u'i')])
        self._add_morpheme_container(root_siz, [(self._suffix_graph.A2Pl_Pron, u'ler'), self._suffix_graph.Pnon_Pron, (self._suffix_graph.Dat_Pron,    u'e')])
        self._add_morpheme_container(root_siz, [(self._suffix_graph.A2Pl_Pron, u'ler'), self._suffix_graph.Pnon_Pron, (self._suffix_graph.Loc_Pron,    u'de')])
        self._add_morpheme_container(root_siz, [(self._suffix_graph.A2Pl_Pron, u'ler'), self._suffix_graph.Pnon_Pron, (self._suffix_graph.Abl_Pron,    u'den')])
        self._add_morpheme_container(root_siz, [(self._suffix_graph.A2Pl_Pron, u'ler'), self._suffix_graph.Pnon_Pron, (self._suffix_graph.Ins_Pron,    u'le')])
        self._add_morpheme_container(root_siz, [(self._suffix_graph.A2Pl_Pron, u'ler'), self._suffix_graph.Pnon_Pron, (self._suffix_graph.Gen_Pron,    u'in')])
        self._add_morpheme_container(root_siz, [(self._suffix_graph.A2Pl_Pron, u'ler'), self._suffix_graph.Pnon_Pron, (self._suffix_graph.AccordingTo, u'ce')])

        self._add_morpheme_container(root_siz, [(self._suffix_graph.A2Pl_Pron, u'ler'), self._suffix_graph.Pnon_Pron, self._suffix_graph.Nom_Pron_Deriv])

    def _create_predefined_path_of_onlar_pron_pers(self):
        root_o = self._find_root(u'o', SyntacticCategory.PRONOUN, SecondarySyntacticCategory.PERSONAL)

        self._add_morpheme_container(root_o, [(self._suffix_graph.A3Pl_Pron, 'nlar'), self._suffix_graph.Pnon_Pron,  self._suffix_graph.Nom_Pron])
        self._add_morpheme_container(root_o, [(self._suffix_graph.A3Pl_Pron, 'nlar'), self._suffix_graph.Pnon_Pron, (self._suffix_graph.Acc_Pron,    u'ı')])
        self._add_morpheme_container(root_o, [(self._suffix_graph.A3Pl_Pron, 'nlar'), self._suffix_graph.Pnon_Pron, (self._suffix_graph.Dat_Pron,    u'a')])
        self._add_morpheme_container(root_o, [(self._suffix_graph.A3Pl_Pron, 'nlar'), self._suffix_graph.Pnon_Pron, (self._suffix_graph.Loc_Pron,    u'da')])
        self._add_morpheme_container(root_o, [(self._suffix_graph.A3Pl_Pron, 'nlar'), self._suffix_graph.Pnon_Pron, (self._suffix_graph.Abl_Pron,    u'dan')])
        self._add_morpheme_container(root_o, [(self._suffix_graph.A3Pl_Pron, 'nlar'), self._suffix_graph.Pnon_Pron, (self._suffix_graph.Ins_Pron,    u'la')])
        self._add_morpheme_container(root_o, [(self._suffix_graph.A3Pl_Pron, 'nlar'), self._suffix_graph.Pnon_Pron, (self._suffix_graph.Gen_Pron,    u'ın')])
        self._add_morpheme_container(root_o, [(self._suffix_graph.A3Pl_Pron, 'nlar'), self._suffix_graph.Pnon_Pron, (self._suffix_graph.AccordingTo, u'ca')])

        self._add_morpheme_container(root_o, [(self._suffix_graph.A3Pl_Pron, 'nlar'), self._suffix_graph.Pnon_Pron,  self._suffix_graph.Nom_Pron_Deriv])

    def _create_predefined_path_of_bu_pron_demons(self):
        root_bu = self._find_root(u'bu', SyntacticCategory.PRONOUN, SecondarySyntacticCategory.DEMONSTRATIVE)

        self._add_morpheme_container(root_bu, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.Pnon_Pron,  self._suffix_graph.Nom_Pron])
        self._add_morpheme_container(root_bu, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Acc_Pron, u'nu')])
        self._add_morpheme_container(root_bu, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Dat_Pron, u'na')])
        self._add_morpheme_container(root_bu, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Loc_Pron, u'nda')])
        self._add_morpheme_container(root_bu, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Abl_Pron, u'ndan')])
        self._add_morpheme_container(root_bu, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Ins_Pron, u'nla')])
        self._add_morpheme_container(root_bu, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Ins_Pron, u'nunla')])
        self._add_morpheme_container(root_bu, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Gen_Pron, u'nun')])

        self._add_morpheme_container(root_bu, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.Pnon_Pron,  self._suffix_graph.Nom_Pron_Deriv])

    def _create_predefined_path_of_su_pron_demons(self):
        root_su = self._find_root(u'şu', SyntacticCategory.PRONOUN, SecondarySyntacticCategory.DEMONSTRATIVE)

        self._add_morpheme_container(root_su, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.Pnon_Pron,  self._suffix_graph.Nom_Pron])
        self._add_morpheme_container(root_su, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Acc_Pron, u'nu')])
        self._add_morpheme_container(root_su, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Dat_Pron, u'na')])
        self._add_morpheme_container(root_su, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Loc_Pron, u'nda')])
        self._add_morpheme_container(root_su, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Abl_Pron, u'ndan')])
        self._add_morpheme_container(root_su, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Ins_Pron, u'nla')])
        self._add_morpheme_container(root_su, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Ins_Pron, u'nunla')])
        self._add_morpheme_container(root_su, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Gen_Pron, u'nun')])

        self._add_morpheme_container(root_su, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.Pnon_Pron,  self._suffix_graph.Nom_Pron_Deriv])

    def _create_predefined_path_of_o_pron_demons(self):
        root_o = self._find_root(u'o', SyntacticCategory.PRONOUN, SecondarySyntacticCategory.DEMONSTRATIVE)

        self._add_morpheme_container(root_o, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.Pnon_Pron, self._suffix_graph.Nom_Pron])
        self._add_morpheme_container(root_o, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Acc_Pron, u'nu')])
        self._add_morpheme_container(root_o, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Dat_Pron, u'na')])
        self._add_morpheme_container(root_o, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Loc_Pron, u'nda')])
        self._add_morpheme_container(root_o, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Abl_Pron, u'ndan')])
        self._add_morpheme_container(root_o, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Ins_Pron, u'nla')])
        self._add_morpheme_container(root_o, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Ins_Pron, u'nunla')])
        self._add_morpheme_container(root_o, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.Pnon_Pron, (self._suffix_graph.Gen_Pron, u'nun')])

        self._add_morpheme_container(root_o, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.Pnon_Pron, self._suffix_graph.Nom_Pron_Deriv])

    def _create_predefined_path_of_bunlar_pron_demons(self):
        root_bu = self._find_root(u'bu', SyntacticCategory.PRONOUN, SecondarySyntacticCategory.DEMONSTRATIVE)

        self._add_morpheme_container(root_bu, [(self._suffix_graph.A3Pl_Pron, 'nlar'), self._suffix_graph.Pnon_Pron, self._suffix_graph.Nom_Pron])
        self._add_morpheme_container(root_bu, [(self._suffix_graph.A3Pl_Pron, 'nlar'), self._suffix_graph.Pnon_Pron, (self._suffix_graph.Acc_Pron, u'ı')])
        self._add_morpheme_container(root_bu, [(self._suffix_graph.A3Pl_Pron, 'nlar'), self._suffix_graph.Pnon_Pron, (self._suffix_graph.Dat_Pron, u'a')])
        self._add_morpheme_container(root_bu, [(self._suffix_graph.A3Pl_Pron, 'nlar'), self._suffix_graph.Pnon_Pron, (self._suffix_graph.Loc_Pron, u'da')])
        self._add_morpheme_container(root_bu, [(self._suffix_graph.A3Pl_Pron, 'nlar'), self._suffix_graph.Pnon_Pron, (self._suffix_graph.Abl_Pron, u'dan')])
        self._add_morpheme_container(root_bu, [(self._suffix_graph.A3Pl_Pron, 'nlar'), self._suffix_graph.Pnon_Pron, (self._suffix_graph.Ins_Pron, u'la')])
        self._add_morpheme_container(root_bu, [(self._suffix_graph.A3Pl_Pron, 'nlar'), self._suffix_graph.Pnon_Pron, (self._suffix_graph.Gen_Pron, u'ın')])

        self._add_morpheme_container(root_bu, [(self._suffix_graph.A3Pl_Pron, 'nlar'), self._suffix_graph.Pnon_Pron, self._suffix_graph.Nom_Pron_Deriv])

    def _create_predefined_path_of_sunlar_pron_demons(self):
        root_su = self._find_root(u'şu', SyntacticCategory.PRONOUN, SecondarySyntacticCategory.DEMONSTRATIVE)

        self._add_morpheme_container(root_su, [(self._suffix_graph.A3Pl_Pron, 'nlar'), self._suffix_graph.Pnon_Pron, self._suffix_graph.Nom_Pron])
        self._add_morpheme_container(root_su, [(self._suffix_graph.A3Pl_Pron, 'nlar'), self._suffix_graph.Pnon_Pron, (self._suffix_graph.Acc_Pron, u'ı')])
        self._add_morpheme_container(root_su, [(self._suffix_graph.A3Pl_Pron, 'nlar'), self._suffix_graph.Pnon_Pron, (self._suffix_graph.Dat_Pron, u'a')])
        self._add_morpheme_container(root_su, [(self._suffix_graph.A3Pl_Pron, 'nlar'), self._suffix_graph.Pnon_Pron, (self._suffix_graph.Loc_Pron, u'da')])
        self._add_morpheme_container(root_su, [(self._suffix_graph.A3Pl_Pron, 'nlar'), self._suffix_graph.Pnon_Pron, (self._suffix_graph.Abl_Pron, u'dan')])
        self._add_morpheme_container(root_su, [(self._suffix_graph.A3Pl_Pron, 'nlar'), self._suffix_graph.Pnon_Pron, (self._suffix_graph.Ins_Pron, u'la')])
        self._add_morpheme_container(root_su, [(self._suffix_graph.A3Pl_Pron, 'nlar'), self._suffix_graph.Pnon_Pron, (self._suffix_graph.Gen_Pron, u'ın')])

        self._add_morpheme_container(root_su, [(self._suffix_graph.A3Pl_Pron, 'nlar'), self._suffix_graph.Pnon_Pron, self._suffix_graph.Nom_Pron_Deriv])

    def _create_predefined_path_of_onlar_pron_demons(self):
        root_o = self._find_root(u'o', SyntacticCategory.PRONOUN, SecondarySyntacticCategory.DEMONSTRATIVE)

        self._add_morpheme_container(root_o, [(self._suffix_graph.A3Pl_Pron, 'nlar'), self._suffix_graph.Pnon_Pron, self._suffix_graph.Nom_Pron])
        self._add_morpheme_container(root_o, [(self._suffix_graph.A3Pl_Pron, 'nlar'), self._suffix_graph.Pnon_Pron, (self._suffix_graph.Acc_Pron, u'ı')])
        self._add_morpheme_container(root_o, [(self._suffix_graph.A3Pl_Pron, 'nlar'), self._suffix_graph.Pnon_Pron, (self._suffix_graph.Dat_Pron, u'a')])
        self._add_morpheme_container(root_o, [(self._suffix_graph.A3Pl_Pron, 'nlar'), self._suffix_graph.Pnon_Pron, (self._suffix_graph.Loc_Pron, u'da')])
        self._add_morpheme_container(root_o, [(self._suffix_graph.A3Pl_Pron, 'nlar'), self._suffix_graph.Pnon_Pron, (self._suffix_graph.Abl_Pron, u'dan')])
        self._add_morpheme_container(root_o, [(self._suffix_graph.A3Pl_Pron, 'nlar'), self._suffix_graph.Pnon_Pron, (self._suffix_graph.Ins_Pron, u'la')])
        self._add_morpheme_container(root_o, [(self._suffix_graph.A3Pl_Pron, 'nlar'), self._suffix_graph.Pnon_Pron, (self._suffix_graph.Gen_Pron, u'ın')])

        self._add_morpheme_container(root_o, [(self._suffix_graph.A3Pl_Pron, 'nlar'), self._suffix_graph.Pnon_Pron, self._suffix_graph.Nom_Pron_Deriv])

    def _create_predefined_path_of_kendi(self):
        root_kendi = self._find_root(u'kendi', SyntacticCategory.PRONOUN, SecondarySyntacticCategory.REFLEXIVE)

        ##### A1Sg
        self._add_morpheme_container(root_kendi, [self._suffix_graph.A1Sg_Pron, (self._suffix_graph.P1Sg_Pron,'m'), self._suffix_graph.Nom_Pron])
        self._add_morpheme_container(root_kendi, [self._suffix_graph.A1Sg_Pron, (self._suffix_graph.P1Sg_Pron,'m'), (self._suffix_graph.Acc_Pron, u'i')])
        self._add_morpheme_container(root_kendi, [self._suffix_graph.A1Sg_Pron, (self._suffix_graph.P1Sg_Pron,'m'), (self._suffix_graph.Dat_Pron, u'e')])
        self._add_morpheme_container(root_kendi, [self._suffix_graph.A1Sg_Pron, (self._suffix_graph.P1Sg_Pron,'m'), (self._suffix_graph.Loc_Pron, u'de')])
        self._add_morpheme_container(root_kendi, [self._suffix_graph.A1Sg_Pron, (self._suffix_graph.P1Sg_Pron,'m'), (self._suffix_graph.Abl_Pron, u'den')])
        self._add_morpheme_container(root_kendi, [self._suffix_graph.A1Sg_Pron, (self._suffix_graph.P1Sg_Pron,'m'), (self._suffix_graph.Ins_Pron, u'le')])
        self._add_morpheme_container(root_kendi, [self._suffix_graph.A1Sg_Pron, (self._suffix_graph.P1Sg_Pron,'m'), (self._suffix_graph.Gen_Pron, u'in')])

        self._add_morpheme_container(root_kendi, [self._suffix_graph.A1Sg_Pron, (self._suffix_graph.P1Sg_Pron,'m'), self._suffix_graph.Nom_Pron_Deriv])

        ##### A2Sg
        self._add_morpheme_container(root_kendi, [self._suffix_graph.A2Sg_Pron, (self._suffix_graph.P2Sg_Pron,'n'), self._suffix_graph.Nom_Pron])
        self._add_morpheme_container(root_kendi, [self._suffix_graph.A2Sg_Pron, (self._suffix_graph.P2Sg_Pron,'n'), (self._suffix_graph.Acc_Pron, u'i')])
        self._add_morpheme_container(root_kendi, [self._suffix_graph.A2Sg_Pron, (self._suffix_graph.P2Sg_Pron,'n'), (self._suffix_graph.Dat_Pron, u'e')])
        self._add_morpheme_container(root_kendi, [self._suffix_graph.A2Sg_Pron, (self._suffix_graph.P2Sg_Pron,'n'), (self._suffix_graph.Loc_Pron, u'de')])
        self._add_morpheme_container(root_kendi, [self._suffix_graph.A2Sg_Pron, (self._suffix_graph.P2Sg_Pron,'n'), (self._suffix_graph.Abl_Pron, u'den')])
        self._add_morpheme_container(root_kendi, [self._suffix_graph.A2Sg_Pron, (self._suffix_graph.P2Sg_Pron,'n'), (self._suffix_graph.Ins_Pron, u'le')])
        self._add_morpheme_container(root_kendi, [self._suffix_graph.A2Sg_Pron, (self._suffix_graph.P2Sg_Pron,'n'), (self._suffix_graph.Gen_Pron, u'in')])

        self._add_morpheme_container(root_kendi, [self._suffix_graph.A2Sg_Pron, (self._suffix_graph.P2Sg_Pron,'n'), self._suffix_graph.Nom_Pron_Deriv])

        ##### A3Sg
        self._add_morpheme_container(root_kendi, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.P3Sg_Pron, self._suffix_graph.Nom_Pron])
        self._add_morpheme_container(root_kendi, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.P3Sg_Pron, (self._suffix_graph.Acc_Pron, u'ni')])
        self._add_morpheme_container(root_kendi, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.P3Sg_Pron, (self._suffix_graph.Dat_Pron, u'ne')])
        self._add_morpheme_container(root_kendi, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.P3Sg_Pron, (self._suffix_graph.Loc_Pron, u'nde')])
        self._add_morpheme_container(root_kendi, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.P3Sg_Pron, (self._suffix_graph.Abl_Pron, u'nden')])
        self._add_morpheme_container(root_kendi, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.P3Sg_Pron, (self._suffix_graph.Ins_Pron, u'yle')])
        self._add_morpheme_container(root_kendi, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.P3Sg_Pron, (self._suffix_graph.Gen_Pron, u'nin')])

        self._add_morpheme_container(root_kendi, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.P3Sg_Pron, self._suffix_graph.Nom_Pron_Deriv])

        self._add_morpheme_container(root_kendi, [self._suffix_graph.A3Sg_Pron, (self._suffix_graph.P3Sg_Pron,'si'), self._suffix_graph.Nom_Pron])
        self._add_morpheme_container(root_kendi, [self._suffix_graph.A3Sg_Pron, (self._suffix_graph.P3Sg_Pron,'si'), (self._suffix_graph.Acc_Pron, u'ni')])
        self._add_morpheme_container(root_kendi, [self._suffix_graph.A3Sg_Pron, (self._suffix_graph.P3Sg_Pron,'si'), (self._suffix_graph.Dat_Pron, u'ne')])
        self._add_morpheme_container(root_kendi, [self._suffix_graph.A3Sg_Pron, (self._suffix_graph.P3Sg_Pron,'si'), (self._suffix_graph.Loc_Pron, u'nde')])
        self._add_morpheme_container(root_kendi, [self._suffix_graph.A3Sg_Pron, (self._suffix_graph.P3Sg_Pron,'si'), (self._suffix_graph.Abl_Pron, u'nden')])
        self._add_morpheme_container(root_kendi, [self._suffix_graph.A3Sg_Pron, (self._suffix_graph.P3Sg_Pron,'si'), (self._suffix_graph.Ins_Pron, u'yle')])
        self._add_morpheme_container(root_kendi, [self._suffix_graph.A3Sg_Pron, (self._suffix_graph.P3Sg_Pron,'si'), (self._suffix_graph.Gen_Pron, u'nin')])

        self._add_morpheme_container(root_kendi, [self._suffix_graph.A3Sg_Pron, (self._suffix_graph.P3Sg_Pron,'si'), self._suffix_graph.Nom_Pron_Deriv])


        ##### A1pl
        self._add_morpheme_container(root_kendi, [self._suffix_graph.A1Pl_Pron, (self._suffix_graph.P1Pl_Pron,'miz'), self._suffix_graph.Nom_Pron])
        self._add_morpheme_container(root_kendi, [self._suffix_graph.A1Pl_Pron, (self._suffix_graph.P1Pl_Pron,'miz'), (self._suffix_graph.Acc_Pron, u'i')])
        self._add_morpheme_container(root_kendi, [self._suffix_graph.A1Pl_Pron, (self._suffix_graph.P1Pl_Pron,'miz'), (self._suffix_graph.Dat_Pron, u'e')])
        self._add_morpheme_container(root_kendi, [self._suffix_graph.A1Pl_Pron, (self._suffix_graph.P1Pl_Pron,'miz'), (self._suffix_graph.Loc_Pron, u'de')])
        self._add_morpheme_container(root_kendi, [self._suffix_graph.A1Pl_Pron, (self._suffix_graph.P1Pl_Pron,'miz'), (self._suffix_graph.Abl_Pron, u'den')])
        self._add_morpheme_container(root_kendi, [self._suffix_graph.A1Pl_Pron, (self._suffix_graph.P1Pl_Pron,'miz'), (self._suffix_graph.Ins_Pron, u'le')])
        self._add_morpheme_container(root_kendi, [self._suffix_graph.A1Pl_Pron, (self._suffix_graph.P1Pl_Pron,'miz'), (self._suffix_graph.Gen_Pron, u'in')])

        self._add_morpheme_container(root_kendi, [self._suffix_graph.A1Pl_Pron, (self._suffix_graph.P1Pl_Pron,'miz'), self._suffix_graph.Nom_Pron_Deriv])

        self._add_morpheme_container(root_kendi, [(self._suffix_graph.A1Pl_Pron,'ler'), (self._suffix_graph.P1Pl_Pron,'imiz'), self._suffix_graph.Nom_Pron])
        self._add_morpheme_container(root_kendi, [(self._suffix_graph.A1Pl_Pron,'ler'), (self._suffix_graph.P1Pl_Pron,'imiz'), (self._suffix_graph.Acc_Pron, u'i')])
        self._add_morpheme_container(root_kendi, [(self._suffix_graph.A1Pl_Pron,'ler'), (self._suffix_graph.P1Pl_Pron,'imiz'), (self._suffix_graph.Dat_Pron, u'e')])
        self._add_morpheme_container(root_kendi, [(self._suffix_graph.A1Pl_Pron,'ler'), (self._suffix_graph.P1Pl_Pron,'imiz'), (self._suffix_graph.Loc_Pron, u'de')])
        self._add_morpheme_container(root_kendi, [(self._suffix_graph.A1Pl_Pron,'ler'), (self._suffix_graph.P1Pl_Pron,'imiz'), (self._suffix_graph.Abl_Pron, u'den')])
        self._add_morpheme_container(root_kendi, [(self._suffix_graph.A1Pl_Pron,'ler'), (self._suffix_graph.P1Pl_Pron,'imiz'), (self._suffix_graph.Ins_Pron, u'le')])
        self._add_morpheme_container(root_kendi, [(self._suffix_graph.A1Pl_Pron,'ler'), (self._suffix_graph.P1Pl_Pron,'imiz'), (self._suffix_graph.Gen_Pron, u'in')])

        self._add_morpheme_container(root_kendi, [(self._suffix_graph.A1Pl_Pron,'ler'), (self._suffix_graph.P1Pl_Pron,'imiz'), self._suffix_graph.Nom_Pron_Deriv])

        ##### A2pl
        self._add_morpheme_container(root_kendi, [self._suffix_graph.A2Pl_Pron, (self._suffix_graph.P2Pl_Pron,'niz'), self._suffix_graph.Nom_Pron])
        self._add_morpheme_container(root_kendi, [self._suffix_graph.A2Pl_Pron, (self._suffix_graph.P2Pl_Pron,'niz'), (self._suffix_graph.Acc_Pron, u'i')])
        self._add_morpheme_container(root_kendi, [self._suffix_graph.A2Pl_Pron, (self._suffix_graph.P2Pl_Pron,'niz'), (self._suffix_graph.Dat_Pron, u'e')])
        self._add_morpheme_container(root_kendi, [self._suffix_graph.A2Pl_Pron, (self._suffix_graph.P2Pl_Pron,'niz'), (self._suffix_graph.Loc_Pron, u'de')])
        self._add_morpheme_container(root_kendi, [self._suffix_graph.A2Pl_Pron, (self._suffix_graph.P2Pl_Pron,'niz'), (self._suffix_graph.Abl_Pron, u'den')])
        self._add_morpheme_container(root_kendi, [self._suffix_graph.A2Pl_Pron, (self._suffix_graph.P2Pl_Pron,'niz'), (self._suffix_graph.Ins_Pron, u'le')])
        self._add_morpheme_container(root_kendi, [self._suffix_graph.A2Pl_Pron, (self._suffix_graph.P2Pl_Pron,'niz'), (self._suffix_graph.Gen_Pron, u'in')])

        self._add_morpheme_container(root_kendi, [self._suffix_graph.A2Pl_Pron, (self._suffix_graph.P2Pl_Pron,'niz'), self._suffix_graph.Nom_Pron_Deriv])

        self._add_morpheme_container(root_kendi, [(self._suffix_graph.A2Pl_Pron,'ler'), (self._suffix_graph.P2Pl_Pron,'iniz'), self._suffix_graph.Nom_Pron])
        self._add_morpheme_container(root_kendi, [(self._suffix_graph.A2Pl_Pron,'ler'), (self._suffix_graph.P2Pl_Pron,'iniz'), (self._suffix_graph.Acc_Pron, u'i')])
        self._add_morpheme_container(root_kendi, [(self._suffix_graph.A2Pl_Pron,'ler'), (self._suffix_graph.P2Pl_Pron,'iniz'), (self._suffix_graph.Dat_Pron, u'e')])
        self._add_morpheme_container(root_kendi, [(self._suffix_graph.A2Pl_Pron,'ler'), (self._suffix_graph.P2Pl_Pron,'iniz'), (self._suffix_graph.Loc_Pron, u'de')])
        self._add_morpheme_container(root_kendi, [(self._suffix_graph.A2Pl_Pron,'ler'), (self._suffix_graph.P2Pl_Pron,'iniz'), (self._suffix_graph.Abl_Pron, u'den')])
        self._add_morpheme_container(root_kendi, [(self._suffix_graph.A2Pl_Pron,'ler'), (self._suffix_graph.P2Pl_Pron,'iniz'), (self._suffix_graph.Ins_Pron, u'le')])
        self._add_morpheme_container(root_kendi, [(self._suffix_graph.A2Pl_Pron,'ler'), (self._suffix_graph.P2Pl_Pron,'iniz'), (self._suffix_graph.Gen_Pron, u'in')])

        self._add_morpheme_container(root_kendi, [(self._suffix_graph.A2Pl_Pron,'ler'), (self._suffix_graph.P2Pl_Pron,'iniz'), self._suffix_graph.Nom_Pron_Deriv])

        ##### A3pl
        self._add_morpheme_container(root_kendi, [(self._suffix_graph.A3Pl_Pron,'leri'), self._suffix_graph.P3Pl_Pron, self._suffix_graph.Nom_Pron])
        self._add_morpheme_container(root_kendi, [(self._suffix_graph.A3Pl_Pron,'leri'), self._suffix_graph.P3Pl_Pron, (self._suffix_graph.Acc_Pron, u'ni')])
        self._add_morpheme_container(root_kendi, [(self._suffix_graph.A3Pl_Pron,'leri'), self._suffix_graph.P3Pl_Pron, (self._suffix_graph.Dat_Pron, u'ne')])
        self._add_morpheme_container(root_kendi, [(self._suffix_graph.A3Pl_Pron,'leri'), self._suffix_graph.P3Pl_Pron, (self._suffix_graph.Loc_Pron, u'nde')])
        self._add_morpheme_container(root_kendi, [(self._suffix_graph.A3Pl_Pron,'leri'), self._suffix_graph.P3Pl_Pron, (self._suffix_graph.Abl_Pron, u'nden')])
        self._add_morpheme_container(root_kendi, [(self._suffix_graph.A3Pl_Pron,'leri'), self._suffix_graph.P3Pl_Pron, (self._suffix_graph.Ins_Pron, u'yle')])
        self._add_morpheme_container(root_kendi, [(self._suffix_graph.A3Pl_Pron,'leri'), self._suffix_graph.P3Pl_Pron, (self._suffix_graph.Gen_Pron, u'nin')])

        self._add_morpheme_container(root_kendi, [(self._suffix_graph.A3Pl_Pron,'leri'), self._suffix_graph.P3Pl_Pron, self._suffix_graph.Nom_Pron_Deriv])

    def _create_predefined_path_of_hepsi(self):
        root_hep = self._find_root(u'hep', SyntacticCategory.PRONOUN, None)
        root_hepsi = self._find_root(u'hepsi', SyntacticCategory.PRONOUN, None)

        ##### No A1Sg

        ##### No A2Sg

        ##### No A3Sg

        ##### A1pl
        self._add_morpheme_container(root_hep, [self._suffix_graph.A1Pl_Pron, (self._suffix_graph.P1Pl_Pron,'imiz'), self._suffix_graph.Nom_Pron])
        self._add_morpheme_container(root_hep, [self._suffix_graph.A1Pl_Pron, (self._suffix_graph.P1Pl_Pron,'imiz'), (self._suffix_graph.Acc_Pron,    u'i')])
        self._add_morpheme_container(root_hep, [self._suffix_graph.A1Pl_Pron, (self._suffix_graph.P1Pl_Pron,'imiz'), (self._suffix_graph.Dat_Pron,    u'e')])
        self._add_morpheme_container(root_hep, [self._suffix_graph.A1Pl_Pron, (self._suffix_graph.P1Pl_Pron,'imiz'), (self._suffix_graph.Loc_Pron,    u'de')])
        self._add_morpheme_container(root_hep, [self._suffix_graph.A1Pl_Pron, (self._suffix_graph.P1Pl_Pron,'imiz'), (self._suffix_graph.Abl_Pron,    u'den')])
        self._add_morpheme_container(root_hep, [self._suffix_graph.A1Pl_Pron, (self._suffix_graph.P1Pl_Pron,'imiz'), (self._suffix_graph.Ins_Pron,    u'le')])
        self._add_morpheme_container(root_hep, [self._suffix_graph.A1Pl_Pron, (self._suffix_graph.P1Pl_Pron,'imiz'), (self._suffix_graph.Gen_Pron,    u'in')])
        self._add_morpheme_container(root_hep, [self._suffix_graph.A1Pl_Pron, (self._suffix_graph.P1Pl_Pron,'imiz'), (self._suffix_graph.AccordingTo, u'ce')])

        self._add_morpheme_container(root_hep, [self._suffix_graph.A1Pl_Pron, (self._suffix_graph.P1Pl_Pron,'imiz'), self._suffix_graph.Nom_Pron_Deriv])

        ##### A2pl
        self._add_morpheme_container(root_hep, [self._suffix_graph.A2Pl_Pron, (self._suffix_graph.P2Pl_Pron,'iniz'), self._suffix_graph.Nom_Pron])
        self._add_morpheme_container(root_hep, [self._suffix_graph.A2Pl_Pron, (self._suffix_graph.P2Pl_Pron,'iniz'), (self._suffix_graph.Acc_Pron,    u'i')])
        self._add_morpheme_container(root_hep, [self._suffix_graph.A2Pl_Pron, (self._suffix_graph.P2Pl_Pron,'iniz'), (self._suffix_graph.Dat_Pron,    u'e')])
        self._add_morpheme_container(root_hep, [self._suffix_graph.A2Pl_Pron, (self._suffix_graph.P2Pl_Pron,'iniz'), (self._suffix_graph.Loc_Pron,    u'de')])
        self._add_morpheme_container(root_hep, [self._suffix_graph.A2Pl_Pron, (self._suffix_graph.P2Pl_Pron,'iniz'), (self._suffix_graph.Abl_Pron,    u'den')])
        self._add_morpheme_container(root_hep, [self._suffix_graph.A2Pl_Pron, (self._suffix_graph.P2Pl_Pron,'iniz'), (self._suffix_graph.Ins_Pron,    u'le')])
        self._add_morpheme_container(root_hep, [self._suffix_graph.A2Pl_Pron, (self._suffix_graph.P2Pl_Pron,'iniz'), (self._suffix_graph.Gen_Pron,    u'in')])
        self._add_morpheme_container(root_hep, [self._suffix_graph.A2Pl_Pron, (self._suffix_graph.P2Pl_Pron,'iniz'), (self._suffix_graph.AccordingTo, u'ce')])

        self._add_morpheme_container(root_hep, [self._suffix_graph.A2Pl_Pron, (self._suffix_graph.P2Pl_Pron,'iniz'), self._suffix_graph.Nom_Pron_Deriv])

        ##### A3pl

        self._add_morpheme_container(root_hepsi, [self._suffix_graph.A3Pl_Pron, self._suffix_graph.P3Pl_Pron, self._suffix_graph.Nom_Pron])
        self._add_morpheme_container(root_hepsi, [self._suffix_graph.A3Pl_Pron, self._suffix_graph.P3Pl_Pron, (self._suffix_graph.Acc_Pron,    u'ni')])
        self._add_morpheme_container(root_hepsi, [self._suffix_graph.A3Pl_Pron, self._suffix_graph.P3Pl_Pron, (self._suffix_graph.Dat_Pron,    u'ne')])
        self._add_morpheme_container(root_hepsi, [self._suffix_graph.A3Pl_Pron, self._suffix_graph.P3Pl_Pron, (self._suffix_graph.Loc_Pron,    u'nde')])
        self._add_morpheme_container(root_hepsi, [self._suffix_graph.A3Pl_Pron, self._suffix_graph.P3Pl_Pron, (self._suffix_graph.Abl_Pron,    u'nden')])
        self._add_morpheme_container(root_hepsi, [self._suffix_graph.A3Pl_Pron, self._suffix_graph.P3Pl_Pron, (self._suffix_graph.Ins_Pron,    u'yle')])
        self._add_morpheme_container(root_hepsi, [self._suffix_graph.A3Pl_Pron, self._suffix_graph.P3Pl_Pron, (self._suffix_graph.Gen_Pron,    u'nin')])
        self._add_morpheme_container(root_hepsi, [self._suffix_graph.A3Pl_Pron, self._suffix_graph.P3Pl_Pron, (self._suffix_graph.AccordingTo, u'nce')])

        self._add_morpheme_container(root_hepsi, [self._suffix_graph.A3Pl_Pron, self._suffix_graph.P3Pl_Pron, self._suffix_graph.Nom_Pron_Deriv])

    def _create_predefined_path_of_herkes(self):
        root_herkes = self._find_root(u'herkes', SyntacticCategory.PRONOUN, None)

        self._add_morpheme_container(root_herkes, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.Pnon_Pron])

    def _create_predefined_path_of_question_particles(self):
        root_mii = self._find_root(u'mı', SyntacticCategory.QUESTION, None)
        root_mi  = self._find_root(u'mi', SyntacticCategory.QUESTION, None)
        root_mu  = self._find_root(u'mu', SyntacticCategory.QUESTION, None)
        root_muu = self._find_root(u'mü', SyntacticCategory.QUESTION, None)

        ##### Pres
        self._add_morpheme_container(root_mii, [self._suffix_graph.Pres_Ques, (self._suffix_graph.A1Sg_Ques,u'yım')])
        self._add_morpheme_container(root_mii, [self._suffix_graph.Pres_Ques, (self._suffix_graph.A2Sg_Ques,u'sın')])
        self._add_morpheme_container(root_mii, [self._suffix_graph.Pres_Ques, (self._suffix_graph.A3Sg_Ques,u'')])
        self._add_morpheme_container(root_mii, [self._suffix_graph.Pres_Ques, (self._suffix_graph.A1Pl_Ques,u'yız')])
        self._add_morpheme_container(root_mii, [self._suffix_graph.Pres_Ques, (self._suffix_graph.A2Pl_Ques,u'sınız')])
        self._add_morpheme_container(root_mii, [self._suffix_graph.Pres_Ques, (self._suffix_graph.A3Pl_Ques,u'lar')])

        self._add_morpheme_container(root_mi , [self._suffix_graph.Pres_Ques, (self._suffix_graph.A1Sg_Ques,u'yim')])
        self._add_morpheme_container(root_mi , [self._suffix_graph.Pres_Ques, (self._suffix_graph.A2Sg_Ques,u'sin')])
        self._add_morpheme_container(root_mi , [self._suffix_graph.Pres_Ques, (self._suffix_graph.A3Sg_Ques,u'')])
        self._add_morpheme_container(root_mi , [self._suffix_graph.Pres_Ques, (self._suffix_graph.A1Pl_Ques,u'yiz')])
        self._add_morpheme_container(root_mi , [self._suffix_graph.Pres_Ques, (self._suffix_graph.A2Pl_Ques,u'siniz')])
        self._add_morpheme_container(root_mi , [self._suffix_graph.Pres_Ques, (self._suffix_graph.A3Pl_Ques,u'ler')])

        self._add_morpheme_container(root_mu , [self._suffix_graph.Pres_Ques, (self._suffix_graph.A1Sg_Ques,u'yum')])
        self._add_morpheme_container(root_mu , [self._suffix_graph.Pres_Ques, (self._suffix_graph.A2Sg_Ques,u'sun')])
        self._add_morpheme_container(root_mu , [self._suffix_graph.Pres_Ques, (self._suffix_graph.A3Sg_Ques,u'')])
        self._add_morpheme_container(root_mu , [self._suffix_graph.Pres_Ques, (self._suffix_graph.A1Pl_Ques,u'yuz')])
        self._add_morpheme_container(root_mu , [self._suffix_graph.Pres_Ques, (self._suffix_graph.A2Pl_Ques,u'sunuz')])
        self._add_morpheme_container(root_mu , [self._suffix_graph.Pres_Ques, (self._suffix_graph.A3Pl_Ques,u'lar')])

        self._add_morpheme_container(root_muu, [self._suffix_graph.Pres_Ques, (self._suffix_graph.A1Sg_Ques,u'yüm')])
        self._add_morpheme_container(root_muu, [self._suffix_graph.Pres_Ques, (self._suffix_graph.A2Sg_Ques,u'sün')])
        self._add_morpheme_container(root_muu, [self._suffix_graph.Pres_Ques, (self._suffix_graph.A3Sg_Ques,u'')])
        self._add_morpheme_container(root_muu, [self._suffix_graph.Pres_Ques, (self._suffix_graph.A1Pl_Ques,u'yüz')])
        self._add_morpheme_container(root_muu, [self._suffix_graph.Pres_Ques, (self._suffix_graph.A2Pl_Ques,u'sünüz')])
        self._add_morpheme_container(root_muu, [self._suffix_graph.Pres_Ques, (self._suffix_graph.A3Pl_Ques,u'ler')])

        ##### Past
        self._add_morpheme_container(root_mii, [(self._suffix_graph.Past_Ques,u'ydı'), (self._suffix_graph.A1Sg_Ques,u'm')])
        self._add_morpheme_container(root_mii, [(self._suffix_graph.Past_Ques,u'ydı'), (self._suffix_graph.A2Sg_Ques,u'n')])
        self._add_morpheme_container(root_mii, [(self._suffix_graph.Past_Ques,u'ydı'), (self._suffix_graph.A3Sg_Ques,u'')])
        self._add_morpheme_container(root_mii, [(self._suffix_graph.Past_Ques,u'ydı'), (self._suffix_graph.A1Pl_Ques,u'k')])
        self._add_morpheme_container(root_mii, [(self._suffix_graph.Past_Ques,u'ydı'), (self._suffix_graph.A2Pl_Ques,u'nız')])
        self._add_morpheme_container(root_mii, [(self._suffix_graph.Past_Ques,u'ydı'), (self._suffix_graph.A3Pl_Ques,u'lar')])

        self._add_morpheme_container(root_mi , [(self._suffix_graph.Past_Ques,u'ydi'), (self._suffix_graph.A1Sg_Ques,u'm')])
        self._add_morpheme_container(root_mi , [(self._suffix_graph.Past_Ques,u'ydi'), (self._suffix_graph.A2Sg_Ques,u'n')])
        self._add_morpheme_container(root_mi , [(self._suffix_graph.Past_Ques,u'ydi'), (self._suffix_graph.A3Sg_Ques,u'')])
        self._add_morpheme_container(root_mi , [(self._suffix_graph.Past_Ques,u'ydi'), (self._suffix_graph.A1Pl_Ques,u'k')])
        self._add_morpheme_container(root_mi , [(self._suffix_graph.Past_Ques,u'ydi'), (self._suffix_graph.A2Pl_Ques,u'niz')])
        self._add_morpheme_container(root_mi , [(self._suffix_graph.Past_Ques,u'ydi'), (self._suffix_graph.A3Pl_Ques,u'ler')])

        self._add_morpheme_container(root_mu , [(self._suffix_graph.Past_Ques,u'ydu'), (self._suffix_graph.A1Sg_Ques,u'm')])
        self._add_morpheme_container(root_mu , [(self._suffix_graph.Past_Ques,u'ydu'), (self._suffix_graph.A2Sg_Ques,u'n')])
        self._add_morpheme_container(root_mu , [(self._suffix_graph.Past_Ques,u'ydu'), (self._suffix_graph.A3Sg_Ques,u'')])
        self._add_morpheme_container(root_mu , [(self._suffix_graph.Past_Ques,u'ydu'), (self._suffix_graph.A1Pl_Ques,u'k')])
        self._add_morpheme_container(root_mu , [(self._suffix_graph.Past_Ques,u'ydu'), (self._suffix_graph.A2Pl_Ques,u'nuz')])
        self._add_morpheme_container(root_mu , [(self._suffix_graph.Past_Ques,u'ydu'), (self._suffix_graph.A3Pl_Ques,u'lar')])

        self._add_morpheme_container(root_muu, [(self._suffix_graph.Past_Ques,u'ydü'), (self._suffix_graph.A1Sg_Ques,u'm')])
        self._add_morpheme_container(root_muu, [(self._suffix_graph.Past_Ques,u'ydü'), (self._suffix_graph.A2Sg_Ques,u'n')])
        self._add_morpheme_container(root_muu, [(self._suffix_graph.Past_Ques,u'ydü'), (self._suffix_graph.A3Sg_Ques,u'')])
        self._add_morpheme_container(root_muu, [(self._suffix_graph.Past_Ques,u'ydü'), (self._suffix_graph.A1Pl_Ques,u'k')])
        self._add_morpheme_container(root_muu, [(self._suffix_graph.Past_Ques,u'ydü'), (self._suffix_graph.A2Pl_Ques,u'nüz')])
        self._add_morpheme_container(root_muu, [(self._suffix_graph.Past_Ques,u'ydü'), (self._suffix_graph.A3Pl_Ques,u'ler')])

        ##### Narr
        self._add_morpheme_container(root_mii, [(self._suffix_graph.Past_Ques,u'ymış'), (self._suffix_graph.A1Sg_Ques,u'ım')])
        self._add_morpheme_container(root_mii, [(self._suffix_graph.Past_Ques,u'ymış'), (self._suffix_graph.A2Sg_Ques,u'sın')])
        self._add_morpheme_container(root_mii, [(self._suffix_graph.Past_Ques,u'ymış'), (self._suffix_graph.A3Sg_Ques,u'')])
        self._add_morpheme_container(root_mii, [(self._suffix_graph.Past_Ques,u'ymış'), (self._suffix_graph.A1Pl_Ques,u'ız')])
        self._add_morpheme_container(root_mii, [(self._suffix_graph.Past_Ques,u'ymış'), (self._suffix_graph.A2Pl_Ques,u'sınız')])
        self._add_morpheme_container(root_mii, [(self._suffix_graph.Past_Ques,u'ymış'), (self._suffix_graph.A3Pl_Ques,u'lar')])

        self._add_morpheme_container(root_mi , [(self._suffix_graph.Past_Ques,u'ymiş'), (self._suffix_graph.A1Sg_Ques,u'im')])
        self._add_morpheme_container(root_mi , [(self._suffix_graph.Past_Ques,u'ymiş'), (self._suffix_graph.A2Sg_Ques,u'sin')])
        self._add_morpheme_container(root_mi , [(self._suffix_graph.Past_Ques,u'ymiş'), (self._suffix_graph.A3Sg_Ques,u'')])
        self._add_morpheme_container(root_mi , [(self._suffix_graph.Past_Ques,u'ymiş'), (self._suffix_graph.A1Pl_Ques,u'iz')])
        self._add_morpheme_container(root_mi , [(self._suffix_graph.Past_Ques,u'ymiş'), (self._suffix_graph.A2Pl_Ques,u'siniz')])
        self._add_morpheme_container(root_mi , [(self._suffix_graph.Past_Ques,u'ymiş'), (self._suffix_graph.A3Pl_Ques,u'ler')])

        self._add_morpheme_container(root_mu , [(self._suffix_graph.Past_Ques,u'ymuş'), (self._suffix_graph.A1Sg_Ques,u'um')])
        self._add_morpheme_container(root_mu , [(self._suffix_graph.Past_Ques,u'ymuş'), (self._suffix_graph.A2Sg_Ques,u'sun')])
        self._add_morpheme_container(root_mu , [(self._suffix_graph.Past_Ques,u'ymuş'), (self._suffix_graph.A3Sg_Ques,u'')])
        self._add_morpheme_container(root_mu , [(self._suffix_graph.Past_Ques,u'ymuş'), (self._suffix_graph.A1Pl_Ques,u'uz')])
        self._add_morpheme_container(root_mu , [(self._suffix_graph.Past_Ques,u'ymuş'), (self._suffix_graph.A2Pl_Ques,u'sunuz')])
        self._add_morpheme_container(root_mu , [(self._suffix_graph.Past_Ques,u'ymuş'), (self._suffix_graph.A3Pl_Ques,u'lar')])

        self._add_morpheme_container(root_muu, [(self._suffix_graph.Past_Ques,u'ymüş'), (self._suffix_graph.A1Sg_Ques,u'üm')])
        self._add_morpheme_container(root_muu, [(self._suffix_graph.Past_Ques,u'ymüş'), (self._suffix_graph.A2Sg_Ques,u'sün')])
        self._add_morpheme_container(root_muu, [(self._suffix_graph.Past_Ques,u'ymüş'), (self._suffix_graph.A3Sg_Ques,u'')])
        self._add_morpheme_container(root_muu, [(self._suffix_graph.Past_Ques,u'ymüş'), (self._suffix_graph.A1Pl_Ques,u'üz')])
        self._add_morpheme_container(root_muu, [(self._suffix_graph.Past_Ques,u'ymüş'), (self._suffix_graph.A2Pl_Ques,u'sünüz')])
        self._add_morpheme_container(root_muu, [(self._suffix_graph.Past_Ques,u'ymüş'), (self._suffix_graph.A3Pl_Ques,u'ler')])

    def _create_predefined_path_of_ora(self):
        root_or = self._find_root(u'or', SyntacticCategory.NOUN, None)

        # define predefined paths for "orda" and "ordan"

        self._add_morpheme_container(root_or, [self._suffix_graph.A3Sg_Noun, self._suffix_graph.Pnon_Noun, (self._suffix_graph.Loc_Noun,'da')])
        self._add_morpheme_container(root_or, [self._suffix_graph.A3Sg_Noun, self._suffix_graph.Pnon_Noun, (self._suffix_graph.Abl_Noun,'dan')])

    def _create_predefined_path_of_bazilari_bazisi(self):
        root_bazisi = self._find_root(u'bazısı', SyntacticCategory.PRONOUN, None)
        root_bazilari = self._find_root(u'bazıları', SyntacticCategory.PRONOUN, None)

        self._add_morpheme_container(root_bazilari, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.P3Sg_Pron])
        self._add_morpheme_container(root_bazilari, [self._suffix_graph.A3Sg_Pron, (self._suffix_graph.P1Pl_Pron, u'mız')])
        self._add_morpheme_container(root_bazilari, [self._suffix_graph.A3Sg_Pron, (self._suffix_graph.P2Pl_Pron, u'nız')])

        self._add_morpheme_container(root_bazisi,   [self._suffix_graph.A3Sg_Pron, self._suffix_graph.P3Sg_Pron])

    def _create_predefined_path_of_kimileri_kimisi_kimi(self):
        root_kimi   = self._find_root(u'kimi',   SyntacticCategory.PRONOUN, None)
        root_kimisi = self._find_root(u'kimisi', SyntacticCategory.PRONOUN, None)
        root_kimileri = self._find_root(u'kimileri', SyntacticCategory.PRONOUN, None)

        self._add_morpheme_container(root_kimileri, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.P3Sg_Pron])
        self._add_morpheme_container(root_kimileri, [self._suffix_graph.A3Sg_Pron, (self._suffix_graph.P1Pl_Pron, u'miz')])
        self._add_morpheme_container(root_kimileri, [self._suffix_graph.A3Sg_Pron, (self._suffix_graph.P2Pl_Pron, u'niz')])

        self._add_morpheme_container(root_kimi, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.P3Sg_Pron])
        self._add_morpheme_container(root_kimi, [self._suffix_graph.A3Sg_Pron, (self._suffix_graph.P1Pl_Pron, u'miz')])
        self._add_morpheme_container(root_kimi, [self._suffix_graph.A3Sg_Pron, (self._suffix_graph.P2Pl_Pron, u'niz')])

        self._add_morpheme_container(root_kimisi, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.P3Sg_Pron])

    def _create_predefined_path_of_birileri_birisi_biri(self):
        root_biri   = self._find_root(u'biri',   SyntacticCategory.PRONOUN, None)
        root_birisi = self._find_root(u'birisi', SyntacticCategory.PRONOUN, None)
        root_birileri = self._find_root(u'birileri', SyntacticCategory.PRONOUN, None)

        self._add_morpheme_container(root_birileri, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.P3Sg_Pron])
        self._add_morpheme_container(root_birileri, [self._suffix_graph.A3Sg_Pron, (self._suffix_graph.P1Pl_Pron, u'miz')])
        self._add_morpheme_container(root_birileri, [self._suffix_graph.A3Sg_Pron, (self._suffix_graph.P2Pl_Pron, u'niz')])

        self._add_morpheme_container(root_biri,   [self._suffix_graph.A3Sg_Pron, self._suffix_graph.P3Sg_Pron])
        self._add_morpheme_container(root_biri,   [self._suffix_graph.A3Sg_Pron, (self._suffix_graph.P1Pl_Pron, u'miz')])
        self._add_morpheme_container(root_biri,   [self._suffix_graph.A3Sg_Pron, (self._suffix_graph.P2Pl_Pron, u'niz')])

        self._add_morpheme_container(root_birisi, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.P3Sg_Pron])

    def _create_predefined_path_of_birbiri(self):
        root_birbir    = self._find_root(u'birbir',    SyntacticCategory.PRONOUN, None)
        root_birbiri   = self._find_root(u'birbiri',   SyntacticCategory.PRONOUN, None)

        self._add_morpheme_container(root_birbiri, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.P3Sg_Pron])
        self._add_morpheme_container(root_birbiri, [self._suffix_graph.A1Pl_Pron, (self._suffix_graph.P1Pl_Pron, u'miz')])
        self._add_morpheme_container(root_birbiri, [self._suffix_graph.A2Pl_Pron, (self._suffix_graph.P2Pl_Pron, u'niz')])

        self._add_morpheme_container(root_birbir,  [self._suffix_graph.A3Pl_Pron, (self._suffix_graph.P3Pl_Pron, u'leri')])

    def _create_predefined_path_of_cogu_bircogu_coklari_bircoklari(self):
        root_cogu       = self._find_root(u'çoğu',        SyntacticCategory.PRONOUN, None)
        root_bircogu    = self._find_root(u'birçoğu',     SyntacticCategory.PRONOUN, None)
        root_coklari    = self._find_root(u'çokları',     SyntacticCategory.PRONOUN, None)
        root_bircoklari = self._find_root(u'birçokları',  SyntacticCategory.PRONOUN, None)

        self._add_morpheme_container(root_cogu, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.P3Sg_Pron])
        self._add_morpheme_container(root_cogu, [self._suffix_graph.A3Sg_Pron, (self._suffix_graph.P1Pl_Pron, u'muz')])
        self._add_morpheme_container(root_cogu, [self._suffix_graph.A3Sg_Pron, (self._suffix_graph.P2Pl_Pron, u'nuz')])

        self._add_morpheme_container(root_bircogu, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.P3Sg_Pron])
        self._add_morpheme_container(root_bircogu, [self._suffix_graph.A3Sg_Pron, (self._suffix_graph.P1Pl_Pron, u'muz')])
        self._add_morpheme_container(root_bircogu, [self._suffix_graph.A3Sg_Pron, (self._suffix_graph.P2Pl_Pron, u'nuz')])

        self._add_morpheme_container(root_coklari, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.P3Pl_Pron])

        self._add_morpheme_container(root_bircoklari, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.P3Pl_Pron])

    def _create_predefined_path_of_birkaci(self):
        root_birkaci = self._find_root(u'birkaçı', SyntacticCategory.PRONOUN, None)

        self._add_morpheme_container(root_birkaci, [self._suffix_graph.A3Sg_Pron, self._suffix_graph.P3Sg_Pron])
        self._add_morpheme_container(root_birkaci, [self._suffix_graph.A3Sg_Pron, (self._suffix_graph.P1Pl_Pron, u'mız')])
        self._add_morpheme_container(root_birkaci, [self._suffix_graph.A3Sg_Pron, (self._suffix_graph.P2Pl_Pron, u'nız')])

