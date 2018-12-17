import pytest
from tests.sale import Price
from tests.test_display_messages_to_console import ConsoleDisplay


@pytest.mark.parametrize("test_input, expected", [

    (789, "$7.89"),
    (520, "$5.20"),
    (400, "$4.00"),
    (0, "$0.00"),
    (2, "$0.02"),
    (37, "$0.37"),
    (418976, "$4,189.76"),
    (210832281, "$2,108,322.81")
])
def test_simplest(test_input, expected):
    assert eval("ConsoleDisplay.format_monetary_amount(Price.cents({0}))".format(
        test_input)) == expected


# REFACTOR Apply Price.cents() to all the numbers so that
# the inputs become Price objects
@pytest.mark.parametrize("test_input, expected", [
    (789, "$7.89"),
    (520, "$5.20"),
    (400, "$4.00"),
    (0, "$0.00"),
    (2, "$0.02"),
    (37, "$0.37"),
    (418976, "$4,189.76"),
    (210832281, "$2,108,322.81")
])
def test_display_price(test_input, expected, capsys):

    ConsoleDisplay().display_price(Price.cents(test_input))
    assert capsys.readouterr().out.splitlines() == [
        expected]
