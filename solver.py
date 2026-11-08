import random
from collections import deque
from cube2 import MOUVEMENTS2, RESOLU2, appliquer2, repeter2, melanger2,afficher2
from cube3 import MOUVEMENTS3, RESOLU3, appliquer3, repeter3, melanger3, afficher3

def inverse(mouv):
    if len(mouv) == 1:
        return mouv + "'"
    elif mouv[1] == "'":
        return mouv[0]
    else:
        return mouv

def reconstruire(dico,etat):
    chemin = []
    while dico[etat] != None:
        precedent, mouv = dico[etat]
        chemin.append(inverse(mouv))
        etat = precedent
    return chemin



def solver_bfs2(etat_actuelle):
    if (len(etat_actuelle) != 24) or (etat_actuelle.count(0) != 4) or (etat_actuelle.count(1) != 4) or (etat_actuelle.count(2) != 4) or (etat_actuelle.count(3) != 4) or (etat_actuelle.count(4) != 4) or (etat_actuelle.count(5) != 4):
        return "il y a une erreur dans ta liste"
    elif etat_actuelle == RESOLU2:
        return []
    etats = deque([RESOLU2])
    vus = {RESOLU2}
    parent = {RESOLU2: None}
    while etats:
        etat = etats.popleft()
        for nom, perm in MOUVEMENTS2.items():
            voisin = appliquer2(etat,nom)
            if voisin in vus:
                continue
            vus.add(voisin)
            parent[voisin] = (etat,nom)
            if voisin == etat_actuelle:
                return reconstruire(parent,voisin)
            etats.append(voisin)

def solver_bfs3(etat_actuelle):
    if (len(etat_actuelle) != 54) or (etat_actuelle.count(0) != 9) or (etat_actuelle.count(1) != 9) or (etat_actuelle.count(2) != 9) or (etat_actuelle.count(3) != 9) or (etat_actuelle.count(4) != 9) or (etat_actuelle.count(5) != 9):
        return "il y a une erreur dans ta liste"
    elif etat_actuelle == RESOLU3:
        return []
    etats = deque([RESOLU3])
    vus = {RESOLU3}
    parent = {RESOLU3: None}
    while etats:
        etat = etats.popleft()
        for nom, perm in MOUVEMENTS3.items():
            voisin = appliquer3(etat,nom)
            if voisin in vus:
                continue
            vus.add(voisin)
            parent[voisin] = (etat,nom)
            if voisin == etat_actuelle:
                return reconstruire(parent,voisin)
            etats.append(voisin)


"""
print("C'est un mélange à 6 mouvements sur un 2x2")
afficher2(melanger2(6,90)[0])
print(" ")
print(melanger2(6,90)[1])
print(" ")
print("Solution:")
print(solver_bfs2(melanger2(6,90)[0]))
"""
print("C'est un mélange à 6 mouvements sur un 3x3")
afficher3(melanger3(6,90)[0])
print(" ")
print(melanger3(6,90)[1])
print(" ")
print("Solution:")
print(solver_bfs3(melanger3(6,90)[0]))