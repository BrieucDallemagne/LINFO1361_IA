from namazon import *
import matplotlib.pyplot as plt

"""
# Benchmarking variables
sizes = [35]
problems = [NAmazonsProblem(size) for size in sizes]

compare_searchers(problems, ["nom", 35], [astar_search])

"""
x = [10,11,12,13,14,15,20,25,30,35]

# A star
A_EN = [21,57,128,448,1527,114,746,252,144, 99]

# BFS
BFS_EN = [325, 24, 173,107,6580,2606,5181,319795]

# DFS
DFS_EN = [2298, 7149, 23923, 87922]

plt.plot(x, A_EN, label="A*")
plt.plot(x[:len(BFS_EN)], BFS_EN, label="BFS")
plt.plot(x[:len(DFS_EN)], DFS_EN, label="DFS")

# set Y log scale
plt.yscale('log')
plt.grid(True)
plt.grid(True, which="minor", axis="y", ls="--")
plt.legend()

plt.title("Amount of Expanded Nodes for NAmazons")
plt.ylabel("Amount Expanded Nodes [EN]")
plt.xlabel("NAmazons Size [N]")

plt.savefig("benchmark_namazon.pdf")
plt.show()