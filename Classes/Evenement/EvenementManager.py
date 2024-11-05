"""
EvenementManager.py \n

ce fichier contient une implémentation du "patron de conception Observateur" / "Observer Pattern" \n
qui est inspire d'une page internet : \n
https://www.protechtraining.com/blog/post/tutorial-the-observer-pattern-in-python-879#observing-events

modifier et retravailler pour fonctionner sans besoin d'instance pour les observateurs, et permettre \n
a plusieurs observateur d'observer un même evenement.
"""

class Observateur:

    _observables = {}

    @classmethod
    def observe(cls, nom, fct):
        if nom not in cls._observables:
            cls._observables[nom] = [fct]
            return
        cls._observables[nom].append(fct)

class Evenement:
    def __init__(self, nom, data=None):
        self._nom = nom
        self._data = data
        self.declencher()
    def declencher(self):
        for key in Observateur._observables:
            if self._nom == key:
                for obs in Observateur._observables[self._nom]:
                    if self._data == None:
                        obs()
                        continue
                    obs(self._data)