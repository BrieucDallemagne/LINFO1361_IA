"""
Simple AI that takes game state and returns the expected win ranging from 0 to 1
"""

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

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
folder = "output_30"

