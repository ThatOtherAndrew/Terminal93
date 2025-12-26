from textual.app import ComposeResult
from textual.widgets import Markdown

from terminal93 import Window

# language=Markdown
MESSAGE = """
# Welcome to Terminal93!

The rest of this welcome message has yet to be written :>
"""


class MainWindow(Window):
    def content(self) -> ComposeResult:
        yield Markdown(MESSAGE)
