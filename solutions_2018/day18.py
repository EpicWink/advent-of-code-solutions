"""Day 18 solution.

https://adventofcode.com/2018/day/18
"""

import logging as lg

import numpy as np
import _common

_logger = lg.getLogger(__name__)


class LCA:
    def __init__(self, acres):
        self.acres = acres

    @classmethod
    def from_data_str(cls, data_str):
        lines = data_str.strip().splitlines()
        width = len(lines[0])
        height = len(lines)
        acres = np.zeros((height, width), dtype=np.uint8)
        type_map = {".": 1, "|": 2, "#": 3}
        for j, line in enumerate(lines):
            for k, char in enumerate(line):
                acres[j, k] = type_map[char]
        return cls(acres)

    @property
    def size(self):
        return self.acres.shape

    def copy(self):
        return type(self)(self.acres.copy())

    def format_acres(self):
        type_map = [" ", ".", "|", "#"]
        return "\n".join("".join(type_map[el] for el in row) for row in self.acres)


class StrangeMagic:
    def __init__(self, initial_lca):
        self.initial_lca = initial_lca
        self.lca = initial_lca.copy()
        self._ds = np.array(
            [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)],
            dtype=np.int8)
        self._valid_adjs = None

    @_common.record_call_times
    def _compute_valid_adjacent_positions(self):
        if self._valid_adjs is not None:
            _logger.info("Already computed valid adjacent positions")
            return
        ds = np.array(
            [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)],
            dtype=np.int8)
        sy, sx = self.lca.size
        assert all(s < 64 for s in self.lca.size)

        valid_adjs = [None] * sy
        for j in range(sy):
            row_valid_adjs = [None] * sx
            for k in range(sx):
                adj = ds + (j, k)
                valid_adj = adj[
                    (adj[:, 0] >= 0)
                    & (adj[:, 0] < sy)
                    & (adj[:, 1] >= 0)
                    & (adj[:, 1] < sx)]
                row_valid_adjs[k] = valid_adj
            valid_adjs[j] = row_valid_adjs
        self._valid_adjs = valid_adjs

    @_common.record_call_times
    def _get_new_type(self, pos):
        valid_adj = self._valid_adjs[pos[0]][pos[1]]
        adj_types = self.lca.acres[valid_adj[:, 0], valid_adj[:, 1]]
        cur_type = self.lca.acres[pos]
        if cur_type == 1 and (adj_types == 2).sum() >= 3:
            return 2
        elif cur_type == 2 and (adj_types == 3).sum() >= 3:
            return 3
        elif cur_type == 3 and ((adj_types == 3).sum() < 1 or (adj_types == 2).sum() < 1):
            return 1
        return cur_type

    @_common.record_call_times
    def step(self):
        new_acres = np.zeros_like(self.lca.acres)
        for j, row in enumerate(self.lca.acres):
            for k, el in enumerate(row):
                new_acres[j, k] = self._get_new_type((j, k))
        self.lca.acres = new_acres

    def run(self, n_steps):
        self._compute_valid_adjacent_positions()
        for j in range(n_steps):
            self.step()
            if j % 50 == 49:
                _s = "Completed step {}, resource value: {}"
                _logger.debug(_s.format(j + 1, self.resource_value))

    @property
    @_common.record_call_times
    def resource_value(self):
        return (self.lca.acres == 2).sum() * (self.lca.acres == 3).sum()


class Solution(_common.InputtedSolution):  # TODO: unit-test, document
    def __init__(self):
        super().__init__()
        self.lca = None

    def parse(self):
        super().parse()
        self.lca = LCA.from_data_str(self.input_text)

    def part_1(self):
        strange_magic = StrangeMagic(self.lca)
        strange_magic.run(10)
        return strange_magic.resource_value

    def part_2(self):
        strange_magic = StrangeMagic(self.lca)
        strange_magic.run(1000000000)
        return strange_magic.resource_value


main = Solution.main
if __name__ == "__main__":  # pragma: no cover
    main()
