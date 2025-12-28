from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import RichLog

from terminal93 import Window

from ..utils.client import Client
from ..widgets.chat_input import ChatInput


class MainWindow(Window):
    # language=SCSS
    DEFAULT_CSS = """
    #sidebar {
        dock: right;
        width: 8;
    }
    """

    WIDTH = 70
    HEIGHT = 30

    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)
        self.client = Client(self)

    def content(self) -> ComposeResult:
        yield VerticalScroll(id='sidebar')
        yield RichLog(wrap=True)
        yield ChatInput()

    def on_mount(self) -> None:
        self.run_worker(self.connect(), exclusive=True)

    async def on_unmount(self) -> None:
        await self.client.disconnect()

    async def on_chat_input_submitted(self, event: ChatInput.Submitted) -> None:
        await self.client.send(event.value)

    async def connect(self) -> None:
        await self.client.start_connection()
