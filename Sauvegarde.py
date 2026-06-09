# Gestion de la sauvegarde
import os

def sauvegarder_partie(difficulte, nom_joueur, grille_actuelle, grille_originale):
    """
    Sauvegarde l'état de la partie dans save.txt.
    Format :
      ligne 1  : difficulte
      ligne 2  : nom_joueur
      lignes 3-11  : grille actuelle (valeurs joueur + cases vides = 0)
      lignes 12-20 : grille originale (cases pré-remplies)
    """
    with open("save.txt", "w") as fichier:
        fichier.write(difficulte + "\n")
        fichier.write(nom_joueur + "\n")
        for ligne in grille_actuelle:
            fichier.write(",".join(str(v) for v in ligne) + "\n")
        for ligne in grille_originale:
            fichier.write(",".join(str(v) for v in ligne) + "\n")
    print("Partie sauvegardée.")

def supprimer_sauvegarde():
    """Supprime save.txt après une partie terminée."""
    try:
        os.remove("save.txt")
    except FileNotFoundError:
        pass
