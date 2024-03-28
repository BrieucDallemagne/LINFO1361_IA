"""
This python script aims at converting this dataset of shobu https://www.kaggle.com/datasets/bsfoltz/shobu-randomly-played-games-104k
to the standard output of the MCTS algorithm implemented in the contest.py file.
In our logs, white plays first
"""
import json
import argparse
import os
import shutil

def which_board(origin):
    """
    The board looks something like this
    oooo oooo
    .... ....
    .... ....
    xxxx xxxx

    oooo oooo
    .... ....
    .... ....
    xxxx xxxx
    And the data set uses those numbers to indicate location
    0 1 2 3  4 5 6 7 
    1    
    ...
    7
    In our games boards are like this:
    2 3
    0 1
    ON VA INVERSER LES TABLEAUX NSM
    """
    x = origin["x"]
    y = origin["y"]
    
    if y < 4:
        if x < 4:
            return 3
        else :
            return 2
    else:
        if x < 4:
            return 1
        else:
            return 0
   
def which_stones(origin):
    """
        Position Indexing on each board:
         12 | 13 | 14 | 15
        -------------------
          8 |  9 | 10 | 11
        -------------------
          4 |  5 |  6 |  7
        -------------------
          0 |  1 |  2 |  3
    """
    x = origin["x"]%4
    y = origin["y"]%4
    
    return 15 - 4*(y) - 3 + x
    
def direction(heading):
    """
    +3  | +4  | +5   (Upwards movements)
    ----------------
     -1  |     | +1   (Horizontal movements)
    ----------------
     -5  | -4  | -3   (Downwards movements)
    """
    x = heading["x"]
    y = heading["y"]
    
    if y > 0:
        if x < 0:
            return -5
        elif x > 0:
            return -3
        return -4
    elif y < 0:
        if x < 0:
            return 3
        elif x > 0:
            return 5
        return 4
    else:
        if x < 0:
            return -1
        return 1 

def length(heading):
    return max(abs(heading["x"]), abs(heading["y"]))

# define the parser
parser = argparse.ArgumentParser(description="Convert the shobu dataset to the standard output of the MCTS algorithm.")
parser.add_argument("input", type=str, help="The path to the input folder.")
parser.add_argument("output", type=str, help="The path to the output folder.")

# parse the arguments
args = parser.parse_args()
input_path = args.input
output_path = args.output

# read all json files one by one
files_black = os.listdir(input_path+"/black") 
files_white = os.listdir(input_path+"/white")

# Create the output folder
if os.path.exists(output_path):
    shutil.rmtree(output_path)
os.mkdir(output_path)
os.mkdir(output_path+"/black")
os.mkdir(output_path+"/white")
        
for filename in files_white:
    with open(input_path+"/white/"+filename) as f:
        data = json.load(f)
        
        turn_begin = data["game_states"][0]["turn"]
        moveset = data["turns"]
        
        #Inverting color (not a mistake) because of the flipped board
        with open(output_path+"/black/"+"".join(filename.split(".")[:-1])+".txt", "w") as out:
            for i, move in enumerate(moveset):
                out.write(f"{i}:{which_board(move['passive']['origin'])}:{which_stones(move['passive']['origin'])}:{which_board(move['aggressive']['origin'])}:{which_stones(move['aggressive']['origin'])}:{direction(move['aggressive']['heading'])}:{length(move['aggressive']['heading'])}\n")

for filename in files_black:
    with open(input_path+"/black/"+filename) as f:
        data = json.load(f)
        
        turn_begin = data["game_states"][0]["turn"]
        moveset = data["turns"]
        
        #Inverting color (not a mistake) because of the flipped board
        with open(output_path+"/white/"+"".join(filename.split(".")[:-1])+".txt", "w") as out:
            for i, move in enumerate(moveset):
                out.write(f"{i}:{which_board(move['passive']['origin'])}:{which_stones(move['passive']['origin'])}:{which_board(move['aggressive']['origin'])}:{which_stones(move['aggressive']['origin'])}:{direction(move['aggressive']['heading'])}:{length(move['aggressive']['heading'])}\n")
