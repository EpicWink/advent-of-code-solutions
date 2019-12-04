"""Day 19 solution.

https://adventofcode.com/2018/day/19
"""

import logging as lg

import _common

_logger = lg.getLogger(__name__)


class State:
    __slots__ = ("r1", "r2", "r3", "r4", "r5", "r6")

    def __init__(self, r1: int, r2: int, r3: int, r4: int, r5: int, r6: int):
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
        self.r4 = r4
        self.r5 = r5
        self.r6 = r6

    def __str__(self):
        _s = "({}, {}, {}, {}, {}, {})"
        return _s.format(self.r1, self.r2, self.r3, self.r4, self.r5, self.r6)

    def __repr__(self):
        return "{}({}, {}, {}, {}, {}, {})".format(
            type(self).__name__,
            repr(self.r1),
            repr(self.r2),
            repr(self.r3),
            repr(self.r4),
            repr(self.r5),
            repr(self.r6))

    def __getitem__(self, idx: int):
        return getattr(self, self.__slots__[idx])
        # if idx == 0:
        #     return self.r1
        # elif idx == 1:
        #     return self.r2
        # elif idx == 2:
        #     return self.r3
        # elif idx == 3:
        #     return self.r4
        # elif idx == 4:
        #     return self.r5
        # elif idx == 5:
        #     return self.r6
        # else:
        #     raise IndexError(idx)

    def __setitem__(self, idx: int, value: int):
        setattr(self, self.__slots__[idx], value)
        # if idx == 0:
        #     self.r1 = value
        # elif idx == 1:
        #     self.r2 = value
        # elif idx == 2:
        #     self.r3 = value
        # elif idx == 3:
        #     self.r4 = value
        # elif idx == 4:
        #     self.r5 = value
        # elif idx == 5:
        #     self.r6 = value
        # else:
        #     raise IndexError(idx)

    def __eq__(self, other):
        if not isinstance(self, type(other)):
            return NotImplemented
        return (
            self.r1 == other.r1
            and self.r2 == other.r2
            and self.r3 == other.r3
            and self.r4 == other.r4
            and self.r5 == other.r5
            and self.r6 == other.r6)

    def copy(self):
        return type(self)(self.r1, self.r2, self.r3, self.r4, self.r5, self.r6)


class Instruction:
    __slots__ = ("opcode", "a", "b", "c")

    def __init__(self, opcode: str, a: int, b: int, c: int):
        self.opcode = opcode
        self.a = a
        self.b = b
        self.c = c

    @classmethod
    def from_str(cls, instruction_str: str):
        vals = instruction_str.strip().split()
        return cls(vals[0], *map(int, vals[1:]))


class Operations:
    def __init__(self):
        self.operations = {}

    def register_operation(self, fn):
        def wrapped(a: int, b: int, c: int, state: State):
            state[c] = fn(a, b, state)
        self.operations[fn.__name__] = wrapped
        return fn

    def apply(self, instruction: Instruction, state: State):
        self.operations[instruction.opcode](instruction.a, instruction.b, instruction.c, state)


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


class Program:
    _instruction_class = Instruction
    _state_class = State

    def __init__(
            self,
            instructions: list,
            instruction_pointer_register: int,
            init_state: _state_class = None):
        self.instructions = instructions
        self.instruction_pointer_register = instruction_pointer_register
        self.init_state = init_state or self._state_class(0, 0, 0, 0, 0, 0)
        self.state = self.init_state.copy()
        self.instruction_idx = 0
        assert self.init_state[self.instruction_pointer_register] == 0

    @classmethod
    def from_data_str(cls, data_str: str):
        lines = data_str.strip().splitlines()
        assert lines[0].startswith("#ip ")
        ipr = int(lines[0][4])
        instructions = [cls._instruction_class.from_str(line) for line in lines[1:]]
        return cls(instructions, ipr)

    @property
    def has_valid_instruction_idx(self):
        return 0 <= self.instruction_idx < len(self.instructions)

    def step(self):
        self.state[self.instruction_pointer_register] = self.instruction_idx
        operations.apply(self.instructions[self.instruction_idx], self.state)
        self.instruction_idx = self.state[self.instruction_pointer_register]
        self.instruction_idx += 1

    def run(self):
        if not self.has_valid_instruction_idx:
            _logger.warning("Program already finished")
        _logger.info("Running program")
        j = 0
        while self.has_valid_instruction_idx:
            self.step()
            if j % 100000 == 99999:
                _logger.debug("Finished step {}, state: {}".format(j + 1, self.state))
            j += 1
        _logger.info("Program finished after {} steps with state: {}".format(j, self.state))


class Solution(_common.InputtedSolution):  # TODO: unit-test, document
    def __init__(self):
        super().__init__()
        self.part_1_program = None

    def part_1(self):
        program = Program.from_data_str(self.input_text)
        program.run()
        self.part_1_program = program
        return program.state[0]

    def part_2(self):
        new_init_state = self.part_1_program.init_state.copy()
        new_init_state[0] = 1
        program = Program(
            self.part_1_program.instructions,
            self.part_1_program.instruction_pointer_register,
            init_state=new_init_state)
        # for j, v in enumerate((42, 10551260, 9366059, 22519, 10, 0)):
        #     program.state[j] = v
        # program.instruction_idx = program.state[4] + 1
        program.run()
        return program.state[0]


main = Solution.main
if __name__ == "__main__":  # pragma: no cover
    main()
