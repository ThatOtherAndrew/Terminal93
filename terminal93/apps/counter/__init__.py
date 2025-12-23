from terminal93 import Application
from .windows.counter import MainWindow


class Counter(Application):
    NAME = 'Counter'
    ICON = '🔢'

    def launch(self) -> None:
        self.spawn_window(MainWindow())
