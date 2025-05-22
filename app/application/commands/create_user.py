from dataclasses import dataclass
from application.mediator import Mediator
from domain.entities.users import User
from domain.values.users import Email, Username
from infrastructure.repositories.user import UserRepository


@dataclass
class CreateUserCommand:
    email: str
    username: str


@dataclass
class CreateUserCommandHandler:
    user_repo: UserRepository
    mediator: Mediator

    async def handle(self, command: CreateUserCommand):
        user = User.create_user(
            email=Email(command.email),
            username=Username(command.username)
        )

        await self.user_repo.save(user)
        return user
