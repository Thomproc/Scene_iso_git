"""
GrilleIso.py

Créer et affiche une grille isométrique qui sert de base
à la modélisation d'une scène composée de cubes isomètriques.
"""

import Classes.Config as Config
import Classes.Utilitaires.Remap as Remap

from Classes.Grille.GrilleFlecheRepere import GrilleFlecheRepere

from Classes.CubeIso.CarreIso import CarreIso

class GrilleIso():
	"""
	Dessine une grille sur le canvas parent, en vue isométrique.
	taille_grille => correspond aux nombres de cases N pour une grille NxN.
	origin => les coordonnées en pixels du point d'origine de la grille.
	"""
	grille_taille = 0
	canvas = None
	instance = None

	def __init__(self, canvas):
		GrilleIso.canvas = canvas
		GrilleIso.instance = self
		self.fleche = None

	"""
	Méthode permettant de reconstruire la grille en fonction de la taille des cubes choisis. (Redimmensionne la grille)
	"""
	@classmethod
	def resize_grille(cls):
		dim = Config.cube_dim
		factor = Remap.reMap(dim, 15, 60, -3, 0.08)
		Config.app_grille_origin[1] = int(Config.app_grille_origin_static[1] + dim * factor) #calcule la nouvelle origine de la grille en fonction de la taille des cubes, pour mieux centrer la grille et empecher les dépassements de l'écran

		taille_grille = ((Config.app_minResolution[1] - Config.app_grille_origin[1]) // dim) - 1
		if taille_grille < 5:
			if taille_grille < 3:
				taille_grille = 3
		else:
			taille_grille -= 2
		cls.grille_taille = taille_grille
		cls.canvas.delete(Config.tag_grille)
		cls.afficher(cls.instance)


	"""
	Affiche la grille sur le canvas parent.
	"""
	def afficher(self):
		self.cube_dimension = Config.cube_dim
		self.origin = Config.app_grille_origin
		self._grille_dict = {}

		if self.fleche != None:
			self.fleche.supprimer()

		self.creer_grille()
		if GrilleIso.grille_taille == 0:
			self.resize_grille()

	"""
	Renvoie les coordonnées (x, y) en pixels correspondants à l'origine de la grille.
	"""
	def get_origin_from_grille(self, index):
		x = self.get_x_from_grille(index)
		y = self.get_y_from_grille(index)
		return (x, y)

	"""
	Renvoie FAUX si un cube est hors de la grille.
	Sinon, elle renvoie VRAI.
	"""
	@classmethod
	def check_pos_in_bounds(cls, positionCube):
		grille_taille = cls.grille_taille
		if positionCube[0] <= 0 or positionCube[0] > grille_taille: return False
		if positionCube[1] <= 0 or positionCube[1] > grille_taille: return False
		return True
	
	"""
	Renvoie les coordonnées x, y en pixels correspondants à l'origine d'une case (x, y, z) de la grille.
	En d'autres termes on récupère les coordonnées en pixels, d'un point x, y, z, dans la grille.
	"""
	@classmethod
	def get_origin_from_pos(cls, positionGrille):
		x, y, z = positionGrille
		grille_origine = Config.app_grille_origin
		dim = Config.cube_dim
		return (grille_origine[0] + (x - y) * dim, grille_origine[1] + (x + y) * dim/2 - z * dim)

	"""
	Renvoie la nouvelle position d'un cube après avoir été tournée.
	Pour chaque cube, on calcule sa prochaine position après rotation grâce à cette formule :
		Soit (x, y, z) les coordonnées d'un cube. Une fois tourné, le cube aura les coordonnées (x', y', z') telles que:
			-x' = taille_grille - (y - 1)
			-y' = x
			-z' = z
	"""
	@classmethod
	def get_position_rotated(cls, position):
		grille_taille = cls.grille_taille
		newPos_X = grille_taille - (position[1] - 1)
		newPos_Y = position[0]
		newPos_Z = position[2]
		return (newPos_X, newPos_Y, newPos_Z)

	"""
	Renvoie la coordonnée x en pixel correspondant à l'origine de la grille.
	"""
	def get_x_from_grille(self, index):
		return self.origin[0] - (index * self.cube_dimension)

	"""
	Renvoie la coordonnée y en pixel correspondant à l'origine de la grille.
	"""
	def get_y_from_grille(self, index):
		return self.origin[1] + (index * self.cube_dimension /2)

	"""
	Créée et affiche les cases de la grille.
	"""
	def creer_grille(self):
		self.fleche = GrilleFlecheRepere(GrilleIso.canvas, self, 1, 1)
		taille = GrilleIso.grille_taille

		for i in range(taille):
			x, y = self.get_origin_from_grille(i)
			for j in range(taille):
				id = CarreIso.gen_face_top(GrilleIso.canvas, (j+1, i+1, 0),
				 							(x, y + self.cube_dimension),
											Config.tag_grille,
											fill=Config.col_grille,
											outline=Config.col_grille_bord,
											activefill=Config.col_case_active,
											activewidth=5,
											activeoutlinestipple='gray75')

				x += self.cube_dimension
				y += self.cube_dimension /2
		return
