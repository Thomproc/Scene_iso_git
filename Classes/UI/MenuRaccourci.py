"""
MenuRaccourci.py

Correspond au menu qui affiche tout les raccourcis clavier de l'application.
"""

class MenuRaccourci:
    frame = None
    canvas = None

    raccourci_txt = "Raccourci \nW  -  Mode Création \nX  -  Mode Couleur \nC  -  Mode Texture \n\nR  -  Rotation de la scène \nD  -  Basculer Mode Développeur \nA  -  Aide Didacticiel \n\nÉchap  -  Quitter l'application \nCtrl + N  -  Nouvelle Scène \nCtrl + O  -  Ouvrir une Scène \nCtrl + S  -  Sauvegarder une Scène"

    @classmethod
    def initialiser(cls, interface):
        cls.frame = interface.creer_frame()
        cls.canvas = interface.canvas
        cls.frame.config(width = 450, height = 250, background = "white")

        cls.setup_raccourci_label(interface)
        cls.setup_raccourci_btn(interface)

    @classmethod
    def setup_raccourci_label(cls, interface):
        cls.label = interface.creer_label(cls.frame, text = cls.raccourci_txt, 
                                                background = "white",
                                                borderwidth = 0,
                                                font = ("Courier New", 15),
                                                justify = 'left')

    @classmethod
    def setup_raccourci_btn(cls, interface):
        cls.fermer_btn = interface.creer_button(cls.frame, text = "Fermer", 
                                                    background = "white", 
                                                    activebackground = "grey", 
                                                    borderwidth = 1,
                                                    command = lambda evt=None: cls.cacher(evt))

    @classmethod
    def cacher(cls, event = None):
        cls.canvas.delete("raccourci")
    
    @classmethod
    def afficher(cls, event=None):
        cls.canvas.create_window(375, 225, window = cls.frame, tags="raccourci")
        cls.frame.lift()
        cls.label.lift()
        cls.fermer_btn.lift()
        cls.label.pack(side="top", anchor="n", padx = 10, pady = 20)
        cls.fermer_btn.pack(side = "bottom", anchor = "s", pady = 12)