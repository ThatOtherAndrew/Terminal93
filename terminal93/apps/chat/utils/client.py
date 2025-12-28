from __future__ import annotations

import html
from typing import TYPE_CHECKING

from socketio import AsyncClient

from . import events, types

if TYPE_CHECKING:
    from ..windows.main_window import MainWindow


def html_unescape(data: dict[str, object]) -> dict[str, object]:
    unescaped = {}
    for key, value in data.items():
        if isinstance(value, str):
            unescaped[key] = html.unescape(value)
        else:
            unescaped[key] = value
    return unescaped


class Client(AsyncClient):
    URL = 'ws://www.windows93.net:8081'

    def __init__(self, window: MainWindow) -> None:
        super().__init__()
        self.window = window

        self.on('connect', self.on_connect)
        self.on('_connected', self.on_ready)
        self.on('message', self.on_message)
        self.on('user joined', self.on_user_join)
        self.on('user left', self.on_user_leave)
        self.on('update users', self.on_update_users)

    async def start_connection(self) -> None:
        await self.connect(self.URL)

    async def on_connect(self) -> None:
        await self.emit('user joined', (self.window.nick, '', '', ''))

    async def on_ready(self) -> None:
        self.window.post_message(events.Connected())

    async def on_user_join(self, data: dict) -> None:
        user = types.User(None, **html_unescape(data))
        self.window.post_message(events.UserJoined(user))

    async def on_user_leave(self, data: dict) -> None:
        user = types.User(None, **html_unescape(data))
        self.window.post_message(events.UserLeft(user))

    async def on_message(self, data: dict) -> None:
        message = types.Message(**html_unescape(data))
        self.window.post_message(events.ChatMessage(message))

    async def on_update_users(self, data: dict) -> None:
        self.window.users = [
            types.User(sid, **html_unescape(user_data))
            for sid, user_data in data.items()
        ]
