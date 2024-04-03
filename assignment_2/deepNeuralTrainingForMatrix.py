"""
Simple AI that takes game state and returns the expected win ranging from 0 to 1
"""
import argparse
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
# import deepcopy
from copy import deepcopy

num_turns = 50
num_pieces = 32

# parsing the data
argparser = argparse.ArgumentParser(description='Shobu game')
argparser.add_argument('folder', type=str, help='The folder containing the logs')
argparser.add_argument("--percent", type=float, help="The percentage of data to use for training")
argparser.add_argument("--load", type=bool, help="Load the numpy array")

args = argparser.parse_args()
folder = args.folder + "/numpy"
if args.load:
    load = True
else:
    load = False
if args.percent:
    percent_of_data = args.percent
else:  
    percent_of_data = 0.7

# Creating the basic model
# Creating 3 models where one is the start of the game, one is the middle and one is the end
class model_turn():
    def __init__(self, num_turns, num_pieces):
        self.model = Sequential()
        self.model.add(Flatten(input_shape=(num_turns, num_pieces)))  # Flatten the 2D input matrix
        self.model.add(Dense(64, activation='relu'))  # Add a dense layer
        self.model.add(Dense(1, activation='sigmoid'))  # Output layer with sigmoid activation for probability

        self.model.compile(optimizer='adam', loss="binary_crossentropy" , metrics=['accuracy'])
        
        self.model.summary()

    def predict(self, data):
        return self.model.predict(data)

    def fit(self, X, Y, epochs=10, batch_size=32):
        self.model.fit(X, Y, epochs=epochs, batch_size=batch_size)
    
    def summary(self):
        self.model.summary()
        
    def save(self, name):
        self.model.save(name)

class models():
    def __init__(self, list_of_models, size_of_models):
        self.models = list_of_models
        self.size = size_of_models
        
    def predict(self, data):
        for i,s in enumerate(self.size):
            if data.shape[0] < s:
                data = np.pad(data, ((s - data.shape[0], 0), (0,0)), 'constant', constant_values=0)
                return self.models[i].predict(data)
        return self.models[-1].predict(data[- self.size[-1]:]) # Too big no need for padding
                
    
# Start is less than 10 turns, middle is between 10 and 40 and end is more than 40
size = [10, 30, 50]
model_begin = model_turn(10, num_pieces)
model_middle = model_turn(30, num_pieces)
model_end = model_turn(50, num_pieces)
model = models([model_begin, model_middle, model_end], size)

# Training the model

