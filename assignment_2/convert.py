"""
This python script aims at converting this dataset of shobu https://www.kaggle.com/datasets/bsfoltz/shobu-randomly-played-games-104k
to the standard output of the MCTS algorithm implemented in the contest.py file.
"""
import json
import argparse
import os

# define the parser
parser = argparse.ArgumentParser(description="Convert the shobu dataset to the standard output of the MCTS algorithm.")
parser.add_argument("input", type=str, help="The path to the input folder.")
parser.add_argument("output", type=str, help="The path to the output folder.")

# parse the arguments
args = parser.parse_args()
input_path = args.input
output_path = args.output

# read all json files one by one
