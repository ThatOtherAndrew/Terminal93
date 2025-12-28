import sys

from textual_serve.server import Server

from terminal93 import Terminal93


def main() -> None:
    match sys.argv:
        case ['--serve', public_url]:
            Server(
                'terminal93',
                host='0.0.0.0',
                port=8000,
                title='Terminal93',
                public_url=public_url,
            ).serve()
        case _:
            Terminal93().run()


if __name__ == '__main__':
    main()
