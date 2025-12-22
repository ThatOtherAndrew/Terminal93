from textual import events
from textual.app import ComposeResult
from textual.containers import Container, HorizontalGroup
from textual.reactive import var
from textual.widget import Widget


class TitleBar(HorizontalGroup):
    is_dragging = var(False)

    def __init__(self, window: Window) -> None:
        super().__init__()
        self.window = window

    # language=SCSS
    DEFAULT_CSS = '''
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
    '''

    def watch_is_dragging(self, new: bool) -> None:
        self.set_class(new, 'dragging')

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
    DEFAULT_CSS = '''
    Window {
        position: absolute;
        width: 40;
        height: 10;
        offset: 5 5;
    }
    '''

    def __init__(self, content: Widget):
        super().__init__()
        self.content = content

    def compose(self) -> ComposeResult:
        yield TitleBar(self)
        yield self.content

    def on_mouse_down(self) -> None:
        # bring to front
        top_window = self.parent.children[-1]
        if top_window is not self:
            self.parent.move_child(self, after=top_window)
