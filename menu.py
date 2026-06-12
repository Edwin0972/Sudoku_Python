# menu.py - Interface graphique du Sudoku

import tkinter as tk
from tkinter import messagebox, simpledialog
import time

from Calcul_Score import calculer_score
from Generation import generer_grille, GRILLE_SOLUTION
from Chargement import charger_sauvegarde, charger_grille
from Sauvegarde import sauvegarder_partie, supprimer_sauvegarde

# Couleurs de l'interface
FOND         = "#f0f2f5"
BANDEAU      = "#000000"
BLANC        = "#ffffff"
CASE_FIXE    = "#dfe6e9"
VIOLET       = "#8e44ad"
VERT         = "#27ae60"
ROUGE        = "#c0392b"
BLEU         = "#2980b9"
TEXTE        = "#2d3436"
GRIS         = "#636e72"
OR           = "#fdcb6e"

# Variables globales
difficulte           = ""
score_total          = 0
frame_jeu            = None
frame_page           = None
cellules             = []
nom_joueur_courant   = ""
grille_orig_courante = []
score_label_jeu      = None
timer_label_jeu      = None
ia_label_jeu         = None
bouton_ia_jeu        = None
timer_actif          = False
debut_partie         = 0
ia_en_cours          = False

FICHIER_SCORES = "scores.txt"

# Gestion des scores dans le fichier
def enregistrer_score(nom, points):
    fichier = open(FICHIER_SCORES, "a")
    fichier.write(nom + "," + str(points) + "\n")
    fichier.close()

def lire_scores():
    scores = {}
    try:
        fichier = open(FICHIER_SCORES, "r")
        for ligne in fichier:
            ligne = ligne.strip()
            if ligne == "":
                continue
            parties = ligne.split(",")
            if len(parties) == 2:
                nom = parties[0]
                pts = int(parties[1])
                if nom in scores:
                    scores[nom] = scores[nom] + pts
                else:
                    scores[nom] = pts
        fichier.close()
    except FileNotFoundError:
        pass
    return scores

# Fenêtre principale
app = tk.Tk()
app.title("Sudoku")
app.geometry("900x680")
app.resizable(True, True)
app.configure(bg=FOND)

def basculer_plein_ecran(event=None):
    nouvel_etat = not app.attributes("-fullscreen")
    app.attributes("-fullscreen", nouvel_etat)

def quitter_plein_ecran(event=None):
    app.attributes("-fullscreen", False)

app.bind("<F11>", basculer_plein_ecran)
app.bind("<Escape>", quitter_plein_ecran)

# Utilitaire : créer un bouton avec un style cohérent

def creer_bouton(parent, texte, commande, couleur=BANDEAU):
    # On utilise tk.Label car sur macOS tk.Button ignore la couleur de fond
    bouton = tk.Label(
        parent,
        text=texte,
        bg=couleur,
        fg=BLANC,
        font=("Arial", 11, "bold"),
        padx=14,
        pady=7,
        relief="flat"
    )
    bouton.bind("<Button-1>", lambda event: commande())
    return bouton

# Navigation entre les pages

def cacher_toutes_les_frames():
    global frame_jeu, frame_page
    frame_accueil.pack_forget()
    if frame_jeu is not None:
        frame_jeu.pack_forget()
    if frame_page is not None:
        frame_page.pack_forget()

def montrer_accueil():
    cacher_toutes_les_frames()
    frame_accueil.pack(fill="both", expand=True)

def montrer_jeu():
    cacher_toutes_les_frames()
    frame_jeu.pack(fill="both", expand=True)

def montrer_page(frame):
    cacher_toutes_les_frames()
    frame.pack(fill="both", expand=True)


# Choix du niveau
def ouvrir_niveaux():
    fenetre = tk.Toplevel(app)
    fenetre.title("Niveau")
    fenetre.geometry("280x220")
    fenetre.configure(bg=FOND)
    fenetre.resizable(False, False)

    tk.Label(fenetre, text="Choisir un niveau",
             font=("Arial", 14, "bold"), bg=FOND, fg=TEXTE).pack(pady=(20, 12))

    def choisir_facile():
        lancer_partie("Facile", fenetre)

    def choisir_intermediaire():
        lancer_partie("Intermédiaire", fenetre)

    def choisir_difficile():
        lancer_partie("Difficile", fenetre)

    b1 = creer_bouton(fenetre, "Facile", choisir_facile)
    b1.config(width=16)
    b1.pack(pady=4)

    b2 = creer_bouton(fenetre, "Intermédiaire", choisir_intermediaire)
    b2.config(width=16)
    b2.pack(pady=4)

    b3 = creer_bouton(fenetre, "Difficile", choisir_difficile)
    b3.config(width=16)
    b3.pack(pady=4)

