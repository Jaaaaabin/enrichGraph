#
# __main__.py
#

from topoCollection import topoCollect
from graphCreation import graphCreate
from pairRooms import getRoomPairs
from featureCollection import featureCollect, cleanCSVPairs, compareCSVFiles, mergeEdgesinCSV, FilterIds
from spatialQuery import buildVerticalEdges
from const_project import DIRS_DATA_RES

if __name__ == "__main__":
    
    # # ----- topo-extraction.
    # topoCollect()
    # graphCreate(plot_graph_accessibility=False)
    
    # # run only for ----- community-detection-buildup.
    # getRoomPairs()
    
    # # # run only for ----- gnn-feature-buildup.
    featureCollect()
    buildVerticalEdges()

    # merge edge data.
    mergeEdgesinCSV()
    FilterIds()

    compareCSVFiles(
        path_1=r'C:\dev\phd\enrichgraph\ec3_2024\enrichGraph\res\df_all_edges.csv',
        path_2=r'C:\dev\phd\enrichgraph\ec3_2024\enrichGraph\inter\Data-Maen.csv',
        diff_path=r'C:\dev\phd\enrichgraph\ec3_2024\enrichGraph\inter\diff.csv',
        overlap_path=r'C:\dev\phd\enrichgraph\ec3_2024\enrichGraph\inter\overlap.csv',
    )