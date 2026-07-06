"""AFN (eps = ''). À COMPLÉTER : to_dfa par sous-ensembles.  -> Jour 1 (E1.3)."""
from __future__ import annotations
from dataclasses import dataclass, field
from .dfa import DFA


@dataclass
class NFA:
    transitions: dict            # (state, sym|'') -> set(states)
    start: str
    accept: set
    alphabet: set = field(default_factory=set)

    def __post_init__(self):
        if not self.alphabet:
            self.alphabet = {a for (_, a) in self.transitions if a != ""}

    # ----- fourni -------------------------------------------------------------
    def _eps_closure(self, states: frozenset) -> frozenset:
        stack, clos = list(states), set(states)
        while stack:
            s = stack.pop()
            for t in self.transitions.get((s, ""), ()):
                if t not in clos:
                    clos.add(t)
                    stack.append(t)
        return frozenset(clos)

    def _move(self, states: frozenset, a: str) -> frozenset:
        out = set()
        for s in states:
            out |= self.transitions.get((s, a), set())
        return frozenset(out)

    def accepts(self, w: str) -> bool:
        cur = self._eps_closure(frozenset({self.start}))
        for c in w:
            cur = self._eps_closure(self._move(cur, c))
        return any(s in self.accept for s in cur)

    # ----- à compléter --------------------------------------------------------
    def to_dfa(self) -> DFA:
            # 1. Calculer le macro-état initial (epsilon-fermeture de l'état de départ)
            start_closure = self._eps_closure(frozenset({self.start}))
            
            # Structures pour l'exploration
            todo = [start_closure]
            seen_closures = {start_closure}
            
            # Dictionnaire pour associer un nom de chaîne (ex: "q0", "q1"...) à chaque macro-état
            closure_to_name = {start_closure: "q0"}
            
            new_transitions = {}
            new_accept = set()
            
            # Si le macro-état initial contient un état acceptant, l'état initial de l'AFD l'est aussi
            if any(s in self.accept for s in start_closure):
                new_accept.add("q0")
                
            # 2. Boucle d'exploration (BFS)
            while todo:
                current_closure = todo.pop(0)
                current_name = closure_to_name[current_closure]
                
                # Pour chaque lettre de l'alphabet, on calcule le macro-état cible
                for a in sorted(self.alphabet):
                    # Déplacement + epsilon-fermeture
                    target_closure = self._eps_closure(self._move(current_closure, a))
                    
                    # Si le macro-état cible n'est pas vide
                    if target_closure:
                        # Si c'est un nouveau macro-état jamais vu, on l'enregistre
                        if target_closure not in seen_closures:
                            seen_closures.add(target_closure)
                            todo.append(target_closure)
                            # On lui attribue un nom unique
                            new_name = f"q{len(closure_to_name)}"
                            closure_to_name[target_closure] = new_name
                            
                            # Si ce macro-état contient un état acceptant de l'AFN, on le marque acceptant
                            if any(s in self.accept for s in target_closure):
                                new_accept.add(new_name)
                        
                        # On ajoute la transition déterministe dans l'AFD
                        new_transitions[(current_name, a)] = closure_to_name[target_closure]
                        
            # 3. Retourner l'AFD construit
            return DFA(
                transitions=new_transitions,
                start="q0",
                accept=new_accept,
                alphabet=self.alphabet
            )