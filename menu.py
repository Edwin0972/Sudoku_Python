# Affichage des menus
import tkinter as tk
from tkinter import messagebox, simpledialog
import random
from Calcul_Score import calculer_score

# ── Variables globales ──
difficulte = ""
score_total = 0

# ── Grille Sudoku valide de référence ──
GRILLE_SOLUTION = [
    [5, 3, 4, 6, 7, 8, 9, 1, 2],
    [6, 7, 2, 1, 9, 5, 3, 4, 8],
    [1, 9, 8, 3, 4, 2, 5, 6, 7],
    [8, 5, 9, 7, 6, 1, 4, 2, 3],
    [4, 2, 6, 8, 5, 3, 7, 9, 1],
    [7, 1, 3, 9, 2, 4, 8, 5, 6],
    [9, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 6, 1, 7, 9],
]

def masquer_cases(niveau):
    if niveau == "Facile":
        nb_visibles = 40
    elif niveau == "Intermédiaire":
        nb_visibles = 35
    else:
        nb_visibles = 30
    grille = [ligne[:] for ligne in GRILLE_SOLUTION]
    positions = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(positions)
    for r, c in positions[nb_visibles:]:
        grille[r][c] = 0
    return grille

# Créer le menu du choix de difficulté
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

# Lancer la partie avec la grille
def lancer_partie(niveau, fenetre_niveaux):
    global difficulte, score_total
    difficulte = niveau
    fenetre_niveaux.destroy()

    nom = simpledialog.askstring("Nom du joueur", "Entrez votre prénom :", parent=app)
    nom_joueur = nom if nom else "Joueur"

    grille_joueur = masquer_cases(difficulte)

    fenetre_jeu = tk.Toplevel(app)
    fenetre_jeu.title(f"Sudoku — {difficulte}")
    fenetre_jeu.geometry("520x620")
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
                    val = grille_joueur[r][c]
                    if val != 0:
                        tk.Label(
                            cadre_boite, text=str(val),
                            width=2, height=1,
                            font=("Arial", 18, "bold"),
                            bg="#c8c8c8", fg="#000000", relief="flat"
                        ).grid(row=i, column=j, padx=1, pady=1)
                    else:
                        var = tk.StringVar()
                        tk.Entry(
                            cadre_boite, textvariable=var,
                            width=2, font=("Arial", 18),
                            justify="center", bg="white", fg="#222222", relief="flat"
                        ).grid(row=i, column=j, padx=1, pady=1)
                        cellules[r][c] = var

    # Boutons Vérifier / Abandonner
    def verifier():
        global score_total
        gains = {"Facile": 2, "Intermédiaire": 4, "Difficile": 8}
        for r in range(9):
            for c in range(9):
                if cellules[r][c] is not None:
                    saisie = cellules[r][c].get()
                    if not saisie.isdigit() or int(saisie) != GRILLE_SOLUTION[r][c]:
                        messagebox.showerror("Incorrect", "La grille est incorrecte ou incomplète !")
                        return
        score_total = calculer_score(score_total, difficulte, partieInterrompu=False)
        score_label.config(text=f"Score : {score_total}")
        messagebox.showinfo("Bravo !",
            f"Félicitations {nom_joueur}, tu as gagné !\n"
            f"Points gagnés : +{gains[difficulte]}\n"
            f"Score total : {score_total}")
        fenetre_jeu.destroy()

    def abandonner():
        global score_total
        pertes = {"Facile": 1, "Intermédiaire": 2, "Difficile": 3}
        score_total = calculer_score(score_total, difficulte, partieInterrompu=True)
        messagebox.showinfo("Partie abandonnée",
            f"Partie interrompue.\n"
            f"Points perdus : -{pertes[difficulte]}\n"
            f"Score total : {score_total}")
        fenetre_jeu.destroy()

    cadre_boutons = tk.Frame(fenetre_jeu, pady=12)
    cadre_boutons.pack()
    tk.Button(cadre_boutons, text="✔  Vérifier", font=("Arial", 12),
              command=verifier, bg="#4CAF50", fg="white", padx=12, pady=4).grid(row=0, column=0, padx=12)
    tk.Button(cadre_boutons, text="✖  Abandonner", font=("Arial", 12),
              command=abandonner, bg="#e53935", fg="white", padx=12, pady=4).grid(row=0, column=1, padx=12)

# Ouvrir le tableau des scores
def ouvrir_scores():
    fenetre_scores = tk.Toplevel(app)
    fenetre_scores.title("Tableau des scores")
    fenetre_scores.geometry("300x200")
    try:
        with open("score.txt", "r") as f:
            contenu = f.read()
        tk.Label(fenetre_scores, text=contenu, font=("Arial", 12)).pack(pady=20)
    except FileNotFoundError:
        tk.Label(fenetre_scores, text="Aucun score enregistré.", font=("Arial", 12)).pack(pady=20)

# Afficher les règles
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
        tk.Label(fenetre_regle, text=ligne, font=("Arial", 11), anchor="w").pack(fill="x", padx=15, pady=2)

# Crédits
def ouvrir_credits():
    fenetre_credits = tk.Toplevel(app)
    fenetre_credits.title("Crédits")
    fenetre_credits.geometry("300x150")
    tk.Label(fenetre_credits, text="Benjamin DIDRIT-VERDIET", font=("Arial", 12)).pack(pady=5)
    tk.Label(fenetre_credits, text="Edwin MOLINIER", font=("Arial", 12)).pack(pady=5)
    tk.Label(fenetre_credits, text="Titouan SABRAS", font=("Arial", 12)).pack(pady=5)

app = tk.Tk()
app.title("Sudoku")
app.geometry("640x480")

# Mettre l'image
try:
    image = tk.PhotoImage(file="sudoku.png")
    label_image = tk.Label(app, image=image)
    label_image.pack(pady=20)
except tk.TclError:
    tk.Label(app, text="SUDOKU", font=("Arial", 40, "bold")).pack(pady=30)

# Créer les boutons
tk.Button(app, text="Start",   command=ouvrir_niveaux).pack()
tk.Button(app, text="Scores",  command=ouvrir_scores).pack(pady=5)
tk.Button(app, text="Règles",  command=ouvrir_regles).pack(pady=5)
tk.Button(app, text="Crédits", command=ouvrir_credits).pack(pady=5)
tk.Button(app, text="Quitter", command=app.destroy).pack(pady=5)

app.mainloop()