# Lancer une partie
def lancer_partie(niveau, fenetre_niveaux):
    global difficulte
    difficulte = niveau
    fenetre_niveaux.destroy()

    sauvegarde = charger_sauvegarde()
    if sauvegarde is not None and sauvegarde[0] == difficulte:
        reprendre = messagebox.askyesno(
            "Sauvegarde",
            "Partie " + difficulte + " sauvegardée pour " + sauvegarde[1] + ".\nReprendre ?"
        )
        if reprendre:
            afficher_grille(sauvegarde[1], sauvegarde[2], sauvegarde[3])
            return

    nom = simpledialog.askstring("Joueur", "Votre prénom :", parent=app)
    if nom is None or nom.strip() == "":
        nom_joueur = "Joueur"
    else:
        nom_joueur = nom.strip()

    grille_originale = charger_grille(difficulte)

    # Copier la grille originale pour la grille de jeu
    grille_actuelle = []
    for ligne in grille_originale:
        grille_actuelle.append(ligne[:])

    afficher_grille(nom_joueur, grille_actuelle, grille_originale)

# Lire la grille depuis les cases Entry
def get_grille_actuelle():
    grille = []
    for r in range(9):
        ligne = []
        for c in range(9):
            if cellules[r][c] is not None:
                valeur = cellules[r][c][0].get()
                if valeur.isdigit():
                    ligne.append(int(valeur))
                else:
                    ligne.append(0)
            else:
                ligne.append(grille_orig_courante[r][c])
        grille.append(ligne)
    return grille

# Remettre toutes les cases en blanc
def reinitialiser_couleurs():
    for r in range(9):
        for c in range(9):
            if cellules[r][c] is not None:
                cellules[r][c][1].config(bg=BLANC)

# Sauvegarder (touche P)
def sauvegarder_partie_joueur(event=None):
    grille = get_grille_actuelle()
    sauvegarder_partie(difficulte, nom_joueur_courant, grille, grille_orig_courante)
    messagebox.showinfo("Sauvegarde", "Partie sauvegardée !")

# Interrompre la partie (touche I)
def interrompre_partie(event=None):
    global score_total, timer_actif
    timer_actif = False

    if difficulte == "Facile":
        pts = -1
    elif difficulte == "Intermédiaire":
        pts = -2
    else:
        pts = -3

    score_total = calculer_score(score_total, difficulte, partieInterrompu=True)
    enregistrer_score(nom_joueur_courant, pts)
    supprimer_sauvegarde()
    messagebox.showinfo("Partie interrompue",
        "Partie abandonnée.\nPoints perdus : " + str(pts) +
        "\nScore total : " + str(score_total))
    montrer_accueil()

# Effacer la case sélectionnée (touche C)
def effacer_case(event=None):
    widget = app.focus_get()
    for r in range(9):
        for c in range(9):
            if cellules[r][c] is not None:
                if cellules[r][c][1] == widget:
                    cellules[r][c][0].set("")
                    return

