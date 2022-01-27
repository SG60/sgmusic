import hypothesis
import pytest
import sympy  # type: ignore
from hypothesis import given
from hypothesis import strategies as st
from sympy import S, symbols  # type: ignore

from sgmusic import Section, __version__, ramp, separatetempolist


def test_version():
    assert __version__ == "0.1.0"


def test_tempolist():
    t, t1, t2 = symbols("t:3")  # type: ignore
    tempolist_combined = [(t, "start"), t1, (t2, "somewhere")]
    tempolist, sections = separatetempolist(tempolist_combined)
    print(f"tempolist: {tempolist}", f"sections: {sections}")
    assert (tempolist == (t, t1, t2)) & (sections == ("start", "", "somewhere"))


def test_Section():
    t, t1, t2 = symbols("t:3")  # type: ignore
    s1 = Section(t, "start")
    s2 = Section(S("t2"))
    s2.name = "middle"
    assert s1.name == "start"
    assert s2.name == "middle"
    expression = s1.tempo + t1 * s2.tempo
    assert expression.subs({t: 0, t1: 5}) == 5 * t2


@pytest.mark.xfail
@given(a=st.integers(10), b=st.integers(10), c=st.integers(10), d=st.decimals(10, 1000))
def test_ramp(a, b, c, d):
    # hypothesis.assume(not (a == b == c == d))
    hypothesis.assume(all((a, b, c, d)))
    s, m, n, r = symbols("s m n r")  # type: ignore
    ramp_eq = sympy.Eq(ramp(a, b, c, s), d).doit()
    try:
        end_beat = sympy.solveset(ramp_eq, s).args[0]
    except IndexError:
        end_beat = None
    try:
        end_beat_2 = (
            sympy.solveset(sympy.Eq(ramp(m, n, r, s), d).doit(), s)
            .args[0]
            .subs([(m, a), (n, b), (r, c)])
        )
    except IndexError:
        end_beat_2 = None
    assert end_beat == end_beat_2
