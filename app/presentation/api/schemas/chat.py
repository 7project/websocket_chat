from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class ChatCreateSchema(BaseModel):
    title: str
    type: str
    creator_id: Optional[str] = None
    participants: Optional[List[str]] = []


class ChatReadSchema(BaseModel):
    id: str
    title: str
    type: str
    participants: List[str]

    model_config = ConfigDict(from_attributes=True)


class AddParticipantSchema(BaseModel):
    user_id: str


class ParticipantSchema(BaseModel):
    user_id: str
    username: Optional[str] = None
    email: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
