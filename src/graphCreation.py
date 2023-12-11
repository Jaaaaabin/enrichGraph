#
# graphCreation.py
#

# import modules
from const_project import DIRS_DATA_TOPO, DIRS_DATA_RES
from const_project import NAME_TOPO_OBJECT, NAME_TOPO_SPACE, FILE_INI_GRAPH

from funct_topo import *

def graphCreate():
    
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
    
    id_space_windows.append('')
    id_space_separationlines.append('')

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
    all_df_edges = [df_edges_wall_h_walls, df_edges_wall_h_inserts, df_edges_space_h_walls, df_edges_space_h_separationlines]
    all_dict_attrs = [attrs_door, attrs_window, attrs_wall, attrs_space, attrs_separationline]

    # save to a networkx graph.
    G_all = build_networkx_graph(all_df_edges, all_dict_attrs)
    pickle.dump(G_all, open(FILE_INI_GRAPH, 'wb'))

    # ================================ save all the required edges to csvs.
    # ------------------------- Space to Wall
    df_edges_space_h_walls.to_csv(DIRS_DATA_RES +'\df_pairs_space_to_wall_tempo.csv', index=False)

    # -------------------------- Wall to windows and doors.
    df_edges_wall_h_inserts.to_csv(DIRS_DATA_RES +'\df_pairs_wall_to_opening_tempo.csv', index=False)

