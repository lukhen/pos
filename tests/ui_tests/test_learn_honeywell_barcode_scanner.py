def main():
    # This test shows us that the Honeywell barcode scanner behaves just like a keyboard device
    # inserting @ sign in front of each scanned barcode.
    # Run this program, then either scan barcodes into stdin or type on the keyboard, then press ENTER.
    # This program will echo each line it reads to stdout.
    # Type "exit" to terminate the program.
    #
    # To test-drive this behavior, it looks like we can simply simulate stdin.
    command = None
    while command != "exit":
        command = input("")  # type: str
        for line in command.splitlines():
            print(line)


if __name__ == "__main__":
    main()
