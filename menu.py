# Affichage des menus
import tkinter as tk
from tkinter import messagebox, simpledialog
from Calcul_Score import calculer_score
from Generation import generer_grille, resoudre_grille
from Chargement import charger_sauvegarde, charger_grille
from Sauvegarde import sauvegarder_partie, supprimer_sauvegarde
from scores import enregistrer_score, lire_scores, meilleur_score

# ── Variables globales ──
difficulte = ""
score_total = 0

# ── Créer le menu du choix de difficulté ──
def ouvrir_niveaux():
    fenetre_niveaux = tk.Toplevel(app)
    fenetre_niveaux.title("Choix du niveau")
    fenetre_niveaux.geometry("300x200")
    tk.Button(fenetre_niveaux, text="Facile",
              command=lambda: lancer_partie("Facile", fenetre_niveaux)).pack(pady=5)
    tk.Button(fenetre_niveaux, text="Intermédiaire",
              command=lambda: lancer_partie("Intermédiaire", fenetre_niveaux)).pack(pady=5)
    tk.Button(fenetre_niveaux, text="Difficile",
              command=lambda: lancer_partie("Difficile", fenetre_niveaux)).pack(pady=5)

# ── Lancer la partie avec la grille ──
def lancer_partie(niveau, fenetre_niveaux):
    global difficulte, score_total
    difficulte = niveau
    fenetre_niveaux.destroy()

    # Vérifier si une sauvegarde existe pour ce niveau
    sauvegarde = charger_sauvegarde()
    if sauvegarde and sauvegarde[0] == difficulte:
        reprendre = messagebox.askyesno(
            "Sauvegarde trouvée",
            f"Une partie en {difficulte} a été sauvegardée pour {sauvegarde[1]}.\nReprendre ?"
        )
        if reprendre:
            _, nom_joueur, grille_actuelle, grille_originale = sauvegarde
            afficher_grille(nom_joueur, grille_actuelle, grille_originale)
            return

    # Nouvelle partie
    nom = simpledialog.askstring("Nom du joueur", "Entrez votre prénom :", parent=app)
    nom_joueur = nom if nom else "Joueur"
    grille_originale = charger_grille(difficulte)
    grille_actuelle  = [ligne[:] for ligne in grille_originale]
    afficher_grille(nom_joueur, grille_actuelle, grille_originale)

