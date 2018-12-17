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


class ConsoleDisplay:
    def display_product_not_found_message(self, barcode):
        print('Product not found for {}'.format(barcode))

    def display_empty_barcode_message(self):
        print('Scanning error: empty barcode')

    def display_price(self, price):
        print(ConsoleDisplay.format_monetary_amount(price))

    @staticmethod
    def format_monetary_amount(price: Price):
        return "${:,.2f}".format(price.dollar_value())
