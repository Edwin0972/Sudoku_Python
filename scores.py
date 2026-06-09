# Gestion des scores des joueurs

FICHIER_SCORES = "scores.txt"


def lire_scores():
    scores = {}
    try:
        with open(FICHIER_SCORES, "r") as fichier:
            for ligne in fichier:
                ligne = ligne.strip()
                if ligne == "":
                    continue
                parties = ligne.split(";")
                if len(parties) == 2:
                    nom = parties[0]
                    points = int(parties[1])
                    scores[nom] = points
    except FileNotFoundError:
        pass
    return scores


def enregistrer_score(nom, points):
    scores = lire_scores()
    if nom in scores:
        scores[nom] += points
    else:
        scores[nom] = points
    with open(FICHIER_SCORES, "w") as fichier:
        for joueur in scores:
            fichier.write(joueur + ";" + str(scores[joueur]) + "\n")
    return scores[nom]


def meilleur_score(scores):
    if len(scores) == 0:
        return None, 0
    meilleur_nom = None
    meilleur_points = None
    for nom in scores:
        if meilleur_points is None or scores[nom] > meilleur_points:
            meilleur_points = scores[nom]
            meilleur_nom = nom
    return meilleur_nom, meilleur_points


def afficher_graphe():
    scores = lire_scores()
    if len(scores) == 0:
        print("Aucun score enregistre pour le moment.")
        return
    nom, points = meilleur_score(scores)
    print("Meilleur score :", nom, "avec", points, "points")
    try:
        import matplotlib.pyplot as plt
        noms = list(scores.keys())
        valeurs = list(scores.values())
        plt.bar(noms, valeurs)
        plt.title("Scores des joueurs")
        plt.xlabel("Joueurs")
        plt.ylabel("Score")
        plt.show()
    except ImportError:
        print("matplotlib n'est pas installe, affichage texte :")
        for n in scores:
            print(n, ":", scores[n])
