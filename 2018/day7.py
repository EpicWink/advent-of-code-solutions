with open("input_day7.txt", "r") as f:
    lines = f.readlines()

import networkx as nx
import logging as lg
lg.basicConfig(
    level=lg.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S")
_logger = lg.getLogger(__name__)


class Requirements:
    def __init__(self):
        self.requirements = {s: [] for s in map(chr, range(65, 91))}

    def add_requirement(self, step_name, require_name):
        assert step_name not in self.requirements[require_name]  # no cycles
        self.requirements[step_name].append(require_name)

    def add_requirements_from_lines(self, lines):
        [self.add_requirement(line[36], line[5]) for line in lines]

    def get_available_steps(self, completed=()):
        valid = []
        for step, reqs in self.requirements.items():
            if step not in completed and all(r in completed for r in reqs):
                valid.append(step)
        return valid


class Order:
    def __init__(self, requirements):
        self.requirements = requirements
        self.order = []

    def _get_available_steps(self):
        return self.requirements.get_available_steps(self.order)

    def _set_next_step(self):
        self.order.append(sorted(self.requirements.get_available_steps(self.order))[0])

    def build_order(self):
        # _reqs_str = "\n".join("{}: {}".format(s, rs) for s, rs in self.requirements.items())
        # _logger.debug("Requirements:\n{}".format(_reqs_str))
        while len(self.order) < 26:
            self._set_next_step()


reqs = Requirements()
reqs.add_requirements_from_lines(lines)
order = Order(reqs)
order.build_order()
assert "".join(order.order) == "FDSEGJLPKNRYOAMQIUHTCVWZXB"
print("Answer pt1:", "".join(order.order))


class Task:
    def __init__(self, step_name, start_second):
        self.step_name = step_name
        self.start_second = start_second

    def __str__(self):
        return "{} @ {}".format(self.step_name, self.start_second)

    def __repr__(self):
        return "{}({}, {})".format(
            type(self).__name__,
            repr(self.step_name),
            repr(self.start_second))

    @property
    def length(self):
        return 60 + ord(self.step_name) - 65


class Schedule:
    def __init__(self, requirements):
        self.requirements = requirements
        self.seconds = []
        self._completed = set()
        self._current = [None] * 5
        self._next = []

    def _update_next(self):
        current = set(t.step_name for t in self._current if t)
        valid = set(self.requirements.get_available_steps(self._completed)) - current
        # _logger.debug("Can start: {}".format(valid))
        self._next = sorted(valid)

    def _finish_tasks(self):
        for j, task in enumerate(self._current):
            if task is None:
                continue
            if len(self.seconds) - task.start_second > task.length:
                self._completed.add(task.step_name)
                self._current[j] = None

    def _start_tasks(self):
        for j, task in enumerate(self._current):
            if task is not None:
                continue
            if not self._next:
                break
            self._current[j] = Task(self._next.pop(0), len(self.seconds))

    def _add_second(self):
        _logger.debug("Second {}: {}".format(len(self.seconds), self._current))
        self.seconds.append(self._current.copy())

    def build_schedule(self):
        while len(self._completed) < 26:
            self._finish_tasks()
            self._update_next()
            self._start_tasks()
            self._add_second()


sched = Schedule(reqs)
sched.build_schedule()
print("Answer pt2:", len(sched.seconds) - 1)
