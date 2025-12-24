from __future__ import annotations

from typing import TYPE_CHECKING

from textual import work
from textual.app import App
from textual.widgets import Static

from terminal93.screens.BootScreen import BootScreen

if TYPE_CHECKING:
    from textual.app import ComposeResult
    from terminal93 import Application


class Terminal93(App):
    # language=SCSS
    CSS = """
    #background {
        width: 100vw;
        height: 100vh;
        hatch: right $primary-background;
    }
    """

    def __init__(self) -> None:
        super().__init__()
        self.apps: list[Application] = []

    def compose(self) -> ComposeResult:
        yield Static(id='background')

    @work
    async def on_mount(self) -> None:
        from terminal93.apps.counter import Counter
        from terminal93.apps.welcome import Welcome

        self.install_app(Counter)
        self.install_app(Welcome)

        await self.push_screen_wait(BootScreen())

        for app in self.apps:
            app.launch()

    def install_app(self, app: type[Application]) -> None:
        app_instance = app(self)
        app_instance.install()
        self.apps.append(app(self))
