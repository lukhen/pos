from abc import ABC, abstractmethod


class Price:
    def __init__(self, cents_value):
        self.cents_value = cents_value

    @staticmethod
    def cents(cents_value):
        return Price(cents_value)

    def dollar_value(self):
        return self.cents_value / 100


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

    @abstractmethod
    def display_empty_barcode_message(self):
        ...


class SaleController:
    def __init__(self, display, catalog):
        self.display = display
        self.catalog = catalog

    def onbarcode(self, barcode):
        # SMELL Should I get an empty barcode at all?
        if barcode != '':
            price = self.catalog.find_price(barcode)
            if price:
                return self.display.display_price(price)
            else:
                self.display.display_product_not_found_message(barcode)
        else:
            self.display.display_empty_barcode_message()


class InMemoryCatalog(Catalog):
    def __init__(self, prices_by_barcode):
        self.prices_by_barcode = prices_by_barcode

    def find_price(self, barcode):
        return self.prices_by_barcode.get(barcode, None)


class EnglishLanguageConsoleDisplay(Display):
    PRODUCT_NOT_FOUND_MESSAGE_FORMAT = "Product not found for {}"
    SCANNING_ERROR_EMPTY_BARCODE_MESSAGE_FORMAT = 'Scanning error: empty barcode'
    PRICE_IN_DOLLARS_MESSAGE_FORMAT = "${:,.2f}"

    def display_product_not_found_message(self, barcode_not_found):
        self._render(self._merge_template(
            self.PRODUCT_NOT_FOUND_MESSAGE_FORMAT, barcode_not_found))

    def display_empty_barcode_message(self):
        self._render(self._merge_template(
            self.SCANNING_ERROR_EMPTY_BARCODE_MESSAGE_FORMAT))

    def display_price(self, price):
        self._render(self._merge_template(
            self.PRICE_IN_DOLLARS_MESSAGE_FORMAT, price.dollar_value()))

    def _render(self, text):
        print(text)

    def _merge_template(self, message_template, *placeholder_values):
        return str.format(message_template, *placeholder_values)
