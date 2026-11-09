from cube2 import MOUVEMENTS2, RESOLU2, appliquer2, repeter2, melanger2
from cube3 import MOUVEMENTS3, RESOLU3, appliquer3, repeter3, melanger3, est_resolu3
from fop import Algorithme2
from cfop import ALGORITHMES3

# TEST ALGORITHME
def test3():
    for m in Algorithme2.values():
        etat = RESOLU2
        for i in range(m[1]):
            for n in m[0]:
                appliquer2(etat,n)
        assert etat == RESOLU2

def test3():
    for m in ALGORITHMES3.values():
        etat = RESOLU3
        for i in range(m[1]):
            for n in m[0]:
                appliquer3(etat,n)
        assert etat == RESOLU3