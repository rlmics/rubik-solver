import random
from collections import deque
from cube3 import MOUVEMENTS3, RESOLU3, appliquer3, repeter3, est_resolu3, cross, ROTATIONS, melanger3
from solver import inverse, reconstruire_fin

#Dictionnaire algo
ALGORITHMES3 = {

    # ---------------- F2L (slot avant-droite) ---------------- [0:42]
    # "jaune" = sticker de la couleur du bas, "verte" = sticker vert de l'arête vert/rouge

    # Section 1A : Les 2 pièces en haut - sticker du bas vers le haut
    "F2L_1A_HAUT_1":        [("R","U'","R'","U2","R","U","R'"),2],  # coin UFR (jaune: haut), arête UL (verte: haut)  | PDF : U2 (R U R') U (R U' R')
    "F2L_1A_HAUT_2":        [("U2","R","U","R'","F'","U'","F"),5],  # coin UFR (jaune: haut), arête UB (verte: arrière)  | PDF : y U2 (L' U' L) U' (L' U L)
    "F2L_1A_HAUT_3":        [("U","R","U2","R2","F","R","F'"),8],  # coin UFR (jaune: haut), arête UB (verte: haut)  | PDF : U (R U2 R') U (R U' R')
    "F2L_1A_HAUT_4":        [("U'","F'","U2","F2","R'","F'","R"),8],  # coin UFR (jaune: haut), arête UL (verte: gauche)  | PDF : y U' (L' U2 L) U' (L' U L)
    "F2L_1A_HAUT_5":        [("U2","R2","U2","R'","U'","R","U'","R2"),5],  # coin UFR (jaune: haut), arête UF (verte: haut)  | PDF : U (R U' R') U' (R U' R' U R U' R')
    "F2L_1A_HAUT_6":        [("U2","F2","U2","F","U","F'","U","F2"),5],  # coin UFR (jaune: haut), arête UR (verte: droite)  | PDF : y U' (L' U L) U (L' U L U' L' U L)
    "F2L_1A_HAUT_7":        [("R","U2","R'","U'","R","U","R'"),5],  # coin UFR (jaune: haut), arête UR (verte: haut)  | PDF : (R U2 R') U' (R U R')
    "F2L_1A_HAUT_8":        [("F'","U2","F","U","F'","U'","F"),5],  # coin UFR (jaune: haut), arête UF (verte: avant)  | PDF : y (L' U2 L) U (L' U' L)

    # Section 1A : Les 2 pièces en haut - sticker du bas sur le côté/devant, stickers du dessus différents
    "F2L_1A_COTE_DIFF_1":   [("R","U","R'"),4],  # coin UFR (jaune: droite), arête UB (verte: haut)  | PDF : (R U R')
    "F2L_1A_COTE_DIFF_2":   [("F'","U'","F"),4],  # coin UFR (jaune: avant), arête UL (verte: gauche)  | PDF : y (L' U' L)
    "F2L_1A_COTE_DIFF_3":   [("U'","R","U","R'","U","R","U","R'"),30],  # coin UFR (jaune: droite), arête UL (verte: haut)  | PDF : U' (R U R') U (R U R')
    "F2L_1A_COTE_DIFF_4":   [("U'","R","U'","R'","U","F'","U'","F"),20],  # coin UFR (jaune: avant), arête UB (verte: arrière)  | PDF : y U (L' U' L) U' (L' U' L)
    "F2L_1A_COTE_DIFF_5":   [("R'","U2","R2","U","R2","U","R"),15],  # coin UFR (jaune: droite), arête UF (verte: haut)  | PDF : R' U2 R2 U R2' U R
    "F2L_1A_COTE_DIFF_6":   [("F","U2","F2","U'","F2","U'","F'"),15],  # coin UFR (jaune: avant), arête UR (verte: droite)  | PDF : y L U2 L2' U' L2 U' L'
    "F2L_1A_COTE_DIFF_7":   [("U'","R","U'","R'","U","R","U","R'"),10],  # coin UFR (jaune: droite), arête UR (verte: haut)  | PDF : U' (R U' R') U (R U R')
    "F2L_1A_COTE_DIFF_8":   [("R","U","R2","F","R","F2","U'","F"),30],  # coin UFR (jaune: avant), arête UF (verte: avant)  | PDF : y U (L' U L) U' (L' U' L)

    # Section 1A : Les 2 pièces en haut - sticker du bas sur le côté/devant, stickers du dessus identiques
    "F2L_1A_COTE_MEME_1":   [("F","R'","F'","R"),6],  # coin UFR (jaune: droite), arête UF (verte: avant)  | PDF : y U' (L' U L)
    "F2L_1A_COTE_MEME_2":   [("U","R","U'","R'"),6],  # coin UFR (jaune: avant), arête UR (verte: haut)  | PDF : U (R U' R')
    "F2L_1A_COTE_MEME_3":   [("R2","U2","F","R2","F'","U2","R2"),2],  # coin UFR (jaune: droite), arête UB (verte: arrière)  | PDF : y U (L' U2 L) U2 (L' U L)
    "F2L_1A_COTE_MEME_4":   [("F2","U2","R'","F2","R","U2","F2"),2],  # coin UFR (jaune: avant), arête UL (verte: haut)  | PDF : U' (R U2 R') U2 (R U' R')
    "F2L_1A_COTE_MEME_5":   [("U'","R","U","R'","U'","R","U2","R'"),12],  # coin UFR (jaune: avant), arête UB (verte: haut)  | PDF : U' (R U R') U2 (R U' R')
    "F2L_1A_COTE_MEME_6":   [("R'","U'","R","F","R'","F'","U","R"),6],  # coin UFR (jaune: droite), arête UL (verte: gauche)  | PDF : y U (L' U' L) U2 (L' U L)
    "F2L_1A_COTE_MEME_7":   [("F'","U","F","U2","R","U","R'"),6],  # coin UFR (jaune: avant), arête UF (verte: haut)  | PDF : M U (L F' L') U' M'
    "F2L_1A_COTE_MEME_8":   [("R","U'","R'","U2","F'","U'","F"),6],  # coin UFR (jaune: droite), arête UR (verte: droite)  | PDF : y M U' (R' F R) U M'

    # Section 1B : 1 pièce dans le slot - arête dans le slot
    "F2L_1B_ARETE_1":       [("U","R","U","R'","U2","R","U","R'"),4],  # coin UFR (jaune: droite), arête dans le slot (verte: avant)  | PDF : U (R U R') U2 (R U R')
    "F2L_1B_ARETE_2":       [("U'","R","U'","R'","U'","R","U2","R'"),4],  # coin UFR (jaune: avant), arête dans le slot (verte: avant)  | PDF : y U' (L' U' L) U2 (L' U' L)
    "F2L_1B_ARETE_3":       [("U","F'","U'","F","U'","R","U","R'"),6],  # coin UFR (jaune: droite), arête dans le slot (verte: droite)  | PDF : U (F' U' F) U' (R U R')
    "F2L_1B_ARETE_4":       [("U'","R","U","R'","U","F'","U'","F"),6],  # coin UFR (jaune: avant), arête dans le slot (verte: droite)  | PDF : y U' (F U F') U (L' U' L)
    "F2L_1B_ARETE_5":       [("R2","U","R2","U","R2","U2","R2"),15],  # coin UFR (jaune: haut), arête dans le slot (verte: avant)  | PDF : (U R U' R')3
    "F2L_1B_ARETE_6":       [("F'","U","F","R","U2","R'"),72],  # coin UFR (jaune: haut), arête dans le slot (verte: droite)  | PDF : U' (R' F R F') (R U' R')

    # Section 1B : 1 pièce dans le slot - coin dans le slot
    "F2L_1B_COIN_1":        [("U","F'","U","F","R","U","R'"),12],  # coin dans le slot (jaune: droite), arête UF (verte: haut)  | PDF : (R U R') U' (R U R')
    "F2L_1B_COIN_2":        [("U2","R","U'","R'","F'","U'","F"),45],  # coin dans le slot (jaune: avant), arête UF (verte: avant)  | PDF : y (L' U' L) U (L' U' L)
    "F2L_1B_COIN_3":        [("U'","R","U'","R2","F","R","F'"),45],  # coin dans le slot (jaune: avant), arête UF (verte: haut)  | PDF : (R U' R') U (R U' R')
    "F2L_1B_COIN_4":        [("R","U2","R'","F'","U2","F"),15],  # coin dans le slot (jaune: droite), arête UF (verte: avant)  | PDF : y (L' U L) U' (L' U L)
    "F2L_1B_COIN_5":        [("F'","U2","F","U2","R","U","R'"),4],  # coin dans le slot (jaune: bas), arête UF (verte: haut)  | PDF : U' (R' F R F') (R U R')
    "F2L_1B_COIN_6":        [("R'","U'","R","F'","R'","U","R","F"),3],  # coin dans le slot (jaune: bas), arête UF (verte: avant)  | PDF : y U (L F' L' F) (L' U' L)

    # Section 1C : Les 2 pièces dans le bon slot
    "F2L_1C_SLOT_1":        [("R","U2","R","U","R'","U","R","U2","R2"),3],  # coin dans le slot (jaune: droite), arête dans le slot (verte: avant)  | PDF : (R U' R') U (R U2 R' U R U' R')
    "F2L_1C_SLOT_2":        [("R2","U2","R'","U'","R","U'","R'","U2","R'"),3],  # coin dans le slot (jaune: avant), arête dans le slot (verte: avant)  | PDF : (R U' R') U' (R U R' U2 R U' R')
    "F2L_1C_SLOT_3":        [("R","U","F","R","U","R'","U'","F'","R'"),12],  # coin dans le slot (jaune: droite), arête dans le slot (verte: droite)  | PDF : (R U' R') (F' L' U2 L F)
    "F2L_1C_SLOT_4":        [("R","F","U","R","U'","R'","F'","U'","R'"),12],  # coin dans le slot (jaune: avant), arête dans le slot (verte: droite)  | PDF : y (L' U L) (F R U2 R' F')
    "F2L_1C_SLOT_5":        [("R","U'","R","U2","F","R2","F'","U2","R2"),24],  # coin dans le slot (jaune: bas), arête dans le slot (verte: droite)  | PDF : R2 U2 F R2 F' U2 R' U R'

    # ---------------- OLL ---------------- [42:100]
    "OLL_1":  [("R","U2","R2","F","R","F'","U2","R'","F","R","F'"),18],  # Point - 0 bords et 0 coins orientés
    "OLL_2":  [("F","R","U","R'","U'","F'","f","R","U","R'","U'","f'"),6],  # Point - 0 bords et 0 coins orientés
    "OLL_3":  [("f","R","U","R'","U'","f'","U'","F","R","U","R'","U'","F'"),4],  # Point - 0 bords et 1 coins orientés
    "OLL_4":  [("f","R","U","R'","U'","f'","U","F","R","U","R'","U'","F'"),4],  # Point - 0 bords et 1 coins orientés
    "OLL_5":  [("r'","U2","R","U","R'","U","r"),6],  # Carré - 2 bords et 1 coins orientés
    "OLL_6":  [("r","U2","R'","U'","R","U'","r'"),6],  # Carré - 2 bords et 1 coins orientés
    "OLL_7":  [("r","U","R'","U","R","U2","r'"),6],  # Petit éclair - 2 bords et 1 coins orientés
    "OLL_8":  [("r'","U'","R","U'","R'","U2","r"),6],  # Petit éclair - 2 bords et 1 coins orientés
    "OLL_9":  [("R","U","R'","U'","R'","F","R2","U","R'","U'","F'"),9],  # Poisson - 2 bords et 1 coins orientés
    "OLL_10": [("R","U","R'","U","R'","F","R","F'","R","U2","R'"),6],  # Poisson - 2 bords et 1 coins orientés
    "OLL_11": [("r","U","R'","U","R'","F","R","F'","R","U2","r'"),6],  # Petit éclair - 2 bords et 1 coins orientés
    "OLL_12": [("F","R","U","R'","U'","F'","U","F","R","U","R'","U'","F'"),4],  # Petit éclair - 2 bords et 1 coins orientés
    "OLL_13": [("F","U","R","U2","R'","U'","R","U","R'","F'"),4],  # Cavalier - 2 bords et 1 coins orientés
    "OLL_14": [("R'","F","R","U","R'","F'","R","F","U'","F'"),3],  # Cavalier - 2 bords et 1 coins orientés
    "OLL_15": [("r'","U'","r","R'","U'","R","U","r'","U","r"),6],  # Cavalier - 2 bords et 1 coins orientés
    "OLL_16": [("r","U","r'","R","U","R'","U'","r","U'","r'"),6],  # Cavalier - 2 bords et 1 coins orientés
    "OLL_17": [("R","U","R'","U","R'","F","R","F'","U2","R'","F","R","F'"),18],  # Point - 0 bords et 2 coins orientés
    "OLL_18": [("r","U","R'","U","R","U2","r2","U'","R","U'","R'","U2","r"),6],  # Point - 0 bords et 2 coins orientés
    "OLL_19": [("M","U","R","U","R'","U'","M'","R'","F","R","F'"),12],  # Point - 0 bords et 2 coins orientés
    "OLL_20": [("M","U","R","U","R'","U'","M2","U","R","U'","r'"),4],  # Point - 0 bords et 4 coins orientés
    "OLL_21": [("R","U2","R'","U'","R","U","R'","U'","R","U'","R'"),3],  # H - 4 bords et 0 coins orientés
    "OLL_22": [("R","U2","R2","U'","R2","U'","R2","U2","R"),6],  # Pi - 4 bords et 0 coins orientés
    "OLL_23": [("R2","D","R'","U2","R","D'","R'","U2","R'"),3],  # Headlights - 4 bords et 2 coins orientés
    "OLL_24": [("r","U","R'","U'","r'","F","R","F'"),3],  # Chameleon - 4 bords et 2 coins orientés
    "OLL_25": [("F'","r","U","R'","U'","r'","F","R"),3],  # Bowtie - 4 bords et 2 coins orientés
    "OLL_26": [("R","U2","R'","U'","R","U'","R'"),6],  # Antisune - 4 bords et 1 coins orientés
    "OLL_27": [("R","U","R'","U","R","U2","R'"),6],  # Sune - 4 bords et 1 coins orientés
    "OLL_28": [("r","U","R'","U'","r'","R","U","R","U'","R'"),3],  # Stealth - 2 bords et 4 coins orientés
    "OLL_29": [("R","U","R'","U'","R","U'","R'","F'","U'","F","R","U","R'"),4],  # Awkward - 2 bords et 2 coins orientés
    "OLL_30": [("F","R'","F","R2","U'","R'","U'","R","U","R'","F2"),4],  # Awkward - 2 bords et 2 coins orientés
    "OLL_31": [("R'","U'","F","U","R","U'","R'","F'","R"),12],  # P - 2 bords et 2 coins orientés
    "OLL_32": [("R","U","B'","U'","R'","U","R","B","R'"),12],  # P - 2 bords et 2 coins orientés
    "OLL_33": [("R","U","R'","U'","R'","F","R","F'"),3],  # T - 2 bords et 2 coins orientés
    "OLL_34": [("R","U","R2","U'","R'","F","R","U","R","U'","F'"),3],  # C - 2 bords et 2 coins orientés
    "OLL_35": [("R","U2","R2","F","R","F'","R","U2","R'"),6],  # Poisson - 2 bords et 2 coins orientés
    "OLL_36": [("R'","U'","R","U'","R'","U","R","U","R","B'","R'","B"),6],  # W - 2 bords et 2 coins orientés
    "OLL_37": [("F","R'","F'","R","U","R","U'","R'"),3],  # Poisson - 2 bords et 2 coins orientés
    "OLL_38": [("R","U","R'","U","R","U'","R'","U'","R'","F","R","F'"),6],  # W - 2 bords et 2 coins orientés
    "OLL_39": [("L","F'","L'","U'","L","U","F","U'","L'"),12],  # Grand éclair - 2 bords et 2 coins orientés
    "OLL_40": [("R'","F","R","U","R'","U'","F'","U","R"),12],  # Grand éclair - 2 bords et 2 coins orientés
    "OLL_41": [("R","U","R'","U","R","U2","R'","F","R","U","R'","U'","F'"),6],  # Awkward - 2 bords et 2 coins orientés
    "OLL_42": [("R'","U'","R","U'","R'","U2","R","F","R","U","R'","U'","F'"),6],  # Awkward - 2 bords et 2 coins orientés
    "OLL_43": [("R'","U'","F'","U","F","R"),6],  # P - 2 bords et 2 coins orientés
    "OLL_44": [("f","R","U","R'","U'","f'"),6],  # P - 2 bords et 2 coins orientés
    "OLL_45": [("F","R","U","R'","U'","F'"),6],  # T - 2 bords et 2 coins orientés
    "OLL_46": [("R'","U'","R'","F","R","F'","U","R"),6],  # C - 2 bords et 2 coins orientés
    "OLL_47": [("R'","U'","R'","F","R","F'","R'","F","R","F'","U","R"),3],  # L - 2 bords et 0 coins orientés
    "OLL_48": [("F","R","U","R'","U'","R","U","R'","U'","F'"),3],  # L - 2 bords et 0 coins orientés
    "OLL_49": [("r","U'","r2","U","r2","U","r2","U'","r"),6],  # L - 2 bords et 0 coins orientés
    "OLL_50": [("r'","U","r2","U'","r2","U'","r2","U","r'"),6],  # L - 2 bords et 0 coins orientés
    "OLL_51": [("f","R","U","R'","U'","R","U","R'","U'","f'"),3],  # Ligne (I) - 2 bords et 0 coins orientés
    "OLL_52": [("R'","F'","U'","F","U'","R","U","R'","U","R"),6],  # Ligne (I) - 2 bords et 0 coins orientés
    "OLL_53": [("r'","U'","R","U'","R'","U","R","U'","R'","U2","r"),3],  # L - 2 bords et 0 coins orientés
    "OLL_54": [("r","U","R'","U","R","U'","R'","U","R","U2","r'"),3],  # L - 2 bords et 0 coins orientés
    "OLL_55": [("R","U2","R2","U'","R","U'","R'","U2","F","R","F'"),18],  # Ligne (I) - 2 bords et 0 coins orientés
    "OLL_56": [("F","R","U","R'","U'","R","F'","r","U","R'","U'","r'"),9],  # Ligne (I) - 2 bords et 0 coins orientés
    "OLL_57": [("R","U","R'","U'","M'","U","R","U'","r'"),3],  # Ligne + 4 coins - 2 bords et 4 coins orientés

    # ---------------- PLL ---------------- [100:]
    "PLL_Aa": [("R'","F","R'","B2","R","F'","R'","B2","R2"),3],
    "PLL_Ab": [("R2","B2","R","F","R'","B2","R","F'","R"),3],
    "PLL_E":  [("R","B'","R'","F","R","B","R'","F'","R","B","R'","F","R","B'","R'","F'"),2],
    "PLL_F":  [("R'","U'","F'","R","U","R'","U'","R'","F","R2","U'","R'","U'","R","U","R'","U","R"),2],
    "PLL_Ga": [("R2","U","R'","U","R'","U'","R","U'","R2","U'","D","R'","U","R","D'"),4],
    "PLL_Gb": [("R'","U'","R","U","D'","R2","U","R'","U","R","U'","R","U'","R2","D"),4],
    "PLL_Gc": [("R2","U'","R","U'","R","U","R'","U","R2","U","D'","R","U'","R'","D"),4],
    "PLL_Gd": [("R","U","R'","U'","D","R2","U'","R","U'","R'","U","R'","U","R2","D'"),4],
    "PLL_H":  [("M2","U","M2","U2","M2","U","M2"),2],
    "PLL_Ja": [("R'","U","L'","U2","R","U'","R'","U2","R","L"),3],
    "PLL_Jb": [("R","U","R'","F'","R","U","R'","U'","R'","F","R2","U'","R'"),3],
    "PLL_Na": [("R","U","R'","U","R","U","R'","F'","R","U","R'","U'","R'","F","R2","U'","R'","U2","R","U'","R'"),2],
    "PLL_Nb": [("R'","U","R","U'","R'","F'","U'","F","R","U","R'","F","R'","F'","R","U'","R"),2],
    "PLL_Ra": [("R","U'","R'","U'","R","U","R","D","R'","U'","R","D'","R'","U2","R'"),3],
    "PLL_Rb": [("R'","U2","R","U2","R'","F","R","U","R'","U'","R'","F'","R2"),3],
    "PLL_T":  [("R","U","R'","U'","R'","F","R2","U'","R'","U'","R","U","R'","F'"),2],
    "PLL_Ua": [("R","U'","R","U","R","U","R","U'","R'","U'","R2"),3],
    "PLL_Ub": [("R2","U","R","U","R'","U'","R'","U'","R'","U","R'"),3],
    "PLL_V":  [("R'","U","R'","U'","B'","R'","B2","U'","B'","U","B'","R","B","R"),2],
    "PLL_Y":  [("F","R","U'","R'","U'","R","U","R'","F'","R","U","R'","U'","R'","F","R","F'"),2],
    "PLL_Z":  [("M'","U'","M2","U'","M2","U'","M'","U2","M2"),4],
}

