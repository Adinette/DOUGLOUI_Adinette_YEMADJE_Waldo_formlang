"""Transducteur fini séquentiel. À COMPLÉTER : transduce.  -> Jour 1 (E1.4)."""
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class SequentialFST:
    transitions: dict            # (state, in_sym) -> (next_state, out_sym)
    start: str
    finals: set
    identity_on_missing: bool = False

    def transduce(self, w: str) -> str:
        current_state = self.start
        output_chars = []
        
        for in_sym in w:
            key = (current_state, in_sym)
            if key in self.transitions:
                next_state, out_sym = self.transitions[key]
                current_state = next_state
                output_chars.append(out_sym)
            elif self.identity_on_missing:
                # Si identity_on_missing est True, on garde la lettre d'origine
                # L'état ne change pas (dans le cas d'un automate à état unique comme leet)
                output_chars.append(in_sym)
            else:
                # Si pas de transition et pas d'identité, la transduction échoue
                return ""
                
        # On vérifie si l'état final atteint fait partie des états finaux acceptants
        if current_state in self.finals:
            return "".join(output_chars)
        return ""

def compose(t1: "SequentialFST", t2: "SequentialFST") -> "SequentialFST":
    # FOURNI : t(w) = t2(t1(w)). États = paires.
    trans = {}
    for (s1, a), (s1n, b) in t1.transitions.items():
        for (s2, x), (s2n, c) in t2.transitions.items():
            if x == b:
                trans[((s1, s2), a)] = ((s1n, s2n), c)
    finals = {(f1, f2) for f1 in t1.finals for f2 in t2.finals}
    return SequentialFST(trans, (t1.start, t2.start), finals)


def leet_fst() -> "SequentialFST":
    transitions = {
        ("q0", "4"): ("q0", "a"),
        ("q0", "3"): ("q0", "e"),
        ("q0", "0"): ("q0", "o"),
        ("q0", "1"): ("q0", "i"),
        ("q0", "5"): ("q0", "s"),
    }
    return SequentialFST(
        transitions=transitions,
        start="q0",
        finals={"q0"},
        identity_on_missing=True
    )

def reverse_twoway(w: str) -> str:
    # FOURNI : renversement (modélise une transduction bidirectionnelle).
    return w[::-1]
