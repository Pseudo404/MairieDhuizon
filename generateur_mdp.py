"""Création des mots de passes sécurisé pour les comptes administrateurs de la Mairie"""

from random import *

def generateur_mdp():
    alphabet_min = "abcdefghijklmnopqrstuvwxyz"
    alphabet_maj = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    caracteres_speciaux = "0123456789!@#$%^&*()"
    mdp = ""
    for i in range(24):
        mdp += choice([choice(alphabet_min), choice(alphabet_maj), choice(caracteres_speciaux)])
    return mdp

print(generateur_mdp())