def auf(k):
    return {0:(),1:("U",),2:("U2",),3:("U'",)}[k]

def solver_cross(etat_actuelle):
    if (len(etat_actuelle) != 54) or (etat_actuelle.count(0) != 9) or (etat_actuelle.count(1) != 9) or (etat_actuelle.count(2) != 9) or (etat_actuelle.count(3) != 9) or (etat_actuelle.count(4) != 9) or (etat_actuelle.count(5) != 9):
        return "il y a une erreur dans ta liste"
    elif cross(etat_actuelle):
        return []
    etats = deque([etat_actuelle])
    vus = {etat_actuelle}
    parent = {etat_actuelle: None}
    while etats:
        etat = etats.popleft()
        for nom, perm in MOUVEMENTS3.items():
            if nom in ROTATIONS:
                continue
            voisin = appliquer3(etat,nom)
            if voisin in vus:
                continue
            vus.add(voisin)
            parent[voisin] = (etat,nom)
            if cross(voisin):
                return reconstruire_fin(parent,voisin)
            etats.append(voisin)
    return "la croix est impossible"

def F2L3(etat_actuelle):
    if len(etat_actuelle) != 54:
        raise ValueError("Tableau non conforme")
    if all(len(set(etat_actuelle[i+3:i+9])) == 1 for i in range(9, 45, 9)):
        return ()
    etat = etat_actuelle
    mouv = ()
    trouve = []
    slot=[0,0,0,0]
    dernier = 0
    for i in range(4):
        if (len(set(etat[13:15]+etat[16:18])) == 1 
            and len(set(etat[21:23]+etat[24:26])) == 1
            and len(set(etat[50:51]+etat[46:48])) == 1):
            trouve.append(i)
        etat = appliquer3(etat,"y")
    for i in trouve:
        slot[i] = 1
    rotation = 0
    while not all(slot):
        if dernier >= 4:
            raise ValueError("bizarre")
        etat_transfo = etat
        if slot[rotation % 4]:
            etat = appliquer3(etat,"y")
            rotation += 1
            mouv += ("y",)
            dernier += 1
            continue   
        for nom, (mouvements, poids) in ALGORITHMES3.items():
            if not nom.startswith("F2L_"):
                continue
            for j in range(4):
                etat = repeter3(etat,"U",j)
                for n in mouvements:
                    etat = appliquer3(etat,n)
                if (len(set(etat[13:15]+etat[16:18])) == 1 
                    and len(set(etat[21:23]+etat[24:26])) == 1
                    and len(set(etat[50:51]+etat[46:48])) == 1):
                    slot[rotation % 4] = 1
                    mouv += auf(j) + mouvements
                    dernier = 0
                    break
                else:
                    etat = etat_transfo
            if slot[rotation % 4]:
                break
        if all(slot):
            break
        for n in ["U","E'","D'"]:
            etat = appliquer3(etat,n)
        rotation += 1
        mouv += ("y",)
        dernier += 1
    return mouv


