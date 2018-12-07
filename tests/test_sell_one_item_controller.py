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

    @abstractmethod
    def display_product_not_found_message(self, barcode):
        ...


class SaleController:
    def __init__(self, display, catalog):
        self.display = display
        self.catalog = catalog

    def onbarcode(self, barcode):
        price = self.catalog.find_price(barcode)
        if price:
            return self.display.display_price(price)
        else:
            self.display.display_product_not_found_message(barcode)


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


def test_product_not_found():
    irrelevant_barcode = '12345'
    display = Mock(spec=Display)
    catalog = Mock(spec=Catalog)
    sale_controller = SaleController(display, catalog)
    catalog.find_price.side_effect = \
        lambda barcode: None if barcode == irrelevant_barcode else Price()

    sale_controller.onbarcode(irrelevant_barcode)

    display.display_product_not_found_message.assert_called_with(
        irrelevant_barcode)
