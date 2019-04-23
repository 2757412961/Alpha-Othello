from engines.alpha.MCTS.MCTS import mctNode
import time
import numpy as np
class mctAgent:
    def __init__(self,myNode):
        self.myNode=myNode

    def respond(self,board,turn):
        st = time.time()

        if turn==-1:
            board.roleChange()

        cnt=0
        for i in range(8):
            for j in range(8):
                if board.state[i][j]!=0:
                    cnt+=1

        cnt-=4

        if cnt<10 :
            pi = self.myNode.getActionVector(board,temperature=1)
            #print("haha")
        else :
            pi = self.myNode.getActionVector(board,temperature=0)


        if turn==-1:
            board.roleChange()


        if cnt<10 :
            action = np.random.choice(len(pi), p=pi)
        else:
            action = np.argmax(pi)      



        #print("~~~~~~~~~~~~~~~~~~~~~~")
        #tp,tv = self.myNode.network.predict(board.state)
        #print(tp)
        #print("network win rate : ")
        #print(tv)
        #print("action : ",action)
        #print("pi : ",pi)
        #print("~~~~~~~~~~~~~~~~~~~~~")
        #print(pi)

        print("step cost : ",time.time()-st," seconds")
        return int(action//board.n),int(action%board.n)


