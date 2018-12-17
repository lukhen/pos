def test_product_not_found_message(capsys):
    console_display = ConsoleDisplay()
    console_display.display_product_not_found_message("91837248")
    assert capsys.readouterr().out.splitlines() == [
        'Product not found for 91837248']


def test_empty_barcode_message(capsys):
    ConsoleDisplay().display_empty_barcode_message()
    assert capsys.readouterr().out.splitlines() == [
        'Scanning error: empty barcode']


def test_multiple_messages(capsys):
    console_display = ConsoleDisplay()
    console_display.display_product_not_found_message("91837248")
    console_display.display_empty_barcode_message()
    console_display.display_product_not_found_message("234523")
    console_display.display_empty_barcode_message()

    assert capsys.readouterr().out.splitlines() == [
        'Product not found for 91837248',
        'Scanning error: empty barcode',
        'Product not found for 234523',
        'Scanning error: empty barcode'
    ]


class ConsoleDisplay:
    def display_product_not_found_message(self, barcode):
        print('Product not found for {}'.format(barcode))

    def display_empty_barcode_message(self):
        print('Scanning error: empty barcode')
