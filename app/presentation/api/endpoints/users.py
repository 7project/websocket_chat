from typing import List

from fastapi import APIRouter, Depends, HTTPException

from application.commands.create_user import CreateUserCommand
from application.mediator import Mediator
from application.dependencies import get_mediator, create_mediator_with_session
from infrastructure.database.session import get_db
from infrastructure.repositories.user import UserRepository
from presentation.api.schemas.user import UserCreateSchema, UserReadSchema

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserReadSchema)
async def create_user(
    schema: UserCreateSchema,
    db=Depends(get_db)
):
    user_repo = UserRepository(db)
    
    existing_user = await user_repo.get_by_email(schema.email)
    if existing_user:
        return UserReadSchema(id=existing_user.id, email=existing_user.email, username=existing_user.username)
    
    mediator = create_mediator_with_session(db)
    command = CreateUserCommand(email=schema.email, username=schema.username)
    user = await mediator.send(command)
    await db.commit()
    return UserReadSchema(id=user.oid, email=user.email.as_generic_type(), username=user.username.as_generic_type())


@router.get("/", response_model=List[UserReadSchema])
async def get_users(db=Depends(get_db)):
    user_repo = UserRepository(db)
    users = await user_repo.get_all()
    return [UserReadSchema(id=u.id, email=u.email, username=u.username) for u in users]


@router.get("/{user_id}", response_model=UserReadSchema)
async def get_user(user_id: str, db=Depends(get_db)):
    user_repo = UserRepository(db)
    user = await user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserReadSchema(id=user.id, email=user.email, username=user.username)
