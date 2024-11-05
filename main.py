"""
PROCUREUR Thomas - LAFFAILLE JASON

-------- RENDU PROJET IHM 2021-2022 ---------
|	Application de Modélisation Isométrique |
---------------------------------------------

main.py
"""


"""
--------------- IMPORTATION ---------------------------------
"""
import Classes.Config as Config

from Classes.Debug import Debug

from Classes.Interface import Interface
from Classes.StartUpMenu import StartUpMenu

from Classes.Grille.GrilleIso import GrilleIso
from Classes.CubeIso.CubeManager import CubeManager

from Classes.Modes.Mode import Mode
from Classes.Modes.Mode_Couleur import ModeCouleur
from Classes.Modes.Mode_Texture import ModeTexture

from Classes.UI.Aide_Didacticiel import AideDidacticiel
from Classes.UI.MenuRaccourci import MenuRaccourci
from Classes.UI.Mouse_Indicator import MouseIndicator
from Classes.UI.Menubar import Menubar

"""
--------------- INITIALISATION ---------------------------------
"""

setup_Complete = False

def app_initialisation():
	interface.resizable(True)
	interface.initialiser()
	start_up.hide()
	app_setup()

def new_scene(event = None):
	app_initialisation()
	
	CubeManager.effacer_scene()

	app_finish_setup()

def load_scene(event = None):
	if(Menubar.ouvrir(succeed_fct=app_initialisation)):
		app_finish_setup()

interface = Interface()
start_up = StartUpMenu(interface, new_scene, load_scene, Menubar.quitter)

""" 
--------------- PRINCIPALE ---------------------------------
"""

def debug_mode(event = None):
	Config.DEBUG_MODE = not Config.DEBUG_MODE
	_debug.update_affichage(Config.DEBUG_MODE)

def app_setup():
	global _debug, grille
	CubeManager.initialiser(interface)
	ModeCouleur.initialiser(interface.canvas)
	ModeTexture.initialiser(interface)

	AideDidacticiel.initialiser(interface)
	MenuRaccourci.initialiser(interface)

	MouseIndicator.initialiser(interface)
	grille = GrilleIso(interface.canvas)
	grille.afficher()

	_debug = Debug(interface.root, interface.canvas)

def app_finish_setup():
	global setup_Complete
	
	interface.canvas.tag_lower(Config.tag_grille)

	MouseIndicator.afficher()

	interface.afficher()
	bind()
	setup_Complete = True

def bind():
	interface.bind('<d>', debug_mode)
	interface.bind('<D>', debug_mode)
	interface.bind('<r>', lambda evt: Interface.rotate_scene(evt))
	interface.bind('<R>', lambda evt: Interface.rotate_scene(evt))
	interface.bind('<a>', lambda evt: AideDidacticiel.didacticiel_afficher_checkbox(True, evt))
	interface.bind('<A>', lambda evt: AideDidacticiel.didacticiel_afficher_checkbox(True, evt))
	interface.bind('<w>', lambda evt: interface.change_mode(0))
	interface.bind('<W>', lambda evt: interface.change_mode(0))
	interface.bind('<x>', lambda evt: interface.change_mode(1))
	interface.bind('<X>', lambda evt: interface.change_mode(1))
	interface.bind('<c>', lambda evt: interface.change_mode(2))
	interface.bind('<C>', lambda evt: interface.change_mode(2))
	interface.tag_bind(Config.tag_click, '<ButtonRelease-1>', lambda evt: Mode.clic_gauche())
	interface.tag_bind(Config.tag_click, '<ButtonRelease-3>', lambda evt: Mode.clic_droit())
	return

def main():
	interface.boucle_principale()

if __name__ == "__main__":
	main()
