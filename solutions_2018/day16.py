"""Day 16 solution.

https://adventofcode.com/2018/day/16
"""

import logging as lg

import numpy as np
import _common

_logger = lg.getLogger(__name__)


class State:
    __slots__ = ("r1", "r2", "r3", "r4")

    def __init__(self, r1: int, r2: int, r3: int, r4: int):
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
        self.r4 = r4

    def __str__(self):
        return "({}, {}, {}, {})".format(self.r1, self.r2, self.r3, self.r4)

    def __repr__(self):
        return "{}({}, {}, {}, {})".format(
            type(self).__name__,
            repr(self.r1),
            repr(self.r2),
            repr(self.r3),
            repr(self.r4))

    def __getitem__(self, idx: int):
        if idx == 0:
            return self.r1
        elif idx == 1:
            return self.r2
        elif idx == 2:
            return self.r3
        elif idx == 3:
            return self.r4
        else:
            raise IndexError(idx)

    def __setitem__(self, idx: int, value: int):
        if idx == 0:
            self.r1 = value
        elif idx == 1:
            self.r2 = value
        elif idx == 2:
            self.r3 = value
        elif idx == 3:
            self.r4 = value
        else:
            raise IndexError(idx)

    def __eq__(self, other):
        if not isinstance(self, type(other)):
            return NotImplemented
        return (
            self.r1 == other.r1
            and self.r2 == other.r2
            and self.r3 == other.r3
            and self.r4 == other.r4)

    def copy(self):
        return type(self)(self.r1, self.r2, self.r3, self.r4)


class Instruction:
    __slots__ = ("opcode", "a", "b", "c")

    def __init__(self, opcode: int, a: int, b: int, c: int):
        self.opcode = opcode
        self.a = a
        self.b = b
        self.c = c

    @classmethod
    def from_str(cls, instruction_str: str):
        return cls(*map(int, instruction_str.strip().split()))


class Operations:
    def __init__(self):
        self.operations = {}
        self._finalised = False
        self.opnames = None

    def register_operation(self, fn):
        if self._finalised:
            raise RuntimeError("Operations set finalised")
        def wrapped(a: int, b: int, c: int, state: State):
            state[c] = fn(a, b, state)
        self.operations[fn.__name__] = wrapped
        return fn

    def apply(self, instruction: Instruction, state: State, opname: str = None):
        if opname is None:
            opname = self.opnames[instruction.opcode]
        self.operations[opname](instruction.a, instruction.b, instruction.c, state)

    def apply_all(self, instruction: Instruction, state: State):
        result_states = {}
        for opname in self.operations:
            result_state = state.copy()
            self.apply(instruction, result_state, opname=opname)
            result_states[opname] = result_state
        return result_states

    def finalise(self):
        self._finalised = True
        self.opnames = tuple(self.operations)


operations = Operations()


@operations.register_operation
def addr(a, b, state):
    return state[a] + state[b]


@operations.register_operation
def addi(a, b, state):
    return state[a] + b


@operations.register_operation
def mulr(a, b, state):
    return state[a] * state[b]


@operations.register_operation
def muli(a, b, state):
    return state[a] * b


@operations.register_operation
def banr(a, b, state):
    return state[a] & state[b]


@operations.register_operation
def bani(a, b, state):
    return state[a] & b


@operations.register_operation
def borr(a, b, state):
    return state[a] | state[b]


@operations.register_operation
def bori(a, b, state):
    return state[a] | b


@operations.register_operation
def setr(a, b, state):
    return state[a]


@operations.register_operation
def seti(a, b, state):
    return a


@operations.register_operation
def gtir(a, b, state):
    return 1 if a > state[b] else 0


@operations.register_operation
def gtri(a, b, state):
    return 1 if state[a] > b else 0


@operations.register_operation
def gtrr(a, b, state):
    return 1 if state[a] > state[b] else 0


@operations.register_operation
def eqir(a, b, state):
    return 1 if a == state[b] else 0


@operations.register_operation
def eqri(a, b, state):
    return 1 if state[a] == b else 0


@operations.register_operation
def eqrr(a, b, state):
    return 1 if state[a] == state[b] else 0


operations.finalise()


