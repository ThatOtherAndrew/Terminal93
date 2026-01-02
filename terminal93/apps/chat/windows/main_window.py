import random
import re
from importlib.resources import files

from rich.text import Text
from textual.app import ComposeResult
from textual.reactive import var
from textual.widgets import RichLog

from terminal93 import Terminal93, Window

from .. import resources
from ..utils import events
from ..utils.client import Client
from ..utils.types import User
from ..widgets.chat_input import ChatInput
from ..widgets.sidebar import Sidebar


class ChatWindow(Window):
    app: Terminal93

    WIDTH = 70
    HEIGHT = 30

    users: var[list[User]] = var([])
    nick: var[str] = var('')

    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)
        self.client = Client(self)
        random_nick = f'term93_{random.randint(1, 999):03}'
        self.set_reactive(ChatWindow.nick, random_nick)

        with (files(resources) / 'nsfw_domains.txt').open('r') as file:
            self.nsfw_domains = {
                line
                for line in map(str.strip, file)
                if line and not line.startswith('#')
            }

    def content(self) -> ComposeResult:
        yield Sidebar().data_bind(ChatWindow.users)
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
            event.message.colour_nick(), (': ', 'dim'), self.sanitise(event.message.msg)
        )
        self.query_one(RichLog).write(msg)

    async def connect(self) -> None:
        await self.client.start_connection()

    def sanitise(self, message: str) -> str:
        for match in re.finditer(r'https?://([^/\s]+)\S*', message):
            url = match.group()
            domain = match.group(1)
            if any(domain.endswith(nsfw) for nsfw in self.nsfw_domains):
                message = message.replace(url, '[[HYPERLINK BLOCKED]]')
        return message
