from textual import events
from textual.app import ComposeResult
from textual.containers import Center, CenterMiddle, Grid
from textual.reactive import reactive
from textual.widgets import Label, Placeholder

from terminal93.apps.base import Application


class DesktopApp(CenterMiddle, can_focus=True):
    # language=SCSS
    DEFAULT_CSS = """
    DesktopApp {
        &, Center {
            hatch: right $primary-background;
        }
        
        &:hover {
            outline: $primary-background;
        }
        
        &:focus {
            outline: $primary;
        }
    } 
    
    Center {
        width: auto;
        margin: 0 1;
    }
    
    Placeholder {
        width: 6;
        height: 3;
        margin-bottom: 1;
    }
    """

    BINDINGS = [('enter', 'launch', 'Launch app')]

    def __init__(self, app: Application) -> None:
        super().__init__()
        self.target_app = app

    def compose(self) -> ComposeResult:
        with Center():
            yield Placeholder()
        with Center():
            yield Label(self.target_app.NAME)

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
