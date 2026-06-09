# Affichage des menus
import tkinter as tk
app = tk.Tk()
app.geometry("640x480")
# Créer le menu du choix de difficulté
def ouvrir_niveaux():
    fenetre_niveaux = tk.Toplevel(app)
    fenetre_niveaux.title("Choix du niveau")
    fenetre_niveaux.geometry("300x200")
    tk.Button(fenetre_niveaux, text="Facile").pack(pady=5)
    tk.Button(fenetre_niveaux, text="Intermédiaire").pack(pady=5)
    tk.Button(fenetre_niveaux, text="Difficile").pack(pady=5)
#Ouvrir le tableau des scores
def ouvrir_scores():
    fenetre_scores=tk.Toplevel(app)
    fenetre_scores.title("Tableau des scores")
    fenetre_scores.gemoetry("300x200")
    open("score.txt")
#Afficher les règles
def ouvrir_regles():
    fenetre_regle=tk.Toplevel(app)
    fenetre_regle.title("Règles")
    fenetre_regle.geometry("300x200")
    tk.Label("Le jeu du sudoku se joue sur une grille 9x9")
    tk.Label("Le but du jeu est de remplir la grille avec des chiffres de 1 à 9")
    tk.Label("Un chiffre ne peut apparaître qu'une seule fois sur chaque ligne, chaque colonne et chaque carré 3x3")
    tk.Label("Vous pouvez mettre la partie à tout moment en appuyant sur 'P', dans ce cas votre partie est sauvegardée")
    tk.Label("Vous pouvez abandonner la partie à tout moment en appuyant sur 'I', dans ce cas votre partie n'est pas sauvegardée.")
    tk.Label("Vous pouvez choisir votre niveau de difficulté : facile, intermédiaire, difficile")
    tk.Label("Une partie gagnée en facile vous rapporte 2 points, 4 points en intermédiaire, 8 points en difficile")
    tk.Label("Une partie interrompue en facile vous fait perdre 1 point, 2 points en intermédiaire et 3 points en difficile")
#Credits
def ouvrir_credits():
    fenetre_credits=tk.Toplevel(app)
    fenetre_credits.title("Credits")
    fenetre_credits.gemetry("300x200")
    tk.Label("Benjamin DIDRIT-VERDIET")
    tk.Label("Edwin MOLINIER")
    tk.Label("Titouan SABRAS")
app.title("Sudoku")
app.geometry("640x480")
# Mettre l’image
image = tk.PhotoImage(file="sudoku.png")
label_image = tk.Label(app, image=image)
label_image.pack(pady=20)
# Créer les boutons
tk.Button(app, text="Start", command=ouvrir_niveaux).pack()
tk.Button(app, text="Scores", command=ouvrir_scores).pack(pady=5)
tk.Button(app, text="Règles", command=ouvrir_regles).pack(pady=5)
tk.Button(app, text="Crédits", command=ouvrir_credits).pack(pady=5)
tk.Button(app, text="Quitter", command=app.destroy).pack(pady=5)
app.mainloop()
