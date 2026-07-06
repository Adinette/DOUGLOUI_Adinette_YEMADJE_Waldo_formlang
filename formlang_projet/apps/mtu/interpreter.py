"""La machine de Turing UNIVERSELLE comme application (TP MTU). À COMPLÉTER.

L'interpréteur ne doit PAS réécrire de boucle d'exécution : il encode M puis
DÉLÈGUE à formlang.utm.UniversalTM.  -> Jour 4 (E4.2 / E4.4)."""
from __future__ import annotations
from formlang.utm import UniversalTM, encode
from .machines import ADD, SUB


def _ones(s: str) -> int:
    return s.count("1")


class UniversalInterpreter:
    def __init__(self):
        self._U = UniversalTM()

    def run(self, machine, word, **kw):
        # Encodage de la machine de Turing pure (ADD ou SUB)
        encoded_m = encode(machine)
        # Délégation de l'exécution complète à la machine universelle U
        return self._U.run(encoded_m, word, **kw)


def addition_via_utm(n: int, m: int) -> int:
    interpreter = UniversalInterpreter()
    word = "1" * n + "+" + "1" * m
    res = interpreter.run(ADD, word)
    return _ones(res.tape)


def soustraction_via_utm(n: int, m: int) -> int:
    interpreter = UniversalInterpreter()
    word = "1" * n + "-" + "1" * m
    res = interpreter.run(SUB, word)
    return _ones(res.tape)