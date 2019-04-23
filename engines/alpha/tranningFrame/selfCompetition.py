from collections import deque
from engines.alpha.tranningFrame.competition import competition
from engines.alpha.MCTS.MCTS import mctNode
from engines.alpha.MCTS.mctAgent import mctAgent
import numpy as np
import time, os, sys
from pickle import Pickler, Unpickler
from random import shuffle

class trainner():
    """
    This class executes the self-play + learning. It uses the functions defined
    in Game and NeuralNet. args are specified in main.py.
    """
    def __init__(self, game, network, args):
        self.game = game
        self.agentNet = network
        self.oldVersion = self.agentNet.__class__(self.game)
        #self.agentTwoNet = self.agentOneNet.__class__(self.game)  # the competitor network
        self.args = args
        self.mcts = mctNode(self.agentNet,self.args,self.game)
        self.trainExamplesHistory = []    # history of examples from args.numItersForTrainExamplesHistory latest iterations
        self.skipFirstSelfPlay = False # can be overriden in loadTrainExamples()

    def selfPlay(self):

        trainExamples = []
        #(state,turn,policyDistribution,result)

        self.game.initBoard()
        step = 0

        while True:
            step += 1
            temperature = int(step < self.args.tempThreshold)

            if self.game.turn==-1:
                self.game.board.roleChange()
            
            pi = self.mcts.getActionVector(self.game.board, temperature = temperature)
            
            if self.game.turn==-1:
                self.game.board.roleChange()

            sym = self.game.getAllDirInstance(pi)

            for b,p in sym:
                trainExamples.append([b, self.game.turn, p, None])
            action = np.random.choice(len(pi), p=pi)

            self.game.placeChess(int(action//self.game.n),int(action%self.game.n))
            
            if self.game.end == True:
                break
        #return [(x[0],x[2],r*((-1)**(x[1]!=self.curPlayer))) for x in trainExamples]
        result = self.game.getResult()

        return [(x[0],x[2],x[1]*result) for x in trainExamples]

        

    def learn(self):
        """
        Performs numIters iterations with numEps episodes of self-play in each
        iteration. After every iteration, it retrains neural network with
        examples in trainExamples (which has a maximium length of maxlenofQueue).
        It then pits the new neural network against the old one and accepts it
        only if it wins >= updateThreshold fraction of games.
        """

        for i in range(1, self.args.numIters+1):
        
            print('------ITER ' + str(i) + '------')
            sti =time.time()
            # examples of the iteration
            if not self.skipFirstSelfPlay or i>1:
                iterationTrainExamples = deque([], maxlen=self.args.maxlenOfQueue)
    
                #eps_time = AverageMeter()
                #bar = Bar('Self Play', max=self.args.numEps)
                #end = time.time()
    
                for eps in range(self.args.numEps):
                    st=time.time()
                    self.mcts = mctNode(self.agentNet, self.args, self.game)   # reset search tree
                    iterationTrainExamples += self.selfPlay()
                    print("sim cost : ",time.time()-st," seconds")
    
                    # bookkeeping + plot progress
                    #eps_time.update(time.time() - end)
                    #end = time.time()
                    #bar.suffix  = '({eps}/{maxeps}) Eps Time: {et:.3f}s | Total: {total:} | ETA: {eta:}'.format(eps=eps+1, maxeps=self.args.numEps, et=eps_time.avg,
                    #total=bar.elapsed_td, eta=bar.eta_td)
                    #bar.next()
                #bar.finish()

                # save the iteration examples to the history 
                self.trainExamplesHistory.append(iterationTrainExamples)
                
            if len(self.trainExamplesHistory) > self.args.numItersForTrainExamplesHistory:
                print("len(trainExamplesHistory) =", len(self.trainExamplesHistory), " => remove the oldest trainExamples")
                self.trainExamplesHistory.pop(0)
            # backup history to a file
            # NB! the examples were collected using the model from the previous iteration, so (i-1)  
            #self.saveTrainExamples(i-1)
            
            # shuffle examples before training
            trainExamples = []
            for e in self.trainExamplesHistory:
                trainExamples.extend(e)
            shuffle(trainExamples)

            # training new network, keeping a copy of the old one
            self.agentNet.save_checkpoint(folder=self.args.checkpoint, filename='temp.pth.tar')
            self.oldVersion.load_checkpoint(folder=self.args.checkpoint, filename='temp.pth.tar')
            
            #(self,network,args,game)
            oldAgent = mctAgent(mctNode(self.oldVersion, self.args, self.game))
            
            self.agentNet.train(trainExamples)
            newAgent = mctAgent(mctNode(self.agentNet, self.args, self.game))

            print('PITTING AGAINST PREVIOUS VERSION')
            comp = competition(newAgent,oldAgent,self.game)
            
            newWins, oldWins, draws = comp.palyWithRecord(self.args.arenaCompare)

            print('NEW/PREV WINS : %d / %d ; DRAWS : %d' % (newWins, oldWins, draws))
            if newWins+oldWins == 0 or float(newWins)/(oldWins+newWins) < self.args.updateThreshold:
                print('REJECTING NEW MODEL')
                self.agentNet.load_checkpoint(folder=self.args.checkpoint, filename='temp.pth.tar')
            else:
                print('ACCEPTING NEW MODEL')
                self.agentNet.save_checkpoint(folder=self.args.checkpoint, filename=self.getCheckpointFile(i))
                self.agentNet.save_checkpoint(folder=self.args.checkpoint, filename='best.pth.tar')        

            print("~~~~~~~~~~~Finish this Round : ")
            print("Time cost of this round : ",(time.time()-sti)/60.0," minutes")




    def getCheckpointFile(self, iteration):
        return 'checkpoint_' + str(iteration) + '.pth.tar'

    def saveTrainExamples(self, iteration):
        folder = self.args.checkpoint
        if not os.path.exists(folder):
            os.makedirs(folder)
        filename = os.path.join(folder, self.getCheckpointFile(iteration)+".examples")
        with open(filename, "wb+") as f:
            Pickler(f).dump(self.trainExamplesHistory)
        f.closed

    def loadTrainExamples(self):
        modelFile = os.path.join(self.args.load_folder_file[0], self.args.load_folder_file[1])
        examplesFile = modelFile+".examples"
        if not os.path.isfile(examplesFile):
            print(examplesFile)
            r = input("File with trainExamples not found. Continue? [y|n]")
            if r != "y":
                sys.exit()
        else:
            print("File with trainExamples found. Read it.")
            with open(examplesFile, "rb") as f:
                self.trainExamplesHistory = Unpickler(f).load()
            f.closed
            # examples based on the model were already collected (loaded)
            self.skipFirstSelfPlay = True
