import time
import logging as lg
import functools as ft

import numpy as np

lg.basicConfig(
    level=lg.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S")
_logger = lg.getLogger(__name__)


def cached_property(fn):
    @ft.wraps(fn)
    def wrapped(self):
        if not hasattr(self, "__cache__"):
            self.__cache__ = {}
        if fn.__name__ not in self.__cache__:
            self.__cache__[fn.__name__] = fn(self)
        return self.__cache__[fn.__name__]
    return property(wrapped)


class Grid:
    ys = np.broadcast_to(np.arange(300)[:, None], (300, 300)) + 1
    xs = np.broadcast_to(np.arange(300)[None, :], (300, 300)) + 1
    coords = np.stack([ys, xs], axis=2)
    rack_ids = xs + 10

    def __init__(self, serial, window_size=3):
        self.serial = serial
        self.window_size = window_size

    @cached_property
    def power_levels(self):
        return ((self.rack_ids * self.ys + self.serial) * self.rack_ids // 100) % 10 - 5

    @cached_property
    def _windows(self):
        _ws = self.window_size
        return np.lib.stride_tricks.as_strided(
            self.power_levels,
            (300 - _ws + 1, 300 - _ws + 1, _ws, _ws),
            self.power_levels.strides * 2)

    @cached_property
    def window_sums(self):
        return np.sum(self._windows, axis=(2, 3))

    @cached_property
    def best_sum_coord(self):
        return np.unravel_index(np.argmax(self.window_sums), self.window_sums.shape)


def main():
    _logger.debug("{} @ {},{}".format(Grid(57).power_levels[78, 121], 122, 79))
    _logger.debug("{} @ {},{}".format(Grid(39).power_levels[195, 216], 217, 196))
    _logger.debug("{} @ {},{}".format(Grid(71).power_levels[152, 100], 101, 153))
    _g18 = Grid(18)
    _logger.debug("{}\n{}".format(_g18.window_sums[44, 32], _g18.power_levels[43:48, 31:36]))
    _g42 = Grid(42)
    _logger.debug("{}\n{}".format(_g42.window_sums[60, 20], _g42.power_levels[59:63, 19:24]))
    _g42 = Grid(18, window_size=16)
    _logger.debug("90,269,16: {}".format(_g42.window_sums[268, 89]))
    _g42 = Grid(42, window_size=12)
    _logger.debug("232,251,12: {}".format(_g42.window_sums[250, 231]))

    serial = int(input("Enter serial number: "))

    grid = Grid(serial)
    _logger.debug("max_coord: {}".format(grid.best_sum_coord))
    _logger.debug("best sum: {}".format(grid.window_sums[grid.best_sum_coord]))
    print("Answer pt1: {},{}".format(grid.best_sum_coord[1] + 1, grid.best_sum_coord[0] + 1))

    t = time.time()
    best_grid = Grid(serial, window_size=1)
    for j in range(2, 300):
        grid = Grid(serial, window_size=j)
        if grid.window_sums[grid.best_sum_coord] > best_grid.window_sums[best_grid.best_sum_coord]:
            best_grid = grid
    best_coord = best_grid.best_sum_coord
    best_window_size = best_grid.window_size
    _logger.debug("best sum: {}".format(best_grid.window_sums[best_coord]))
    print("Answer pt2: {},{},{}".format(best_coord[1] + 1, best_coord[0] + 1, best_window_size))
    _logger.debug("Finished in {:.2f} seconds".format(time.time() - t))


if __name__ == "__main__":
    main()