class BeforeNAfter:
    __slots__ = ("before_state", "after_state", "instruction", "_valid_ops_cache")
    _state_class = State
    _instruction_class = Instruction

    def __init__(self, before_state: State, after_state: State, instruction: Instruction = None):
        self.before_state = before_state
        self.after_state = after_state
        self.instruction = instruction
        self._valid_ops_cache = None

    @classmethod
    def from_lines(cls, lines: list):
        lines = [line for line in lines if line]
        assert lines[0].startswith("Before: ")
        assert lines[2].startswith("After: ")
        before_state = cls._state_class(*map(int, lines[0][9:19].split(", ")))
        after_state = cls._state_class(*map(int, lines[2][9:19].split(", ")))
        instruction = cls._instruction_class.from_str(lines[1])
        return cls(before_state, after_state, instruction=instruction)

    @property
    def valid_ops(self):
        if self._valid_ops_cache is None:
            result_states = operations.apply_all(self.instruction, self.before_state)
            valid_opnames = []
            for opname, result_state in result_states.items():
                if result_state == self.after_state:
                    valid_opnames.append(opname)
            self._valid_ops_cache = valid_opnames
        return self._valid_ops_cache


class Program:
    _instruction_class = Instruction
    _state_class = State

    def __init__(self, instructions: list, init_state: _state_class = None):
        self.instructions = instructions
        self.init_state = init_state or self._state_class(0, 0, 0, 0)
        self.state = self.init_state.copy()

    def run(self):
        for instruction in self.instructions:
            operations.apply(instruction, self.state)

    @classmethod
    def from_lines(cls, lines):
        instructions = [cls._instruction_class.from_str(line) for line in lines]
        return cls(instructions)


def get_validity_matrix(bnas: list):
    n_ops = len(operations.opnames)
    validity = np.ones((len(bnas), n_ops, n_ops), dtype=np.bool8)
    for j, bna in enumerate(bnas):
        validity[j, bna.instruction.opcode] = False  # 16 falses
        for valid_op in bna.valid_ops:
            validity[j, bna.instruction.opcode, operations.opnames.index(valid_op)] = True
    validity = np.all(validity, axis=0)
    return validity


def reduce_validity(validity: np.ndarray):
    n_ops = len(operations.opnames)
    while np.sum(validity) > n_ops:
        for j in range(n_ops):
            if np.sum(validity[j]) == 1:
                k = np.argwhere(validity[j])[0, 0]
                _logger.debug("Setting column {} to False except row {}".format(k, j))
                validity[:, k] = False
                validity[j, k] = True
        if not np.all(np.any(validity, axis=1)):
            return None
        for j in range(n_ops):
            if np.sum(validity[j]) == 1:
                continue
            for k in range(n_ops):
                if not validity[j, k]:
                    continue
                _logger.debug("Attempting reduction by setting row {} to {}".format(j, k))
                validity_temp = validity.copy()
                validity_temp[j] = False
                validity_temp[j, k] = True
                validity_reduced = reduce_validity(validity_temp)
                if validity_reduced is not None:
                    _logger.debug("Reduction by setting row {} to {} succeeded".format(j, k))
                    validity = validity_reduced
                    break
                _logger.debug("Reduction by setting row {} to {} failed".format(j, k))
            else:
                continue
            break
    return validity


def update_op_names(validity: np.ndarray):
    idxs = [np.argwhere(row)[0, 0] for row in validity]
    operations.opnames = tuple(operations.opnames[j] for j in idxs)
    _logger.debug("Opnames: {}".format(", ".join(operations.opnames)))


class Solution(_common.InputLinesSolution):  # TODO: unit-test, document
    def __init__(self):
        super().__init__()
        self.bnas = None

    def part_1(self):
        self.bnas = [BeforeNAfter.from_lines(self.items[j:j + 4]) for j in range(0, 3244, 4)]
        return len([bna for bna in self.bnas if len(bna.valid_ops) > 2])

    def part_2(self):
        validity = get_validity_matrix(self.bnas)
        _logger.debug("Initial validity matrix:\n{}".format(validity.astype(np.uint8)))

        validity = reduce_validity(validity.copy())
        assert np.array_equal(
            np.sum(validity, axis=1),
            np.ones((validity.shape[0],), dtype=np.uint8))
        assert np.array_equal(
            np.sum(validity, axis=0),
            np.ones((validity.shape[1],), dtype=np.uint8))
        _logger.debug("Reduced validity matrix:\n{}".format(validity.astype(np.uint8)))

        update_op_names(validity)

        program = Program.from_lines(self.items[3246:])
        program.run()
        _logger.debug("Final program state: {}".format(program.state))
        return program.state[0]


def main():  # pragma: no cover
    Solution().run()


if __name__ == "__main__":  # pragma: no cover
    main()
