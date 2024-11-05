"""
CubeManager.py

Le chef d'orchestre de tous les cubes.
Pas besoin d'instance de cette classe pour l'utiliser.
Il s'occupe d'instancier les cubes dans la scène,
de tourner la scene et gérer les cubes et leur perspective
en conséquence.
Ainsi que le chargement de nouvelle scène vierge ou à partir d'un fichier,
le chef d'orchestre s'en charge.
"""

import Classes.Config as Config
from Classes.Grille.GrilleIso import GrilleIso
import Classes.Utilitaires.PositionTagConverter as PosTagConverter

from Classes.CubeIso.Cube import Cube

from Classes.Evenement.EvenementManager import Observateur, Evenement

from Classes.Modes.Mode_Texture import ModeTexture


class CubeManager():

	dico_cubes = {}
	canvas = None
	interface = None
	
	@classmethod
	def initialiser(cls, interface):
		cls.canvas = interface.canvas
		cls.interface = interface
		Observateur.observe(Config.evt_rotation, cls.tourner_cube)

	"""
	Méthode permettant de créer un cube suite à un clique.
	"""
	@classmethod
	def creer_cube(cls):
		dicoTags = eval(cls.canvas.gettags("current")[3]) #conversion de la chaine de caract�re en dictionnaire
		posNewCube = dicoTags.get("posCS") #case sur laquelle le prochain cube sera construit
		if GrilleIso.check_pos_in_bounds(posNewCube) == False: return

		x, y = dicoTags.get("origineCS") #coordonn�es du cube � cr�er

		newCube = Cube(cls.canvas, x, y, posNewCube)
		posTag = PosTagConverter.convertPosToStrTag(posNewCube[0], posNewCube[1], posNewCube[2])

		cls.dico_cubes[posTag] = newCube
		Evenement(Config.evt_nombre_cube_update, len(cls.dico_cubes))

		cls.ajuster_perspective(posNewCube)
		return

	"""
	Détruit le cube sur lequel l'utilisateur clique.
	"""
	@classmethod
	def detruire_cube(cls):
		current = cls.canvas.gettags("current")
		objTag = current[1]
		if objTag != Config.tag_cube: return
		
		posTagCube = current[2]
		cls.canvas.delete(posTagCube)#suppression du cube dans le canvas
		cube = cls.dico_cubes[posTagCube]
		if cube.hasTexture == True:
			cube.supprimer_texture()
		cls.dico_cubes.pop(posTagCube)
		Evenement(Config.evt_nombre_cube_update, len(cls.dico_cubes))
		return

	"""
	Méthode permettant de modifier la couleur des faces des cubes.
	"""
	@classmethod
	def changer_couleur_face(cls, new_couleur = None):
		currentIdFace = cls.canvas.find_withtag("current")[-1]
		current = cls.canvas.gettags("current")
		objTag = current[1]
		if objTag != Config.tag_cube: return
		
		posTagCube = current[2]
		cube = cls.dico_cubes[posTagCube]
		cube.changer_couleur_face(currentIdFace, new_couleur)


	"""
	Méthode permettant de modifier la texture d'un cube, soit l'ajouter, soit la supprimer, en fonction de l'argument texture
	"""
	@classmethod
	def changer_texture_cube(cls, texture = None):
		current = cls.canvas.gettags("current")
		objTag = current[1]
		if objTag != Config.tag_cube: return

		posTagCube = current[2]
		cube = cls.dico_cubes[posTagCube]
		cube.changer_texture_cube(texture)
		posCubeTuple = PosTagConverter.convertTagToTuple(posTagCube)
		cls.ajuster_perspective(posCubeTuple)

	"""
	Méthode permettant d'effectuer une rotation de la scène.
	"""
	@classmethod
	def tourner_cube(cls, rotationIndex):
		newDico_cubes = {}

		#cette boucle rempli le nouveau dictionnaire de cube ayant subi une "rotation"
		for posCubeTag in cls.dico_cubes.keys():
			posCubeTuple = PosTagConverter.convertTagToTuple(posCubeTag)

			newPosition = GrilleIso.get_position_rotated(posCubeTuple)
			newPosCubeTag = PosTagConverter.convertPosToStrTag(newPosition[0], newPosition[1], newPosition[2])

			#remplisage du nouveau dictionnaire
			newDico_cubes[newPosCubeTag] = cls.dico_cubes[posCubeTag]

			cube = newDico_cubes[newPosCubeTag]
			cube.origine = GrilleIso.get_origin_from_pos(newPosition)
			cube.position = newPosition

		#on supprime tout les anciens cubes de la scène
		for posCubeTag in cls.dico_cubes.keys():
			cls.canvas.delete(posCubeTag)

		#modification du dictionnaire des cubes enregistrés dans le CubeManager
		cls.dico_cubes = newDico_cubes

		#puis on affiche les nouveaux cubes 
		for cube in cls.dico_cubes.values():
			cube.afficher()
		
		#on ajuste la perspective à partir de la position la plus éloignée
		cls.ajuster_perspective((0, 0, 0))
		return


	"""
	Ajustement de la perspective des Cubes.
	"""
	@classmethod
	def ajuster_perspective(cls, posCube):
		#Soit (x, y, z) et (x', y', z') deux positions dans la grille où se situent un cube.
		#Si (x + y < x' + y' ET z <= z') OU (x + y = x' + y' ET z < z'), alors le cube en (x', y', z') doit être placé devant.
		#Ainsi, à chaque création d'un cube sur (x, y, z), on stock dans un dictionnaire tous les cubes existant qui respectent une des propriétés
		#ci-dessus. 
		#Le dictionnaire est ordonné comme suit : 
		#	La clé est (x' + y') car tous les cubes sur une même ligne auront la même valeur.
		#	Ainsi, le dictionnaire renvoie une liste de cubes qui sont tous sur la même ligne.
		
		#Ensuite, il faut trier la liste des clés (x' + y') dans l'ordre croissant afin que les cubes les plus éloignés du cube créé soient 'raise' en dernier.
		#Enfin, il faut trier la liste des cubes avec pour clé (x' + y') selon la coordonnée z' afin que ceux ayant une coordonnée z' plus élevée soient 'raise' en dernier.

		dico_cube_a_ajuster = {}

		sommeXY = posCube[0] + posCube[1]
		for posCubeDevantTag in cls.dico_cubes.keys():
			posCubeDevantTuple = PosTagConverter.convertTagToTuple(posCubeDevantTag)
			if posCubeDevantTuple[0] <= posCube[0] and posCubeDevantTuple[1] <= posCube[1] and posCubeDevantTuple[2] <= posCube[2]: continue

			sommeXYprime = posCubeDevantTuple[0] + posCubeDevantTuple[1]
			
			if(posCube[2] <= posCubeDevantTuple[2] and sommeXY < sommeXYprime or sommeXY == sommeXYprime and posCube[2] < posCubeDevantTuple[2]):
				if sommeXYprime not in dico_cube_a_ajuster:
					dico_cube_a_ajuster[sommeXYprime] = [posCubeDevantTag]
				elif posCubeDevantTag not in dico_cube_a_ajuster:
					dico_cube_a_ajuster[sommeXYprime].append(posCubeDevantTag)
		ajuster_sorted = sorted(dico_cube_a_ajuster)

		for key_sorted in ajuster_sorted:
			dico_values_sorted = sorted(dico_cube_a_ajuster[key_sorted], key=lambda x: PosTagConverter.convertTagToTuple(x)[2])
			for tag in dico_values_sorted:
				cls.canvas.tag_raise(tag)
				cls.dico_cubes[tag].raise_texture()

	"""
	Permet de récupérer les informations liées au cube courant et les afficher en tooltip.
	"""
	@classmethod
	def get_cube_tooltip_msg(cls, canvas):
		posTag = canvas.gettags("current")[2]
		cube = cls.dico_cubes[posTag]
		if cube == None: return
		return cube.tooltip_txt()

	"""
	Permet de reconstruire une scène à partir du dictionnaire contenu dans un fichier texte.
	"""
	@classmethod
	def charger_scene(cls, dico_scene):
		has_to_rotate = [False, 0]

		for key in dico_scene:

			if key == "cube_dim":
				Config.cube_dim = int(dico_scene.get(key))
				GrilleIso.resize_grille()
				continue
			if key == "rotation_index":
				has_to_rotate = [True, int(dico_scene.get(key))]
				continue

			#Récupération des options du cube
			option = dico_scene.get(key)
			dico_opt = eval(str(option))

			#Récupération des coordonnées du cube
			posNewCube = PosTagConverter.convertTagToTuple(key)
			if GrilleIso.check_pos_in_bounds(posNewCube) == False: continue
			x, y = GrilleIso.get_origin_from_pos(posNewCube)

			#Récupération de la couleur des faces du cube
			couleur_face = dico_opt.get("couleur_face")
			dico_couleur_face = eval(str(couleur_face))

			#Création du cube avec les faces de la bonne couleur
			newCube = Cube(cls.canvas, x, y, posNewCube, dico_couleur_face)

			#Application de la texture au cube
			textureIndex = dico_opt.get("textureIndex")
			if(textureIndex != None):
				texture = ModeTexture.get_texture_from_index(int(textureIndex))
				newCube.changer_texture_cube(texture)

			cls.dico_cubes[key] = newCube

		if has_to_rotate[0] == True:
			cls.interface.rotate_scene(destination = has_to_rotate[1])
		
		cls.ajuster_perspective((0, 0, 0))	#on réajuste la perspective à partir du fond de la scène.
		Evenement(Config.evt_nombre_cube_update, len(cls.dico_cubes))
		return

	"""
	Efface tous les cubes présents sur la scène ainsi que leur texture.
	"""
	@classmethod
	def effacer_scene(cls):
		for key, cube in cls.dico_cubes.items():
			if cube.hasTexture == True:
				cube.supprimer_texture()
			cls.canvas.delete(key)
		cls.dico_cubes.clear()
		Evenement(Config.evt_nombre_cube_update, len(cls.dico_cubes))