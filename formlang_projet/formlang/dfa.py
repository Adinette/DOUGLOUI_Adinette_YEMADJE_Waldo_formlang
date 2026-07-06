"""AFD. À COMPLÉTER : run, accepts, minimize (Moore).  -> Jour 1 (E1.1, E1.2)."""
from __future__ import annotations
from dataclasses import dataclass, field
from collections import deque


@dataclass
class DFA:
    transitions: dict            # (state, sym) -> state
    start: str
    accept: set
    alphabet: set = field(default_factory=set)

    def __post_init__(self):
        if not self.alphabet:
            self.alphabet = {a for (_, a) in self.transitions}

    def run(self, w: str):
            # On commence à l'état initial
            current_state = self.start
            
            # On lit le mot lettre par lettre
            for sym in w:
                # On cherche s'il y a une transition pour (état_actuel, lettre)
                if (current_state, sym) in self.transitions:
                    current_state = self.transitions[(current_state, sym)]
                else:
                    # Si la transition manque, l'automate bloque -> renvoyer None
                    return None
                    
            # On renvoie l'état final atteint après avoir lu tout le mot
            return current_state

    def accepts(self, w: str) -> bool:
        # On exécute le mot sur l'automate
        final_state = self.run(w)
        
        # Le mot est accepté si l'état atteint existe et fait partie des états acceptants
        return final_state is not None and final_state in self.accept

    # ----- fourni : utilitaires pour la minimisation --------------------------
    def _reachable(self) -> set:
        seen, todo = {self.start}, deque([self.start])
        while todo:
            s = todo.popleft()
            for a in self.alphabet:
                t = self.transitions.get((s, a))
                if t is not None and t not in seen:
                    seen.add(t)
                    todo.append(t)
        return seen

    def _completed(self):
        SINK = "__sink__"
        trans = dict(self.transitions)
        states = self._reachable()
        need = False
        for s in states:
            for a in self.alphabet:
                if (s, a) not in trans:
                    trans[(s, a)] = SINK
                    need = True
        if need:
            states = states | {SINK}
            for a in self.alphabet:
                trans[(SINK, a)] = SINK
        return states, trans

    def minimize(self) -> "DFA":
        # Étape 1 : On complète l'automate et on récupère la liste des états accessibles
        states, trans = self._completed()
        
        # Étape 2 : Partition initiale -> États Finaux (F) vs États Non-Finaux (Non-F)
        # On utilise des frozenset pour pouvoir les stocker facilement
        final_states = frozenset(s for s in states if s in self.accept)
        non_final_states = frozenset(s for s in states if s not in self.accept)
        
        # Notre partition est un ensemble de blocs (on filtre les blocs vides)
        P = {b for b in (final_states, non_final_states) if b}
        
        # Boucle de raffinement de Moore
        while True:
            new_P = set()
            
            # Fonction d'aide pour identifier dans quel bloc actuel un état atterrit après une lettre
            def get_block(state, alphabet_letter):
                target = trans.get((state, alphabet_letter))
                for block in P:
                    if target in block:
                        return block
                return None

            # On essaie de découper chaque bloc existant
            for block in P:
                # On regroupe les états du bloc selon leur "signature" de transition
                # Signature = pour chaque lettre de l'alphabet, quel bloc est atteint ?
                split_dict = {}
                for state in block:
                    signature = tuple(get_block(state, a) for a in sorted(self.alphabet))
                    if signature not in split_dict:
                        split_dict[signature] = set()
                    split_dict[signature].add(state)
                
                # On ajoute les nouveaux sous-blocs formés
                for sub_block in split_dict.values():
                    new_P.add(frozenset(sub_block))
            
            # Condition d'arrêt : si la partition n'a pas changé, on a fini !
            if new_P == P:
                break
            P = new_P
            
        # Étape 3 : Reconstruction du nouvel AFD minimal
        # Chaque bloc de P devient un état unique de l'AFD minimal
        # On donne un nom textuel simple à chaque bloc (ex: "s0", "s1"...)
        block_list = list(P)
        state_mapping = {}
        for idx, block in enumerate(block_list):
            for state in block:
                state_mapping[state] = f"s{idx}"
                
        # Déterminer les composants du nouvel AFD
        new_start = state_mapping[self.start]
        new_accept = {state_mapping[s] for s in states if s in self.accept}
        new_transitions = {}
        
        for block in block_list:
            # On prend un représentant du bloc pour copier ses transitions
            rep = next(iter(block))
            # On ignore l'état puits fictif s'il a été généré mais qu'il n'est pas acceptant
            if rep == "__sink__" and rep not in self.accept:
                continue
                
            for a in self.alphabet:
                target = trans.get((rep, a))
                # Si la cible fait partie du puits non acceptant, on n'ajoute pas la transition
                if target == "__sink__" and target not in self.accept:
                    continue
                if rep in state_mapping and target in state_mapping:
                    new_transitions[(state_mapping[rep], a)] = state_mapping[target]
                    
        return DFA(transitions=new_transitions, start=new_start, accept=new_accept, alphabet=self.alphabet)
    def num_states(self) -> int:
        st = {self.start}
        for (s, _), t in self.transitions.items():
            st.add(s)
            st.add(t)
        return len(st)
