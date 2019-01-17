from unittest.mock import Mock, call
import io
from abc import abstractmethod, ABC
import pytest
from tests.sale import TextCommandInterpreter, BarcodeScannedListener


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


def test_several_barcodes_interspersed_with_empty_lines():
    barcode_scanned_listener = Mock(spec=BarcodeScannedListener)
    tci = TextCommandInterpreter(barcode_scanned_listener)
    text_input = "::barcode 1::\n\n\n::barcode 2::\n\n::barcode 3::"
    valid_commands = tci.read_valid_commands(text_input.splitlines())
    calls = [call(command) for command in valid_commands]

    tci.process(io.StringIO(text_input))

    barcode_scanned_listener.onbarcode.assert_has_calls(calls)
