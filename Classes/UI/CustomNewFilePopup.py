"""
CustomNewFilePopup.py

une popup personnalisé lorsque l'utilisateur souhaite créer une nouvelle scène.
inclut un slider pour changer la taille des cubes, ainsi qu'un avertissement
que les données non sauvegardées seront perdues.
"""

from tkinter import IntVar, Scale
import Classes.Config as Config

class CustomNewFilePopup:

    canvas = None
    frame = None

    scale_var = None

    @classmethod
    def initialiser(cls, interface, ok_cmd):
        cls.canvas = interface.canvas
        cls.frame = interface.creer_frame()
        cls.frame.config(bg = "white")

        cls.frame_btn = interface.creer_frame(cls.frame)

        cls.frame_btn.config(bg = "white")

        cls.scale_var = IntVar()
        cls.scale_var.set(Config.cube_dim)

        cls.setup_popup(interface, ok_cmd)

    @classmethod
    def setup_popup(cls, interface, ok_cmd):
        cls.label = interface.creer_label(cls.frame, text = "Nouveau \n\nToutes les données\nnon enregistrées seront perdues.\n\nSouhaitez-vous continuer ?\n", 
                                                background = "white",
                                                borderwidth = 0,
                                                font = ("Courier New", 15),
                                                justify = 'center')

        cls.ok_btn = interface.creer_button(cls.frame_btn, text = "OK", 
                                                    background = "white", 
                                                    activebackground = "grey", 
                                                    borderwidth = 1,
                                                    command = lambda: ok_cmd(cls.scale_var.get()))

        cls.fermer_btn = interface.creer_button(cls.frame_btn, text = "Annuler",
                                                    background = "white", 
                                                    activebackground = "grey", 
                                                    borderwidth = 1,
                                                    command = lambda evt=None: cls.cacher(evt))

        cls.scale = Scale( cls.frame, from_= Config.min_cube_dim,
                                    to = Config.max_cube_dim,
                                    label = "Taille des Cubes",
                                    fg = "black",
                                    variable = cls.scale_var,
                                    sliderlength = 25,
                                    sliderrelief = 'flat',
                                    orient = "horizontal",
                                    font = ("Courier New",15),
                                    length = 200,
                                    bg = "white",
                                    troughcolor = "grey",
                                    borderwidth = 1,
                                    highlightthickness = 0)
    
    @classmethod
    def afficher(cls):
        cls.canvas.create_window(375, 220, window = cls.frame, tags="nouveau_fichier_popup")
        cls.frame.lift()
        cls.frame_btn.lift()
        cls.label.lift()
        cls.ok_btn.lift()
        cls.fermer_btn.lift()
        cls.frame_btn.pack(side = "bottom", anchor="s", pady = 10)
        cls.scale.pack(side="bottom", anchor="s", padx = 5, pady = 35)
        cls.label.pack(side="top", anchor="n", padx = 10, pady = 4)
        cls.fermer_btn.pack(side = "left", padx = 20)
        cls.ok_btn.pack(side = "left", padx = 20)
        

    @classmethod
    def cacher(cls, event = None):
        cls.canvas.delete("nouveau_fichier_popup")