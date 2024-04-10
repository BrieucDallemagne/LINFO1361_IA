def find_subcarre(sudoku):
    subcarres = []
    for i in range(0, 9, 3):  # Parcours des lignes de 3 en 3
        for j in range(0, 9, 3):  # Parcours des colonnes de 3 en 3
            subcarre = []
            for k in range(3):  # Parcours des lignes du sous-carré
                for l in range(3):  # Parcours des colonnes du sous-carré
                    subcarre.append(sudoku[i + k][j + l])
            subcarres.append(subcarre)
    return subcarres

def subcarres_to_sudoku(subcarres):
    sudoku = [[0] * 9 for _ in range(9)]  # Initialisation du tableau Sudoku
    
    for i in range(0, 9, 3):  # Parcours des lignes de 3 en 3
        for j in range(0, 9, 3):  # Parcours des colonnes de 3 en 3
            subcarre = subcarres.pop(0)  # Retire le premier sous-carré de la liste
            for k in range(3):  # Parcours des lignes du sous-carré
                for l in range(3):  # Parcours des colonnes du sous-carré
                    sudoku[i + k][j + l] = subcarre[k * 3 + l]
    
    return sudoku

# Exemple d'utilisation :
sudoku = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

print("Sudoku initial :")
for row in sudoku:
    print(row)
sous_carres = find_subcarre(sudoku)
for i, sous_carre in enumerate(sous_carres, 1):
    print(f"Sous-carré {i}: {sous_carre}")

sudoku_reconstruit = subcarres_to_sudoku(sous_carres)
print("Sudoku reconstruit :")
for row in sudoku_reconstruit:
    print(row)