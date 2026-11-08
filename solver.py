import random
from collections import deque
from cube2 import MOUVEMENTS2, RESOLU2, appliquer2, repeter2, melanger2

def inverse(caracter):
    if len(caracter) == 1:
        return caracter + "'"
    elif caracter[1] == "'":
        return caracter[0]
    else:
        return caracter

def reconstruire(dico,etat):
    chemin = []
    while dico[etat] != None:
        precedent, mouv = dico[etat]
        chemin.append(mouv)
        etat = precedent
    chemin.reverse()
    solut = ()
    for n in chemin:
        solut += inverse(n)
    return solut



def solver_bfs(etat_actuelle):
    if (len(etat_actuelle) != 24) or (etat_actuelle.count(0) != 4) or (etat_actuelle.count(1) != 4) or (etat_actuelle.count(2) != 4) or (etat_actuelle.count(3) != 4) or (etat_actuelle.count(4) != 4) or (etat_actuelle.count(5) != 4):
        return "il y a une erreur dans ta liste"
    elif etat_actuelle == RESOLU2:
        return ()
    etats = deque(RESOLU2)
    vus = {RESOLU2}
    parent = {RESOLU2: None}
    while etats:
        etat = etats.popleft()
        for nom, perm in MOUVEMENTS2.items():
            voisin = appliquer2(etat_actuelle,nom)
            if voisin in vus:
                continue
            vus.add(voisin)
            parent[voisin] = (etat,nom)
        if voisin == RESOLU2:
            return reconstruire(parent,voisin)
        etats.append(voisin)
