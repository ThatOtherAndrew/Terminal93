from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, cast

from textual.containers import Container, HorizontalGroup
from textual.message import Message
from textual.reactive import reactive, var
from textual.widgets import Button, Label, Placeholder

if TYPE_CHECKING:
    from textual import events
    from textual.app import ComposeResult, RenderResult

    from terminal93 import Application, Terminal93


class WindowAction(Enum):
    MINIMISE = '🗕'
    MAXIMISE = '🗖'
    UNMAXIMISE = '🗗'
    CLOSE = '🗙'


class TitleLabel(Label):
    # language=SCSS
    DEFAULT_CSS = """
    TitleLabel {
        width: 1fr;
        padding: 0 2;
        text-overflow: ellipsis;
    }
    """

    ALLOW_SELECT = False

    title = reactive('')

    def render(self) -> RenderResult:
        return self.title


class TitleBarButton(Button):
    # language=SCSS
    DEFAULT_CSS = """
    TitleBarButton.-style-default {
        max-width: 3;
        max-height: 1;
        background: transparent;
        
        &:hover {
            background: $primary-darken-3;
        }
    }
    """

    def __init__(self, window: Window, action: WindowAction) -> None:
        super().__init__(label=action.value, compact=True)
        self.window = window
        self.window_action = action

    @staticmethod
    def on_mouse_down(event: events.MouseDown) -> None:
        event.stop()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        event.stop()

        if self.window_action == WindowAction.CLOSE:
            self.post_message(Window.Close(self.window))


class TitleBar(HorizontalGroup):
    # language=SCSS
    DEFAULT_CSS = """
    TitleBar {
        height: 1;
        background: $primary;

        &:hover {
            background: $primary-lighten-1;
        }

        &.dragging {
          background: $primary-darken-1;
        }
    }
    
    HorizontalGroup {
        width: auto;
    }
    """

    title = var('')
    is_dragging = var(False, toggle_class='dragging')

    def __init__(self, window: Window) -> None:
        super().__init__()
        self.window = window

    def compose(self) -> ComposeResult:
        yield TitleLabel().data_bind(TitleBar.title)
        with HorizontalGroup():
            yield TitleBarButton(self.window, WindowAction.MINIMISE)
            yield TitleBarButton(self.window, WindowAction.MAXIMISE)
            yield TitleBarButton(self.window, WindowAction.CLOSE)

    def on_mouse_down(self, event: events.MouseDown) -> None:
        # don't handle drag if not left-clicked
        if event.button != 1:
            return

        # handle drag
        self.capture_mouse()
        self.is_dragging = True

    def on_mouse_move(self, event: events.MouseMove) -> None:
        if self.is_dragging:
            self.window.styles.offset = (
                self.window.styles.offset.x.value + event.delta_x,
                self.window.styles.offset.y.value + event.delta_y,
            )

    def on_mouse_up(self) -> None:
        self.release_mouse()
        self.is_dragging = False


class Window(Container):
    # language=SCSS
    DEFAULT_CSS = """
    Window {
        position: absolute;
        min-width: 15;
        min-height: 1;
        
        * {
            tint: black 25%;
        }
        
        &:focus-within * {
            tint: transparent;
        }
    }

    #content {
        padding: 1 2;
    }
    """

    WIDTH = 40
    HEIGHT = 10
    TITLE: str | None = None

    class Close(Message):
        def __init__(self, window: Window) -> None:
            super().__init__()
            self.window = window

    title = var('')
    position = var((0, 0))

    def __init__(
        self,
        owner: Application,
        *,
        position: tuple[int, int] = (10, 5),
    ) -> None:
        super().__init__()
        self.owner = owner
        self.position = position
        self.title = self.owner.NAME if self.TITLE is None else self.TITLE

        self.styles.width = self.WIDTH
        self.styles.height = self.HEIGHT
        self.can_focus = True

    @property
    def app(self) -> Terminal93:
        return cast('Terminal93', super().app)

    def content(self) -> ComposeResult:
        yield Placeholder('<no content>')

    def compose(self) -> ComposeResult:
        yield TitleBar(self).data_bind(Window.title)
        with Container(id='content'):
            yield from self.content()

    def watch_position(self, new: tuple[int, int]) -> None:
        self.styles.offset = new

    def on_focus(self) -> None:
        # bring to front
        top_window = self.parent.children[-1]
        if top_window is not self:
            self.parent.move_child(self, after=top_window)

    def on_descendant_focus(self) -> None:
        self.on_focus()

    def on_window_close(self, event: Window.Close) -> None:
        event.stop()
        self.owner.quit()
