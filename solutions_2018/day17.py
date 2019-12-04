"""Day 17 solution.

https://adventofcode.com/2018/day/17
"""

import logging as lg

import numpy as np
import _common

_logger = lg.getLogger(__name__)


class Scan:
    def __init__(self, is_clay, grid_min_x):
        self.is_clay = is_clay
        self.grid_min_x = grid_min_x

    @property
    def size(self):
        return self.is_clay.shape

    @classmethod
    def from_data_str(cls, data_str):
        clay_pts = []
        for line in data_str.strip().splitlines():
            left_part, right_parts = line.split(", ")
            single_coord = int(left_part[2:])
            multi_coords = tuple(map(int, right_parts[2:].split("..")))
            multi_coords = tuple(range(multi_coords[0], multi_coords[1] + 1))
            for coord in multi_coords:
                pt = (single_coord, coord) if left_part[0] == "y" else (coord, single_coord)
                clay_pts.append(pt)
        clay_pts = np.array(clay_pts)
        min_x = clay_pts[:, 1].min() - 1
        max_pt = clay_pts.max(axis=0)
        size = (max_pt[0] + 1, max_pt[1] - min_x + 2)
        is_clay = np.zeros(size, dtype=np.bool8)
        _logger.debug("clay_pts.shape: {}".format(clay_pts.shape))
        _logger.debug("min_x: {}".format(min_x))
        _logger.debug("max_pt: {}".format(max_pt))
        _logger.debug("size: {}".format(size))
        _logger.debug("is_clay.shape: {}".format(is_clay.shape))
        clay_pts_sh = clay_pts - (0, min_x)
        is_clay[clay_pts_sh[:, 0], clay_pts_sh[:, 1]] = True
        return cls(is_clay, min_x)

    def format_clay(self):
        return "\n".join("".join("#" if el else "." for el in row) for row in self.is_clay)


class WaterFlow:
    def __init__(self, scan, spring_location=(0, 500)):
        self.scan = scan
        self.spring_location = spring_location
        self._water = np.zeros(scan.size, dtype=np.bool8)
        self._water_touched = np.zeros(scan.size, dtype=np.bool8)
        self._spring_location_sh = (
            self.spring_location[0],
            self.spring_location[1] - self.scan.grid_min_x)
        self._water_pts = []

    def _available(self, pos):
        if pos[0] > self.scan.size[0] - 1 or pos[1] < 0 or pos[1] > self.scan.size[1] - 1:
            return False
        return not self._water[pos] and not self.scan.is_clay[pos] and pos not in self._water_pts

    def _update_water_pos(self, old_pos):
        below = (old_pos[0] + 1, old_pos[1])
        if self._available(below):
            return below

        left = (old_pos[0], old_pos[1] - 1)
        right = (old_pos[0], old_pos[1] + 1)
        can_go_left = self._available(left)
        can_go_right = self._available(right)
        if can_go_left and not self._water_touched[left]:  # prefer going where not already gone
            return left
        elif can_go_right and not self._water_touched[right]:
            return right
        elif can_go_left:
            return left
        elif can_go_right:
            return right
        return None

        # left_blocked = self._water[left] or self.scan.is_clay[left]
        # right_blocked = self._water[right] or self.scan.is_clay[right]
        # if left_blocked and right_blocked:
        #     print("Drop stopped at {}".format(old_pos))
        #     self._water[old_pos] = True
        #     return None  # can't go anwhere
        # return old_pos  # can't go anwhere for now (keep simulating)

    def _drop_at_bottom(self, pos):
        return pos[0] >= self.scan.size[0] - 1

    def _update_water_pts(self):
        self._water_pts.sort(key=lambda x: -x[0])
        to_remove = []
        updated = False
        for j, pos in enumerate(self._water_pts):
            self._water_touched[pos] = True
            if self._drop_at_bottom(pos):
                # print("Removing drop {} at {} falling off scan".format(j, pos))
                to_remove.append(j)
            new_pos = self._update_water_pos(pos)
            if new_pos is None:
                # print("Removing stopped drop {} at {}".format(j, pos))
                self._water[pos] = True
                to_remove.append(j)
            elif new_pos != pos:
                updated = True
                self._water_pts[j] = new_pos
                # print("Drop {}: {} -> {}".format(j, pos, new_pos))
        [self._water_pts.pop(j) for j in reversed(to_remove)]
        return updated

    def _moving_water_changed(self, old_water_pts):
        return set(old_water_pts) != set(self._water_pts)

    def _stopped_water_changed(self, old_water):
        return not np.array_equal(old_water, self._water)

    def _water_touched_changed(self, old_water_touched):
        return not np.array_equal(old_water_touched, self._water_touched)

    def simulate(self):
        import time
        one_below_spring = (self._spring_location_sh[0] + 1, self._spring_location_sh[1])
        self._water_pts.append(one_below_spring)
        j = 0
        while True:
            old_water_touched = self._water_touched.copy()
            old_water = self._water.copy()
            old_water_pts = self._water_pts.copy()
            self._update_water_pts()
            self._water_pts.append(one_below_spring)
            print(self.format_water(include_running=True))
            time.sleep(0.2)
            # if not np.any(self._water_touched[-1]):
            #     continue
            if self._moving_water_changed(old_water_pts):
                continue
            if not self._stopped_water_changed(old_water) and not self._water_touched_changed(old_water_touched):
                break
            j += 1
            _logger.debug("Completed simulation step: {}".format(j))

        _logger.debug("Water-adding finished. Finalising drops")
        self._water_pts = [tuple(pos) for pos in np.argwhere(self._water).tolist()]
        self._water[:] = False
        while True:
            old_water_touched = self._water_touched.copy()
            old_water = self._water.copy()
            old_water_pts = self._water_pts.copy()
            self._update_water_pts()
            print(self.format_water(include_running=True))
            time.sleep(0.2)
            # if not np.any(self._water_touched[-1]):
            #     continue
            if self._moving_water_changed(old_water_pts):
                continue
            if not self._stopped_water_changed(old_water) and not self._water_touched_changed(old_water_touched):
                break
            j += 1
            _logger.debug("Completed simulation step: {}".format(j))


    @property
    def n_touched(self):
        return self._water_touched.sum()

    def format_water(self, include_running=False):
        chars = np.full(self.scan.size, ".")
        chars[self.scan.is_clay] = "#"
        chars[self._water_touched] = "|"
        if include_running:
            for pos in self._water_pts:
                chars[pos] = "o"
        chars[self._water] = "~"
        chars[self._spring_location_sh] = "+"
        return "\n".join("".join(map(str, row)) for row in chars)


class Solution(_common.InputtedSolution):  # TODO: unit-test, document
    def __init__(self):
        super().__init__()
        self.scan = None
        self.simulation = None

    def parse(self):
        super().parse()
        self.scan = Scan.from_data_str(self.input_text)
        # print(self.scan.format_clay())
        self.simulation = WaterFlow(self.scan)

    def part_1(self):
        self.simulation.simulate()
        return self.simulation.n_touched

    def part_2(self):  # TODO: implement
        return None


main = Solution.main
if __name__ == "__main__":  # pragma: no cover
    main()
