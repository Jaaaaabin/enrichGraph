#
# featureCollection.py
#

# import modules
from const_project import DIRS_DATA_GNN, DIRS_DATA_RES, NAME_FEATURE_COLLECTION, NAME_FEATURES_INSTANCES, NAME_FEATURES_INSTANCES_ARE
from const_project import NAME_FEATURE_INSTANCES_UNIT_DY, NAME_FEATURE_INSTANCES_UNIT_CM, CT_METER2FEET
from funct_topo import *


def featureCollect():

    for feature_inst in NAME_FEATURES_INSTANCES:

        # set files
        df_instance_init =  DIRS_DATA_GNN + NAME_FEATURE_COLLECTION + feature_inst + '.csv'
        df_instance_init = pd.read_csv(df_instance_init, header=0)
        df_instance_init = df_instance_init.fillna(0)

        for c in df_instance_init.columns.to_list():
            
            # feet to meter
            if c in NAME_FEATURE_INSTANCES_UNIT_DY:
                df_instance_init[c] = df_instance_init[c].apply(lambda x: round(x/CT_METER2FEET,2))
            
            # cm to m.
            if c in NAME_FEATURE_INSTANCES_UNIT_CM:
                df_instance_init[c] = df_instance_init[c].apply(lambda x: x*0.01)

        # area calculation.
        if feature_inst in NAME_FEATURES_INSTANCES_ARE:

            df_instance_init['area'] = df_instance_init['height'] * df_instance_init['width']

        else:
            df_instance_init['area'] = 0
        
        # add classes.
        for inst in NAME_FEATURES_INSTANCES[1:]:
            df_instance_init[inst] = 1 if inst==feature_inst else 0
        
        df_instance = df_instance_init
        df_instance.to_csv(
            DIRS_DATA_RES+'\df_feature_'+ feature_inst +'.csv',
            index=False,
            encoding = 'utf-8-sig')# encoding = 'utf-8-sig' for special characters.

def cleanCSVPairs(csv_file_path, output_file_path):

    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path, header=None)

    # Assuming the ID pairs are in the first two columns
    # Sort each pair to ensure (A, B) and (B, A) are treated as the same
    df_sorted = df.apply(lambda x: sorted(x), axis=1)
    df_sorted = pd.DataFrame(df_sorted.tolist(), columns=df.columns)

    # Drop duplicate rows
    df_cleaned = df_sorted.drop_duplicates()

    # Save the cleaned DataFrame to a new CSV file
    df_cleaned.to_csv(output_file_path, index=False, header=False)

def compareCSVFiles(path_1, path_2, diff_path, overlap_path):

    def read_and_sort_csv(file_path):
        df = pd.read_csv(file_path, header=None)
        df_sorted = df.apply(lambda x: sorted(x), axis=1)
        return pd.DataFrame(df_sorted.tolist(), columns=df.columns)

    # Read and sort both CSV files
    df1 = read_and_sort_csv(path_1)
    df2 = read_and_sort_csv(path_2)

    # Find different and overlapping pairs
    different_pairs = pd.concat([df1, df2]).drop_duplicates(keep=False)
    overlapping_pairs = df1.merge(df2).drop_duplicates()

    # Save the results to separate CSV files
    different_pairs.to_csv(diff_path, index=False, header=False)
    overlapping_pairs.to_csv(overlap_path, index=False, header=False)

def mergeEdgesinCSV():
    
    def combine_csv_files(csv_files):

        # Create an empty DataFrame to store combined data
        combined_df = pd.DataFrame()

        # Loop through each file and append to the DataFrame
        for file in csv_files:
            df = pd.read_csv(file, header=None)
            combined_df = pd.concat([combined_df, df])

        # Reset the index of the combined DataFrame
        combined_df.reset_index(drop=True, inplace=True)

        return combined_df
    
    edge_csv_files = [
        DIRS_DATA_RES + '\df_pairs_space_intersection.csv',
        DIRS_DATA_RES + '\df_pairs_space_intersection_to_wall.csv',
        DIRS_DATA_RES + '\df_pairs_wall_intersection.csv',
        DIRS_DATA_RES + '\df_pairs_space_intersection_to_wall_to_opening.csv']
    
    combined_edge_csv_path = DIRS_DATA_RES + '\df_all_edges.csv'
    combined_edge_df = combine_csv_files(edge_csv_files)
    combined_edge_df.to_csv(combined_edge_csv_path, index=False, header=False)

    feature_csv_files = [
        DIRS_DATA_RES + '\df_feature_space.csv',
        DIRS_DATA_RES + '\df_feature_wall.csv',
        DIRS_DATA_RES + '\df_feature_window.csv',
        DIRS_DATA_RES + '\df_feature_door.csv',]

    combined_feature_csv_path = DIRS_DATA_RES + '\df_all_features_all.csv'
    combined_feature_df = combine_csv_files(feature_csv_files)
    combined_feature_df.to_csv(combined_feature_csv_path, index=False, header=False)

def FilterIds(
        
    edge_csv_file=DIRS_DATA_RES + '\df_all_edges.csv', 
    feature_csv_file=DIRS_DATA_RES + '\df_all_features_all.csv', 
    output_csv=DIRS_DATA_RES + '\df_all_features.csv'):

    # Read CSV1 and extract IDs from the first column
    df_edge = pd.read_csv(edge_csv_file, header=None)
    ids_from_edges = set(df_edge[0]).union(set(df_edge[1]))

    # Read CSV2
    df_features = pd.read_csv(feature_csv_file)

    # Filter rows from CSV2 where the ID is in CSV1
    filtered_df = df_features[df_features.iloc[:, 0].isin(ids_from_edges)]

    # Save the filtered DataFrame to a new CSV file
    filtered_df.to_csv(output_csv, index=False)