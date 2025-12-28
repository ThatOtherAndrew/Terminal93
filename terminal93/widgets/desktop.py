from textual import events
from textual.app import ComposeResult
from textual.containers import CenterMiddle, Grid
from textual.reactive import reactive
from textual.widgets import Label, Placeholder

from terminal93.apps.base import Application


class AppIcon(Placeholder):
    # language=SCSS
    DEFAULT_CSS = """
    AppIcon {
        text-align: center;
    }
    """

    ALLOW_SELECT = False

    def __init__(self, icon: str) -> None:
        super().__init__(icon)

    @staticmethod
    def on_click(event: events.Click) -> None:
        event.prevent_default()


class AppLabel(Label):
    # language=SCSS
    DEFAULT_CSS = """
    AppLabel {
        text-align: center;
    }
    """

    ALLOW_SELECT = False


class DesktopApp(CenterMiddle, can_focus=True):
    # language=SCSS
    DEFAULT_CSS = """
    DesktopApp {
        &, AppLabel {
            hatch: right $primary-background;
        }
        
        &:hover {
            outline: $primary-background;
            AppLabel {
                outline-left: $primary-background;
                outline-right: $primary-background;
            }
        }
        
        &:focus {
            outline: $primary;
            AppLabel {
                outline-left: $primary;
                outline-right: $primary;
            }
        }
    }
    
    Placeholder {
        position: absolute;
        offset: 3 1;
        width: 6;
        height: 3;
    }
    
    AppLabel {
        position: absolute;
        offset: 0 5;
        width: 12;
        height: 1;
    }
    """

    BINDINGS = [('enter', 'launch', 'Launch app')]

    def __init__(self, app: Application) -> None:
        super().__init__()
        self.target_app = app

    def compose(self) -> ComposeResult:
        yield AppIcon(self.target_app.ICON)
        yield AppLabel(self.target_app.NAME)

    def action_launch(self) -> None:
        self.target_app.launch()

    def on_click(self, event: events.Click) -> None:
        if event.chain == 2:
            self.action_launch()


class Desktop(Grid):
    # language=SCSS
    DEFAULT_CSS = """
    Desktop {
        position: absolute;
        width: 100%;
        height: 100%;
        padding: 1 2;

        grid-gutter: 1;
        grid-rows: 7;
        grid-columns: 12;
        
        hatch: right $primary-background;
    } 
    """

    apps: reactive[list[Application]] = reactive([], recompose=True)

    def compose(self) -> ComposeResult:
        yield from map(DesktopApp, self.apps)
