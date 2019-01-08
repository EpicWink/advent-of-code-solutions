import sys
import time
import pathlib
import logging as lg

import numpy as np

lg.basicConfig(
    level=lg.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S")
_logger = lg.getLogger(__name__)
sys.setrecursionlimit(100000)


class LinkedListElement:
    def __init__(self, value, prev=None, next_=None):
        self.value = value
        self.prev = prev or self
        self.next_ = next_ or self

    def __str__(self):
        return self.value

    def __repr__(self):
        return "{}({})".format(type(self).__name__, repr(self.value))

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
        new_el = type(self)(value, prev=self, next_=self.next_)
        self.next_.prev = new_el
        self.next_ = new_el
        return new_el

    def pop(self):
        self.prev.next_ = self.next_
        self.next_.prev = self.prev
        return self


class LinkedList:
    _el_class = LinkedListElement

    def __init__(self):
        self.start = self.end = None
        self._n = 0

    def __bool__(self):
        return self._n > 0

    def __len__(self):
        return self._n

    def __iter__(self):
        if not self:
            raise StopIteration
        current = self.start
        while current is not self.end:
            yield current
            current = current.next_
        yield current

    def __getitem__(self, idxs):
        if not self:
            raise IndexError("Empty list")
        if isinstance(idxs, int):
            return self._get(idxs)
        elif isinstance(idxs, slice):
            start, stop, step = idxs.indices(self._n)
            current = self._get(start)
            vals = []
            j = start
            while j < stop:
                vals.append(current)
                current = self._get_next(current, n=step)
                j += step
            return vals
        else:
            raise TypeError(type(idxs))

    def _get(self, idx):
        idx %= self._n
        if idx > self._n // 2:
            return self._get_prev(self.start, n=self._n - idx)
        else:
            return self._get_next(self.start, n=idx)

    @staticmethod
    def _get_next(el, n=1):
        while n > 0:
            el = el.next_
            n -= 1
        return el

    @staticmethod
    def _get_prev(el, n=1):
        while n > 0:
            el = el.prev
            n -= 1
        return el

    def append(self, value):
        if self.start is None:
            self.start = self.end = self._el_class(value)
        else:
            self.end = self.end.insert_next(value)
        self._n += 1

    def pop(self, idx):
        if self._n > 1:
            el = self._get(idx)
            el.pop()
        else:
            if not self:
                raise IndexError("Empty list")
            self.start = self.end = None
        self._n -= 1


class RecipeScore:
    def __init__(self, initial_score_1, initial_score_2):
        self.initial_score_1 = initial_score_1
        self.initial_score_2 = initial_score_2
        self.scoreboard = LinkedList()
        self.scoreboard.append(initial_score_1)
        self.scoreboard.append(initial_score_2)
        self.current1 = self.scoreboard.start
        self.current2 = self.scoreboard.end

    def create_new(self):
        new_sum = self.current1.value + self.current2.value
        if new_sum > 9:
            self.scoreboard.append(1)
            self.scoreboard.append(new_sum - 10)
        else:
            self.scoreboard.append(new_sum)

    def update_current(self):
        self.current1 = self.current1.get_next(self.current1.value + 1)
        self.current2 = self.current2.get_next(self.current2.value + 1)

    def step(self):
        self.create_new()
        self.update_current()

    def _format_score(self, score):
        if score is self.current1:
            _fmt = "({})"
        elif score is self.current2:
            _fmt = "[{}]"
        else:
            _fmt = " {} "
        return _fmt.format(score.value)

    def format_scoreboard(self):
        return "".join(self._format_score(score) for score in self.scoreboard)

    def run(self, n=1):
        j = 0
        while len(self.scoreboard) < n:
            if j % 10000 == 0:
                _logger.debug("Step {}".format(j))
            # print(self.format_scoreboard())
            self.step()
            j += 1

    def _last_match(self, values):
        if len(values) > len(self.scoreboard) + 1:
            return None
        elif tuple(s.value for s in self.scoreboard[-len(values):]) == tuple(values):
            return len(self.scoreboard) - len(values)
        elif tuple(s.value for s in self.scoreboard[-len(values) - 1:-1]) == tuple(values):
            return len(self.scoreboard) - len(values) - 1
        else:
            return None

    def find(self, values):
        j = 0
        while True:
            if j % 10000 == 0:
                _logger.debug("Step {}".format(j))
            self.step()
            if self._last_match(values) is not None:
                return self._last_match(values)
            j += 1


def main():
    in_val = int(input("Number of recipes: "))

    runner = RecipeScore(3, 7)
    runner.run(n=2018 + 10)
    _logger.debug("After 9 steps: {}".format("".join(str(s.value) for s in runner.scoreboard[9:19])))
    _logger.debug("After 5 steps: {}".format("".join(str(s.value) for s in runner.scoreboard[5:15])))
    _logger.debug("After 18 steps: {}".format("".join(str(s.value) for s in runner.scoreboard[18:28])))
    _logger.debug("After 2018 steps: {}".format("".join(str(s.value) for s in runner.scoreboard[2018:2028])))
    runner.run(n=in_val + 10)
    print("Answer pt1:", "".join(str(s.value) for s in runner.scoreboard[in_val:in_val + 10]))

    runner2 = RecipeScore(3, 7)
    print("Answer pt2:", runner2.find(tuple(map(int, str(in_val)))))


if __name__ == "__main__":
    main()
