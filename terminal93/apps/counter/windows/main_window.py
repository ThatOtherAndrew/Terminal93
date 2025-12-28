from textual.app import ComposeResult
from textual.containers import CenterMiddle
from textual.reactive import var

from terminal93 import Window

from ..widgets.button import CounterButton


class CounterWindow(Window):
    count = var(0)

    def content(self) -> ComposeResult:
        with CenterMiddle():
            yield CounterButton().data_bind(CounterWindow.count)

    def watch_count(self, new: int) -> None:
        self.title = f'Counter: {new}'

        if new == 1:
            self.app.achievements.grant('where_cookies')
        elif new == 67:
            self.app.achievements.grant('unfunny_number')
        elif new == 69:
            self.app.achievements.grant('funny_number')

    def on_button_pressed(self) -> None:
        self.count += 1
