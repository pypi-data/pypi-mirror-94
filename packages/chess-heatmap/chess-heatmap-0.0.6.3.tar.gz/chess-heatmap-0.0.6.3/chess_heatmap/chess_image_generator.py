"""
This module is used to represent the control logic data in 2-dimensional form. 
The data values are represented as colors in the graph.
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns
import matplotlib

class ChessImageGenerator:
    "Class to create the gif"

    @staticmethod
    def create_gif(gameData):
        "Prepare the rows and columns for the graph"
        matplotlib.use('agg')
        
        gameDataMapWhite = gameData["white"]
        gameDataMapBlack = gameData["black"]

        filename = gameData["filename"]

        gameMaxControlWhite = gameData["max_white_value"]
        gameMaxControlBlack = gameData["max_black_value"]

        xlabels = ["a", "b", "c", "d", "e", "f", "g", "h"]
        ylabels = ["8", "7", "6", "5", "4", "3", "2", "1"]

        fig, (ax1, ax2) = plt.subplots(1, 2)

        sns.heatmap(gameDataMapWhite[0], cmap="YlGn", vmax = gameMaxControlWhite, xticklabels=xlabels,yticklabels=ylabels, ax = ax1)
        sns.heatmap(gameDataMapBlack[0], cmap="YlGn", vmax = gameMaxControlBlack, xticklabels=xlabels,yticklabels=ylabels, ax = ax2)

        def animate(i):
            "Create a single animated gif containing the heatmaps for all the different plys in a single game"
            ax1.cla()
            ax2.cla()
            sns.heatmap(gameDataMapWhite[i], cmap="YlGn", vmax = gameMaxControlWhite, xticklabels=xlabels,yticklabels=ylabels, ax = ax1, cbar = None)
            sns.heatmap(gameDataMapBlack[i], cmap="YlGn", vmax = gameMaxControlBlack, xticklabels=xlabels,yticklabels=ylabels, ax = ax2, cbar = None)

        anim = animation.FuncAnimation(fig, animate, interval=1000, save_count = len(gameDataMapWhite))
        anim.save("resources/output/" + filename + ".gif", dpi=80, writer='imagemagick')
