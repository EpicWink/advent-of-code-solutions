"""Common methods for my Advent of Code solutions."""

import time
import atexit
import pathlib
import argparse
import logging as lg
import functools as ft

import numpy as np

_logger = lg.getLogger(__name__)
_timings = {}


class LogTime:
    """Log time of context.

    Args:
        name (str): name of context
    """

    def __init__(self, name):
        self.name = name
        self._t = None

    def __enter__(self):
        self._t = time.time()
        return self

    def __exit__(self, t, v, tb):
        _s = "completed" if (t, v, tb) == (None, None, None) else "failed"
        _logger.debug("{} {} in {:.2f} s".format(self.name, _s, time.time() - self._t))
        return False


def setup_logging():
    """Setup logging."""
    lg.basicConfig(
        level=lg.DEBUG,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S")


def record_call_times(fn):
    """Record call times of function. Use as a decorator.

    Args:
        fn (callable): function to record call times of

    Returns:
        callable: wrapping function
    """

    _timings[fn.__name__] = []

    @ft.wraps(fn)
    def wrapped(*args, **kwargs):
        t = time.time()
        res = fn(*args, **kwargs)
        _timings[fn.__name__].append(time.time() - t)
        return res

    return wrapped


class Solution:  # TODO: unit-test
    """Solution interface."""
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.args = None

    def part_1(self):
        """Part 1 solution computation."""
        raise NotImplementedError

    def part_2(self):
        """Part 2 solution computation."""
        raise NotImplementedError

    def parse(self):
        """Parse command-line argument."""
        self.args = self.parser.parse_args()

    def run(self):
        """Run solution."""
        setup_logging()
        self.parse()
        with LogTime("Part 1"):
            print("Part 1 answer:", self.part_1())
        with LogTime("Part 2"):
            print("Part 2 answer:", self.part_2())


class InputtedSolution(Solution):  # TODO: unit-test
    """Solution interface with an input text file."""
    def __init__(self):
        super().__init__()
        self.parser.add_argument(
            "input_txt",
            type=pathlib.Path,
            help="input data file",
        )
        self.input_text = None

    def parse(self):
        super().parse()
        self.input_text = self.args.input_txt.read_text()


class InputLinesSolution(InputtedSolution):  # TODO: unit-test
    """Solution interface with an input text file of lines."""
    def __init__(self):
        super().__init__()
        self.items = None

    @staticmethod
    def line_type(line):
        """Line conversion function."""
        return line

    def parse(self):
        super().parse()
        self.items = [self.line_type(line) for line in self.input_text.strip().splitlines()]


def get_input_file():
    """Parse command-line arguments to load input file.

    Returns:
        str: input file contents
    """

    soln = InputtedSolution()
    soln.part_1 = lambda: None
    soln.part_2 = lambda: None
    soln.run()
    return soln.input_text


def log_call_times():
    """Log recorded call times."""
    if not _timings:
        return
    len_names = max(len(n) for n in _timings)
    sp = " " * (len_names - 13)
    s = "Function name{}  Total (s)  N         Mean (s)  StdDev (s)  Max (s)  Min (s)".format(sp)
    lines = [s]
    _fmt = "{:" + str(len_names) + "s}  {:9.2g}  {:8d}  {:8.2g}  {:10.2g}  {:7.2g}  {:7.2g}"
    for name, times in _timings.items():
        if len(times) == 0:
            continue
        ts = np.array(times)
        lines.append(_fmt.format(name, ts.sum(), len(ts), ts.mean(), ts.std(), ts.max(), ts.min()))
    if len(lines) < 2:
        return
    _logger.debug("Call times:\n{}".format("\n".join(lines)))


atexit.register(log_call_times)
