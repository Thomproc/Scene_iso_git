"""
Mode_Texture.py

Ce fichier gère le fonctionnement du mode texture, c'est-à-dire 
la manière dont on propose à l'utilisateur de choisir une texture à appliquer aux cubes.
Ainsi que l'interface dédié au mode texture.
"""


import glob
from PIL import Image, ImageTk
import Classes.Config as Config

class ModeTexture:
    canvas = None
    frame = None

    current_texture_selected = None

    texture_l = []
    texture_icon_l = []
    texture_btn_l = []

    @classmethod
    def initialiser(cls, interface):
        cls.frame = interface.creer_frame()
        cls.canvas = interface.canvas

        #get all textures images
        cls.get_all_textures()
        cls.generate_texture_btns(interface)        

        cls.set_current_texture(0)
        cls.texture_btn_l[0].config(borderwidth = 5)

    @classmethod
    def get_all_textures(cls):
        taille_bouton = (Config.ui_taille_bouton_texture, Config.ui_taille_bouton_texture)

        i = 0
        for filePath in glob.glob('./Images/Toolbar_Textures/*.png'):
            icon = Image.open(filePath)
            resized_icon = icon.resize(taille_bouton)
            imgTk = ImageTk.PhotoImage(resized_icon)
            cls.texture_l.append(imgTk)
            cls.texture_icon_l.append(icon)
            i += 1

    @classmethod
    def generate_texture_btns(cls, interface):
        for i in range(len(cls.texture_l)):
            btn = interface.creer_button(cls.frame, image= cls.texture_l[i], 
                            background=Config.col_app_background, 
                            activebackground=Config.col_case_active, 
                            borderwidth=0,
                            command= lambda evt=None, index=i: cls.texture_btn_click(index, evt))
            cls.texture_btn_l.append(btn)

    @classmethod
    def texture_btn_click(cls, btn_index, event=None):
        cls.set_current_texture(btn_index)

        for i in range(len(cls.texture_btn_l)):
            btn = cls.texture_btn_l[i]
            if i == btn_index:
                btn.config(borderwidth=5)
            else:
                btn.config(borderwidth=0)

    @classmethod
    def afficher_texture_selector(cls):
        cls.frame.pack(fill='x', side='bottom', padx=15, pady=10)

        for btn in cls.texture_btn_l:
            btn.pack(padx = 5, side = "left")

    @classmethod
    def destroy_texture_selector(cls):
        if cls.frame == None: return

        for btn in cls.texture_btn_l:
            btn.pack_forget()
        cls.frame.pack_forget()

    @classmethod
    def get_texture_from_index(cls, texture_index):
        icon = cls.texture_icon_l[texture_index]
        new_size = Config.cube_dim * 3
        new_size_X = (new_size - Config.cube_dim // 2) - 5
        new_size_Y = new_size - Config.cube_dim + 2
        resized_icon = icon.resize((new_size_X, new_size_Y))
        imgTk = ImageTk.PhotoImage(resized_icon)
        return [imgTk, texture_index]

    @classmethod
    def set_current_texture(cls, new_texture_index):
        cls.current_texture_selected = cls.get_texture_from_index(new_texture_index)