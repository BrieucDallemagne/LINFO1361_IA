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
count = 0
bad = 0


for file in files:
    data = np.load(folder+"/"+file)
    res = model.predict(data)
    x = np.linspace(0, 1, len(res))
    
    plt.plot(x, res)
    # Add a red dot at the end if the last value is under 0.5
    if res[-1] < 0.5:
        plt.plot(1, res[-1], 'ro')
        bad += 1
    count += 1

plt.ylim(0,1)
# Draw horizontal line at 0.5
plt.axhline(y=0.5, color='r', linestyle='-')
plt.text(0, 0, f'bad: {bad/count *100:.2f} %', color='red', fontsize=12)


plt.show()
