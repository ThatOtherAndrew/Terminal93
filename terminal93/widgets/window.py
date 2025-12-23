from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from textual.containers import Container, HorizontalGroup
from textual.reactive import var
from textual.widget import Widget
from textual.widgets import Button, Label

if TYPE_CHECKING:
    from terminal93 import Application
    from textual import events
    from textual.app import ComposeResult


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
    }
    """

    ALLOW_SELECT = False


class TitleBarButton(Button):
    # language=SCSS
    DEFAULT_CSS = """
    TitleBarButton.-style-default {
        max-width: 3;
        max-height: 1;
        background: $primary;
        
        &:hover {
            background: $primary-darken-3   ;
        }
    }
    """

    def __init__(self, action: WindowAction) -> None:
        super().__init__(label=action.value, compact=True)
        self.action = action


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

    is_dragging = var(False, toggle_class='dragging')

    def __init__(self, window: Window) -> None:
        super().__init__()
        self.window = window

    def compose(self) -> ComposeResult:
        yield TitleLabel(self.window.title)
        with HorizontalGroup():
            yield TitleBarButton(WindowAction.MINIMISE)
            yield TitleBarButton(WindowAction.MAXIMISE)
            yield TitleBarButton(WindowAction.CLOSE)

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
    # language=CSS
    DEFAULT_CSS = """
    Window {
        position: absolute;
        width: 40;
        height: 10;
        offset: 5 5;
    }
    """

    title = var('')
    position = var((0, 0))

    def __init__(
        self,
        owner: Application,
        title: str,
        content: Widget,
        *,
        position: tuple[int, int] = (10, 5),
    ) -> None:
        super().__init__()
        self.owner = owner
        self.title = title
        self.content = content
        self.position = position

    def compose(self) -> ComposeResult:
        yield TitleBar(self)
        yield self.content

    def watch_title(self, new: str) -> None:
        if self.is_mounted:
            self.query_one(TitleBar).title = new

    def watch_position(self, new: tuple[int, int]) -> None:
        self.styles.offset = new

    def on_mouse_down(self) -> None:
        # bring to front
        top_window = self.parent.children[-1]
        if top_window is not self:
            self.parent.move_child(self, after=top_window)
