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
        for line in reader.getvalue().splitlines():
            self.interpret_text_command(line)
        reader.close()

    def interpret_text_command(self, line):
        self._barcode_scanned_listener.onbarcode(line)


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
