"""Grammaire hors-contexte : génération bornée. À COMPLÉTER.  -> Jour 2 (E2.2)."""
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class CFG:
    rules: dict
    start: str
    nonterminals: set

    def generate(self, max_len: int) -> set:
        from collections import deque

        words = set()
        seen = set()
        
        start_sentential = (self.start,)
        queue = deque([start_sentential])
        seen.add(start_sentential)
        
        while queue:
            current = queue.popleft()
            num_terminals = sum(1 for sym in current if sym not in self.nonterminals)
            
            if num_terminals > max_len:
                continue
                
            idx = next((i for i, sym in enumerate(current) if sym in self.nonterminals), None)
            
            if idx is None:
                if len(current) <= max_len:
                    words.add("".join(current))
                continue
                
            num_nonterminals = len(current) - num_terminals
            if num_nonterminals > max_len + 2:
                continue

            nt = current[idx]
            for production in self.rules.get(nt, []):
                new_sentential = current[:idx] + tuple(production) + current[idx+1:]
                if new_sentential not in seen:
                    if len(new_sentential) <= max_len + num_nonterminals + 2:
                        seen.add(new_sentential)
                        queue.append(new_sentential)
                        
        return words


def balanced_cfg() -> "CFG":
    # FOURNI : S -> S S | [ S ] | ( S ) | a | o | r | eps
    return CFG(
        rules={"S": [("S", "S"), ("[", "S", "]"), ("(", "S", ")"),
                     ("a",), ("o",), ("r",), ()]},
        start="S", nonterminals={"S"},
    )