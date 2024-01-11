#
# spatialQuery.py
#

# import modules
from const_project import DIRS_DATA_RES, NAME_FEATURE_COLLECTION, NAME_FEATURES_INSTANCES, NAME_FEATURES_INSTANCES_ARE
from const_project import DIRS_DATA_TOPO,NAME_INSTANCE_COLLECTION

from funct_topo import *

import itertools

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

def is_included(box1, box2, tol_inclusion=0.0):
    
    # if box1 is IN box2.
    inclusion_side_min = all(i>=j-tol_inclusion for (i,j) in zip(box1[:3], box2[:3])) # xmin ymin zmin
    inclusion_side_max = all(i<=j+tol_inclusion for (i,j) in zip(box1[3:], box2[3:])) # xmax ymax zmax

    return inclusion_side_min and inclusion_side_max

def is_intersected(
    box1, box2, tol_z=0.0, refined_box=0, count_inclusion=False):
    
    # for box1 and box2: xmin, ymin, zmin, xmax, ymax, zmax.
    if not (box1.loc[0] <= box1.loc[3] and box1.loc[1] <= box1.loc[4] and box1.loc[2] <= box1.loc[5] and \
    box2.loc[0] <= box2.loc[3] and box2.loc[1] <= box2.loc[4] and box2.loc[2] <= box2.loc[5]):
        
        raise Exception("Sorry, check here.")
    
    # z tolerance
    box1.loc[2] -= tol_z 
    box1.loc[5] += tol_z
    
    box2.loc[2] -= tol_z 
    box2.loc[5] += tol_z
    
    if refined_box != 0 :

        # in case extra-intersection among walls on the same floor needs to be excluded, refined boxes are considered.
        per_refine = refined_box
        
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
    
    # if count the inclusion as intersection.
    if count_inclusion:

        if is_included(box1,box2) or is_included(box2,box1):
            return True
    
    # or not.
    else:

        if is_included(box1,box2) or is_included(box2,box1):
            return False
    
    if (box1[0] > box2[3] or box2[0] > box1[3]) or \
        (box1[1] > box2[4] or box2[1] > box1[4]) or \
        (box1[2] > box2[5] or box2[2] > box1[5]):
        
        return False

    else:
        
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
        included_spaces,included_indices = [], []
        
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
    
    return df_included_spaces
    
def findIntersectedSpaces(all_spaces, tol_z = 0.0, count_inclusion=False):

    ids =  all_spaces['id'].tolist()
    ids_index = range(0, len(ids))

    combinations_ids_index = list(itertools.combinations(ids_index,2))
    
    element_intersection_pairs = []

    for (a,b) in combinations_ids_index:

        box_a = pd.Series(
            [all_spaces.loc[a]['xmin'], all_spaces.loc[a]['ymin'], all_spaces.loc[a]['zmin'], all_spaces.loc[a]['xmax'], all_spaces.loc[a]['ymax'], all_spaces.loc[a]['zmax']])

        box_b = pd.Series(
            [all_spaces.loc[b]['xmin'], all_spaces.loc[b]['ymin'], all_spaces.loc[b]['zmin'], all_spaces.loc[b]['xmax'], all_spaces.loc[b]['ymax'], all_spaces.loc[b]['zmax']])
        
        intersected_element_ids = [int(all_spaces.loc[a]['id']), int(all_spaces.loc[b]['id'])]

        if is_intersected(
            box_a, box_b, tol_z=tol_z, refined_box=0, count_inclusion=count_inclusion) and intersected_element_ids not in element_intersection_pairs:
            
            print(" Intersection Space Number +1.")
            element_intersection_pairs.append(intersected_element_ids)
            
    return element_intersection_pairs

