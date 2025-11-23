from app.db import User
from app.schemas.user_schema import UserCreate, UserUpdate
from sqlalchemy import select, delete as sql_delete, func
from uuid import UUID


class UserRepository:
    def __init__(self, session):
        self.session = session


    async def get_by_id(self, user_id: UUID) -> User | None:
        query = await self.session.get(User, user_id)
        return query


    async def get_by_filter(self, count: int, page: int, **kwargs) -> list[User]:
        query = await self.session.execute(
            select(User).filter_by(**kwargs).limit(count).offset((page - 1) * count)
        )
        results = query.scalars().all()
        return results


    async def create(self, user_data: UserCreate) -> User:
        new_user = User(**user_data.model_dump())
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user


    async def update(self, user_id: UUID, user_data: UserUpdate) -> User:
        user = await self.session.get(User, user_id)
        if not user:
            return None
        for key, value in user_data.model_dump(exclude_unset=True).items():
            setattr(user, key, value)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user


    async def delete(self, user_id: UUID) -> None:
        await self.session.execute(sql_delete(User).where(User.id == user_id))
        await self.session.commit()


    async def get_users_count(self) -> int:
        query = await self.session.execute(select(func.count(User.id)))
        return query.scalar()
