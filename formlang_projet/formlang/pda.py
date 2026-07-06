"""Automate à pile (acceptation pile vide). À COMPLÉTER.  -> Jour 2 (E2.1)."""
from __future__ import annotations


class DelimiterPDA:
    def __init__(self, pairs=(("[", "]"), ("(", ")")), ignore=("a", "o", "r", "e")):
        self.open = {o for o, _ in pairs}
        self.match = {c: o for o, c in pairs}     # fermant -> ouvrant attendu
        self.ignore = set(ignore)

    def accepts(self, w: str) -> bool:
        stack = []
        
        for char in w:
            if char in self.open:
                # C'est un délimiteur ouvrant, on l'empile
                stack.append(char)
            elif char in self.match:
                # C'est un délimiteur fermant
                # On vérifie si la pile n'est pas vide et si le sommet correspond
                expected_open = self.match[char]
                if not stack or stack[-1] != expected_open:
                    return False
                # Correspondance correcte, on dépile
                stack.pop()
            elif char in self.ignore:
                # Caractère à ignorer, on passe au suivant
                continue
            else:
                # Si un caractère inconnu se présente et n'est pas ignoré, 
                # on peut décider de rejeter selon la politique stricte de l'automate
                return False
                
        # Le mot est accepté si et seulement si la pile est complètement vide à la fin
        return len(stack) == 0