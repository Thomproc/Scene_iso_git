"""
Toolbar.py

Gere la barre d'outil sur le cote droit de l'ecran
et permet de creer les boutons utilisant la classe CustomButton
en leur attribuant leur differentes images respectives.

S'occupe aussi des evenements des boutons, pour changer de mode d'utilisation dans Mode.py
"""

import glob
import Classes.Config as Config
from PIL import Image, ImageTk
from Classes.UI.CustomButtons import CustomButton

from Classes.Utilitaires.ToolTip import ToolTip

from Classes.Modes.Mode import Mode

from Classes.Evenement.EvenementManager import Observateur

class Toolbar:
    def __init__(self, interface, frame):
        self.interface = interface
        self.frame = frame

        self.taille_bouton = (Config.ui_taille_bouton_outil, Config.ui_taille_bouton_outil)

        self.btns_tooltip = {   0: "Créer ou Supprimer des Cubes",
                                1: "Changer la couleur d'un Cube",
                                2: "Ajouter ou Supprimer une Texture sur un Cube" }

        self.get_all_buttons_images()
        self.generate_buttons()
        self._buttons_l[0].isSelected = True

        Observateur.observe(Config.evt_nombre_cube_update, self.update_toolbar)
        self.update_toolbar(0)

    def get_all_buttons_images(self):
        self.images_l = {}
        files = []
        i = 0
        for filePath in glob.glob('./Images/Toolbar_Buttons_Icon/*.png'):
            files.append(filePath)
        
        files = sorted(files) #on tri pour obtenir le bonne ordre des fichiers, glob ne prend pas les fichiers dans le bon ordre comme voulu
        for file in files:
            icon = Image.open(file)
            resized_icon = icon.resize(self.taille_bouton)
            imgTk = ImageTk.PhotoImage(resized_icon)

            if "_selected_" not in file:
                self.images_l[i % 3] = [imgTk]
            else:
                self.images_l[i % 3].append(imgTk)
            i += 1

        rotate_icon_file = Image.open("./Images/rotation_arrow.png")
        rotate_arrow_resized = rotate_icon_file.resize(self.taille_bouton)
        self.rotate_imgTk = ImageTk.PhotoImage(rotate_arrow_resized)

    def generate_buttons(self):
        self._buttons_l = []
        for key in self.images_l.keys():
            b = CustomButton(self.frame, int(key), self.images_l[key], self.btns_tooltip[key], self.button_event_click)
            self._buttons_l.append(b)

        self.rotate_button = self.interface.creer_button(self.frame, 
                                                        borderwidth = 0,
                                                        background = Config.col_app_background,
                                                        activebackground = Config.col_case_active,
                                                        image = self.rotate_imgTk,
                                                        command = self.rotate_scene)
        rot_tooltip = ToolTip(self.frame)
        self.rotate_button.bind("<Enter>", lambda evt: self.tooltip_rotate_button(rot_tooltip, evt))
        self.rotate_button.bind("<ButtonPress>", rot_tooltip.leave)
        self.rotate_button.bind("<Leave>", rot_tooltip.leave)
        
    def tooltip_rotate_button(self, tooltip, event=None):
        tooltip.set_text("Rotation de la Scène")
        tooltip.enter(event)

    def rotate_scene(self, event=None):
        self.interface.rotate_scene(event)

    def button_event_click(self, index, event=None):
        if self._buttons_l[index]["state"] == "disabled": return

        for i in range(len(self._buttons_l)):
            if i == index:
                self._buttons_l[i].isSelected = True
            else:
                self._buttons_l[i].isSelected = False
        Mode.set_mode_courant(index)

    def update_toolbar(self, nbrCube):
        if nbrCube == 0:
            self._buttons_l[0].isSelected = True
            self._buttons_l[1]["state"] = "disabled"
            self._buttons_l[1].isSelected = False
            self._buttons_l[2]["state"] = "disabled"
            self._buttons_l[2].isSelected = False
            Mode.set_mode_courant(0)
        else:
            self._buttons_l[1]["state"] = "normal"
            self._buttons_l[2]["state"] = "normal"

    def afficher(self):
        self.frame.pack(fill='y', side='right', padx=15, pady=5)

        for i in range(len(self._buttons_l)):
            self._buttons_l[i].grid(row=i, column=0, pady=4)
        self.rotate_button.grid(row = len(self._buttons_l), column=0, pady=4)

    def __getitem__(self, index):
        return self._buttons_l[index]
    def __setitem__(self, index, value):
        self._buttons_l[index] = value