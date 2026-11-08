import random
from cube2 import MOUVEMENTS2, RESOLU2, appliquer2, repeter2, melanger2
from solver import solver_bfs, inverse

def test_mouvement_puis_inverse():
    for mouv, (perm) in MOUVEMENTS2.items():
        assert appliquer2(appliquer2(RESOLU2, mouv), inverse(mouv)) == RESOLU2

def test_melange():
    etat = melanger2(3,90)[0]
    for n in solver_bfs(etat):
        etat = appliquer2(etat,n)
    assert etat == RESOLU2