import time
import pathlib
import logging as lg

import numpy as np

lg.basicConfig(
    level=lg.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S")
_logger = lg.getLogger(__name__)


class TrackTypeDetermine:
    type_names = (None, "vert", "horz", "upright", "downright", "downleft", "upleft", "isect")
    type_symbols = (" ", "|", "-", "\\", "/", "\\", "/", "+")
    vert_cart_symbols = ("^", "v")
    horz_cart_symbols = (">", "<")

    def __init__(self):
        self.curve_symbols = ("/", "\\")
        self._track_for_cart = {s: "|" for s in self.vert_cart_symbols}
        self._track_for_cart.update({s: "-" for s in self.horz_cart_symbols})
        self.cart_symbols = self.vert_cart_symbols + self.horz_cart_symbols
        self.valid_ids_vert = tuple(j for j, s in enumerate(self.type_symbols) if s in ("|", "+"))
        self.valid_ids_horz = tuple(j for j, s in enumerate(self.type_symbols) if s in ("-", "+"))
        self.vert_id = self.type_symbols.index("|")
        self.horz_id = self.type_symbols.index("-")
        self.curve_ids = tuple(
            j for j, symb in enumerate(self.type_symbols)
            if symb in self.curve_symbols)
        self.isect_id = self.type_symbols.index("+")

    def name(self, type_id):
        return self.type_names[type_id]

    def symb(self, type_id):
        return self.type_symbols[type_id]

    def get_id(self, symb, above_symb, below_symb, right_symb, left_symb):
        if above_symb in self.cart_symbols:
            above_symb = self._track_for_cart[above_symb]
        if below_symb in self.cart_symbols:
            below_symb = self._track_for_cart[below_symb]
        if right_symb in self.cart_symbols:
            right_symb = self._track_for_cart[right_symb]
        if left_symb in self.cart_symbols:
            left_symb = self._track_for_cart[left_symb]

        if symb in self.curve_symbols:
            above = self.type_symbols.index(above_symb) if above_symb else 0
            below = self.type_symbols.index(below_symb) if below_symb else 0
            right = self.type_symbols.index(right_symb) if right_symb else 0
            left = self.type_symbols.index(left_symb) if left_symb else 0
            above_vert = above in self.valid_ids_vert
            below_vert = below in self.valid_ids_vert
            right_horz = right in self.valid_ids_horz
            left_horz = left in self.valid_ids_horz
            if above_vert and not below_vert and right_horz and not left_horz:
                return self.type_names.index("upright")
            elif not above_vert and below_vert and right_horz and not left_horz:
                return self.type_names.index("downright")
            elif not above_vert and below_vert and not right_horz and left_horz:
                return self.type_names.index("downleft")
            elif above_vert and not below_vert and not right_horz and left_horz:
                return self.type_names.index("upleft")
            else:
                _symbs = symb, above_symb, below_symb, right_symb, left_symb
                raise ValueError("{}: {} {} {} {}".format(*_symbs))
        elif symb in self.cart_symbols:
            return self.type_symbols.index(self._track_for_cart[symb])
        else:
            return self.type_symbols.index(symb)


class Cart:
    track_determine = TrackTypeDetermine()
    _next_turns = {"l": "s", "s": "r", "r": "l"}
    _velocities = {"^": (-1, 0), "v": (1, 0), ">": (0, 1), "<": (0, -1)}
    _left_turns = {"^": "<", "<": "v", "v": ">", ">": "^"}
    _straight_turns = {"^": "^", "<": "<", "v": "v", ">": ">"}
    _right_turns = {"^": ">", "<": "^", "v": "<", ">": "v"}
    _turns = {"l": _left_turns, "s": _straight_turns, "r": _right_turns}

    def __init__(self, id_, init_pos, init_dir, track_ids):
        self.id_ = id_
        self.init_pos = init_pos
        self.init_dir = init_dir
        self.track_ids = track_ids
        self.cur_pos = init_pos
        self.cur_dir = init_dir
        self.next_turn = "l"

    def __str__(self):
        track_symb = self.track_determine.symb(self.track_ids[self.cur_pos])
        return "{}: {} on {} @ {}".format(self.id_, self.cur_dir, track_symb, self.cur_pos)

    def _update_dir_curve(self):
        cur_track_id = self.track_ids[self.cur_pos]
        if self.track_determine.name(cur_track_id) == "upright":
            self.cur_dir = "^" if self.cur_dir == "<" else ">"
        elif self.track_determine.name(cur_track_id) == "downright":
            self.cur_dir = "v" if self.cur_dir == "<" else ">"
        elif self.track_determine.name(cur_track_id) == "downleft":
            self.cur_dir = "v" if self.cur_dir == ">" else "<"
        elif self.track_determine.name(cur_track_id) == "upleft":
            self.cur_dir = "^" if self.cur_dir == ">" else "<"
        else:
            raise ValueError("Not on a curve")

    def _update_dir_isect(self):
        t = self.next_turn
        self.next_turn = self._next_turns[t]
        self.cur_dir = self._turns[t][self.cur_dir]

    def advance(self):
        vel = self._velocities[self.cur_dir]
        self.cur_pos = (self.cur_pos[0] + vel[0], self.cur_pos[1] + vel[1])
        cur_track_id = self.track_ids[self.cur_pos]
        if cur_track_id in self.track_determine.curve_ids:
            self._update_dir_curve()
        elif cur_track_id == self.track_determine.isect_id:
            self._update_dir_isect()


class Layout:
    track_determine = TrackTypeDetermine()

    def __init__(self, track_ids, carts):
        self.track_ids = track_ids
        self.carts = carts

    @classmethod
    def from_data_str(cls, data_str):
        t = time.time()
        lines = data_str.splitlines()
        lines = lines if lines[-1] else lines[:-1]
        height, width = len(lines), len(lines[0])
        _logger.debug("Layout size: {}, {}".format(height, width))

        track_ids = np.zeros((height, width), dtype=np.uint8)
        carts = []
        for j, line in enumerate(lines):
            for k, symb in enumerate(line):
                above = lines[j - 1][k] if j > 0 else None
                below = lines[j + 1][k] if j < height - 1 else None
                right = lines[j][k + 1] if k < width - 1 else None
                left = lines[j][k - 1] if k > 0 else None
                try:
                    track_ids[j, k] = cls.track_determine.get_id(symb, above, below, right, left)
                except Exception:
                    _logger.error("Error at {}, {} for track '{}'".format(j, k, symb))
                    raise
                if symb in cls.track_determine.cart_symbols:
                    carts.append(Cart(len(carts), (j, k), symb, track_ids))

        _logger.debug("Track building finished in {:.2f}s".format(time.time() - t))
        _logger.debug("Carts:\n{}".format("\n".join(map(str, carts))))
        _logger.debug("Have {} carts".format(len(carts)))
        return cls(track_ids, carts)

    def _cart_priority(self, cart):
        return cart.cur_pos[0] * self.track_ids.shape[0] + cart.cur_pos[1]

    def tick(self):
        carts_ordered = sorted(enumerate(self.carts), key=lambda x: self._cart_priority(x[1]))
        has_crashed = [False] * len(self.carts)
        for j, cart in carts_ordered:
            if has_crashed[j]:
                continue
            # _logger.debug("Cart before: {}".format(cart))
            cart.advance()
            # _logger.debug("Cart after: {}".format(cart))
            if self.any_crashes():
                ks = self.carts_at(cart.cur_pos)
                for k in ks:
                    has_crashed[k] = True

    def any_crashes(self):
        priorities = [self._cart_priority(cart) for cart in self.carts]
        return len(np.unique(priorities)) < len(self.carts)

    def carts_at(self, pos):
        return [j for j, cart in enumerate(self.carts) if cart.cur_pos == pos]

    def first_crash(self):
        for j, cart1 in enumerate(self.carts[:-1]):
            for cart2 in self.carts[j + 1:]:
                if cart1.cur_pos == cart2.cur_pos:
                    return cart1.cur_pos

    def remove_carts_at(self, pos):
        js = self.carts_at(pos)
        for j in js[::-1]:
            cart = self.carts.pop(j)
            _logger.debug("Removed cart {} (index {})".format(cart, j))

    def get_current_str(self):
        track_ids = self.track_ids.copy()
        n_types = len(self.track_determine.type_symbols)
        for cart in self.carts:
            if track_ids[cart.cur_pos] < n_types:
                track_ids[cart.cur_pos] = {"^": 0, "v": 1, ">": 2, "<": 3}[cart.cur_dir] + n_types
            else:
                track_ids[cart.cur_pos] = n_types + 4
        symbs = self.track_determine.type_symbols + ("^", "v", ">", "<", "X")
        return "\n".join("".join(symbs[j] for j in row) for row in track_ids)


def main():
    data_str = pathlib.Path("input_day13.txt").read_text()
    layout = Layout.from_data_str(data_str)
    assert layout.get_current_str() + "\n" == data_str

    t = time.time()
    j = 0
    while True:
        if j % 100 == 0:
            _logger.debug("Tick {}".format(j))
        layout.tick()
        # print(layout.get_current_str())
        # print("Tick:", j)
        # time.sleep(1.0 / 3.0)
        if layout.any_crashes():
            # _logger.debug("Current layout:\n{}".format(layout.get_current_str()))
            _logger.debug("Crash at tick {}".format(j))
            print("Answer pt1:", layout.first_crash()[::-1])
            break
        j += 1
    _logger.debug("Finished in {:.2f}s".format(time.time() - t))

    layout = Layout.from_data_str(data_str)

    t = time.time()
    j = 0
    while True:
        if j % 500 == 0:
            _logger.debug("Tick {}".format(j))
        if len(layout.carts) < 2:
            print("Answer pt2:", layout.carts[0].cur_pos[::-1])
        layout.tick()
        while layout.any_crashes():
            layout.remove_carts_at(layout.first_crash())
        j += 1
    _logger.debug("Finished in {:.2f}s".format(time.time() - t))


if __name__ == "__main__":
    main()