# ── Afficher la fenêtre de jeu ──
def afficher_grille(nom_joueur, grille_actuelle, grille_originale):
    global score_total

    fenetre_jeu = tk.Toplevel(app)
    fenetre_jeu.title(f"Sudoku — {difficulte}")
    fenetre_jeu.geometry("520x650")
    fenetre_jeu.resizable(False, False)

    # En-tête
    cadre_info = tk.Frame(fenetre_jeu, pady=10)
    cadre_info.pack()
    tk.Label(cadre_info, text=f"Joueur : {nom_joueur}", font=("Arial", 12)).grid(row=0, column=0, padx=15)
    tk.Label(cadre_info, text=f"Niveau : {difficulte}", font=("Arial", 12)).grid(row=0, column=1, padx=15)
    score_label = tk.Label(cadre_info, text=f"Score : {score_total}", font=("Arial", 12, "bold"))
    score_label.grid(row=0, column=2, padx=15)

    # Grille 9x9
    cadre_grille = tk.Frame(fenetre_jeu, bg="black", padx=3, pady=3)
    cadre_grille.pack(pady=5)

    cellules = [[None] * 9 for _ in range(9)]

    for boite_row in range(3):
        for boite_col in range(3):
            cadre_boite = tk.Frame(cadre_grille, bg="black", padx=1, pady=1)
            cadre_boite.grid(row=boite_row, column=boite_col, padx=2, pady=2)
            for i in range(3):
                for j in range(3):
                    r = boite_row * 3 + i
                    c = boite_col * 3 + j
                    val_origine = grille_originale[r][c]
                    val_actuelle = grille_actuelle[r][c]

                    if val_origine != 0:
                        # Case pré-remplie (non modifiable)
                        tk.Label(
                            cadre_boite, text=str(val_origine),
                            width=2, height=1,
                            font=("Arial", 18, "bold"),
                            bg="#c8c8c8", fg="#000000", relief="flat"
                        ).grid(row=i, column=j, padx=1, pady=1)
                    else:
                        # Case vide (saisissable), pré-remplie si reprise de sauvegarde
                        var = tk.StringVar()
                        if val_actuelle != 0:
                            var.set(str(val_actuelle))
                        tk.Entry(
                            cadre_boite, textvariable=var,
                            width=2, font=("Arial", 18),
                            justify="center", bg="white", fg="#222222", relief="flat"
                        ).grid(row=i, column=j, padx=1, pady=1)
                        cellules[r][c] = var

    # ── Helpers ──
    # Solution calculee a partir de la grille de depart (sert a verifier ET a l'IA)
    solution = [ligne[:] for ligne in grille_originale]
    resoudre_grille(solution)

    def get_grille_actuelle():
        """Retourne la grille 9x9 avec les saisies du joueur."""
        grille = []
        for r in range(9):
            ligne = []
            for c in range(9):
                if cellules[r][c] is not None:
                    val = cellules[r][c].get()
                    ligne.append(int(val) if val.isdigit() else 0)
                else:
                    ligne.append(grille_originale[r][c])
            grille.append(ligne)
        return grille

    # ── Sauvegarde sur touche P ──
    def sauvegarder(event=None):
        sauvegarder_partie(difficulte, nom_joueur, get_grille_actuelle(), grille_originale)
        messagebox.showinfo("Sauvegarde", "Partie sauvegardée !\nAppuyez sur OK pour continuer.")

    # ── Interruption sur touche I ──
    def interrompre(event=None):
        global score_total
        pertes = {"Facile": 1, "Intermédiaire": 2, "Difficile": 3}
        score_total = calculer_score(score_total, difficulte, partieInterrompu=True)
        enregistrer_score(nom_joueur, -pertes[difficulte])
        supprimer_sauvegarde()
        messagebox.showinfo("Partie interrompue",
            f"Partie abandonnée (non sauvegardée).\n"
            f"Points perdus : -{pertes[difficulte]}\n"
            f"Score total : {score_total}")
        fenetre_jeu.destroy()

    fenetre_jeu.bind("<p>", sauvegarder)
    fenetre_jeu.bind("<P>", sauvegarder)
    fenetre_jeu.bind("<i>", interrompre)
    fenetre_jeu.bind("<I>", interrompre)

    # ── IA_Joueur : remplit la grille case par case (animation) ──
    def jouer_ia():
        # Liste des cases a remplir (celles vides au depart)
        a_remplir = []
        for r in range(9):
            for c in range(9):
                if cellules[r][c] is not None:
                    a_remplir.append((r, c))
                    cellules[r][c].set("")  # repartir d'une case vide
        # Desactiver les boutons pendant que l'IA joue
        bouton_ia.config(state="disabled")
        bouton_verif.config(state="disabled")

        def remplir(index):
            if index < len(a_remplir):
                r, c = a_remplir[index]
                cellules[r][c].set(str(solution[r][c]))
                fenetre_jeu.after(80, lambda: remplir(index + 1))
            else:
                # Fin : on attribue le score comme une victoire, puis retour au menu
                global score_total
                gains = {"Facile": 2, "Intermédiaire": 4, "Difficile": 8}
                score_total = calculer_score(score_total, difficulte, partieInterrompu=False)
                enregistrer_score(nom_joueur + " (IA)", gains[difficulte])
                supprimer_sauvegarde()
                messagebox.showinfo("IA_Joueur",
                    f"IA_Joueur a terminé la grille !\n"
                    f"Points : +{gains[difficulte]}")
                fenetre_jeu.destroy()

        remplir(0)

    # ── Boutons ──
    def verifier():
        global score_total
        gains = {"Facile": 2, "Intermédiaire": 4, "Difficile": 8}
        for r in range(9):
            for c in range(9):
                if cellules[r][c] is not None:
                    saisie = cellules[r][c].get()
                    if not saisie.isdigit() or int(saisie) != solution[r][c]:
                        messagebox.showerror("Incorrect", "La grille est incorrecte ou incomplète !")
                        return
        score_total = calculer_score(score_total, difficulte, partieInterrompu=False)
        enregistrer_score(nom_joueur, gains[difficulte])
        score_label.config(text=f"Score : {score_total}")
        supprimer_sauvegarde()
        messagebox.showinfo("Bravo !",
            f"Félicitations {nom_joueur}, tu as gagné !\n"
            f"Points gagnés : +{gains[difficulte]}\n"
            f"Score total : {score_total}")
        fenetre_jeu.destroy()

    def abandonner():
        interrompre()

    cadre_boutons = tk.Frame(fenetre_jeu, pady=12)
    cadre_boutons.pack()
    tk.Button(cadre_boutons, text="💾  Sauvegarder (P)", font=("Arial", 11),
              command=sauvegarder, bg="#2196F3", fg="white", padx=10, pady=4).grid(row=0, column=0, padx=6)
    bouton_verif = tk.Button(cadre_boutons, text="✔  Vérifier", font=("Arial", 11),
              command=verifier, bg="#4CAF50", fg="white", padx=10, pady=4)
    bouton_verif.grid(row=0, column=1, padx=6)
    bouton_ia = tk.Button(cadre_boutons, text="🤖  IA_Joueur", font=("Arial", 11),
              command=jouer_ia, bg="#9C27B0", fg="white", padx=10, pady=4)
    bouton_ia.grid(row=0, column=2, padx=6)
    tk.Button(cadre_boutons, text="✖  Abandonner (I)", font=("Arial", 11),
              command=abandonner, bg="#e53935", fg="white", padx=10, pady=4).grid(row=0, column=3, padx=6)

    tk.Label(fenetre_jeu, text="P = Sauvegarder  |  I = Interrompre",
             font=("Arial", 9), fg="gray").pack()

