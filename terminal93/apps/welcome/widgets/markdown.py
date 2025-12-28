from textual.widgets import Markdown

from terminal93 import Terminal93

# noinspection MarkdownUnresolvedFileReference
# language=Markdown
MESSAGE = """
# Welcome to Terminal93!

Terminal93 is a lil fantasy desktop inspired by the likes of
[WINDOWS93](https://www.windows93.net/).

The trick? Everything you see is rendered in the terminal, using *only text!*
It's all an elaborate **illusion** of a graphical user interface using the
power of [Rich](https://rich.readthedocs.io/en/stable/introduction.html),
[Textual](https://textual.textualize.io/), and
[Unicode](https://home.unicode.org/).

Think of this as a **sandbox** - it's not a game in the sense of levels and
bosses to beat, but there are some [achievements](secret_link) to hunt down!
Can you find them all?

Have fun~

— ⚝
"""


class WelcomeMarkdown(Markdown):
    app: Terminal93

    def __init__(self) -> None:
        super().__init__(MESSAGE)

    def on_markdown_link_clicked(self, event: Markdown.LinkClicked) -> None:
        if event.href == 'secret_link':
            event.stop()
            event.prevent_default()
            self.app.achievements.grant('warm_welcome')
