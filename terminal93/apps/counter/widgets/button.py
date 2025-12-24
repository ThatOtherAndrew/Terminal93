from textual import events
from textual.reactive import var
from textual.widgets import Button


class CounterButton(Button):
    count = var(0)

    def __init__(self) -> None:
        super().__init__('0', 'primary')
        self.active_effect_duration = 0.2

    def watch_count(self, new: int) -> None:
        self.label = str(new)

    def on_mouse_down(self, event: events.MouseDown) -> None:
        event.stop()
        event.prevent_default()
        self.hold()

    def on_mouse_up(self, event: events.MouseUp) -> None:
        event.stop()
        event.prevent_default()
        self.release()

    @staticmethod
    def on_click(event: events.Click) -> None:
        event.prevent_default()

    def hold(self) -> None:
        self.add_class('-active')

    def release(self) -> None:
        self.remove_class('-active')

        if self.action is None:
            self.post_message(Button.Pressed(self))
        else:
            self.call_later(
                self.app.run_action, self.action, default_namespace=self._parent
            )
