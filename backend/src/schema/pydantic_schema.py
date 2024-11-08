from pydantic import BaseModel
from typing import List
from typing import Any, Union
from datetime import datetime
from uuid import UUID




class QueryResponse(BaseModel):
    status: Any
    response: Any


class UpsertVectorRequest(BaseModel):
    collection_name: str
    file_path : str



class ChatBase(BaseModel):
    topic: str





class Chat(ChatBase):
    id: Union[str, UUID]
    created_at: datetime
    updated_at: datetime
    last_message_datetime: datetime

    class Config:
        orm_mode = True
        from_attributes = True



class MessageBase(BaseModel):
    text: str
    sender: str


class MessageCreate(MessageBase):
    pass

class ReportMessage(BaseModel):
    description: str
    message_id: str

class Message(MessageBase):
    id: Union[str, UUID]
    chat_id: Union[str, UUID]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True

class QueryInput(BaseModel):
    message: Message
    output_language: str
    chat_history: List[str]

class ChatCreateMessage(BaseModel):
    created_at: datetime
    id : Union[str, UUID]
    sender : str
    text : str
    updated_at : datetime

class ChatCreate(BaseModel):
    message : ChatCreateMessage