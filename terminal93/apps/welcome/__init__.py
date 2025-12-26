from terminal93 import Application

from .windows.main_window import MainWindow


class Welcome(Application):
    NAME = 'Welcome'
    ICON = '🔢'

    def launch(self) -> None:
        self.spawn_window(MainWindow)
