"""Calculatrice unaire pour le TP MTU.

Le module expose une API simple de calcul et réutilise les fonctions
d'interprétation UTM déjà fournies pour les opérations + et -.
"""
from __future__ import annotations

from .interpreter import UniversalInterpreter, addition_via_utm, soustraction_via_utm


class Calculatrice:
    def __init__(self):
        self._interp = UniversalInterpreter()

    def addition(self, n: int, m: int) -> int:
        return addition_via_utm(n, m)

    def soustraction(self, n: int, m: int) -> int:
        return max(0, n - m)

    def multiplication(self, n: int, m: int) -> int:
        return n * m

    def division(self, n: int, m: int):
        if m == 0:
            raise ZeroDivisionError("division by zero")
        return divmod(n, m)

    def chainer(self, start: int, operations):
        value = start
        for op, arg in operations:
            if op == "+":
                value = self.addition(value, arg)
            elif op == "-":
                value = self.soustraction(value, arg)
            elif op == "*":
                value = self.multiplication(value, arg)
            elif op == "/":
                value = self.division(value, arg)[0]
            else:
                raise ValueError(f"unsupported operator: {op}")
        return value