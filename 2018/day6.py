import numpy as np
import logging as lg
lg.basicConfig(level=lg.DEBUG, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s", datefmt="%H:%M:%S")
_logger = lg.getLogger(__name__)

points = np.loadtxt("input_day6.txt", dtype=np.int16, delimiter=", ")
_logger.debug("points.shape: {}".format(points.shape))

points -= points.min(axis=0) - 1
bbox_size = points.max(axis=0) + 3

grid = [
    np.broadcast_to(np.arange(bbox_size[0])[:, None], bbox_size),
    np.broadcast_to(np.arange(bbox_size[1])[None, :], bbox_size)]
grid = np.stack(grid, axis=2)
dists = np.linalg.norm(grid[:, :, None, :] - points[None, None, :], ord=1, axis=3)

nearest = np.argmin(dists, axis=2)
nearest2 = len(points) - 1 - np.argmin(dists[..., ::-1], axis=2)
_logger.debug("number of ties: {} / {}".format(np.sum(nearest != nearest2), nearest.size))
# _logger.debug(nearest[120:130, 100:110])
# _logger.debug(nearest2[120:130, 100:110])
nearest[nearest != nearest2] = 2**16 - 1  # remove ties
# _logger.debug(nearest[120:130, 100:110])
_logger.debug("nearest.shape: {}".format(nearest.shape))

bdys = np.concatenate([nearest[:, 0], nearest[0, :], nearest[:, -1], nearest[-1, :]], axis=0)
bdy_js = np.unique(bdys)
_logger.debug("Points with infite areas: {}".format(bdy_js))
max_size = 0
max_j = 0
for j in range(len(points)):
    if j in bdy_js:
        continue
    size_j = np.sum(nearest == j)
    _logger.debug("Size of area {}: {}".format(j, size_j))
    if size_j > max_size:
        max_size = size_j
        max_j = j
print("Answer pt1:", max_size)

print("Answer pt2:", np.sum(np.sum(dists, axis=2) < 10000))
