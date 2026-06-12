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


def placement_valide(grille, ligne, colonne, valeur):
    """Verifie si valeur peut etre placee en (ligne, colonne) selon les regles."""
    for j in range(9):
        if grille[ligne][j] == valeur:
            return False
    for i in range(9):
        if grille[i][colonne] == valeur:
            return False
    debut_l = (ligne // 3) * 3
    debut_c = (colonne // 3) * 3
    for i in range(debut_l, debut_l + 3):
        for j in range(debut_c, debut_c + 3):
            if grille[i][j] == valeur:
                return False
    return True


def resoudre_grille(grille):
    """
    Resout la grille par backtracking (modifie la grille en place).
    Retourne True si une solution est trouvee.
    """
    for i in range(9):
        for j in range(9):
            if grille[i][j] == 0:
                for valeur in range(1, 10):
                    if placement_valide(grille, i, j, valeur):
                        grille[i][j] = valeur
                        if resoudre_grille(grille):
                            return True
                        grille[i][j] = 0
                return False
    return True
