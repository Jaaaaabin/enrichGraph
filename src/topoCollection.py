#
# topoCollection.py
#

# import modules
from const_project import DIRS_DATA_TOPO, DIRS_DATA_GNN, NAME_INSTANCE_COLLECTION, NAME_TOPO_INSTANCES
from funct_topo import *


def topoCollect():

    for topo_inst in NAME_TOPO_INSTANCES:

        # set JSON files
        js_file_instance =  DIRS_DATA_TOPO + NAME_INSTANCE_COLLECTION + topo_inst + '.json'

        # load the dict from Revit
        with open(js_file_instance, encoding="utf-8-sig") as json_file: # encoding = 'utf-8-sig' for special characters.
            revit_instances = json.load(json_file)
        
        #---
        # remove the "#" in the json keys.
        test_ins = revit_instances[0]
        old_key, new_key = [], []
        for key in test_ins.keys():
            if "#" in key:
                old_key = key
                new_key = key.replace("#","")
                print("yes")
        if old_key != new_key:
            for ii in range(len(revit_instances)):
                revit_instances[ii][new_key] = revit_instances[ii].pop(old_key)
        #---
        
        # create class objects for each dict.
        cls_objs_instances = convert_revitdict_to_clsobjs(revit_instances, class_name=topo_inst)

        if topo_inst =='separationline':

            # instances: room separation line
            df_instances = build_instance_df(cls_objs_instances, topo_inst, final_index_name='id')
            df_instances.index = df_instances.index.map(str) if df_instances.index.is_integer() else df_instances.index
            df_instances.to_csv(DIRS_DATA_TOPO+'\df_'+ topo_inst +'.csv')
            
        else:
            # instances: non-parameter building elements/spaces.
            df_instances = build_instance_df(cls_objs_instances, topo_inst, final_index_name='id')
            df_instances.to_csv(DIRS_DATA_TOPO+'\df_'+ topo_inst +'.csv', encoding = 'utf-8-sig') # encoding = 'utf-8-sig' for special characters.