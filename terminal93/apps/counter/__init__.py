from terminal93 import Application

from .windows.main_window import CounterWindow


class Counter(Application):
    NAME = 'Counter'
    ICON = '🔢'

    def launch(self) -> None:
        self.spawn_window(CounterWindow)
