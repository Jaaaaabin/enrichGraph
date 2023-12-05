#
# __main__.py
#

from topoCollection import topoCollect
from graphCreation import graphCreate
from featureCollection import featureCollect
from spatialQuery import securityroomQuery

from graphEnricher import graphEnrich
from pairRooms import getRoomPairs

if __name__ == "__main__":

    #=================================#
    #                ini               #
    #=================================#
    # topoCollect()
    # graphCreate()
    # featureCollect()
    securityroomQuery()
    # graphEnrich(plot_graph=True)
    # getRoomPairs()
