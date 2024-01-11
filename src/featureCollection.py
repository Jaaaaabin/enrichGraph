#
# featureCollection.py
#

# import modules
from const_project import DIRS_DATA_TOPO, NAME_INSTANCE_COLLECTION
from const_project import DIRS_DATA_GNN, DIRS_DATA_RES, NAME_FEATURE_COLLECTION, NAME_FEATURES_INSTANCES, NAME_FEATURES_INSTANCES_ARE, NAME_FEATURES_INSTANCES_INPUTARE
# from const_project import NAME_FEATURE_INSTANCES_UNIT_DY, NAME_FEATURE_INSTANCES_UNIT_CM, CT_METER2FEET
from funct_topo import *

def list_of_dicts_to_dict(list_of_dicts, key_as_new_key):
    """
    Convert a list of dictionaries to a dictionary with specified key as new keys.

    :param list_of_dicts: List of dictionaries.
    :param key_as_new_key: The key in the original dicts to use as the new keys.
    :return: A new dictionary with keys from key_as_new_key and remaining part of dicts as values.
    """
    new_dict = {}

    for d in list_of_dicts:
        if key_as_new_key in d:
            # Extract the value for the new key
            new_key = d[key_as_new_key]

            # Create a new dict from the original, excluding the new key
            new_value = {k: v for k, v in d.items() if k != key_as_new_key}

            new_dict[new_key] = new_value

    return new_dict


def featureCollect():

    for feature_inst in NAME_FEATURES_INSTANCES:

        # bounding box files
        df_feature_init =  DIRS_DATA_GNN + NAME_FEATURE_COLLECTION + feature_inst + '.csv'
        df_feature_init = pd.read_csv(df_feature_init, header=0)
        df_feature_init = df_feature_init.fillna(0)

        # for c in df_feature_init.columns.to_list():
            # # feet to meter
            # if c in NAME_FEATURE_INSTANCES_UNIT_DY:
            #     df_feature_init[c] = df_feature_init[c].apply(lambda x: round(x/CT_METER2FEET,2))
            # # cm to m.
            # if c in NAME_FEATURE_INSTANCES_UNIT_CM:
            #     df_feature_init[c] = df_feature_init[c].apply(lambda x: x*0.01)

        if feature_inst == 'wall':
            df_feature_init ['width'] = 0
        
        # area calculation.
        if feature_inst in NAME_FEATURES_INSTANCES_ARE:

            df_feature_init['area'] = df_feature_init['height'] * df_feature_init['width']

        elif feature_inst in NAME_FEATURES_INSTANCES_INPUTARE:
            
            # load the additional feature files from Revit 
            js_file_instance = DIRS_DATA_TOPO + NAME_INSTANCE_COLLECTION + feature_inst + '.json'
            
            with open(js_file_instance, encoding="utf-8-sig") as json_file: # encoding = 'utf-8-sig' for special characters.
                revit_instances = json.load(json_file)

            new_revit_instances = list_of_dicts_to_dict(revit_instances, 'Id')
            def getInstanceArea(instance_id):
                str_id = str(instance_id)
                return new_revit_instances[str_id]['Area']

            df_feature_init['area'] = df_feature_init['id'].apply(getInstanceArea)

        else:
            df_feature_init['area'] = 0
        
        # add classes.
        for inst in NAME_FEATURES_INSTANCES[1:]:
            df_feature_init[inst] = 1 if inst==feature_inst else 0
        
        df_instance = df_feature_init
        df_instance.to_csv(
            DIRS_DATA_RES+'\df_feature_'+ feature_inst +'.csv',
            index=False,
            encoding = 'utf-8-sig')# encoding = 'utf-8-sig' for special characters.

def mergeEdgesinCSV():
    
    def combine_csv_files(csv_files):

        # Create an empty DataFrame to store combined data
        combined_df = pd.DataFrame()

        # Loop through each file and append to the DataFrame
        for file in csv_files:
            df = pd.read_csv(file)
            combined_df = pd.concat([combined_df, df])

        # Reset the index of the combined DataFrame
        combined_df.reset_index(drop=True, inplace=True)

        return combined_df
    
    # edges.
    edge_csv_files = [
        DIRS_DATA_RES + '\df_pairs_space_intersection.csv',
        DIRS_DATA_RES + '\df_pairs_space_intersection_to_wall.csv',
        DIRS_DATA_RES + '\df_pairs_wall_intersection.csv',
        DIRS_DATA_RES + '\df_pairs_space_intersection_to_wall_to_opening.csv']
    
    combined_edge_csv_path = DIRS_DATA_RES + '\df_all_edges.csv'
    combined_edge_df = combine_csv_files(edge_csv_files)

    df_getcolumns = pd.read_csv(edge_csv_files[0])
    combined_edge_df.columns = df_getcolumns.columns

    combined_edge_df.to_csv(combined_edge_csv_path, index=False, header=True)

    # features.
    feature_csv_files = [
        DIRS_DATA_RES + '\df_feature_space.csv',
        DIRS_DATA_RES + '\df_feature_wall.csv',
        DIRS_DATA_RES + '\df_feature_window.csv',
        DIRS_DATA_RES + '\df_feature_door.csv',]

    combined_feature_csv_path = DIRS_DATA_RES + '\df_all_features_all.csv'
    combined_feature_df = combine_csv_files(feature_csv_files)

    # df_getcolumns = pd.read_csv(feature_csv_files[0])
    # combined_feature_df.columns = df_getcolumns.columns

    combined_feature_df.to_csv(combined_feature_csv_path, index=False, header=True)

