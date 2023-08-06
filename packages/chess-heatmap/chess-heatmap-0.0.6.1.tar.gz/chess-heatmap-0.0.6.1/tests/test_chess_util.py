"""
This module contains unit tests for all the methods part of the Chess util class.
"""
import unittest
import glob
import sys
import os
import chess
import pytest
from mock import patch, call
from chess import WHITE
from chess import BLACK
from chess import parse_square
from chess import pgn
from chess import Board
from mock_game import MockGame
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from chess_util import ChessUtil

class TestChessUtil(unittest.TestCase):
    "This class tests the chess specific methods"

    @patch('glob.glob') 
    def test_reading_games_from_pgn_files(self, mockglob):
        """
        Given two pgn files, when one has 3 games and the other has 1 game,
        then 4 games should be read and Event names should match
        """
        file1 = os.path.join(os.path.dirname(os.path.abspath(__file__)),'input/Adams.pgn')
        file2 = os.path.join(os.path.dirname(os.path.abspath(__file__)),'input/Anand.pgn')
        mockglob.return_value = [file1, file2]
        games = ChessUtil.get_games_from_pgn_files()
        self.assertEqual(len(games), 4)
        game_names = ["Game1", "Game2", "Game3", "Game4"]
        i = 0
        for game in games:
            self.assertEqual(game.headers["Event"], game_names[i])
            i = i + 1

    def test_generating_tasks_for_a_game(self):
        """
        Given a game, when two plies are present in that game,
        then 128 tasks have to be created with valid squares and ply applied board
        """
        #MockGame contains two plies
        mocked_game = MockGame()
        game_ply_info = ChessUtil.generate_ply_info_list_for_game(mocked_game)
        self.assertEqual(len(game_ply_info["ply_info_list"]),128)
        self.assertEqual(game_ply_info["ply_count"],2)
        ply_no = 0
        fen = 'rnbqkbnr/pppppppp/8/8/8/1P6/P1PPPPPP/RNBQKBNR'

        count = 0
        for game_task in game_ply_info["ply_info_list"]:
            if count == 64:
                ply_no = ply_no + 1
                fen = 'rnbqkbnr/1ppppppp/p7/8/8/1P6/P1PPPPPP/RNBQKBNR'
            self.assertEqual(game_task["ply_no"],ply_no)
            self.assertEqual(game_task["board"].board_fen(),fen)
            count = count + 1

    def test_calculate_control_for_square_scneario(self):
        """
        Given a game and a color is specified, when a specific square is considered,
        then the number of attackers for that square should be the number of pieces of
        that color which can move to the specified square
        """
        board = chess.Board('rnbqkbnr/pppppppp/8/8/8/1P6/P1PPPPPP/RNBQKBNR w KQkq - 0 1')
        square = "f3"
        parsed_square = parse_square(square)
        ply_no = 0
        ply_info = {"ply_no": ply_no, "square": parsed_square, "board": board}

        square_power = ChessUtil.find_control_for_square_for_color(ply_info,WHITE)
        self.assertEqual(square_power,4)

    @patch('chess_util.ChessUtil.find_control_for_square_for_color')
    def test_control_for_square(self,mocked_control_info):
        """
        Given a game, when a specific square is considered,
        then the control should be calculated correctly for both White and Black"
        """
        mocked_control_info.side_effect = [2,5]
        board = chess.Board('8/2q2n2/8/8/pp2b3/8/1RP5/2B1K3 w - - 0 1')
        color = WHITE
        square = "d2"
        parsed_square = parse_square(square)
        ply_no = 0
        ply_info = {"ply_no": ply_no, "square": parsed_square, "color": color, "board": board}

        square_total_info = ChessUtil.find_control_for_square(ply_info)

        self.assertEqual(square_total_info["square"],11)
        self.assertEqual(square_total_info["white"],2)
        self.assertEqual(square_total_info["black"],5)
        self.assertEqual(square_total_info["ply"],0)

        mocked_control_info.assert_has_calls([call(ply_info, WHITE), call(ply_info, BLACK)])

if __name__ == '__main__':
    unittest.main()
