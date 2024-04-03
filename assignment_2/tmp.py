import os
import numpy as np

file = "ingi.txt"

with open(file, "r") as f_in:
    f_in = f_in.readlines()[0].replace("|", "\n")
    print(f_in)
    
    with open(file+"Out", "w") as f_out:
        f_out.write(f_in)

