from textual.app import ComposeResult

from terminal93 import Window
from ..widgets.markdown import WelcomeMarkdown


class MainWindow(Window):
    TITLE = 'Welcome!'
    WIDTH = 60
    HEIGHT = 25

    def content(self) -> ComposeResult:
        yield WelcomeMarkdown()
