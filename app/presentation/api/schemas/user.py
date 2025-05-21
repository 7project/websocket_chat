from pydantic import BaseModel, ConfigDict


class UserCreateSchema(BaseModel):
    email: str
    username: str
    password: str


class UserReadSchema(BaseModel):
    id: str
    email: str
    username: str

    model_config = ConfigDict(from_attributes=True)
