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

    def within_bounds(x: int, y: int) -> bool:

        return 0 <= x < size and 0 <= y < size

    def add_clause(expression: list[Clause], x1: int, y1: int, x2: int, y2: int):

        if within_bounds(x1, y1) and within_bounds(x2, y2):
            clause = Clause(size)
            clause.add_negative(x1, y1)
            clause.add_negative(x2, y2)
            expression.append(clause)

    lst = [[1,4],[-1,4],[1,-4],[-1,-4],[4,1],[-4,1],[4,-1],[-4,-1],[2,3],[-2,3],[2,-3],[-2,-3],[3,2],[-3,2],[3,-2],[-3,-2]]

    expression = []

    for y in range(size):
        for x1 in range(size):
            for x2 in range(x1 + 1, size):
                add_clause(expression, x1, y, x2, y)

    for x in range(size):
        for y1 in range(size):
            for y2 in range(y1 + 1, size):
                add_clause(expression, x, y1, x, y2)

    for x1 in range(size):
        for y1 in range(size):
            for dx, dy in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                x2, y2 = x1 + dx, y1 + dy
                while within_bounds(x2, y2):
                    add_clause(expression, x1, y1, x2, y2)
                    x2, y2 = x2 + dx, y2 + dy

    for amazon in placed_amazons:
        x, y = amazon
        clause = Clause(size)
        clause.add_positive(x, y)
        expression.append(clause)

    for x, y in placed_amazons:
        for dx, dy in lst:
            x1, y1 = x + dx, y + dy
            if within_bounds(x1, y1):
                clause = Clause(size)
                clause.add_negative(x, y)
                clause.add_negative(x1, y1)
                expression.append(clause)

    return expression