from tests.sale import TextCommandInterpreter, BarcodeScannedListener
from unittest.mock import Mock, call
import io


def test_several_barcodes_interspersed_with_empty_lines():
    barcode_scanned_listener = Mock(spec=BarcodeScannedListener)
    tci = TextCommandInterpreter(barcode_scanned_listener)
    text_input = "::barcode 1::\n\n\n::barcode 2::\n\n::barcode 3::"
    tci.read_valid_commands = Mock()

    tci.process(io.StringIO(text_input))

    tci.read_valid_commands.assert_called_once_with(
        ["::barcode 1::", "", "", "::barcode 2::", "", "::barcode 3::"]
    )


def test_read_commands_from_text_with_barcodes_interspersed_with_empty_lines():
    barcode_scanned_listener = Mock(spec=BarcodeScannedListener)
    tci = TextCommandInterpreter(barcode_scanned_listener)
    tci.is_valid = Mock()

    tci.read_valid_commands(["::barcode 1::", "", "\t  ", "  "])

    tci.is_valid.assert_has_calls(
        (call("::barcode 1::"), call(""), call("\t  "), call("  "))
    )


def test_produce_list_of_valid_commands():
    barcode_scanned_listener = Mock(spec=BarcodeScannedListener)
    tci = TextCommandInterpreter(barcode_scanned_listener)
    lines = "::barcode 1::", "", "\t  ", "  ", "::barcode 2::"

    valid_commands = tci.read_valid_commands(lines)

    assert all(command in valid_commands for command in filter(tci.is_valid, lines))
