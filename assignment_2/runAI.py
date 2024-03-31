import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import matplotlib.pyplot as plt

# Creating the basic model
model = Sequential([
    Dense(26, activation='relu', input_shape=(33,)),
    Dense(16, activation='relu'),
    Dense(8, activation='relu'),
    Dense(1, activation='sigmoid')
])

#model.compile(optimizer='adam', loss="binary_crossentropy" , metrics=['accuracy'])


model.load_weights("shobu_model_big2.keras")

for i,weight in enumerate(model.weights):
    print(weight.shape)
    print(weight.numpy())
    np.savetxt(f"weights/w{i}.txt", weight.numpy(), delimiter=",")

folder = "output_random100/numpy/black"
files = os.listdir(folder)
count = 0
bad = 0


for file in files:
    data = np.load(folder+"/"+file)
    turn = np.arange(data.shape[0])
    data = np.hstack([data, turn.reshape(-1,1)])
    
    res = model.predict(data)
    x = np.linspace(0, 1, len(res))
    
    plt.plot(x, res)
    # Add a red dot at the end if the last value is under 0.5
    if res[-1] < 0.5:
        plt.plot(1, res[-1], 'ro')
        bad += 1
    count += 1

plt.title("Évolution de la probabilité de victoire du joueur noir au cours de la partie")
plt.grid()
plt.ylabel("Probabilité de victoire")
plt.xlabel("Numéro du coup")
plt.grid()

plt.ylim(0,1)
# Draw horizontal line at 0.5
plt.axhline(y=0.5, color='r', linestyle='-')
plt.text(0, 0, f'bad: {bad/count *100:.2f} %', color='red', fontsize=12)


plt.show()