# First loading all the training data
# Just loading a game
if not load:
    
    X_small = []
    Y_small = []
    
    X_middle = []
    Y_middle = []
    
    X_end = []
    Y_end = []
    
    X = []
    Y = []
    size = 0

    games = os.listdir(folder+"/draw")

    for game in games[:int(percent_of_data*len(games))]:
        data_main = np.load(folder+"/draw/"+game)
        # Trim the data to the last 50 turns
        # check if enough turns
        for i in range(len(data_main)-1):
            data = deepcopy(data_main)
            data = data[:i+1]
            # Check for what it would fit in
            if data.shape[0] < 10 and False:
                data = np.pad(data, ((10 - data.shape[0], 0), (0,0)), 'constant', constant_values=0)
                X_small.append(data)
                Y_small.append(0.5)
                
            elif data.shape[0] < 30 and False:
                data = np.pad(data, ((30 - data.shape[0], 0), (0,0)), 'constant', constant_values=0)
                X_middle.append(data)
                Y_middle.append(0.5)
                
            elif data.shape[0] < 50:
                data = np.pad(data, ((50 - data.shape[0], 0), (0,0)), 'constant', constant_values=0)
                X_end.append(data)
                Y_end.append(0.5)
                
            else:
                data = data[-50:]
                X_end.append(data)
                Y_end.append(0.5)
        
    print("Draw done")

    games = os.listdir(folder+"/black")

    for game in games[:int(percent_of_data*len(games))]:
        data = np.load(folder+"/black/"+game)
        # Trim the data to the last 50 turns
        # check if enough turns

        for i in range(len(data_main)-1):
            data = deepcopy(data_main)
            data = data[:i+1]
            # Check for what it would fit in
            if data.shape[0] < 10 and False:
                data = np.pad(data, ((10 - data.shape[0], 0), (0,0)), 'constant', constant_values=0)
                X_small.append(data)
                Y_small.append(1)
                
            elif data.shape[0] < 30 and False:
                data = np.pad(data, ((30 - data.shape[0], 0), (0,0)), 'constant', constant_values=0)
                X_middle.append(data)
                Y_middle.append(1)
                
            elif data.shape[0] < 50:
                data = np.pad(data, ((50 - data.shape[0], 0), (0,0)), 'constant', constant_values=0)
                X_end.append(data)
                Y_end.append(1)
                
            else:
                data = data[-50:]
                X_end.append(data)
                Y_end.append(1)
        
    print("Black done")

    
    games = os.listdir(folder+"/white")

    for game in games[:int(percent_of_data*len(games))]:
        data = np.load(folder+"/white/"+game)
        # Trim the data to the last 50 turns
        # check if enough turns
        for i in range(len(data_main)-1):
            data = deepcopy(data_main)
            data = data[:i+1]
            # Check for what it would fit in
            if data.shape[0] < 10 and False:
                data = np.pad(data, ((10 - data.shape[0], 0), (0,0)), 'constant', constant_values=0)
                X_small.append(data)
                Y_small.append(0)
                
            elif data.shape[0] < 30 and False:
                data = np.pad(data, ((30 - data.shape[0], 0), (0,0)), 'constant', constant_values=0)
                X_middle.append(data)
                Y_middle.append(0)
                
            elif data.shape[0] < 50:
                data = np.pad(data, ((50 - data.shape[0], 0), (0,0)), 'constant', constant_values=0)
                X_end.append(data)
                Y_end.append(0)
                
            else:
                data = data[-50:]
                X_end.append(data)
                Y_end.append(0)
        

    """
    print("White done")
    X_small = np.array(X_small)
    Y_small = np.array(Y_small)
    print("X_small done")
    
    X_middle = np.array(X_middle)
    Y_middle = np.array(Y_middle)
    print("X_middle done")
    """
    X_end = np.array(X_end)
    Y_end = np.array(Y_end)
    print("X_end done")
    """
    np.save("X_small.npy", X_small)
    np.save("Y_small.npy", Y_small)
    
    np.save("X_middle.npy", X_middle)
    np.save("Y_middle.npy", Y_middle)   
    """
    np.save("X_end.npy", X_end) 
    np.save("Y_end.npy", Y_end)
    
else:
    X_small = np.load("X_small.npy")
    Y_small = np.load("Y_small.npy")
    
    X_middle = np.load("X_middle.npy")
    Y_middle = np.load("Y_middle.npy")   
    
    X_end = np.load("X_end.npy") 
    Y_end = np.load("Y_end.npy")

""" 
model_begin.fit(X_small, Y_small, epochs=10, batch_size=32)
model_begin.save("model_begin.keras")

model_middle.fit(X_middle, Y_middle, epochs=10, batch_size=32)
model_middle.save("model_middle.keras")
"""
model_end.fit(X_end, Y_end, epochs=10, batch_size=32)
model_end.save("model_end.keras")

# Testing the model
# Example with a white win

games = os.listdir("output_random100"+"/numpy/white")

for game in games:
    data = np.load("output_random100"+"/numpy/white/"+game)
    if data.shape[0] > num_turns:
        data = data[-num_turns:]
    else:
        data = np.pad(data, ((num_turns - data.shape[0], 0), (0,0)), 'constant', constant_values=0)
    
    print(model.predict(data))