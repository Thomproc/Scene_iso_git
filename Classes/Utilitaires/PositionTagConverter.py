"""
PositionTagConverter.py

ce fichier contient quelque méthode utilitaire
utiliser principalement lorsque l'on ajuste la perspective ou qu'on tourne la scène
dans CubeManager.py

sert principalement a convertir les coordonnees x y z
en chaine de caractere et inversement
pour l'appliquer ensuite aux tags des differents cubes
evitant les effets de bord avec tkinter et sa conversion automatique des tags
"""

def convertPosToStrTag(x, y, z):
    return "x" + str(x) + ", y" + str(y) + ", z" + str(z)

def convertTagToList(tagStr):
    l = tagStr.split(", ")
    for i in range(len(l)):
        l[i] = int(l[i][1:])
    return l

def convertTagToTuple(tagStr):
    return tuple(convertTagToList(tagStr))