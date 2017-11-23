#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Module contenant la classe Compteur"""

class Compteur(object):
    """Classe Compteur, créer dictionnaire qui compte le nombre d'occurrences des clés"""

    def __init__(self, val_init=None):
        """Méthode d'initialisation de la classe Compteur. Peut s'initialiser avec une séquence."""
        self._compteur = {e:1 for e in val_init} if val_init != None else {}

    def incrementer(self, element):
        """Méthode qui incrémente le nombre d'occurrences d'une clé"""
        if element in self._compteur:
            self._compteur[element] += 1
        else:
            self.fixer(element, 1)

    def fixer(self, element, valeur):
        """Méthode qui fixe la valeur d'une clé"""
        self._compteur[element] = valeur

    def nb_occurences(self, element):
        """Méthode qui retourne le nombre d'occurrences d'une clé"""
        return self._compteur[element] if element in self._compteur else 0

    @property
    def elements(self):
        """Méthode retournant la liste des clés"""
        return list(self._compteur.keys())

    def _elements_condition(self, valeur):
        """Méthode qui retourne une liste de clé selon une condition sur le nombre d'occurrences"""
        return [k for k in self.elements if self._compteur[k] == valeur]

    def elements_moins_frequents(self):
        """Méthode qui retourne les clés qui apparaissent le moins"""
        return self._elements_condition(min(self._compteur.values()))

    def elements_plus_frequents(self):
        """Méthode qui retourne les clés qui apparaissent le plus"""
        return self._elements_condition(max(self._compteur.values()))

    def elements_par_nb_occurrences(self):
        """Méthode qui retourne les clés et les occurrences, classés par nombre d'occurrences"""
        return [(i, self._elements_condition(i)) for i in set(self._compteur.values())]

    def __repr__(self):
        """Redéfinition de __repr__"""
        return "Compteur, taille: %d"%len(self._compteur)

    def __str__(self):
        """Redéfinition de __str__"""
        return "Compteur contenant: %s"%self.elements

if __name__ == "__main__":
    C = Compteur()
    C.incrementer('a')
    C.incrementer('a')
    C.incrementer('b')
    C.incrementer('c')
    C.incrementer('c')
    C.incrementer('c')
    C.incrementer('d')
    print(repr(C))
    print(C.elements)
    print(C.elements_plus_frequents())
    print(C.elements_moins_frequents())
    print(C.elements_par_nb_occurrences())
