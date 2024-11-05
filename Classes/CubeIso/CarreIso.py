"""
CarreIso.py

Contient des methodes statiques pour la generation de face en vue isometrique.
Utilisé pour generer chaque face de la grille
ou encore par Cube.py pour generer chaque face d'un cube
"""

import Classes.Config as Config

"""
Cette classe s'occupe de créer une face d'un cube isométrique depuis une origine x, y
Elle contient des méthodes statiques, pour créer des faces, ou directement récupérer les vertices d'une face
(pas besoin d'instancier cette classe)
"""
class CarreIso():
	
	"""
	Méthodes renvoyant la liste des coordonnées des faces à générer selon leur origine x, y en pixel -----
	"""
	@staticmethod
	def coords_face_top(x, y):
		dim = Config.cube_dim
		return [(x, y), (x + dim, y - dim/2), (x, y - dim), (x - dim, y - dim/2)]
	@staticmethod
	def coords_face_top_G(x, y):
		dim = Config.cube_dim
		return [(x, y), (x, y + dim), (x - dim, y + dim/2), (x - dim, y - dim/2)]
	@staticmethod
	def coords_face_top_D(x, y):
		dim = Config.cube_dim
		return [(x, y), (x + dim, y - dim/2), (x + dim, y + dim/2), (x, y + dim)]

	"""
	-------------------------------------------------------------------------------------------------------

	Méthodes créant les faces gauche, droite et haute pour former un cube
	"""
	@staticmethod
	def gen_face_top(canvas, position, origine, tag, **kwargs):
		dim = Config.cube_dim
		x, y = origine
		coords = CarreIso.coords_face_top(x, y)

		dico = {
			"origine": origine,
			"posCS": (position[0], position[1], position[2] + 1),
			"origineCS": (x, y - dim)
		}
		positionTag = "x" + str(position[0]) + ", y" + str(position[1]) + ", z" + str(position[2])

		tags=(Config.tag_click, tag, positionTag, dico)
		kwargs["tag"] = tags

		id = canvas.create_polygon(coords, kwargs)
		return id

	@staticmethod
	def gen_face_top_G(canvas, position, origine, tag, **kwargs):
		dim = Config.cube_dim
		x, y = origine

		dico = {
			"origine": origine,
			"posCS": (position[0], position[1] + 1, position[2]),
			"origineCS": (x - dim, y + dim/2)
		}
		positionTag = "x" + str(position[0]) + ", y" + str(position[1]) + ", z" + str(position[2])

		tags=(Config.tag_click, tag, positionTag, dico)
		kwargs["tag"] = tags
		coords = CarreIso.coords_face_top_G(x, y)
		id = canvas.create_polygon(coords, kwargs)
		return id

	@staticmethod
	def gen_face_top_D(canvas, position, origine, tag, **kwargs):
		dim = Config.cube_dim
		x, y = origine

		dico = {
			"origine": origine,
			"posCS": (position[0] + 1, position[1], position[2]),
			"origineCS": (x + dim, y + dim/2)
		}
		positionTag = "x" + str(position[0]) + ", y" + str(position[1]) + ", z" + str(position[2])

		tags=(Config.tag_click, tag, positionTag, dico)
		kwargs["tag"] = tags
		coords = CarreIso.coords_face_top_D(x, y)
		id = canvas.create_polygon(coords, kwargs)
		return id

	"""
	-----------------------------------------------------------------------------------------------------
	"""