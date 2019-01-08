with open("input_day4.txt", "r") as f:
    lines = f.readlines()

import datetime
import numpy as np


class Event:
    _event_types = ("wakes up", "falls asleep", "begins shift")

    def __init__(self, dt, event_type, guard_id=None):
        self.dt = dt
        self.event_type = event_type
        self.guard_id = guard_id
        assert event_type < len(self._event_types)

    def __str__(self):
        return "[{}]{} {}".format(self.dt, " ({})".format(self.guard_id) if self.guard_id else "", self.event_str)

    @property
    def event_str(self):
        return self._event_types[self.event_type]

    @classmethod
    def from_line(cls, line):
        # print("Processing line:", line)
        event_str = line.strip()[19:]
        # print("event_str:", event_str)
        # print("line[1:17]:", line[1:17])
        dt = datetime.datetime.strptime(line[1:17], "%Y-%m-%d %H:%M")
        if event_str.startswith("Guard"):
            _, guard_id, event_str = event_str.split(" ", maxsplit=2)
            # print("guard_id:", guard_id)
            # print("event_str (new):", event_str)
            return cls(dt, cls._event_types.index(event_str), guard_id=guard_id)
        else:
            return cls(dt, cls._event_types.index(event_str))


class Shift:
    def __init__(self, start_event):
        assert start_event.event_type == 2
        self.events = [start_event]

    def __str__(self):
        # print("".join(map(str, self.is_asleep.astype(np.uint8))))
        return "Shift for guard {}\n  {}".format(self.guard_id, "\n  ".join(map(str, self.events)))

    def clear_cache(self):
        pass

    @property
    def guard_id(self):
        return self.events[0].guard_id

    def add_event(self, event):
        self.clear_cache()
        assert event.dt >= self.events[-1].dt
        event.guard_id = self.guard_id
        self.events.append(event)

    @property
    def is_asleep(self):
        is_asleep = np.zeros((60,), dtype=np.bool8)
        for event in self.events[1:]:
            # print("event.dt.minute:", event.dt.minute)
            # print("bool(event.event_type):", bool(event.event_type))
            # print("event.event_str:", event.event_str)
            is_asleep[event.dt.minute:] = bool(event.event_type)
        return is_asleep

    @property
    def minutes_asleep(self):
        return np.sum(self.is_asleep)


class Guard:
    def __init__(self, guard_id):
        self.guard_id = guard_id
        self.shifts = []

    def __str__(self):
        return "Guard {} shifts:\n {}".format(self.guard_id, "\n ".join(map(str, self.shifts)))

    def clear_cache(self):
        pass

    def add_shift(self, shift):
        self.clear_cache()
        assert shift.guard_id == self.guard_id
        self.shifts.append(shift)

    @property
    def minutes_asleep(self):
        return np.sum([s.minutes_asleep for s in self.shifts])

    @property
    def is_asleep_sum(self):
        is_asleep = np.stack([s.is_asleep for s in self.shifts], axis=0)
        return np.sum(is_asleep, axis=0)

    @property
    def minute_most_asleep(self):
        return np.argmax(self.is_asleep_sum)


def main():
    events = [Event.from_line(line) for line in lines]
    events = sorted(events, key=lambda event: event.dt)

    shifts = []
    for event in events:
        if event.event_type == 2:
            if shifts:
                assert event.dt > shifts[-1].events[0].dt
            shifts.append(Shift(event))
        else:
            shifts[-1].add_event(event)

    guards = {}
    for shift in shifts:
        # print(shift)
        guards.setdefault(shift.guard_id, Guard(shift.guard_id)).add_shift(shift)

    for guard in sorted(guards.values(), key=lambda guard: int(guard.guard_id[1:])):
        print(guard)

    print("len(guards.shifts):", [len(guard.shifts) for guard in guards.values()])

    # most_asleep_guard = max(guards.values(), key=lambda guard: guard.minutes_asleep)
    most_asleep_guard = max(guards.values(), key=lambda guard: guard.minutes_asleep / len(guard.shifts))
    print("most_asleep_guard.guard_id:", most_asleep_guard.guard_id)
    print("len(most_asleep_guard.shifts):", len(most_asleep_guard.shifts))
    print("most_asleep_guard.minutes_asleep:", most_asleep_guard.minutes_asleep)
    print("most_asleep_guard.is_asleep_sum:", most_asleep_guard.is_asleep_sum)
    print("most_asleep_guard.minute_most_asleep:", most_asleep_guard.minute_most_asleep)
    print("answer pt1:", int(most_asleep_guard.guard_id[1:]) * most_asleep_guard.minute_most_asleep)

    # most_freq_asleep_guard = max(guards.values(), key=lambda guard: np.max(guard.is_asleep_sum))
    most_freq_asleep_guard = max(guards.values(), key=lambda guard: np.max(guard.is_asleep_sum) / len(guard.shifts))
    print("most_freq_asleep_guard.guard_id:", most_freq_asleep_guard.guard_id)
    print("len(most_freq_asleep_guard.shifts):", len(most_freq_asleep_guard.shifts))
    print("most_freq_asleep_guard.is_asleep_sum:", most_freq_asleep_guard.is_asleep_sum)
    print("np.argmax(most_freq_asleep_guard.is_asleep_sum):", np.argmax(most_freq_asleep_guard.is_asleep_sum))
    print("answer pt2:", int(most_freq_asleep_guard.guard_id[1:]) * np.argmax(most_freq_asleep_guard.is_asleep_sum))



if __name__ == "__main__":
    main()
