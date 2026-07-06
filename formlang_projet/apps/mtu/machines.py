"""Opérations comme VRAIES machines de Turing. Tables ADD, SUB.

-> Jour 4 (E4.3)."""
from formlang.turing import TuringMachine

ADD = TuringMachine(
    transitions={
        ("q0", "1"): ("q0", "1", "R"),
        ("q0", "+"): ("q1", "1", "R"),
        ("q1", "1"): ("q1", "1", "R"),
        ("q1", "_"): ("q2", "_", "L"),
        ("q2", "1"): ("qf", "_", "L"),
    },
    start="q0",
    accept={"qf"},
)

SUB = TuringMachine(
    transitions={
        ("q_init", "1"): ("q_init", "1", "R"),
        ("q_init", "-"): ("q_init", "-", "R"),
        ("q_init", "_"): ("q_back", "_", "L"),

        ("q_back", "1"): ("q_back", "1", "L"),
        ("q_back", "-"): ("q_back", "-", "L"),
        ("q_back", "_"): ("q0", "_", "R"),

        ("q0", "1"): ("q0", "1", "R"),
        ("q0", "-"): ("q1", "-", "R"),
        ("q1", "1"): ("q2", "X", "L"),
        ("q1", "X"): ("q1", "X", "R"),
        ("q1", "_"): ("q5", "_", "L"),

        ("q2", "1"): ("q2", "1", "L"),
        ("q2", "X"): ("q2", "X", "L"),
        ("q2", "_"): ("q2", "_", "L"),
        ("q2", "-"): ("q3", "-", "L"),

        ("q3", "1"): ("q4", "X", "R"),
        ("q3", "X"): ("q3", "X", "L"),
        ("q3", "_"): ("q3", "_", "L"),

        ("q4", "1"): ("q4", "1", "R"),
        ("q4", "X"): ("q4", "X", "R"),
        ("q4", "_"): ("q4", "_", "R"),
        ("q4", "-"): ("q1", "-", "R"),

        ("q5", "1"): ("q5", "1", "L"),
        ("q5", "X"): ("q5", "X", "L"),
        ("q5", "_"): ("q5", "_", "L"),
        ("q5", "-"): ("qf", "_", "S"),
    },
    start="q_init",
    accept={"qf"},
)
