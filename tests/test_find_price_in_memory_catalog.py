from tests.sale import Price, InMemoryCatalog, Catalog
from abc import ABC, abstractmethod


class FindPriceInCatalogContract(ABC):
    @abstractmethod
    def catalog_with(self, barcode, price):
        ...

    @abstractmethod
    def catalog_without(self, barcode_to_avoid):
        ...

    def test_product_found(self):
        found_price = Price.cents(1250)
        catalog = self.catalog_with('12345', found_price)
        assert catalog.find_price('12345') == found_price

    def test_product_not_found(self):
        catalog = self.catalog_without('12345')
        assert catalog.find_price('12345') is None


class TestFindPriceInMemoryCatalog(FindPriceInCatalogContract):

    def catalog_without(self, barcode_to_avoid):
        return InMemoryCatalog({'anything but ' + barcode_to_avoid:
                                Price.cents(0)})

    def catalog_with(self, barcode, found_price) -> Catalog:
        return InMemoryCatalog({
            'definitely not ' + barcode: Price.cents(0),
            barcode: found_price,
            'once again, definitely not ' + barcode: Price.cents(10000000)
        })
