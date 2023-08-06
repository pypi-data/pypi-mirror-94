"""
This module tests the method that calculates the number of attackers for each square.
Input is a CSV file
"""
import os
import sys
import csv
import chess
import pytest
from chess import parse_square
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from chess_util import ChessUtil

def get_data():
    "Fetches data from a CSV file"
    ret_list = []
    csv_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),'board.csv')
    with open(csv_file) as csvfile:
        boardreader = csv.reader(csvfile, delimiter=',')
        for row in boardreader:
            ret_list.append(row)
    return ret_list

@pytest.mark.parametrize("fen,square,color,expected", get_data())
def test_calculate_control_for_square_multiple_values(fen, square, color, expected):
    """
    Given a game and a color is specified, when a specific square is considered,
    then the number of attackers for that square should be the number of pieces
    of that color which can move to the specified square
    """
    board = chess.Board(fen)
    parsed_square = parse_square(square)
    ply_no = 0
    ply_info = {"ply_no": ply_no, "square": parsed_square, "board": board}

    square_power = ChessUtil.find_control_for_square_for_color(ply_info, color == 'W')
    assert str(square_power) == expected
