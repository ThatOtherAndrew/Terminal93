from __future__ import annotations

import tomllib
from datetime import UTC, datetime
from importlib.resources import files
from typing import TYPE_CHECKING, TypedDict

from terminal93 import resources

if TYPE_CHECKING:
    from terminal93 import Terminal93


class Achievement(TypedDict):
    name: str
    description: str
    achieved: datetime | None


class Achievements(dict[str, Achievement]):
    def __init__(self, app: Terminal93) -> None:
        self.app = app

        with (files(resources) / 'achievements.toml').open('rb') as file:
            super().__init__(
                (
                    key,
                    {
                        'name': achievement['name'],
                        'description': achievement['description'],
                        'achieved': None,
                    },
                )
                for key, achievement in tomllib.load(file).items()
            )

    def grant(self, key: str) -> None:
        achievement = self.get(key, None)
        if achievement is None or achievement['achieved'] is not None:
            return

        achievement['achieved'] = datetime.now(UTC)
        self.app.mutate_reactive(type(self.app).achievements)

        self.app.notify(
            achievement['description'],
            title='🏆 ' + achievement['name'],
            severity='warning',
            timeout=8,
        )
