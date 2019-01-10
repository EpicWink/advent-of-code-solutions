from solutions_2018 import day19 as tscr
# import pytest
import logging as lg

lg.getLogger().setLevel(lg.DEBUG)


def test_program():
    data_str = "\n".join((
        "#ip 0",
        "seti 5 0 1",
        "seti 6 0 2",
        "addi 0 1 0",
        "addr 1 2 3",
        "setr 1 0 0",
        "seti 8 0 4",
        "seti 9 0 5"))
    program = tscr.Program.from_data_str(data_str)
    assert program.state == tscr.State(0, 0, 0, 0, 0, 0)
    assert program.instruction_idx == 0
    program.step()
    assert program.state == tscr.State(0, 5, 0, 0, 0, 0)
    assert program.instruction_idx == 1
    program.step()
    assert program.state == tscr.State(1, 5, 6, 0, 0, 0)
    assert program.instruction_idx == 2
    program.step()
    assert program.state == tscr.State(3, 5, 6, 0, 0, 0)
    assert program.instruction_idx == 4
    program.step()
    assert program.state == tscr.State(5, 5, 6, 0, 0, 0)
    assert program.instruction_idx == 6
    program.step()
    assert program.state == tscr.State(6, 5, 6, 0, 0, 9)
    assert program.instruction_idx == 7
