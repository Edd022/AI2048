import sys
import os
sys.path.append(os.getcwd)
from game_defs_2048 import board, rm_zeros, new_game
import numpy as np
import copy
from random import randint, random, choice
from tkinter import *
from PIL import Image, ImageTk
import os
import time
options=['up', 'down', 'left', 'right']
n=4


def mcts():
  while b0.over == False:
   show_board(b0.score, b0.state)
   #time.sleep(0.2)
   b0.game_state()
   if b0.over == False:
    mcts_move=np.zeros(100)
    mcts_score=np.zeros(100)
    avg_mcts_score=np.zeros(4)
    for i in range(500):
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
        #print b0.state



def show_board(score, state):
	window.update()
	lbl=Label(window, text=score, fg='black', font=("Helvetica", 26))
	lbl.place(x=225, y=88)
	#top row
	if state[0,0]>0:
	 pos0=Label(window, text=state[0, 0], fg='black', font=("Helvetica", 26))
	 pos0.place(x=108, y=185)
	if state[0,1]>0:
	 pos1=Label(window, text=state[0, 1], fg='black', font=("Helvetica", 26))
	 pos1.place(x=228, y=185)
	if state[0,2]>0:
	 pos2=Label(window, text=state[0, 2], fg='black', font=("Helvetica", 26))
	 pos2.place(x=348, y=185)
	if state[0,3]>0:
	 pos3=Label(window, text=state[0, 3], fg='black', font=("Helvetica", 26))
	 pos3.place(x=468, y=185)

	if state[1,0]>0:
	 pos4=Label(window, text=state[1, 0], fg='black', font=("Helvetica", 26))
	 pos4.place(x=108, y=280)
	if state[1,1]>0:
	 pos5=Label(window, text=state[1, 1], fg='black', font=("Helvetica", 26))
	 pos5.place(x=228, y=280)
	if state[1,2]>0:
	 pos6=Label(window, text=state[1, 2], fg='black', font=("Helvetica", 26))
	 pos6.place(x=348, y=280)
	if state[1,3]>0:
	 pos7=Label(window, text=state[1, 3], fg='black', font=("Helvetica", 26))
	 pos7.place(x=468, y=280)

	if state[2,0]>0:
	 pos8=Label(window, text=state[2, 0], fg='black', font=("Helvetica", 26))
	 pos8.place(x=108, y=380)
	if state[2,1]>0:
	 pos9=Label(window, text=state[2, 1], fg='black', font=("Helvetica", 26))
	 pos9.place(x=228, y=380)
	if state[2,2]>0:
	 pos10=Label(window, text=state[2, 2], fg='black', font=("Helvetica", 26))
	 pos10.place(x=348, y=380)
	if state[2,3]>0:
	 pos11=Label(window, text=state[2, 3], fg='black', font=("Helvetica", 26))
	 pos11.place(x=468, y=380)

	if state[3,0]>0:
	 pos12=Label(window, text=state[3, 0], fg='black', font=("Helvetica", 26))
	 pos12.place(x=108, y=480)
	if state[3,1]>0:
	 pos13=Label(window, text=state[3, 1], fg='black', font=("Helvetica", 26))
	 pos13.place(x=228, y=480)
	if state[3,2]>0:
	 pos14=Label(window, text=state[3, 2], fg='black', font=("Helvetica", 26))
	 pos14.place(x=348, y=480)
	if state[3,3]>0:
	 pos15=Label(window, text=state[3, 3], fg='black', font=("Helvetica", 26))
	 pos15.place(x=468, y=480)
	window.update()


	if state[0,0]>0:
	 pos0.destroy()
	if state[0,1]>0:
	 pos1.destroy()
	if state[0,2]>0:
	 pos2.destroy()
	if state[0,3]>0:
 	 pos3.destroy()
	if state[1,0]>0:
	 pos4.destroy()
	if state[1,1]>0:
	 pos5.destroy()
	if state[1,2]>0:
	 pos6.destroy()
	if state[1,3]>0:
	 pos7.destroy()
	if state[2,0]>0:
	 pos8.destroy()
	if state[2,1]>0:
	 pos9.destroy()
	if state[2,2]>0:
 	 pos10.destroy()
	if state[2,3]>0:
	 pos11.destroy()
	if state[3,0]>0:
	 pos12.destroy()
	if state[3,1]>0:
	 pos13.destroy()
	if state[3,2]>0:
	 pos14.destroy()
	if state[3,3]>0:
	 pos15.destroy()



b0=board()
b0.game_state()
window = Tk()
window.title('2048 - AI')
window.geometry("654x608")
img = ImageTk.PhotoImage(Image.open("background.png"))
lbl = Label(window, image = img)
lbl.place(x=0, y=0)
lbl=Label(window, text=b0.score, fg='black', font=("Helvetica", 26))
lbl.place(x=225, y=88)

while b0.over == False:
  try:
   mcts()
  except:
   failed_attempt=[]
print(b0.score)



