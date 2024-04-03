import os
import numpy as np

folder = "output_random1000/numpy/white"
files = os.listdir(folder)

for file in files:
    data = np.load(folder+"/"+file)
    data = data[:, 32:]
    
    print(data[-2:,:]) 

