"""
Debug.py

Classe pour le debug, utiliser si DEBUG_MODE = True dans Config.py
permet simplement d'afficher avec le tooltip les tags présent sur un cube
simplifie la vie pour le developpeur qui ne se souvenait jamais de tout les
tags present sur un cube (a permis de debugger le bug de perspective).

Si le debug mode est activé, il suffit de placer sa souris sur un cube
un petit instant pour y voir ses tags associés.
"""

import tkinter as tk
import Classes.Config as Config

from Classes.CubeIso.CubeManager import CubeManager

from Classes.Evenement.EvenementManager import Observateur

from Classes.Utilitaires.ToolTip import ToolTip

class Debug:
    def __init__(self, root, canvas):
        self.root = root
        self.canvas = canvas
        self.tooltip = ToolTip(Config.tag_cube, canvas)
        self.setup_tooltip()
        self.setup_debug_label()

        Observateur.observe(Config.evt_didacticiel_update, self.didact_update)

        self.isVisible = False
        
    def tooltip_enter(self, event=None):
        if self.isVisible == False: return
        self.tooltip.set_text(CubeManager.get_cube_tooltip_msg(self.canvas))
        self.tooltip.enter(event)

    def setup_tooltip(self):
        self.tooltip.tag_bind(Config.tag_cube, '<Enter>', lambda event: self.tooltip_enter(event))
        self.tooltip.tag_bind(Config.tag_cube, '<Leave>', self.tooltip.leave)
        self.tooltip.tag_bind(Config.tag_cube, '<ButtonPress>', self.tooltip.leave)

    def setup_debug_label(self):
        self.label = tk.Label(self.root, text="DEBUG MODE ENABLED", background=Config.col_app_background, foreground="white")

    def afficher(self):
        self.canvas.create_window(10, 110, anchor = "nw", window = self.label, tags="debug_label")

    def didact_update(self, value):
        if value:
            self.label.lower()
        else:
            self.label.lift()

    def cacher(self):
        self.canvas.delete("debug_label")

    def update_affichage(self, value):
        self.isVisible = value
        if value:
            self.afficher()
        else:
            self.cacher()
