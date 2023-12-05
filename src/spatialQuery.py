#
# spatialQuery.py
#

# import modules
from const_project import DIRS_DATA_TOPO
from const_project import NAME_TOPO_OBJECT, NAME_TOPO_SPACE, FILE_INI_GRAPH

from funct_topo import *

from const_project import DIRS_DATA_GNN, NAME_FEATURE_COLLECTION, NAME_FEATURES_INSTANCES, NAME_FEATURES_INSTANCES_ARE

def boundingbox

def securityroomQuery():

    sr_feature_inst = 'space_sr'
    non_sr_feature_inst = 'space_non_sr'

    df_sr_space =  pd.read_csv(
        DIRS_DATA_GNN +'\df_feature_'+ sr_feature_inst +'.csv',
        header=0,)
    df_non_sr_space = pd.read_csv(
        DIRS_DATA_GNN +'\df_feature_'+ non_sr_feature_inst +'.csv',
        header=0)

    print('ps')