import random

from rich.text import Text
from textual.app import ComposeResult
from textual.reactive import var
from textual.widgets import RichLog

from terminal93 import Terminal93, Window

from ..utils import events
from ..utils.client import Client
from ..utils.types import User
from ..widgets.chat_input import ChatInput
from ..widgets.sidebar import Sidebar


class MainWindow(Window):
    app: Terminal93

    WIDTH = 70
    HEIGHT = 30

    users: var[list[User]] = var([])
    nick: var[str] = var('')

    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)
        self.client = Client(self)
        random_nick = f'term93_{random.randint(1, 999):03}'
        self.set_reactive(MainWindow.nick, random_nick)

    def content(self) -> ComposeResult:
        yield Sidebar().data_bind(MainWindow.users)
        yield RichLog(min_width=1, wrap=True)
        yield ChatInput()

    def on_mount(self) -> None:
        self.title = 'Chat - Disconnected'
        self.run_worker(self.connect(), exclusive=True)

    async def on_unmount(self) -> None:
        await self.client.disconnect()

    async def on_chat_input_submitted(self, event: ChatInput.Submitted) -> None:
        await self.client.send(event.value)
        self.app.achievements.grant('chatterbox')
        if any(
            magic_word in event.value.lower() for magic_word in ('please', 'thank you')
        ):
            self.app.achievements.grant('magic_word')

    def on_connected(self) -> None:
        self.title = 'Chat - Connected'
        self.query_one(Sidebar).loading = False

    def on_user_joined(self, event: events.UserJoined) -> None:
        msg = Text('User joined: ', 'dim') + event.user.colour_nick()
        self.query_one(RichLog).write(msg)

    def on_user_left(self, event: events.UserLeft) -> None:
        msg = Text('User left: ', 'dim') + event.user.colour_nick()
        self.query_one(RichLog).write(msg)

    def on_chat_message(self, event: events.ChatMessage) -> None:
        msg = Text.assemble(
            event.message.colour_nick(), (': ', 'dim'), event.message.msg
        )
        self.query_one(RichLog).write(msg)

    async def connect(self) -> None:
        await self.client.start_connection()
