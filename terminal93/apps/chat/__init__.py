from terminal93 import Application

from .windows.main_window import MainWindow


class Chat(Application):
    NAME = 'Chat'
    ICON = '💬'

    def launch(self) -> None:
        self.spawn_window(MainWindow)