def PLL3(etat_actuelle):
    if (len(etat_actuelle) == 12):
        etat_initial = RESOLU3[0:9]+etat_actuelle[0:3]+RESOLU3[12:18]+etat_actuelle[3:6]+RESOLU3[21:27]+etat_actuelle[6:9]+RESOLU3[30:36]+etat_actuelle[9:]+RESOLU3[39:]
    elif (len(etat_actuelle) == 54):
        etat_initial = etat_actuelle
    else:
        return "euhhhhh comment dire... t'as fais une erreur d'entrée"
    for k in range(4):
        if est_resolu3(repeter3(etat_initial, "U", k)):
            return ("U",)*k
    etat = etat_initial
    trouve = False
    for nom, (mouvements, poids) in ALGORITHMES3.items():
        indice_start = 0
        indice_stop = 0
        if not nom.startswith("PLL_"):
            continue
        for i in range(4):
            indice_stop = 0
            etat = repeter3(etat,"U",i)
            for n in mouvements:
                etat = appliquer3(etat,n)
            etat_transfo = etat
            for j in range(4):
                if est_resolu3(repeter3(etat,"U",j)):
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

    return auf(indice_start) + mouvements + auf(indice_stop) if trouve else "chef... t'as fais une erreur quelque part"

def OLL3(etat_actuelle):
    if (len(etat_actuelle) == 21):
        etat_initial=etat_actuelle[0:12]+RESOLU3[12:18]+etat_actuelle[12:15]+RESOLU3[21:27]+etat_actuelle[15:18]+RESOLU3[30:36]+etat_actuelle[18:21]+RESOLU3[39:]
    elif (len(etat_actuelle) == 54):
        etat_initial = etat_actuelle
    else: 
        return "euhhhhh comment dire... t'as fais une erreur d'entree"
    if len(set(etat_initial[0:9])) == 1:
        return ()
    etat = etat_initial
    trouve = False
    for nom, (mouvements, poids) in ALGORITHMES3.items():
        indice_i = 0
        if not nom.startswith("OLL_"):
            continue
        
        for i in range(4):
            etat = repeter3(etat,"U",i)
            for n in mouvements:
                etat = appliquer3(etat,n)
            if len(set(etat[0:9])) == 1:
                trouve = True
                break
            else:
                indice_i += 1
                etat = etat_initial
        if trouve:
            break

    return auf(indice_i) + mouvements if trouve else "chef... C'est juste impossible"

