from textual.app import ComposeResult
from textual.containers import HorizontalGroup
from textual.reactive import var
from textual.widgets import ProgressBar


class AchievementProgressBar(HorizontalGroup):
    # language=SCSS
    DEFAULT_CSS = """
    AchievementProgressBar {
        margin-bottom: 1;
        
        ProgressBar Bar {
            width: 1fr;
            
            .bar--bar {
                color: $success;
            }
            
            .bar--complete {
                color: $warning;
            }
        }
    }
    """

    progress = var(0)
    total = var(0)

    def __init__(self, progress: int, total: int) -> None:
        super().__init__()
        self.progress = progress
        self.total = total

    def compose(self) -> ComposeResult:
        yield ProgressBar(show_eta=False).data_bind(
            AchievementProgressBar.progress,
            AchievementProgressBar.total,
        )