# Vérifier la grille
def verifier_grille():
    global score_total, timer_actif

    if difficulte == "Facile":
        pts_victoire = 2
    elif difficulte == "Intermédiaire":
        pts_victoire = 4
    else:
        pts_victoire = 8

    grille = get_grille_actuelle()

    # Vérifier si la grille est complète
    for r in range(9):
        for c in range(9):
            if grille[r][c] == 0:
                messagebox.showinfo("Incomplet", "La grille n'est pas encore complète !")
                return

    # Vérifier les doublons dans une liste
    def a_des_doublons(valeurs):
        vus = []
        for v in valeurs:
            if v != 0:
                if v in vus:
                    return True
                vus.append(v)
        return False

    # Trouver les cases en erreur
    cases_erreur = []

    for i in range(9):
        # Vérifier la ligne i
        if a_des_doublons(grille[i]):
            for c in range(9):
                if (i, c) not in cases_erreur:
                    cases_erreur.append((i, c))

        # Vérifier la colonne i
        colonne = []
        for r in range(9):
            colonne.append(grille[r][i])
        if a_des_doublons(colonne):
            for r in range(9):
                if (r, i) not in cases_erreur:
                    cases_erreur.append((r, i))

        # Vérifier la boîte 3x3
        debut_r = (i // 3) * 3
        debut_c = (i % 3) * 3
        boite        = []
        coords_boite = []
        for dr in range(3):
            for dc in range(3):
                boite.append(grille[debut_r + dr][debut_c + dc])
                coords_boite.append((debut_r + dr, debut_c + dc))
        if a_des_doublons(boite):
            for r, c in coords_boite:
                if (r, c) not in cases_erreur:
                    cases_erreur.append((r, c))

    # Colorier les cases en erreur
    reinitialiser_couleurs()
    for r, c in cases_erreur:
        if cellules[r][c] is not None:
            cellules[r][c][1].config(bg="#fab1a0")

    if len(cases_erreur) > 0:
        messagebox.showerror("Erreurs", "La grille contient des erreurs (cases en rose).")
        return

    # Victoire : calculer le bonus temps
    timer_actif   = False
    temps_ecoule  = int(time.time() - debut_partie)

    if difficulte == "Facile":
        if temps_ecoule <= 120:
            bonus = 3
        elif temps_ecoule <= 300:
            bonus = 2
        elif temps_ecoule <= 600:
            bonus = 1
        else:
            bonus = 0
    elif difficulte == "Intermédiaire":
        if temps_ecoule <= 180:
            bonus = 3
        elif temps_ecoule <= 480:
            bonus = 2
        elif temps_ecoule <= 900:
            bonus = 1
        else:
            bonus = 0
    else:
        if temps_ecoule <= 300:
            bonus = 3
        elif temps_ecoule <= 720:
            bonus = 2
        elif temps_ecoule <= 1200:
            bonus = 1
        else:
            bonus = 0

    pts_total   = pts_victoire + bonus
    score_total = calculer_score(score_total, difficulte, partieInterrompu=False)
    if bonus > 0:
        score_total = score_total + bonus

    score_label_jeu.config(text="Score : " + str(score_total))
    enregistrer_score(nom_joueur_courant, pts_total)
    supprimer_sauvegarde()

    minutes  = temps_ecoule // 60
    secondes = temps_ecoule % 60
    message  = "Félicitations " + nom_joueur_courant + ", tu as gagné !\n"
    message += "Temps : " + str(minutes).zfill(2) + ":" + str(secondes).zfill(2) + "\n"
    message += "Points : +" + str(pts_victoire)
    if bonus > 0:
        message += "  +  Bonus temps : +" + str(bonus)
    message += "\nScore total : " + str(score_total)
    messagebox.showinfo("Bravo !", message)
    montrer_accueil()

# Chronomètre
def maj_timer():
    if not timer_actif:
        return
    temps_ecoule = int(time.time() - debut_partie)
    minutes  = temps_ecoule // 60
    secondes = temps_ecoule % 60
    timer_label_jeu.config(text=str(minutes).zfill(2) + ":" + str(secondes).zfill(2))
    app.after(1000, maj_timer)

# IA Joueur
def lancer_ia():
    global ia_en_cours
    if ia_en_cours:
        return

    # Trouver toutes les cases vides
    cases_vides = []
    for r in range(9):
        for c in range(9):
            if cellules[r][c] is not None:
                if cellules[r][c][0].get() == "":
                    cases_vides.append((r, c))

    if len(cases_vides) == 0:
        ia_label_jeu.config(text="La grille est déjà remplie !")
        return

    ia_en_cours = True

    # Placer les chiffres un par un avec un délai
    def jouer_case(index):
        global ia_en_cours
        if index >= len(cases_vides):
            ia_en_cours = False
            ia_label_jeu.config(text="IA a terminé ! Vérification...")
            app.after(600, verifier_grille)
            return
        r, c    = cases_vides[index]
        valeur  = GRILLE_SOLUTION[r][c]
        cellules[r][c][0].set(str(valeur))
        lettres = "ABCDEFGHI"
        ia_label_jeu.config(
            text="IA place " + str(valeur) +
                 "  ->  ligne " + str(r + 1) +
                 ", colonne " + lettres[c]
        )
        app.after(400, lambda: jouer_case(index + 1))

    jouer_case(0)

# Validation de saisie (1 à 9 uniquement)
def valider_saisie(valeur):
    if valeur == "":
        return True
    if valeur.isdigit() and valeur != "0" and len(valeur) == 1:
        return True
    return False

# Afficher la grille de jeu dans la fenêtre principale
def afficher_grille(nom_joueur, grille_actuelle, grille_originale):
    global score_total, frame_jeu, cellules
    global nom_joueur_courant, grille_orig_courante
    global score_label_jeu, timer_label_jeu, ia_label_jeu, bouton_ia_jeu
    global timer_actif, debut_partie

    # Supprimer l'ancienne frame si elle existe
    if frame_jeu is not None:
        frame_jeu.destroy()
    frame_jeu = tk.Frame(app, bg=FOND)

    # Mémoriser les données de la partie
    nom_joueur_courant   = nom_joueur
    grille_orig_courante = grille_originale
    debut_partie         = time.time()
    timer_actif          = True

    # Enregistrer la fonction de validation
    vcmd = (app.register(valider_saisie), "%P")

    # Bandeau du haut
    bandeau = tk.Frame(frame_jeu, bg=BANDEAU, pady=10)
    bandeau.pack(fill="x")
    tk.Label(bandeau, text="Joueur : " + nom_joueur,
             font=("Arial", 12), bg=BANDEAU, fg=BLANC).pack(side="left", padx=20)
    tk.Label(bandeau, text="Niveau : " + difficulte,
             font=("Arial", 12), bg=BANDEAU, fg=BLANC).pack(side="left", padx=10)
    score_label_jeu = tk.Label(bandeau, text="Score : " + str(score_total),
                               font=("Arial", 12, "bold"), bg=BANDEAU, fg=OR)
    score_label_jeu.pack(side="right", padx=20)
    timer_label_jeu = tk.Label(bandeau, text="00:00",
                               font=("Arial", 12), bg=BANDEAU, fg="#b2bec3")
    timer_label_jeu.pack(side="right", padx=20)

    # Grille 9x9
    cadre_grille = tk.Frame(frame_jeu, bg=BANDEAU, padx=4, pady=4)
    cadre_grille.pack(pady=12)

    # Initialiser le tableau de cellules
    cellules = []
    for r in range(9):
        ligne_cellules = []
        for c in range(9):
            ligne_cellules.append(None)
        cellules.append(ligne_cellules)

    # Construire les 9 boîtes 3x3
    for boite_row in range(3):
        for boite_col in range(3):
            cadre_boite = tk.Frame(cadre_grille, bg=BANDEAU, padx=2, pady=2)
            cadre_boite.grid(row=boite_row, column=boite_col, padx=3, pady=3)
            for i in range(3):
                for j in range(3):
                    r = boite_row * 3 + i
                    c = boite_col * 3 + j
                    val_originale = grille_originale[r][c]
                    val_actuelle  = grille_actuelle[r][c]
                    if val_originale != 0:
                        # Case pré-remplie
                        label = tk.Label(
                            cadre_boite,
                            text=str(val_originale),
                            width=2, height=1,
                            font=("Arial", 20, "bold"),
                            bg=CASE_FIXE, fg=TEXTE, relief="flat"
                        )
                        label.grid(row=i, column=j, padx=1, pady=1)
                    else:
                        # Case vide et modifiable
                        var = tk.StringVar()
                        if val_actuelle != 0:
                            var.set(str(val_actuelle))
                        entry = tk.Entry(
                            cadre_boite,
                            textvariable=var,
                            width=2,
                            font=("Arial", 20),
                            justify="center",
                            bg=BLANC,
                            fg=VIOLET,
                            relief="flat",
                            insertbackground=VIOLET,
                            validate="key",
                            validatecommand=vcmd
                        )
                        entry.grid(row=i, column=j, padx=1, pady=1)
                        cellules[r][c] = (var, entry)

    # Label pour les messages de l'IA
    ia_label_jeu = tk.Label(frame_jeu, text="",
                            font=("Arial", 10, "italic"), bg=FOND, fg=GRIS)
    ia_label_jeu.pack()

    # Boutons du gameplay
    cadre_boutons = tk.Frame(frame_jeu, bg=FOND, pady=10)
    cadre_boutons.pack()

    b_verif = creer_bouton(cadre_boutons, "Vérifier",
                           verifier_grille, couleur=BANDEAU)
    b_verif.grid(row=0, column=0, padx=6)

    b_aband = creer_bouton(cadre_boutons, "Abandonner (I)",
                           interrompre_partie, couleur=ROUGE)
    b_aband.grid(row=0, column=1, padx=6)

    b_sauv = creer_bouton(cadre_boutons, "Sauvegarder (P)",
                          sauvegarder_partie_joueur, couleur=BANDEAU)
    b_sauv.grid(row=0, column=2, padx=6)

    bouton_ia_jeu = creer_bouton(cadre_boutons, "Lancer IA",
                                 lancer_ia, couleur=BANDEAU)
    bouton_ia_jeu.grid(row=0, column=3, padx=6)

    # Raccourcis clavier
    app.bind("<p>", sauvegarder_partie_joueur)
    app.bind("<P>", sauvegarder_partie_joueur)
    app.bind("<i>", interrompre_partie)
    app.bind("<I>", interrompre_partie)
    app.bind("<c>", effacer_case)
    app.bind("<C>", effacer_case)

    # Démarrer le chronomètre
    maj_timer()

    montrer_jeu()


# Page Scores
def ouvrir_scores():
    global frame_page
    if frame_page is not None:
        frame_page.destroy()
    frame_page = tk.Frame(app, bg=FOND)

    scores = lire_scores()

    # Bandeau
    bandeau = tk.Frame(frame_page, bg=BANDEAU, pady=12)
    bandeau.pack(fill="x")
    tk.Label(bandeau, text="Tableau des scores",
             font=("Arial", 15, "bold"), bg=BANDEAU, fg=BLANC).pack()

    if len(scores) == 0:
        tk.Label(frame_page, text="Aucun score enregistré.",
                 font=("Arial", 13), bg=FOND, fg=GRIS).pack(expand=True)
    else:
        # Trier les joueurs du meilleur au moins bon
        liste_triee = []
        for nom in scores:
            liste_triee.append((scores[nom], nom))
        liste_triee.sort(reverse=True)

        noms_tries = []
        for score_val, nom in liste_triee:
            noms_tries.append(nom)

        meilleur = noms_tries[0]
        tk.Label(bandeau,
                 text="Meilleur : " + meilleur + "  ·  " + str(scores[meilleur]) + " pts",
                 font=("Arial", 11), bg=BANDEAU, fg=OR).pack()

        # En-tête du tableau
        entete = tk.Frame(frame_page, bg="#dfe6e9", pady=5)
        entete.pack(fill="x", padx=24, pady=(10, 0))
        tk.Label(entete, text="#",      width=4,  font=("Arial", 10, "bold"),
                 bg="#dfe6e9", fg=GRIS).pack(side="left", padx=6)
        tk.Label(entete, text="Joueur", width=18, font=("Arial", 10, "bold"),
                 bg="#dfe6e9", fg=GRIS, anchor="w").pack(side="left")
        tk.Label(entete, text="Score",  width=8,  font=("Arial", 10, "bold"),
                 bg="#dfe6e9", fg=GRIS, anchor="e").pack(side="right", padx=12)

        # Zone liste avec scroll
        MAX_VISIBLE  = 5
        wrap         = tk.Frame(frame_page, bg=FOND)
        wrap.pack(fill="both", expand=True, padx=24, pady=4)
        scrollbar    = tk.Scrollbar(wrap, orient="vertical")
        canvas_liste = tk.Canvas(wrap, bg=FOND, highlightthickness=0,
                                 yscrollcommand=scrollbar.set)
        scrollbar.config(command=canvas_liste.yview)
        frame_liste  = tk.Frame(canvas_liste, bg=FOND)

        id_fenetre = canvas_liste.create_window((0, 0), window=frame_liste, anchor="nw")

        def on_redim_frame(event):
            canvas_liste.configure(scrollregion=canvas_liste.bbox("all"))

        def on_redim_canvas(event):
            canvas_liste.itemconfig(id_fenetre, width=event.width)

        frame_liste.bind("<Configure>", on_redim_frame)
        canvas_liste.bind("<Configure>", on_redim_canvas)

        if len(noms_tries) > MAX_VISIBLE:
            scrollbar.pack(side="right", fill="y")
        canvas_liste.pack(side="left", fill="both", expand=True)

        def scroll_souris(event):
            canvas_liste.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas_liste.bind("<MouseWheel>", scroll_souris)

        # Lignes du tableau
        for idx in range(len(noms_tries)):
            nom = noms_tries[idx]
            val = scores[nom]
            if idx == 0:
                bg_ligne = "#fffde7"
            else:
                bg_ligne = BLANC
            ligne = tk.Frame(frame_liste, bg=bg_ligne, pady=7, padx=6,
                             highlightbackground="#dfe6e9", highlightthickness=1)
            ligne.pack(fill="x", pady=2, padx=2)
            rang = "  " + str(idx + 1)
            tk.Label(ligne, text=rang, width=4, font=("Arial", 12),
                     bg=bg_ligne, fg=TEXTE).pack(side="left", padx=4)
            tk.Label(ligne, text=nom, width=18, font=("Arial", 12),
                     bg=bg_ligne, fg=TEXTE, anchor="w").pack(side="left")
            if idx == 0:
                couleur_pts = VERT
            else:
                couleur_pts = TEXTE
            tk.Label(ligne, text=str(val) + " pts", width=9,
                     font=("Arial", 12, "bold"), bg=bg_ligne,
                     fg=couleur_pts, anchor="e").pack(side="right", padx=10)

        # Graphique matplotlib
        try:
            import matplotlib.pyplot as plt
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

            noms_graph    = noms_tries
            valeurs_graph = []
            couleurs_barres = []
            for n in noms_graph:
                valeurs_graph.append(scores[n])
                if n == meilleur:
                    couleurs_barres.append("#fdcb6e")
                else:
                    couleurs_barres.append("#74b9ff")

            fig, ax = plt.subplots(figsize=(6, 2.2))
            fig.patch.set_facecolor(FOND)
            ax.set_facecolor(BLANC)
            barres = ax.bar(noms_graph, valeurs_graph, color=couleurs_barres,
                            edgecolor="#b2bec3", linewidth=0.8)
            ax.set_title("Classement", fontsize=11, color=TEXTE)
            ax.tick_params(colors=GRIS, labelsize=9)
            for spine in ax.spines.values():
                spine.set_edgecolor("#dfe6e9")
            for i in range(len(barres)):
                barre = barres[i]
                val   = valeurs_graph[i]
                x     = barre.get_x() + barre.get_width() / 2
                ax.text(x, barre.get_height() + 0.05, str(val),
                        ha="center", va="bottom", fontsize=9, color=TEXTE)
            fig.tight_layout(pad=0.8)

            canvas_graph = FigureCanvasTkAgg(fig, master=frame_page)
            canvas_graph.draw()
            canvas_graph.get_tk_widget().pack(fill="x", padx=24, pady=4)
        except ImportError:
            pass

    b_retour = creer_bouton(frame_page, "<- Retour", montrer_accueil)
    b_retour.pack(pady=10, side="bottom")

    montrer_page(frame_page)

# Page Règles

def ouvrir_regles():
    global frame_page
    if frame_page is not None:
        frame_page.destroy()
    frame_page = tk.Frame(app, bg=FOND)

    bandeau = tk.Frame(frame_page, bg=BANDEAU, pady=12)
    bandeau.pack(fill="x")
    tk.Label(bandeau, text="Règles du Sudoku",
             font=("Arial", 15, "bold"), bg=BANDEAU, fg=BLANC).pack()

    cadre = tk.Frame(frame_page, bg=FOND, padx=40, pady=20)
    cadre.pack(expand=True, fill="both")

    regles = [
        "Grille 9x9 divisee en 9 carres de 3x3.",
        "Remplir chaque case avec un chiffre de 1 a 9.",
        "Chaque chiffre apparait une seule fois par ligne,",
        "colonne et carre 3x3.",
        "",
        "Touches :",
        "P  ->  Pause (partie sauvegardee)",
        "I  ->  Interrompre (score negatif, non sauvegarde)",
        "C  ->  Effacer la case selectionnee",
        "",
        "Scores  :  Facile +2 / Intermediaire +4 / Difficile +8",
        "Abandon :  Facile -1 / Intermediaire -2 / Difficile -3",
        "",
        "Bonus temps :",
        "Facile : moins de 2 min : +3 / moins de 5 min : +2  /  moins de 10 min : +1",
        "Intermediair : moins de 3 min : +3  / moins de 8 min : +2  /  moins de 15 min : +1",
        "Difficile : moins de 5 min : +3  /  moins de 12 min : +2  /  moins de 20 min : +1",
        "",
        "IA_Joueur :",
        "Remplit automatiquement les cases vides une par une.",
        "Affiche chaque placement (ligne + colonne) en temps reel.",
        "Lance la verification automatiquement a la fin.",
    ]

    for ligne in regles:
        if ligne == "":
            tk.Label(cadre, text="", bg=FOND).pack(fill="x")
        else:
            tk.Label(cadre, text=ligne, font=("Arial", 12),
                     bg=FOND, fg=TEXTE, anchor="w").pack(fill="x", pady=1)

    tk.Frame(frame_page, bg=FOND).pack(expand=True)
    b_retour = creer_bouton(frame_page, "<- Retour", montrer_accueil)
    b_retour.pack(pady=10, side="bottom")

    montrer_page(frame_page)

# Page Crédits
def ouvrir_credits():
    global frame_page
    if frame_page is not None:
        frame_page.destroy()
    frame_page = tk.Frame(app, bg=FOND)

    bandeau = tk.Frame(frame_page, bg=BANDEAU, pady=12)
    bandeau.pack(fill="x")
    tk.Label(bandeau, text="Equipe",
             font=("Arial", 15, "bold"), bg=BANDEAU, fg=BLANC).pack()

    cadre = tk.Frame(frame_page, bg=FOND)
    cadre.pack(expand=True)

    membres = ["Benjamin DIDRIT-VERDIET", "Edwin MOLINIER", "Titouan SABRAS"]
    for membre in membres:
        tk.Label(cadre, text=membre, font=("Arial", 13),
                 bg=FOND, fg=TEXTE).pack(pady=10)

    tk.Frame(frame_page, bg=FOND).pack(expand=True)
    b_retour = creer_bouton(frame_page, "<- Retour", montrer_accueil)
    b_retour.pack(pady=10, side="bottom")

    montrer_page(frame_page)

# Frame Accueil (créée après les fonctions)
frame_accueil = tk.Frame(app, bg=FOND)
frame_accueil.pack(fill="both", expand=True)

centre_accueil = tk.Frame(frame_accueil, bg=FOND)
centre_accueil.place(relx=0.5, rely=0.5, anchor="center")

try:
    image_brut  = tk.PhotoImage(file="sudoku.png")
    image       = image_brut.subsample(2, 2)
    label_image = tk.Label(centre_accueil, image=image, bg=FOND)
    label_image.image = image
    label_image.pack(pady=(0, 20))
except tk.TclError:
    tk.Label(centre_accueil, text="SUDOKU", font=("Arial", 48, "bold"),
             bg=FOND, fg=BANDEAU).pack(pady=(0, 20))

bouton_jouer   = creer_bouton(centre_accueil, "Jouer",   ouvrir_niveaux)
bouton_scores  = creer_bouton(centre_accueil, "Scores",  ouvrir_scores)
bouton_regles  = creer_bouton(centre_accueil, "Règles",  ouvrir_regles)
bouton_credits = creer_bouton(centre_accueil, "Crédits", ouvrir_credits)
bouton_quitter = creer_bouton(centre_accueil, "Quitter", app.destroy)

for btn in [bouton_jouer, bouton_scores, bouton_regles, bouton_credits, bouton_quitter]:
    btn.config(width=18)
    btn.pack(pady=4)

# Lancement de l'application
app.mainloop()
