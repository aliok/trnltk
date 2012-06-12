__author__ = 'ali'


from trnltk.suffixgraph.suffixgraph import *
from trnltk.suffixgraph.extendedsuffixgraph import *


import networkx as nx


def generate_directed_graph(suffix_graph):
    graph=nx.MultiDiGraph()

    possible_edge_group_colors = {'red', 'blue', 'yellow', 'green', 'cyan', 'magenta', 'purple', 'brown', 'orange', 'skyblue', 'turquoise'}

    for state in suffix_graph.ALL_STATES:
        graph.add_node(state.name)
        if state.name in graph:
            if state.type==State.TERMINAL:
                graph.node[state.name]['shape'] = 'doubleoctagon'
            elif state.type==State.DERIV:
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

def write_graph_to_file(graph, file_path):
    A=nx.to_agraph(graph)

    roots_sub_graph = A.add_subgraph('roots')
    roots_sub_graph.graph_attr['rank'] = 'same'

    roots_sub_graph.add_node('NOUN_ROOT')
    roots_sub_graph.add_node('VERB_ROOT')
    roots_sub_graph.add_node('PRONOUN_ROOT')


    terminals_sub_graph = A.add_subgraph('terminals')
    terminals_sub_graph.graph_attr['rank'] = 'same'

    terminal_transfers_sub_graph = A.add_subgraph('terminal_transfers')
    terminal_transfers_sub_graph.graph_attr['rank'] = 'same'

    for node in A.nodes_iter():
        if node.endswith('TERMINAL'):
            terminals_sub_graph.add_node(node)
        elif node.endswith('TERMINAL_TRANSFER'):
            terminal_transfers_sub_graph.add_node(node)

    A.write(file_path)

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
    write_graph_to_file(di_graph, output_file_path)