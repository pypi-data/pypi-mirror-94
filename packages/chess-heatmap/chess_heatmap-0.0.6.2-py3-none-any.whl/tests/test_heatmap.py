"""
This module is used to test the control heatmap manually by sending mocked data.
"""
import os
import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns
import matplotlib
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class ChessHeatmap:
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

        sns.heatmap(gameDataMapWhite[0], cmap="YlGn", vmin = 0, vmax = gameMaxControlWhite, xticklabels=xlabels,yticklabels=ylabels, ax = ax1)
        sns.heatmap(gameDataMapBlack[0], cmap="YlGn", vmin = 0, vmax = gameMaxControlBlack, xticklabels=xlabels,yticklabels=ylabels, ax = ax2)

        def animate(i):
            "Create a single animated gif containing the heatmaps for all the different plys in a single game"
            ax1.cla()
            ax2.cla()
            sns.heatmap(gameDataMapWhite[i], cmap="YlGn", vmin = 0, vmax = gameMaxControlWhite, xticklabels=xlabels,yticklabels=ylabels, ax = ax1, cbar = None)
            sns.heatmap(gameDataMapBlack[i], cmap="YlGn", vmin = 0, vmax = gameMaxControlBlack, xticklabels=xlabels,yticklabels=ylabels, ax = ax2, cbar = None)

        anim = animation.FuncAnimation(fig, animate, interval=1000, save_count = len(gameDataMapWhite))
        anim.save("resources/output/" + filename + ".gif", dpi=80, writer='imagemagick')
    
    @staticmethod
    def generate_data():
        game_data = []
        for j in range(64):
            ply = []
            row = []
            for i in range(64):
                value_to_print = 0
                if j == i:
                    value_to_print = 1
                row.append(value_to_print)
                if (i + 1) % 8 == 0:
                    ply.append(row)
                    row = []
            game_data.append(ply)
            ply = []
        return game_data

if __name__ == '__main__':
    chess_heatmap = ChessHeatmap()
    ply0 = [0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]
    ply1 = [1,1,1,1,1,1],[1,1,1,1,1,1],[1,1,1,1,1,1],[1,1,1,1,1,1],[1,1,1,1,1,1],[1,1,1,1,1,1],[1,1,1,1,1,1],[1,1,1,1,1,1]
    ply2 = [2,2,2,2,2,2],[2,2,2,2,2,2],[2,2,2,2,2,2],[2,2,2,2,2,2],[2,2,2,2,2,2],[2,2,2,2,2,2],[2,2,2,2,2,2],[2,2,2,2,2,2]
    ply3 = [3,3,3,3,3,3],[3,3,3,3,3,3],[3,3,3,3,3,3],[3,3,3,3,3,3],[3,3,3,3,3,3],[3,3,3,3,3,3],[3,3,3,3,3,3],[3,3,3,3,3,3]
    ply4 = [4,4,4,4,4,4],[4,4,4,4,4,4],[4,4,4,4,4,4],[4,4,4,4,4,4],[4,4,4,4,4,4],[4,4,4,4,4,4],[4,4,4,4,4,4],[4,4,4,4,4,4]
    ply5 = [5,5,5,5,5,5],[5,5,5,5,5,5],[5,5,5,5,5,5],[5,5,5,5,5,5],[5,5,5,5,5,5],[5,5,5,5,5,5],[5,5,5,5,5,5],[5,5,5,5,5,5]
    
    plyData = ChessHeatmap.generate_data()
   
    #gameData = {"white":[plyData[0]], "black":[plyData[1]],"max_white_value":5,"max_black_value":5,"filename":"Game1"}

    gameData = {}
    plywhite = []
    plyblack = []
    for i in range(64):
        plywhite.append(plyData[i])
        plyblack.append(plyData[i])
    
    gameData["white"] = plywhite
    gameData["black"] = plyblack
    gameData["max_white_value"] = 5
    gameData["max_black_value"] = 5
    gameData["filename"] = "Game1"

    chess_heatmap.create_gif(gameData)