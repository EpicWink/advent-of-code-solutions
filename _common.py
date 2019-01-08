import time
import atexit
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


def _log_call_times():
    len_names = max(len(n) for n in _timings)
    space = " " * (len_names - 13)
    s = "Function name{}  Total (s)  N      Mean (s)  StdDev (s)  Max (s)  Min (s)".format(space)
    lines = [s]
    _fmt = "{:" + str(len_names) + "s}  {:9.2g}  {:5d}  {:8.2g}  {:10.2g}  {:7.2g}  {:7.2g}"
    for name, times in _timings.items():
        if len(times) == 0:
            continue
        ts = np.array(times)
        lines.append(_fmt.format(name, ts.sum(), len(ts), ts.mean(), ts.std(), ts.max(), ts.min()))
    if len(lines) < 2:
        return
    _logger.debug("Call times:\n{}".format("\n".join(lines)))


atexit.register(_log_call_times)
