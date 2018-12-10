from tests.sale import Price


class TestFindPriceInMemoryCatalog:
    def test_product_found(self):
        found_price = Price.cents(1250)
        catalog = InMemoryCatalog({'12345': found_price})
        assert catalog.find_price('12345') == found_price


class InMemoryCatalog:
    def __init__(self, prices_by_barcode):
        self.prices_by_barcode = prices_by_barcode

    def find_price(self, barcode):
        return self.prices_by_barcode.get(barcode, None)
