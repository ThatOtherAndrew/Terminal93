from textual.app import App, ComposeResult
from textual.widgets import Placeholder

from terminal93.screens.BootScreen import BootScreen


class Terminal93(App):
    # language=CSS
    CSS = '''
    BootScreen {
        overflow: hidden;
    }
    '''

    def compose(self) -> ComposeResult:
        yield Placeholder('Hello, World!')

    def on_mount(self) -> None:
        self.push_screen(BootScreen())
