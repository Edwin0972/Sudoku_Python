#  Gestion de la sauvegarde
from Tkinter import *
root=Tk()
# Permettre de sauvegarder si on appuye sur « P »
root.bind("<P>", Sauvegarde)
# Sauvegarder
def Sauvegarde():
    with open("save.txt", "w") as fichier:
        fichier.write("contenu de la partie")
        