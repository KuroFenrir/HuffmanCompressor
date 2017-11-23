#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Module concernant la compression et la décompression de Huffman
"""
import io
import sys
from .compteur import Compteur
from .file_de_priorite import FileDePriorite
from .code_binaire import Bit, CodeBinaire
from .arbre_huffman import ArbreHuffman

def statistiques(source: io.RawIOBase) -> (Compteur, int):
    """
    Fonction de calcul des statistiques dans le cadre de la compression de Huffman
    """
    compteur = Compteur()
    source.seek(0)
    octet = source.read(1)
    iterator = 0
    while octet:
        compteur.incrementer(octet)
        iterator += 1
        octet = source.read(1)
    return (compteur, iterator)

def arbre_de_huffman(stat: Compteur) -> ArbreHuffman:
    """
    Fonction de calcul de l'arbre de huffman dans le cadre de la compression de Huffman
    """
    def file_de_priorite(stat: Compteur) -> FileDePriorite:
        """
        Fonction qui transforme un compteur en file de priorité
        """
        fdp = FileDePriorite()
        for element in sorted(stat.elements):
            fdp.enfiler(ArbreHuffman(element=element, nb_occurrences=stat.nb_occurences(element)))
        return fdp

    def mise_a_jour_fdp(file):
        """
        Fonction qui met à jour la file de priorité
        """
        arbre = ArbreHuffman(fils_droit=file.defiler(), fils_gauche=file.defiler())
        file.enfiler(arbre)

    file = file_de_priorite(stat)
    while len(file) > 1:
        mise_a_jour_fdp(file)
    return file.defiler()

def code_binaire(arbre: ArbreHuffman) -> {int, CodeBinaire}:
    """
    Fonction de calcul du code bianire de chaque octet dans le cadre de la compression de Huffman
    """
    def table_codage(arbre: ArbreHuffman, table: {int, CodeBinaire}, code: CodeBinaire):
        """
        Fonction qui ressort un dictionnaire qui contient le code binaire pour chaque octet
        """
        if arbre.est_une_feuille:
            table[arbre.element] = code
        else:
            code_tmp0 = CodeBinaire(*code.bits)
            code_tmp1 = CodeBinaire(*code.bits)
            code_tmp0.ajouter(Bit.BIT_0)
            code_tmp1.ajouter(Bit.BIT_1)
            table_codage(arbre.fils_gauche, table, code_tmp0)
            table_codage(arbre.fils_droit, table, code_tmp1)

    table = {}
    if not arbre.est_une_feuille:
        table_codage(arbre.fils_gauche, table, CodeBinaire(Bit.BIT_0))
        table_codage(arbre.fils_droit, table, CodeBinaire(Bit.BIT_1))
    else:
        table[arbre.element] = Bit.BIT_0
    return table

def compresser(destination: io.RawIOBase, source: io.RawIOBase):
    """
    Fonction de compression suivant la méthode d'Huffman.
    """
    def list_to_byte(liste):
        """
        Fonction qui transforme une liste de bits(sous forme de naturel) en un octet.
        """
        i = 7
        temp = 0
        for bit in liste:
            temp = temp+bit*(2**i)
            i -= 1
        temp = int(temp).to_bytes(1, sys.byteorder)
        return temp

    def identifiant_write(identifiant: str):
        """
        Fonction prend un identifiant et l'écrit dans le flux de destination.
        """
        for char in identifiant:
            temp = ord(char).to_bytes(1, sys.byteorder)
            destination.write(temp)

    def longueur_write(longueur: int):
        """
        Fonction qui écrit la longueur des statistiques dans le flux destination.
        """
        longueur = longueur.to_bytes(4, sys.byteorder)
        destination.write(longueur)

    def stats_write_big_file(stats):
        """
        Fonction qui écrit chaque nombre d'occurences des statistiques dans le flux destination.
        """
        for i in range(256):
            temp_occur = stats.nb_occurences(
                i.to_bytes(1, sys.byteorder)
                ).to_bytes(4, sys.byteorder)
            destination.write(temp_occur)

    #def stats_write(stats):
    #    """
    #    Fonction qui écrit les statistiques dans le flux destination.
    #    """
    #    for key in stats.elements:
    #        temp_key = ord(key).to_bytes(1, sys.byteorder)
    #        destination.write(temp_key)
    #        temp_occur = stats.nb_occurences(key).to_bytes(4, sys.byteorder)
    #        destination.write(temp_occur)

    def code_write(stats):
        """
        Fonction qui écrit les octets compressés
        à partir de la table de codage dans le flux destination.
        """
        arbre = arbre_de_huffman(stats)
        table = code_binaire(arbre)
        source.seek(0)
        byte = source.read(1)
        temp_bit2 = []
        while byte:
            temp_bit = []
            temp_bit.extend(temp_bit2)
            temp_bit2 = []
            while byte and len(temp_bit) < 8:
                code = table[byte]
                for bit in code:
                    if len(temp_bit) < 8:
                        temp_bit.append(int(str(bit)))
                    else:
                        temp_bit2.append(int(str(bit)))
                byte = source.read(1)
            temp_bit = list_to_byte(temp_bit)
            destination.write(temp_bit)

    yield "Compression"
    (stats, longueur) = statistiques(source)
    identifiant = "HUFF"
    yield "Cas général"
    if longueur == 0:
        yield "Ecriture de l'identifiant"
        identifiant_write(identifiant)
        yield "Ecriture de la longueur"
        longueur_write(longueur)
        yield "Ecriture des statistiques"
        stats_write_big_file(stats)
    else:
        yield "Ecriture de l'identifiant"
        identifiant_write(identifiant)
        yield "Ecriture de la longueur"
        longueur_write(longueur)
        yield "Ecriture des statistiques"
        stats_write_big_file(stats)
        yield "Ecriture des octets"
        code_write(stats)
    yield "Création du fichier compressé"

