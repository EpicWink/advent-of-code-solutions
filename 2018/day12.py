import time
import pathlib
import logging as lg
import functools as ft

import numpy as np

lg.basicConfig(
    level=lg.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S")
_logger = lg.getLogger(__name__)


class PlantSimulate:
    _pad = np.zeros((4,), dtype=np.bool8)

    def __init__(self, init_state, kernels):
        self.init_state = init_state
        self.kernels = kernels
        self.generation = 0
        self.current_state = self.init_state
        self.offset = 0
        self._states = [self.init_state]

    @classmethod
    def from_data_str(cls, data_str):
        def get_arr(text):
            return np.array([c == "#" for c in text], dtype=np.bool8)

        lines = data_str.splitlines()
        init_state = get_arr(lines[0][15:].strip())
        kernels = [(get_arr(line[:5]), line[9] == "#") for line in lines[2:]]
        return cls(init_state, kernels)

    def _find_pattern(self):
        for j in range(1, len(self._states) // 2 - 1):
            states1 = self._states[-2 * j:-j]
            states2 = self._states[-j:]
            assert len(states1) == len(states2)
            for state1, state2 in zip(states1, states2):
                if not np.array_equal(state1, state2):
                    break
            else:
                _s = "Found repeating pattern at generation {} with period {}"
                _logger.debug(_s.format(self.generation, j))
                return j
        return False

    def step(self):
        old_state_padded = np.concatenate([self._pad, self.current_state, self._pad])
        old_state_view = np.lib.stride_tricks.as_strided(
            old_state_padded,
            (len(old_state_padded) - 4, 5),
            (1, 1))
        new_state = np.zeros((len(old_state_view),), dtype=np.bool8)
        for kernel, has_plant in self.kernels:
            new_state[np.all(old_state_view == kernel, axis=1)] = has_plant
        lowest_j = np.argmax(new_state)
        highest_j = len(new_state) - np.argmax(new_state[::-1]) + 1
        self.offset += lowest_j - 2
        self.current_state = new_state[lowest_j:highest_j]
        self.generation += 1
        self._states.append(self.current_state)
        _logger.debug("generation: {}, offset: {}".format(self.generation, self.offset))

    def run(self, n=0):
        for j in range(n):
            if j % 10000 == 0:
                _logger.debug("{} / {}".format(j, n))
            self.step()
            self._find_pattern()

    def get_plant_pot_sum(self):
        return np.sum(np.nonzero(self.current_state)[0] + self.offset)


def main():
    data_str = pathlib.Path("input_day12.txt").read_text()
    sim = PlantSimulate.from_data_str(data_str)
    sim.run(n=200)
    _logger.debug("sim.init_state.shape: {}".format(sim.init_state.shape))
    _logger.debug("sim.generation: {}".format(sim.generation))
    # _logger.debug("sim.current_state: {}".format(sim.current_state))
    _logger.debug("sim.offset: {}".format(sim.offset))
    print("Answer:", sim.get_plant_pot_sum())
    print("Answer pt2:", np.sum(np.nonzero(sim.current_state)[0] + 5 * 10**10 - 36))


if __name__ == "__main__":
    main()
