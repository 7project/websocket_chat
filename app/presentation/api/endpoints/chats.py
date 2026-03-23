from typing import List

from fastapi import APIRouter, Depends, HTTPException

from application.commands.create_chat import CreateChatCommand
from application.mediator import Mediator
from application.dependencies import get_mediator, create_mediator_with_session
from infrastructure.database.session import get_db
from infrastructure.repositories.chat import ChatRepository
from infrastructure.repositories.user import UserRepository
from presentation.api.schemas.chat import ChatCreateSchema, ChatReadSchema, AddParticipantSchema, ParticipantSchema

router = APIRouter(prefix="/chats", tags=["chats"])


@router.post("/", response_model=ChatReadSchema)
async def create_chat(
    schema: ChatCreateSchema,
    db=Depends(get_db)
):
    creator_id = schema.creator_id
    if not creator_id:
        raise HTTPException(status_code=400, detail="creator_id is required")
    
    mediator = create_mediator_with_session(db)
    command = CreateChatCommand(
        title=schema.title,
        creator_id=creator_id,
        participants=schema.participants or []
    )
    chat = await mediator.send(command)
    await db.commit()
    
    chat_repo = ChatRepository(db)
    saved_chat = await chat_repo.get_by_id(chat.oid)
    
    return ChatReadSchema(
        id=saved_chat.id,
        title=saved_chat.title,
        type=saved_chat.type,
        participants=[p.user_id for p in saved_chat.participants]
    )


@router.get("/", response_model=List[ChatReadSchema])
async def get_chats(db=Depends(get_db)):
    chat_repo = ChatRepository(db)
    chats = await chat_repo.get_all()
    return [
        ChatReadSchema(
            id=c.id,
            title=c.title,
            type=c.type,
            participants=[p.user_id for p in c.participants]
        )
        for c in chats
    ]


@router.get("/{chat_id}", response_model=ChatReadSchema)
async def get_chat(chat_id: str, db=Depends(get_db)):
    chat_repo = ChatRepository(db)
    chat = await chat_repo.get_by_id(chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return ChatReadSchema(
        id=chat.id,
        title=chat.title,
        type=chat.type,
        participants=[p.user_id for p in chat.participants]
    )


@router.post("/{chat_id}/participants", response_model=ChatReadSchema)
async def add_participant(
    chat_id: str,
    schema: AddParticipantSchema,
    db=Depends(get_db)
):
    chat_repo = ChatRepository(db)
    chat = await chat_repo.get_by_id(chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    user_repo = UserRepository(db)
    user = await user_repo.get_by_id(schema.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    added = await chat_repo.add_participant(chat_id, schema.user_id)
    await db.commit()
    
    saved_chat = await chat_repo.get_by_id(chat_id)
    return ChatReadSchema(
        id=saved_chat.id,
        title=saved_chat.title,
        type=saved_chat.type,
        participants=[p.user_id for p in saved_chat.participants]
    )


@router.delete("/{chat_id}/participants/{user_id}")
async def remove_participant(
    chat_id: str,
    user_id: str,
    db=Depends(get_db)
):
    chat_repo = ChatRepository(db)
    chat = await chat_repo.get_by_id(chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    removed = await chat_repo.remove_participant(chat_id, user_id)
    if not removed:
        raise HTTPException(status_code=404, detail="Participant not found")
    
    await db.commit()
    
    saved_chat = await chat_repo.get_by_id(chat_id)
    return ChatReadSchema(
        id=saved_chat.id,
        title=saved_chat.title,
        type=saved_chat.type,
        participants=[p.user_id for p in saved_chat.participants]
    )


@router.get("/{chat_id}/participants", response_model=List[ParticipantSchema])
async def get_participants(chat_id: str, db=Depends(get_db)):
    chat_repo = ChatRepository(db)
    chat = await chat_repo.get_by_id(chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    user_repo = UserRepository(db)
    participants = []
    for p in chat.participants:
        user = await user_repo.get_by_id(p.user_id)
        participants.append(ParticipantSchema(
            user_id=p.user_id,
            username=user.username if user else None,
            email=user.email if user else None
        ))
    return participants
