import numpy as np
from engines.alpha.chessGame.reversiGame import reversiGame
from engines.alpha.chessGame.chessBoard import Board
import time
import math
class mctNode:
    def __init__(self,network,args,game):
        self.game=game
        self.network=network
        self.args=args
        self.Q={}
        self.Nsa={}
        self.Ns={}
        self.P={}
        self.visitedState={}    #访问过的结束状态就不用再重复计算了，起到一个记忆化搜索的作用
        self.validAction={}

    def clear(self):
        self.Q={}
        self.Nsa={}
        self.Ns={}
        self.P={}
        self.visitedState={}    
        self.validAction={}


    def getActionVector(self,currentBoard,temperature=1.0):
        self.clear()
        stepTime = 0
        #print("ha")
        #print(currentBoard.state)
        for i in range(self.args.simCntOfMCT) :
            st=time.time()

            self.treePolicy(currentBoard)
          
            stepTime+=time.time()-st
            if(stepTime>30.0):
                break
        #print(currentBoard.state)
        #input("...")
        current = currentBoard.toString()

        size = self.game.getActionSize()
 
        p=[]
        for i in range(size):
            if (current,i) in self.Nsa :
                p.append(self.Nsa[(current,i)])
            else :
                p.append(0)
 

        if temperature == 0:
            target = np.argmax(p)
            for i in range(size):
                if i!=target:
                    p[i]=0
                else :
                    p[i]=1
            return p
        else :
            temperature=1.0/temperature
            for i in range(size):
                p[i]=p[i]**temperature
            tot=sum(p)
            for i in range(size):
                p[i]/=tot
            return p

    def simulate(self,s,currentBoard):
        self.P[s] , result = self.network.predict(currentBoard.state)
        actionVector= currentBoard.getActionVector(1)
  
        self.P[s]*=actionVector
        
        tot = np.sum(self.P[s])

        if tot!=0 :
            self.P[s]/=tot
        else :
            self.P[s]+=actionVector
            tot = np.sum(self.P[s])
            self.P[s]/=tot
        

        self.validAction[s] = actionVector
        self.Ns[s]=0

        return result

    def bestChild(self,s,actionVector):
        size = self.game.getActionSize()
        maxU = None
        targetChild =None
       
        for a in range(size):
            if actionVector[a]==1 :
                if (s,a) in self.Q :
                    ubc = self.Q[(s,a)]+self.args.excOfUCT*self.P[s][a]*math.sqrt(self.Ns[s])/(1+self.Nsa[(s,a)])
                    #print(self.Q[(s,a)]," + ",self.args.excOfUCT*self.P[s][a]*math.sqrt(self.Ns[s])/(1+self.Nsa[(s,a)]))
                    #input("...")
                else :
                    targetChild = a
                    break
                
                if (targetChild is None) or maxU<ubc : 
                    maxU=ubc
                    targetChild =a 

        if targetChild is None:
            print("opps ? no child ? ")
            print(actionVector)
            exit()
        return targetChild


    def treePolicy(self,currentBoard):
        s=currentBoard.toString()
        #print("emmm?")
        if s not in self.visitedState :
            self.visitedState[s]=currentBoard.isEndState(1)

        if self.visitedState[s]!=0:
            return -self.visitedState[s]
        
        if s not in self.P:
            return -self.simulate(s,currentBoard)
        
        actionVector = self.validAction[s]
        child = self.bestChild(s,actionVector)

       # print(currentBoard.state)
   
        nextState = currentBoard.reverse(int(child//self.game.n),int(child%self.game.n),1,getNext=True) 
    
        mark=1
        if nextState.hasValidAction(-1) == True:
            nextState.roleChange()
        else :
            mark=-1

        v = self.treePolicy(nextState)*mark

        if (s,child) in self.Q:
            self.Q[(s,child)] = (self.Nsa[(s,child)]*self.Q[(s,child)] + v)/(self.Nsa[(s,child)]+1)
            self.Nsa[(s,child)] += 1
        else:
            self.Q[(s,child)] = v
            self.Nsa[(s,child)] = 1

        self.Ns[s] += 1
    
        return -v
