__author__ = 'ali'


from trnltk.suffixgraph.suffixgraph import *

import networkx as nx


def generate_directed_graph():
    graph=nx.MultiDiGraph()

    possible_edge_group_colors = {'red', 'blue', 'yellow', 'green', 'cyan'}

    for state in ALL_STATES:
        colormap = dict()

        for (suffix, output_state) in state.outputs:
            label = '{}({})'.format(suffix.name, suffix.rank)
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

        if state.name in graph:
            if state.type==State.TERMINAL:
                graph.node[state.name]['shape'] = 'doubleoctagon'
            elif state.type==State.DERIV:
                graph.node[state.name]['shape'] = 'house'

    return graph

def write_graph_to_file(graph, file_path):
    A=nx.to_agraph(graph)
    A.write(file_path)

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print "Usage:\n"
        print sys.argv[0] + " <output file path> \n"
        sys.exit(2)

    output_file_path = sys.argv[1]

    di_graph = generate_directed_graph()
    write_graph_to_file(di_graph, output_file_path)