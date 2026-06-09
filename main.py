# Projet Sudoku - mode console
# Jeu de Sudoku pour un joueur (humain ou IA_Joueur)

from grille import (charger_grille, copier_grille, afficher_grille,
                    grille_complete, placement_possible)
from ia_joueur import jouer_ia
from scores import enregistrer_score, afficher_graphe
from sauvegarde import (sauvegarder_partie, partie_existe, charger_partie)


def lettre_en_colonne(lettre):
    lettres = "ABCDEFGHI"
    lettre = lettre.upper()
    if lettre in lettres:
        return lettres.index(lettre)
    return -1


def points_victoire(difficulte):
    if difficulte == "Facile":
        return 2
    elif difficulte == "Intermediaire":
        return 4
    else:
        return 8


def points_interruption(difficulte):
    if difficulte == "Facile":
        return -1
    elif difficulte == "Intermediaire":
        return -2
    else:
        return -3


def choisir_difficulte():
    print("Choisissez le niveau de difficulte :")
    print("  1 - Facile")
    print("  2 - Intermediaire")
    print("  3 - Difficile")
    choix = input("Votre choix : ")
    if choix == "1":
        return "Facile", "niveau_facile.txt"
    elif choix == "2":
        return "Intermediaire", "niveau_intermediaire.txt"
    else:
        return "Difficile", "niveau_difficile.txt"


def tour_joueur(grille, depart):
    # depart contient les cases fixes du debut (non modifiables)
    print("Commandes : un coup (ex: 5 B 7), C pour effacer, P pour pause, I pour interrompre")
    saisie = input("Votre coup : ").strip()

    if saisie.upper() == "P":
        return "pause"
    if saisie.upper() == "I":
        return "interruption"

    if saisie.upper().startswith("C"):
        morceaux = saisie.split()
        if len(morceaux) != 3:
            print("Format attendu : C ligne colonne (ex: C 5 B)")
            return "continue"
        ligne = int(morceaux[1]) - 1
        colonne = lettre_en_colonne(morceaux[2])
        if ligne < 0 or ligne > 8 or colonne < 0:
            print("Emplacement invalide.")
            return "continue"
        if depart[ligne][colonne] != 0:
            print("Cette case fait partie de la grille de depart, on ne peut pas l'effacer.")
            return "continue"
        if grille[ligne][colonne] == 0:
            print("La case est deja vide.")
        else:
            grille[ligne][colonne] = 0
            print("Case effacee.")
        return "continue"

    morceaux = saisie.split()
    if len(morceaux) != 3:
        print("Format attendu : ligne colonne valeur (ex: 5 B 7)")
        return "continue"

    ligne = int(morceaux[0]) - 1
    colonne = lettre_en_colonne(morceaux[1])
    valeur = int(morceaux[2])

    if ligne < 0 or ligne > 8 or colonne < 0 or valeur < 1 or valeur > 9:
        print("Saisie invalide.")
        return "continue"
    if depart[ligne][colonne] != 0:
        print("Cette case est fixe, vous ne pouvez pas la modifier.")
        return "continue"
    if placement_possible(grille, ligne, colonne, valeur):
        grille[ligne][colonne] = valeur
    else:
        print("Placement impossible : ce nombre est deja present sur la ligne, colonne ou carre.")
    return "continue"


def partie_humain(grille, depart, nom_joueur, difficulte, score):
    while True:
        afficher_grille(grille)
        print("Joueur :", nom_joueur, "| Niveau :", difficulte)
        resultat = tour_joueur(grille, depart)

        if resultat == "pause":
            sauvegarder_partie(grille, nom_joueur, difficulte, score)
            print("Aucun score n'est attribue pour une partie en pause.")
            return
        if resultat == "interruption":
            points = points_interruption(difficulte)
            total = enregistrer_score(nom_joueur, points)
            print("Partie interrompue. Score de la partie :", points)
            print("Score total :", total)
            return

        if grille_complete(grille):
            afficher_grille(grille)
            points = points_victoire(difficulte)
            total = enregistrer_score(nom_joueur, points)
            print("Bravo", nom_joueur, ", vous avez gagne !")
            print("Score de la partie :", points)
            print("Score total :", total)
            return


def nouvelle_partie():
    nom_joueur = input("Nom du joueur : ")
    print("Qui joue ?")
    print("  1 - Moi (joueur humain)")
    print("  2 - IA_Joueur")
    type_joueur = input("Votre choix : ")

    difficulte, fichier = choisir_difficulte()
    try:
        grille = charger_grille(fichier)
    except FileNotFoundError:
        print("Fichier de grille introuvable :", fichier)
        return
    depart = copier_grille(grille)

    if type_joueur == "2":
        jouer_ia(grille)
    else:
        partie_humain(grille, depart, nom_joueur, difficulte, 0)


def reprendre_partie():
    if not partie_existe():
        print("Aucune sauvegarde disponible.")
        return
    grille, nom_joueur, difficulte, score = charger_partie()
    depart = copier_grille(grille)
    print("Reprise de la partie de", nom_joueur)
    partie_humain(grille, depart, nom_joueur, difficulte, score)


def afficher_regles():
    print()
    print("Regles du Sudoku :")
    print("La grille fait 9x9 et contient 9 carres de 3x3.")
    print("Chaque ligne, chaque colonne et chaque carre doit contenir")
    print("les chiffres de 1 a 9 sans repetition.")
    print()


def afficher_credits():
    print()
    print("Projet Sudoku - M1 ILMSI ESIEE-IT 2025-2026")
    print("Realise par l'equipe.")
    print()


def menu():
    while True:
        print("===== SUDOKU =====")
        print("1 - Nouvelle partie")
        print("2 - Reprendre la partie sauvegardee")
        print("3 - Scores")
        print("4 - Regles")
        print("5 - Credits")
        print("6 - Quitter")
        choix = input("Votre choix : ")

        if choix == "1":
            nouvelle_partie()
        elif choix == "2":
            reprendre_partie()
        elif choix == "3":
            afficher_graphe()
        elif choix == "4":
            afficher_regles()
        elif choix == "5":
            afficher_credits()
        elif choix == "6":
            print("Au revoir !")
            break
        else:
            print("Choix invalide.")


if __name__ == "__main__":
    menu()