def melanger_OLL3(n,seed):
    etat = RESOLU3
    mouv_oll = []
    for nom, (mouvements,poids) in ALGORITHMES3.items():
        if not nom.startswith("OLL_"):
            continue
        else:
            mouv_oll.append(mouvements)
    mouv=[]
    rng = random.Random(seed)
    for _ in range(n):
        nom = rng.choice(list(mouv_oll))
        auf = rng.randrange(4)
        etat = repeter3(etat, "U",auf)
        for m in nom:
            etat = appliquer3(etat,m)
        mouv.append(nom)
    res = [etat,mouv]
    return res

def melanger_PLL3(n,seed):
    etat = RESOLU3
    mouv_pll = []
    for nom, (mouvements,poids) in ALGORITHMES3.items():
        if not nom.startswith("PLL_"):
            continue
        else:
            mouv_pll.append(mouvements)
    mouv=[]
    rng = random.Random(seed)
    for _ in range(n):
        nom = rng.choice(list(mouv_pll))
        auf = rng.randrange(4)
        etat = repeter3(etat,"U",auf)
        for m in nom:
            etat = appliquer3(etat,m)
        mouv.append(nom)
    res = [etat,mouv]
    return res


def solver_cfop(etat):
    etat_actuelle = etat
    solution = []

    for nom_etape, fonction in (("cross", solver_cross),
                                ("F2L", F2L3),
                                ("OLL", OLL3),
                                ("PLL", PLL3)):
        mouv = fonction(etat_actuelle)
        if not isinstance(mouv, (list, tuple)):
            return f"échec à l'étape {nom_etape} : {mouv}"
        print(nom_etape, ":", mouv)
        print(" ")
        for n in mouv:
            etat_actuelle = appliquer3(etat_actuelle, n)
        solution += mouv

    return solution

print(melanger3(20,90)[1])
print(solver_cfop(melanger3(20,90)[0]))