from clause import *

"""
For the n-amazon problem, the only code you have to do is in this file.

You should replace

# your code here

by a code generating a list of clauses modeling the n-amazons problem
for the input file.

You should build clauses using the Clause class defined in clause.py

Here is an example presenting how to create a clause:
Let's assume that the length/width of the chessboard is 4.
To create a clause X_0_1 OR ~X_1_2 OR X_3_3
you can do:

clause = Clause(4)
clause.add_positive(0, 1)
clause.add_negative(1, 2)
clause.add_positive(3, 3)

The clause must be initialized with the length/width of the chessboard.
The reason is that we use a 2D index for our variables but the format
imposed by MiniSAT requires a 1D index.
The Clause class automatically handle this change of index, but needs to know the
number of column and row in the chessboard.

X_0_0 is the literal representing the top left corner of the chessboard
"""


def get_expression(size: int, placed_amazons: list[(int, int)]) -> list[Clause]:
    """
    Defines the clauses for the N-amazons problem
    :param size: length/width of the chessboard
    :param placed_amazons: a list of the already placed amazons
    :return: a list of clauses
    """


    lst = [(1, 4), (-1, 4), (1, -4), (-1, -4), (4, 1), 
        (-4, 1), (4, -1), (-4, -1), (2, 3), (-2, 3),
        (2, -3), (-2, -3), (3, 2), (-3, 2), (3, -2), (-3, -2)]

    expression = []

    for (i, j) in placed_amazons:
        clause = Clause(size)
        clause.add_positive(i, j)
        expression.append(clause)

    for i in range(size):
        clause = Clause(size)
        for j in range(size):
            clause.add_positive(i, j)
        expression.append(clause)

    for i in range(size):
        for j in range(size):
            for k in range( size):
                if k != j:
                    clause = Clause(size)
                    clause.add_negative(i, j)
                    clause.add_negative(i, k)
                    expression.append(clause)

    for i in range(size):
        for j in range(size):
            for k in range( size):
                if k != i:
                    clause = Clause(size)
                    clause.add_negative(i, j)
                    clause.add_negative(k, j)
                    expression.append(clause)

    #rising diagonals
    for d in range(2*size - 1):
        for i in range(max(0, d - size + 1), min(d + 1, size)):
            for j in range(i+1, min(d + 1, size)):
                if d - i < size and d - j < size:
                    clause = Clause(size)
                    clause.add_negative(i, d - i)
                    clause.add_negative(j, d - j)
                    expression.append(clause)

    #falling diagonals
    for d in range(-size + 1, size):
        for i in range(max(0, -d), min(size, size - d)):
            for j in range(i+1, min(size, size - d)):
                if i + d < size and j + d < size:
                    clause = Clause(size)
                    clause.add_negative(i, i + d)
                    clause.add_negative(j, j + d)
                    expression.append(clause)


    for i in range(size):
        for j in range(size):
            for (dx, dy) in lst:
                x = i + dx
                y = j + dy
                if x >= 0 and x < size and y >= 0 and y < size:
                    clause = Clause(size)
                    clause.add_negative(i, j)
                    clause.add_negative(x, y)
                    expression.append(clause)


    return expression