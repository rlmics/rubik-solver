import random
from cube2 import MOUVEMENTS2, RESOLU2, appliquer2, repeter2, raccourci, est_resolu2
from cfop import auf
from collections import deque
from solver import reconstruire_fin

#Dictionnaire algo
Algorithme2 = {
    #Mouvement important
    "SEXYMOVE":     [("R","U","R'","U'"),6,[]],
    "REVERSE-SEXYMOVE": [("U","R","U'","R'"),6,[]],


    #derniere face
    "OLL_SUNE":         [("R","U","R'","U","R","U2","R'"),6,[]],                                                   #1 sticker bien place   (droite)
    "OLL_ANTI-SUNE":    [("R","U2","R'","U'","R","U'","R'"),6,[]],                                                 #1 sticker bien place   (gauche)
    "OLL_CORNER":       [("F","R","U'","R'","U'","R","U","R'","F'"),4,[]],                                         #2 stickers bien places (corner)
    "OLL_BARRE":        [("R","U","R'","U'","R'","F","R","F'"),3,[]],                                              #2 stickers bien places (1 barre + 0 barre exterieure)
    "OLL_HEADLIGHTS":   [("F","R","U","R'","U'","F'"),6,[]],                                                       #2 stickers bien places (1 barre + 1 barre exterieure)
    "OLL_T":            [("R","U2","R2","U'","R2","U'","R2","U2","R"),2,[]],                                       #0 sticker bien place   (0 barre + 1 barre exterieure)
    "OLL_DOUBLE-SUNE":  [("R","U2","R'","U'","R","U","R'","U'","R","U'","R'"),3,[]],                               #0 sticker bien place   (0 barre + 2 barre exterieure)

    #Derniere etape
    "PLL_T-PERM":       [("R","U","R'","U'","R'","F","R2","U'","R'","U'","R","U","R'","F'"),2,[]],                 #4 barres basses correctes & 1 barre haute correcte
    "PLL_J-PERM":       [("F","R","U'","R'","U'","R","U","R'","F'","R","U","R'","U'","R'","F","R","F'"),2,[]],     #4 barres basses correctes & 0 barre haute correcte
    
    #ortega
    "ortega_COUPLE":       [("R2","U'","B2","U2","R2","U'","R2"),2,[[1,1]]],                                       #1 barre basse correct     & 1 barre haute correcte
    "ortega_LONELY":       [("R","U'","R","F2","R'","U","R'"),2,[[1,0],[0,1]]],                                    #0 barre basse correcte    & 1 barre haute correcte
    "ortega_VOID":         [("R2","F2","R2"),2,[[0,0]]],                                                           #0 barre basse correcte    & 0 barre haute correcte
}

def PLL2(etat_actuelle):
    if (len(etat_actuelle) == 8):
        etat_initial = RESOLU2[0:4]+etat_actuelle[0:2]+RESOLU2[6:8]+etat_actuelle[2:4]+RESOLU2[10:12]+etat_actuelle[4:6]+RESOLU2[14:16]+etat_actuelle[6:]+RESOLU2[18:]
    elif (len(etat_actuelle) == 24):
        etat_initial = etat_actuelle
    else:
        return "euhhhhh comment dire... t'as fais une erreur d'entrée"
    for k in range(4):
        if est_resolu2(repeter2(etat_initial, "U", k)):
            return ("U",)*k
    if len(set(etat_initial[4:6])) == 1 and len(set(etat_initial[8:10])) == 1:
        etat_initial = appliquer2(etat_initial,"z2")
        mouv = ("z2",)
    else:
        mouv = ()
    etat = etat_initial
    trouve = False
    for nom, (mouvements, poids,liste) in Algorithme2.items():
        indice_start = 0
        indice_stop = 0
        if not nom.startswith("PLL_"):
            continue
        for i in range(4):
            indice_stop = 0
            etat = repeter2(etat,"U",i)
            for n in mouvements:
                etat = appliquer2(etat,n)
            etat_transfo = etat
            for j in range(4):
                if est_resolu2(repeter2(etat,"U",j)):
                    trouve = True
                    break
                else:
                    indice_stop += 1
                    etat = etat_transfo
            if trouve:
                break
            else:
                indice_start += 1
                etat = etat_initial
        if trouve:
            break

    return mouv + auf(indice_start) + mouvements + auf(indice_stop) if trouve else "chef... t'as fais une erreur quelque part"

def OLL2(etat_actuelle):
    if (len(etat_actuelle) == 12):
        etat_initial =etat_actuelle[0:6]+RESOLU2[6:8]+etat_actuelle[6:8]+RESOLU2[10:12]+etat_actuelle[8:10]+RESOLU2[14:16]+etat_actuelle[10:]+RESOLU2[18:]
    elif (len(etat_actuelle) == 24):
        etat_initial = etat_actuelle
    else:
        return "euhhhhh comment dire... t'as fais une erreur d'entree"
    if etat_initial[0:4] == (0,0,0,0):
        return ()
    etat = etat_initial
    trouve = False
    for nom, (mouvements, poids,liste) in Algorithme2.items():
        indice_i = 0
        if not nom.startswith("OLL_"):
            continue

        for i in range (4):
            etat = repeter2(etat,"U",i)   
            for n in mouvements:
                etat = appliquer2(etat,n)
            if etat[0:4] == (0,0,0,0):
                trouve = True
                break
            else:
                etat = etat_initial
                indice_i += 1
        if trouve:
            break
    return auf(indice_i) + mouvements if trouve else "chef... C'est juste impossible"

