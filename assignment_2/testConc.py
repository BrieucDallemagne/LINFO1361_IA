import numpy as np
import os

folderPath = "numpy_test/numpy/black"
files_black = os.listdir(folderPath)

a1 = np.load(folderPath + "/" + files_black[0])
a2 = np.load(folderPath + "/" + files_black[1])

a3 = np.array([*a1, *a2])
print(a3.shape)