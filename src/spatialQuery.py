#
# spatialQuery.py
#

# import modules
from const_project import DIRS_DATA_RES, NAME_FEATURE_COLLECTION, NAME_FEATURES_INSTANCES, NAME_FEATURES_INSTANCES_ARE

from funct_topo import *

import itertools

def is_included(box1, box2, tol_inclusion=0.0):
    
    # if box1 is IN box2.
    inclusion_side_min = all(i>=j-tol_inclusion for (i,j) in zip(box1[:3], box2[:3])) # xmin ymin zmin
    inclusion_side_max = all(i<=j+tol_inclusion for (i,j) in zip(box1[3:], box2[3:])) # xmax ymax zmax

    return inclusion_side_min and inclusion_side_max

def is_intersected(box1, box2, tol_z=0.0, refined_box=False):
    
    # no tolerance.
    if box1.loc[2] < box1.loc[5]:
        box1.loc[2] -= tol_z 
        box1.loc[5] += tol_z
    else:
        box1.loc[2] += tol_z 
        box1.loc[5] -= tol_z

    if box2.loc[2] < box2.loc[5]:
        box2.loc[2] -= tol_z 
        box2.loc[5] += tol_z
    else:
        box2.loc[2] += tol_z 
        box2.loc[5] -= tol_z

    if refined_box:

        # in case extra-intersection among walls on the same floor needs to be excluded, refined boxes are considered.
        per_refine = 0.2
        
        #box1.
        d_x_1, d_y_1 = box1.loc[3] - box1.loc[0], box1.loc[4] - box1.loc[1] 
        
        box1.loc[0] += d_x_1 * per_refine
        box1.loc[3] -= d_x_1 * per_refine
        box1.loc[1] += d_y_1 * per_refine
        box1.loc[4] -= d_y_1 * per_refine

        #box2.
        d_x_2, d_y_2 = box2.loc[3] - box2.loc[0], box2.loc[4] - box2.loc[1] 
        
        box2.loc[0] += d_x_2 * per_refine
        box2.loc[3] -= d_x_2 * per_refine
        box2.loc[1] += d_y_2 * per_refine
        box2.loc[4] -= d_y_2 * per_refine

    # if box1 is IN box2.
    if is_included(box1,box2):

        return False
    
    # if box1 is not IN box2.
    elif (box1[3] >=box2[0] and box2[3] >=box1[0]) and \
        (box1[4] >=box2[1] and box2[4] >=box1[1]) and \
            (box1[5] >=box2[2] and box2[5] >=box1[2]):
        
        return True 
    
    # if box2 is not in box1.
    elif (box2[3] >=box1[0] and box1[3] >=box2[0]) and \
        (box2[4] >=box1[1] and box1[4] >=box2[1]) and \
            (box2[5] >=box1[2] and box1[5] >=box2[2]):
        
        return True 
    
def securityroomQueryBasic(sr_feature_inst, secondary_feature_insts):
    
    # read and extend the SR space.
    df_sr_space =  pd.read_csv(
        DIRS_DATA_RES +'\df_feature_'+ sr_feature_inst +'.csv',
        header=0,)
    df_sr_space['zmin'] = df_sr_space['zmin'].apply(lambda x:x-1000)
    df_sr_space['zmax'] = df_sr_space['zmax'].apply(lambda x:x+1000)
    
    secondary_dfs = {}

    for inst in secondary_feature_insts:

        # read all the rest
        df =  pd.read_csv(
            DIRS_DATA_RES +'\df_feature_'+ inst +'.csv',header=0,)

        # add class columns
        for cl in secondary_feature_insts:
            if cl == inst:
                df[cl] = 1
            else:
                df[cl] = 0

        secondary_dfs.update(
            {inst: {'feature': df,},}
                )
    
    return df_sr_space, secondary_dfs


