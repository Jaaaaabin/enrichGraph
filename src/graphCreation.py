#
# graphCreation.py
#

# import modules
from const_project import DIRS_DATA_TOPO
from const_project import NAME_TOPO_OBJECT, NAME_TOPO_SPACE, FILE_INI_GRAPH

from funct_topo import *

def graphCreate():
    
    # object-based
    FILE_OBJECT_HOST = DIRS_DATA_TOPO + NAME_TOPO_OBJECT + 'host.txt'
    FILE_OBJECT_WALLS = DIRS_DATA_TOPO + NAME_TOPO_OBJECT + 'walls.txt'
    FILE_OBJECT_SLABS = DIRS_DATA_TOPO + NAME_TOPO_OBJECT + 'slabs.txt'
    FILE_OBJECT_INSERTS = DIRS_DATA_TOPO + NAME_TOPO_OBJECT + 'inserts.txt'

    guid_wall_host, guid_wall_inserts, guid_wall_walls, guid_wall_slabs = [],[],[],[]
    with open(FILE_OBJECT_HOST) as file:
        for line in file:
            guid_wall_host.append(line.rstrip())
    with open(FILE_OBJECT_WALLS) as file:
        for line in file:
            guid_wall_walls.append(line.rstrip())
    with open(FILE_OBJECT_SLABS) as file:
        for line in file:
            guid_wall_slabs.append(line.rstrip())
    with open(FILE_OBJECT_INSERTS) as file:
        for line in file:
            guid_wall_inserts.append(line.rstrip())      
    guid_wall_inserts.append('') # due to the ISSUE:miss the last line for guid_wall_inserts

    # space-based
    FILE_SPACE_HOST = DIRS_DATA_TOPO + NAME_TOPO_SPACE + 'host.txt'
    FILE_SPACE_WALLS = DIRS_DATA_TOPO + NAME_TOPO_SPACE + 'walls.txt'
    FILE_SPACE_DOORS = DIRS_DATA_TOPO + NAME_TOPO_SPACE + 'doors.txt'
    FILE_SPACE_WINDOWS = DIRS_DATA_TOPO + NAME_TOPO_SPACE + 'windows.txt'
    FILE_SPACE_SEPARATIONS = DIRS_DATA_TOPO + NAME_TOPO_SPACE + 'separationlines.txt'

    guid_space_host, guid_space_walls, guid_space_doors, guid_space_windows, guid_space_separationlines = [],[],[],[],[]
    with open(FILE_SPACE_HOST) as file:
        for line in file:
            guid_space_host.append(line.rstrip())
    with open(FILE_SPACE_WALLS) as file:
        for line in file:
            guid_space_walls.append(line.rstrip())
    with open(FILE_SPACE_DOORS) as file:
        for line in file:
            guid_space_doors.append(line.rstrip())
    with open(FILE_SPACE_WINDOWS) as file:
        for line in file:
            guid_space_windows.append(line.rstrip())
    with open(FILE_SPACE_SEPARATIONS) as file:
        for line in file:
            guid_space_separationlines.append(line.rstrip())
    guid_space_separationlines.append('') # due to the ISSUE:miss the last line for guid_wall_inserts

    # Build networkx edges 
    # wall-based edges.
    guid_wall_host_indi = split_guids(guid_wall_host)
    guid_wall_walls_indi = split_guids(guid_wall_walls)
    guid_wall_inserts_indi = split_guids(guid_wall_inserts)
    guid_wall_slabs_indi = split_guids(guid_wall_slabs)

    edges_wall_h_walls = build_guid_edges(guid_wall_host_indi, guid_wall_walls_indi)
    edges_wall_h_inserts = build_guid_edges(guid_wall_host_indi, guid_wall_inserts_indi)
    edges_wall_h_slabs = build_guid_edges(guid_wall_host_indi, guid_wall_slabs_indi)

    df_edges_wall_h_walls = pd.DataFrame.from_records(edges_wall_h_walls, columns = ['host','target'])
    df_edges_wall_h_inserts = pd.DataFrame.from_records(edges_wall_h_inserts, columns = ['host','target'])
    df_edges_wall_h_slabs = pd.DataFrame.from_records(edges_wall_h_slabs, columns = ['host','target'])

    # space-based edges.
    guid_space_host_indi = split_guids(guid_space_host)
    guid_space_walls_indi = split_guids(guid_space_walls)
    guid_space_doors_indi = split_guids(guid_space_doors)
    guid_space_windows_indi = split_guids(guid_space_windows)
    guid_space_separationlines_indi = split_guids(guid_space_separationlines, remove_repeat=True) 

    edges_space_h_walls = build_guid_edges(guid_space_host_indi, guid_space_walls_indi)
    edges_space_h_doors = build_guid_edges(guid_space_host_indi, guid_space_doors_indi)
    edges_space_h_windows = build_guid_edges(guid_space_host_indi, guid_space_windows_indi)
    edges_space_h_separationlines = build_guid_edges(guid_space_host_indi, guid_space_separationlines_indi)

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

    ## =================================EC3. first part.
    # all_df_edges = [df_edges_space_h_separationlines, df_edges_space_h_doors]

    # ## =================================EC3. second part.
    all_df_edges = [df_edges_wall_h_walls, df_edges_wall_h_inserts, df_edges_space_h_walls, df_edges_space_h_separationlines]
    all_dict_attrs = [attrs_door, attrs_window, attrs_wall, attrs_space, attrs_separationline]

    G_all = build_networkx_graph(all_df_edges, all_dict_attrs)
    pickle.dump(G_all, open(FILE_INI_GRAPH, 'wb'))