def findIntersectedWalls(
    all_walls,
    orientation_dict=[],
    tol_z=0.0,
    refined_box=0,
    count_inclusion=True):

    def check_wall_orientation(wall_ids, orientation_dict):
        
        id_0, id_1 = str(wall_ids[0]), str(wall_ids[1])

        if orientation_dict[id_0]['Orientation'] == orientation_dict[id_1]['Orientation']:
            return True
        else:
            return False
        
    ids =  all_walls['id'].tolist()
    ids_index = range(0, len(ids))

    combinations_ids_index = list(itertools.combinations(ids_index,2))
    
    element_intersection_pairs = []

    for (a,b) in combinations_ids_index:

        box_a = pd.Series(
            [all_walls.loc[a]['xmin'], all_walls.loc[a]['ymin'], all_walls.loc[a]['zmin'], all_walls.loc[a]['xmax'], all_walls.loc[a]['ymax'], all_walls.loc[a]['zmax']])

        box_b = pd.Series(
            [all_walls.loc[b]['xmin'], all_walls.loc[b]['ymin'], all_walls.loc[b]['zmin'], all_walls.loc[b]['xmax'], all_walls.loc[b]['ymax'], all_walls.loc[b]['zmax']])
        
        intersected_element_ids = [int(all_walls.loc[a]['id']), int(all_walls.loc[b]['id'])]

        if is_intersected(
            box_a, box_b, tol_z=tol_z, refined_box=refined_box, count_inclusion=count_inclusion) and intersected_element_ids not in element_intersection_pairs:
            
            if check_wall_orientation(intersected_element_ids, orientation_dict):

                print(" Intersection Wall (in the same direction) Number +1.")
                element_intersection_pairs.append(intersected_element_ids)
            
    return element_intersection_pairs

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

                    if is_intersected(box_a, box_b, tol_z=tol_z, count_inclusion=False) and intersected_element_ids not in element_intersection_pairs:
                        
                        print(" Intersection Space Number +1.")
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

                if is_intersected(box_a, box_b, tol_z=tol_z, refined_box=True, count_inclusion=True) and intersected_element_ids not in element_intersection_pairs:
                    
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
    # identify the Serucity Spaces and gather all the feature documents, and find spaces included by the vertical boxes by each Security Spaces

    df_sr_space, secondary_dfs = securityroomQueryBasic(NAME_FEATURES_INSTANCES[0], NAME_FEATURES_INSTANCES[1:])
    secondary_df = secondary_dfs['space']['feature']
    df_included_spaces = findInclusionSpace(df_sr_space, secondary_df)

    # --------------------------------------------- Space Level Connections.
    # df_included_spaces.to_csv(DIRS_DATA_RES + '\df_feature_all_spaces_included_bysr.csv', index=False)

    df_included_spaces = df_included_spaces[df_included_spaces[['xmin','ymin','zmin','xmax','ymax','zmax']].sum(axis=1) != 0]
    df_included_spaces.reset_index(drop=True, inplace=True)
    space_intersection_pairs = findIntersectedSpaces(
        df_included_spaces, tol_z=0.2)
    df_pairs_space_intersection = pd.DataFrame(space_intersection_pairs, columns=['host', 'target']).drop_duplicates()
    df_pairs_space_intersection.to_csv(DIRS_DATA_RES + '\df_pairs_space_intersection.csv', index=False)

    # --------------------------------------------- Space -> Wall.
    # filter those connected to covered spaces.
    df_pairs_space_to_wall = pd.read_csv(DIRS_DATA_RES + '\df_pairs_space_to_wall_tempo.csv')
    
    df_pairs_space_intersection_to_wall = filterElement(df_pairs_space_intersection, df_pairs_space_to_wall, columns_second='host')
    df_pairs_space_intersection_to_wall.to_csv(DIRS_DATA_RES + '\df_pairs_space_intersection_to_wall.csv', index=False)

    # # --------------------------------------------- Wall Level Connections.
    all_intersection_related_walls = df_pairs_space_intersection_to_wall['target'].values.tolist()
    secondary_df = secondary_dfs['wall']['feature']
    df_related_walls = secondary_df.loc[secondary_df['id'].isin(all_intersection_related_walls)]
    df_related_walls.reset_index(drop=True, inplace=True)
    
    # load the additional feature files from Revit 
    js_file_instance = DIRS_DATA_TOPO + NAME_INSTANCE_COLLECTION + 'wall' + '.json'        
    with open(js_file_instance, encoding="utf-8-sig") as json_file: # encoding = 'utf-8-sig' for special characters.
        revit_wall_instances = json.load(json_file)
    revit_wall_orientation_dict = list_of_dicts_to_dict(revit_wall_instances, 'Id')

    wall_intersection_pairs = findIntersectedWalls(
        df_related_walls,
        orientation_dict=revit_wall_orientation_dict,
        tol_z=0.2,
        refined_box=0.1)
    df_pairs_wall_intersection = pd.DataFrame(wall_intersection_pairs, columns=['host', 'target']).drop_duplicates()
    df_pairs_wall_intersection.to_csv(DIRS_DATA_RES + '\df_pairs_wall_intersection.csv', index=False)

    # # --------------------------------------------- Wall -> Openings.
    df_pairs_wall_to_opening = pd.read_csv(DIRS_DATA_RES + '\df_pairs_wall_to_opening_tempo.csv')
    df_pairs_space_intersection_to_wall_to_opening = filterElement(df_pairs_space_intersection_to_wall, df_pairs_wall_to_opening, columns_primary='target', columns_second='host')
    df_pairs_space_intersection_to_wall_to_opening.to_csv(DIRS_DATA_RES + '\df_pairs_space_intersection_to_wall_to_opening.csv', index=False)