# Calcul du score

def calculer_score(score, difficulte, partieInterrompu):
    """
    Met à jour le score selon la difficulté et l'issue de la partie.
    - partieInterrompu = True  → score négatif
    - partieInterrompu = False → partie gagnée, score positif
    Retourne le nouveau score.
    """
    if partieInterrompu:
        if difficulte == "Facile":
            score -= 1
        elif difficulte == "Intermédiaire":
            score -= 2
        else:
            score -= 3
    else:
        if difficulte == "Facile":
            score += 2
        elif difficulte == "Intermédiaire":
            score += 4
        else:
            score += 8

    return score
