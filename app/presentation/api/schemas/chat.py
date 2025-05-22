from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class ChatCreateSchema(BaseModel):
    title: str
    type: str
    participants: Optional[List[str]] = []


class ChatReadSchema(BaseModel):
    id: str
    title: str
    type: str
    participants: List[str]

    model_config = ConfigDict(from_attributes=True)
