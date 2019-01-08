from solutions_2018 import day15 as tscr
import pytest


sample_data_str_0 = "\n".join((
    "#######",
    "#.G...#",
    "#...EG#",
    "#.#.#G#",
    "#..G#E#",
    "#.....#",
    "#######"))
sample_final_0 = "\n".join((
    "#######",
    "#G....#",
    "#.G...#",
    "#.#.#G#",
    "#...#.#",
    "#....G#",
    "#######"))
sample_final_0_pt2 = "\n".join((
    "#######",
    "#..E..#",
    "#...E.#",
    "#.#.#.#",
    "#...#.#",
    "#.....#",
    "#######"))

sample_data_str_1 = "\n".join((
    "#######",
    "#G..#E#",
    "#E#E.E#",
    "#G.##.#",
    "#...#E#",
    "#...E.#",
    "#######"))
sample_final_1 = "\n".join((
    "#######",
    "#...#E#",
    "#E#...#",
    "#.E##.#",
    "#E..#E#",
    "#.....#",
    "#######"))

sample_data_str_2 = "\n".join((
    "#######",
    "#E..EG#",
    "#.#G.E#",
    "#E.##E#",
    "#G..#.#",
    "#..E#.#",
    "#######"))
sample_final_2 = "\n".join((
    "#######",
    "#.E.E.#",
    "#.#E..#",
    "#E.##.#",
    "#.E.#.#",
    "#...#.#",
    "#######"))
sample_final_2_pt2 = "\n".join((
    "#######",
    "#.E.E.#",
    "#.#E..#",
    "#E.##E#",
    "#.E.#.#",
    "#...#.#",
    "#######"))

sample_data_str_3 = "\n".join((
    "#######",
    "#E.G#.#",
    "#.#G..#",
    "#G.#.G#",
    "#G..#.#",
    "#...E.#",
    "#######"))
sample_final_3 = "\n".join((
    "#######",
    "#G.G#.#",
    "#.#G..#",
    "#..#..#",
    "#...#G#",
    "#...G.#",
    "#######"))
sample_final_3_pt2 = "\n".join((
    "#######",
    "#.E.#.#",
    "#.#E..#",
    "#..#..#",
    "#...#.#",
    "#.....#",
    "#######"))

sample_data_str_4 = "\n".join((
    "#######",
    "#.E...#",
    "#.#..G#",
    "#.###.#",
    "#E#G#G#",
    "#...#G#",
    "#######"))
sample_final_4 = "\n".join((
    "#######",
    "#.....#",
    "#.#G..#",
    "#.###.#",
    "#.#.#.#",
    "#G.G#G#",
    "#######"))
sample_final_4_pt2 = "\n".join((
    "#######",
    "#...E.#",
    "#.#..E#",
    "#.###.#",
    "#.#.#.#",
    "#...#.#",
    "#######"))

sample_data_str_5 = "\n".join((
    "#########",
    "#G......#",
    "#.E.#...#",
    "#..##..G#",
    "#...##..#",
    "#...#...#",
    "#.G...G.#",
    "#.....G.#",
    "#########"))
sample_final_5 = "\n".join((
    "#########",
    "#.G.....#",
    "#G.G#...#",
    "#.G##...#",
    "#...##..#",
    "#.G.#...#",
    "#.......#",
    "#.......#",
    "#########"))
sample_final_5_pt2 = "\n".join((
    "#########",
    "#.......#",
    "#.E.#...#",
    "#..##...#",
    "#...##..#",
    "#...#...#",
    "#.......#",
    "#.......#",
    "#########"))

@pytest.mark.parametrize(
    ("data_str", "exp", "exp_n_rounds", "exp_final_state"),
    [
        (sample_data_str_0, 27730, 47, sample_final_0),
        (sample_data_str_1, 36334, 37, sample_final_1),
        (sample_data_str_2, 39514, 46, sample_final_2),
        (sample_data_str_3, 27755, 35, sample_final_3),
        (sample_data_str_4, 28944, 54, sample_final_4),
        (sample_data_str_5, 18740, 20, sample_final_5)])
def test_part_1(data_str, exp, exp_n_rounds, exp_final_state):
    game = tscr.Game.from_data_str(data_str)
    assert game.format_state() == data_str
    game.run()
    assert game.n_rounds_completed == exp_n_rounds
    assert game.outcome == exp
    assert game.format_state() == exp_final_state


@pytest.mark.parametrize(
    ("data_str", "e_ap", "exp", "exp_n_rounds", "exp_final_state"),
    [
        (sample_data_str_0, 15, 4988, 29, sample_final_0_pt2),
        (sample_data_str_2, 4, 31284, 33, sample_final_2_pt2),
        (sample_data_str_3, 15, 3478, 37, sample_final_3_pt2),
        (sample_data_str_4, 12, 6474, 39, sample_final_4_pt2),
        (sample_data_str_5, 34, 1140, 30, sample_final_5_pt2)])
def test_part_2(data_str, e_ap, exp, exp_n_rounds, exp_final_state):
    game = tscr.Game.from_data_str(data_str, ap_map={"E": e_ap})
    assert game.format_state() == data_str
    game.run()
    assert game.n_rounds_completed == exp_n_rounds
    assert game.outcome == exp
    assert game.format_state() == exp_final_state
    initial_e = [unit for unit in game.units if unit.team == "E"]
    remaining_e = [unit for unit in game.remaining_units if unit.team == "E"]
    assert len(remaining_e) == len(initial_e)

    game_bad = tscr.Game.from_data_str(data_str, ap_map={"E": e_ap - 1})
    assert game_bad.format_state() == data_str
    game_bad.run()
    initial_e = [unit for unit in game_bad.units if unit.team == "E"]
    remaining_e = [unit for unit in game_bad.remaining_units if unit.team == "E"]
    assert len(remaining_e) < len(initial_e)
