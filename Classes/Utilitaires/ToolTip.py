"""
Tooltip.py
un tooltip tres inspire de cette page internet

https://stackoverflow.com/questions/3221956/how-do-i-display-tooltips-in-tkinter

modifie selon nos besoins et la flexibilite pour plusieurs widget a la fois
utiliser pour afficher des informations utiles a l'utilisateur
si sa souris reste un petit instant sur un widget sans clic.
"""

import tkinter as tk
from tkinter.constants import LEFT, SOLID

class ToolTip:
    def __init__(self, binder, canvas=None, attente_ms=1250, auto_event=True, txt=""):
        
        self.canvas = canvas
        self.attente_ms = attente_ms
        
        self.isTagBind = False
        self.custom_text = txt

        if isinstance(binder, str):
            self.isTagBind = True
        else:
            self.widget = binder

        self.tooltip_window = None
        self.id_timer = None

    def tag_bind(self, tag, nom, fct):
        self.canvas.tag_bind(tag, nom, fct)
    def bind(self, nom, fct):
        self.widget.bind(nom, fct)

    def set_text(self, txt):
        self.custom_text = txt

    def enter(self, event=None):
        self.timer_affichage()

    def leave(self, event=None):
        self.stop_timer_affichage()
        self.supprimer()

    def timer_affichage(self):
        self.stop_timer_affichage()
        if self.isTagBind:
            self.id_timer = self.canvas.after(self.attente_ms, self.afficher_window)
        else:
            self.id_timer = self.widget.after(self.attente_ms, self.afficher_window)
    
    def stop_timer_affichage(self):
        tmp = self.id_timer
        self.id_timer = None
        if tmp == None: return
        if self.isTagBind:
            self.canvas.after_cancel(tmp)
        else:
            self.widget.after_cancel(tmp)
            

    def afficher_window(self):
        if self.tooltip_window != None: return

        if self.isTagBind:
            self.tooltip_window = tk.Toplevel(self.canvas)
        else:
            self.tooltip_window = tk.Toplevel(self.widget)

        x, y = self.tooltip_window.winfo_pointerxy()
        x += 15
        y += 15
        self.tooltip_window.wm_overrideredirect(1)
        self.tooltip_window.wm_geometry("+%d+%d" % (x, y))
        self.afficher()

    def afficher(self, txt="Default Text"):
        if self.custom_text != "":
            txt = self.custom_text
            
        label = tk.Label(self.tooltip_window, text=txt, 
                            justify=LEFT, 
                            background="white", 
                            foreground="black", 
                            relief=SOLID, 
                            borderwidth=1)
        label.pack()

    def supprimer(self):
        tmp = self.tooltip_window
        self.tooltip_window = None
        if tmp == None: return

        tmp.destroy()