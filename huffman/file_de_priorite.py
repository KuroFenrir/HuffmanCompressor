#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Module contenant la classe FileDePriorite, les exceptions FDPVide et ElementNonComparable"""

class FileDePrioriteVideError(Exception):
    """Exception qui se déclenche lorsque qu'on essaie d'accéder à un élément d'une file vide"""
    pass

class ElementNonComparableError(Exception):
    """Exception concernant les éléments non comparable."""
    pass

class FileDePriorite(object):
    """Classe FileDePriorite. Collection d'éléments"""

    def __init__(self, *elements):
        """Méthode d'initialisation de la classe FileDePriorite"""
        self._file = []
        for element in elements:
            self.enfiler(element)

    def enfiler(self, element, i=0):
        """Méthode qui enfile un élément dans la file"""
        try:
            element < element
        except Exception:
            raise ElementNonComparableError(
                "La classe de %s ne possède pas les méthodes de comparaison." %str(element))
        for iterable in self._file:
            try:
                element < iterable
            except Exception:
                raise ElementNonComparableError(
                    "%s n'est pas comparable aux autres éléments de la file" %str(element))
        if not self.est_vide:
            while i < len(self._file) and element > self._file[i]:
                i = i+1
        self._file.insert(i, element)

    def defiler(self):
        """Méthode qui défile l'élément le plus prioritaire de la file"""
        element = self.element
        self._file.remove(element)
        return element

    @property
    def element(self):
        """Méthode qui retourne l'élément le plus prioritaire d'une file"""
        if not self.est_vide:
            return min(self._file)
        else:
            raise FileDePrioriteVideError(
                "%s est vide. Impossible d'avoir son élément prioritaire." %self.__class__.__name__)
    @property
    def est_vide(self):
        """Méthode qui retourne un booléen si la file est vide"""
        return len(self._file) == 0

    def __len__(self):
        return len(self._file)

    def __repr__(self):
        """Redéfinition de __repr__"""
        return "FileDePriorité: %s"%self._file

    def __str__(self, cdc=""):
        """Redéfinition de __str__"""
        for pos, element in enumerate(self._file):
            cdc = cdc+"pos(%s): %s, "%(pos+1, element)
        return cdc[:-2]
