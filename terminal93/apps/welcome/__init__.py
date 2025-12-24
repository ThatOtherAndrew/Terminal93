from terminal93 import Application

from .windows.welcome import MainWindow


class Welcome(Application):
    NAME = 'Welcome'
    ICON = '🔢'

    def launch(self) -> None:
        self.spawn_window(MainWindow)
