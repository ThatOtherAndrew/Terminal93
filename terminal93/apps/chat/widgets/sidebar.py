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
        width: 8;
    }
    """

    users: reactive[list[User]] = reactive([], recompose=True)

    def compose(self) -> ComposeResult:
        for user in self.users:
            yield Label(user.nick)
