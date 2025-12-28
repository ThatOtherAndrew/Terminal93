from __future__ import annotations

from typing import TYPE_CHECKING

from socketio import AsyncClient
from textual.widgets import RichLog

if TYPE_CHECKING:
    from ..windows.main_window import MainWindow


class Client(AsyncClient):
    URL = 'http://www.windows93.net:8081'
    HEADERS = {
        'Accept': '*/*',
        'Accept-Encoding': 'identity',
        'Accept-Language': '*',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': 'www.windows93.net',
        'Origin': 'https://www.windows93.net',
        'Pragma': 'no-cache',
        'Referer': 'https://www.windows93.net/trollbox/index.php',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    }

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
        await self.connect(self.URL, self.HEADERS)

    async def on_connect(self) -> None:
        await self.emit('user joined', ('AndromedaClient', '', '', ''))

    async def on_ready(self) -> None:
        self.window.notify('Connected to server')

    async def on_user_join(self, data: dict) -> None:
        self.window.query_one(RichLog).write(data)

    async def on_user_leave(self, data: dict) -> None:
        self.window.query_one(RichLog).write(data)

    async def on_message(self, data: dict) -> None:
        self.window.query_one(RichLog).write(data)

    async def on_update_users(self, data: dict) -> None: ...
