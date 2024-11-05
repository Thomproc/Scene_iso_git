"""
CustomButtons.py \n

cette classe herite des boutons de tkinter, donnant plus de controle \n
permettant d'imiter le comportement des radio buttons, par exemple \n
ou encore d'utiliser les methodes de Tooltip pour chaque instance de cette classe
"""


import Classes.Config as Config

from tkinter import Button

from Classes.Utilitaires.ToolTip import ToolTip

class CustomButton(Button):
    def __init__(self, parent, id, images, tooltipText, fct_onClick, **kwargs):
        super().__init__(parent, kwargs)        
        self.id = id
        self.images = images
        self.tooltipTxt = tooltipText

        self.config(borderwidth = 0)
        self.config(background = Config.col_app_background)
        self.config(activebackground = Config.col_case_active)
        self.config(image = self.images[0])

        self._isSelected = False

        self.tooltip = ToolTip(parent)
        self.tooltip.bind('<ButtonPress>', self.tooltip.leave)

        self.bind("<Enter>", lambda event=None: self.button_event_enter(event))
        self.bind("<Leave>", lambda event=None: self.tooltip.leave(event))
        self.bind("<ButtonRelease-1>", lambda event=None, index=id: fct_onClick(index, event))
        

    def button_event_enter(self, event=None):
        self.tooltip.set_text(self.tooltipTxt)
        self.tooltip.enter(event)

    @property
    def isSelected(self):
        return self._isSelected

    @isSelected.setter
    def isSelected(self, value):
        self.config(image=self.images[value])
        self._isSelected = value
