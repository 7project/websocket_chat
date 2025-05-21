from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ReadReceiptCreateSchema(BaseModel):
    message_id: str
    user_id: str


class ReadReceiptReadSchema(BaseModel):
    message_id: str
    user_id: str
    read_at: datetime

    model_config = ConfigDict(from_attributes=True)
