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

    