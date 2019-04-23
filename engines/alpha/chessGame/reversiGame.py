import numpy as np
#import pygame
#from pygame.locals import *
from .chessBoard import Board
#------ The Basic Frame Of the Game Environment : BEGIN ------#
class reversiGame :
    def __init__(self,n,display=False):
        self.n=n
        self.board=Board(self.n,withRender=display)
        self.turn=1
        self.display=display
        self.end=False
    
    def initBoard(self):
        self.board = Board(self.n,withRender=self.display)
        self.turn=1
        self.end=False
    
    def getBoardSize(self):
        return (self.n,self.n)
    
    def getActionSize(self):
        return self.n*self.n+1
    
    def placeChess(self,x,y):
        if self.board.checkLegitimacy(x,y,self.turn) == False :
            print("Invalid Action")
            return
        else :
            self.board.reverse(x,y,self.turn)
            
        if self.display==True :
            self.board.draw()

        self.turn *= -1
        if self.board.hasValidAction(self.turn)==False :
            self.turn *= -1
            if self.board.hasValidAction(self.turn)==False :
                self.gameOver()
    
    def gameOver(self):
        print("Black - White : ",self.board.countDiff(1))
        self.end=True

    def getResult(self):
        diff = self.board.countDiff(1)
        if diff>0:
            return 1
        elif diff<0:
            return -1
        else :
            return 0

    def getAllDirInstance(self,pi):
        pi_board = np.reshape(pi[:-1], (self.n, self.n))
        l = []
        for i in range(1, 5):
            for j in [True, False]:
                newBoard = np.rot90(self.board.state, i)
                newPi = np.rot90(pi_board, i)
                if j:
                    newBoard = np.fliplr(newBoard)
                    newPi = np.fliplr(newPi)
                l += [(newBoard, list(newPi.ravel()) + [pi[-1]])]
        return l

    def Start(self,player,agent):
        #self.initBoard()
        self.board = Board(self.n,True)
        while True :
            self.board.draw()
            if self.turn == player :
                for event in pygame.event.get():
                    if event.type == QUIT:
                        exit()
                    elif event.type == MOUSEBUTTONDOWN :
                        x=int()
                        y=int()
                        x, y = pygame.mouse.get_pos()
                        if x<80 or x>720 or y<80 or y>720 :
                            continue
                        x=(x-1)//80 - 1
                        y=(y-1)//80 - 1
                        self.placeChess(x,y)
            else :
                for event in pygame.event.get():
                    if event.type == QUIT:
                        exit()
                x,y = agent.respond(self.board,self.turn)
                self.placeChess(x,y)

            if  self.end==True :
                self.initBoard() 
                self.end=False
    def A2A(self,agent1,agent2):
        self.board = Board(self.n,True)
        players=[None,agent1,agent2]
        while True :
            self.board.draw()
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
            x,y = players[self.turn].respond(self.board,self.turn)
            self.placeChess(x,y)
            if self.end==True :
                input("again?")
                self.end=False;
                self.initBoard();

    #direction array
    # dx=[0, -1,-1,-1,0,1,1,1]
    #dy=[-1,-1 ,0 ,1,1 ,1,0,-1]    
        
#------ The Basic Frame Of the Game Environment : END ------#
