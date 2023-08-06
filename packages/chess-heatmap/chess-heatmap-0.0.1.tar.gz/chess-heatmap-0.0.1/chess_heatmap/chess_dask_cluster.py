"""
This module is for parallelizing the calculation of power of each square (in a ply) using dask tasks and parallelizing 
multiple games in PGNs
"""

from dask.distributed import LocalCluster
from dask.distributed import Client
from dask.distributed import worker_client
from distributed import wait
import coiled
from chess_util import ChessUtil
from chess_image_generator import ChessImageGenerator

class ChessDaskCluster:
    client: Client

    @staticmethod
    def get_game_data(result_list):
        #Convert the passed list of control per square per ply for all plies in the game into an object that is used for gif creation
        
        gameDataMapWhite = []
        gameDataMapBlack = []
        gameMaxControlWhite = 0
        gameMaxControlBlack = 0
        plyMapWhite = [[0 for x in range(8)] for y in range(8)]
        plyMapBlack = [[0 for x in range(8)] for y in range(8)]
        columnIndex = 0
        row = []
        rowIndex = 0
        plyNo = 0
        for result in result_list:
            square_index = result["square"]
            row = square_index//8
            column = square_index%8
            if result["white"] > gameMaxControlWhite:
                gameMaxControlWhite = result["white"]
            if result["black"] > gameMaxControlBlack:
                gameMaxControlBlack = result["black"]
            plyMapWhite[7-row][column] = result["white"]
            plyMapBlack[7-row][column] = result["black"]
            rowIndex = rowIndex + 1
            if rowIndex == 8:
                rowIndex = 0
                columnIndex = columnIndex + 1
                if columnIndex == 8:
                    columnIndex = 0
                    gameDataMapWhite.append(plyMapWhite)
                    gameDataMapBlack.append(plyMapBlack)
                    plyNo = plyNo + 1
                    plyMapWhite = [[0 for x in range(8)] for y in range(8)]
                    plyMapBlack = [[0 for x in range(8)] for y in range(8)]
        return {"white": gameDataMapWhite, "black": gameDataMapBlack, "max_white_value": gameMaxControlWhite, "max_black_value": gameMaxControlBlack}

    @staticmethod
    def run_in_parallel(game, game_no):
        """
        For the given game, for every ply, generate tasks to be run in parallel in a dask cluster. One task is created per square
        to find the control of both the sides. A worker client is used here because this method itself is run inside a worker (called
        from analyse_games_in_cluster)
        """
        task_futures = []
        tasks_for_game = ChessUtil.generate_ply_info_list_for_game(game)
        with worker_client() as client:
            for game_task in tasks_for_game["ply_info_list"]:
                task_futures.append(
                    client.submit(ChessUtil.find_control_for_square, game_task))

        wait(task_futures)
        control_list_for_game = []
        for task_future in task_futures:
            control_list_for_game.append(task_future.result())
        game_data = ChessDaskCluster.get_game_data(control_list_for_game)
        game_data["filename"] = "Game" + str(game_no)
        ChessImageGenerator.create_gif(game_data)

    def __init__(self):
        # coiled.create_software_environment(name="chess-env", pip="requirements.txt")
        # # TODO: change to get the following from config, instead of hardcoding them
        # cluster = coiled.Cluster(name="chess-cluster", n_workers=25, worker_cpu=4, worker_memory="16 GiB",
        #     scheduler_memory="16 GiB", software="chess-env")
        # # TODO: have a boolean in config to either run in local or run in coiled
        cluster = LocalCluster(n_workers=8, threads_per_worker=1)
        self.client = Client(cluster)

    def analyse_games_in_cluster(self, game_list):
        #Find control heatmap for all the games passed in parallel in a dask cluster
        game_no = 0
        game_futures = []
        for game in game_list:
            game_futures.append(self.client.submit(ChessDaskCluster.run_in_parallel, *(game, game_no)))
            game_no = game_no + 1
        wait(game_futures)


     
