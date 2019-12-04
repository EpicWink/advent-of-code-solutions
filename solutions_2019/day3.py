"""Day 3 solution.

https://adventofcode.com/2019/day/3
"""

import _common
import numpy as np


def get_movement_from_str(text):
    if text[0] == "U":
        return int(text[1:]), 0
    elif text[0] == "D":
        return -int(text[1:]), 0
    elif text[0] == "R":
        return 0, int(text[1:])
    elif text[0] == "L":
        return 0, -int(text[1:])
    else:
        raise ValueError(text)


def get_vertices(movements):  # TODO: unit-test, document
    vertices = np.empty((len(movements) + 1, 2), dtype=np.int32)
    vertices[0] = 0
    for j, movement in enumerate(movements):
        vertices[j + 1] = vertices[j] + movement
    return vertices


def construct_grid(vertices_1, vertices_2):
    vertices = np.concatenate([vertices_1, vertices_2], axis=0)
    min_ = vertices.min(axis=0)
    max_ = vertices.max(axis=0)
    grid = np.zeros(max_ - min_, dtype=np.bool8)
    return grid, (-min_[0], -min_[1])


def fill_grid(movements, grid, centre):
    position = np.array(centre)
    for movement in movements:
        assert movement[0] == 0 or movement[1] == 0
        for j in range(abs(movement[0])):
            if movement[0] < 0:
                j = -j
            grid[centre[0] + j, centre[1]] = True
        for j in range(abs(movement[1])):
            if movement[1] < 0:
                j = -j
            grid[centre[0], centre[1] + j] = True
        position += movement


def part_1(movements_1, movements_2):  # TODO: unit-test, document
    vertices_1 = get_vertices(movements_1)
    vertices_2 = get_vertices(movements_2)
    grid, centre = construct_grid(vertices_1, vertices_2)
    grid_1 = grid.copy()
    grid_2 = grid.copy()
    fill_grid(movements_1, grid_1, centre)
    fill_grid(movements_2, grid_2, centre)
    intersects = grid_1 & grid_2
    intersects[centre[0], centre[1]] = False
    intersections = np.argwhere(intersects)
    intersections -= centre
    distances = np.sum(np.abs(intersections), axis=1)
    return np.min(distances)
    # idx = np.argmin(distances)
    # return intersections[idx]


class Wires:
    def __init__(self, movements_1_line, movements_2_line):
        self.movements_1_line = movements_1_line
        self.movements_2_line = movements_2_line
        self.movements_1 = None
        self.movements_2 = None
        self.intersection_distance = None

    def run(self):
        movements_1_texts = self.movements_1_line.strip().split(",")
        movements_2_texts = self.movements_2_line.strip().split(",")
        self.movements_1 = [get_movement_from_str(s) for s in movements_1_texts]
        self.movements_2 = [get_movement_from_str(s) for s in movements_2_texts]
        self.intersection_distance = part_1(self.movements_1, self.movements_2)


class Solution(_common.InputLinesSolution):  # TODO: unit-test, document
    year = 2019
    day = 3

    def part_1(self):
        wires = Wires(*self.items)
        wires.run()
        return wires.intersection_distance

    def part_2(self):
        return None


main = Solution.main
if __name__ == "__main__":  # pragma: no cover
    main()
