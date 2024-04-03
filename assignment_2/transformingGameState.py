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

def reward_system(game, state, actions, depth=2):
    """
    Returns the reward for the given state
    take point of view of black ! Positive is for black negative for white
    
    1. reward the amount of pieces on the board 
    2. reward if there is a win 
    3. punish if it loses a piece
    4. punish if it loses the game
    """
    # It's either I generate tons of state from this state or just read ahead ?
    value = 0
    equivalence_list = [-50, -10, -5, -2, 0, 2, 5, 10, 50]
    value_board = [0, 0, 0, 0]
    a = 0

    for i in range(4):
        white_value = len(state.board[i][0])
        black_value = len(state.board[i][1])
        
        # Check for win
        if white_value == 0:
            value_board[i] += equivalence_list[8]
        elif black_value == 0:
            value_board[i] += equivalence_list[0]
        else:
            value_board[i] += equivalence_list[8-black_value] # 4 is the middle of the list
            value_board[i] += equivalence_list[white_value] # 4 is the middle of the list
    
    for action, _ in actions:
        state = game.result(state, action)
        for i in range(4):
            white_value = len(state.board[i][0])
            black_value = len(state.board[i][1])

            # Check for win
            if white_value == 0:
                value_board[i] += equivalence_list[8]
            elif black_value == 0:
                value_board[i] += equivalence_list[0]
            else:
                value_board[i] += equivalence_list[8-black_value] # 4 is the middle of the list
                value_board[i] += equivalence_list[white_value] # 4 is the middle of the list
        a+=1 # to count the amount of action actually taken

    for i in range(4):
        value_board[i] /= (1+a)
    #print(value_board)
    return np.array(value_board).reshape(1,4)
            

# New function to convert the game state to a numpy array
def game_state_to_numpy(actions, depth=5):
    game = ShobuGame()
    state = game.initial
    game_result = np.zeros((1,36))
    i = 0
    
    # Depth indicates how many moves we want to look ahead O(2^n) watch out !

    for action, _ in actions:
        numpy_board = convert_to_numpy(state)
        numpy_board = np.hstack([numpy_board, reward_system(game, state, actions[i:i+depth], depth)])
        game_result = np.vstack([game_result, numpy_board])
        state = game.result(state, action)

        i += 1
    
    # To have the end state
    numpy_board = convert_to_numpy(state)
    numpy_board = np.hstack([numpy_board, reward_system(game, state, actions[i:i+depth], depth)])
    game_result = np.vstack([game_result, numpy_board])

    game_result = game_result[1:]
    
    return game_result

    
for f in files_black:
    actions = read_logs(folder+"/black/"+f)

    game_result = game_state_to_numpy(actions)
    #print(game_result[-2:,32:])
    #print(np.count_nonzero(game_result[-1,32:]==50))
    np.save(folder+"/numpy/black/"+f, game_result)

for f in files_white:
    actions = read_logs(folder+"/white/"+f)

    game_result = game_state_to_numpy(actions)
    np.save(folder+"/numpy/white/"+f, game_result)
    
for f in files_draw:
    actions = read_logs(folder+"/draw/"+f)

    game_result = game_state_to_numpy(actions)
    np.save(folder+"/numpy/draw/"+f, game_result)
    