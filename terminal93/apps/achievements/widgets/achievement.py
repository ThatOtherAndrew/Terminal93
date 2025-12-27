from textual.app import ComposeResult
from textual.containers import HorizontalGroup, VerticalGroup
from textual.widgets import Label, Static

from terminal93.utils.achievements import Achievement


class AchievementEntry(HorizontalGroup):
    # language=SCSS
    DEFAULT_CSS = """
    AchievementEntry {
        padding: 0 1;
        margin-right: 1;
        border: round $panel;
        
        &:hover {
            border: round $primary-background;
        }
        
        &:focus {
            border: round $primary;
        }
    }
    
    #icon {
        box-sizing: content-box;
        width: auto;
        background: $panel;
        border: block $panel;
        margin-right: 2;
    }
    
    #name {
        margin-bottom: 1;
    }
    
    VerticalGroup {
        width: 1fr;
    }
    """

    def __init__(self, achievement: Achievement) -> None:
        super().__init__()
        self.achievement = achievement
        self.can_focus = True

    def compose(self) -> ComposeResult:
        yield Static(self.achievement['icon'], id='icon')
        with VerticalGroup():
            yield Label(self.achievement['name'], id='name')
            yield Label(self.achievement['description'], id='description')
