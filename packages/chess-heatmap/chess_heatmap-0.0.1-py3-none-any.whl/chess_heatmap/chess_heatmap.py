"""
This module produces a control heatmap for a chess game which shows which side controls which squares how many times per ply/move
in a Chess board
Use dask to do parallelism to analyze multiple games in a single PGN and finally for multiple PGNs
"""
from chess_util import ChessUtil
from chess_dask_cluster import ChessDaskCluster

class ControlHeatmap:
    "Class to calculate the control heatmap"

#----START OF SCRIPT
if __name__== '__main__':
 
    game_list = ChessUtil.get_games_from_pgn_files()
  
    dask_cluster = ChessDaskCluster()
    dask_cluster.analyse_games_in_cluster(game_list)
   
