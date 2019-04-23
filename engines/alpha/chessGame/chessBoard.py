import numpy as np
#import pygame
class Board():      # the board environment
    directionV=[(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1)]  #direction vector

    def __init__(self,size=8,withRender=False,copy=None):       #initial the board
        
        if copy is None :
            self.n=size
            self.state=[None]*self.n
            for i in range(self.n):
                self.state[i]=[0]*self.n
            self.state[int(self.n/2)-1][int(self.n/2)] = 1
            self.state[int(self.n/2)][int(self.n/2)-1] = 1
            self.state[int(self.n/2)-1][int(self.n/2)-1] = -1
            self.state[int(self.n/2)][int(self.n/2)] = -1
            if withRender==True :
                #self.render=None
                #exit()
                #pass
                self.render=render(self)
            else :
                self.render=None
        else :
            self.n=copy.n
            self.state=[None]*self.n
            for i in range(self.n):
                self.state[i]=[0]*self.n
            for i in range(self.n):
                for j in range(self.n):
                    self.state[i][j]=copy.state[i][j] 


    def getPointState(self,x,y):        #state of the target point
        if x<0 or x>=self.n or y<0 or y>=self.n :
            return None
        else :
            return self.state[x][y]
    
    def countDiff(self,target):
        cnt = 0
        for x in range(self.n) :
            for y in range(self.n) :
                if self.state[x][y]==target:
                    cnt+=1
                elif self.state[x][y]==-target:
                    cnt-=1
        return cnt
    
    def getActionSize(self):
        return self.n*self.n+1

    def getActionSet(self,turn):
        action = list()
        for x in range(self.n):
            for y in range(self.n):
                if self.checkLegitimacy(x,y,turn) == True :
                    action.append((x,y))
        return action
    
    def getActionVector(self,turn):
        action = self.getActionSet(turn)
        vec = np.zeros([self.n*self.n+1])
        for x,y in action :
            vec[x*self.n+y]=1
        return vec


    def hasValidAction(self,turn):
        temp = self.getActionSet(turn)
        if len(temp)==0 :
            return False
        else :
            return True

    def checkLegitimacy(self,x,y,turn) :
        if  self.state[x][y]!=0 :
            return False
        for i in range(0,8):
            tx,ty = x+self.directionV[i][0] , y+self.directionV[i][1]
            cnt=0
            while(tx>=0 and tx<self.n and ty>=0 and ty<self.n) :
                if self.state[tx][ty]==0 :
                    break
                elif self.state[tx][ty]==turn :
                    if cnt!=0 :
                        return True
                    break
                tx,ty = tx+self.directionV[i][0] , ty+self.directionV[i][1]
                cnt=cnt+1
        return False
    
    def reverse(self,x,y,turn,getNext=False) :
        if self.state[x][y]!=0 :
            print("ERROR!")
            exit()
        
        nextBoard=None
        state=None

        if getNext==False :
            state=self.state
        else :
            nextBoard=Board(copy=self)
            state=nextBoard.state

        state[x][y]=turn
        Dir=[]
        for i in range(0,8):
            tx,ty = x+self.directionV[i][0] , y+self.directionV[i][1]
            cnt=0
            while(tx>=0 and tx<self.n and ty>=0 and ty<self.n) :
                if state[tx][ty]==0 :
                    break
                elif state[tx][ty]==turn :
                    if cnt!=0 :
                        Dir.append((i,cnt))
                    break
                tx,ty = tx+self.directionV[i][0] , ty+self.directionV[i][1]
                cnt=cnt+1

        for i,cnt in Dir :
            tx,ty = x+self.directionV[i][0] , y+self.directionV[i][1]
            for j in range(cnt):
                state[tx][ty]=turn
                tx,ty = tx+self.directionV[i][0] , ty+self.directionV[i][1]
        
        if getNext==True:
            return nextBoard

    def reset(self):
        for i in range(self.n):
            self.state[i]=[0]*self.n
        self.state[int(self.n/2)-1][int(self.n/2)] = 1
        self.state[int(self.n/2)][int(self.n/2)-1] = 1
        self.state[int(self.n/2)-1][int(self.n/2)-1] = -1
        self.state[int(self.n/2)][int(self.n/2)] = -1
    
    def draw(self):
        if self.render == None :
            print("No render Exist !")
            exit()
        self.render.draw()

    def toString(self):
        result=""
        for i in range(self.n):
            for j in range(self.n):
                result=result+str(self.state[i][j]+1)
        return result
    
    def isEndState(self,turn):
        if self.hasValidAction(1):
            return 0
        elif self.hasValidAction(-1):
            return 0
        else :
            result = self.countDiff(turn)
            if result>0 :
                return 1
        return -1
    
    def roleChange(self):
        for i in range(self.n):
            for j in range(self.n):
                self.state[i][j]*=-1
    
"""
class render:

    screen = pygame.display.set_mode((800,800),0,32)
    backGroundImageFileName = 'board.png'
    blackChessImageFileName = 'black-circle.png'
    whiteChessImageFileName='white.png'
    background = pygame.image.load(backGroundImageFileName).convert_alpha()
    blackChess = pygame.image.load(blackChessImageFileName).convert_alpha()
    whiteChess = pygame.image.load(whiteChessImageFileName).convert_alpha()

    loc = np.zeros(shape=(8),dtype=int)

    def __init__(self,board):
        self.board=board
        pygame.init()
        pygame.display.set_caption("Inversi Game")
        for i in range(0,8) : 
            self.loc[i]=(i+1)*80+5
    
    def draw(self) :
        #draw the background
        self.screen.blit(self.background, (0,0))
        #draw the chess
        for i in range(0,8):
            for j in range(0,8):
                if self.board.state[i][j]==1 :
                    self.screen.blit(self.blackChess, (self.loc[i],self.loc[j]))
                elif self.board.state[i][j]==-1 :
                    self.screen.blit(self.whiteChess, (self.loc[i],self.loc[j]))
        pygame.display.update()
"""
