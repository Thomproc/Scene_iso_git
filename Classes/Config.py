"""
Config.py \n
Fichier de configuration de toute l'application \n
Ces variables sont utilises par beaucoup d'autres modules.
"""


"""
APPLICATION ---------------------------------
"""
app_titre = "Application de Modélisation Isométrique"
app_icon_path = "./Images/isometric-icon.ico"
app_minResolution = (750, 450) #en pixel

app_grille_origin_static = [350, 200]
app_grille_origin = [350, 200]

app_rotation_index = 0

app_is_didacticiel_enable = False

"""
TAGS ------------------------------------------
"""
tag_grille = "grille"
tag_cube = "cube"
tag_click = "click"
tag_grille_fleche = "grille_fleche"

"""
CUBE -----------------------------------------
"""
cube_dim = 30
min_cube_dim = 15
max_cube_dim = 60

"""
UI --------------------------------------
"""

ui_taille_bouton_outil = 50
ui_taille_bouton_couleur = 40
ui_taille_bouton_texture = 30

"""
COULEURS -------------------------------------
"""

col_cube_top = '#d1ccc0'
col_cube_gauche = '#aaa69d'
col_cube_droite = '#84817a'
col_cube_bord = '#2f3542'

col_app_background = '#57606f'
col_app_background_darker = '#444a54'

col_grille = '#57606f'
col_grille_bord ='#b2bec3'

col_case_active = '#dfe4ea'

"""
EVENEMENTS -------------------------------------
"""

evt_rotation = "evt_Rotation"
evt_nombre_cube_update = "evt_nbr_cube_update"
evt_mode_update = "evt_mode_update"
evt_didacticiel_update = "evt_didact_update"
evt_app_init = "evt_app_init"

"""
DEV ONLY ------------------------------------
"""
DEBUG_MODE = False