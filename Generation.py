# Generation de la grille de jeu
import random

# Grille Sudoku valide de référence (solution complète)
GRILLE_SOLUTION = [
    [5, 3, 4, 6, 7, 8, 9, 1, 2],
    [6, 7, 2, 1, 9, 5, 3, 4, 8],
    [1, 9, 8, 3, 4, 2, 5, 6, 7],
    [8, 5, 9, 7, 6, 1, 4, 2, 3],
    [4, 2, 6, 8, 5, 3, 7, 9, 1],
    [7, 1, 3, 9, 2, 4, 8, 5, 6],
    [9, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 6, 1, 7, 9],
]

def generer_grille(difficulte):
    """
    Retourne la grille à afficher au joueur (cases masquées = 0)
    selon le niveau de difficulté.
    Facile : 40 cases visibles
    Intermédiaire : 35 cases visibles
    Difficile : 30 cases visibles
    """
    if difficulte == "Facile":
        nb_visibles = 40
    elif difficulte == "Intermédiaire":
        nb_visibles = 35
    else:
        nb_visibles = 30

    grille = [ligne[:] for ligne in GRILLE_SOLUTION]
    positions = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(positions)

    for r, c in positions[nb_visibles:]:
        grille[r][c] = 0

    return grille
