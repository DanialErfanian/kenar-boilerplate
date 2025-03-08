import abc
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel

from chat.models import Chat


class EventType(str, Enum):
    UNKNOWN = "UNKNOWN"
    NEW_MESSAGE = "NEW_MESSAGE"
    NEW_CHATBOT_MESSAGE = "NEW_CHATBOT_MESSAGE"


class MessageSenderSide(str, Enum):
    SIDE_UNKNOWN = "SIDE_UNKNOWN"
    BUYER = "BUYER"
    SELLER = "SELLER"


class MessageSenderType(str, Enum):
    TYPE_UNKNOWN = "TYPE_UNKNOWN"
    HUMAN = "HUMAN"
    BOT = "BOT"


class MessageSender(BaseModel):
    side: MessageSenderSide = MessageSenderSide.SIDE_UNKNOWN
    type: MessageSenderType = MessageSenderType.TYPE_UNKNOWN


class ConversationType(str, Enum):
    UNKNOWN = "UNKNOWN"
    POST = "POST"
    BOT = "BOT"


class Conversation(BaseModel):
    id: str
    type: ConversationType
    post_token: Optional[str] = None


class MessageType(str, Enum):
    UNKNOWN = "UNKNOWN"
    TEXT = "TEXT"


class Message(BaseModel):
    id: str
    conversation: Conversation
    sender: MessageSender
    type: MessageType
    sent_at: datetime
    text: Optional[str] = None


class Event(BaseModel):
    type: EventType
    new_message: Optional[Message] = None
    new_chatbot_message: Optional[Message] = None
    metadata: Optional[dict] = None


class EventHandler(BaseModel):
    def handle_event(self, event: Event):
        if event.type == EventType.NEW_MESSAGE:
            self.handle_new_message(event)
        elif event.type == EventType.NEW_CHATBOT_MESSAGE:
            self.handle_new_chatbot_message(event)
        else:
            raise ValueError(f"Unknown event type: {event.type}")

    def handle_new_message(self, event: Event):
        raise NotImplemented

    def handle_new_chatbot_message(self, event: Event):
        raise NotImplemented


class StartChatSessionUser(BaseModel):
    id: str


class StartChatSessionRequest(BaseModel):
    post_token: str
    user_id: str
    peer_id: str
    callback_url: str
    supplier: StartChatSessionUser
    demand: StartChatSessionUser


class ChatMessagePayloadUser(BaseModel):
    id: str
    is_supply: bool


class ChatMessagePayloadMetadata(BaseModel):
    title: str
    category: str
    post_token: str


class ChatMessageTextData(BaseModel):
    text: str


class ChatMessagePayload(BaseModel):
    id: str
    type: str
    data: ChatMessageTextData
    sender: ChatMessagePayloadUser
    receiver: ChatMessagePayloadUser
    metadata: ChatMessagePayloadMetadata
    sent_at: int


class Notification(BaseModel):
    type: str
    timestamp: int
    payload: ChatMessagePayload


class Handler(abc.ABC):
    @abc.abstractmethod
    def handle(self, notification: Notification):
        raise NotImplemented


class ChatNotificationHandler(Handler):
    def __init__(self, chat: Chat):
        self.chat = chat

    def handle(self, notification: Notification):
        match notification.type:
            case "CHAT_MESSAGE":
                if not notification.payload.sender.is_supply:
                    self.handle_chat_message(notification.timestamp, notification.payload)

    @abc.abstractmethod
    def handle_chat_message(self, timestamp: int, payload: ChatMessagePayload):
        raise NotImplemented
