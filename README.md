# Sudoku_Python

Vous réaliserez ce projet en équipe (les détails de la constitution des équipes tels que donnés sur BlackBoard), mais la note pourra être individualisée. Au sein d'une même équipe de projet, chaque étudiant devra s'investir à part égale dans la conception et le développement.

## Lancement

```
python3 main.py
```

## Structure du projet

- `main.py` : menu principal et boucle de jeu (mode console)
- `grille.py` : chargement, affichage et validation des règles du Sudoku
- `ia_joueur.py` : IA_Joueur, résolution automatique par backtracking
- `scores.py` : enregistrement des scores et graphe matplotlib
- `sauvegarde.py` : pause (P) et reprise de partie
- `niveau_facile.txt`, `niveau_intermediaire.txt`, `niveau_difficile.txt` : grilles de départ

## Commandes en partie

- `5 B 7` : place le 7 en ligne 5, colonne B
- `C 5 B` : efface la case ligne 5 colonne B
- `P` : pause (sauvegarde la partie, aucun score)
- `I` : interruption (score négatif)

## Scores

- Facile : +2 (gagné) / -1 (interrompu)
- Intermédiaire : +4 / -2
- Difficile : +8 / -3
