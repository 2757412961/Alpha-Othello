import numpy as np
#from pytorch_classification.utils import Bar, AverageMeter
import time

class competition():
    """
    An Arena class where any 2 agents can be pit against each other.
    """
    def __init__(self, agent1, agent2, game):
        self.agent1 = agent1
        self.agent2 = agent2
        self.game = game

    def play(self):
        self.game.initBoard()
        players=[None,self.agent1,self.agent2]
        while True :
            player = players[self.game.turn]
            x,y = player.respond(self.game.board,self.game.turn)
            self.game.placeChess(x,y)
            if self.game.end == True:
                break
        return self.game.getResult()
        

    def palyWithRecord(self, cnt):

        num = int(cnt/2)
        agentOneWin = 0
        agentTwoWin = 0
        tie = 0
        for i in range(num):
            result = self.play()
            if result==1:
                agentOneWin+=1
            elif result==-1:
                agentTwoWin+=1
            else:
                tie+=1

        self.agent1, self.agent2 = self.agent2, self.agent1
        
        for i in range(num):
            result = self.play()
            if result==-1:
                agentOneWin+=1
            elif result==1:
                agentTwoWin+=1
            else:
                tie+=1
            
        return agentOneWin, agentTwoWin, tie