import time
import pathlib
import logging as lg

import numpy as np

lg.basicConfig(
    level=lg.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S")
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
        return cls(walls)


class Unit:
    def __init__(self, init_pos, team, hp=200, ap=3):
        self.init_pos = init_pos
        self.team = team
        self.hp = hp
        self.ap = ap
        self.pos = init_pos

    @property
    def is_dead(self):
        return self.hp <= 0


class Game:
    _map_class = Map
    _unit_class = Unit

    def __init__(self, map_, units):
        self.map = map_
        self.units = units
        self._n_rounds_completed = 0
        self._unit_poss_cache = None

    @classmethod
    def from_data_str(cls, data_str):
        map_ = cls._map_class.from_data_str(data_str)
        lines = data_str.strip().splitlines()
        units = []
        for j, line in enumerate(lines):
            for k, char in enumerate(line):
                if char in ("G", "E"):
                    _logger.debug("Unit '{}' at {}".format(char, (j, k)))
                    unit = cls._unit_class((j, k), char)
                    units.append(unit)
        return cls(map_, units)

    @property
    def _unit_poss(self):
        if self._unit_poss_cache is None:
            self._unit_poss_cache = {unit.pos for unit in self.units}
        return self._unit_poss_cache

    @property
    def units_sorted(self):
        return sorted(self.units, key=lambda x: self._reading_order(x.pos))

    def _reading_order(self, pos):
        return pos[0] * self.map.size[1] + pos[1]

    def _get_enemies(self, unit):
        return [unit_ for unit_ in self.units if unit_.team != unit.team]

    def _is_open(self, pos):
        return self.map[pos] and pos not in self._unit_poss

    def _get_open_in_range(self, unit, enemies):
        dydxs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        in_range = set()
        for enemy in enemies:
            for pos in [(enemy.pos[0] + dy, enemy.pos[1] + dx) for dy, dx in dydxs]:
                if self._is_open(pos):
                    in_range.add(pos)
        return in_range

    def _get_reachable(self, unit, in_range_locations):
        raise NotImplementedError

    def _get_nearest(self, unit, reachable_locations):
        raise NotImplementedError

    def _get_chosen(self, unit, nearest_locations):
        raise NotImplementedError

    def _get_distances(self, unit, chosen_location):
        raise NotImplementedError

    def _get_step(self, unit, distances):
        raise NotImplementedError

    def _move_unit(self, unit, pos):
        unit.pos = pos
        self._unit_poss_cache = None

    def move_unit(self, unit):
        enemies = self._get_enemies(unit)
        in_range_locations = self._get_open_in_range(unit, enemies)
        reachable_locations = self._get_reachable(unit, in_range_locations)
        if not reachable_locations:
            return
        nearest_locations = self._get_nearest(unit, reachable_locations)
        chosen_location = self._get_chosen(unit, nearest_locations)
        distances = self._get_chosen(unit, chosen_location)
        self._move_unit(unit, self._get_step(unit, distances))

    def _get_enemies_in_range(self, unit, enemies):
        raise NotImplementedError

    def _get_enemy_lowest_hp(self, enemies):
        lowest_hp = sorted(unit.hp for unit in enemies)[0]
        lowest_hp_enemies = [unit for unit in enemies if unit.hp == lowest_hp]
        return sorted(lowest_hp_enemies, key=lambda x: self._reading_order(x.pos))

    def target_in_range(self, unit):
        enemies = self._get_enemies(unit)
        enemies_in_range = self._get_enemies_in_range(unit, enemies)
        if not enemies_in_range:
            return None
        return self._get_enemy_lowest_hp(enemies_in_range)

    def _attack(self, unit, target):
        target.hp -= unit.ap

    def remove_dead(self):
        to_remove = [j for j in reveresed(range(len(self.units))) if self.units[j].is_dead]
        removed = [self.units.pop(j) for j in to_remove]
        if removed:
            _logger.debug("Removed dead units: {}".format(", ".join(map(str, removed))))

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

    def run(self):
        while True:
            if self._n_rounds_completed % 10 == 0:
                _logger.debug("Rounds completed: {}".format(self._n_rounds_completed))
            try:
                self.run_round()
            except GameFinished:
                break
            self._n_rounds_completed += 1

    @property
    def outcome(self):
        return self._n_rounds_completed + sum(unit.hp for unit in self.units)


def main():
    data_str = pathlib.Path("input_day15.txt").read_text()
    game = Game.from_data_str(data_str)
    game.run()
    print("Answer pt1:", game.outcome)


if __name__ == "__main__":
    main()
