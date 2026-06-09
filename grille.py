# Gestion de la grille de Sudoku
# Une grille est une liste de 9 listes de 9 entiers (0 = case vide)


def charger_grille(nom_fichier):
    grille = []
    with open(nom_fichier, "r") as fichier:
        for ligne in fichier:
            ligne = ligne.strip()
            if ligne == "":
                continue
            nombres = []
            for c in ligne:
                if c.isdigit():
                    nombres.append(int(c))
            if len(nombres) == 9:
                grille.append(nombres)
    return grille


def copier_grille(grille):
    nouvelle = []
    for ligne in grille:
        nouvelle.append(list(ligne))
    return nouvelle


def afficher_grille(grille):
    print()
    print("     A B C   D E F   G H I")
    print("   +-------+-------+-------+")
    for i in range(9):
        ligne_txt = str(i + 1) + "  | "
        for j in range(9):
            valeur = grille[i][j]
            if valeur == 0:
                ligne_txt += ". "
            else:
                ligne_txt += str(valeur) + " "
            if j == 2 or j == 5:
                ligne_txt += "| "
        ligne_txt += "|"
        print(ligne_txt)
        if i == 2 or i == 5:
            print("   +-------+-------+-------+")
    print("   +-------+-------+-------+")
    print()


def grille_complete(grille):
    for i in range(9):
        for j in range(9):
            if grille[i][j] == 0:
                return False
    return True


# Verifie si on peut placer valeur en (ligne, colonne) selon les regles
def placement_possible(grille, ligne, colonne, valeur):
    # Verifier la ligne
    for j in range(9):
        if grille[ligne][j] == valeur:
            return False
    # Verifier la colonne
    for i in range(9):
        if grille[i][colonne] == valeur:
            return False
    # Verifier le carre 3x3
    debut_ligne = (ligne // 3) * 3
    debut_colonne = (colonne // 3) * 3
    for i in range(debut_ligne, debut_ligne + 3):
        for j in range(debut_colonne, debut_colonne + 3):
            if grille[i][j] == valeur:
                return False
    return True
