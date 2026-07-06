"""SingularityDetector. À COMPLÉTER : table de l'AFD 'or'.  -> Jour 1 (E1.1)."""
from formlang.dfa import DFA

_DFA_OR = DFA(
    transitions={
        # Depuis l'état A
        ("A", "a"): "A",
        ("A", "o"): "B",
        ("A", "r"): "A",
        
        # Depuis l'état B (armé avec un 'o')
        ("B", "a"): "A",
        ("B", "o"): "B",
        ("B", "r"): "C",
        
        # Depuis l'état C (gagnant / absorbant)
        ("C", "a"): "C",
        ("C", "o"): "C",
        ("C", "r"): "C",
    },
    start="A", accept={"C"}, alphabet={"a", "o", "r"},
)


def contains_or(w: str) -> bool:
    return _DFA_OR.accepts(w)


def detector_dfa() -> DFA:
    return _DFA_OR