def lastlayer_fop(etat_actuelle):
    if len(etat_actuelle) != 24:
        return "il me faut l'état complet"
    etat = etat_actuelle
    etat_initial= etat
    mouv = ()
    if type(OLL2(etat_actuelle)) is str:
        return "mhhh tu t'es trompe"
    for n in OLL2(etat_actuelle):
        etat = appliquer2(etat,n)
    mouv += OLL2(etat_initial)
    etat_transfo = etat
    if type(PLL2(etat_transfo)) is str:
        return "mhhh tu t'es trompe"
    mouv += PLL2(etat_transfo)
    return mouv

def firstlayer_fop(etat_actuelle):
    if ((len(etat_actuelle) != 24) 
        or (etat_actuelle.count(0) != 4) 
        or (etat_actuelle.count(1) != 4) 
        or (etat_actuelle.count(2) != 4) 
        or (etat_actuelle.count(3) != 4) 
        or (etat_actuelle.count(4) != 4) 
        or (etat_actuelle.count(5) != 4)):
        return "il y a une erreur dans ta liste"
    elif etat_actuelle == RESOLU2:
        return []
    etats = deque([etat_actuelle])
    vus = {etat_actuelle}
    parent = {etat_actuelle: None}
    while etats:
        etat = etats.popleft()
        for nom, perm in MOUVEMENTS2.items():
            voisin = appliquer2(etat,nom)
            if voisin in vus:
                continue
            vus.add(voisin)
            parent[voisin] = (etat,nom)
            if len(set(voisin[20:24])) == 1:
                return reconstruire_fin(parent,voisin)
            etats.append(voisin)

def ortega(etat_actuelle):
    if (len(etat_actuelle) == 16):
        etat_initial = RESOLU2[0:4] + etat_actuelle + RESOLU2[20:]
    elif (len(etat_actuelle) == 24):
        etat_initial = etat_actuelle
    else:
        return "i"
    if ((len(set(etat_initial[4:6])) == 1
        and len(set(etat_initial[8:10])) == 1
        and len(set(etat_initial[12:14])) == 1
        and len(set(etat_initial[16:18])) == 1)
        or
        (len(set(etat_initial[6:8])) == 1
        and len(set(etat_initial[10:12])) == 1
        and len(set(etat_initial[14:16])) == 1
        and len(set(etat_initial[18:20])) == 1)):
        return PLL2(etat_initial)
    elif (len(set(etat_initial[0:4])) != 1 
        or len(set(etat_initial[20:24])) != 1
        ):
        return "a"
    barre = [0,0]
    for i in range(2):
        for j in range(4):
            etat_initial = appliquer2(etat_initial, "y")
            if len(set(etat_initial[4 + 2*i :6 + 2*i])) == 1:
                barre[i] += 1
    etat = etat_initial
    mouv = ()
    rota = 0
    rota_bas = 0
    trouve = False
    if barre[0]:
        while not len(set(etat[4:6])) == 1:
            etat = appliquer2(etat,"y")
            rota += 1
    if rota != 0: mouv += (raccourci("y",rota),)
    if barre[1]:
        while not len(set(etat[6:8])) == 1:
            etat = appliquer2(etat,"D'")
            rota_bas += 1
    if rota_bas != 0: mouv += (raccourci("D'",rota_bas),)
    for nom, (mouvements,poids,liste) in Algorithme2.items():
        if not nom.startswith("ortega_"):
            continue
        if not barre in liste:
            continue
        etat_initial = etat
        for i in range(2):
            etat = etat_initial
            etat = repeter2(etat,"z2",i)
            for n in mouvements:
                etat = appliquer2(etat,n)
            for k in range(4):
                if est_resolu2(etat):
                    trouve = True
                    if i > 0: mouv += ("z2",)
                    mouv += mouvements
                    if k > 0: mouv+= (raccourci("U",k),)
                    break
                etat = appliquer2(etat,"U")
            if trouve:
                break
        if trouve:
            break
        
    return mouv if trouve else "e"


def melanger_OLL2(n,seed):
    etat = RESOLU2
    mouv_oll = []
    for nom, (mouvements,poids,liste) in Algorithme2.items():
        if not nom.startswith("OLL_"):
            continue
        else:
            mouv_oll.append(mouvements)
    mouv=[]
    rng = random.Random(seed)
    for _ in range(n):
        nom = rng.choice(list(mouv_oll))
        auf = rng.randrange(4)
        etat = repeter2(etat, "U",auf)
        for m in nom:
            etat = appliquer2(etat,m)
        mouv.append(nom)
    res = [etat,mouv]
    return res

def melanger_PLL2(n,seed):
    etat = RESOLU2
    mouv_pll = []
    for nom, (mouvements,poids,liste) in Algorithme2.items():
        if not nom.startswith("PLL_"):
            continue
        else:
            mouv_pll.append(mouvements)
    mouv=[]
    rng = random.Random(seed)
    for _ in range(n):
        nom = rng.choice(list(mouv_pll))
        auf = rng.randrange(4)
        etat = repeter2(etat,"U",auf)
        for m in nom:
            etat = appliquer2(etat,m)
        mouv.append(nom)
    res = [etat,mouv]
    return res

def melanger_ortega(n,seed):
    etat = RESOLU2
    mouv_pll = []
    for nom, (mouvements,poids,liste) in Algorithme2.items():
        if not nom.startswith("ortega_"):
            continue
        else:
            mouv_pll.append(mouvements)
    mouv=[]
    rng = random.Random(seed)
    for _ in range(n):
        nom = rng.choice(list(mouv_pll))
        auf = rng.randrange(4)
        etat = repeter2(etat,rng.choice(["U","D"]),auf)
        for m in nom:
            etat = appliquer2(etat,m)
        mouv.append(nom)
    res = [etat,mouv]
    return res
