from terminal93 import Application

from .windows.main_window import ThemesWindow


class Themes(Application):
    NAME = 'Themes'
    ICON = '🎨'

    def launch(self) -> None:
        self.spawn_window(ThemesWindow)
