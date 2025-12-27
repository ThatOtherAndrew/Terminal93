from __future__ import annotations

import os
from typing import TYPE_CHECKING

from textual import work
from textual.app import App
from textual.features import parse_features
from textual.reactive import var

from terminal93.screens.BootScreen import BootScreen
from terminal93.utils.achievements import Achievements
from terminal93.widgets.desktop import Desktop

if TYPE_CHECKING:
    from textual.app import ComposeResult

    from terminal93 import Application


class Terminal93(App):
    apps: var[list[Application]] = var([])
    achievements: var[Achievements] = var(None)

    def __init__(self) -> None:
        css_path = None
        if 'debug' in parse_features(os.getenv('TEXTUAL', '')):
            css_path = 'resources/global.tcss'
        super().__init__(css_path=css_path)
        self.apps: list[Application] = []
        self.achievements = Achievements(self)

    def compose(self) -> ComposeResult:
        yield Desktop().data_bind(Terminal93.apps)

    @work
    async def on_mount(self) -> None:
        from terminal93.apps.achievements import Achievements
        from terminal93.apps.chat import Chat
        from terminal93.apps.counter import Counter
        from terminal93.apps.welcome import Welcome

        self.install_app(Welcome).launch()
        self.install_app(Achievements)
        self.install_app(Counter)
        self.install_app(Chat)

        await self.push_screen_wait(BootScreen())

        self.achievements.grant('hello_world')

    def install_app(self, app: type[Application]) -> Application:
        app_instance = app(self)
        app_instance.install()
        self.apps.append(app(self))
        self.mutate_reactive(Terminal93.apps)
        return app_instance
