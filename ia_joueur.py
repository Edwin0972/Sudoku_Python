# IA_Joueur : resout la grille automatiquement (backtracking)

from grille import placement_possible, afficher_grille


def colonne_en_lettre(colonne):
    lettres = "ABCDEFGHI"
    return lettres[colonne]


# Resolution par backtracking, avec affichage des placements
def resoudre(grille, affichage=True):
    for i in range(9):
        for j in range(9):
            if grille[i][j] == 0:
                for valeur in range(1, 10):
                    if placement_possible(grille, i, j, valeur):
                        grille[i][j] = valeur
                        if affichage:
                            print("IA_Joueur place le", valeur,
                                  "en ligne", i + 1,
                                  "colonne", colonne_en_lettre(j))
                        if resoudre(grille, affichage):
                            return True
                        grille[i][j] = 0
                return False
    return True


def jouer_ia(grille):
    print("IA_Joueur commence a jouer...")
    if resoudre(grille, True):
        print("IA_Joueur a termine la grille !")
        afficher_grille(grille)
        return True
    else:
        print("Aucune solution possible pour cette grille.")
        return False
