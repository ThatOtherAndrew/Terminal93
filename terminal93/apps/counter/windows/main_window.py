from textual.app import ComposeResult
from textual.containers import CenterMiddle
from textual.reactive import var

from terminal93 import Window

from ..widgets.button import CounterButton


class MainWindow(Window):
    count = var(0)

    def content(self) -> ComposeResult:
        with CenterMiddle():
            yield CounterButton().data_bind(MainWindow.count)

    def watch_count(self, new: int) -> None:
        self.title = f'Counter: {new}'

    def on_button_pressed(self) -> None:
        self.count += 1
