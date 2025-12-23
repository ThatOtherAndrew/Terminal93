from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from ..widgets.window import Window

if TYPE_CHECKING:
    from textual.widget import Widget
    from terminal93 import Terminal93


class Application(ABC):
    NAME = 'Unnamed App'
    ICON = '❓'

    def __init__(self, app: Terminal93) -> None:
        self.app = app
        self.windows: list[Window] = []

    def install(self) -> None:
        pass

    def spawn_window(self, content: Widget, title: str | None = None) -> Window:
        if title is None:
            title = self.NAME

        window = Window(self, title, content)
        self.windows.append(window)
        self.app.mount(window)
        return window

    @abstractmethod
    def launch(self) -> None:
        pass

    def quit(self) -> None:
        # close windows in reverse spawn order for stack-like behaviour
        for window in reversed(self.windows):
            window.remove()
