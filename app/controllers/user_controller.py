from litestar import Controller, get, post, delete, put
from litestar.exceptions import NotFoundException
from app.services.user_service import UserService
from app.schemas.user_schema import UserCreate, UserResponse, UserUpdate, UserListResponse
from uuid import UUID


class UserController(Controller):
    path = "/users"
    # указал зависимость в main.py
    # dependencies = {"user_service": Provide("user_service")}


    @get("/{user_id:str}") # тут str, т.к передается строка UUID (поскольку модель из прошлой лабы)
    async def get_user_by_id(
        self,
        user_service: UserService,
        user_id: str,
    ) -> UserResponse:
        """Получить пользователя по ID"""
        try:
            uuid_id = UUID(user_id)
        except ValueError:
            raise NotFoundException(detail=f"Invalid user ID format")
        user = await user_service.get_by_id(uuid_id)
        if not user:
            raise NotFoundException(detail=f"User with ID {user_id} not found")
        return UserResponse.model_validate(user)


    @get()
    async def get_all_users(
        self,
        user_service: UserService,
    ) -> UserListResponse:
        """Получить всех пользователей"""
        try:
            users, users_count = await user_service.get_all_users(count=1000, page=1)
            return UserListResponse(
                users=[UserResponse.model_validate(user) for user in users],
                users_count=users_count
            )
        except Exception as e:
            raise NotFoundException(f"Error in get_all_users: {e}")


    @post()
    async def create_user(
        self,
        user_service: UserService,
        data: UserCreate,
    ) -> UserResponse:
        """Создать нового пользователя"""
        new_user = await user_service.create_user(data)
        return UserResponse.model_validate(new_user)


    @delete("/{user_id:str}")
    async def delete_user(
        self,
        user_service: UserService,
        user_id: str,
    ) -> None:
        """Удалить пользователя по ID"""
        try:
            uuid_id = UUID(user_id)
        except ValueError:
            raise NotFoundException(detail=f"Invalid user ID format")
        await user_service.delete_user(uuid_id)


    @put("/{user_id:str}")
    async def update_user(
        self,
        user_service: UserService,
        user_id: str,
        data: UserUpdate,
    ) -> UserResponse:
        """Обновить данные пользователя по ID"""
        try:
            uuid_id = UUID(user_id)
        except ValueError:
            raise NotFoundException(detail=f"Invalid user ID format")
        updated_user = await user_service.update_user(uuid_id, data)
        if not updated_user:
            raise NotFoundException(detail=f"User with ID {user_id} not found")
        return UserResponse.model_validate(updated_user)
