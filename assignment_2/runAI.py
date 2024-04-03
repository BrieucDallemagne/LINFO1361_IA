import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import matplotlib.pyplot as plt

# Creating the basic model
model = Sequential()
model.add(Dense(64, input_shape=(32,), activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(16, activation='relu'))
model.add(Dense(4, activation='linear'))  # Output layer with linear activation

#model.compile(optimizer='adam', loss="binary_crossentropy" , metrics=['accuracy'])


model.load_weights("shobu_reward.keras")

for i,weight in enumerate(model.weights):
    print(weight.shape)
    print(weight.numpy())
    np.savetxt(f"weights/w{i}.txt", weight.numpy(), delimiter=",")

folder = "output_random100/numpy/white"
files = os.listdir(folder)
count = 0
bad = 0


for file in files:
    data = np.load(folder+"/"+file)
    data = data[:, :32]
        
    res = model.predict(data)
    x = np.linspace(0, 1, len(res))
    
    plt.plot(x, np.sum(res, axis=1))
    # Add a red dot at the end if the last value is under 0.5
    """if res[-1] < 0.5:
        plt.plot(1, res[-1], 'ro')
        bad += 1
    count += 1"""

plt.title("Évolution de la probabilité de victoire du joueur noir au cours de la partie")
plt.grid()
plt.ylabel("Probabilité de victoire")
plt.xlabel("Numéro du coup")

plt.ylim(-50,50)
# Draw horizontal line at 0.5
plt.axhline(y=0, color='r', linestyle='-')
#plt.text(0, 0, f'bad: {bad/count *100:.2f} %', color='red', fontsize=12)


plt.show()
