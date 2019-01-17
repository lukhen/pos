from tests.sale import TextCommandInterpreter


def test_empty_line():
    tci = TextCommandInterpreter(None)

    assert tci.is_valid("") is not True
