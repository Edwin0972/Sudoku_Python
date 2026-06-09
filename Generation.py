# Generation nombre aléatoire
import random

if difficulte == "Facile":
    nombre_cases = 40
elif difficulte == "Intermediaire":
    nombre_cases = 35
else:
    nombre_cases = 30

for i in range(nombre_cases):

    ligne = random.randint(0, 8)
    colonne = random.randint(0, 8)
    valeur = random.randint(1, 9)

    # Vérifier ici que la valeur respecte les règles
    # puis l'écrire dans la grille
