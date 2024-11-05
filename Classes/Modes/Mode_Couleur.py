"""
Mode_Couleur.py

Ce fichier gere le fonctionnement du mode couleur, c'est a dire 
la manière dont on propose à l'utilisateur de choisir une couleur avec laquelle colorier
les faces des cubes.
Ainsi que l'interface dédié au mode couleur, dont les 3 presets de couleur mis à disposition
"""


from tkinter import colorchooser

import Classes.Config as Config

class ModeCouleur:
    canvas = None
    couleurs_panneau = ["white", "grey", "black"]
    color_picker_l = []
    current_couleur_selected = None

    @classmethod
    def initialiser(cls, canvas):
        cls.canvas = canvas

    #Permet d'ouvrir un sélecteur de couleurs et choisir une couleur à attribuer sur un des presets.
    @classmethod
    def color_picker_double_click(cls, event = None):
        current = cls.canvas.gettags("current")
        currentIndex = int(current[1])
        currentId = int(current[2])
        new_couleur_hex = colorchooser.askcolor(title= "Choisir une couleur")[1]
        if new_couleur_hex == None: return

        cls.set_current_couleur(new_couleur_hex)
        cls.couleurs_panneau[currentIndex] = new_couleur_hex

        cls.canvas.itemconfigure(currentId, tags=("color-picker", currentIndex, currentId), fill=new_couleur_hex)

    #Sélectionne une couleur avec laquelle l'utilisateur va colorier les faces des cubes à partir du preset sélectionner.
    @classmethod
    def color_picker_click(cls, event = None):
        current = cls.canvas.gettags("current")
        currentIndex = int(current[1])
        currentId = int(current[2])
        cls.set_current_couleur(cls.couleurs_panneau[currentIndex])

        for picker in cls.color_picker_l:
            if picker == currentId:
                cls.canvas.itemconfigure(picker, width = 5)
            else:
                cls.canvas.itemconfigure(picker, width = 1)

    #Affiche les boutons grâce auxquels on peut choisir une couleur.
    @classmethod
    def afficher_color_picker(cls):
        taille_carre = Config.ui_taille_bouton_couleur
        espace_entre_carre = 10
        nombre_carre = 3

        screen_w, screen_h = Config.app_minResolution
        screen_w -= ((taille_carre + espace_entre_carre) * nombre_carre) + 100
        screen_h -= taille_carre * 2

        row = 0
        for i in range(nombre_carre):
            btn = cls.canvas.create_rectangle(screen_w + row, screen_h, screen_w + row + taille_carre, screen_h + taille_carre, 
                                                fill = cls.couleurs_panneau[i],
                                                outline = "black",
                                                activewidth = 3,
                                                activeoutlinestipple='gray75')
            idBtn = btn
            index = i
            cls.canvas.itemconfigure(btn, tags = ("color-picker", index, idBtn))
            row += taille_carre + espace_entre_carre
            cls.color_picker_l.append(btn)

        #bind clic gauche et double clic gauche sur les color pickers
        cls.canvas.tag_bind("color-picker", "<Double-1>", cls.color_picker_double_click)
        cls.canvas.tag_bind("color-picker", "<Button-1>", cls.color_picker_click)
        
        #selectionne la premire couleur par defaut
        cls.current_couleur_selected = cls.couleurs_panneau[0]
        cls.canvas.itemconfigure(cls.color_picker_l[0], width = 5)

    #Destruction des boutons permettant de choisir une couleur.
    @classmethod
    def destroy_color_picker(cls):
        if cls.canvas == None: return
        cls.canvas.delete("color-picker")
        cls.color_picker_l = []
        cls.current_couleur_selected = None

    @classmethod
    def set_current_couleur(cls, new_couleur):
        cls.current_couleur_selected = new_couleur