#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Module contenant la classe ArbreHuffman et les exceptions associées
"""

class ArbreHuffmanError(Exception):
    """
    Exception mère des erreurs du module arbre_huffman
    """

class DoitEtreUneFeuilleError(ArbreHuffmanError):
    """
    Exception qui est levé lorsque l'on utilise une méthode
    sur une arbre alors que ça devrait être sur une feuille
    """

class NeDoitPasEtreUneFeuilleError(ArbreHuffmanError):
    """
    Exception qui est levé lorsque l'on utilise une méthode
    sur une feuille alors que ça devrait être sur un arbre
    """

class ArbreHuffmanIncoherentError(ArbreHuffmanError):
    """
    Exception levé lorsque l'initialisation d'un Arbre de Huffman
    présente une incohérence quelconque.
    """

class ArbreHuffman(object):
    """
    Classe ArbreHuffman permettant d'instancier un Arbre de Huffman, un arbre binaire,
    sous la forme d'une feuille ou d'un noeud.
    """

    def __init__(self, element=None, nb_occurrences=None, fils_gauche=None, fils_droit=None):
        """
        Pour initialiser une Arbre de Huffman, on a deux choix:
         -On initialise une feuille, à l'aide d'un élément et d'un nombre d'occurrences
         -On initialise un noeud, à l'aide de deux fils.

        L'initialisation à l'aide d'un nombre d'occurrence et d'un fils ou d'un élément
        et d'un fils par exemple ne donnera qu'une incohérence levée par
        l'exception ArbreHuffmanIncoherentError
        """
        if (element and nb_occurrences) and not (fils_gauche or fils_droit):
            self._element = element
            self._nb_occurrences = nb_occurrences
            self._fils_gauche = fils_gauche
            self._fils_droit = fils_droit
        elif ((fils_gauche or fils_droit) and not (nb_occurrences or element)
              and (fils_gauche is not fils_droit)):
            self._element = element
            self._nb_occurrences = fils_droit.nb_occurrences + fils_gauche.nb_occurrences
            self._fils_gauche = fils_gauche
            self._fils_droit = fils_droit
        else:
            raise ArbreHuffmanIncoherentError(
                "Il est impossible d'initialiser un Arbre de Huffman de cette façon")

    @property
    def est_une_feuille(self):
        """
        Property qui retourne si l'ArbreHuffman est une feuille ou non.
        """
        return self._element is not None

    @property
    def nb_occurrences(self):
        """
        Property qui retourne l'attribut _nb_occurrences
        """
        return self._nb_occurrences

    @property
    def element(self):
        """
        Property qui retourne l'attribut _element si il existe.
        Sinon l'exception DoitEtreUneFeuilleError est levée
        """
        if self.est_une_feuille:
            return self._element
        else:
            raise DoitEtreUneFeuilleError(
                "%s doit être une feuille pour posséder un élément" %self)

    @property
    def fils_gauche(self):
        """
        Property qui retourne l'attribut _fils_gauche.
        Exception NeDoitPasEtreUneFeuilleError levée si l'instance est une feuille
        """
        if self.est_une_feuille:
            raise NeDoitPasEtreUneFeuilleError(
                "%s est une feuille. Elle ne possède pas de fils gauche"%self)
        else:
            return self._fils_gauche

    @property
    def fils_droit(self):
        """
        Property qui retourne l'attribut _fils_droit.
        Exception NeDoitPasEtreUneFeuilleError levée si l'instance est une feuille
        """
        if self.est_une_feuille:
            raise NeDoitPasEtreUneFeuilleError(
                "%s est une feuille. Elle ne possède pas de fils droit"%self)
        else:
            return self._fils_droit

    def __repr__(self):
        """
        Redéfinition de la méthode __repr__
        """
        if self.est_une_feuille:
            return ("ArbreHuffman(element = '%s', nb_occurrences = %s)"
                    %(self.element, self.nb_occurrences))
        else:
            return ("ArbreHuffman(fils_gauche = %s, fils_droit = %s)"
                    %(self.fils_gauche, self.fils_droit))

    def __str__(self):
        """
        Redéfinition de la méthode __str__
        """
        if self.est_une_feuille:
            return "(%s, %s)"%(self.nb_occurrences, self.element)
        else:
            return "(%s, %s, %s)"%(self.nb_occurrences, self.fils_gauche, self.fils_droit)

    def __ge__(self, autre):
        """
        Redéfinition de la méthode __ge__
        """
        return self.nb_occurrences >= autre.nb_occurrences

    def __gt__(self, autre):
        """
        Redéfinition de la méthode __gt__
        """
        return self.nb_occurrences > autre.nb_occurrences

    def __le__(self, autre):
        """
        Redéfinition de la méthode __le__
        """
        return self.nb_occurrences <= autre.nb_occurrences

    def __lt__(self, autre):
        """
        Redéfinition de la méthode __lt__
        """
        return self.nb_occurrences < autre.nb_occurrences

    def __eq__(self, autre):
        """
        Redéfinition de la méthode __eq__
        """
        if self.est_une_feuille and autre.est_une_feuille:
            return ((self.element == autre.element)
                    and (self.nb_occurrences == autre.nb_occurrences))
        elif not (self.est_une_feuille or autre.est_une_feuille):
            return ((self.nb_occurrences == autre.nb_occurrences)
                    and (self.fils_gauche == autre.fils_gauche)
                    and (self.fils_droit == autre.fils_droit))
        else:
            return False

    def __hash__(self):
        """
        Redéfinition de la méthode __hash__
        """
        if self.est_une_feuille:
            return 3*hash(self.nb_occurrences)+5*hash(self.element)
        else:
            return 3*hash(self.nb_occurrences)+3*hash(self.fils_gauche)+5*hash(self.fils_droit)

    def __ne__(self, autre):
        """
        Redéfinition de la méthode __ne__
        """
        return not self == autre
