"""
Cube.py

Pour chaque instance, créé un cube
et l'affiche dans la scene dans le canvas parent.
Chaque instance est créée par le CubeManager.py
"""

import Classes.Config as Config

from Classes.CubeIso.CarreIso import CarreIso as cIso

class Cube():
	"""
	Constructeur des cubes. 
	Possibilité de fournir un dictionnaire de couleur pour créer un cube avec des faces colorées.
	Dans le cas contraire, une couleur par défaut est appliquées à chaque face.
	"""
	def __init__(self, canvas, x, y, position, dico_couleur_face = None):
		self.canvas = canvas
		self.origine = (x, y)
		self.position = position
		self.hasTexture = False

		if dico_couleur_face == None:
			self.couleur_face = {	"top": Config.col_cube_top,
									"gauche": [Config.col_cube_gauche, Config.col_cube_droite],
									"droite": [Config.col_cube_droite, Config.col_cube_gauche]	} # [face avant, face arriere]
		else:
			self.couleur_face = dico_couleur_face

		self.face_gauche_dico = {
			0: ("gauche", 0),
			1: ("droite", 0),
			2: ("droite", 1),
			3: ("gauche", 1)
		}

		self.face_droite_dico = {
			0: ("droite", 0),
			1: ("droite", 1),
			2: ("gauche", 1),
			3: ("gauche", 0)
		}

		self.afficher()

	"""
	Méthode permettant d'afficher un cube avec les bonnes couleurs et textures.
	"""
	def afficher(self):
		top   = cIso.gen_face_top(self.canvas, self.position,
									self.origine,
									Config.tag_cube,
									fill= self.couleur_face["top"],
									outline=Config.col_cube_bord,
									activefill=Config.col_case_active)
		top_G = cIso.gen_face_top_G(self.canvas, self.position,
										self.origine,
										Config.tag_cube,
										fill=self.get_face_gauche_couleur_rotation(),
										outline=Config.col_cube_bord,
										activefill=Config.col_case_active)
		top_D = cIso.gen_face_top_D(self.canvas, self.position,
										self.origine,
										Config.tag_cube,
										fill=self.get_face_droite_couleur_rotation(),
										outline=Config.col_cube_bord,
										activefill=Config.col_case_active)

		if self.hasTexture == True:
			self.changer_texture_cube(self.textureData)

		self.idFaces = { "top": top,
						"gauche": top_G, 
						"droite": top_D }
		return self.idFaces

	"""
	Méthode permettant de modifier la couleur du Cube, d'après un dictionnaire fourni en paramètre.
	"""
	def changer_couleur_cube(self, new_couleur_face):
		self.couleur_face = new_couleur_face
		self.idFaces["top"].config(fill = self.couleur_face["top"])
		self.idFaces["gauche"].config(fill = self.get_face_gauche_couleur_rotation())
		self.idFaces["droite"].config(fill = self.get_face_droite_couleur_rotation())

	"""
	Méthode permettant de modifier la couleur d'une face unique, appartenant au Cube.
	"""
	def changer_couleur_face(self, idFace, new_couleur):
		for key, faceId in self.idFaces.items():
			if key == "top" and faceId == idFace:
				c = new_couleur if new_couleur != None else Config.col_cube_top
				self.couleur_face["top"] = c
				self.canvas.itemconfigure(idFace, fill=c)
			elif faceId == idFace:
				if key == "gauche":
					c = new_couleur if new_couleur != None else Config.col_cube_gauche
					self.set_face_gauche_couleur_rotation(c)
					self.canvas.itemconfigure(idFace, fill=self.get_face_gauche_couleur_rotation())
				elif key == "droite":
					c = new_couleur if new_couleur != None else Config.col_cube_droite
					self.set_face_droite_couleur_rotation(c)
					self.canvas.itemconfigure(idFace, fill=self.get_face_droite_couleur_rotation())

	"""
	Méthode permettant de modifier la texture lié au Cube
	"""
	def changer_texture_cube(self, textureData):
		#supprimer la texture
		if textureData == None:
			if self.hasTexture == False: return
			self.canvas.delete(self.textureId)
			self.textureId = None
			self.textureIndex = None
			self.texture = None
			self.textureData = None
			self.texturePosition = (0, 0)
			self.hasTexture = False
			return

		#ajoute ou remplace la texture sur le cube
		if self.hasTexture == True:
			self.canvas.delete(self.textureId)
		self.textureData = textureData
		self.texture = textureData[0]
		self.textureIndex = textureData[1]
		self.textureId = self.canvas.create_image(self.origine[0], self.origine[1], image=textureData[0], state="disabled")
		self.texturePosition = self.origine
		self.hasTexture = True

	def raise_texture(self):
		if self.hasTexture == False: return
		self.canvas.tag_raise(self.textureId)

	def supprimer_texture(self):
		self.changer_texture_cube(None)

	"""
	Méthodes permettant d'obtenir ou modifier les informations liées à la couleur des faces lors de la rotation.----------------------
	"""
	def get_face_gauche_couleur_rotation(self):
		rot_index = Config.app_rotation_index
		gauche_tuple = self.face_gauche_dico[rot_index]
		return self.couleur_face[gauche_tuple[0]][gauche_tuple[1]]

	def set_face_gauche_couleur_rotation(self, value):
		rot_index = Config.app_rotation_index
		gauche_tuple = self.face_gauche_dico[rot_index]
		self.couleur_face[gauche_tuple[0]][gauche_tuple[1]] = value

	def get_face_droite_couleur_rotation(self):
		rot_index = Config.app_rotation_index
		droite_tuple = self.face_droite_dico[rot_index]
		return self.couleur_face[droite_tuple[0]][droite_tuple[1]]

	def set_face_droite_couleur_rotation(self, value):
		rot_index = Config.app_rotation_index
		droite_tuple = self.face_droite_dico[rot_index]
		self.couleur_face[droite_tuple[0]][droite_tuple[1]] = value

	"""
	-----------------------------------------------------------------------------------------------------------------------------------
	"""

	"""
	Méthode qui génère le texte affiché par le tooltip sur ce Cube.
	contenant tout ces tags et ces étiquettes attribuées.
	"""
	def tooltip_txt(self):
		id = self.canvas.find_withtag("current")
		tags = self.canvas.gettags(id)
		message = "tags {\n"
		for i in range(len(tags) - 2):
			message += "   " + tags[i] + '\n'
		message += "   étiquettes : " + tags[3] + '\n}'
		return message