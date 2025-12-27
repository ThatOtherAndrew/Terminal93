from textual.app import ComposeResult
from textual.containers import HorizontalGroup
from textual.reactive import var
from textual.widgets import ProgressBar


class AchievementProgressBar(HorizontalGroup):
    # language=SCSS
    DEFAULT_CSS = """
    AchievementProgressBar {
        margin-bottom: 1;
    }
    """

    progress = var(0)
    total = var(0)

    def compose(self) -> ComposeResult:
        yield ProgressBar(show_eta=False).data_bind(
            AchievementProgressBar.progress,
            AchievementProgressBar.total,
        )