def findInclusionSpace(df_sr_space, secondary_df):
    
    # find the inclusion relationship between spaces. 

    df_intersected_all, df_included_all = [], []

    # Initialize lists to store the indices of included and intersecting rows
    all_included_spaces_indices, all_intersected_spaces_indices  = [], []
    
    # Initialize lists for vertical_box_edges.
    all_included_spaces, all_intersected_spaces = [], []

    
    # Check for pairs of bounding boxes (sr bounding box vs other spaces).
    for index_sr, row_sr in df_sr_space.iterrows():
        
        box_sr = pd.Series([row_sr['xmin'], row_sr['ymin'], row_sr['zmin'], row_sr['xmax'], row_sr['ymax'], row_sr['zmax']])
        
        # the secondary box.
        included_spaces, intersected_spaces = [], []
        included_indices, intersected_indices = [], []
        
        for index_sec, row_sec in secondary_df.iterrows():
            box_second = pd.Series([row_sec['xmin'], row_sec['ymin'], row_sec['zmin'], row_sec['xmax'], row_sec['ymax'], row_sec['zmax']])
            
            # if included.
            if is_included(box_second, box_sr):
                included_indices.append(index_sec)
                included_spaces.append(int(row_sec['id']))

        # for each big vertical box.
        all_included_spaces.append(included_spaces)
        all_included_spaces_indices.append(included_indices)
    
    flatten_all_included_spaces_indices = [item for sublist in all_included_spaces_indices for item in sublist]
    df_included_spaces = secondary_df.loc[flatten_all_included_spaces_indices].drop_duplicates()
    
    return df_included_spaces, all_included_spaces, all_included_spaces_indices
    

def findIntersectedElements(secondary_df, all_element_indices, tol_z=0.0):

    element_intersection_pairs = []
    
    # for space intersection.
    if isinstance(all_element_indices, list) and isinstance(all_element_indices[0], list):

        for ids in all_element_indices:
            
            # ----------------------------
            if len(ids) >= 2:
            
                combinations_ids = itertools.combinations(ids,2)
                for (a,b) in combinations_ids:

                    box_a = pd.Series(
                        [secondary_df.loc[a]['xmin'], secondary_df.loc[a]['ymin'], secondary_df.loc[a]['zmin'], secondary_df.loc[a]['xmax'], secondary_df.loc[a]['ymax'], secondary_df.loc[a]['zmax']])

                    box_b = pd.Series(
                        [secondary_df.loc[b]['xmin'], secondary_df.loc[b]['ymin'], secondary_df.loc[b]['zmin'], secondary_df.loc[b]['xmax'], secondary_df.loc[b]['ymax'], secondary_df.loc[b]['zmax']])
                    
                    intersected_element_ids = [int(secondary_df.loc[a]['id']),int(secondary_df.loc[b]['id'])]

                    if is_intersected(box_a, box_b, tol_z=tol_z) and intersected_element_ids not in element_intersection_pairs:
                        
                        print("intersection space +1")
                        element_intersection_pairs.append(intersected_element_ids)

            else:
                continue
            # ----------------------------

    # for wall intersection.
    elif isinstance(all_element_indices, list) and not isinstance(all_element_indices[0], list):

        ids = all_element_indices

        # ----------------------------
        if len(ids) >= 2:
        
            combinations_ids = itertools.combinations(ids,2)
            for (a,b) in combinations_ids:

                box_a = pd.Series(
                    [secondary_df.loc[a]['xmin'], secondary_df.loc[a]['ymin'], secondary_df.loc[a]['zmin'], secondary_df.loc[a]['xmax'], secondary_df.loc[a]['ymax'], secondary_df.loc[a]['zmax']])

                box_b = pd.Series(
                    [secondary_df.loc[b]['xmin'], secondary_df.loc[b]['ymin'], secondary_df.loc[b]['zmin'], secondary_df.loc[b]['xmax'], secondary_df.loc[b]['ymax'], secondary_df.loc[b]['zmax']])
                
                intersected_element_ids = [int(secondary_df.loc[a]['id']),int(secondary_df.loc[b]['id'])]

                if is_intersected(box_a, box_b, tol_z=tol_z, refined_box=True) and intersected_element_ids not in element_intersection_pairs:
                    
                    print("intersection wall +1")
                    element_intersection_pairs.append(intersected_element_ids)
            # ----------------------------

    return element_intersection_pairs

