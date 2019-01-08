import logging as lg
import time

lg.basicConfig(
    level=lg.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S")
_logger = lg.getLogger(__name__)


class Marble:
    def __init__(self, value, prev=None, next_=None):
        self.value = value
        self.prev = prev or self
        self.next_ = next_ or self

    def get_next(self, n=1):
        # assert n >= 0
        if n == 0:
            return self
        else:
            return self.next_.get_next(n - 1)

    def get_prev(self, n=1):
        # assert n >= 0
        if n == 0:
            return self
        else:
            return self.prev.get_prev(n - 1)

    def insert_next(self, value):
        new_marble = type(self)(value, prev=self, next_=self.next_)
        self.next_.prev = new_marble
        self.next_ = new_marble
        return new_marble

    def pop(self):
        self.prev.next_ = self.next_
        self.next_.prev = self.prev
        return self


n_players = int(input("Number of players: "))
last_marble = int(input("Enter last marble points: "))

t = time.time()
scores = [0] * n_players
current = Marble(0)
player = 0
for value in range(1, last_marble + 1):
    if value % 23 == 0:
        back7 = current.get_prev(n=7).pop()
        current = back7.next_
        scores[player] += value + back7.value
    else:
        current = current.get_next(n=1).insert_next(value)
    player = (player + 1) % n_players
print("Answer:", max(scores))
print("Finished in {:.3f} seconds".format(time.time() - t))
