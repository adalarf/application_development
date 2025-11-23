from app.repositories.user_repository import UserRepository
from app.db import User
from app.schemas.user_schema import UserCreate, UserUpdate
from uuid import UUID


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository


    async def get_by_id(self, user_id: UUID) -> User | None:
        return await self.user_repository.get_by_id(user_id)


    async def get_by_filter(self, count: int, page: int, **kwargs) -> list[User]:
        return await self.user_repository.get_by_filter(count, page, **kwargs)


    async def create_user(self, user_data: UserCreate) -> User:
        return await self.user_repository.create(user_data)


    async def update_user(self, user_id: UUID, user_data: UserUpdate) -> User:
        return await self.user_repository.update(user_id, user_data)


    async def delete_user(self, user_id: UUID) -> None:
        await self.user_repository.delete(user_id)


    async def get_all_users(self, count: int, page: int) -> tuple[list[User], int]:
        users = await self.user_repository.get_by_filter(count, page)
        total = await self.user_repository.get_users_count()
        return users, total
