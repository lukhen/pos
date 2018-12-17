import pytest
from tests.sale import Price


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
    assert eval("format_monetary_amount(Price.cents({0}))".format(
        test_input)) == expected


def format_monetary_amount(price: Price):
    return "${:,.2f}".format(price.dollar_value())
