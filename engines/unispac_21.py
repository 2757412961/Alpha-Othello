from .alpha.chessGame.reversiGame import reversiGame
from .alpha.NetWork.networkFrame import NNetWrapper
from .alpha.MCTS.mctAgent import mctAgent
from .alpha.MCTS.MCTS import mctNode
from .alpha.myUtil.util import dotdict
from .alpha.tranningFrame.selfCompetition import trainner
from .alpha.chessGame.chessBoard import Board as gameBoard
from engines import Engine
from copy import deepcopy
import os



args = dotdict({
    'numIters': 1000,
    'numEps': 100,
    'tempThreshold': 15,
    'updateThreshold': 0.6,
    'maxlenOfQueue': 200000,
    'simCntOfMCT': 10000,
    'arenaCompare': 40,
    'excOfUCT': 2.0,
    'checkpoint': './temp/',
    'load_model': False,
    'load_folder_file': ('/dev/models/8x100x50','best.pth.tar'),
    'numItersForTrainExamplesHistory': 20,
})

class agent(Engine):
    
    myGame = reversiGame(8,False)
    myNet = NNetWrapper(myGame)
    myNet.load_checkpoint("./engines/alpha/model/", "best.pth.tar")
    myAgent = mctAgent(mctNode(myNet,args,myGame))

    def get_move(self, board, color, move_num=None,
                 time_remaining=None, time_opponent=None):
        tempBoard=gameBoard()
        board = board.pieces
        color = -color
        for x in range(8):
            for y in range(8):
                tempBoard.state[x][y]=-board[x][y]

        x,y=self.myAgent.respond(tempBoard,color)
        return (x,y)
        
engine = agent
