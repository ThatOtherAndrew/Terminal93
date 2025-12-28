from dataclasses import dataclass

from textual.message import Message

from . import types


class Connected(Message):
    pass


@dataclass
class UserJoined(Message):
    user: types.User


@dataclass
class UserLeft(Message):
    user: types.User


@dataclass
class ChatMessage(Message):
    message: types.Message
