#
# __main__.py
#

from topoCollection import topoCollect
from graphCreation import graphCreate
from pairRooms import getRoomPairs
from featureCollection import featureCollect, cleanCSVPairs, compareCSVFiles
from spatialQuery import buildVerticalEdges

if __name__ == "__main__":
    
    # # ----- topo-extraction.
    # topoCollect()
    # graphCreate(plot_graph_accessibility=False)
    
    # # # run only for ----- community-detection-buildup.
    # getRoomPairs()
    
    # # # run only for ----- gnn-feature-buildup.
    # featureCollect()
    # buildVerticalEdges()

    compareCSVFiles(
        path_1=r'C:\dev\phd\enrichgraph\ec3_2024\enrichGraph\res\df_edges.csv',
        path_2=r'H:\2024ec3\new_Edges_clean.csv',
        diff_path=r'H:\2024ec3\diff.csv',
        overlap_path=r'H:\2024ec3\overlap.csv',
    )