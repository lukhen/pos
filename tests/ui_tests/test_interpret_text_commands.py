from unittest.mock import Mock
import io
from abc import abstractmethod, ABC
import pytest


class TextCommandInterpreter:
    def __init__(self, barcode_scanned_listener):
        self._barcode_scanned_listener = barcode_scanned_listener

    def process(self, reader):
        barcode = reader.readline().strip()
        print(barcode)
        if barcode:
            self._barcode_scanned_listener.onbarcode(barcode)


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
