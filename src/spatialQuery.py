#
# spatialQuery.py
#

# import modules
from const_project import DIRS_DATA_RES, NAME_FEATURE_COLLECTION, NAME_FEATURES_INSTANCES, NAME_FEATURES_INSTANCES_ARE

from funct_topo import *

def is_included(box1, box2, tol_inclusion=0.05):
    
    # if box1 is IN box2.
    inclusion_side_min = all(i>=j-tol_inclusion for (i,j) in zip(box1[:3], box2[:3])) # xmin ymin zmin
    inclusion_side_max = all(i<=j+tol_inclusion for (i,j) in zip(box1[3:], box2[3:])) # xmax ymax zmax

    ################################
    # Discussion for the tolerance.
    ################################
    
    return inclusion_side_min and inclusion_side_max

def is_intersected(box1, box2):
    
    # known that box2 is bigger
    # no tolerance.

    # if box1 is IN box2.
    if is_included(box1,box2):

        return False
    
    # if box1 is not IN box2.
    elif (box1[3] >=box2[0] and box2[3] >=box1[0]) and \
        (box1[4] >=box2[1] and box2[4] >=box1[1]) and \
            (box1[5] >=box2[2] and box2[5] >=box1[2]):
        
        return True 

def securityroomQuery():

    sr_feature_inst = NAME_FEATURES_INSTANCES[0]
    secondary_feature_insts = NAME_FEATURES_INSTANCES[1:]

    # read and extend the SR space.
    df_sr_space =  pd.read_csv(
        DIRS_DATA_RES +'\df_feature_'+ sr_feature_inst +'.csv',
        header=0,)
    df_sr_space['zmin'] = df_sr_space['zmin'].apply(lambda x:x-1000)
    df_sr_space['zmax'] = df_sr_space['zmax'].apply(lambda x:x+1000)
    
    secondary_dfs = {}

    for sec_inst in secondary_feature_insts:

        # read all the rest
        df =  pd.read_csv(
            DIRS_DATA_RES +'\df_feature_'+ sec_inst +'.csv',header=0,)

        # add class columns
        for cl in secondary_feature_insts:
            if cl == sec_inst:
                df[cl] = 1
            else:
                df[cl] = 0

        secondary_dfs.update(
            {sec_inst: {'feature': df,},}
                )

    # output.
    df_intersected_all, df_included_all = [], []

    for sec_inst in secondary_feature_insts:

        # Initialize lists to store the indices of included and intersecting rows
        included_indices, intersected_indices  = [], []
        
        # Initialize lists for vertical_box_edges.
        included_pairs_spaces,  intersected_pairs_spaces = [], []

        secondary_df = secondary_dfs[sec_inst]['feature']
        
        # Check each pair of bounding boxes
        # .... vs box of SR space.
        for index_sr, row_sr in df_sr_space.iterrows():
            
            box_sr = pd.Series([row_sr['xmin'], row_sr['ymin'], row_sr['zmin'], row_sr['xmax'], row_sr['ymax'], row_sr['zmax']])
            
            # the secondary box.
            for index_sec, row_sec in secondary_df.iterrows():
                box_second = pd.Series([row_sec['xmin'], row_sec['ymin'], row_sec['zmin'], row_sec['xmax'], row_sec['ymax'], row_sec['zmax']])
                
                # if included.
                if is_included(box_second, box_sr):
                    included_indices.append(index_sec)

                    if sec_inst == 'space':
                        included_pairs_spaces.append([int(row_sr['id']),int(row_sec['id'])])
                
                # if intersected.
                elif is_intersected(box_second, box_sr):
                    intersected_indices.append(index_sec)

                    if sec_inst == 'space':
                        intersected_pairs_spaces.append([int(row_sr['id']),int(row_sec['id'])])
        
        # for vertical_box_edges among spaces.
        if sec_inst == 'space':

            df_included_pairs_spaces = pd.DataFrame(included_pairs_spaces, columns=['host', 'target']).drop_duplicates()
            df_included_pairs_spaces.to_csv(DIRS_DATA_RES + '\df_all_vertical_edges_included.csv', index=False)

            df_intersected_pairs_spaces = pd.DataFrame(intersected_pairs_spaces, columns=['host', 'target']).drop_duplicates()
            df_intersected_pairs_spaces.to_csv(DIRS_DATA_RES + '\df_all_vertical_edges_intersected.csv', index=False)
                
        # record the indices.
        secondary_dfs[sec_inst].update(
            {
                'included_indices': included_indices,
                'intersected_indices': intersected_indices,}
        )

        # write out per category
        df_included = secondary_dfs[sec_inst]['feature'].loc[secondary_dfs[sec_inst]['included_indices']].drop_duplicates()
        df_intersected = secondary_dfs[sec_inst]['feature'].loc[secondary_dfs[sec_inst]['intersected_indices']].drop_duplicates()
        df_included.to_csv(DIRS_DATA_RES + '\df_included_feature_' + sec_inst + '.csv', index=False)
        df_intersected.to_csv(DIRS_DATA_RES +'\df_intersected_feature_' + sec_inst + '.csv', index=False)

        # merge all
        df_included_all.append(df_included)
        df_intersected_all.append(df_intersected)

        print ("---> done with", sec_inst)
    
    # write out all/
    df_included_all = pd.concat(df_included_all)
    df_intersected_all = pd.concat(df_intersected_all)

    df_included_all.to_csv(DIRS_DATA_RES + '\df_included_feature_all.csv', index=False)
    df_intersected_all.to_csv(DIRS_DATA_RES +'\df_intersected_feature_all.csv', index=False)