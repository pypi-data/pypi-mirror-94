"""
This module contains unit tests the method part of the Chess image generator class.
"""
import sys
import os
import unittest
from unittest.mock import patch, call
from mock_animate import MockAnimate
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from chess_image_generator import ChessImageGenerator


class TestChessImageGenerator(unittest.TestCase):
    "This class tests the method that creates the gif"

    @patch('chess_image_generator.animation.FuncAnimation')
    @patch('chess_image_generator.sns.heatmap')
    @patch('chess_image_generator.plt.subplots')
    @patch('matplotlib.use')
    def test_create_gif(self, mocked_graph, mocked_plot, mocked_sns_heatmap, mocked_func_animate):
        mocked_graph.return_value = None
        mocked_sns_heatmap.return_value = None
        animate_obj = MockAnimate()
        mocked_func_animate.return_value = animate_obj
        ax1 = 1
        ax2 = 2
        fig = 3
        mocked_plot.return_value = [fig, (ax1, ax2)]
        ply1 = [[1, 2, 3, 4, 5, 6, 7, 8], [1, 2, 3, 4, 5, 6, 7, 8],
                [1, 2, 3, 4, 5, 6, 7, 8], [1, 2, 3, 4, 5, 6, 7, 8],
                [1, 2, 3, 4, 5, 6, 7, 8], [1, 2, 3, 4, 5, 6, 7, 8],
                [1, 2, 3, 4, 5, 6, 7, 8], [1, 2, 3, 4, 5, 6, 7, 8]]

        xlabels = ["a", "b", "c", "d", "e", "f", "g", "h"]
        ylabels = ["8", "7", "6", "5", "4", "3", "2", "1"]

        mocked_game_data = {"white": [ply1, ply1, ply1], "black": [ply1, ply1, ply1],
                            "max_white_value": 3, "max_black_value": 4, "filename": "Game0"}
        ChessImageGenerator.create_gif(mocked_game_data)
        mocked_graph.assert_called_with('agg')
        mocked_plot.assert_called_with(1, 2)
        mocked_sns_heatmap.assert_has_calls([call(ply1, cmap="YlGn", vmax=3, xticklabels=xlabels,
                                                  yticklabels=ylabels, ax=1),
                                             call(ply1, cmap="YlGn", vmax=4, xticklabels=xlabels,
                                                  yticklabels=ylabels, ax=2)])


if __name__ == '__main__':
    unittest.main()
