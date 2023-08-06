"""
This module contains unit tests for all the methods part of the Chess dask cluster class.
"""
import sys
import os
import unittest
from unittest.mock import Mock
from unittest.mock import patch, call
from dask.distributed import LocalCluster
from mock_client import MockClient
from mock_future import MockFuture
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from chess_util import ChessUtil
from chess_dask_cluster import ChessDaskCluster

class TestDaskChessCluster(unittest.TestCase):
    "This class tests the methods that implement parallelism using dask tasks"

    def test_get_game_data(self):
        "This method verifies whether the data required to plot the map is generated correctly"

        mocked_ply_info = []
        ply_no = 0
        count = 0
        for square in range(128):
            mock_data = {}
            mock_data["square"] = count
            mock_data["white"] = 1
            mock_data["black"] = 2
            mock_data["ply"] = ply_no
            count = count + 1
            if square == 63:
                ply_no = 1
                count = 0
            mocked_ply_info.append(mock_data)

        mock_result_list = ChessDaskCluster.get_game_data(mocked_ply_info)

        self.assertEqual(mock_result_list["max_white_value"], 1)
        self.assertEqual(mock_result_list["max_black_value"], 2)

        for ply in mock_result_list["white"]:
            for row in ply:
                for square_control in row:
                    self.assertEqual(square_control, 1)

        for ply in mock_result_list["black"]:
            for row in ply:
                for square_control in row:
                    self.assertEqual(square_control, 2)

    @patch('chess_dask_cluster.ChessDaskCluster.__init__')
    @patch('chess_dask_cluster.wait')
    def test_analyse_games_in_cluster(self, mocked_wait, mocked_constructor):
        mocked_constructor.return_value = None
        mocked_wait.return_value = None
        mocked_game1 = {'game_name': "game1", "ply_count": 1}
        mocked_game2 = {'game_name': "game2", "ply_count": 2}
        game_list = [mocked_game1, mocked_game2]

        dask_cluster = ChessDaskCluster()
        mock_client = MockClient()
        dask_cluster.client = mock_client
        mock_client.result_list_to_be_sent_in_future = [1, 2]
        dask_cluster.analyse_games_in_cluster(game_list)

        passed_args = mock_client.passed_args
        self.assertEqual(len(passed_args), 2)
        for passed_arg in range(2):
            self.assertEqual(passed_args[passed_arg][0], dask_cluster.run_in_parallel)
            self.assertEqual(passed_args[passed_arg][1], game_list[passed_arg])
            self.assertEqual(passed_args[passed_arg][2], passed_arg)

    @patch('chess_dask_cluster.wait')
    @patch('chess_dask_cluster.worker_client')
    @patch('chess_dask_cluster.ChessDaskCluster.get_game_data')
    @patch('chess_util.ChessUtil.find_control_for_square')
    @patch('chess_util.ChessUtil.generate_ply_info_list_for_game')
    @patch('chess_image_generator.ChessImageGenerator.create_gif')
    def test_run_in_parallel(self, create_gif_mock, mocked_generated_info,
                             mocked_control, mocked_game_data, mocked_worker_client, mocked_wait):
        mocked_wait.return_value = None
        create_gif_mock.return_value = None
        mock_game_data = []
        mocked_game_no = 0
        mocked_game = {'game_name': "game1", "ply_count": 1}
        mocked_game_list = {'ply_info_list': ["game_task1", "game_task2"]}
        mocked_generated_info.return_value = mocked_game_list

        mock_client = MockClient()
        mocked_worker_client.return_value.__enter__.return_value = mock_client

        mock_client.result_list_to_be_sent_in_future = [1, 2]
        mocked_game_data.return_value = {"name": 'Chess_game'}
        ChessDaskCluster.run_in_parallel(mocked_game, mocked_game_no)
        passed_args = mock_client.passed_args
        self.assertEqual(len(passed_args), 2)
        for passed_arg in range(2):
            self.assertEqual(passed_args[passed_arg][0],
                             ChessUtil.find_control_for_square)
            self.assertEqual(passed_args[passed_arg][1],
                             mocked_game_list["ply_info_list"][passed_arg])
        mocked_game_data.assert_called_with([1, 2])
        create_gif_mock.assert_called_with(
            {"name": 'Chess_game', "filename": "Game0"})


if __name__ == "__main__":
    unittest.main()
