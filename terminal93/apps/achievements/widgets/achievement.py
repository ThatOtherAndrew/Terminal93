from textual.app import ComposeResult
from textual.containers import HorizontalGroup, VerticalGroup
from textual.reactive import var
from textual.widgets import Label

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
        
        &.achieved {
            border: round $success;
            &:hover {
                border: round $success-lighten-1;
            }
            #icon {
                background: $success;
                border: block $success;
            }
        }
        
        &:focus {
            border: round $primary;
            &:hover {
                border: round $primary-lighten-1;
            }
        }
    }
    
    #icon {
        box-sizing: content-box;
        background: $panel;
        border: block $panel;
        margin-right: 2;
    }
    
    #name {
        margin-bottom: 1;
        text-style: bold;
    }
    
    #description {
        color: $text-muted;
    }
    
    VerticalGroup {
        width: 1fr;
    }
    """

    achievement: var[Achievement] = var(None)

    def __init__(self, achievement: Achievement) -> None:
        super().__init__()
        self.set_reactive(AchievementEntry.achievement, achievement)
        self.can_focus = True

    def compose(self) -> ComposeResult:
        yield Label(id='icon')
        with VerticalGroup():
            yield Label(self.achievement['name'], id='name')
            yield Label(self.achievement['description'], id='description')

    def watch_achievement(self, new: Achievement) -> None:
        achieved = new['achieved']
        self.set_class(bool(achieved), 'achieved')
        self.query_one('#icon', Label).content = (
            '❓' if new['secret'] and not achieved else new['icon']
        )
        self.query_one('#description', Label).content = (
            'This is a secret achievement!'
            if new['secret'] and not achieved
            else new['description']
        )

        if achieved:
            self.border_subtitle = f'Achieved {achieved.strftime("%H:%M")}'
