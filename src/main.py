#
# __main__.py
#

from topoCollection import topoCollect
from graphCreation import graphCreate
from featureCollection import featureCollect
from spatialQuery import securityroomQuery

if __name__ == "__main__":
    
    # ----- topo-extraction.
    # topoCollect()
    # graphCreate()
    
    # -----  gnn-feature-buildup.
    # featureCollect()
    securityroomQuery()
