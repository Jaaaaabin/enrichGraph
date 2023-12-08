from const_project import DIRS_DATA_TOPO, DIRS_DATA_RES
import pandas as pd
import itertools

# Specify the input and output file names

spaces_csv_file = DIRS_DATA_TOPO + r'\df_space.csv'

host_file = DIRS_DATA_TOPO + r'\collected_topology_space_host.txt'
doors_file = DIRS_DATA_TOPO + r'\collected_topology_space_doors.txt'
separationlines_file = DIRS_DATA_TOPO + r'\collected_topology_space_separationlines.txt'

output_file_by_door = DIRS_DATA_RES + r'\space_pairs_by_doors_'
output_file_by_separationline = DIRS_DATA_RES + r'\space_pairs_by_separationlines_'

def read_txt_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def get_space_pairs_via_connections_per_level(spaces_file, host_file, host_connections_file, output_file, pair_connection_type=''):
    
    # Read the space and connection data from files
    all_spaces = pd.read_csv(spaces_file, index_col=None)

    space_levels = list(set(all_spaces['level'].tolist()))

    for level in space_levels:
        
        # select the spaces from the level.
        spaces_per_level = all_spaces.loc[all_spaces['level'] == level, 'id'].tolist()

        host_space = read_txt_file(host_file)
        host_connection_list = read_txt_file(host_connections_file)

        # check and remove repeated values in the connection list.
        connections_per_space = [c.replace(',', ' ').split() for c in host_connection_list]
        connections_per_space = [list(set(c)) for c in connections_per_space]

        # Create a dictionary to associate doors with spaces
        dict_connection_to_spaces = {}

        for space, connections in zip(host_space, connections_per_space):
            
            # filter via space levels.
            if int(space) in spaces_per_level:

                for connection in connections:
                    if connection in dict_connection_to_spaces:
                        dict_connection_to_spaces[connection].append(space)
                    else:
                        dict_connection_to_spaces[connection] = [space]

        # Create a set to store unique pairs of spaces
        space_pairs = set()

        # Iterate through the door to space mapping
        for spaces in dict_connection_to_spaces.values():
            
            # one door can only connect two space..
            if pair_connection_type == 'Door':
                
                if len(spaces) == 2:  
                    space_pair = tuple(sorted(spaces))
                    space_pairs.add(space_pair)
                else:
                    print(f"The {pair_connection_type} connects more than two spaces: {spaces}")

            # one separation line can connect more than two spaces..
            elif pair_connection_type == "SeparationLine":

                if len(spaces) == 2:            
                    space_pair = tuple(sorted(spaces))
                    space_pairs.add(space_pair)

                elif len(spaces) > 2:
                    tempo_all_space_pair = itertools.combinations(spaces, 2)
                    all_space_pair = sorted([tuple(space_pair) for space_pair in tempo_all_space_pair])
                    [space_pairs.add(space_pair) for space_pair in all_space_pair]

                else:
                    print(f"The {pair_connection_type} connects less than two spaces: {spaces}")
                    

        output_file_per_level = output_file + level + '.txt'

        # Write the pairs to the output file
        with open(output_file_per_level, 'w') as out_file:
            for pair in space_pairs:
                out_file.write(f"{pair[0]}, {pair[1]}\n")

def getRoomPairs():
    
    get_space_pairs_via_connections_per_level(
        spaces_csv_file,
        host_file,
        doors_file,
        output_file_by_door,
        pair_connection_type='Door')

    get_space_pairs_via_connections_per_level(
        spaces_csv_file,
        host_file,
        separationlines_file,
        output_file_by_separationline,
        pair_connection_type='SeparationLine')