"""
Mouse_Indicator.py

Gère l'affichage de la petite souris en haut à gauche de l'écran
aidant à mieux comprendre les actions du clic gauche et droit en fonction du Mode actuel.
(Peut être désactiver par le Menu Options si l'utilisateur le souhaite)
"""

from PIL import Image, ImageTk

import Classes.Config as Config

from Classes.Evenement.EvenementManager import Observateur

class MouseIndicator:

    canvas = None
    label = None
    
    mouseImgTk = None
    mouseClickImg = []

    isVisible = True

    @classmethod
    def initialiser(cls, interface):
        cls.canvas = interface.canvas
        cls.label = interface.creer_label(None, background=Config.col_app_background,
                                                fg = "white")

        interface.bind("<Button-1>", cls.left_click_start)
        interface.bind("<ButtonRelease-1>", cls.left_click_end)
        interface.bind("<Button-3>", cls.right_click_start)
        interface.bind("<ButtonRelease-3>", cls.right_click_end)

        Observateur.observe(Config.evt_mode_update, cls.update_label)
        Observateur.observe(Config.evt_didacticiel_update, cls.didact_update)

        cls.get_all_mouse_img()
        cls.update_label(0)        

    @classmethod
    def get_all_mouse_img(cls):
        path = "./Images/Mouse_Indicator/"
        mouse_img = Image.open(path + "mouse_icon.png")
        mouse_resize = mouse_img.resize((50, 65))
        mouseImgTk = ImageTk.PhotoImage(mouse_resize)
        cls.mouseImgTk = mouseImgTk

        left_btn_img = Image.open(path + "left_click_icon.png")
        right_btn_img = Image.open(path + "right_click_icon.png")

        left_resize = left_btn_img.resize((12, 12))
        right_resize = right_btn_img.resize((12, 12))

        left_imgTk = ImageTk.PhotoImage(left_resize)
        right_imgTk = ImageTk.PhotoImage(right_resize)

        cls.mouseClickImg = [left_imgTk, right_imgTk]
        pass

    @classmethod
    def afficher(cls):
        cls.canvas.create_window(10, 10, window = cls.label,
                                        anchor = 'nw',
                                        tags = "mouse_indicator_window")
        cls.canvas.create_image(87, 37, image = cls.mouseImgTk,
                                        anchor = 'nw',
                                        tags = "mouse_indicator_window")
    
    @classmethod
    def didact_update(cls, value):
        if value:
            cls.label.lower()
        else:
            cls.label.lift()
    
    @classmethod
    def hide(cls):
        cls.canvas.delete("mouse_indicator_window")

    @classmethod
    def toggle_mouse_indicator(cls, value):
        if value:
            cls.afficher()
        else:
            cls.hide()
        cls.isVisible = value

    @classmethod
    def left_click_start(cls, event=None):
        if cls.isVisible == False: return
        cls.canvas.create_image(93, 43, image = cls.mouseClickImg[0],
                                        anchor = 'nw', 
                                        tags = 'mouse_indicator_left')
    @classmethod
    def left_click_end(cls, event=None):
        if cls.isVisible == False: return
        cls.canvas.delete('mouse_indicator_left')

    @classmethod
    def right_click_start(cls, event=None):
        if cls.isVisible == False: return
        cls.canvas.create_image(119, 43, image = cls.mouseClickImg[1],
                                        anchor = 'nw',
                                        tags = 'mouse_indicator_right')
    @classmethod
    def right_click_end(cls, event=None):
        if cls.isVisible == False: return
        cls.canvas.delete('mouse_indicator_right')

    @classmethod
    def update_label(cls, mode_index):
        if mode_index == 0:
            #creation
            cls.label.config(text = "Créer des Cubes    |     Supprimer des Cubes")
            pass
        elif mode_index == 1:
            #couleur
            cls.label.config(text = "Colore une face    |     Supprime la Couleur")
            pass
        elif mode_index == 2:
            #texture
            cls.label.config(text = "Ajoute une texture |     Supprimer la Texture")
            pass
