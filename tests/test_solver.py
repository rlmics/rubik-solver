import random
from cube2 import MOUVEMENTS2, RESOLU2, appliquer2, repeter2, melanger2
from cube3 import MOUVEMENTS3, RESOLU3, appliquer3, repeter3, melanger3
from solver import solver_bfs2, inverse, solver_bfs3

def test_mouvement_puis_inverse2():
    for mouv, (perm) in MOUVEMENTS2.items():
        assert appliquer2(appliquer2(RESOLU2, mouv), inverse(mouv)) == RESOLU2

def test_mouvement_puis_inverse3():
    for mouv, (perm) in MOUVEMENTS3.items():
        assert appliquer3(appliquer3(RESOLU3, mouv), inverse(mouv)) == RESOLU3

def test_melange2():
    etat = melanger2(3,90)[0]
    for n in solver_bfs2(etat):
        etat = appliquer2(etat,n)
    assert etat == RESOLU2

def test_melange3():
    etat = melanger3(3,90)[0]
    for n in solver_bfs3(etat):
        etat = appliquer3(etat,n)
    assert etat == RESOLU3