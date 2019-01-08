import pathlib
import logging as lg

import numpy as np

lg.basicConfig(
    level=lg.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S")
_logger = lg.getLogger(__name__)


def parse_data(data_str):
    pts = []
    vs = []
    for line in data_str.strip().splitlines():
        x = int(line[10:16].strip())
        y = int(line[18:24].strip())
        vx = int(line[36:38].strip())
        vy = int(line[40:42].strip())
        pts.append((y, x))
        vs.append((vy, vx))
    return np.array(pts), np.array(vs)


def print_points(points):
    size = points.ptp(axis=0) + 1
    points = points - points.min(axis=0)
    grid = np.zeros(size, dtype=np.uint8)
    grid[points[:, 0], points[:, 1]] = 1
    print("\n".join("".join(("#" if el else " ") for el in row) for row in grid))


def main_loop(points, velocities):
    j = 0
    while True:
        points += velocities
        if np.all(points.ptp(axis=0) < (88, 317)):
            _logger.debug("Second {}".format(j))
            print_points(points)
            input("Press enter to continue (CTRL+C to quit)")
        j += 1


def main():
    data_str = pathlib.Path("input_day10.txt").read_text()
    points, velocities = parse_data(data_str)
    main_loop(points, velocities)


if __name__ == "__main__":
    main()
