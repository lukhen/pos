from unittest.mock import Mock, call
import io
from abc import abstractmethod, ABC
import pytest


class TextCommandInterpreter:
    def __init__(self, barcode_scanned_listener):
        self._barcode_scanned_listener = barcode_scanned_listener

    def process(self, reader):
        self.process_text_input(reader)

    def process_text_input(self, reader):
        self.read_valid_commands(reader.getvalue().splitlines())
        for line in reader.getvalue().splitlines():
            self.interpret_text_command(line)
        reader.close()

    def interpret_text_command(self, line):
        self._barcode_scanned_listener.onbarcode(line)

    def read_valid_commands(self, lines):
        valid_commands = []
        for line in lines:
            if self.is_valid(line):
                valid_commands.append(line)
        return valid_commands

    def is_valid(self, line):
        return True


class BarcodeScannedListener(ABC):
    def onbarcode(self, barcode):
        ...


def test_zero():
    barcode_scanned_listener = Mock(spec=BarcodeScannedListener)

    TextCommandInterpreter(barcode_scanned_listener).process(io.StringIO(""))

    assert barcode_scanned_listener.mock_calls == []


def test_one():
    barcode_scanned_listener = Mock(spec=BarcodeScannedListener)

    TextCommandInterpreter(barcode_scanned_listener).process(
        io.StringIO("::barcode::\n")
    )

    barcode_scanned_listener.onbarcode.assert_called_once_with("::barcode::")


def test_many():
    barcode_scanned_listener = Mock(spec=BarcodeScannedListener)

    TextCommandInterpreter(barcode_scanned_listener).process(
        io.StringIO("::barcode 1::\n::barcode 2::\n::barcode 3::")
    )

    expected_onbarcode_calls = [
        call("::barcode 1::"),
        call("::barcode 2::"),
        call("::barcode 3::"),
    ]
    barcode_scanned_listener.onbarcode.assert_has_calls(expected_onbarcode_calls)


# SMELL This test actually doesn't test interpreting but reading,
#       Probably the name is wrong and maybe it should be localized somewhere else
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
