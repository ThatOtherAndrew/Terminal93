from __future__ import annotations

import inspect
import os
from importlib import import_module
from pkgutil import iter_modules
from typing import TYPE_CHECKING

from textual import work
from textual.app import App
from textual.features import parse_features
from textual.reactive import var

from terminal93 import apps
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
        self.apps: dict[str, Application] = {}
        self.achievements = Achievements(self)

    def compose(self) -> ComposeResult:
        yield Desktop().data_bind(Terminal93.apps)

    @work
    async def on_mount(self) -> None:
        from terminal93 import Application

        for module_info in iter_modules(apps.__path__):
            if not module_info.ispkg:
                continue
            app = import_module(f'{apps.__name__}.{module_info.name}')
            for _, cls in inspect.getmembers(app, inspect.isclass):
                if issubclass(cls, Application) and cls is not Application:
                    self.install_app(cls, module_info.name)

        await self.push_screen_wait(BootScreen())

        self.apps['welcome'].launch()
        self.achievements.grant('hello_world')

    def install_app(self, app: type[Application], app_id: str) -> Application:
        app_instance = app(self)
        app_instance.install()
        self.apps[app_id] = app_instance
        self.mutate_reactive(Terminal93.apps)
        return app_instance
