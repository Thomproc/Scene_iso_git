"""
Mode.py

Cette classe gere les differents mode d'utilisation de l'application
notamment en changeant le comportement du clic gauche et droit de la souris
selon le mode courant de l'application.

Les différentes interactions possibles sont :

    -------------------------------------------------------------------------------------
    |   Mode Actuel     |   Clic Gauche             |   Clic Droit                      |
    |                   |                           |                                   |
    |-------------------|---------------------------|-----------------------------------|
    |   Création        |   Création d'un Cube      |   Suppression d'un Cube           |
    |-------------------|---------------------------|-----------------------------------|
    |   Couleur         |   Colore une face         |   Retire la couleur d'une face    |
    |-------------------|---------------------------|-----------------------------------|
    |   Texture         |   Applique une texture    |   Retire une texture              |
    -------------------------------------------------------------------------------------
"""

from enum import IntEnum
import Classes.Config as Config
from Classes.CubeIso.CubeManager import CubeManager

from Classes.Modes.Mode_Couleur import ModeCouleur
from Classes.Modes.Mode_Texture import ModeTexture

from Classes.Evenement.EvenementManager import Evenement

class ModeEnum(IntEnum):
    CREATION = 0
    COULEUR = 1
    TEXTURE = 2

class Mode:

    mode_courant = ModeEnum.CREATION

    @classmethod
    def clic_gauche(cls, event = None):

        if cls.mode_courant == ModeEnum.CREATION:
            CubeManager.creer_cube()
        elif cls.mode_courant == ModeEnum.COULEUR:
            CubeManager.changer_couleur_face(ModeCouleur.current_couleur_selected)
        elif cls.mode_courant == ModeEnum.TEXTURE:
            CubeManager.changer_texture_cube(ModeTexture.current_texture_selected)

    @classmethod
    def clic_droit(cls, event = None):

        if cls.mode_courant == ModeEnum.CREATION:
            CubeManager.detruire_cube()
        elif cls.mode_courant == ModeEnum.COULEUR:
            CubeManager.changer_couleur_face() #aucune couleur en argument, supprime la couleur de la face, et la remet à la couleur d'origine
        elif cls.mode_courant == ModeEnum.TEXTURE:
            CubeManager.changer_texture_cube()

    @classmethod
    def update_interface(cls):
        if cls.mode_courant == ModeEnum.COULEUR:
            ModeCouleur.afficher_color_picker()
        else:
            ModeCouleur.destroy_color_picker()

        if cls.mode_courant == ModeEnum.TEXTURE:
            ModeTexture.afficher_texture_selector()
        else:
            ModeTexture.destroy_texture_selector()

    @classmethod
    def set_mode_courant(cls, index):
        cls.mode_courant = ModeEnum(index)
        Evenement(Config.evt_mode_update, index)
        Mode.update_interface()