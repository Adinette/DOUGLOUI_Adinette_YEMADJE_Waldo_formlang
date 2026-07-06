"""Automate d'arbres ascendant (BUTA) générique. À COMPLÉTER : run, accepts,
product.  -> Jour 3 (E3.1, E3.4)."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Hashable


@dataclass(frozen=True)
class Term:
    symbol: str
    children: tuple["Term", ...] = ()
    label: Optional[str] = None


class _Reject:
    __slots__ = ()
    def __repr__(self):
        return "REJECT"


REJECT = _Reject()


class TreeAutomaton:
    def __init__(self, final_states):
        self.delta: dict[tuple[str, tuple], Hashable] = {}
        self.final: set = set(final_states)

    def add_rule(self, symbol: str, child_states, result) -> None:
        # FOURNI
        self.delta[(symbol, tuple(child_states))] = result

    def run(self, t: "Term"):
        # 1. Évaluer récursivement tous les enfants (Post-ordre)
        child_states = []
        for child in t.children:
            state = self.run(child)
            if state is REJECT:
                return REJECT
            child_states.append(state)
            
        # 2. Chercher la règle correspondante pour le nœud actuel
        key = (t.symbol, tuple(child_states))
        if key in self.delta:
            return self.delta[key]
            
        return REJECT

    def accepts(self, t: "Term") -> bool:
        root_state = self.run(t)
        if root_state is REJECT:
            return False
        return root_state in self.final

def product(a1: "TreeAutomaton", a2: "TreeAutomaton") -> "TreeAutomaton":
    # On récupère les attributs d'états finaux (on teste final_states ou final au cas où)
    final_states_1 = getattr(a1, "final_states", getattr(a1, "final", set()))
    final_states_2 = getattr(a2, "final_states", getattr(a2, "final", set()))
    
    # Construction de l'ensemble combiné (f1, f2)
    new_final = {(f1, f2) for f1 in final_states_1 for f2 in final_states_2}
    
    # Instanciation de l'automate produit avec ses états finaux
    prod_automaton = TreeAutomaton(final_states=new_final)
    
    # Fusion et croisement de toutes les règles de transition delta
    for (sym1, kids1), res1 in a1.delta.items():
        for (sym2, kids2), res2 in a2.delta.items():
            if sym1 == sym2 and len(kids1) == len(kids2):
                new_kids = tuple(zip(kids1, kids2))
                prod_automaton.add_rule(sym1, new_kids, (res1, res2))
                
    return prod_automaton