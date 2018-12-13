import io


def test_product_not_found_message(capsys):
    console_display = ConsoleDisplay()
    console_display.display_product_not_found_message("91837248")
    assert capsys.readouterr().out.splitlines() == [
        'Product not found for 91837248']


class ConsoleDisplay:
    def display_product_not_found_message(self, barcode):
        print('Product not found for {}'.format(barcode))
