from textual.app import App, ComposeResult
from textual.widgets import Placeholder

from terminal93.screens.BootScreen import BootScreen
from terminal93.widgets.window import Window


class Terminal93(App):
    # language=CSS
    CSS = '''
    BootScreen {
        overflow: hidden;
    }
    '''

    def compose(self) -> ComposeResult:
        for i in range(3):
            yield Window(f'Window {i + 1}', Placeholder('Hello, World!'))

    def on_mount(self) -> None:
        self.push_screen(BootScreen())
