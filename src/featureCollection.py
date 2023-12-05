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