# ── Ouvrir le tableau des scores ──
def ouvrir_scores():
    fenetre_scores = tk.Toplevel(app)
    fenetre_scores.title("Tableau des scores")
    fenetre_scores.geometry("360x420")

    scores = lire_scores()

    if len(scores) == 0:
        tk.Label(fenetre_scores, text="Aucun score enregistré.",
                 font=("Arial", 13)).pack(pady=30)
        return

    # Meilleur score
    nom_best, points_best = meilleur_score(scores)
    tk.Label(fenetre_scores,
             text=f"🏆 Meilleur score : {nom_best} ({points_best})",
             font=("Arial", 13, "bold"), fg="#9C27B0").pack(pady=12)

    # Tableau (classement decroissant)
    cadre = tk.Frame(fenetre_scores)
    cadre.pack(pady=5)
    tk.Label(cadre, text="Joueur", font=("Arial", 11, "bold"),
             width=18, anchor="w").grid(row=0, column=0, padx=5)
    tk.Label(cadre, text="Score", font=("Arial", 11, "bold"),
             width=6).grid(row=0, column=1, padx=5)
    classement = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    for i, (n, p) in enumerate(classement):
        tk.Label(cadre, text=n, font=("Arial", 11),
                 width=18, anchor="w").grid(row=i + 1, column=0, padx=5, pady=1)
        tk.Label(cadre, text=str(p), font=("Arial", 11),
                 width=6).grid(row=i + 1, column=1, padx=5, pady=1)

    # Bouton graphe matplotlib
    def afficher_graphe():
        try:
            import matplotlib.pyplot as plt
            noms = list(scores.keys())
            valeurs = list(scores.values())
            plt.figure("Scores des joueurs")
            plt.bar(noms, valeurs, color="#9C27B0")
            plt.title("Scores des joueurs")
            plt.xlabel("Joueurs")
            plt.ylabel("Score")
            plt.tight_layout()
            plt.show()
        except ImportError:
            messagebox.showinfo("Graphe",
                "matplotlib n'est pas installé.\nFaire : pip install matplotlib")

    tk.Button(fenetre_scores, text="📊  Voir le graphique",
              font=("Arial", 11), bg="#9C27B0", fg="white",
              padx=10, pady=4, command=afficher_graphe).pack(pady=16)

# ── Afficher les règles ──
def ouvrir_regles():
    fenetre_regle = tk.Toplevel(app)
    fenetre_regle.title("Règles")
    fenetre_regle.geometry("420x280")
    regles = [
        "Le jeu du sudoku se joue sur une grille 9x9.",
        "Le but est de remplir la grille avec des chiffres de 1 à 9.",
        "Un chiffre ne peut apparaître qu'une seule fois par ligne,",
        "colonne et carré 3x3.",
        "Appuyez sur 'P' pour mettre en pause (partie sauvegardée).",
        "Appuyez sur 'I' pour interrompre (partie non sauvegardée).",
        "Facile : +2 pts | Intermédiaire : +4 pts | Difficile : +8 pts",
        "Interruption : -1 / -2 / -3 pts selon le niveau.",
    ]
    for ligne in regles:
        tk.Label(fenetre_regle, text=ligne, font=("Arial", 15), anchor="center").pack(fill="x", padx=15, pady=2)

# ── Crédits ──
def ouvrir_credits():
    fenetre_credits = tk.Toplevel(app)
    fenetre_credits.title("Crédits")
    fenetre_credits.geometry("300x150")
    tk.Label(fenetre_credits, text="Benjamin DIDRIT-VERDIET", font=("Arial", 15),justify="center").pack(pady=5)
    tk.Label(fenetre_credits, text="Edwin MOLINIER",          font=("Arial", 15),justify="center").pack(pady=5)
    tk.Label(fenetre_credits, text="Titouan SABRAS",          font=("Arial", 15),justify="center").pack(pady=5)

# ── Fenêtre principale ──
app = tk.Tk()
app.title("Sudoku")
app.geometry("640x480")

try:
    image = tk.PhotoImage(file="sudoku.png")
    label_image = tk.Label(app, image=image)
    label_image.pack(pady=20)
except tk.TclError:
    tk.Label(app, text="SUDOKU", font=("Arial", 40, "bold")).pack(pady=30)

tk.Button(app, text="Start",   command=ouvrir_niveaux).pack()
tk.Button(app, text="Scores",  command=ouvrir_scores).pack(pady=5)
tk.Button(app, text="Règles",  command=ouvrir_regles).pack(pady=5)
tk.Button(app, text="Crédits", command=ouvrir_credits).pack(pady=5)
tk.Button(app, text="Quitter", command=app.destroy).pack(pady=5)

app.mainloop()
