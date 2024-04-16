from namazon import *
import matplotlib.pyplot as plt

# Benchmarking variables
sizes = [10, 11, 12, 13, 20, 25, 30]
problems = [NAmazonsProblem(size) for size in sizes]

compare_searchers(problems, ["nom", 10, 11, 12, 13, 20, 25, 30], [astar_search, breadth_first_graph_search, depth_first_graph_search])