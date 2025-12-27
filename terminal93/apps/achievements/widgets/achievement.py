from textual.app import ComposeResult
from textual.containers import HorizontalGroup
from textual.widgets import Placeholder

from terminal93.utils.achievements import Achievement


class AchievementEntry(HorizontalGroup):
    # language=SCSS
    DEFAULT_CSS = """
    AchievementEntry {
        height: 5;
    }
        
    #name {
        width: 8;
    }
    
    #description {
        width: 1fr;
    }
    """

    def __init__(self, achievement: Achievement) -> None:
        self.achievement = achievement
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Placeholder(self.achievement['name'], id='name')
        yield Placeholder(self.achievement['description'], id='description')
