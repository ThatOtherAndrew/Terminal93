from textual.app import ComposeResult
from textual.widgets import Label, Select

from terminal93 import Terminal93, Window


class ThemesWindow(Window):
    WIDTH = 40
    HEIGHT = 8

    # language=SCSS
    DEFAULT_CSS = """
    #content {
        Select {
            margin-bottom: 1;
        }
    
        Label {
            color: $text-muted;
            width: 100%;
            text-align: center;
        }
    }
    """

    app: Terminal93

    def content(self) -> ComposeResult:
        yield Select(
            ((key, key) for key in sorted(self.app.available_themes)),
            allow_blank=False,
            value=self.app.current_theme.name,
        )
        yield Label(f'{len(self.app.available_themes)} themes available')

    def on_select_changed(self, event: Select.Changed) -> None:
        if event.value != self.app.current_theme.name:
            self.app.theme = event.value
            self.app.achievements.grant('stylish')
