# Sauvegarde et chargement d'une partie en pause

FICHIER_SAVE = "save.txt"


def sauvegarder_partie(grille, nom_joueur, difficulte, score):
    with open(FICHIER_SAVE, "w") as fichier:
        fichier.write(nom_joueur + "\n")
        fichier.write(difficulte + "\n")
        fichier.write(str(score) + "\n")
        for ligne in grille:
            ligne_txt = ""
            for valeur in ligne:
                ligne_txt += str(valeur)
            fichier.write(ligne_txt + "\n")
    print("Partie sauvegardee.")


def partie_existe():
    try:
        with open(FICHIER_SAVE, "r") as fichier:
            contenu = fichier.read()
            if contenu.strip() != "":
                return True
    except FileNotFoundError:
        return False
    return False


def charger_partie():
    with open(FICHIER_SAVE, "r") as fichier:
        lignes = fichier.read().split("\n")
    nom_joueur = lignes[0]
    difficulte = lignes[1]
    score = int(lignes[2])
    grille = []
    for i in range(3, 12):
        ligne = lignes[i]
        nombres = []
        for c in ligne:
            nombres.append(int(c))
        grille.append(nombres)
    return grille, nom_joueur, difficulte, score
