#
# const_project.py
#

# # # # # # # # #

# EC3 paper

# DIRS_DATA_TOPO = r'C:\dev\phd\enrichgraph\ec3_2024\enrichGraph\data\Bld type3_detached_topology'
DIRS_DATA_TOPO = r'H:\2024ec3\ec3_new\topology'

# DIRS_DATA_GNN = r'C:\dev\phd\enrichgraph\ec3_2024\enrichGraph\data\Bld type3_detached_gnn'
DIRS_DATA_GNN = r'H:\2024ec3\ec3_new\gnn'

DIRS_DATA_RES =  r'C:\dev\phd\enrichgraph\ec3_2024\enrichGraph\res'

FILE_INI_GRAPH_ACCESS = DIRS_DATA_RES + r'\res_graph_access.txt'
FILE_INI_GRAPH = DIRS_DATA_RES + r'\res_graph.txt'

NAME_TOPO_INSTANCES = ['door','window','wall','slab','space','separationline']
NAME_INSTANCE_COLLECTION = r'\collected_instances_'

NAME_TOPO_OBJECT = r'\collected_topology_wall_'
NAME_TOPO_SPACE = r'\collected_topology_space_'

NAME_FEATURE_COLLECTION = r'\feature_'

NAME_FEATURES_INSTANCES = ['space_sr','space','wall','door','window']
NAME_FEATURES_INSTANCES_ARE = ['door','window']
NAME_FEATURES_INSTANCES_INPUTARE = ['space_sr', 'space','wall']

NAME_FEATURE_INSTANCES_UNIT_DY= ['xmax','ymax','zmax','xmin','ymin','zmin']
NAME_FEATURE_INSTANCES_UNIT_CM= ['xmax','ymax','zmax','xmin','ymin','zmin','length','height','width']

CT_METER2FEET = 3.28084


# 