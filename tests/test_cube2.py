import random
from cube2 import MOUVEMENTS2, RESOLU2, appliquer2, repeter2, melanger2
from fop import PLL2, OLL2, lastlayer_fop, melanger_OLL2, melanger_PLL2

# TEST MOUVEMENT
def test_quatre_fois_identite():
    for m in ["U", "R", "F","D","L","B"]:
        assert repeter2(RESOLU2, m, 4) == RESOLU2

def test_mouvement_puis_inverse():
    for m in ["U", "R", "F","D","L","B"]:
        assert appliquer2(appliquer2(RESOLU2, m), m + "'") == RESOLU2

def test_sexy_moveR_six_fois():
    etat = RESOLU2
    for _ in range(6):
        for m in ["R", "U", "R'", "U'"]:
            etat = appliquer2(etat, m)
    assert etat == RESOLU2

def test_sexy_moveL_six_fois():
    etat = RESOLU2
    for _ in range(6):
        for m in ["L'", "U'", "L", "U"]:
            etat = appliquer2(etat, m)
    assert etat == RESOLU2

def test_tables_sont_des_permutations():
    for perm in MOUVEMENTS2.values():
        assert sorted(perm) == list(range(24))

def test_OLL2():
    for i in range(1000):
        etat = melanger_OLL2(random.randrange(100),random.randrange(1000))[0]
        for m in OLL2(etat):
            etat = appliquer2(etat,m)
        assert etat[0:4] == (0,0,0,0)

def test_PLL2():
    for i in range(1000):
        etat = melanger_PLL2(random.randrange(100),random.randrange(1000))[0]
        for m in PLL2(etat):
            etat = appliquer2(etat,m)
        assert etat == RESOLU2

def test_lastlayer_cfop():
    for i in range(1000):
        etat = melanger_OLL2(random.randrange(100),random.randrange(1000))[0]
        for m in lastlayer_fop(etat):
            etat = appliquer2(etat, m)
        assert etat == RESOLU2