#
# graphEnricher.py
#

# import modules
from const_project import FILE_INI_GRAPH, DIRS_DATA_GNN
from funct_topo import *

# from GraphNeighbor import GraphNeighbor

def graphEnrich(plot_graph=False):

    # - - - - - - - - - - - - - - 
    # collect the built Graph data.
    with open(FILE_INI_GRAPH, 'rb') as f:
        G_all = pickle.load(f)

    # - - - - - - - - - - - - - - 
    # visualization settings.
    nodesize_map_by_object_type = {
        'door':100,
        'window':100,
        'wall':200,
        'separationline':200,
        'space':250,
        }

    nodecolor_map_by_object_type = {
        'door':'darkorange',
        'window':'gold',
        'wall':'maroon',
        'separationline':'navy',
        'space':'green',
        }
    
    # - - - - - - - - - - - - - -
    # create a dictory covering a specific graph per rule.

    G = copy.deepcopy(G_all)
    
    # search neighbor.
    
    # # plot the whole networkx.
    # if plot_graph:
    #     plot_networkx_per_rule(
    #         DIRS_DATA_GNN,
    #         G,
    #         nodesize_map_by_object_type,
    #         nodecolor_map_by_object_type,
    #         )
    
    # # split the graph to subgraphs
    # node_classification = nx.get_node_attributes(G,'classification')
    # node_level = nx.get_node_attributes(G,'level')
    # node_name = nx.get_node_attributes(G,'name')

    # space_levels = [node_level[key] for key in node_classification.keys() if node_classification[key] == 'space']
    # space_levels = list(set(space_levels))

    # for l in space_levels:
    #     nodes = (
    #         node for node, data in G.nodes(data=True) if data.get("level") == l
    #     )
    #     subgraph = G.subgraph(nodes)
    # subgraph.nodes  # NodeView((1, 2, 3))