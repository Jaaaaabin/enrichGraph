#
# __main__.py
#

from topoCollection import topoCollect
from graphCreation import graphCreate
from pairRooms import getRoomPairs
from featureCollection import featureCollect
from spatialQuery import securityroomQuery
if __name__ == "__main__":
    
    # ----- topo-extraction.
    # topoCollect()
    # graphCreate()
    
    # run only ----- community-detection-buildup.
    getRoomPairs()

    # ----- gnn-feature-buildup.
    # featureCollect()
    # securityroomQuery()
