import os
import platform
import random
import sys
from asyncio import sleep
from importlib.metadata import version

from textual import work
from textual.app import ComposeResult
from textual.containers import Center
from textual.renderables.bar import Bar
from textual.screen import Screen
from textual.widget import Widget
from textual.widgets import Static, ProgressBar

LOGO = r'''
M""""""""M                              oo                   dP .d888b. d8888b.
Mmmm  mmmM                                                   88 Y8' `88     `88
MMMM  MMMM .d8888b. 88d888b. 88d8b.d8b. dP 88d888b. .d8888b. 88 `8bad88  aaad8'
MMMM  MMMM 88ooood8 88'  `88 88'`88'`88 88 88'  `88 88'  `88 88     `88     `88
MMMM  MMMM 88.  ... 88       88  88  88 88 88    88 88.  .88 88 d.  .88     .88
MMMM  MMMM `88888P' dP       dP  dP  dP dP dP    dP `88888P8 dP `8888P  d88888P
MMMMMMMMMM                                                                     
'''.strip('\n')


class LoadingBar(ProgressBar):
    # https://github.com/Textualize/textual/pull/5963
    class ThickBarRenderable(Bar):
        HALF_BAR_LEFT = "▐"
        BAR = "█"
        HALF_BAR_RIGHT = "▌"

    def __init__(self) -> None:
        super().__init__(show_percentage=False, show_eta=False)
        self.BAR_RENDERABLE = LoadingBar.ThickBarRenderable


class Splash(Widget):
    # language=CSS
    DEFAULT_CSS = '''
    Static {
        width: auto;
    }
    
    .spacer {
        width: 1fr;
        height: 1fr;
    }
    '''

    def compose(self) -> ComposeResult:
        yield Static(classes='spacer')
        yield Static(classes='spacer')
        with Center():
            yield Static(LOGO, id='logo')
        yield Static(classes='spacer')
        with Center():
            yield LoadingBar()
        yield Static(classes='spacer')


class BootScreen(Screen):
    # language=CSS
    DEFAULT_CSS = '''
    #log {
        margin: 1 2;
    }
    '''

    BINDINGS = [
        ('escape,enter', 'app.pop_screen', 'Skip boot screen'),
    ]

    LINES = [
        'Twiddling thumbs...',
        'Wasting your time...',
        'Pushing bits...',
        'Downloading malware...',
        'Coming up with mediocre jokes...',
        'Preparing crashes...',
        'Implementing bugs...',
    ]

    def compose(self) -> ComposeResult:
        yield Static(
            f'Terminal93 OS version {version('terminal93')}\n'
            f'(C) 1993 Andromeda Industries, Inc.\n'
            f'\n'
            f'Python ({platform.python_implementation()}) {sys.version}\n'
            f'Platform {platform.platform()}\n'
            f'Terminal {os.environ.get('TERM', 'unknown')}\n'
            f'\n'
            f'Textual:  v{version('textual')}\n'
            f'Rich:     v{version('rich')}\n'
            f'\n',
            id='log'
        )

    def on_mount(self) -> None:
        self.simulate_load()

    @work
    async def simulate_load(self):
        log = self.query_one(Static)

        await sleep(0.5)
        for line in random.sample(self.LINES, 5):
            log.content += line + '\n'
            await sleep(random.random())
        await sleep(0.5)

        await self.remove_children()
        await self.mount(Splash())
        await sleep(3)

        # noinspection PyAsyncCall
        self.dismiss()
