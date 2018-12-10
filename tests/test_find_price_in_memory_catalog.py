from tests.sale import Price, InMemoryCatalog, Catalog


class TestFindPriceInMemoryCatalog:
    def test_product_found(self):
        found_price = Price.cents(1250)
        catalog = InMemoryCatalog({'12345': found_price})
        assert catalog.find_price('12345') == found_price

    def test_product_not_found(self):
        catalog = InMemoryCatalog({})
        assert catalog.find_price('12345') is None
