# Chargement des grilles et des sauvegardes

def charger_sauvegarde():
    """
    Charge une partie sauvegardée depuis save.txt.
    Retourne le contenu sous forme de liste 9x9, ou None si aucune sauvegarde.
    """
    try:
        with open("save.txt", "r") as fichier:
            lignes = fichier.read().strip().split("\n")
        grille = []
        for ligne in lignes:
            grille.append([int(x) for x in ligne.split(",")])
        print("Sauvegarde chargée.")
        return grille
    except FileNotFoundError:
        print("Aucune sauvegarde.")
        return None

def charger_grille(difficulte):
    """
    Charge une grille depuis un fichier texte selon le niveau.
    Retourne la grille sous forme de liste 9x9, ou None si fichier introuvable.
    """
    if difficulte == "Facile":
        nom_fichier = "niveau_facile.txt"
    elif difficulte == "Intermédiaire":
        nom_fichier = "niveau_intermediaire.txt"
    else:
        nom_fichier = "niveau_difficile.txt"

    try:
        with open(nom_fichier, "r") as fichier:
            lignes = fichier.read().strip().split("\n")
        grille = []
        for ligne in lignes:
            grille.append([int(x) for x in ligne.split(",")])
        return grille
    except FileNotFoundError:
        print(f"Fichier introuvable : {nom_fichier}")
        return None
