import random
import time
import math
import sys
import numpy as np

 

def objective_score(board):
    score = 0
    for i in range(9):
        score += 9-len(np.unique(board[i])) 
        score += 9-len(np.unique([board[j][i] for j in range(9)]))
    return score

def remplir_zeros(array):
    counts = [np.count_nonzero(array == i) for i in range(1, 10)]
    for i in range(len(array)):
        for j in range(len(array[i])):
            if array[i][j] == 0:
                for k in range(1, 10):
                    if counts[k-1] < 9:
                        array[i][j] = k
                        counts[k-1] += 1
                        break
    return array
        



def simulated_annealing_solver(initial_board):

    """Simulated annealing Sudoku solver."""

    current_solution = [row[:] for row in initial_board]
    best_solution = current_solution
    
    current_score = objective_score(current_solution)
    best_score = current_score
    n = 0

    temperature = 1.0
    cooling_rate = 0.999

    while temperature > 0.0001:

        try:  
            n += 1
            
            neighbor = current_solution.copy()           
            neighbor_score = 0
            if n == 1:
                neighbor = remplir_zeros(neighbor)
                neighbor_score = objective_score(neighbor)
            else:
                for i in range(9):
                    pos1 = (random.randint(0, 8), random.randint(0, 8))
                    pos2 = (random.randint(0, 8), random.randint(0, 8))
                    while initial_board[pos1[0]][pos1[1]] != 0 or initial_board[pos2[0]][pos2[1]] != 0:
                        pos1 = (random.randint(0, 8), random.randint(0, 8))
                        pos2 = (random.randint(0, 8), random.randint(0, 8))
                    
                        neighbor[pos1[0]][pos1[1]], neighbor[pos2[0]][pos2[1]] = neighbor[pos2[0]][pos2[1]], neighbor[pos1[0]][pos1[1]]


            # Evaluate the neighbor
            neighbor_score = objective_score(neighbor)

            # Calculate acceptance probability
            delta = float(current_score - neighbor_score)

            if current_score == 0:

                return current_solution, current_score

            # Accept the neighbor with a probability based on the acceptance probability
            if neighbor_score < current_score or (neighbor_score > 0 and math.exp((delta/temperature)) > random.random()):

                current_solution = neighbor
                current_score = neighbor_score

                if (current_score < best_score):
                    best_solution = current_solution
                    best_score = current_score

            # Cool down the temperature
            temperature *= cooling_rate
        except:

            print("Break asked")
            break
        
    return best_solution, best_score

 
def print_board(board):

    """Print the Sudoku board."""

    for row in board:
        print("".join(map(str, row)))

 

def read_sudoku_from_file(file_path):
    """Read Sudoku puzzle from a text file."""
    
    with open(file_path, 'r') as file:
        sudoku = [[int(num) for num in line.strip()] for line in file]

    return sudoku
 

if __name__ == "__main__":

    # Reading Sudoku from file
    initial_board = read_sudoku_from_file(sys.argv[1])

    # Solving Sudoku using simulated annealing
    start_timer = time.perf_counter()

    solved_board, current_score = simulated_annealing_solver(initial_board)

    end_timer = time.perf_counter()

    print_board(solved_board)
    print("\nValue(C):", current_score)

    # print("\nTime taken:", end_timer - start_timer, "seconds")