# Calcul du score
# Vérifier si la partie est interrompu et calculer le score en conséquence
if partieInterrompu:
    if difficulte == "Facile":
        score -= 1
    elif difficulte == "Intermédiaire":
        score -= 2
    else:
        score -= 3
# Calculer le score si la partie est gagné
else:
    if difficulte == "Facile":
        score += 2
    elif difficulte == "Intermédiaire":
        score += 4
    else:
        score += 8
