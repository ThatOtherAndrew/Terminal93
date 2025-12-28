import sys

from textual_serve.server import Server

from terminal93 import Terminal93


def main() -> None:
    if '--serve' in sys.argv:
        Server('terminal93', host='0.0.0.0').serve()
    else:
        Terminal93().run()


if __name__ == '__main__':
    main()
