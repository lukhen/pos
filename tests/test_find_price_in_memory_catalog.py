from tests.sale import Price, InMemoryCatalog, Catalog


class TestFindPriceInMemoryCatalog:
    def test_product_found(self):
        found_price = Price.cents(1250)
        catalog = self.catalogWith('12345', found_price)
        assert catalog.find_price('12345') == found_price

    def test_product_not_found(self):
        catalog = self.catalog_without('12345')
        assert catalog.find_price('12345') is None

    def catalog_without(self, barcode_to_avoid):
        return InMemoryCatalog({})

    def catalogWith(self, barcode, found_price) -> Catalog:
        return InMemoryCatalog({barcode: found_price})
