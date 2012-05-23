__author__ = 'ali'


from trnltk.suffixgraph.suffixgraph import *

import networkx as nx
import matplotlib.pyplot as plt
import pygraphviz as pgv


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


A=nx.to_agraph(graph)
A.write("../resources/suffix_graph.dot")