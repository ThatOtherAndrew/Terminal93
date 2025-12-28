from terminal93 import Application

from .windows.main_window import AchievementsWindow


class Achievements(Application):
    NAME = 'Achievements'
    ICON = '🏆'

    def launch(self) -> None:
        self.spawn_window(AchievementsWindow)