def FilterIds(
    edge_csv_file=DIRS_DATA_RES + '\df_all_edges.csv', 
    feature_csv_file=DIRS_DATA_RES + '\df_all_features_all.csv', 
    output_csv=DIRS_DATA_RES + '\df_all_features.csv'):

    # Read CSV1 and extract IDs from the first column
    df_edge = pd.read_csv(edge_csv_file, header=0)
    
    # ids_from_edges = set(df_edge['host']).union(set(df_edge['target']))
    ids_from_edges = df_edge.values.tolist()
    ids_from_edges = list(set([item for sublist in ids_from_edges for item in sublist]))

    # Read CSV2
    df_features = pd.read_csv(feature_csv_file)

    # Filter rows from CSV2 where the ID is in CSV1
    filtered_df = df_features[df_features.iloc[:, 0].isin(ids_from_edges)]

    # Save the filtered DataFrame to a new CSV file
    filtered_df.to_csv(output_csv, index=False)

# unused.
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

#
def compareCSVFiles(
    path_1,
    path_2,
    diff_path,
    overlap_path,
    database_path = DIRS_DATA_RES + '\df_all_features_all.csv'):

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
    overlapping_pairs.to_csv(overlap_path, index=False, header=False)
    different_pairs.to_csv(diff_path, index=False, header=False)

    # further analysis.
    different_pairs.reset_index(drop=True, inplace=True)
    split_index = different_pairs.index[different_pairs[different_pairs.columns.values.tolist()[0]] == 'Source'].tolist()

    unique_data_auto = different_pairs.iloc[:split_index[0],:]
    unique_data_manu = different_pairs.iloc[split_index[0]:,:]

    def pdFirstRowAsHeader(ini_pd):
        
        new_header = ini_pd.iloc[0] #grab the first row for the header
        ini_pd = ini_pd[1:] #take the data less the header row
        ini_pd.columns = new_header
        ini_pd.reset_index(drop=True, inplace=True)
        
        return ini_pd

    unique_data_auto = pdFirstRowAsHeader(unique_data_auto)
    unique_data_manu = pdFirstRowAsHeader(unique_data_manu)

    def enrichAviaB(
        df_data,
        df_database_all,
        labels = ['',''],
        classes=['id', 'space','wall','door','window']):

        # Select only the class columns.
        df_database = copy.deepcopy(df_database_all[classes])

        # Merge DataFrame A with DataFrame B to via the 'host' column
        df_database.rename(
            columns={'id': labels[0]}, inplace = True)
        df_database[labels[0]] = df_database[labels[0]].astype(int)
        df_data[labels[0]] = df_data[labels[0]].astype(int)
        df_data = df_data.merge(df_database, how='inner', on=labels[0])

        # Rename the relevant column from DataFrame B to 'host class'
        df_data.rename(
            columns={
                'space': labels[0] + '-' + 'space',
                'wall': labels[0] + '-' + 'wall',
                'door': labels[0] + '-' + 'door',
                'window': labels[0] + '-' + 'window',
                }, inplace=True)

        # Merge DataFrame A with DataFrame B to via the 'target' column
        df_database.rename(
            columns={labels[0]: labels[1]}, inplace = True)
        df_database[labels[1]] = df_database[labels[1]].astype(int)
        df_data[labels[1]] = df_data[labels[1]].astype(int)
        df_data = df_data.merge(df_database, how='inner', on=labels[1])

        # Rename the relevant column from DataFrame B to 'target class'
        df_data.rename(
            columns={
                'space': labels[1] + '-' + 'space',
                'wall': labels[1] + '-' + 'wall',
                'door': labels[1] + '-' + 'door',
                'window': labels[1] + '-' + 'window',
                }, inplace=True)

        return df_data

    df_database_all = pd.read_csv(database_path, header=0)
    enriched_unique_data_auto = enrichAviaB(unique_data_auto, df_database_all, labels=['host','target'])
    enriched_unique_data_manu = enrichAviaB(unique_data_manu, df_database_all, labels=['Source','Target'])
    
    path_diff_data_auto = diff_path.replace('.csv', '_auto.csv')
    path_diff_data_manu = diff_path.replace('.csv', '_manu.csv')

    enriched_unique_data_auto.to_csv(path_diff_data_auto, index=False, header=True)
    enriched_unique_data_manu.to_csv(path_diff_data_manu, index=False, header=True)