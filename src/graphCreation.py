#
# graphCreation.py
#

# import modules
from const_project import DIRS_DATA_TOPO, DIRS_DATA_RES
from const_project import NAME_TOPO_OBJECT, NAME_TOPO_SPACE, FILE_INI_GRAPH, FILE_INI_GRAPH_ACCESS

from funct_topo import *

def graphCreate(plot_graph_accessibility=False):

    # object-based
    FILE_OBJECT_HOST = DIRS_DATA_TOPO + NAME_TOPO_OBJECT + 'host.txt'
    FILE_OBJECT_WALLS = DIRS_DATA_TOPO + NAME_TOPO_OBJECT + 'walls.txt'
    FILE_OBJECT_SLABS = DIRS_DATA_TOPO + NAME_TOPO_OBJECT + 'slabs.txt'
    FILE_OBJECT_INSERTS = DIRS_DATA_TOPO + NAME_TOPO_OBJECT + 'inserts.txt'

    id_wall_host, id_wall_inserts, id_wall_walls, id_wall_slabs = [],[],[],[]
    with open(FILE_OBJECT_HOST) as file:
        for line in file:
            id_wall_host.append(line.rstrip())
    with open(FILE_OBJECT_WALLS) as file:
        for line in file:
            id_wall_walls.append(line.rstrip())
    with open(FILE_OBJECT_SLABS) as file:
        for line in file:
            id_wall_slabs.append(line.rstrip())
    with open(FILE_OBJECT_INSERTS) as file:
        for line in file:
            id_wall_inserts.append(line.rstrip())

    # space-based
    FILE_SPACE_HOST = DIRS_DATA_TOPO + NAME_TOPO_SPACE + 'host.txt'
    FILE_SPACE_WALLS = DIRS_DATA_TOPO + NAME_TOPO_SPACE + 'walls.txt'
    FILE_SPACE_DOORS = DIRS_DATA_TOPO + NAME_TOPO_SPACE + 'doors.txt'
    FILE_SPACE_WINDOWS = DIRS_DATA_TOPO + NAME_TOPO_SPACE + 'windows.txt'
    FILE_SPACE_SEPARATIONS = DIRS_DATA_TOPO + NAME_TOPO_SPACE + 'separationlines.txt'

    id_space_host, id_space_walls, id_space_doors, id_space_windows, id_space_separationlines = [],[],[],[],[]
    with open(FILE_SPACE_HOST) as file:
        for line in file:
            id_space_host.append(line.rstrip()) # ok
    with open(FILE_SPACE_WALLS) as file:
        for line in file:
            id_space_walls.append(line.rstrip()) # ok
    with open(FILE_SPACE_DOORS) as file:
        for line in file:
            id_space_doors.append(line.rstrip()) # ok
    with open(FILE_SPACE_WINDOWS) as file:
        for line in file:
            id_space_windows.append(line.rstrip())
    with open(FILE_SPACE_SEPARATIONS) as file:
        for line in file:
            id_space_separationlines.append(line.rstrip())

    # ==================== manual correction!
    id_wall_inserts.append('')
    id_space_separationlines.append('')
    # ==================== manual correction!
    
    # Build networkx edges 
    # wall-based edges.
    id_wall_host_indi = split_ids(id_wall_host)
    id_wall_walls_indi = split_ids(id_wall_walls)
    id_wall_inserts_indi = split_ids(id_wall_inserts)
    id_wall_slabs_indi = split_ids(id_wall_slabs)

    edges_wall_h_walls = build_id_edges(id_wall_host_indi, id_wall_walls_indi)
    edges_wall_h_inserts = build_id_edges(id_wall_host_indi, id_wall_inserts_indi)
    edges_wall_h_slabs = build_id_edges(id_wall_host_indi, id_wall_slabs_indi)

    df_edges_wall_h_walls = pd.DataFrame.from_records(edges_wall_h_walls, columns = ['host','target'])
    df_edges_wall_h_inserts = pd.DataFrame.from_records(edges_wall_h_inserts, columns = ['host','target'])
    df_edges_wall_h_slabs = pd.DataFrame.from_records(edges_wall_h_slabs, columns = ['host','target'])

    # space-based edges.
    id_space_host_indi = split_ids(id_space_host)
    id_space_walls_indi = split_ids(id_space_walls)
    id_space_doors_indi = split_ids(id_space_doors)
    id_space_windows_indi = split_ids(id_space_windows)
    id_space_separationlines_indi = split_ids(id_space_separationlines, remove_repeat=True) 

    edges_space_h_walls = build_id_edges(id_space_host_indi, id_space_walls_indi)
    edges_space_h_doors = build_id_edges(id_space_host_indi, id_space_doors_indi)
    edges_space_h_windows = build_id_edges(id_space_host_indi, id_space_windows_indi)
    edges_space_h_separationlines = build_id_edges(id_space_host_indi, id_space_separationlines_indi)

    df_edges_space_h_walls = pd.DataFrame.from_records(edges_space_h_walls, columns = ['host','target'])
    df_edges_space_h_doors = pd.DataFrame.from_records(edges_space_h_doors, columns = ['host','target'])
    df_edges_space_h_windows = pd.DataFrame.from_records(edges_space_h_windows, columns = ['host','target'])
    df_edges_space_h_separationlines = pd.DataFrame.from_records(edges_space_h_separationlines, columns = ['host','target'])

    # Build networkx attributes
    # object attributes
    index_col_name = 'id'
    df_doorinstances = pd.read_csv(DIRS_DATA_TOPO+'\df_door.csv', index_col =index_col_name, dtype={'id':str})
    df_windowinstances = pd.read_csv(DIRS_DATA_TOPO+'\df_window.csv', index_col =index_col_name, dtype={'id':str})
    df_wallinstances = pd.read_csv(DIRS_DATA_TOPO+'\df_wall.csv', index_col =index_col_name, dtype={'id':str})
    df_slabinstances = pd.read_csv(DIRS_DATA_TOPO+'\df_slab.csv', index_col =index_col_name, dtype={'id':str})

    attrs_door = df_doorinstances.to_dict(orient = 'index')
    attrs_window = df_windowinstances.to_dict(orient = 'index')
    attrs_wall = df_wallinstances.to_dict(orient = 'index')
    attrs_slab = df_slabinstances.to_dict(orient = 'index')
    
    # space attributes
    df_spaceinstances = pd.read_csv(DIRS_DATA_TOPO+'\df_space.csv', index_col =index_col_name, dtype={'id':str})
    attrs_space = df_spaceinstances.to_dict(orient = 'index')

    # separation line attributes.
    df_separationlineinstances = pd.read_csv(DIRS_DATA_TOPO+'\df_separationline.csv', index_col = index_col_name, dtype={'id':str})
    attrs_separationline = df_separationlineinstances.to_dict(orient = 'index')

    # ================================ for ec3.

    # ------------------------- for vertical graph.
    all_df_edges = [df_edges_wall_h_walls, df_edges_wall_h_inserts, df_edges_space_h_walls, df_edges_space_h_separationlines]
    all_dict_attrs = [attrs_door, attrs_window, attrs_wall, attrs_space, attrs_separationline]

    # save to a networkx graph.
    G_all = build_networkx_graph(all_df_edges, all_dict_attrs)
    pickle.dump(G_all, open(FILE_INI_GRAPH, 'wb'))

    #  save all the required edges to csvs.
    df_edges_space_h_walls.to_csv(DIRS_DATA_RES +'\df_pairs_space_to_wall_tempo.csv', index=False)
    df_edges_wall_h_inserts.to_csv(DIRS_DATA_RES +'\df_pairs_wall_to_opening_tempo.csv', index=False)

    # ------------------------- for horizontal graph.
    accessibility_df_edges = [df_edges_space_h_doors, df_edges_space_h_separationlines]
    accessibility_df_attrs = [attrs_door, attrs_space, attrs_separationline]
    accessibility_G_all = build_networkx_graph(accessibility_df_edges, accessibility_df_attrs)
    pickle.dump(accessibility_G_all, open(FILE_INI_GRAPH_ACCESS, 'wb'))

    if plot_graph_accessibility:

        # visualization settings.
        nodesize_map_by_object_type = {
            'door':100,
            'separationline':100,
            'space':200,
            }

        nodecolor_map_by_object_type = {
            'door':'black',
            'separationline':'darkgreen',
            'space':'darkorange',
            }
        
        with open(FILE_INI_GRAPH_ACCESS, 'rb') as f:
            UG = pickle.load(f)

        # - - - - - - - - - - - - - - 
        sub_graphs = [UG.subgraph(c).copy() for c in nx.connected_components(UG)]
        
        for i, SG in enumerate(sub_graphs):

            fig = plt.figure(figsize=(30, 18))
            ax = plt.axes((0.05, 0.05, 0.90, 0.90))
            G_nodes_sizes = [nodesize_map_by_object_type[SG.nodes[n]['classification']]
                            for n in SG]
            G_nodes_colors = [nodecolor_map_by_object_type[SG.nodes[n]['classification']]
                            for n in SG]

            nx.draw_networkx(
                SG,
                # pos=nx.kamada_kawai_layout(UG, scale=0.75),
                # pos = nx.spiral_layout(G, scale=pos_layout_scale),
                arrows=True,
                with_labels=False,
                node_size=G_nodes_sizes,
                node_shape="o",
                node_color=G_nodes_colors,
                linewidths=0.1,
                width=2,
                alpha=0.80,
                edge_color='black')
            ax.title.set_position([.5, 0.975])

            for kk in list(nodecolor_map_by_object_type.keys()):
                plt.scatter([], [], c=nodecolor_map_by_object_type[kk], label=kk)

            plt.legend(fontsize="xx-large", ncol=4, loc=(0.40,0.025))
            plt.savefig(DIRS_DATA_RES + '\\plotting_G_{}.png'.format(i), dpi=200)