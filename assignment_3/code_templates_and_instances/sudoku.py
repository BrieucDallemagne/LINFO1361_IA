import random
import time
import math
import sys
import numpy as np

 

def objective_score(board):
    score = 0
    for i in range(9):
        if len(np.unique(board[i])) != 9:
            score += 9 - len(np.unique(board[i]))
        if len(np.unique([board[j][i] for j in range(9)])) != 9:
            score += 9 - len(np.unique([board[j][i] for j in range(9)]))
        for j in range(9):
            if board[i][j] == 0:
                score += 1
    return score

def remplir_zeros(array):
    sub = find_subcarre(array)
    for carre in sub:
        for i in range(9):
            if carre[i] == 0:
                for j in range(9):
                    if j +1 not in carre:
                        carre[i] = j+1
                        

    array = subcarres_to_sudoku(sub)
    return array



def find_subcarre(sudoku):
    subcarres = []
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):  
            subcarre = []
            for k in range(3):  
                for l in range(3): 
                    subcarre.append(sudoku[i + k][j + l])
            subcarres.append(subcarre)
    return subcarres

def subcarres_to_sudoku(subcarres):
    sudoku = [[0] * 9 for _ in range(9)]    
    for i in range(0, 9, 3): 
        for j in range(0, 9, 3):  
            subcarre = subcarres.pop(0)  
            for k in range(3):  
                for l in range(3):  
                    sudoku[i + k][j + l] = subcarre[k * 3 + l]
    return sudoku

def random_swap(board,initial_board):
    
    sub_board = find_subcarre(board)
    sub_initial_board = find_subcarre(initial_board)
    for _ in range(10):
        board = random.randint(0,8)
        i = random.randint(0,8)
        j = random.randint(0,8)
        while sub_initial_board[board][i] != 0 or sub_initial_board[board][j] != 0:
            board = random.randint(0,8)
            i = random.randint(0,8)
            j = random.randint(0,8)
        sub_board[board][i],sub_board[board][j] = sub_board[board][j],sub_board[board][i]
    toreturn = subcarres_to_sudoku(sub_board)
    return toreturn
    
    
        



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
            if current_score == 0:

                return current_solution, current_score  
            n += 1  
            neighbor = [row[:] for row in current_solution]       
            neighbor_score = 0
            if n == 1:
                neighbor = remplir_zeros(neighbor)
                neighbor_score = objective_score(neighbor)
            else:
                random_swap(neighbor,initial_board)
                neighbor_score = objective_score(neighbor)
            
            # Calculate acceptance probability
            delta = float(current_score - neighbor_score)
            # Accept the neighbor with a probability based on the acceptance probability
            if neighbor_score < current_score or (neighbor_score > 0 and math.exp((delta/temperature)) > random.random()):

                current_solution = [row[:] for row in neighbor] 
                current_score = neighbor_score

                if (current_score < best_score):
                    best_solution = [row[:] for row in current_solution] 
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