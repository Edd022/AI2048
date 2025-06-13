import sys
sys.path.append("/home/brain/Downloads/2048_python/")
from game_defs_2048 import board, rm_zeros, new_game
import numpy as np
import copy
from random import randint, random, choice
n=4
options=['up', 'down', 'left', 'right']


#option 1: random moves:
def random_play():
 b0=board()
 while b0.over == False:
  options=['up', 'down', 'left', 'right']
  try:
    b0.game_state()
    if b0.over == False:
      b0.move(options[randint(0, 3)])
      print (b0.state)
  except:
    print("sth went wrong")
 print (b0.score)

#figure out how to only select from the available moves - e.g. block the vert moves if there are no same cells in vert



#option 2: MCTS

def mcts(self, verbose):
  while b0.over == False:
   b0.game_state()
   if b0.over == False:
    mcts_move=np.zeros(100)
    mcts_score=np.zeros(100)
    avg_mcts_score=np.zeros(4)
    for i in range(100):
      btest=copy.deepcopy(b0)
      try:
        for d in range(10):
          btest.game_state()
          if btest.over == False:
           try:
            k=randint(0, 3)
            if d==0:
              mcts_move[i]=k
            btest.move(options[k])
           except:
            try:
             l=[0, 1, 2, 3]
             l.remove(k)
             k=choice(l)
             btest.move(options[k])
            except:
             fail_move=[]
          else:
            mcts_score[i]=btest.score
          mcts_score[i]=btest.score
        del btest
      except:
        fail_move=[]
    for i in range(len(options)):
      avg_mcts_score[i]=np.mean(mcts_score[mcts_move==i])
    for i in range(len(options)):
      if avg_mcts_score[i]==max(avg_mcts_score):
        b0.move(options[i])
        if verbose==1:
         print (b0.state)


for i in range(10):
 b0=board()
 b0.game_state()
 while b0.over == False:
  try:
   mcts(0)
  except:
   failed_attempt=[]
 print (b0.score)
