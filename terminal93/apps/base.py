from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from terminal93 import Terminal93, Window


class Application(ABC):
    NAME = 'Unnamed App'
    ICON = '❓'

    def __init__(self, app: Terminal93) -> None:
        self.app = app
        self.windows: list[Window] = []

    def install(self) -> None:
        pass

    def spawn_window(self, window: type[Window], focus: bool = True) -> Window:
        window_instance = window(self)
        self.windows.append(window_instance)
        self.app.mount(window_instance)

        if focus:
            window_instance.focus_window()

        return window_instance

    @abstractmethod
    def launch(self) -> None:
        pass

    def quit(self) -> None:
        # close windows in reverse spawn order for stack-like behaviour
        for window in reversed(self.windows):
            window.remove()
