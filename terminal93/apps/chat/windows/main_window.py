from textual.app import ComposeResult
from textual.reactive import var
from textual.widgets import RichLog

from terminal93 import Window

from ..utils import events
from ..utils.client import Client
from ..utils.types import User
from ..widgets.chat_input import ChatInput
from ..widgets.sidebar import Sidebar


class MainWindow(Window):
    WIDTH = 70
    HEIGHT = 30

    users: var[list[User]] = var([])

    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)
        self.client = Client(self)

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

    def on_connected(self) -> None:
        self.title = 'Chat - Connected'
        self.query_one(Sidebar).loading = False

    def on_user_joined(self, event: events.UserJoined) -> None:
        self.query_one(RichLog).write('User joined: ' + event.user.nick)

    def on_user_left(self, event: events.UserLeft) -> None:
        self.query_one(RichLog).write('User left: ' + event.user.nick)

    def on_chat_message(self, event: events.ChatMessage) -> None:
        self.query_one(RichLog).write(f'{event.message.nick}: {event.message.msg}')

    async def connect(self) -> None:
        await self.client.start_connection()
