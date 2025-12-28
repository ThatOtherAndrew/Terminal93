from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.reactive import reactive
from textual.widgets import Label

from ..utils.types import User


class Sidebar(VerticalScroll):
    # language=SCSS
    DEFAULT_CSS = """
    Sidebar {
        dock: right;
        width: 15;
    }
    
    Label {
        width: 100%;
        height: 1;
        text-overflow: ellipsis;

        &:hover {
            background: $primary-background;
        }
    }
    """

    users: reactive[list[User]] = reactive([], recompose=True)

    def __init__(self) -> None:
        super().__init__()
        self.loading = True

    def compose(self) -> ComposeResult:
        for user in self.users:
            yield Label(user.colour_nick())
