"""Machine de Turing déterministe (ruban dict bi-infini).

-> Jour 4 (E4.1)."""
from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class TMResult:
    accepted: bool
    tape: str
    steps: int
    trace: list = field(default_factory=list)


@dataclass
class TuringMachine:
    transitions: dict           # (q, a) -> (q', b, d in {'L','R','S'})
    start: str
    accept: set
    blank: str = "_"
    reject: set = field(default_factory=set)

    def _read(self, tape: dict) -> str:
        if not tape:
            return ""
        lo, hi = min(tape), max(tape)
        result = "".join(tape.get(i, self.blank) for i in range(lo, hi + 1)).strip(self.blank)
        # Remove X markers (used internally by SUB machine for matched digits)
        result = result.replace("X", "").strip(self.blank)
        return result

    def _window(self, tape: dict) -> str:
        if not tape:
            return ""
        lo, hi = min(tape), max(tape)
        return "".join(tape.get(i, self.blank) for i in range(lo, hi + 1))

    def run(self, word: str, max_steps: int = 1_000_000, trace: bool = False) -> "TMResult":
        tape = {i: c for i, c in enumerate(word)}
        head = 0
        state = self.start
        steps = 0
        trace_list = []

        while state not in self.accept and state not in self.reject and steps < max_steps:
            if trace:
                clean_tape_trace = {int(k) if str(k).isdigit() else k: v for k, v in tape.items()}
                trace_list.append((head, state, clean_tape_trace))

            current_sym = tape.get(head, self.blank)

            key = (state, current_sym)
            if key not in self.transitions:
                break

            next_state, write_sym, move = self.transitions[key]
            tape[head] = write_sym

            if move == "R":
                head += 1
            elif move == "L":
                head -= 1

            state = next_state
            steps += 1

        actual_tape_content = self._read(tape) if tape else ""
        accepted = state in self.accept
        return TMResult(accepted=accepted, tape=actual_tape_content, steps=steps, trace=trace_list)

    def accepts(self, word: str) -> bool:
        return self.run(word).accepted