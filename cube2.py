import random

#Initialisation cube resolu
# 0 = blanc; 1 = vert; 2 = rouge; 3 = bleu; 4 = orange; 5 = jaune
# Ordre des faces : U(0-3), F(4-7), R(8-11), B(12-15), L(16-19), D(20-23)
RESOLU2 = (
    0,0,0,0, # face du haut
    1,1,1,1, #face avant
    2,2,2,2, #face droite
    3,3,3,3, #face arriere
    4,4,4,4, #face gauche
    5,5,5,5 #face du bas
)

# Numerotation des stickers de chaque face (ligne par ligne, vue de l'exterieur) :
#   0 1
#   3 2
# Orientation de lecture : U vue de dessus avec B en haut, D vue de dessous avec F en haut,
# les autres faces avec U en haut.



#dictionnaire mouvement
MOUVEMENTS2 = {
    "U":    (3,0,1,2,8,9,6,7,12,13,10,11,16,17,14,15,4,5,18,19,20,21,22,23),
    "U'":   (1,2,3,0,16,17,6,7,4,5,10,11,8,9,14,15,12,13,18,19,20,21,22,23),
    "D":    (0,1,2,3,4,5,18,19,8,9,6,7,12,13,10,11,16,17,14,15,23,20,21,22),
    "D'":   (0,1,2,3,4,5,10,11,8,9,14,15,12,13,18,19,16,17,6,7,21,22,23,20),
    "R":    (0,5,6,3,4,21,22,7,11,8,9,10,2,13,14,1,16,17,18,19,20,15,12,23),
    "R'":   (0,15,12,3,4,1,2,7,9,10,11,8,22,13,14,21,16,17,18,19,20,5,6,23),
    "L":    (14,1,2,13,0,5,6,3,8,9,10,11,12,23,20,15,19,16,17,18,4,21,22,7),
    "L'":   (4,1,2,7,20,5,6,23,8,9,10,11,12,3,0,15,17,18,19,16,14,21,22,13),
    "F":    (0,1,17,18,7,4,5,6,3,9,10,2,12,13,14,15,16,20,21,19,11,8,22,23),
    "F'":   (0,1,11,8,5,6,7,4,21,9,10,20,12,13,14,15,16,2,3,19,17,18,22,23),
    "B":    (9,10,2,3,4,5,6,7,8,22,23,11,15,12,13,14,1,17,18,0,20,21,19,16),
    "B'":   (19,16,2,3,4,5,6,7,8,0,1,11,13,14,15,12,23,17,18,22,20,21,9,10),
    "D2":   (0,1,2,3,4,5,14,15,8,9,18,19,12,13,6,7,16,17,10,11,22,23,20,21),
    "U2":   (2,3,0,1,12,13,6,7,16,17,10,11,4,5,14,15,8,9,18,19,20,21,22,23),
    "R2":   (0,21,22,3,4,15,12,7,10,11,8,9,6,13,14,5,16,17,18,19,20,1,2,23),
    "L2":   (20,1,2,23,14,5,6,13,8,9,10,11,12,7,4,15,18,19,16,17,0,21,22,3),
    "F2":   (0,1,20,21,6,7,4,5,18,9,10,17,12,13,14,15,16,11,8,19,2,3,22,23),
    "B2":   (22,23,2,3,4,5,6,7,8,19,16,11,14,15,12,13,10,17,18,9,20,21,0,1),
}

def appliquer2(etat_actuelle, mouv):
    perm = MOUVEMENTS2[mouv]
    return (tuple(etat_actuelle[i] for i in perm))

def repeter2(etat_actuelle, mouv, n):
    for _ in range(n):
        etat_actuelle = appliquer2(etat_actuelle, mouv)
    return etat_actuelle

def melanger2(n,seed):
    etat = RESOLU2
    mouv=[]
    rng = random.Random(seed)
    for _ in range(n):
        nom = rng.choice(list(MOUVEMENTS2))
        etat = appliquer2(etat, nom)
        mouv.append(nom)
    res = [etat,mouv]
    return res

def afficher2(etat):
    print("      _______")
    print("******|",etat[0],etat[1],"|******")
    print("******|",etat[3],etat[2],"|******")
    print("___________________")
    print("|",etat[16],etat[17],"|",etat[4],etat[5],"|",etat[8],etat[9],"|")
    print("|",etat[19],etat[18],"|",etat[7],etat[6],"|",etat[11],etat[10],"|")
    print("___________________")
    print("******|",etat[20],etat[21],"|******")
    print("******|",etat[23],etat[22],"|******")
    print("      _______")
    print("******|",etat[14],etat[15],"|******")
    print("******|",etat[13],etat[12],"|******")
    print("      _______")


