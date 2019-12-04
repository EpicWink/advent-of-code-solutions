"""Day 2 solution.

https://adventofcode.com/2019/day/2
"""

import logging as lg

import _common
import numpy as np

logger = lg.getLogger(__name__)


class Halt(Exception):  # TODO: unit-test, document
    pass


def state_from_text(text):  # TODO: unit-test, document
    items = text.strip().split(",")
    items = [int(item) for item in items]
    return np.array(items)


class Program:  # TODO: unit-test, document
    def __init__(self, state):
        self.state = state
        self.initial_state = state.copy()
        self.head = 0
        self.ops = {
            1: lambda a, b: a + b,
            2: lambda a, b: a * b,
            99: None
        }
        self.opcode = None
        self.a_idx = None
        self.b_idx = None
        self.c_idx = None

    @property
    def output(self):
        return self.state[0]

    def step(self):
        self.opcode = self.state[self.head]
        op = self.ops[self.opcode]
        if op is None:
            raise Halt
        self.a_idx, self.b_idx, self.c_idx = self.state[self.head + 1:self.head + 4]
        a = self.state[self.a_idx]
        b = self.state[self.b_idx]
        res = op(a, b)
        self.state[self.c_idx] = res
        self.head += 4

    def run(self):
        while True:
            try:
                self.step()
            except Halt:
                break
            except Exception:
                logger.debug("head: {}".format(self.head))
                logger.debug("opcode: {}".format(self.opcode))
                logger.debug("a_idx: {}".format(self.a_idx))
                logger.debug("b_idx: {}".format(self.b_idx))
                logger.debug("c_idx: {}".format(self.c_idx))
                raise


class Solution(_common.InputtedSolution):  # TODO: unit-test, document
    year = 2019
    day = 2

    def part_1(self):
        state = state_from_text(self.input_text)
        state[1] = 12
        state[2] = 2
        program = Program(state)
        program.run()
        return program.output

    def part_2(self):
        state = state_from_text(self.input_text)
        jks = ((j, k) for j in range(100) for k in range(100))
        for j, k in jks:
            state_attempt = state.copy()
            state_attempt[1] = j
            state_attempt[2] = k
            program = Program(state_attempt)
            program.run()
            if program.output == 19690720:
                break
        else:
            raise RuntimeError("No valid values found")
        return 100 * j + k


main = Solution.main
if __name__ == "__main__":  # pragma: no cover
    main()
