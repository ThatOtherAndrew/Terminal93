from textual.app import ComposeResult
from textual.widgets import ProgressBar

from terminal93 import Terminal93, Window
from terminal93.utils.achievements import Achievements


class MainWindow(Window):
    # language=SCSS
    DEFAULT_CSS = """
    """

    app: Terminal93

    def content(self) -> ComposeResult:
        yield ProgressBar(total=len(self.app.achievements), show_eta=False)

    def on_mount(self) -> None:
        achievements: Achievements = self.app.achievements
        self.query_one(ProgressBar).advance(
            sum(1 for a in achievements.values() if a['achieved'])
        )
