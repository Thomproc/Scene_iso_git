"""
StartUpMenu.py

Il s'agit de tout ce qui concerne le menu de démarrage de l'application,
avec les 3 boutons Nouveau, Charger et Quitter
ainsi que le slider pour changer la taille de cube, et l'aperçu au dessus
un menu principale en soit
"""

from tkinter import Scale, IntVar
from PIL import Image, ImageTk

import Classes.Config as Config

from Classes.CubeIso.Cube import Cube

class StartUpMenu:
    def __init__(self, interface, new_scene_fct, load_scene_fct, quit_app_fct):
        self.interface = interface
        self.canvas = interface.creer_canvas()
        self.canvas.create_rectangle(315, 0, 750, 450, fill=Config.col_app_background_darker, width=0)

        self.scale_var = IntVar()
        self.scale_var.set(Config.cube_dim)

        self.demo_taille_cube = Cube(self.canvas, 550, 150, (1, 1, 1))
        self.demo_taille_cube.afficher()

        self.new_scene_fct = new_scene_fct
        self.load_scene_fct = load_scene_fct
        self.quit_app_fct = quit_app_fct
        
        self.get_all_img()
        self.generate_all_img()
        self.btn_bind()
        self.generate_scale()
        self.afficher()

    def load_startup_img(self, fileName):
        img = Image.open("./Images/StartUpMenu/" + fileName)
        imgTk = ImageTk.PhotoImage(img)
        return imgTk

    def get_all_img(self):
        self.new_btn = [ self.load_startup_img("Nouveau.png"), self.load_startup_img("Nouveau_Selected.png") ]
        self.load_btn = [ self.load_startup_img("Charger.png"), self.load_startup_img("Charger_Selected.png") ]
        self.quit_btn = [ self.load_startup_img("Quitter.png"), self.load_startup_img("Quitter_Selected.png") ]

        self.ok_btn = [ self.load_startup_img("ok_button.png"), self.load_startup_img("ok_button_selected.png") ]
        self.arrow = self.load_startup_img("arrow.png")

    def generate_all_img(self):
        self.canvas.create_image(40, 150, image = self.new_btn[1],
                                anchor = 'w',
                                tags = ("start_button", "new"))
        self.canvas.create_image(40, 250, image = self.load_btn[0], 
                                activeimage = self.load_btn[1], 
                                anchor = 'w',
                                tags = ("start_button", "load"))
        self.canvas.create_image(40, 350, image = self.quit_btn[0], 
                                activeimage = self.quit_btn[1], 
                                anchor = 'w',
                                tags = ("start_button", "quit"))

        self.canvas.create_image(315, 150, image = self.arrow, anchor = 'w')

        self.canvas.create_image(725, 425, image = self.ok_btn[0], 
                                activeimage = self.ok_btn[1],
                                anchor = 'se',
                                tags = ("start_button", "ok"))

    def generate_scale(self):
        self.scale = Scale(self.canvas, from_= Config.min_cube_dim,
                                    to = Config.max_cube_dim,
                                    label = "Taille des Cubes",
                                    fg = "white",
                                    variable = self.scale_var,
                                    sliderlength = 25,
                                    sliderrelief = 'flat',
                                    orient = "horizontal",
                                    font = ("Courier New",15),
                                    length = 325,
                                    bg = Config.col_app_background_darker,
                                    troughcolor = Config.col_app_background,
                                    borderwidth = 0,
                                    highlightthickness = 0,
                                    command = self.taille_cube_scale_update)

    def start_menu_button_clic(self, event = None):
        current = self.canvas.gettags("current")
        if current[1] == "ok":
            self.new_scene_fct()
        elif current[1] == "load":
            self.load_scene_fct()
        elif current[1] == "quit":
            self.quit_app_fct()

    def taille_cube_scale_update(self, event=None):
        scale_int = self.scale_var.get()
        if Config.cube_dim == scale_int: return
        Config.cube_dim = scale_int
        self.canvas.delete("x1, y1, z1")
        self.demo_taille_cube.afficher()

    def btn_bind(self):
        self.canvas.tag_bind("start_button", "<ButtonRelease-1>", self.start_menu_button_clic)

    def afficher(self):
        self.canvas.pack(expand=True, fill='both')
        self.scale.pack(side = 'bottom', anchor = "se", padx = 25, pady = 125)
    
    def hide(self):
        self.canvas.pack_forget()