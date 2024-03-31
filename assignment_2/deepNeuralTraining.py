"""
Simple AI that takes game state and returns the expected win ranging from 0 to 1
"""
import argparse
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

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
model = Sequential([
    Dense(26, activation='relu', input_shape=(33,)),
    Dense(16, activation='relu'),
    Dense(8, activation='relu'),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss="binary_crossentropy" , metrics=['accuracy'])

model.summary()

# Training the model

# First loading all the training data
# Just loading a game
if not load:
    X = []
    Y = []
    size = 0

    games = os.listdir(folder+"/draw")

    for game in games[:int(percent_of_data*len(games))]:
        data = np.load(folder+"/draw/"+game)
        turn = np.arange(data.shape[0])
        data = np.hstack([data, turn.reshape(-1,1)])
        
        X = [*X,*data]
    
    tmp = np.zeros(len(X) - size)
    tmp.fill(0.5)
    Y = [*Y, *tmp]
    size = len(X)
    
    print(len(X))
    print(len(Y))
    print(size)


    games = os.listdir(folder+"/black")

    for game in games[:int(percent_of_data*len(games))]:
        data = np.load(folder+"/black/"+game)
        turn = np.arange(data.shape[0])
        data = np.hstack([data, turn.reshape(-1,1)])
        
        X = [*X,*data]
        
    Y = [*Y, *np.ones(len(X) - size)]
    size = len(X)

        
    print(len(X))
    print(len(Y))
    print(size)

    
    games = os.listdir(folder+"/white")

    for game in games[:int(percent_of_data*len(games))]:
        data = np.load(folder+"/white/"+game)
        turn = np.arange(data.shape[0])
        data = np.hstack([data, turn.reshape(-1,1)])
        
        X = [*X,*data]

    Y = [*Y, *np.zeros(len(X) - size)]
    size = len(X)


    print(len(X))
    print(len(Y))
    print(size)

    Y = np.array(Y)
    X = np.array(X)

    np.save("X.npy", X)
    np.save("Y.npy", Y)
else:
    X = np.load("X.npy")
    Y = np.load("Y.npy")

    
model.fit(X, Y, epochs=10, batch_size=32)


# Saving the model
model.save("shobu_model_big2.keras")

# Testing the model
# Example with a white win

exit()
game = games[-4:-1]

for g in game:
    data = np.load(folder+"/white/"+g)
    print(model.predict(data).mean()) # Takes the mean of all moves at all states to show if it's a win or not
print("______")
games = os.listdir(folder+"/black")

for game in games[int(percent_of_data*len(games)):]:
    data = np.load(folder+"/black/"+game)
    print(model.predict(data).mean())