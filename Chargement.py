# Chargement des grilles et des sauvegardes

def charger_sauvegarde():
    """
    Charge une partie sauvegardée depuis save.txt.
    Retourne (difficulte, nom_joueur, grille_actuelle, grille_originale)
    ou None si aucune sauvegarde.
    """
    try:
        with open("save.txt", "r") as fichier:
            lignes = fichier.read().strip().split("\n")
        difficulte    = lignes[0]
        nom_joueur    = lignes[1]
        grille_actuelle  = [[int(x) for x in lignes[i].split(",")]   for i in range(2, 11)]
        grille_originale = [[int(x) for x in lignes[i].split(",")]   for i in range(11, 20)]
        print("Sauvegarde chargée.")
        return difficulte, nom_joueur, grille_actuelle, grille_originale
    except (FileNotFoundError, IndexError, ValueError):
        return None

def charger_grille(difficulte):
    """
    Charge une grille depuis un fichier texte selon le niveau.
    Si le fichier n'existe pas, utilise generer_grille() comme fallback.
    Retourne la grille sous forme de liste 9x9.
    """
    from Generation import generer_grille  # import ici pour éviter les imports circulaires

    if difficulte == "Facile":
        nom_fichier = "niveau_facile.txt"
    elif difficulte == "Intermédiaire":
        nom_fichier = "niveau_intermediaire.txt"
    else:
        nom_fichier = "niveau_difficile.txt"

    try:
        with open(nom_fichier, "r") as fichier:
            lignes = fichier.read().strip().split("\n")
        grille = [[int(x) for x in ligne.split(",")] for ligne in lignes]
        print(f"Grille chargée depuis {nom_fichier}.")
        return grille
    except FileNotFoundError:
        print(f"{nom_fichier} introuvable, génération aléatoire.")
        return generer_grille(difficulte)
