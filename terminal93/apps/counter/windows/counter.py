from textual.app import ComposeResult
from textual.containers import CenterMiddle
from textual.reactive import var
from textual.widgets import Button

from terminal93 import Window


class MainWindow(Window):
    count = var(0)

    def content(self) -> ComposeResult:
        with CenterMiddle():
            yield Button('0', 'primary')

    def watch_count(self, new: int) -> None:
        self.query_one(Button).label = str(new)
        self.title = f'Counter: {self.count}'

    def on_button_pressed(self) -> None:
        self.count += 1
