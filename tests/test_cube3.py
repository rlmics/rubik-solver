import random
from cube3 import MOUVEMENTS3, RESOLU3, appliquer3, repeter3, melanger3, est_resolu3
from cfop import OLL3, PLL3, melanger_OLL3, melanger_PLL3, auf, solver_cfop

def test_quatre_fois_identite():
    for m in ["U", "R", "F","D","L","B","M", "E", "S", "u", "d", "r", "l", "f", "b"]:
        assert repeter3(RESOLU3, m, 4) == RESOLU3

def test_mouvement_puis_inverse():
    for m in ["U", "R", "F","D","L","B","M", "E", "S", "u", "d", "r", "l", "f", "b"]:
        assert appliquer3(appliquer3(RESOLU3, m), m + "'") == RESOLU3

def test_sexy_moveR_six_fois():
    etat = RESOLU3
    for _ in range(6):
        for m in ["R", "U", "R'", "U'"]:
            etat = appliquer3(etat, m)
    assert etat == RESOLU3

def test_sexy_moveL_six_fois():
    etat = RESOLU3
    for _ in range(6):
        for m in ["L'", "U'", "L", "U"]:
            etat = appliquer3(etat, m)
    assert etat == RESOLU3

def test_tables_sont_des_permutations():
    for perm in MOUVEMENTS3.values():
        assert sorted(perm) == list(range(54))

def test_double_egal_deux_quarts_de_tour():
    for m in ["U", "D", "R", "L", "F", "B", "M", "E", "S", "u", "d", "r", "l", "f", "b"]:
        assert appliquer3(RESOLU3, m + "2") == repeter3(RESOLU3, m, 2)

def test_double_layers_definition():
    etat = RESOLU3
    for m in ["R", "U", "F'", "L", "D2", "B"]:
        etat = appliquer3(etat, m)
    assert appliquer3(etat, "r") == appliquer3(appliquer3(etat, "R"), "M'")
    assert appliquer3(etat, "l") == appliquer3(appliquer3(etat, "L"), "M")
    assert appliquer3(etat, "u") == appliquer3(appliquer3(etat, "U"), "E'")
    assert appliquer3(etat, "d") == appliquer3(appliquer3(etat, "D"), "E")
    assert appliquer3(etat, "f") == appliquer3(appliquer3(etat, "F"), "S")
    assert appliquer3(etat, "b") == appliquer3(appliquer3(etat, "B"), "S'")

def test_conservation_des_couleurs():
    for m in MOUVEMENTS3:
        assert sorted(appliquer3(RESOLU3, m)) == sorted(RESOLU3)

def test_OLL3():
    for i in range(1000):
        etat = melanger_OLL3(random.randrange(100),random.randrange(1000))[0]
        for m in OLL3(etat):
            etat = appliquer3(etat,m)
        assert etat[0:9] == (0,0,0,0,0,0,0,0,0)

def test_PLL3():
    for i in range(1000):
        etat = melanger_PLL3(random.randrange(100),random.randrange(1000))[0]
        for m in PLL3(etat):
            etat = appliquer3(etat,m)
        assert etat == RESOLU3


def test_cfop():
    etat = melanger3(10,90)[0]
    for m in solver_cfop(melanger3(10,90)[0]):
        etat = appliquer3(etat, m)
    assert est_resolu3(etat)