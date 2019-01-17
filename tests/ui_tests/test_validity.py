from tests.sale import TextCommandInterpreter


def test_empty_line():
    tci = TextCommandInterpreter(None)

    assert tci.is_valid("") is not True


def test_nonempty_line():
    tci = TextCommandInterpreter(None)

    assert tci.is_valid("::barcode::") is True
