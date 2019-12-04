"""Day 15 solution.

https://adventofcode.com/2018/day/15
"""

import logging as lg

import numpy as np
import _common

_logger = lg.getLogger(__name__)


class GameFinished(RuntimeError):
    def __init__(self, *args, **kwargs):
        super().__init__("Game has finished", *args, **kwargs)


class Map:
    def __init__(self, walls):
        self.walls = walls

    def __getitem__(self, pos):
        return bool(self.walls[pos])

    @property
    def size(self):
        return self.walls.shape

    @classmethod
    def from_data_str(cls, data_str):
        lines = data_str.strip().splitlines()
        walls = np.zeros((len(lines), len(lines[0])), dtype=np.bool8)
        _logger.debug("Map size: {}".format(walls.shape))
        for j, line in enumerate(lines):
            for k, char in enumerate(line):
                walls[j, k] = char == "#"
        return cls(walls)


class Unit:
    def __init__(self, init_pos, team, hp=200, ap=3):
        self.init_pos = init_pos
        self.team = team
        self.hp = hp
        self.ap = ap
        self.pos = init_pos

    def __str__(self):
        return "{}({}) [{}] @ {}".format(self.team, self.hp, self.init_pos, self.pos)

    def __repr__(self):
        return "{}({}, {}, {}, {})".format(
            type(self).__name__,
            repr(self.init_pos),
            repr(self.team),
            repr(self.hp),
            repr(self.ap))

    @property
    def is_dead(self):
        return self.hp <= 0


