import numpy as np
import copy
from random import randint, choice, random
from tkinter import *
from PIL import Image, ImageTk
import time

# Parámetros
n = 4
options = ['up', 'down', 'left', 'right']

def rm_zeros(the_list, val):
    return [value for value in the_list if value != val]

def new_game(n):
    return [[0]*n for _ in range(n)]

# Clase Board
class board:
    def __init__(self):
        self.state = np.array(new_game(n))
        self.score = 0
        self.over = False
        self.win = False

    def get_empty_cells(self):
        return [(i, j) for i in range(n) for j in range(n) if self.state[i][j] == 0]

    def get_same_cells(self):
        for i in range(n):
            for j in range(n-1):
                if self.state[i][j] == self.state[i][j+1]:
                    return True
        for i in range(n-1):
            for j in range(n):
                if self.state[i][j] == self.state[i+1][j]:
                    return True
        return False

    def game_state(self):
        self.over = False
        self.win = np.any(self.state == 2048)
        if not self.get_empty_cells() and not self.get_same_cells():
            self.over = True

    def move(self, direction):
        addscore = 0
        new_state = np.copy(self.state)

        def slide(row):
            non_zero = row[row != 0]
            new_row = []
            skip = False
            i = 0
            while i < len(non_zero):
                if i + 1 < len(non_zero) and non_zero[i] == non_zero[i + 1]:
                    new_val = non_zero[i] * 2
                    new_row.append(new_val)
                    nonlocal addscore
                    addscore += new_val
                    i += 2
                else:
                    new_row.append(non_zero[i])
                    i += 1
            return np.array(new_row + [0]*(n - len(new_row)))

        if direction == 'left':
            for i in range(n):
                new_state[i] = slide(new_state[i])
        elif direction == 'right':
            for i in range(n):
                new_state[i] = slide(new_state[i][::-1])[::-1]
        elif direction == 'up':
            new_state = new_state.T
            for i in range(n):
                new_state[i] = slide(new_state[i])
            new_state = new_state.T
        elif direction == 'down':
            new_state = new_state.T
            for i in range(n):
                new_state[i] = slide(new_state[i][::-1])[::-1]
            new_state = new_state.T

        if not np.array_equal(self.state, new_state):
            self.state = new_state
            self.score += addscore
            empty = self.get_empty_cells()
            if empty:
                i, j = choice(empty)
                self.state[i][j] = 2 if random() < 0.9 else 4

# Inicialización gráfica
b0 = board()
b0.game_state()

window = Tk()
window.title('2048 - AI')
window.geometry("654x608")

img = ImageTk.PhotoImage(Image.open("background.png"))
lbl_bg = Label(window, image=img)
lbl_bg.place(x=0, y=0)

lbl_score = Label(window, text=b0.score, fg='black', font=("Helvetica", 26))
lbl_score.place(x=225, y=88)

tile_labels = [[None for _ in range(n)] for _ in range(n)]

def show_board(score, state):
    lbl_score.config(text=score)
    for i in range(n):
        for j in range(n):
            if tile_labels[i][j]:
                tile_labels[i][j].destroy()
                tile_labels[i][j] = None
            value = state[i][j]
            if value > 0:
                tile_labels[i][j] = Label(window, text=value, fg='black', font=("Helvetica", 26))
                tile_labels[i][j].place(x=108 + 120 * j, y=185 + 100 * i)
    window.update_idletasks()
    time.sleep(0.1)

# MCTS básico
def mcts():
    if b0.over: return
    mcts_move = np.zeros(50)
    mcts_score = np.zeros(50)
    avg_mcts_score = np.zeros(4)
    for i in range(50):
        btest = copy.deepcopy(b0)
        for d in range(10):
            btest.game_state()
            if btest.over: break
            k = randint(0, 3)
            if d == 0:
                mcts_move[i] = k
            try:
                btest.move(options[k])
            except:
                continue
        mcts_score[i] = btest.score

    for i in range(4):
        avg_mcts_score[i] = np.mean(mcts_score[mcts_move == i])
    best_move = np.argmax(avg_mcts_score)
    b0.move(options[best_move])

# Loop del juego
def play_game():
    if not b0.over:
        mcts()
        b0.game_state()
        show_board(b0.score, b0.state)
        window.after(100, play_game)
    else:
        print("Game Over! Final Score:", b0.score)

# Comienza el juego
play_game()
window.mainloop()
