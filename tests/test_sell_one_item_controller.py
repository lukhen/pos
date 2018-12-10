
from unittest.mock import Mock
from tests.sale import Price, Catalog, Display, SaleController


def test_product_found():
    irrelevant_price = Price.cents(795)
    catalog = Mock(spec=Catalog)
    display = Mock(spec=Display)
    sale_controller = SaleController(display, catalog)
    catalog.find_price.side_effect = \
        lambda barcode: irrelevant_price if barcode == '::product found::' else None

    sale_controller.onbarcode('::product found::')

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


def test_empty_barcode():
    display = Mock(spec=Display)
    sale_controller = SaleController(display, None)

    sale_controller.onbarcode('')

    display.display_empty_barcode_message.assert_called_with()
