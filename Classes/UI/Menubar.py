"""
Menubar.py

Permet de créer et gérer la menu barre en haut de l'écran.
Celle-ci contient les onglets :
    - Fichier : Nouveau / Ouvrir / Enregistrer sous... / Quitter
    - Options : Raccourcis / Activer ou Désactiver l'indicateur de souris
    - Aide : Didacticiel
"""

from os import stat
import sys
import tkinter as tk
import Classes.Config as Config

from Classes.Evenement.EvenementManager import Observateur

from Classes.CubeIso.CubeManager import CubeManager
from Classes.Grille.GrilleIso import GrilleIso
from Classes.UI.Aide_Didacticiel import AideDidacticiel
from Classes.UI.CustomNewFilePopup import CustomNewFilePopup
from Classes.UI.MenuRaccourci import MenuRaccourci
from Classes.UI.Mouse_Indicator import MouseIndicator

if(sys.version_info >= (3,)):
    from tkinter import messagebox
    from tkinter import filedialog
else:
    import tkMessageBox as messagebox
    import tkFileDialog as filedialog

class Menubar:
    interface = None

    def __init__(self, interface):
        Menubar.interface = interface
        self.menubar = tk.Menu(interface.root)

        self.fichier = tk.Menu(self.menubar, tearoff = 0)
        self.option = tk.Menu(self.menubar, tearoff = 0)
        self.aide = tk.Menu(self.menubar, tearoff = 0)

        self.menubar_set_fichier(self.fichier)
        self.menubar_set_options(self.option)
        self.menubar_set_aide(self.aide)

        self.menubar.add_cascade(label = "Fichier", menu = self.fichier)
        self.menubar.add_cascade(label = "Options", menu = self.option)
        self.menubar.add_cascade(label = "Aide", menu = self.aide)

        CustomNewFilePopup.initialiser(interface, self.start_new_scene)

        Observateur.observe(Config.evt_nombre_cube_update, self.update_menubar)
        self.update_menubar(0)

    def menubar_set_fichier(self, fichier):
        fichier.add_command(label = "Nouveau", command = self.nouveau)
        fichier.add_command(label = "Ouvrir", command = self.ouvrir)
        fichier.add_command(label = "Enregistrer sous...", command = self.enregistrer, state = "disabled")
        fichier.add_command(label = "Quitter", command = self.quitter)

        Menubar.interface.bind('<Control-n>', Menubar.nouveau)
        Menubar.interface.bind('<Control-N>', Menubar.nouveau)
        Menubar.interface.bind('<Control-o>', Menubar.ouvrir)
        Menubar.interface.bind('<Control-O>', Menubar.ouvrir)
        Menubar.interface.bind('<Escape>', Menubar.quitter)

    def menubar_set_options(self, options):
        options.add_command(label = "Raccourcis", command = MenuRaccourci.afficher)

        self.toggle_mouse_indicator = tk.BooleanVar()
        self.toggle_mouse_indicator.set(True)

        options.add_checkbutton(label = "Activer / Désactiver Indicateur Souris", 
                                onvalue = True, 
                                offvalue = False, 
                                variable = self.toggle_mouse_indicator,
                                command = lambda: MouseIndicator.toggle_mouse_indicator(self.toggle_mouse_indicator.get()))

    def menubar_set_aide(self, aide):
        aide.add_command(label = "Didacticiel", command = lambda: AideDidacticiel.didacticiel_afficher_checkbox(True))

    def afficher(self):
        Menubar.interface.root.config(menu = self.menubar)

    """
    Permet de rendre accessible ou non la fonction "enregistrer sous..." selon si un cube est présent sur la scène.
    (pas besoin d'enregistrer une scène vide).
    """
    def update_menubar(self, nbrCube):
        if nbrCube == 0:
            self.fichier.entryconfig(2, state = "disabled")
            Menubar.interface.unbind('<Control-s>')
            Menubar.interface.unbind('<Control-S>')
        else:
            self.fichier.entryconfig(2, state = "normal")
            Menubar.interface.bind('<Control-s>', Menubar.enregistrer)
            Menubar.interface.bind('<Control-S>', Menubar.enregistrer)

    @staticmethod
    def nouveau(evt = None):
        CustomNewFilePopup.afficher()
    
    @staticmethod
    def start_new_scene(newCubeSize, evt = None):
        CubeManager.effacer_scene()
        Menubar.interface.rotate_scene(destination = 0)

        if Config.cube_dim != newCubeSize:
            Config.cube_dim = newCubeSize
            GrilleIso.resize_grille()
        
        CustomNewFilePopup.cacher()

    @staticmethod
    def ouvrir(evt = None, succeed_fct = None):
        path = filedialog.askopenfilename(initialdir = "./Saves/", 
                                            title = "Ouvrir", 
                                            filetypes = (("Fichier texte","*.txt"), ))
        if path == '': return False
        if succeed_fct != None:
            succeed_fct()

        fichier = open(path, 'r')
        dico_scene = eval(fichier.read())

        CubeManager.effacer_scene()
        Menubar.interface.rotate_scene(destination = 0)
        CubeManager.charger_scene(dico_scene)
        fichier.close()

        return True

    """
    L'enregistrement d'une scène se fait par l'écriture d'un dictionnaire dans un fichier texte
    que l'on va ensuite récupérer et exploiter grâce à la fonction "eval()" de python.
    """
    @staticmethod
    def enregistrer(evt = None):
        path = filedialog.asksaveasfilename(initialdir = "./Saves/", 
                                            title = "Enregistrer", 
                                            filetypes = (("Fichier texte","*.txt"), ),
                                            defaultextension = ".txt")

        if (path):
            rotation_index = Config.app_rotation_index
            Menubar.interface.rotate_scene(destination = 0)
            fichier = open(path, 'w')
            dico_opt = {}
            dico_cubes = CubeManager.dico_cubes
            fichier.write('{')
            
            cube_dim_txt = '\'cube_dim\': ' + str(Config.cube_dim) + ', '
            rotation_index_txt = '\'rotation_index\': ' + str(rotation_index) + ', '
            fichier.write(cube_dim_txt)
            fichier.write(rotation_index_txt)
            for key in dico_cubes:
                cube = dico_cubes.get(key)

                #on enregistre la texture du cube
                if(cube.hasTexture):
                    textureIndex = str(cube.textureIndex)
                else:
                    textureIndex = None
                dico_opt["textureIndex"] = textureIndex

                #on enregistre la couleur des faces du cube
                couleur_face = str(cube.couleur_face)
                dico_opt["couleur_face"] = couleur_face

                text = '\'' + str(key) + '\': ' + str(dico_opt) + ', '
                fichier.write(text)
            fichier.write('}')
            fichier.close()
            Menubar.interface.rotate_scene(destination = rotation_index)
        return

    @staticmethod
    def quitter(evt = None):
        reponse = messagebox.askyesno(title = 'Quitter', 
                                        message = 'Voulez-vous quitter ?')
        if(reponse):
            exit(1)