#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import os
from huffman import huffman
"""
Main du projet de compresseur de Huffman.
"""

parser = argparse.ArgumentParser(description='Huffman compressor')

parser.add_argument("-v","--verbose", help="affiche des informations lors des phases de compression et de décompression", action="store_true")
parser.add_argument("commande", choices=['c','d'], help="commande: c pour compression, d pour décompression")
parser.add_argument("nom_fichier_source", help="nom du fichier à compresser ou décompresser")
parser.add_argument("nom_fichier_destination", help="nom du fichier à créer")

args = parser.parse_args()

if args.verbose:
    def verboseprint(*args):
        """
        Print when verbose is True.
        """
        for arg in args:
            print(arg)
    #Could also be: verboseprint = print if verbose else lambda *a, **k: None
else:
    verboseprint = lambda *args: None #It's a do-nothing function

if os.path.isfile(args.nom_fichier_source):
    if not os.path.isfile(args.nom_fichier_destination):
        with open(args.nom_fichier_source, 'rb') as source:
            with open(args.nom_fichier_destination, 'wb') as destination:
                if args.commande == 'c':
                    for i in huffman.compresser(destination, source):
                        verboseprint(i)
                else:
                    for i in huffman.decompresser(destination, source):
                        verboseprint(i)
    else:
        raise FileExistsError("%s existe déjà. Impossible de l'écraser."%args.nom_fichier_destination)
else:
    raise FileNotFoundError("%s n'existe pas. Il ne peut pas être traité."%args.nom_fichier_source)
