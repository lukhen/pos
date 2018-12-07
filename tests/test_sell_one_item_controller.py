from abc import ABC, abstractmethod
from unittest.mock import Mock


class Catalog(ABC):
    @abstractmethod
    def find_price(self, barcode):
        ...


class Display(ABC):
    @abstractmethod
    def display_price(self, price):
        ...


class SaleController:
    def __init__(self, display, catalog):
        self.display = display
        self.catalog = catalog

    def onbarcode(self, barcode):
        return self.display.display_price(self.catalog.find_price(barcode))


class Price:
    @staticmethod
    def cents(cents_value):
        return Price()


def test_product_found():
    irrelevant_price = Price.cents(795)
    catalog = Mock(spec=Catalog)
    display = Mock(spec=Display)
    sale_controller = SaleController(display, catalog)
    catalog.find_price.side_effect = \
        lambda barcode: irrelevant_price if barcode == '12345' else None

    sale_controller.onbarcode('12345')

    display.display_price.assert_called_with(irrelevant_price)
