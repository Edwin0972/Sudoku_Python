#Charger une partie
# Vérifiez qu’une partie est existante
try:
    with open("save.txt", "r") as fichier:
        contenu = fichier.read()
except FileNotFoundError:
    print("Aucune sauvegarde")


# Charger nouvelle grille
if difficulte == "Facile":
    with open("niveau_facile.txt", "r") as fichier:
        grille = fichier.read()

elif difficulte == "Intermediaire":
    with open("niveau_intermediaire.txt", "r") as fichier:
        grille = fichier.read()

else:
    with open("niveau_difficile.txt", "r") as fichier:
        grille = fichier.read()
