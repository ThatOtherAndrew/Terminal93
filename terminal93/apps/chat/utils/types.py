from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    sid: str | None
    nick: str
    color: str
    style: str
    home: str
    room: str
    isBot: bool


@dataclass(frozen=True)
class Message:
    date: int
    nick: str
    color: str
    style: str
    home: str
    msg: str
