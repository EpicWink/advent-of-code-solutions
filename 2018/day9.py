import logging as lg
import time

lg.basicConfig(
    level=lg.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S")
_logger = lg.getLogger(__name__)

n_players = int(input("Number of players: "))
last_marble = int(input("Enter last marble points: "))

t = time.time()
scores = [0] * n_players
circle = [0]
player = 0
current = 0
for marble in range(1, last_marble + 1):
    if marble % 23 == 0:
        current = (current - 7) % len(circle)
        scores[player] += marble + circle.pop(current)
    else:
        current = (current + 2) % len(circle)
        circle.insert(current, marble)
    player = (player + 1) % n_players
print("Answer:", max(scores))
print("Finished in {:.3f} seconds".format(time.time() - t))