def decompresser(destination: io.RawIOBase, source: io.RawIOBase):
    """
    Fonction qui permet la décompression selon la méthode de Huffman.
    """
    def naturel_to_list(naturel):
        """
        Fonction qui permet de passer d'un naturel à une liste de Bit.
        """
        liste = []
        while naturel != 0:
            liste.append(Bit.BIT_0 if naturel%2 == 0 else Bit.BIT_1)
            naturel = naturel // 2
        if len(liste) < 8:
            liste += [Bit.BIT_0 for i in range(8-len(liste))]
        liste.reverse()
        return liste

    def recherche_identifiant():
        """
        Fonction qui recherche l'identifiant du flux source.
        """
        identifiant = ""
        for i in range(4):
            identifiant = identifiant + chr(int.from_bytes(source.read(1), sys.byteorder))
        return identifiant

    def recherche_stats():
        """
        Fonction qui recherche les nombres d'occurences des 256 octets dans le flux source.
        """
        stat = Compteur()
        for i in range(256):
            occurence = int.from_bytes(source.read(4), sys.byteorder)
            if occurence > 0:
                stat.fixer(i.to_bytes(1, sys.byteorder), occurence)
        return stat

    def reconstruction():
        """
        Fonction qui reconstruit le contenu du flux source
        avant compression à partir de l'arbre obtenu des statistiques.
        """
        octet = source.read(1)
        arbre_courant = arbre
        longueur_courante = 0
        while longueur_courante < longueur and octet:
            liste_bits = naturel_to_list(int.from_bytes(octet, sys.byteorder))
            for i in liste_bits:
                if arbre_courant.est_une_feuille:
                    destination.write(arbre_courant.element)
                    arbre_courant = arbre
                    longueur_courante += 1
                if i == Bit.BIT_0:
                    arbre_courant = arbre_courant.fils_gauche
                else:
                    arbre_courant = arbre_courant.fils_droit
            octet = source.read(1)

    yield "Décompression"
    source.seek(0)
    yield "Cas général"
    identifiant = recherche_identifiant()
    if identifiant == "HUFF":
        longueur = int.from_bytes(source.read(4), sys.byteorder)
        yield "Lecture des stats"
        stat = recherche_stats()
        yield "Création de l'arbre de Huffman"
        arbre = arbre_de_huffman(stat)
        yield "Création du fichier decompressé"
        reconstruction()

if __name__ == "__main__":
    F = io.StringIO("azzeeerrrrttttt")
    (STAT, I) = statistiques(F)
    ARBRE = arbre_de_huffman(STAT)
    TABLE = code_binaire(ARBRE)
    print(TABLE)
    with open('source.txt', 'rb') as g:
        with open('test.txt', 'wb') as f:
            compresser(f, g)
    with open('test2.txt', 'wb') as g:
        with open('test.txt', 'rb') as f:
            decompresser(g, f)
