from textual.app import ComposeResult
from textual.containers import VerticalScroll

from terminal93 import Terminal93, Window

from ..widgets.achievement import AchievementEntry
from ..widgets.progress import AchievementProgressBar


class MainWindow(Window):
    app: Terminal93

    def content(self) -> ComposeResult:
        yield AchievementProgressBar()
        with VerticalScroll():
            for achievement in self.app.achievements.values():
                yield AchievementEntry(achievement)
