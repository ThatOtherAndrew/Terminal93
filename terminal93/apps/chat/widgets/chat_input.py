from textual import events
from textual.message import Message
from textual.widgets import TextArea


class ChatInput(TextArea):
    # language=SCSS
    DEFAULT_CSS = """
    ChatInput {
        height: auto;
        max-height: 10;
    }
    """

    BINDINGS = [('shift+enter', 'newline', 'New line')]

    class Submitted(Message):
        def __init__(self, value: str) -> None:
            super().__init__()
            self.value = value

    def __init__(self) -> None:
        super().__init__(placeholder='Send a message...')

    async def action_newline(self) -> None:
        await self._on_key(events.Key('enter', '\r'))

    def action_submit(self) -> None:
        self.post_message(ChatInput.Submitted(self.clear().replaced_text))

    def on_key(self, event: events.Key) -> None:
        if event.key == 'enter':
            event.stop()
            event.prevent_default()
            self.action_submit()
