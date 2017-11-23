#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Module contenant le type énum Bit et la classe CodeBinaire"""

from enum import Enum

class AuMoinsUnBitError(Exception):
    """Exception qui se déclenche si on essaie de supprimer le
     dernier bit d'un CodeBinaire"""

class Bit(Enum):
    """Enumération de Bits."""
    BIT_0 = 0
    BIT_1 = 1

    def __len__(self):
        return 1

    def __repr__(self):
        """Redéfinition de la méthode spéciale __repr__"""
        return "Bit.%s" %self.name

    def __str__(self):
        """Redéfinition del a méthode spéciale __str__"""
        return "%i"%self.value

class CodeBinaire(object):
    """Classe CodeBinaire. Suite de Bits"""

    def __init__(self, bit, *bits):
        """Init de la classe CodeBinaire"""
        if not isinstance(bit, Bit):
            raise TypeError(
                "%s n'est pas un Bit."%str(bit))
        for iterable in list(bits):
            if not isinstance(iterable, Bit):
                raise TypeError(
                    "%s n'est pas un Bit."%str(iterable))
        self._code = [bit, *bits]

    def ajouter(self, bit):
        """Méthode d'ajout de bits dans le CodeBinaire"""
        if not isinstance(bit, Bit):
            raise TypeError(
                "%s n'est pas un Bit."%str(bit))
        self._code.append(bit)

    @property
    def bits(self):
        """getter de CodeBinaire. Retourne une liste."""
        return self._code

    def __len__(self):
        """Redéfinition de la méthode spéciale __len__"""
        return len(self.bits)

    def __getitem__(self, cle):
        """Redéfinition de la méthode spéciale __getitem__"""
        if isinstance(cle, int):
            return self.bits[cle]
        return CodeBinaire(*self.bits[cle])

    def __setitem__(self, cle, bit):
        """Redéfinition de la méthode spéciale __setitem__"""
        self._verification_type(cle, bit)
        if len(bit) == 0:
            raise AuMoinsUnBitError(
                "%s ne peut avoir moins de 1 bit. Suppression impossible."
                %str(self))
        self.bits[cle] = bit.bits if isinstance(bit, CodeBinaire) else bit

    @classmethod
    def _verification_type(cls, cle, bit):
        """Méthode privée de vérification de type pour lever un TypeError"""
        if isinstance(cle, slice):
            if not isinstance(bit, CodeBinaire):
                if isinstance(bit, list):
                    if not cls._verification_bit(bit):
                        raise TypeError(
                            "%s n'est pas composé de Bits."%str(bit))
                else:
                    raise TypeError(
                        "%s n'est pas une liste de Bits."%str(bit))
        else:
            if not isinstance(bit, Bit):
                raise TypeError(
                    "%s n'est pas un Bit."%str(bit))

    @classmethod
    def _verification_bit(cls, liste):
        """Méthode privée qui vérifie si une liste est composée de bits"""
        for element in liste:
            if not isinstance(element, Bit):
                return False
        return True

    def __delitem__(self, cle):
        """Redéfinition de la méthode spéciale __delitem__"""
        if len(self)-len(self.bits[cle]) < 1:
            raise AuMoinsUnBitError(
                "%s ne peut avoir moins de 1 bit. Suppression impossible."
                %str(self))
        del self.bits[cle]

    def __iter__(self):
        """Redéfinition de la méthode spéciale __iter__"""
        for cle in self.bits:
            yield cle

    def __eq__(self, autre):
        """Redéfinition de la méthode spéciale __eq__"""
        return self.bits == autre.bits

    def __hash__(self):
        """Redéfinition de la méthode spéciale __hash__"""
        return hash(tuple(self.bits))

    def __add__(self, autre):
        return CodeBinaire(*(self.bits+autre.bits))

    def __repr__(self):
        """Redéfinition de la méthode spéciale __repr__"""
        cdc = "%s(" %self.__class__.__name__
        for bit in self:
            cdc = cdc+"%s, " %repr(bit)
        return cdc[:-2]+")"

    def __str__(self, cdc=""):
        """Redéfinition de la méthode spéciale __str__"""
        for bit in self:
            cdc = cdc+"%s" %bit
        return cdc