def filterElement(df_primary, df_second, columns_primary=[], columns_second='',):
    
    df_second_filtered = []
    v_primary =  df_primary[columns_primary].values.tolist() if columns_primary else df_primary.values.tolist()

    v_primary  = [item for sublist in v_primary for item in sublist] if isinstance(v_primary, list) and isinstance(v_primary[0], list) else v_primary
    v_primary = list(set(v_primary))

    if columns_second:

        df_second_filtered = df_second.loc[df_second[columns_second].isin(v_primary)]
        
    return df_second_filtered

def buildVerticalEdges():
    
    # --------------------------------------------- SR -> Space
    # identify the Serucity Spaces and gather all the feature documents 
    # find spaces included by the vertical boxes by each Security Spaces

    df_sr_space, secondary_dfs = securityroomQueryBasic(NAME_FEATURES_INSTANCES[0], NAME_FEATURES_INSTANCES[1:])
    secondary_df = secondary_dfs['space']['feature']
    df_included_spaces, all_included_spaces, all_included_spaces_indices = findInclusionSpace(df_sr_space, secondary_df)
    
    # --------------------------------------------- Space Level.
    # output the features of all the related/covered/included spaces  
    df_included_spaces.to_csv(DIRS_DATA_RES + '\df_feature_all_spaces_included_bysr.csv', index=False)

    space_intersection_pairs = findIntersectedElements(
        secondary_df, all_included_spaces_indices, tol_z=0.15)
    df_pairs_space_intersection = pd.DataFrame(space_intersection_pairs, columns=['host', 'target']).drop_duplicates()
    df_pairs_space_intersection.to_csv(DIRS_DATA_RES + '\df_pairs_space_intersection.csv', index=False)

    # --------------------------------------------- Space -> Wall.
    # filter those connected to covered spaces.
    df_pairs_space_to_wall = pd.read_csv(DIRS_DATA_RES + '\df_pairs_space_to_wall_tempo.csv')
    
    df_pairs_space_intersection_to_wall = filterElement(df_pairs_space_intersection, df_pairs_space_to_wall, columns_second='host') # here's the issue.
    df_pairs_space_intersection_to_wall.to_csv(DIRS_DATA_RES + '\df_pairs_space_intersection_to_wall.csv', index=False)
    
    # # --------------------------------------------- Wall Level.
    all_intersection_related_walls = df_pairs_space_intersection_to_wall['target'].values.tolist()
    secondary_df = secondary_dfs['wall']['feature']
    related_secondary_df = secondary_df.loc[secondary_df['id'].isin(all_intersection_related_walls)]
    all_intersection_related_walls_indices = related_secondary_df.index.values.tolist()
    
    wall_intersection_paris = findIntersectedElements(
        secondary_df, all_intersection_related_walls_indices, tol_z=0.15)
    df_pairs_wall_intersection = pd.DataFrame(wall_intersection_paris, columns=['host', 'target']).drop_duplicates()
    df_pairs_wall_intersection.to_csv(DIRS_DATA_RES + '\df_pairs_wall_intersection.csv', index=False)

    # # --------------------------------------------- Wall -> Openings.
    df_pairs_wall_to_opening = pd.read_csv(DIRS_DATA_RES + '\df_pairs_wall_to_opening_tempo.csv')
    df_pairs_space_intersection_to_wall_to_opening = filterElement(df_pairs_space_intersection_to_wall, df_pairs_wall_to_opening, columns_primary='target', columns_second='host')
    df_pairs_space_intersection_to_wall_to_opening.to_csv(DIRS_DATA_RES + '\df_pairs_space_intersection_to_wall_to_opening.csv', index=False)

    # df_intersected.to_csv(DIRS_DATA_RES +'\df_intersected_feature_all.csv', index=False)

    # # merge all
    # df_included_all.append(df_included)
    # df_intersected_all.append(df_intersected)

    # # write out all/
    # df_included_all = pd.concat(df_included_all)
    # df_intersected_all = pd.concat(df_intersected_all)
