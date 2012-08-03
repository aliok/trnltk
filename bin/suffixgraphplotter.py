import os
from trnltk.morphology.morphotactics.suffixgraph import *
from trnltk.morphology.morphotactics.extendedsuffixgraph import *


import networkx as nx


def generate_directed_graph(suffix_graph):
    graph=nx.MultiDiGraph()

    possible_edge_group_colors = {'red', 'blue', 'green', 'cyan', 'magenta', 'purple',
                                  'brown', 'orange', 'skyblue', 'turquoise', 'yellowgreen',
                                  'yellow4', 'springgreen4', 'salmon', 'purple', 'lawngreen',
                                  'goldenrod3'}

    for state in suffix_graph.ALL_STATES:
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

    set_same_rank(['NOUN_ROOT', 'VERB_ROOT', 'PRONOUN_ROOT', 'NUMERAL_ROOT'], A, 'source')
#    set_same_rank(['VERB_WITH_POLARITY', 'VERB_COPULA_WITHOUT_TENSE'], A)
#
#    set_same_rank([node.name for node in filter(lambda node : node.name.endswith('TERMINAL_TRANSFER'), A.nodes())], A)
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
        print sys.argv[0] + " {S|E}  <output file path> \n Type S is simple, and type E is extended (with copula, etc.)"
        sys.exit(2)

    graph_type = sys.argv[1]
    output_file_path = sys.argv[2]

    suffix_graph = None
    if(graph_type=='S'):
        suffix_graph = SuffixGraph()
    elif(graph_type=='E'):
        suffix_graph = ExtendedSuffixGraph()

    if not suffix_graph:
        print "Unknown graph type : {} ".format(graph_type)
        sys.exit(2)

    di_graph = generate_directed_graph(suffix_graph)
    write_graph_to_file(di_graph, output_file_path, os.path.splitext(output_file_path)[1][1:])