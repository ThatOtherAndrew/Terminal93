from textual.app import ComposeResult
from textual.containers import CenterMiddle
from textual.reactive import var
from textual.widgets import Button


class MainWindow(CenterMiddle):
    count = var(0)

    def compose(self) -> ComposeResult:
        yield Button(str(self.count), 'primary')

    def watch_count(self, new: int) -> None:
        if self.is_mounted:
            self.query_one(Button).label = str(new)

    def on_button_pressed(self) -> None:
        self.count += 1
