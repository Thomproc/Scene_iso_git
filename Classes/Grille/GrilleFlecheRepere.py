"""
GrilleFlecheRepere.py \n

cette classe est instancier par la grille isometrique, \n
creer et affiche simplement les fleches indiquant l'origine du repere isometrique \n
ainsi que son orientation. \n
a chaque rotation de la scene les fleces vont se reafficher oriente a la nouvelle origine.
"""

from tkinter import ROUND, LAST
import Classes.Config as Config

from Classes.Evenement.EvenementManager import Observateur

class GrilleFlecheRepere:
    def __init__(self, canvas, grille, x, y):
        self.canvas = canvas
        self.grille = grille
        self.fleches = [None, None, None]
        self.position = [x, y, 1]
        self.origin = self.grille.get_origin_from_grille(0)
        self.rotationIndex = Config.app_rotation_index
        self.redessiner_fleche()
        Observateur.observe(Config.evt_rotation, lambda data: self.rotation_fleche(data))
    
    def rotation_fleche(self, rotation_index):
        tuplePos = tuple(self.position)
        posRotated = self.grille.get_position_rotated(tuplePos)
        origin_rotated = self.grille.get_origin_from_pos(posRotated)
        self.position = [posRotated[0], posRotated[1], posRotated[2]]
        self.origin = origin_rotated
        self.rotationIndex = rotation_index
        self.redessiner_fleche()
        return

    def redessiner_fleche(self):
        dim = Config.cube_dim
        arrow_size = dim * 2
        
        arrow_x, arrow_y = self.origin

        if self.rotationIndex == 0:
            arrow_y -= 4
        elif self.rotationIndex == 1:
            arrow_x += dim
            arrow_y += (dim / 2) - 4
        elif self.rotationIndex == 2:
            arrow_y += dim + 4
        elif self.rotationIndex == 3:
            arrow_x -= dim
            arrow_y += (dim / 2) - 4
        
        arrow_args = { "fill": Config.col_grille_bord, "width":3, "dash":(5, 2), "arrow":LAST, "capstyle":ROUND}

        for fleche in self.fleches:
            if fleche == None:
                continue
            self.canvas.delete(fleche)

        self.fleches[0] = self.canvas.create_line(arrow_x, arrow_y, arrow_x, arrow_y-arrow_size, arrow_args, tags=(Config.tag_grille, Config.tag_grille_fleche)) #Y arrow

        if self.rotationIndex == 0: #haut vers le bas
            self.fleches[1] = self.canvas.create_line(arrow_x, arrow_y, arrow_x+arrow_size, arrow_y+arrow_size/2, arrow_args, tags=(Config.tag_grille, Config.tag_grille_fleche)) #X Arrow
            self.fleches[2] = self.canvas.create_line(arrow_x, arrow_y, arrow_x-arrow_size, arrow_y+arrow_size/2, arrow_args, tags=(Config.tag_grille, Config.tag_grille_fleche)) #Z Arrow
        elif self.rotationIndex == 1: #droite vers gauche
            self.fleches[1] = self.canvas.create_line(arrow_x, arrow_y, arrow_x-arrow_size, arrow_y+arrow_size/2, arrow_args, tags=(Config.tag_grille, Config.tag_grille_fleche)) #X Arrow
            self.fleches[2] = self.canvas.create_line(arrow_x, arrow_y, arrow_x-arrow_size, arrow_y-arrow_size/2, arrow_args, tags=(Config.tag_grille, Config.tag_grille_fleche)) #Z Arrow
        elif self.rotationIndex == 2: #bas vers haut
            self.fleches[1] = self.canvas.create_line(arrow_x, arrow_y, arrow_x-arrow_size, arrow_y-arrow_size/2, arrow_args, tags=(Config.tag_grille, Config.tag_grille_fleche)) #X Arrow
            self.fleches[2] = self.canvas.create_line(arrow_x, arrow_y, arrow_x+arrow_size, arrow_y-arrow_size/2, arrow_args, tags=(Config.tag_grille, Config.tag_grille_fleche)) #Z Arrow
        elif self.rotationIndex == 3: #gauche vers droite
            self.fleches[1] = self.canvas.create_line(arrow_x, arrow_y, arrow_x+arrow_size, arrow_y-arrow_size/2, arrow_args, tags=(Config.tag_grille, Config.tag_grille_fleche)) #X Arrow
            self.fleches[2] = self.canvas.create_line(arrow_x, arrow_y, arrow_x+arrow_size, arrow_y+arrow_size/2, arrow_args, tags=(Config.tag_grille, Config.tag_grille_fleche)) #Z Arrow
        
        self.canvas.tag_lower(Config.tag_grille)

    def supprimer(self):
        self.canvas.delete(Config.tag_grille_fleche)