class Game:
    _map_class = Map
    _unit_class = Unit

    def __init__(self, map_, units):
        self.map = map_
        self.units = units
        self.n_rounds_completed = 0
        self._unit_poss_cache = None
        self.remaining_units = units.copy()

    @classmethod
    def from_data_str(cls, data_str, ap_map=None):
        ap_map = ap_map or {}
        map_ = cls._map_class.from_data_str(data_str)
        lines = data_str.strip().splitlines()
        units = []
        for j, line in enumerate(lines):
            for k, char in enumerate(line):
                if char in ("G", "E"):
                    ap = ap_map.setdefault(char, 3)
                    _logger.debug("Adding unit '{}' at {} with {}".format(char, (j, k), ap))
                    unit = cls._unit_class((j, k), char, ap=ap)
                    units.append(unit)
        return cls(map_, units)

    @property
    def _unit_poss(self):
        if self._unit_poss_cache is None:
            self._unit_poss_cache = {unit.pos for unit in self.remaining_units}
        return self._unit_poss_cache

    @property
    @_common.record_call_times
    def units_sorted(self):
        return sorted(self.remaining_units, key=lambda x: self._reading_order(x.pos))

    def _reading_order(self, pos):
        return pos[0] * self.map.size[1] + pos[1]

    @_common.record_call_times
    def _get_enemies(self, unit):
        return [unit_ for unit_ in self.remaining_units if unit_.team != unit.team]

    def _is_open(self, pos):
        return not self.map[pos] and pos not in self._unit_poss

    @_common.record_call_times
    def _get_open_in_range(self, enemies):
        dydxs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        in_range = set()
        for enemy in enemies:
            for pos in [(enemy.pos[0] + dy, enemy.pos[1] + dx) for dy, dx in dydxs]:
                if self._is_open(pos):
                    in_range.add(pos)
        return in_range

    @_common.record_call_times
    def _get_obstacles(self):
        obstacles = self.map.walls.copy()
        for unit in self.remaining_units:
            obstacles[unit.pos] = True
        return obstacles

    @_common.record_call_times
    def _compute_walk_distances(self, loc):
        dydxs = np.array([[0, 1], [0, -1], [1, 0], [-1, 0]], dtype=np.int16)
        obstacles = self._get_obstacles()
        dists = np.full(self.map.size, 2**15 - 1, dtype=np.int16)
        dists[loc] = 0
        dist = 0
        while True:
            points = np.argwhere(dists == dist)
            if len(points) == 0:
                break
            dist += 1
            for point in points:
                for dydx in dydxs:
                    if np.any(point + dydx >= self.map.size):
                        continue
                    neighbour = tuple(point + dydx)
                    if not obstacles[neighbour] and dists[neighbour] > dist:
                        dists[neighbour] = dist
        return dists

    @_common.record_call_times
    def _get_step(self, unit, in_range_locations):
        distss = [self._compute_walk_distances(loc) for loc in in_range_locations]
        distss = np.stack(distss, axis=-1)
        dists = np.min(distss, axis=-1)

        dydxs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        poss = [(unit.pos[0] + dy, unit.pos[1] + dx) for dy, dx in dydxs]

        neighbour_dists = [dists[p] for p in poss]
        if all(d == 2**15 - 1 for d in neighbour_dists):
            return None

        best_dist = min(neighbour_dists)
        best = [p for p in poss if dists[p] == best_dist]
        return sorted(best, key=self._reading_order)[0]

    def _move_unit(self, unit, pos):
        unit.pos = pos
        self._unit_poss_cache = None

    @_common.record_call_times
    def move_unit(self, unit):
        enemies = self._get_enemies(unit)
        in_range_locations = self._get_open_in_range(enemies)
        if not in_range_locations:
            return
        new_pos = self._get_step(unit, in_range_locations)
        if new_pos is not None:
            self._move_unit(unit, new_pos)

    @_common.record_call_times
    def _get_enemies_in_range(self, unit, enemies):
        dists2 = [(unit.pos[0] - en.pos[0])**2 + (unit.pos[1] - en.pos[1])**2 for en in enemies]
        return [enemies[j] for j, dist2 in enumerate(dists2) if dist2 == 1]

    @_common.record_call_times
    def _get_enemy_lowest_hp(self, enemies):
        lowest_hp = sorted(unit.hp for unit in enemies)[0]
        lowest_hp_enemies = [unit for unit in enemies if unit.hp == lowest_hp]
        return sorted(lowest_hp_enemies, key=lambda x: self._reading_order(x.pos))

    @_common.record_call_times
    def target_in_range(self, unit):
        enemies = self._get_enemies(unit)
        enemies_in_range = self._get_enemies_in_range(unit, enemies)
        if not enemies_in_range:
            return None
        return self._get_enemy_lowest_hp(enemies_in_range)[0]

    def _attack(self, unit, target):
        target.hp -= unit.ap

    @_common.record_call_times
    def remove_dead(self):
        units = self.remaining_units
        to_remove = [j for j in reversed(range(len(units))) if units[j].is_dead]
        removed = [self.remaining_units.pop(j) for j in to_remove]
        if removed:
            _logger.debug("Removed dead units: {}".format(", ".join(map(str, removed))))
            self._unit_poss_cache = None

    @_common.record_call_times
    def run_round(self):
        for unit in self.units_sorted:
            if unit.is_dead:
                continue
            if not self._get_enemies(unit):
                raise GameFinished()
            target = self.target_in_range(unit)
            if target is None:
                self.move_unit(unit)
                target = self.target_in_range(unit)
            if target is not None:
                self._attack(unit, target)
                self.remove_dead()

    def run(self, log_state=False):
        while True:
            if self.n_rounds_completed % 10 == 0:
                _logger.debug("Rounds completed: {}".format(self.n_rounds_completed))
            try:
                self.run_round()
            except GameFinished:
                break
            self.n_rounds_completed += 1
            if log_state:
                _logger.debug("Round {}:\n{}\n{}".format(
                    self.n_rounds_completed,
                    self.format_units(),
                    self.format_state()))
                # time.sleep(0.3)

    @property
    def winning_team(self):
        assert len(set(unit.team for unit in self.remaining_units)) == 1
        return list(set(unit.team for unit in self.remaining_units))[0]

    @property
    def outcome(self):
        assert len(set(unit.team for unit in self.remaining_units)) == 1
        return self.n_rounds_completed * sum(unit.hp for unit in self.remaining_units)

    def format_state(self):
        lines = []
        for j, row in enumerate(self.map.walls):
            line = []
            for k, el in enumerate(row):
                if el:
                    line.append("#")
                elif (j, k) in self._unit_poss:
                    unit = [unit_ for unit_ in self.remaining_units if unit_.pos == (j, k)][0]
                    line.append(unit.team)
                else:
                    line.append(".")
            lines.append("".join(line))
        return "\n".join(lines)

    def format_units(self):
        return "\n".join(map(str, self.remaining_units))


class Solution(_common.InputtedSolution):  # TODO: unit-test, document
    def part_1(self):
        game = Game.from_data_str(self.input_text)
        _logger.debug("Initial units:\n{}".format(game.format_units()))
        _logger.debug("Initial state:\n{}".format(game.format_state()))
        game.run(log_state=True)
        _logger.debug("Completed rounds: {}".format(game.n_rounds_completed))
        _logger.debug("Final units:\n{}".format(game.format_units()))
        _logger.debug("Final state:\n{}".format(game.format_state()))
        return game.outcome

    def part_2(self):
        e_ap = 4
        while True:
            _logger.info("Trying elf AP: {}".format(e_ap))
            game = Game.from_data_str(self.input_text, ap_map={"E": e_ap})
            game.run()
            _logger.debug("Completed rounds: {}".format(game.n_rounds_completed))
            _logger.debug("Final units:\n{}".format(game.format_units()))
            _logger.debug("Final state:\n{}".format(game.format_state()))
            initial_e = [unit for unit in game.units if unit.team == "E"]
            remaining_e = [unit for unit in game.remaining_units if unit.team == "E"]
            if len(initial_e) == len(remaining_e):
                return game.outcome
            e_ap += 1


def main():  # pragma: no cover
    Solution().run()


if __name__ == "__main__":  # pragma: no cover
    main()
