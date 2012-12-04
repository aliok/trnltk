# coding=utf-8
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
from trnltk.morphology.model.lexeme import SecondarySyntacticCategory, SyntacticCategory
from trnltk.morphology.contextless.parser.suffixapplier import *
from trnltk.morphology.model.morpheme import SuffixForm
from trnltk.morphology.model.morphemecontainer import MorphemeContainer

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

        return None

    def _discover_intermediate_state_and_suffix(self, state, suffix):
        # go only one level
        found_state = None
        found_suffix = None
        for (out_suffix, out_state) in state.outputs:
            for (deep_out_suffix, deep_out_state) in out_state.outputs:
                if deep_out_suffix == suffix:
                    if found_state:
                        raise Exception(u'Output state not found for {} {}. Tried states that are accessible, but found two states :{}, {}'.format(state, suffix, found_state, deep_out_state))
                    else:
                        found_state = out_state
                        found_suffix = out_suffix

        return found_state, found_suffix


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

            surface_so_far = morpheme_container.get_surface_so_far()
            path_result = surface_so_far + suffix_form_application_str
            to_state = self._find_to_state(morpheme_container.get_last_state(), suffix)
            if not to_state:
                intermediate_state, intermediate_suffix = self._discover_intermediate_state_and_suffix(morpheme_container.get_last_state(), suffix)
                if not intermediate_state:
                    raise Exception(u'Also tried to discover intermediate states, but unable to find output state for {} {}'.format(to_state, suffix))
                morpheme_container = self._add_transition(morpheme_container, u'', intermediate_suffix, intermediate_state, surface_so_far)
                to_state = self._find_to_state(morpheme_container.get_last_state(), suffix)
                if not to_state:
                    raise Exception(u'Unable to find output state which has been suggested by intermediate state before, for {} {}'.format(to_state, suffix))
                morpheme_container = self._add_transition(morpheme_container, suffix_form_application_str, suffix, to_state, path_result)
            else:
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
        self._create_predefined_path_of_di()
        self._create_predefined_path_of_yi()

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
        self._create_predefined_path_of_ne()

        self._create_predefined_path_of_ora_bura_sura_nere()

        self._create_predefined_path_of_iceri_disari()

        self._create_predefined_path_of_bazilari_bazisi()
        self._create_predefined_path_of_kimileri_kimisi_kimi()
        self._create_predefined_path_of_birileri_birisi_biri()
        self._create_predefined_path_of_hicbirisi_hicbiri()
        self._create_predefined_path_of_birbiri()
        self._create_predefined_path_of_cogu_bircogu_coklari_bircoklari()
        self._create_predefined_path_of_birkaci()
        self._create_predefined_path_of_cumlesi()
        self._create_predefined_path_of_digeri_digerleri()

    def _create_predefined_path_of_di(self):
        root_di = self._find_root(u'di', SyntacticCategory.VERB, None)

        Positive = self._suffix_graph.get_suffix(u'Pos')
        Negative = self._suffix_graph.get_suffix(u'Neg')

        self._add_morpheme_container(root_di, [Positive, (self._suffix_graph.get_suffix(u'Fut'), u'yecek')])
        self._add_morpheme_container(root_di, [Positive, (self._suffix_graph.get_suffix(u'Fut'), u'yeceğ')])
        self._add_morpheme_container(root_di, [Positive, (self._suffix_graph.get_suffix(u'Future_to_Adj'), u'yecek')])
        self._add_morpheme_container(root_di, [Positive, (self._suffix_graph.get_suffix(u'Future_to_Adj'), u'yeceğ')])
        self._add_morpheme_container(root_di, [Positive, (self._suffix_graph.get_suffix(u'FutPart_Noun'), u'yecek')])
        self._add_morpheme_container(root_di, [Positive, (self._suffix_graph.get_suffix(u'FutPart_Noun'), u'yeceğ')])
        self._add_morpheme_container(root_di, [Positive, (self._suffix_graph.get_suffix(u'FutPart_Adj'), u'yecek')])
        self._add_morpheme_container(root_di, [Positive, (self._suffix_graph.get_suffix(u'FutPart_Adj'), u'yeceğ')])

        self._add_morpheme_container(root_di, [Positive, (self._suffix_graph.get_suffix(u'Prog'), u'yor')])

        self._add_morpheme_container(root_di, [Positive, (self._suffix_graph.get_suffix(u'PresPart'), u'yen')])

        self._add_morpheme_container(root_di, [(self._suffix_graph.get_suffix(u'Able'), u'yebil'), Positive])
        self._add_morpheme_container(root_di, [(self._suffix_graph.get_suffix(u'Able'), u'ye'), (Negative, "me")])

        self._add_morpheme_container(root_di, [Positive, (self._suffix_graph.get_suffix(u'Opt'), u'ye')])

        self._add_morpheme_container(root_di, [Positive, (self._suffix_graph.get_suffix(u'ByDoingSo'), u'yerek')])


    def _create_predefined_path_of_yi(self):
        root_yi = self._find_root(u'yi', SyntacticCategory.VERB, None)

        Positive = self._suffix_graph.get_suffix(u'Pos')
        Negative = self._suffix_graph.get_suffix(u'Neg')

        self._add_morpheme_container(root_yi, [Positive, (self._suffix_graph.get_suffix(u'Fut'), u'yecek')])
        self._add_morpheme_container(root_yi, [Positive, (self._suffix_graph.get_suffix(u'Fut'), u'yeceğ')])
        self._add_morpheme_container(root_yi, [Positive, (self._suffix_graph.get_suffix(u'Future_to_Adj'), u'yecek')])
        self._add_morpheme_container(root_yi, [Positive, (self._suffix_graph.get_suffix(u'Future_to_Adj'), u'yeceğ')])
        self._add_morpheme_container(root_yi, [Positive, (self._suffix_graph.get_suffix(u'FutPart_Noun'), u'yecek')])
        self._add_morpheme_container(root_yi, [Positive, (self._suffix_graph.get_suffix(u'FutPart_Noun'), u'yeceğ')])
        self._add_morpheme_container(root_yi, [Positive, (self._suffix_graph.get_suffix(u'FutPart_Adj'), u'yecek')])
        self._add_morpheme_container(root_yi, [Positive, (self._suffix_graph.get_suffix(u'FutPart_Adj'), u'yeceğ')])

        self._add_morpheme_container(root_yi, [Positive, (self._suffix_graph.get_suffix(u'Prog'), u'yor')])

        self._add_morpheme_container(root_yi, [Positive, (self._suffix_graph.get_suffix(u'PresPart'), u'yen')])

        self._add_morpheme_container(root_yi, [(self._suffix_graph.get_suffix(u'Able'), u'yebil'), Positive])
        self._add_morpheme_container(root_yi, [(self._suffix_graph.get_suffix(u'Able'), u'ye'), (Negative, "me")])

        self._add_morpheme_container(root_yi, [Positive, (self._suffix_graph.get_suffix(u'Opt'), u'ye')])

        self._add_morpheme_container(root_yi, [Positive, (self._suffix_graph.get_suffix(u'ByDoingSo'), u'yerek')])

        # different from "demek"
        self._add_morpheme_container(root_yi, [Positive, (self._suffix_graph.get_suffix(u'AfterDoingSo'), u'yip')])

    def _create_predefined_path_of_ben(self):
        root_ben = self._find_root(u'ben', SyntacticCategory.PRONOUN, SecondarySyntacticCategory.PERSONAL)
        root_ban = self._find_root(u'ban', SyntacticCategory.PRONOUN, SecondarySyntacticCategory.PERSONAL)

        A1Sg_Pron = self._suffix_graph.get_suffix(u'A1Sg_Pron')
        Pnon_Pron = self._suffix_graph.get_suffix(u'Pnon_Pron')

        self._add_morpheme_container(root_ben, [A1Sg_Pron, Pnon_Pron,  self._suffix_graph.get_suffix(u'Nom_Pron')])
        self._add_morpheme_container(root_ben, [A1Sg_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Acc_Pron'),    u'i')])
        self._add_morpheme_container(root_ban, [A1Sg_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Dat_Pron'),    u'a')])
        self._add_morpheme_container(root_ben, [A1Sg_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Loc_Pron'),    u'de')])
        self._add_morpheme_container(root_ben, [A1Sg_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Abl_Pron'),    u'den')])
        self._add_morpheme_container(root_ben, [A1Sg_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Ins_Pron'),    u'le')])
        self._add_morpheme_container(root_ben, [A1Sg_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Ins_Pron'),    u'imle')])
        self._add_morpheme_container(root_ben, [A1Sg_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Gen_Pron'),    u'im')])
        self._add_morpheme_container(root_ben, [A1Sg_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'AccordingTo'), u'ce')])

        self._add_morpheme_container(root_ben, [A1Sg_Pron, Pnon_Pron, self._suffix_graph.get_suffix(u'Nom_Pron_Deriv')])

    def _create_predefined_path_of_sen(self):
        root_sen = self._find_root(u'sen', SyntacticCategory.PRONOUN, SecondarySyntacticCategory.PERSONAL)
        root_san = self._find_root(u'san', SyntacticCategory.PRONOUN, SecondarySyntacticCategory.PERSONAL)

        A2Sg_Pron = self._suffix_graph.get_suffix(u'A2Sg_Pron')
        Pnon_Pron = self._suffix_graph.get_suffix(u'Pnon_Pron')

        self._add_morpheme_container(root_sen, [A2Sg_Pron, Pnon_Pron,  self._suffix_graph.get_suffix(u'Nom_Pron')])
        self._add_morpheme_container(root_sen, [A2Sg_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Acc_Pron'),    u'i')])
        self._add_morpheme_container(root_san, [A2Sg_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Dat_Pron'),    u'a')])
        self._add_morpheme_container(root_sen, [A2Sg_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Loc_Pron'),    u'de')])
        self._add_morpheme_container(root_sen, [A2Sg_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Abl_Pron'),    u'den')])
        self._add_morpheme_container(root_sen, [A2Sg_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Ins_Pron'),    u'le')])
        self._add_morpheme_container(root_sen, [A2Sg_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Ins_Pron'),    u'inle')])
        self._add_morpheme_container(root_sen, [A2Sg_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Gen_Pron'),    u'in')])
        self._add_morpheme_container(root_sen, [A2Sg_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'AccordingTo'), u'ce')])

        self._add_morpheme_container(root_sen, [A2Sg_Pron, Pnon_Pron, self._suffix_graph.get_suffix(u'Nom_Pron_Deriv')])

    def _create_predefined_path_of_o_pron_pers(self):
        root_o = self._find_root(u'o', SyntacticCategory.PRONOUN, SecondarySyntacticCategory.PERSONAL)

        A3Sg_Pron = self._suffix_graph.get_suffix(u'A3Sg_Pron')
        Pnon_Pron = self._suffix_graph.get_suffix(u'Pnon_Pron')

        self._add_morpheme_container(root_o, [A3Sg_Pron, Pnon_Pron,  self._suffix_graph.get_suffix(u'Nom_Pron')])
        self._add_morpheme_container(root_o, [A3Sg_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Acc_Pron'),    u'nu')])
        self._add_morpheme_container(root_o, [A3Sg_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Dat_Pron'),    u'na')])
        self._add_morpheme_container(root_o, [A3Sg_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Loc_Pron'),    u'nda')])
        self._add_morpheme_container(root_o, [A3Sg_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Abl_Pron'),    u'ndan')])
        self._add_morpheme_container(root_o, [A3Sg_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Ins_Pron'),    u'nla')])
        self._add_morpheme_container(root_o, [A3Sg_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Ins_Pron'),    u'nunla')])
        self._add_morpheme_container(root_o, [A3Sg_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Gen_Pron'),    u'nun')])
        self._add_morpheme_container(root_o, [A3Sg_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'AccordingTo'), u'nca')])

        self._add_morpheme_container(root_o, [A3Sg_Pron, Pnon_Pron,  self._suffix_graph.get_suffix(u'Nom_Pron_Deriv')])

    def _create_predefined_path_of_biz(self):
        root_biz = self._find_root(u'biz', SyntacticCategory.PRONOUN, SecondarySyntacticCategory.PERSONAL)

        A1Pl_Pron = self._suffix_graph.get_suffix(u'A1Pl_Pron')
        Pnon_Pron = self._suffix_graph.get_suffix(u'Pnon_Pron')

        self._add_morpheme_container(root_biz, [A1Pl_Pron, Pnon_Pron,  self._suffix_graph.get_suffix(u'Nom_Pron')])
        self._add_morpheme_container(root_biz, [A1Pl_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Acc_Pron'),    u'i')])
        self._add_morpheme_container(root_biz, [A1Pl_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Dat_Pron'),    u'e')])
        self._add_morpheme_container(root_biz, [A1Pl_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Loc_Pron'),    u'de')])
        self._add_morpheme_container(root_biz, [A1Pl_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Abl_Pron'),    u'den')])
        self._add_morpheme_container(root_biz, [A1Pl_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Ins_Pron'),    u'le')])
        self._add_morpheme_container(root_biz, [A1Pl_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Ins_Pron'),    u'imle')])
        self._add_morpheme_container(root_biz, [A1Pl_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Gen_Pron'),    u'im')])
        self._add_morpheme_container(root_biz, [A1Pl_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'AccordingTo'), u'ce')])

        self._add_morpheme_container(root_biz, [A1Pl_Pron, Pnon_Pron, self._suffix_graph.get_suffix(u'Nom_Pron_Deriv')])

        self._add_morpheme_container(root_biz, [(A1Pl_Pron, u'ler'), Pnon_Pron,  self._suffix_graph.get_suffix(u'Nom_Pron')])
        self._add_morpheme_container(root_biz, [(A1Pl_Pron, u'ler'), Pnon_Pron, (self._suffix_graph.get_suffix(u'Acc_Pron'),    u'i')])
        self._add_morpheme_container(root_biz, [(A1Pl_Pron, u'ler'), Pnon_Pron, (self._suffix_graph.get_suffix(u'Dat_Pron'),    u'e')])
        self._add_morpheme_container(root_biz, [(A1Pl_Pron, u'ler'), Pnon_Pron, (self._suffix_graph.get_suffix(u'Loc_Pron'),    u'de')])
        self._add_morpheme_container(root_biz, [(A1Pl_Pron, u'ler'), Pnon_Pron, (self._suffix_graph.get_suffix(u'Abl_Pron'),    u'den')])
        self._add_morpheme_container(root_biz, [(A1Pl_Pron, u'ler'), Pnon_Pron, (self._suffix_graph.get_suffix(u'Ins_Pron'),    u'le')])
        self._add_morpheme_container(root_biz, [(A1Pl_Pron, u'ler'), Pnon_Pron, (self._suffix_graph.get_suffix(u'Gen_Pron'),    u'in')])
        self._add_morpheme_container(root_biz, [(A1Pl_Pron, u'ler'), Pnon_Pron, (self._suffix_graph.get_suffix(u'AccordingTo'), u'ce')])

        self._add_morpheme_container(root_biz, [(A1Pl_Pron, u'ler'), Pnon_Pron, self._suffix_graph.get_suffix(u'Nom_Pron_Deriv')])

    def _create_predefined_path_of_siz(self):
        root_siz = self._find_root(u'siz', SyntacticCategory.PRONOUN, SecondarySyntacticCategory.PERSONAL)

        A2Pl_Pron = self._suffix_graph.get_suffix(u'A2Pl_Pron')
        Pnon_Pron = self._suffix_graph.get_suffix(u'Pnon_Pron')

        self._add_morpheme_container(root_siz, [A2Pl_Pron, Pnon_Pron,  self._suffix_graph.get_suffix(u'Nom_Pron')])
        self._add_morpheme_container(root_siz, [A2Pl_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Acc_Pron'),    u'i')])
        self._add_morpheme_container(root_siz, [A2Pl_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Dat_Pron'),    u'e')])
        self._add_morpheme_container(root_siz, [A2Pl_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Loc_Pron'),    u'de')])
        self._add_morpheme_container(root_siz, [A2Pl_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Abl_Pron'),    u'den')])
        self._add_morpheme_container(root_siz, [A2Pl_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Ins_Pron'),    u'le')])
        self._add_morpheme_container(root_siz, [A2Pl_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Ins_Pron'),    u'inle')])
        self._add_morpheme_container(root_siz, [A2Pl_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Gen_Pron'),    u'in')])
        self._add_morpheme_container(root_siz, [A2Pl_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'AccordingTo'), u'ce')])

        self._add_morpheme_container(root_siz, [A2Pl_Pron, Pnon_Pron, self._suffix_graph.get_suffix(u'Nom_Pron_Deriv')])

        self._add_morpheme_container(root_siz, [(A2Pl_Pron, u'ler'), Pnon_Pron,  self._suffix_graph.get_suffix(u'Nom_Pron')])
        self._add_morpheme_container(root_siz, [(A2Pl_Pron, u'ler'), Pnon_Pron, (self._suffix_graph.get_suffix(u'Acc_Pron'),    u'i')])
        self._add_morpheme_container(root_siz, [(A2Pl_Pron, u'ler'), Pnon_Pron, (self._suffix_graph.get_suffix(u'Dat_Pron'),    u'e')])
        self._add_morpheme_container(root_siz, [(A2Pl_Pron, u'ler'), Pnon_Pron, (self._suffix_graph.get_suffix(u'Loc_Pron'),    u'de')])
        self._add_morpheme_container(root_siz, [(A2Pl_Pron, u'ler'), Pnon_Pron, (self._suffix_graph.get_suffix(u'Abl_Pron'),    u'den')])
        self._add_morpheme_container(root_siz, [(A2Pl_Pron, u'ler'), Pnon_Pron, (self._suffix_graph.get_suffix(u'Ins_Pron'),    u'le')])
        self._add_morpheme_container(root_siz, [(A2Pl_Pron, u'ler'), Pnon_Pron, (self._suffix_graph.get_suffix(u'Gen_Pron'),    u'in')])
        self._add_morpheme_container(root_siz, [(A2Pl_Pron, u'ler'), Pnon_Pron, (self._suffix_graph.get_suffix(u'AccordingTo'), u'ce')])

        self._add_morpheme_container(root_siz, [(A2Pl_Pron, u'ler'), Pnon_Pron, self._suffix_graph.get_suffix(u'Nom_Pron_Deriv')])

    def _create_predefined_path_of_onlar_pron_pers(self):
        root_o = self._find_root(u'o', SyntacticCategory.PRONOUN, SecondarySyntacticCategory.PERSONAL)

        A3Pl_Pron = self._suffix_graph.get_suffix(u'A3Pl_Pron')
        Pnon_Pron = self._suffix_graph.get_suffix(u'Pnon_Pron')

        self._add_morpheme_container(root_o, [(A3Pl_Pron, 'nlar'), Pnon_Pron,  self._suffix_graph.get_suffix(u'Nom_Pron')])
        self._add_morpheme_container(root_o, [(A3Pl_Pron, 'nlar'), Pnon_Pron, (self._suffix_graph.get_suffix(u'Acc_Pron'),    u'ı')])
        self._add_morpheme_container(root_o, [(A3Pl_Pron, 'nlar'), Pnon_Pron, (self._suffix_graph.get_suffix(u'Dat_Pron'),    u'a')])
        self._add_morpheme_container(root_o, [(A3Pl_Pron, 'nlar'), Pnon_Pron, (self._suffix_graph.get_suffix(u'Loc_Pron'),    u'da')])
        self._add_morpheme_container(root_o, [(A3Pl_Pron, 'nlar'), Pnon_Pron, (self._suffix_graph.get_suffix(u'Abl_Pron'),    u'dan')])
        self._add_morpheme_container(root_o, [(A3Pl_Pron, 'nlar'), Pnon_Pron, (self._suffix_graph.get_suffix(u'Ins_Pron'),    u'la')])
        self._add_morpheme_container(root_o, [(A3Pl_Pron, 'nlar'), Pnon_Pron, (self._suffix_graph.get_suffix(u'Gen_Pron'),    u'ın')])
        self._add_morpheme_container(root_o, [(A3Pl_Pron, 'nlar'), Pnon_Pron, (self._suffix_graph.get_suffix(u'AccordingTo'), u'ca')])

        self._add_morpheme_container(root_o, [(A3Pl_Pron, 'nlar'), Pnon_Pron,  self._suffix_graph.get_suffix(u'Nom_Pron_Deriv')])

    def _create_predefined_path_of_bu_pron_demons(self):
        root_bu = self._find_root(u'bu', SyntacticCategory.PRONOUN, SecondarySyntacticCategory.DEMONSTRATIVE)

        A3Sg_Pron = self._suffix_graph.get_suffix(u'A3Sg_Pron')
        Pnon_Pron = self._suffix_graph.get_suffix(u'Pnon_Pron')

        self._add_morpheme_container(root_bu, [A3Sg_Pron, Pnon_Pron,  self._suffix_graph.get_suffix(u'Nom_Pron')])
        self._add_morpheme_container(root_bu, [A3Sg_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Acc_Pron'), u'nu')])
        self._add_morpheme_container(root_bu, [A3Sg_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Dat_Pron'), u'na')])
        self._add_morpheme_container(root_bu, [A3Sg_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Loc_Pron'), u'nda')])
        self._add_morpheme_container(root_bu, [A3Sg_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Abl_Pron'), u'ndan')])
        self._add_morpheme_container(root_bu, [A3Sg_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Ins_Pron'), u'nla')])
        self._add_morpheme_container(root_bu, [A3Sg_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Ins_Pron'), u'nunla')])
        self._add_morpheme_container(root_bu, [A3Sg_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Gen_Pron'), u'nun')])

        self._add_morpheme_container(root_bu, [A3Sg_Pron, Pnon_Pron,  self._suffix_graph.get_suffix(u'Nom_Pron_Deriv')])

    def _create_predefined_path_of_su_pron_demons(self):
        root_su = self._find_root(u'şu', SyntacticCategory.PRONOUN, SecondarySyntacticCategory.DEMONSTRATIVE)

        A3Sg_Pron = self._suffix_graph.get_suffix(u'A3Sg_Pron')
        Pnon_Pron = self._suffix_graph.get_suffix(u'Pnon_Pron')

        self._add_morpheme_container(root_su, [A3Sg_Pron, Pnon_Pron,  self._suffix_graph.get_suffix(u'Nom_Pron')])
        self._add_morpheme_container(root_su, [A3Sg_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Acc_Pron'), u'nu')])
        self._add_morpheme_container(root_su, [A3Sg_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Dat_Pron'), u'na')])
        self._add_morpheme_container(root_su, [A3Sg_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Loc_Pron'), u'nda')])
        self._add_morpheme_container(root_su, [A3Sg_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Abl_Pron'), u'ndan')])
        self._add_morpheme_container(root_su, [A3Sg_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Ins_Pron'), u'nla')])
        self._add_morpheme_container(root_su, [A3Sg_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Ins_Pron'), u'nunla')])
        self._add_morpheme_container(root_su, [A3Sg_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Gen_Pron'), u'nun')])

        self._add_morpheme_container(root_su, [A3Sg_Pron, Pnon_Pron,  self._suffix_graph.get_suffix(u'Nom_Pron_Deriv')])

    def _create_predefined_path_of_o_pron_demons(self):
        root_o = self._find_root(u'o', SyntacticCategory.PRONOUN, SecondarySyntacticCategory.DEMONSTRATIVE)

        A3Sg_Pron = self._suffix_graph.get_suffix(u'A3Sg_Pron')
        Pnon_Pron = self._suffix_graph.get_suffix(u'Pnon_Pron')

        self._add_morpheme_container(root_o, [A3Sg_Pron, Pnon_Pron, self._suffix_graph.get_suffix(u'Nom_Pron')])
        self._add_morpheme_container(root_o, [A3Sg_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Acc_Pron'), u'nu')])
        self._add_morpheme_container(root_o, [A3Sg_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Dat_Pron'), u'na')])
        self._add_morpheme_container(root_o, [A3Sg_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Loc_Pron'), u'nda')])
        self._add_morpheme_container(root_o, [A3Sg_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Abl_Pron'), u'ndan')])
        self._add_morpheme_container(root_o, [A3Sg_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Ins_Pron'), u'nla')])
        self._add_morpheme_container(root_o, [A3Sg_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Ins_Pron'), u'nunla')])
        self._add_morpheme_container(root_o, [A3Sg_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Gen_Pron'), u'nun')])

        self._add_morpheme_container(root_o, [A3Sg_Pron, Pnon_Pron, self._suffix_graph.get_suffix(u'Nom_Pron_Deriv')])

    def _create_predefined_path_of_bunlar_pron_demons(self):
        root_bu = self._find_root(u'bu', SyntacticCategory.PRONOUN, SecondarySyntacticCategory.DEMONSTRATIVE)

        A3Pl_Pron = self._suffix_graph.get_suffix(u'A3Pl_Pron')
        Pnon_Pron = self._suffix_graph.get_suffix(u'Pnon_Pron')

        self._add_morpheme_container(root_bu, [(A3Pl_Pron, 'nlar'), Pnon_Pron,  self._suffix_graph.get_suffix(u'Nom_Pron')])
        self._add_morpheme_container(root_bu, [(A3Pl_Pron, 'nlar'), Pnon_Pron, (self._suffix_graph.get_suffix(u'Acc_Pron'), u'ı')])
        self._add_morpheme_container(root_bu, [(A3Pl_Pron, 'nlar'), Pnon_Pron, (self._suffix_graph.get_suffix(u'Dat_Pron'), u'a')])
        self._add_morpheme_container(root_bu, [(A3Pl_Pron, 'nlar'), Pnon_Pron, (self._suffix_graph.get_suffix(u'Loc_Pron'), u'da')])
        self._add_morpheme_container(root_bu, [(A3Pl_Pron, 'nlar'), Pnon_Pron, (self._suffix_graph.get_suffix(u'Abl_Pron'), u'dan')])
        self._add_morpheme_container(root_bu, [(A3Pl_Pron, 'nlar'), Pnon_Pron, (self._suffix_graph.get_suffix(u'Ins_Pron'), u'la')])
        self._add_morpheme_container(root_bu, [(A3Pl_Pron, 'nlar'), Pnon_Pron, (self._suffix_graph.get_suffix(u'Gen_Pron'), u'ın')])

        self._add_morpheme_container(root_bu, [(A3Pl_Pron, 'nlar'), Pnon_Pron, self._suffix_graph.get_suffix(u'Nom_Pron_Deriv')])

    def _create_predefined_path_of_sunlar_pron_demons(self):
        root_su = self._find_root(u'şu', SyntacticCategory.PRONOUN, SecondarySyntacticCategory.DEMONSTRATIVE)

        A3Pl_Pron = self._suffix_graph.get_suffix(u'A3Pl_Pron')
        Pnon_Pron = self._suffix_graph.get_suffix(u'Pnon_Pron')

        self._add_morpheme_container(root_su, [(A3Pl_Pron, 'nlar'), Pnon_Pron,  self._suffix_graph.get_suffix(u'Nom_Pron')])
        self._add_morpheme_container(root_su, [(A3Pl_Pron, 'nlar'), Pnon_Pron, (self._suffix_graph.get_suffix(u'Acc_Pron'), u'ı')])
        self._add_morpheme_container(root_su, [(A3Pl_Pron, 'nlar'), Pnon_Pron, (self._suffix_graph.get_suffix(u'Dat_Pron'), u'a')])
        self._add_morpheme_container(root_su, [(A3Pl_Pron, 'nlar'), Pnon_Pron, (self._suffix_graph.get_suffix(u'Loc_Pron'), u'da')])
        self._add_morpheme_container(root_su, [(A3Pl_Pron, 'nlar'), Pnon_Pron, (self._suffix_graph.get_suffix(u'Abl_Pron'), u'dan')])
        self._add_morpheme_container(root_su, [(A3Pl_Pron, 'nlar'), Pnon_Pron, (self._suffix_graph.get_suffix(u'Ins_Pron'), u'la')])
        self._add_morpheme_container(root_su, [(A3Pl_Pron, 'nlar'), Pnon_Pron, (self._suffix_graph.get_suffix(u'Gen_Pron'), u'ın')])

        self._add_morpheme_container(root_su, [(A3Pl_Pron, 'nlar'), Pnon_Pron, self._suffix_graph.get_suffix(u'Nom_Pron_Deriv')])

    def _create_predefined_path_of_onlar_pron_demons(self):
        root_o = self._find_root(u'o', SyntacticCategory.PRONOUN, SecondarySyntacticCategory.DEMONSTRATIVE)

        A3Pl_Pron = self._suffix_graph.get_suffix(u'A3Pl_Pron')
        Pnon_Pron = self._suffix_graph.get_suffix(u'Pnon_Pron')

        self._add_morpheme_container(root_o, [(A3Pl_Pron, 'nlar'), Pnon_Pron,  self._suffix_graph.get_suffix(u'Nom_Pron')])
        self._add_morpheme_container(root_o, [(A3Pl_Pron, 'nlar'), Pnon_Pron, (self._suffix_graph.get_suffix(u'Acc_Pron'), u'ı')])
        self._add_morpheme_container(root_o, [(A3Pl_Pron, 'nlar'), Pnon_Pron, (self._suffix_graph.get_suffix(u'Dat_Pron'), u'a')])
        self._add_morpheme_container(root_o, [(A3Pl_Pron, 'nlar'), Pnon_Pron, (self._suffix_graph.get_suffix(u'Loc_Pron'), u'da')])
        self._add_morpheme_container(root_o, [(A3Pl_Pron, 'nlar'), Pnon_Pron, (self._suffix_graph.get_suffix(u'Abl_Pron'), u'dan')])
        self._add_morpheme_container(root_o, [(A3Pl_Pron, 'nlar'), Pnon_Pron, (self._suffix_graph.get_suffix(u'Ins_Pron'), u'la')])
        self._add_morpheme_container(root_o, [(A3Pl_Pron, 'nlar'), Pnon_Pron, (self._suffix_graph.get_suffix(u'Gen_Pron'), u'ın')])

        self._add_morpheme_container(root_o, [(A3Pl_Pron, 'nlar'), Pnon_Pron, self._suffix_graph.get_suffix(u'Nom_Pron_Deriv')])

    def _create_predefined_path_of_kendi(self):
        root_kendi = self._find_root(u'kendi', SyntacticCategory.PRONOUN, SecondarySyntacticCategory.REFLEXIVE)

        A1Sg_Pron = self._suffix_graph.get_suffix(u'A1Sg_Pron')
        P1Sg_Pron = self._suffix_graph.get_suffix(u'P1Sg_Pron')
        A2Sg_Pron = self._suffix_graph.get_suffix(u'A2Sg_Pron')
        P2Sg_Pron = self._suffix_graph.get_suffix(u'P2Sg_Pron')
        A3Sg_Pron = self._suffix_graph.get_suffix(u'A3Sg_Pron')
        P3Sg_Pron = self._suffix_graph.get_suffix(u'P3Sg_Pron')
        A1Pl_Pron = self._suffix_graph.get_suffix(u'A1Pl_Pron')
        P1Pl_Pron = self._suffix_graph.get_suffix(u'P1Pl_Pron')
        A2Pl_Pron = self._suffix_graph.get_suffix(u'A2Pl_Pron')
        P2Pl_Pron = self._suffix_graph.get_suffix(u'P2Pl_Pron')
        A3Pl_Pron = self._suffix_graph.get_suffix(u'A3Pl_Pron')
        P3Pl_Pron = self._suffix_graph.get_suffix(u'P3Pl_Pron')

        ##### A1Sg
        self._add_morpheme_container(root_kendi, [A1Sg_Pron, (P1Sg_Pron,'m'),  self._suffix_graph.get_suffix(u'Nom_Pron')])
        self._add_morpheme_container(root_kendi, [A1Sg_Pron, (P1Sg_Pron,'m'), (self._suffix_graph.get_suffix(u'Acc_Pron'), u'i')])
        self._add_morpheme_container(root_kendi, [A1Sg_Pron, (P1Sg_Pron,'m'), (self._suffix_graph.get_suffix(u'Dat_Pron'), u'e')])
        self._add_morpheme_container(root_kendi, [A1Sg_Pron, (P1Sg_Pron,'m'), (self._suffix_graph.get_suffix(u'Loc_Pron'), u'de')])
        self._add_morpheme_container(root_kendi, [A1Sg_Pron, (P1Sg_Pron,'m'), (self._suffix_graph.get_suffix(u'Abl_Pron'), u'den')])
        self._add_morpheme_container(root_kendi, [A1Sg_Pron, (P1Sg_Pron,'m'), (self._suffix_graph.get_suffix(u'Ins_Pron'), u'le')])
        self._add_morpheme_container(root_kendi, [A1Sg_Pron, (P1Sg_Pron,'m'), (self._suffix_graph.get_suffix(u'Gen_Pron'), u'in')])

        self._add_morpheme_container(root_kendi, [A1Sg_Pron, (P1Sg_Pron,'m'),  self._suffix_graph.get_suffix(u'Nom_Pron_Deriv')])

        ##### A2Sg
        self._add_morpheme_container(root_kendi, [A2Sg_Pron, (P2Sg_Pron,'n'),  self._suffix_graph.get_suffix(u'Nom_Pron')])
        self._add_morpheme_container(root_kendi, [A2Sg_Pron, (P2Sg_Pron,'n'), (self._suffix_graph.get_suffix(u'Acc_Pron'), u'i')])
        self._add_morpheme_container(root_kendi, [A2Sg_Pron, (P2Sg_Pron,'n'), (self._suffix_graph.get_suffix(u'Dat_Pron'), u'e')])
        self._add_morpheme_container(root_kendi, [A2Sg_Pron, (P2Sg_Pron,'n'), (self._suffix_graph.get_suffix(u'Loc_Pron'), u'de')])
        self._add_morpheme_container(root_kendi, [A2Sg_Pron, (P2Sg_Pron,'n'), (self._suffix_graph.get_suffix(u'Abl_Pron'), u'den')])
        self._add_morpheme_container(root_kendi, [A2Sg_Pron, (P2Sg_Pron,'n'), (self._suffix_graph.get_suffix(u'Ins_Pron'), u'le')])
        self._add_morpheme_container(root_kendi, [A2Sg_Pron, (P2Sg_Pron,'n'), (self._suffix_graph.get_suffix(u'Gen_Pron'), u'in')])

        self._add_morpheme_container(root_kendi, [A2Sg_Pron, (P2Sg_Pron,'n'),  self._suffix_graph.get_suffix(u'Nom_Pron_Deriv')])

        ##### A3Sg
        self._add_morpheme_container(root_kendi, [A3Sg_Pron, P3Sg_Pron,  self._suffix_graph.get_suffix(u'Nom_Pron')])
        self._add_morpheme_container(root_kendi, [A3Sg_Pron, P3Sg_Pron, (self._suffix_graph.get_suffix(u'Acc_Pron'), u'ni')])
        self._add_morpheme_container(root_kendi, [A3Sg_Pron, P3Sg_Pron, (self._suffix_graph.get_suffix(u'Dat_Pron'), u'ne')])
        self._add_morpheme_container(root_kendi, [A3Sg_Pron, P3Sg_Pron, (self._suffix_graph.get_suffix(u'Loc_Pron'), u'nde')])
        self._add_morpheme_container(root_kendi, [A3Sg_Pron, P3Sg_Pron, (self._suffix_graph.get_suffix(u'Abl_Pron'), u'nden')])
        self._add_morpheme_container(root_kendi, [A3Sg_Pron, P3Sg_Pron, (self._suffix_graph.get_suffix(u'Ins_Pron'), u'yle')])
        self._add_morpheme_container(root_kendi, [A3Sg_Pron, P3Sg_Pron, (self._suffix_graph.get_suffix(u'Gen_Pron'), u'nin')])

        self._add_morpheme_container(root_kendi, [A3Sg_Pron, P3Sg_Pron,  self._suffix_graph.get_suffix(u'Nom_Pron_Deriv')])

        self._add_morpheme_container(root_kendi, [A3Sg_Pron, (P3Sg_Pron,'si'),  self._suffix_graph.get_suffix(u'Nom_Pron')])
        self._add_morpheme_container(root_kendi, [A3Sg_Pron, (P3Sg_Pron,'si'), (self._suffix_graph.get_suffix(u'Acc_Pron'), u'ni')])
        self._add_morpheme_container(root_kendi, [A3Sg_Pron, (P3Sg_Pron,'si'), (self._suffix_graph.get_suffix(u'Dat_Pron'), u'ne')])
        self._add_morpheme_container(root_kendi, [A3Sg_Pron, (P3Sg_Pron,'si'), (self._suffix_graph.get_suffix(u'Loc_Pron'), u'nde')])
        self._add_morpheme_container(root_kendi, [A3Sg_Pron, (P3Sg_Pron,'si'), (self._suffix_graph.get_suffix(u'Abl_Pron'), u'nden')])
        self._add_morpheme_container(root_kendi, [A3Sg_Pron, (P3Sg_Pron,'si'), (self._suffix_graph.get_suffix(u'Ins_Pron'), u'yle')])
        self._add_morpheme_container(root_kendi, [A3Sg_Pron, (P3Sg_Pron,'si'), (self._suffix_graph.get_suffix(u'Gen_Pron'), u'nin')])

        self._add_morpheme_container(root_kendi, [A3Sg_Pron, (P3Sg_Pron,'si'), self._suffix_graph.get_suffix(u'Nom_Pron_Deriv')])


        ##### A1pl
        self._add_morpheme_container(root_kendi, [A1Pl_Pron, (P1Pl_Pron,'miz'),  self._suffix_graph.get_suffix(u'Nom_Pron')])
        self._add_morpheme_container(root_kendi, [A1Pl_Pron, (P1Pl_Pron,'miz'), (self._suffix_graph.get_suffix(u'Acc_Pron'), u'i')])
        self._add_morpheme_container(root_kendi, [A1Pl_Pron, (P1Pl_Pron,'miz'), (self._suffix_graph.get_suffix(u'Dat_Pron'), u'e')])
        self._add_morpheme_container(root_kendi, [A1Pl_Pron, (P1Pl_Pron,'miz'), (self._suffix_graph.get_suffix(u'Loc_Pron'), u'de')])
        self._add_morpheme_container(root_kendi, [A1Pl_Pron, (P1Pl_Pron,'miz'), (self._suffix_graph.get_suffix(u'Abl_Pron'), u'den')])
        self._add_morpheme_container(root_kendi, [A1Pl_Pron, (P1Pl_Pron,'miz'), (self._suffix_graph.get_suffix(u'Ins_Pron'), u'le')])
        self._add_morpheme_container(root_kendi, [A1Pl_Pron, (P1Pl_Pron,'miz'), (self._suffix_graph.get_suffix(u'Gen_Pron'), u'in')])

        self._add_morpheme_container(root_kendi, [A1Pl_Pron, (P1Pl_Pron,'miz'),  self._suffix_graph.get_suffix(u'Nom_Pron_Deriv')])

        self._add_morpheme_container(root_kendi, [(A1Pl_Pron,'ler'), (P1Pl_Pron,'imiz'),  self._suffix_graph.get_suffix(u'Nom_Pron')])
        self._add_morpheme_container(root_kendi, [(A1Pl_Pron,'ler'), (P1Pl_Pron,'imiz'), (self._suffix_graph.get_suffix(u'Acc_Pron'), u'i')])
        self._add_morpheme_container(root_kendi, [(A1Pl_Pron,'ler'), (P1Pl_Pron,'imiz'), (self._suffix_graph.get_suffix(u'Dat_Pron'), u'e')])
        self._add_morpheme_container(root_kendi, [(A1Pl_Pron,'ler'), (P1Pl_Pron,'imiz'), (self._suffix_graph.get_suffix(u'Loc_Pron'), u'de')])
        self._add_morpheme_container(root_kendi, [(A1Pl_Pron,'ler'), (P1Pl_Pron,'imiz'), (self._suffix_graph.get_suffix(u'Abl_Pron'), u'den')])
        self._add_morpheme_container(root_kendi, [(A1Pl_Pron,'ler'), (P1Pl_Pron,'imiz'), (self._suffix_graph.get_suffix(u'Ins_Pron'), u'le')])
        self._add_morpheme_container(root_kendi, [(A1Pl_Pron,'ler'), (P1Pl_Pron,'imiz'), (self._suffix_graph.get_suffix(u'Gen_Pron'), u'in')])

        self._add_morpheme_container(root_kendi, [(A1Pl_Pron,'ler'), (P1Pl_Pron,'imiz'), self._suffix_graph.get_suffix(u'Nom_Pron_Deriv')])

        ##### A2pl
        self._add_morpheme_container(root_kendi, [A2Pl_Pron, (P2Pl_Pron,'niz'),  self._suffix_graph.get_suffix(u'Nom_Pron')])
        self._add_morpheme_container(root_kendi, [A2Pl_Pron, (P2Pl_Pron,'niz'), (self._suffix_graph.get_suffix(u'Acc_Pron'), u'i')])
        self._add_morpheme_container(root_kendi, [A2Pl_Pron, (P2Pl_Pron,'niz'), (self._suffix_graph.get_suffix(u'Dat_Pron'), u'e')])
        self._add_morpheme_container(root_kendi, [A2Pl_Pron, (P2Pl_Pron,'niz'), (self._suffix_graph.get_suffix(u'Loc_Pron'), u'de')])
        self._add_morpheme_container(root_kendi, [A2Pl_Pron, (P2Pl_Pron,'niz'), (self._suffix_graph.get_suffix(u'Abl_Pron'), u'den')])
        self._add_morpheme_container(root_kendi, [A2Pl_Pron, (P2Pl_Pron,'niz'), (self._suffix_graph.get_suffix(u'Ins_Pron'), u'le')])
        self._add_morpheme_container(root_kendi, [A2Pl_Pron, (P2Pl_Pron,'niz'), (self._suffix_graph.get_suffix(u'Gen_Pron'), u'in')])

        self._add_morpheme_container(root_kendi, [A2Pl_Pron, (P2Pl_Pron,'niz'), self._suffix_graph.get_suffix(u'Nom_Pron_Deriv')])

        self._add_morpheme_container(root_kendi, [(A2Pl_Pron,'ler'), (P2Pl_Pron,'iniz'),  self._suffix_graph.get_suffix(u'Nom_Pron')])
        self._add_morpheme_container(root_kendi, [(A2Pl_Pron,'ler'), (P2Pl_Pron,'iniz'), (self._suffix_graph.get_suffix(u'Acc_Pron'), u'i')])
        self._add_morpheme_container(root_kendi, [(A2Pl_Pron,'ler'), (P2Pl_Pron,'iniz'), (self._suffix_graph.get_suffix(u'Dat_Pron'), u'e')])
        self._add_morpheme_container(root_kendi, [(A2Pl_Pron,'ler'), (P2Pl_Pron,'iniz'), (self._suffix_graph.get_suffix(u'Loc_Pron'), u'de')])
        self._add_morpheme_container(root_kendi, [(A2Pl_Pron,'ler'), (P2Pl_Pron,'iniz'), (self._suffix_graph.get_suffix(u'Abl_Pron'), u'den')])
        self._add_morpheme_container(root_kendi, [(A2Pl_Pron,'ler'), (P2Pl_Pron,'iniz'), (self._suffix_graph.get_suffix(u'Ins_Pron'), u'le')])
        self._add_morpheme_container(root_kendi, [(A2Pl_Pron,'ler'), (P2Pl_Pron,'iniz'), (self._suffix_graph.get_suffix(u'Gen_Pron'), u'in')])

        self._add_morpheme_container(root_kendi, [(A2Pl_Pron,'ler'), (P2Pl_Pron,'iniz'), self._suffix_graph.get_suffix(u'Nom_Pron_Deriv')])

        ##### A3pl
        self._add_morpheme_container(root_kendi, [(A3Pl_Pron,'leri'), P3Pl_Pron,  self._suffix_graph.get_suffix(u'Nom_Pron')])
        self._add_morpheme_container(root_kendi, [(A3Pl_Pron,'leri'), P3Pl_Pron, (self._suffix_graph.get_suffix(u'Acc_Pron'), u'ni')])
        self._add_morpheme_container(root_kendi, [(A3Pl_Pron,'leri'), P3Pl_Pron, (self._suffix_graph.get_suffix(u'Dat_Pron'), u'ne')])
        self._add_morpheme_container(root_kendi, [(A3Pl_Pron,'leri'), P3Pl_Pron, (self._suffix_graph.get_suffix(u'Loc_Pron'), u'nde')])
        self._add_morpheme_container(root_kendi, [(A3Pl_Pron,'leri'), P3Pl_Pron, (self._suffix_graph.get_suffix(u'Abl_Pron'), u'nden')])
        self._add_morpheme_container(root_kendi, [(A3Pl_Pron,'leri'), P3Pl_Pron, (self._suffix_graph.get_suffix(u'Ins_Pron'), u'yle')])
        self._add_morpheme_container(root_kendi, [(A3Pl_Pron,'leri'), P3Pl_Pron, (self._suffix_graph.get_suffix(u'Gen_Pron'), u'nin')])

        self._add_morpheme_container(root_kendi, [(A3Pl_Pron,'leri'), P3Pl_Pron, self._suffix_graph.get_suffix(u'Nom_Pron_Deriv')])

    def _create_predefined_path_of_hepsi(self):
        root_hep = self._find_root(u'hep', SyntacticCategory.PRONOUN, None)
        root_hepsi = self._find_root(u'hepsi', SyntacticCategory.PRONOUN, None)

        A1Pl_Pron = self._suffix_graph.get_suffix(u'A1Pl_Pron')
        P1Pl_Pron = self._suffix_graph.get_suffix(u'P1Pl_Pron')
        A2Pl_Pron = self._suffix_graph.get_suffix(u'A2Pl_Pron')
        P2Pl_Pron = self._suffix_graph.get_suffix(u'P2Pl_Pron')
        A3Pl_Pron = self._suffix_graph.get_suffix(u'A3Pl_Pron')
        P3Pl_Pron = self._suffix_graph.get_suffix(u'P3Pl_Pron')

        ##### No A1Sg

        ##### No A2Sg

        ##### No A3Sg

        ##### A1pl
        self._add_morpheme_container(root_hep, [A1Pl_Pron, (P1Pl_Pron,'imiz'),  self._suffix_graph.get_suffix(u'Nom_Pron')])
        self._add_morpheme_container(root_hep, [A1Pl_Pron, (P1Pl_Pron,'imiz'), (self._suffix_graph.get_suffix(u'Acc_Pron'),    u'i')])
        self._add_morpheme_container(root_hep, [A1Pl_Pron, (P1Pl_Pron,'imiz'), (self._suffix_graph.get_suffix(u'Dat_Pron'),    u'e')])
        self._add_morpheme_container(root_hep, [A1Pl_Pron, (P1Pl_Pron,'imiz'), (self._suffix_graph.get_suffix(u'Loc_Pron'),    u'de')])
        self._add_morpheme_container(root_hep, [A1Pl_Pron, (P1Pl_Pron,'imiz'), (self._suffix_graph.get_suffix(u'Abl_Pron'),    u'den')])
        self._add_morpheme_container(root_hep, [A1Pl_Pron, (P1Pl_Pron,'imiz'), (self._suffix_graph.get_suffix(u'Ins_Pron'),    u'le')])
        self._add_morpheme_container(root_hep, [A1Pl_Pron, (P1Pl_Pron,'imiz'), (self._suffix_graph.get_suffix(u'Gen_Pron'),    u'in')])
        self._add_morpheme_container(root_hep, [A1Pl_Pron, (P1Pl_Pron,'imiz'), (self._suffix_graph.get_suffix(u'AccordingTo'), u'ce')])

        self._add_morpheme_container(root_hep, [A1Pl_Pron, (P1Pl_Pron,'imiz'), self._suffix_graph.get_suffix(u'Nom_Pron_Deriv')])

        ##### A2pl
        self._add_morpheme_container(root_hep, [A2Pl_Pron, (P2Pl_Pron,'iniz'),  self._suffix_graph.get_suffix(u'Nom_Pron')])
        self._add_morpheme_container(root_hep, [A2Pl_Pron, (P2Pl_Pron,'iniz'), (self._suffix_graph.get_suffix(u'Acc_Pron'),    u'i')])
        self._add_morpheme_container(root_hep, [A2Pl_Pron, (P2Pl_Pron,'iniz'), (self._suffix_graph.get_suffix(u'Dat_Pron'),    u'e')])
        self._add_morpheme_container(root_hep, [A2Pl_Pron, (P2Pl_Pron,'iniz'), (self._suffix_graph.get_suffix(u'Loc_Pron'),    u'de')])
        self._add_morpheme_container(root_hep, [A2Pl_Pron, (P2Pl_Pron,'iniz'), (self._suffix_graph.get_suffix(u'Abl_Pron'),    u'den')])
        self._add_morpheme_container(root_hep, [A2Pl_Pron, (P2Pl_Pron,'iniz'), (self._suffix_graph.get_suffix(u'Ins_Pron'),    u'le')])
        self._add_morpheme_container(root_hep, [A2Pl_Pron, (P2Pl_Pron,'iniz'), (self._suffix_graph.get_suffix(u'Gen_Pron'),    u'in')])
        self._add_morpheme_container(root_hep, [A2Pl_Pron, (P2Pl_Pron,'iniz'), (self._suffix_graph.get_suffix(u'AccordingTo'), u'ce')])

        self._add_morpheme_container(root_hep, [A2Pl_Pron, (P2Pl_Pron,'iniz'), self._suffix_graph.get_suffix(u'Nom_Pron_Deriv')])

        ##### A3pl

        self._add_morpheme_container(root_hepsi, [A3Pl_Pron, P3Pl_Pron,  self._suffix_graph.get_suffix(u'Nom_Pron')])
        self._add_morpheme_container(root_hepsi, [A3Pl_Pron, P3Pl_Pron, (self._suffix_graph.get_suffix(u'Acc_Pron'),    u'ni')])
        self._add_morpheme_container(root_hepsi, [A3Pl_Pron, P3Pl_Pron, (self._suffix_graph.get_suffix(u'Dat_Pron'),    u'ne')])
        self._add_morpheme_container(root_hepsi, [A3Pl_Pron, P3Pl_Pron, (self._suffix_graph.get_suffix(u'Loc_Pron'),    u'nde')])
        self._add_morpheme_container(root_hepsi, [A3Pl_Pron, P3Pl_Pron, (self._suffix_graph.get_suffix(u'Abl_Pron'),    u'nden')])
        self._add_morpheme_container(root_hepsi, [A3Pl_Pron, P3Pl_Pron, (self._suffix_graph.get_suffix(u'Ins_Pron'),    u'yle')])
        self._add_morpheme_container(root_hepsi, [A3Pl_Pron, P3Pl_Pron, (self._suffix_graph.get_suffix(u'Gen_Pron'),    u'nin')])
        self._add_morpheme_container(root_hepsi, [A3Pl_Pron, P3Pl_Pron, (self._suffix_graph.get_suffix(u'AccordingTo'), u'nce')])

        self._add_morpheme_container(root_hepsi, [A3Pl_Pron, P3Pl_Pron, self._suffix_graph.get_suffix(u'Nom_Pron_Deriv')])

    def _create_predefined_path_of_herkes(self):
        root_herkes = self._find_root(u'herkes', SyntacticCategory.PRONOUN, None)

        self._add_morpheme_container(root_herkes, [self._suffix_graph.get_suffix(u'A3Sg_Pron'), self._suffix_graph.get_suffix(u'Pnon_Pron')])

    def _create_predefined_path_of_question_particles(self):
        root_mii = self._find_root(u'mı', SyntacticCategory.QUESTION, None)
        root_mi  = self._find_root(u'mi', SyntacticCategory.QUESTION, None)
        root_mu  = self._find_root(u'mu', SyntacticCategory.QUESTION, None)
        root_muu = self._find_root(u'mü', SyntacticCategory.QUESTION, None)

        Pres_Ques = self._suffix_graph.get_suffix(u'Pres_Ques')
        Past_Ques = self._suffix_graph.get_suffix(u'Past_Ques')
        Narr_Ques = self._suffix_graph.get_suffix(u'Narr_Ques')

        A1Sg_Ques = self._suffix_graph.get_suffix(u'A1Sg_Ques')
        A2Sg_Ques = self._suffix_graph.get_suffix(u'A2Sg_Ques')
        A3Sg_Ques = self._suffix_graph.get_suffix(u'A3Sg_Ques')
        A1Pl_Ques = self._suffix_graph.get_suffix(u'A1Pl_Ques')
        A2Pl_Ques = self._suffix_graph.get_suffix(u'A2Pl_Ques')
        A3Pl_Ques = self._suffix_graph.get_suffix(u'A3Pl_Ques')


        ##### Pres
        self._add_morpheme_container(root_mii, [Pres_Ques, (A1Sg_Ques,u'yım')])
        self._add_morpheme_container(root_mii, [Pres_Ques, (A2Sg_Ques,u'sın')])
        self._add_morpheme_container(root_mii, [Pres_Ques, (A3Sg_Ques,u'')])
        self._add_morpheme_container(root_mii, [Pres_Ques, (A1Pl_Ques,u'yız')])
        self._add_morpheme_container(root_mii, [Pres_Ques, (A2Pl_Ques,u'sınız')])
        self._add_morpheme_container(root_mii, [Pres_Ques, (A3Pl_Ques,u'lar')])

        self._add_morpheme_container(root_mi , [Pres_Ques, (A1Sg_Ques,u'yim')])
        self._add_morpheme_container(root_mi , [Pres_Ques, (A2Sg_Ques,u'sin')])
        self._add_morpheme_container(root_mi , [Pres_Ques, (A3Sg_Ques,u'')])
        self._add_morpheme_container(root_mi , [Pres_Ques, (A1Pl_Ques,u'yiz')])
        self._add_morpheme_container(root_mi , [Pres_Ques, (A2Pl_Ques,u'siniz')])
        self._add_morpheme_container(root_mi , [Pres_Ques, (A3Pl_Ques,u'ler')])

        self._add_morpheme_container(root_mu , [Pres_Ques, (A1Sg_Ques,u'yum')])
        self._add_morpheme_container(root_mu , [Pres_Ques, (A2Sg_Ques,u'sun')])
        self._add_morpheme_container(root_mu , [Pres_Ques, (A3Sg_Ques,u'')])
        self._add_morpheme_container(root_mu , [Pres_Ques, (A1Pl_Ques,u'yuz')])
        self._add_morpheme_container(root_mu , [Pres_Ques, (A2Pl_Ques,u'sunuz')])
        self._add_morpheme_container(root_mu , [Pres_Ques, (A3Pl_Ques,u'lar')])

        self._add_morpheme_container(root_muu, [Pres_Ques, (A1Sg_Ques,u'yüm')])
        self._add_morpheme_container(root_muu, [Pres_Ques, (A2Sg_Ques,u'sün')])
        self._add_morpheme_container(root_muu, [Pres_Ques, (A3Sg_Ques,u'')])
        self._add_morpheme_container(root_muu, [Pres_Ques, (A1Pl_Ques,u'yüz')])
        self._add_morpheme_container(root_muu, [Pres_Ques, (A2Pl_Ques,u'sünüz')])
        self._add_morpheme_container(root_muu, [Pres_Ques, (A3Pl_Ques,u'ler')])

        ##### Past
        self._add_morpheme_container(root_mii, [(Past_Ques,u'ydı'), (A1Sg_Ques,u'm')])
        self._add_morpheme_container(root_mii, [(Past_Ques,u'ydı'), (A2Sg_Ques,u'n')])
        self._add_morpheme_container(root_mii, [(Past_Ques,u'ydı'), (A3Sg_Ques,u'')])
        self._add_morpheme_container(root_mii, [(Past_Ques,u'ydı'), (A1Pl_Ques,u'k')])
        self._add_morpheme_container(root_mii, [(Past_Ques,u'ydı'), (A2Pl_Ques,u'nız')])
        self._add_morpheme_container(root_mii, [(Past_Ques,u'ydı'), (A3Pl_Ques,u'lar')])

        self._add_morpheme_container(root_mi , [(Past_Ques,u'ydi'), (A1Sg_Ques,u'm')])
        self._add_morpheme_container(root_mi , [(Past_Ques,u'ydi'), (A2Sg_Ques,u'n')])
        self._add_morpheme_container(root_mi , [(Past_Ques,u'ydi'), (A3Sg_Ques,u'')])
        self._add_morpheme_container(root_mi , [(Past_Ques,u'ydi'), (A1Pl_Ques,u'k')])
        self._add_morpheme_container(root_mi , [(Past_Ques,u'ydi'), (A2Pl_Ques,u'niz')])
        self._add_morpheme_container(root_mi , [(Past_Ques,u'ydi'), (A3Pl_Ques,u'ler')])

        self._add_morpheme_container(root_mu , [(Past_Ques,u'ydu'), (A1Sg_Ques,u'm')])
        self._add_morpheme_container(root_mu , [(Past_Ques,u'ydu'), (A2Sg_Ques,u'n')])
        self._add_morpheme_container(root_mu , [(Past_Ques,u'ydu'), (A3Sg_Ques,u'')])
        self._add_morpheme_container(root_mu , [(Past_Ques,u'ydu'), (A1Pl_Ques,u'k')])
        self._add_morpheme_container(root_mu , [(Past_Ques,u'ydu'), (A2Pl_Ques,u'nuz')])
        self._add_morpheme_container(root_mu , [(Past_Ques,u'ydu'), (A3Pl_Ques,u'lar')])

        self._add_morpheme_container(root_muu, [(Past_Ques,u'ydü'), (A1Sg_Ques,u'm')])
        self._add_morpheme_container(root_muu, [(Past_Ques,u'ydü'), (A2Sg_Ques,u'n')])
        self._add_morpheme_container(root_muu, [(Past_Ques,u'ydü'), (A3Sg_Ques,u'')])
        self._add_morpheme_container(root_muu, [(Past_Ques,u'ydü'), (A1Pl_Ques,u'k')])
        self._add_morpheme_container(root_muu, [(Past_Ques,u'ydü'), (A2Pl_Ques,u'nüz')])
        self._add_morpheme_container(root_muu, [(Past_Ques,u'ydü'), (A3Pl_Ques,u'ler')])

        ##### Narr
        self._add_morpheme_container(root_mii, [(Narr_Ques,u'ymış'), (A1Sg_Ques,u'ım')])
        self._add_morpheme_container(root_mii, [(Narr_Ques,u'ymış'), (A2Sg_Ques,u'sın')])
        self._add_morpheme_container(root_mii, [(Narr_Ques,u'ymış'), (A3Sg_Ques,u'')])
        self._add_morpheme_container(root_mii, [(Narr_Ques,u'ymış'), (A1Pl_Ques,u'ız')])
        self._add_morpheme_container(root_mii, [(Narr_Ques,u'ymış'), (A2Pl_Ques,u'sınız')])
        self._add_morpheme_container(root_mii, [(Narr_Ques,u'ymış'), (A3Pl_Ques,u'lar')])

        self._add_morpheme_container(root_mi , [(Narr_Ques,u'ymiş'), (A1Sg_Ques,u'im')])
        self._add_morpheme_container(root_mi , [(Narr_Ques,u'ymiş'), (A2Sg_Ques,u'sin')])
        self._add_morpheme_container(root_mi , [(Narr_Ques,u'ymiş'), (A3Sg_Ques,u'')])
        self._add_morpheme_container(root_mi , [(Narr_Ques,u'ymiş'), (A1Pl_Ques,u'iz')])
        self._add_morpheme_container(root_mi , [(Narr_Ques,u'ymiş'), (A2Pl_Ques,u'siniz')])
        self._add_morpheme_container(root_mi , [(Narr_Ques,u'ymiş'), (A3Pl_Ques,u'ler')])

        self._add_morpheme_container(root_mu , [(Narr_Ques,u'ymuş'), (A1Sg_Ques,u'um')])
        self._add_morpheme_container(root_mu , [(Narr_Ques,u'ymuş'), (A2Sg_Ques,u'sun')])
        self._add_morpheme_container(root_mu , [(Narr_Ques,u'ymuş'), (A3Sg_Ques,u'')])
        self._add_morpheme_container(root_mu , [(Narr_Ques,u'ymuş'), (A1Pl_Ques,u'uz')])
        self._add_morpheme_container(root_mu , [(Narr_Ques,u'ymuş'), (A2Pl_Ques,u'sunuz')])
        self._add_morpheme_container(root_mu , [(Narr_Ques,u'ymuş'), (A3Pl_Ques,u'lar')])

        self._add_morpheme_container(root_muu, [(Narr_Ques,u'ymüş'), (A1Sg_Ques,u'üm')])
        self._add_morpheme_container(root_muu, [(Narr_Ques,u'ymüş'), (A2Sg_Ques,u'sün')])
        self._add_morpheme_container(root_muu, [(Narr_Ques,u'ymüş'), (A3Sg_Ques,u'')])
        self._add_morpheme_container(root_muu, [(Narr_Ques,u'ymüş'), (A1Pl_Ques,u'üz')])
        self._add_morpheme_container(root_muu, [(Narr_Ques,u'ymüş'), (A2Pl_Ques,u'sünüz')])
        self._add_morpheme_container(root_muu, [(Narr_Ques,u'ymüş'), (A3Pl_Ques,u'ler')])

    def _create_predefined_path_of_ne(self):
        root_ne = self._find_root(u'ne', SyntacticCategory.PRONOUN, SecondarySyntacticCategory.QUESTION)

        A3Sg_Pron = self._suffix_graph.get_suffix(u'A3Sg_Pron')

        self._add_morpheme_container(root_ne, [A3Sg_Pron, (self._suffix_graph.get_suffix(u'P1Sg_Pron'),u'm')])
        self._add_morpheme_container(root_ne, [A3Sg_Pron, (self._suffix_graph.get_suffix(u'P1Sg_Pron'),u'yim')])

        self._add_morpheme_container(root_ne, [A3Sg_Pron, (self._suffix_graph.get_suffix(u'P2Sg_Pron'),u'n')])
        self._add_morpheme_container(root_ne, [A3Sg_Pron, (self._suffix_graph.get_suffix(u'P2Sg_Pron'),u'yin')])

        self._add_morpheme_container(root_ne, [A3Sg_Pron, (self._suffix_graph.get_suffix(u'P3Sg_Pron'),u'yi')])
        self._add_morpheme_container(root_ne, [A3Sg_Pron, (self._suffix_graph.get_suffix(u'P3Sg_Pron'),u'si')])

        self._add_morpheme_container(root_ne, [A3Sg_Pron, (self._suffix_graph.get_suffix(u'P1Pl_Pron'),u'yimiz')])

        self._add_morpheme_container(root_ne, [A3Sg_Pron, (self._suffix_graph.get_suffix(u'P2Pl_Pron'),u'yiniz')])

        self._add_morpheme_container(root_ne, [A3Sg_Pron, (self._suffix_graph.get_suffix(u'P3Pl_Pron'),u'leri')])

        self._add_morpheme_container(root_ne, [A3Sg_Pron,  self._suffix_graph.get_suffix(u'Pnon_Pron'),     (self._suffix_graph.get_suffix(u'Gen_Pron'), u'yin')])

        self._add_morpheme_container(root_ne, [A3Sg_Pron,  self._suffix_graph.get_suffix(u'Pnon_Pron')])

        self._add_morpheme_container(root_ne, [(self._suffix_graph.get_suffix(u'A3Pl_Pron'), u'ler'),  self._suffix_graph.get_suffix(u'Pnon_Pron')])

    def _create_predefined_path_of_ora_bura_sura_nere(self):
        root_or = self._find_root(u'or', SyntacticCategory.PRONOUN, None)
        root_bur = self._find_root(u'bur', SyntacticCategory.PRONOUN, None)
        root_sur = self._find_root(u'şur', SyntacticCategory.PRONOUN, None)
        root_ner = self._find_root(u'ner', SyntacticCategory.PRONOUN, SecondarySyntacticCategory.QUESTION)

        A3Sg_Pron = self._suffix_graph.get_suffix(u'A3Sg_Pron')
        Pnon_Pron = self._suffix_graph.get_suffix(u'Pnon_Pron')

        # define predefined paths for "orda" and "ordan" etc.

        self._add_morpheme_container(root_or,  [A3Sg_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Loc_Pron'),'da')])
        self._add_morpheme_container(root_or,  [A3Sg_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Abl_Pron'),'dan')])

        self._add_morpheme_container(root_bur, [A3Sg_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Loc_Pron'),'da')])
        self._add_morpheme_container(root_bur, [A3Sg_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Abl_Pron'),'dan')])

        self._add_morpheme_container(root_sur, [A3Sg_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Loc_Pron'),'da')])
        self._add_morpheme_container(root_sur, [A3Sg_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Abl_Pron'),'dan')])

        self._add_morpheme_container(root_ner, [A3Sg_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Loc_Pron'),'de')])
        self._add_morpheme_container(root_ner, [A3Sg_Pron, Pnon_Pron, (self._suffix_graph.get_suffix(u'Abl_Pron'),'den')])

    def _create_predefined_path_of_iceri_disari(self):
        root_icer = self._find_root(u'içer', SyntacticCategory.NOUN, None)
        root_disar = self._find_root(u'dışar', SyntacticCategory.NOUN, None)

        A3Sg_Noun = self._suffix_graph.get_suffix(u'A3Sg_Noun')
        Pnon_Noun = self._suffix_graph.get_suffix(u'Pnon_Noun')
        P3Sg_Noun = self._suffix_graph.get_suffix(u'P3Sg_Noun')

        # define predefined paths for "içerde" and "dışardan" etc.

        self._add_morpheme_container(root_icer,  [A3Sg_Noun,  Pnon_Noun, (self._suffix_graph.get_suffix(u'Loc_Noun'),'de')])
        self._add_morpheme_container(root_icer,  [A3Sg_Noun,  Pnon_Noun, (self._suffix_graph.get_suffix(u'Abl_Noun'),'den')])
        self._add_morpheme_container(root_icer,  [A3Sg_Noun, (P3Sg_Noun,'si')])

        self._add_morpheme_container(root_disar, [A3Sg_Noun,  Pnon_Noun, (self._suffix_graph.get_suffix(u'Loc_Noun'),'da')])
        self._add_morpheme_container(root_disar, [A3Sg_Noun,  Pnon_Noun, (self._suffix_graph.get_suffix(u'Abl_Noun'),'dan')])
        self._add_morpheme_container(root_disar, [A3Sg_Noun, (P3Sg_Noun,u'sı')])

    def _create_predefined_path_of_bazilari_bazisi(self):
        root_bazisi = self._find_root(u'bazısı', SyntacticCategory.PRONOUN, None)
        root_bazilari = self._find_root(u'bazıları', SyntacticCategory.PRONOUN, None)

        A3Sg_Pron = self._suffix_graph.get_suffix(u'A3Sg_Pron')

        self._add_morpheme_container(root_bazilari, [A3Sg_Pron,  self._suffix_graph.get_suffix(u'P3Sg_Pron')])
        self._add_morpheme_container(root_bazilari, [A3Sg_Pron, (self._suffix_graph.get_suffix(u'P1Pl_Pron'), u'mız')])
        self._add_morpheme_container(root_bazilari, [A3Sg_Pron, (self._suffix_graph.get_suffix(u'P2Pl_Pron'), u'nız')])

        self._add_morpheme_container(root_bazisi,   [A3Sg_Pron,  self._suffix_graph.get_suffix(u'P3Sg_Pron')])

    def _create_predefined_path_of_kimileri_kimisi_kimi(self):
        root_kimi   = self._find_root(u'kimi',   SyntacticCategory.PRONOUN, None)
        root_kimisi = self._find_root(u'kimisi', SyntacticCategory.PRONOUN, None)
        root_kimileri = self._find_root(u'kimileri', SyntacticCategory.PRONOUN, None)

        A3Sg_Pron = self._suffix_graph.get_suffix(u'A3Sg_Pron')

        self._add_morpheme_container(root_kimileri, [A3Sg_Pron,  self._suffix_graph.get_suffix(u'P3Sg_Pron')])
        self._add_morpheme_container(root_kimileri, [A3Sg_Pron, (self._suffix_graph.get_suffix(u'P1Pl_Pron'), u'miz')])
        self._add_morpheme_container(root_kimileri, [A3Sg_Pron, (self._suffix_graph.get_suffix(u'P2Pl_Pron'), u'niz')])

        self._add_morpheme_container(root_kimi,     [A3Sg_Pron,  self._suffix_graph.get_suffix(u'P3Sg_Pron')])
        self._add_morpheme_container(root_kimi,     [A3Sg_Pron, (self._suffix_graph.get_suffix(u'P1Pl_Pron'), u'miz')])
        self._add_morpheme_container(root_kimi,     [A3Sg_Pron, (self._suffix_graph.get_suffix(u'P2Pl_Pron'), u'niz')])

        self._add_morpheme_container(root_kimisi,   [A3Sg_Pron,  self._suffix_graph.get_suffix(u'P3Sg_Pron')])

    def _create_predefined_path_of_birileri_birisi_biri(self):
        root_biri   = self._find_root(u'biri',   SyntacticCategory.PRONOUN, None)
        root_birisi = self._find_root(u'birisi', SyntacticCategory.PRONOUN, None)
        root_birileri = self._find_root(u'birileri', SyntacticCategory.PRONOUN, None)

        A3Sg_Pron = self._suffix_graph.get_suffix(u'A3Sg_Pron')

        self._add_morpheme_container(root_birileri, [A3Sg_Pron,  self._suffix_graph.get_suffix(u'P3Sg_Pron')])
        self._add_morpheme_container(root_birileri, [A3Sg_Pron, (self._suffix_graph.get_suffix(u'P1Pl_Pron'), u'miz')])
        self._add_morpheme_container(root_birileri, [A3Sg_Pron, (self._suffix_graph.get_suffix(u'P2Pl_Pron'), u'niz')])

        self._add_morpheme_container(root_biri,     [A3Sg_Pron,  self._suffix_graph.get_suffix(u'P3Sg_Pron')])
        self._add_morpheme_container(root_biri,     [A3Sg_Pron, (self._suffix_graph.get_suffix(u'P1Pl_Pron'), u'miz')])
        self._add_morpheme_container(root_biri,     [A3Sg_Pron, (self._suffix_graph.get_suffix(u'P2Pl_Pron'), u'niz')])

        self._add_morpheme_container(root_birisi,   [A3Sg_Pron,  self._suffix_graph.get_suffix(u'P3Sg_Pron')])

    def _create_predefined_path_of_hicbirisi_hicbiri(self):
        root_hicbiri   = self._find_root(u'hiçbiri',   SyntacticCategory.PRONOUN, None)
        root_hicbirisi = self._find_root(u'hiçbirisi', SyntacticCategory.PRONOUN, None)

        A3Sg_Pron = self._suffix_graph.get_suffix(u'A3Sg_Pron')

        self._add_morpheme_container(root_hicbiri,   [A3Sg_Pron,  self._suffix_graph.get_suffix(u'P3Sg_Pron')])
        self._add_morpheme_container(root_hicbiri,   [A3Sg_Pron, (self._suffix_graph.get_suffix(u'P1Pl_Pron'), u'miz')])
        self._add_morpheme_container(root_hicbiri,   [A3Sg_Pron, (self._suffix_graph.get_suffix(u'P2Pl_Pron'), u'niz')])

        self._add_morpheme_container(root_hicbirisi, [A3Sg_Pron,  self._suffix_graph.get_suffix(u'P3Sg_Pron')])

    def _create_predefined_path_of_birbiri(self):
        root_birbir    = self._find_root(u'birbir',    SyntacticCategory.PRONOUN, None)
        root_birbiri   = self._find_root(u'birbiri',   SyntacticCategory.PRONOUN, None)

        self._add_morpheme_container(root_birbiri, [self._suffix_graph.get_suffix(u'A3Sg_Pron'),  self._suffix_graph.get_suffix(u'P3Sg_Pron')])
        self._add_morpheme_container(root_birbiri, [self._suffix_graph.get_suffix(u'A1Pl_Pron'), (self._suffix_graph.get_suffix(u'P1Pl_Pron'), u'miz')])
        self._add_morpheme_container(root_birbiri, [self._suffix_graph.get_suffix(u'A2Pl_Pron'), (self._suffix_graph.get_suffix(u'P2Pl_Pron'), u'niz')])

        self._add_morpheme_container(root_birbir,  [self._suffix_graph.get_suffix(u'A3Pl_Pron'), (self._suffix_graph.get_suffix(u'P3Pl_Pron'), u'leri')])

    def _create_predefined_path_of_cogu_bircogu_coklari_bircoklari(self):
        root_cogu       = self._find_root(u'çoğu',        SyntacticCategory.PRONOUN, None)
        root_bircogu    = self._find_root(u'birçoğu',     SyntacticCategory.PRONOUN, None)
        root_coklari    = self._find_root(u'çokları',     SyntacticCategory.PRONOUN, None)
        root_bircoklari = self._find_root(u'birçokları',  SyntacticCategory.PRONOUN, None)

        A3Sg_Pron = self._suffix_graph.get_suffix(u'A3Sg_Pron')

        self._add_morpheme_container(root_cogu,    [A3Sg_Pron,  self._suffix_graph.get_suffix(u'P3Sg_Pron')])
        self._add_morpheme_container(root_cogu,    [A3Sg_Pron, (self._suffix_graph.get_suffix(u'P1Pl_Pron'), u'muz')])
        self._add_morpheme_container(root_cogu,    [A3Sg_Pron, (self._suffix_graph.get_suffix(u'P2Pl_Pron'), u'nuz')])

        self._add_morpheme_container(root_bircogu, [A3Sg_Pron,  self._suffix_graph.get_suffix(u'P3Sg_Pron')])
        self._add_morpheme_container(root_bircogu, [A3Sg_Pron, (self._suffix_graph.get_suffix(u'P1Pl_Pron'), u'muz')])
        self._add_morpheme_container(root_bircogu, [A3Sg_Pron, (self._suffix_graph.get_suffix(u'P2Pl_Pron'), u'nuz')])

        self._add_morpheme_container(root_coklari, [A3Sg_Pron,  self._suffix_graph.get_suffix(u'P3Pl_Pron')])

        self._add_morpheme_container(root_bircoklari, [A3Sg_Pron, self._suffix_graph.get_suffix(u'P3Pl_Pron')])

    def _create_predefined_path_of_birkaci(self):
        root_birkaci = self._find_root(u'birkaçı', SyntacticCategory.PRONOUN, None)

        A3Sg_Pron = self._suffix_graph.get_suffix(u'A3Sg_Pron')

        self._add_morpheme_container(root_birkaci, [A3Sg_Pron,  self._suffix_graph.get_suffix(u'P3Sg_Pron')])
        self._add_morpheme_container(root_birkaci, [A3Sg_Pron, (self._suffix_graph.get_suffix(u'P1Pl_Pron'), u'mız')])
        self._add_morpheme_container(root_birkaci, [A3Sg_Pron, (self._suffix_graph.get_suffix(u'P2Pl_Pron'), u'nız')])

    def _create_predefined_path_of_cumlesi(self):
        root_cumlesi = self._find_root(u'cümlesi', SyntacticCategory.PRONOUN, None)

        self._add_morpheme_container(root_cumlesi, [self._suffix_graph.get_suffix(u'A3Sg_Pron'), self._suffix_graph.get_suffix(u'P3Sg_Pron')])

    def _create_predefined_path_of_digeri_digerleri(self):
        root_digeri    = self._find_root(u'diğeri',    SyntacticCategory.PRONOUN, None)
        root_digerleri = self._find_root(u'diğerleri', SyntacticCategory.PRONOUN, None)

        A3Sg_Pron = self._suffix_graph.get_suffix(u'A3Sg_Pron')

        self._add_morpheme_container(root_digeri,    [A3Sg_Pron,  self._suffix_graph.get_suffix(u'P3Sg_Pron')])
        self._add_morpheme_container(root_digeri,    [A3Sg_Pron, (self._suffix_graph.get_suffix(u'P1Pl_Pron'), u'miz')])
        self._add_morpheme_container(root_digeri,    [A3Sg_Pron, (self._suffix_graph.get_suffix(u'P2Pl_Pron'), u'niz')])

        self._add_morpheme_container(root_digerleri, [A3Sg_Pron,  self._suffix_graph.get_suffix(u'P3Pl_Pron')])
        self._add_morpheme_container(root_digerleri, [A3Sg_Pron, (self._suffix_graph.get_suffix(u'P1Pl_Pron'), u'miz')])
        self._add_morpheme_container(root_digerleri, [A3Sg_Pron, (self._suffix_graph.get_suffix(u'P2Pl_Pron'), u'niz')])