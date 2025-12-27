from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import RichLog

from terminal93 import Window

from ..widgets.chat_input import ChatInput


class MainWindow(Window):
    # language=SCSS
    DEFAULT_CSS = """
    #sidebar {
        dock: right;
    }
    """

    WIDTH = 70
    HEIGHT = 30

    def content(self) -> ComposeResult:
        yield VerticalScroll(id='sidebar')
        yield RichLog(wrap=True)
        yield ChatInput()

    def on_chat_input_submitted(self, event: ChatInput.Submitted) -> None:
        self.notify(event.value)
