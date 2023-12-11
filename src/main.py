#
# __main__.py
#

from topoCollection import topoCollect
from graphCreation import graphCreate
from pairRooms import getRoomPairs
from featureCollection import featureCollect
from spatialQuery import buildVerticalEdges

if __name__ == "__main__":
    
    # # ----- topo-extraction.
    # topoCollect()
    # graphCreate()
    
    # # run only for ----- community-detection-buildup.
    # getRoomPairs()
    
    # # run only for ----- gnn-feature-buildup.
    # featureCollect()
    buildVerticalEdges()