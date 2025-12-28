from textual.app import ComposeResult
from textual.widgets import Markdown

from terminal93 import Window

# language=Markdown
MESSAGE = """
# Welcome to Terminal93!

Terminal93 is a lil fantasy desktop inspired by the likes of [WINDOWS93](https://www.windows93.net/)
"""


class MainWindow(Window):
    TITLE = 'Welcome!'

    def content(self) -> ComposeResult:
        yield Markdown(MESSAGE)
