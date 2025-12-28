from __future__ import annotations

import tomllib
from datetime import UTC, datetime
from importlib.resources import files
from typing import TYPE_CHECKING, TypedDict

from terminal93 import resources

if TYPE_CHECKING:
    from terminal93 import Terminal93


class Achievement(TypedDict):
    icon: str
    name: str
    description: str
    secret: bool
    achieved: datetime | None


class Achievements(dict[str, Achievement]):
    def __init__(self, app: Terminal93) -> None:
        self.app = app
        self.achieved_count = 0

        with (files(resources) / 'achievements.toml').open('rb') as file:
            super().__init__(
                (key, {'secret': False, **achievement, 'achieved': None})
                for key, achievement in tomllib.load(file).items()
            )

    def grant(self, key: str) -> None:
        achievement = self.get(key, None)
        if achievement is None or achievement['achieved'] is not None:
            return

        achievement['achieved'] = datetime.now(UTC)
        self.achieved_count += 1
        self.app.mutate_reactive(type(self.app).achievements)

        self.app.notify(
            achievement['description'],
            title='🏆 ' + achievement['name'],
            severity='warning',
            timeout=8,
        )
