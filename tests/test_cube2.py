import random
from cube2 import MOUVEMENTS2, RESOLU2, appliquer2, repeter2, melanger2, est_resolu2
from fop import PLL2, OLL2, lastlayer_fop, melanger_OLL2, melanger_PLL2, firstlayer_fop, melanger_ortega, ortega

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
        assert len(set(etat[0:4])) == 1

def test_PLL2():
    for i in range(1000):
        n = random.randrange(100)
        seed = random.randrange(1000)
        etat = melanger_PLL2(n,seed)[0]
        for m in PLL2(etat):
            etat = appliquer2(etat,m)
        print(firstlayer_fop(melanger_ortega(n,seed)[0]))
        print(etat)
        print(melanger_ortega(n,seed)[1])
        assert est_resolu2(etat)

def test_lastlayer_fop():
    for i in range(1000):
        etat = melanger_OLL2(random.randrange(100),random.randrange(1000))[0]
        for m in lastlayer_fop(etat):
            etat = appliquer2(etat, m)
        assert est_resolu2(etat)

def test_firstlayer_fop():
    for i in range(1000):
        etat = melanger2(random.randrange(100),random.randrange(1000))[0]
        for m in firstlayer_fop(etat):
            etat = appliquer2(etat,m)
        assert len(set(etat[20:24])) == 1


def test_ortega():
    for i in range(1000):
            etat = melanger_ortega(random.randrange(100),random.randrange(1000))[0]
            for m in ortega(etat):
                etat = appliquer2(etat,m)
            assert est_resolu2(etat)
