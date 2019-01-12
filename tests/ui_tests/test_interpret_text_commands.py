from unittest.mock import Mock
import io
from abc import abstractmethod, ABC


class TextCommandInterpreter:
    def process(self, reader):
        ...


class BarcodeScannedListener(ABC):
    ...


def test_zero():
    barcode_scanned_listener = Mock(spec=BarcodeScannedListener)

    TextCommandInterpreter().process(io.StringIO(""))

    assert barcode_scanned_listener.mock_calls == []
