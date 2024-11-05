import Classes.Config as Config

from Classes.Evenement.EvenementManager import Evenement

class AideDidacticiel:

    frame = None
    canvas = None

    tuto_phrase = [ "Bienvenue dans le didacticiel, vous apprendrez le fonctionnement basique de l'application, cliquer sur Suivant.",
                    "Par défaut le [ Mode Création ] est sélectionné en haut à droite de l'application, et les deux autres modes sont pour l'instant inutilisable tant que vous n'avez pas de cube à disposition sur votre scène, cliquer sur Suivant.",
                    "Dans le [ Mode Création ], vous pouvez faire clic gauche sur une case de la grille pour créer un Cube, allez-y essayez, cliquer sur Suivant.",
                    "Une fois votre Cube crée sur la scène, vous pouvez effectuer un clic droit dessus pour le supprimer, cliquer sur Suivant.",
                    "Vous l'aurez peut être remarqué, lorsqu'un Cube au minimum est présent sur la scène, vous avez désormais accès aux autres Mode en haut à droite de l'application, crée un cube sur la grille si ce n'est pas déjà fait, puis cliquer sur Suivant.",
                    "Veuillez cliquer sur le deuxième outil pour passer en [ Mode Couleur ], cliquer sur Suivant.",
                    "Vous verrez 3 cases de couleur apparaitre en bas à droite de l'application, il s'agit de preset de couleur, par défaut le premier est sélectionné. cliquer sur Suivant.",
                    "Essayez donc, passer votre souris sur une face du Cube présent sur la scène, et effectuer un clic gauche, cela aura pour effet de changer la couleur de la face sélectionné, cliquer sur Suivant.",
                    "Inversement, clic droit permet d'enlever la couleur présente sur une face du Cube, cliquer sur Suivant.",
                    "Vous pouvez donc cliquer sur différent preset de Couleur, pour changer rapidement de couleur lorsque vous voudrez peindre une scène rapidement. cliquer sur Suivant",
                    "Effectuer un double clic gauche sur les différent preset de couleur, pour changer la dîte couleur à votre guise. cliquer sur Suivant",
                    "Enfin le dernière outil, le [ Mode Texture ], qui fera apparaitre différentes textures en bas de l'écran, et permet d'appliquer une texture directement à un Cube. cliquer sur Suivant",
                    "Vous pouvez choisir une texture de celle qui vous sont mis à disposition, puis effectuer un clic gauche sur un Cube, pour lui appliquer. cliquer sur Suivant.",
                    "Évidemment clic droit supprimera la dîte texture du Cube. cliquer sur Suivant",
                    "Dernièrement, vous pouvez également cliquer sur les flèches de rotation (ou la touche R du clavier) pour tourner la scène de 90 degré. cliquer sur Suivant",
                    "Si vous avez un doute, passer la souris sur un des outils pendant quelques instants, une aide vous sera afficher ! cliquer sur Suivant.",
                    "Voilà ! vous connaissez désormais les contrôles basiques de l'application, merci et amusez-vous bien !"]
    tuto_index = 0

    @classmethod
    def initialiser(cls, interface):
        cls.frame = interface.creer_frame()
        cls.canvas = interface.canvas
        cls.frame.config(width = 100, height = 50, background = "white")

        cls.frame_btn = interface.creer_frame(cls.frame)
        cls.frame_btn.config(background="white")

        Config.app_is_didacticiel_enable = False

        cls.tuto_index = 0
        cls.setup_didacticiel_label(interface)
        cls.setup_didacticiel_btn(interface)

    @classmethod
    def setup_didacticiel_label(cls, interface):
        cls.label = interface.creer_label(cls.frame, text="Didacticiel", 
                                                background="white",
                                                borderwidth = 0,
                                                font=("Courier New", 15))

        cls.label_tuto = interface.creer_label(cls.frame,
                                                justify='left',
                                                wraplength=450,
                                                background="white",
                                                borderwidth=0,
                                                font=("Arial", 12))

    @classmethod
    def setup_didacticiel_btn(cls, interface):
        cls.suivant_btn = interface.creer_button(cls.frame_btn, text="Suivant", 
                                                    background="white", 
                                                    activebackground="grey", 
                                                    borderwidth=1,
                                                    command= lambda evt=None: cls.suivant_button_click(1, evt))
        cls.fermer_btn = interface.creer_button(cls.frame_btn, text="Fermer", 
                                                    background="white", 
                                                    activebackground="grey", 
                                                    borderwidth=1,
                                                    command= lambda evt=None: cls.suivant_button_click(100, evt))

    @classmethod
    def cacher_didacticiel(cls):
        cls.canvas.delete("didact_frame")
    
    @classmethod
    def afficher_didacticiel(cls, event = None):
        cls.canvas.create_window(15, 15, window = cls.frame, anchor="nw", tags="didact_frame")
        cls.frame.lift()
        cls.frame_btn.lift()
        cls.label.lift()
        cls.suivant_btn.lift()
        cls.fermer_btn.lift()
        cls.frame_btn.pack(side='bottom', fill='x')

    @classmethod
    def suivant_button_click(cls, value, event = None):
        cls.tuto_index += value
        if cls.tuto_index >= len(cls.tuto_phrase):
            cls.tuto_index = 0
            cls.didacticiel_afficher_checkbox(False)
        cls.update_tuto_phrase()
    
    @classmethod
    def update_tuto_phrase(cls):
        if not Config.app_is_didacticiel_enable: return

        t_index = cls.tuto_index

        if t_index >= 1 and t_index <= 4:
            cls.label.config(text="Didacticiel - Mode Création")
        elif t_index > 4 and t_index <= 10:
            cls.label.config(text="Didacticiel - Mode Couleur")
        elif t_index > 10 and t_index <= 13:
            cls.label.config(text="Didacticiel - Mode Texture")
        elif t_index == 14:
            cls.label.config(text="Didacticiel - Rotation")
        else:
            cls.label.config(text="Didacticiel")


        cls.label.pack(side='top', padx=20, pady=7)

        cls.label_tuto.config(text=cls.tuto_phrase[t_index])
        cls.label_tuto.pack(side='top', anchor='w', padx=10, pady=10)

        cls.suivant_btn.pack(side='right', padx=7, pady=7)
        cls.fermer_btn.pack(side='left', padx=7, pady=7)

    @classmethod
    def didacticiel_afficher_checkbox(cls, value, event = None):
        if value:
            cls.afficher_didacticiel()
        else:
            cls.cacher_didacticiel()
        cls.isDiplayed = value
        Config.app_is_didacticiel_enable = value
        Evenement(Config.evt_didacticiel_update, value)
        cls.update_tuto_phrase()