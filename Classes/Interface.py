"""
Interface.py

Gère tout ce qui concerne l'interface de base de l'application.
Elle gère aussi la root window et permet de créer des canvas, boutons, etc
"""

import Classes.Config as Config
import tkinter as tk

from Classes.UI.Toolbar import Toolbar
from Classes.UI.Menubar import Menubar

from Classes.Evenement.EvenementManager import Evenement

class Interface():
	def __init__(self):
		self.root = tk.Tk()
		self.root.title(Config.app_titre)
		self.root.iconbitmap(Config.app_icon_path)

		self.min_resolution = Config.app_minResolution
		self.root.minsize(self.min_resolution[0], self.min_resolution[1])

		self.resizable(False)
	
	#initialiser appeler après start up menu, quand on crée une nouvelle scène ou charger une scène
	def initialiser(self):
		self.canvas = self.creer_canvas()
		self.creer_toolbar()
		self.creer_menubar()

	def afficher(self):
		self.canvas.pack(expand=True, fill="both")
		self.toolbar.afficher()

	def supprimer(self, id):
		self.canvas.delete(id)

	def boucle_principale(self):
		self.root.mainloop()

	def bind(self, nom, fct):
		self.root.bind(nom, fct)
	
	def unbind(self, nom, fct = None):
		if fct == None:
			self.root.unbind(nom)
		else:
			self.root.unbind(nom, fct)

	def tag_bind(self, nom, evt, fct):
		self.canvas.tag_bind(nom, evt, fct)

	def resizable(self, value):
		self.root.resizable(value, value)

	def creer_button(self, parent, **kwargs):
		if parent == None:
			parent = self.root
		b = tk.Button(parent, kwargs)
		return b

	def creer_label(self, parent, **kwargs):
		if parent == None:
			parent = self.root
		l = tk.Label(parent, kwargs)
		return l

	def creer_canvas(self, parent=None):
		if parent == None:
			parent = self.root
		canvas = tk.Canvas(parent)
		canvas.configure(bg=Config.col_app_background)
		return canvas
	
	def creer_frame(self, parent=None):
		if parent == None:
			parent = self.canvas
		frame = tk.Frame(parent)
		frame.config(bg=Config.col_app_background)
		return frame

	def creer_toolbar(self):
		frame = self.creer_frame()
		self.toolbar = Toolbar(self, frame)

	def creer_menubar(self):
		self.menubar = Menubar(self)
		self.menubar.afficher()

	def change_mode(self, index):
		self.toolbar.button_event_click(index)

	@classmethod
	def rotate_scene(cls, event=None, destination = None):
		if destination != None:
			if Config.app_rotation_index > destination:
				number_of_rotation = ((4 - Config.app_rotation_index) + destination) % 4
			else:
				number_of_rotation = (Config.app_rotation_index + destination) % 4
			for i in range(number_of_rotation):
				cls.rotate_scene()
			return

		Config.app_rotation_index = (Config.app_rotation_index + 1) % 4
		Evenement(Config.evt_rotation, Config.app_rotation_index) #envoi un evènement pour la rotation de la scène, à CubeManager et GrilleFleche
