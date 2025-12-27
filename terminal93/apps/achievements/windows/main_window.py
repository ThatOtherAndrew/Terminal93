from textual.app import ComposeResult
from textual.containers import VerticalScroll

from terminal93 import Terminal93, Window
from terminal93.utils.achievements import Achievements

from ..widgets.achievement import AchievementEntry
from ..widgets.progress import AchievementProgressBar


class MainWindow(Window):
    WIDTH = 60
    HEIGHT = 25

    app: Terminal93

    def content(self) -> ComposeResult:
        yield AchievementProgressBar(
            self.app.achievements.achieved_count, len(self.app.achievements)
        )

        with VerticalScroll():
            for achievement in self.app.achievements.values():
                yield AchievementEntry(achievement)

    def on_mount(self) -> None:
        def update(new: Achievements) -> None:
            self.title = f'Achievements: {new.achieved_count}/{len(new)}'
            self.query_one(AchievementProgressBar).progress = new.achieved_count

        self.watch(self.app, 'achievements', update)
