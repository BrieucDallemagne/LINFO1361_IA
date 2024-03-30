# Replay all the games in a folder and save the position on the board as numpy arrays
import numpy as np
import argparse 
from main import read_logs
from shobu import ShobuGame
import os

# parse the arguments
parser = argparse.ArgumentParser(description='Shobu game')
parser.add_argument('folder', type=str, help='The folder containing the logs')

args = parser.parse_args()
folder = args.folder

files_black = os.listdir(folder+"/black")
files_white = os.listdir(folder+"/white")
files_draw  = os.listdir(folder+"/draw")

def convert_to_numpy(state):
    """
    state looks like [[{0,1,2,3}, {12,13,14,15}]]
    """
    boards = state.board
    numpy_board = np.zeros((1, 2*4*4))
    numpy_board.fill(-1)
    
    for i,board in enumerate(boards):
        for j,col in enumerate(board):
            for k,pawn in enumerate(col):
                numpy_board[0,i*8 + j*4 + k] = pawn

    return numpy_board

# New function to convert the game state to a numpy array
def game_state_to_numpy(actions):
    game = ShobuGame()
    state = game.initial
    game_result = np.zeros((1,32))
    
    for action, _ in actions:
        if action is not None:
            numpy_board = convert_to_numpy(state)
            game_result = np.vstack([game_result, numpy_board])
            state = game.result(state, action)

    game_result = game_result[1:]
    
    return game_result

    
for f in files_black:
    actions = read_logs(folder+"/black/"+f)

    game_result = game_state_to_numpy(actions)
    np.save(folder+"/numpy/black/"+f, game_result)
    
for f in files_white:
    actions = read_logs(folder+"/white/"+f)

    game_result = game_state_to_numpy(actions)
    np.save(folder+"/numpy/white/"+f, game_result)
    
    
for f in files_draw:
    actions = read_logs(folder+"/draw/"+f)

    game_result = game_state_to_numpy(actions)
    np.save(folder+"/numpy/draw/"+f, game_result)
    