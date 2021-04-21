from sgmusic import __version__, separatetempolist, Section
from sympy import symbols, S


def test_version():
    assert __version__ == "0.1.0"


def test_tempolist():
    t, t1, t2 = symbols("t:3")
    tempolist_combined = [(t, "start"), t1, (t2, "somewhere")]
    tempolist, sections = separatetempolist(tempolist_combined)
    print(f"tempolist: {tempolist}", f"sections: {sections}")
    assert (tempolist == (t, t1, t2)) & (sections == ("start", "", "somewhere"))


def test_Section():
    t, t1, t2 = symbols("t:3")
    s1 = Section(t, "start")
    s2 = Section(S("t2"))
    s2.name = "middle"
    assert s1.name == "start"
    assert s2.name == "middle"
    expression = s1.tempo + t1 * s2.tempo
    assert expression.subs({t: 0, t1: 5}) == 5 * t2
