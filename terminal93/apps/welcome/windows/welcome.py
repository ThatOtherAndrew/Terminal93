from textual.app import ComposeResult
from textual.containers import CenterMiddle
from textual.widgets import Markdown

# language=Markdown
MESSAGE = """
# Welcome to Terminal93!

The rest of this welcome message has yet to be written :>
"""


class MainWindow(CenterMiddle):
    def compose(self) -> ComposeResult:
        yield Markdown(MESSAGE)
