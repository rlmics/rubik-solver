import random
from collections import deque
from cube2 import MOUVEMENTS2, RESOLU2, appliquer2, repeter2, melanger2,afficher2

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



def solver_bfs(etat_actuelle):
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



print("C'est un mélange à 10 mouvements")
afficher2(melanger2(10,90)[0])
print(" ")
print(melanger2(12,90)[1])
print(" ")
print("Solution:")
print(solver_bfs(melanger2(10,90)[0]))