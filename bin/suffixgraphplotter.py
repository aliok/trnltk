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
import os
from trnltk.morphology.morphotactics.basicsuffixgraph import *
from trnltk.morphology.morphotactics.copulasuffixgraph import *


import networkx as nx
from trnltk.morphology.morphotactics.numeralsuffixgraph import NumeralSuffixGraph
from trnltk.morphology.morphotactics.propernounsuffixgraph import ProperNounSuffixGraph


def generate_directed_graph(suffix_graph):
    graph=nx.MultiDiGraph()

    possible_edge_group_colors = {'red', 'blue', 'green', 'cyan', 'magenta', 'purple',
                                  'brown', 'orange', 'skyblue', 'turquoise', 'yellowgreen',
                                  'yellow4', 'springgreen4', 'salmon', 'purple', 'lawngreen',
                                  'goldenrod3'}

    for state in suffix_graph.get_all_states():
        graph.add_node(state.name)
        if state.name in graph:
            if state.type==State.TERMINAL:
                graph.node[state.name]['shape'] = 'doubleoctagon'
            elif state.type==State.DERIVATIONAL:
                graph.node[state.name]['shape'] = 'house'

        colormap = dict()

        for (suffix, output_state) in state.outputs:
            label = suffix.name
            print 'Adding edge ', state.name, output_state.name, label

            color = 'black'

            if suffix.group:
                group_name = suffix.group.name
                if colormap.has_key(group_name):
                    color = colormap[group_name]
                else:
                    color = possible_edge_group_colors.pop()
                    if not color:
                        raise Exception('Not enough colors to color groups')
                    colormap[group_name] = color

            graph.add_edge(state.name, output_state.name, label = label, color = color)


    return graph

def write_graph_to_file(graph, file_path, format='dot'):
    A=nx.to_agraph(graph)

    set_same_rank([node.name for node in A.nodes() if node.name in ['NOUN_ROOT', 'VERB_ROOT', 'PRONOUN_ROOT', 'PROPER_NOUN_ROOT', 'NOUN_COMPOUND_ROOT']], A, 'source')
    set_same_rank([node.name for node in A.nodes() if node.name in ['ADJECTIVE_ROOT', 'ADVERB_ROOT']], A, 'same')

#    set_same_rank(['VERB_WITH_POLARITY', 'VERB_COPULA_WITHOUT_TENSE'], A)
#
    #    set_same_rank([node.name for node in filter(lambda node : node.name.endswith('ROOT'), A.nodes())], A, 'source')
    set_same_rank([node.name for node in filter(lambda node : node.name.endswith('TERMINAL_TRANSFER'), A.nodes())], A)
    set_same_rank([node.name for node in filter(lambda node : node.name.endswith('COPULA'), A.nodes())], A)
    set_same_rank([node.name for node in filter(lambda node : node.name.endswith('TERMINAL'), A.nodes())], A, 'sink')

    A.layout(prog='dot')
    A.draw(file_path, format)

#    A.write(file_path)

def set_same_rank(node_names, A, rank='same'):
    sub_graph = A.add_subgraph()
    sub_graph.graph_attr['rank'] = rank
    for name_name in node_names:
        sub_graph.add_node(name_name)

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print "Usage:\n"
        print sys.argv[0] + " {B|C|P|N}  <output file path> \n", \
            "Extension of the output file path can be in PNG, DOT, JPG. It will be recognized and used while rendering. \n", \
            "Type B is basic suffix graph \n", \
            "Type C is copula suffix graph (with copula, etc.) \n", \
            "Type P is proper noun and abbreviation suffix graph \n", \
            "Type N is numeral suffix graph \n" \
            "Example : {} BNP /home/ali/Desktop/suffixGraph.png \n".format(sys.argv[0])

        sys.exit(2)

    graph_type = sys.argv[1]
    output_file_path = sys.argv[2]

    for char in graph_type:
        if char not in 'BCNP':
            print "Unknown graph type : {} ".format(char)
            sys.exit(2)

    suffix_graph = BasicSuffixGraph()
    if 'B' in graph_type:
        pass
    if 'P' in graph_type:
        suffix_graph = ProperNounSuffixGraph(suffix_graph)
    if 'N' in graph_type:
        suffix_graph = NumeralSuffixGraph(suffix_graph)
    if 'C' in graph_type:
        suffix_graph = CopulaSuffixGraph(suffix_graph)

    if not suffix_graph:
        print "Unknown graph type : {} ".format(graph_type)
        sys.exit(2)

    suffix_graph.initialize()

    di_graph = generate_directed_graph(suffix_graph)
    write_graph_to_file(di_graph, output_file_path, os.path.splitext(output_file_path)[1][1:])