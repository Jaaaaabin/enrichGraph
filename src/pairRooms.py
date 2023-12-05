from const_project import DIRS_DATA_TOPO
import pandas as pd

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
            if len(spaces) == 2:  # Assuming one door connects exactly two spaces
                space_pair = tuple(sorted(spaces))
                space_pairs.add(space_pair)
            else:
                print(f"The {pair_connection_type} connects more than two spaces: {spaces}")

        output_file_per_level = output_file + level + '.txt'
        # Write the pairs to the output file
        with open(output_file_per_level, 'w') as out_file:
            for pair in space_pairs:
                out_file.write(f"{pair[0]}, {pair[1]}\n")


# Specify the input and output file names
filepath = DIRS_DATA_TOPO

spaces_csv_file = filepath + r'\df_space.csv'

host_file = filepath + r'\collected_topology_space_host.txt'
doors_file = filepath + r'\collected_topology_space_doors.txt'
separationlines_file = filepath + r'\collected_topology_space_separationlines.txt'

output_file_by_door = filepath + r'\space_pairs_by_doors_'
output_file_by_separationline = filepath + r'\space_pairs_by_separationlines_'

def getRoomPairs():
    
    # Use the function to get space pairs and write them to a file
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