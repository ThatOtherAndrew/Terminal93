from dataclasses import dataclass

from rich.text import Text


def colour_nick(data: User | Message) -> Text:
    safe_colour = data.color.lower().split(';')[0]
    return Text(data.nick, safe_colour)


@dataclass(frozen=True)
class User:
    sid: str | None
    nick: str
    color: str
    style: str
    home: str
    room: str
    isBot: bool

    def colour_nick(self) -> Text:
        return colour_nick(self)


@dataclass(frozen=True)
class Message:
    date: int
    nick: str
    color: str
    style: str
    home: str
    msg: str

    def colour_nick(self) -> Text:
        return colour_nick(self)
