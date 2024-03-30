import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import matplotlib.pyplot as plt

# Creating the basic model
model = Sequential([
    Dense(26, activation='relu', input_shape=(32,)),
    Dense(16, activation='relu'),
    Dense(8, activation='relu'),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss="binary_crossentropy" , metrics=['accuracy'])


model.load_weights("shobu_model_big.keras")

folder = "output_random100/numpy/black"
files = os.listdir(folder)

for file in files:
    data = np.load(folder+"/"+file)
    res = model.predict(data)
    plt.plot(res)
    plt.ylim(0,1)
    plt.show()
    exit()