from sale import SaleController, InMemoryCatalog, EnglishLanguageConsoleDisplay, Price


def main():
    sale_controller = SaleController(
        EnglishLanguageConsoleDisplay(),
        InMemoryCatalog({
            "12345": Price(795),
            "33445": Price(1285),
            "99999": Price(75)
        }))

    sale_controller.onbarcode('12345')
    sale_controller.onbarcode('8768')
    sale_controller.onbarcode('')
    sale_controller.onbarcode('33445')
    sale_controller.onbarcode('99999')


if __name__ == "__main__":
    main()
