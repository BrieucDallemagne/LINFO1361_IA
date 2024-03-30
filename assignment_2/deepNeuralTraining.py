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

args = argparser.parse_args()
folder = args.folder + "/numpy"
if args.percent:
    percent_of_data = args.percent
else:  
    percent_of_data = 0.7

# Creating the basic model
model = Sequential([
    Dense(16, activation='relu', input_shape=(32,)),
    Dense(8, activation='relu'),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

model.summary()

# Training the model

# First loading all the training data
# Just loading a game

X = np.zeros((1, 32))
Y = np.zeros((1, 1))

games = os.listdir(folder+"/draw")

for game in games[:int(percent_of_data*len(games))]:
    data = np.load(folder+"/draw/"+game)
    X = np.vstack([X, data])
    tmp = np.zeros((data.shape[0], 1))
    tmp.fill(0.5)
    Y = np.vstack([Y, tmp])
    
print(X.shape)
print(Y.shape)


games = os.listdir(folder+"/black")

for game in games[:int(percent_of_data*len(games))]:
    data = np.load(folder+"/black/"+game)
    X = np.vstack([X, data])
    Y = np.vstack([Y, np.zeros((data.shape[0], 1))])
    
print(X.shape)
print(Y.shape)
    
games = os.listdir(folder+"/white")

for game in games[:int(percent_of_data*len(games))]:
    data = np.load(folder+"/white/"+game)
    X = np.vstack([X, data])
    Y = np.vstack([Y, np.ones((data.shape[0], 1))])
    
print(X.shape)
print(Y.shape)

X = X[1:]
Y = Y[1:]

model.fit(X, Y, epochs=10, batch_size=32)
    