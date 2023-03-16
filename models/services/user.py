import base64
from typing import cast, Optional

from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession

from defs import sqlite
from models.models.user import User, PWStatusEnum
from cqwu.types.user import User as CQWUUser


class UserAction:
    @staticmethod
    async def add_user(user: User):
        async with sqlite.session() as session:
            session = cast(AsyncSession, session)
            session.add(user)
            await session.commit()

    @staticmethod
    async def get_user_by_username(username: int) -> Optional[User]:
        async with sqlite.session() as session:
            session = cast(AsyncSession, session)
            statement = select(User).where(User.username == username)
            results = await session.exec(statement)
            return user[0] if (user := results.first()) else None

    @staticmethod
    async def update_user(old_user: User, new_user: User = None):
        if new_user:
            old_user.password = new_user.password
            old_user.fake_password = new_user.fake_password
            old_user.status = new_user.status
            old_user.name = new_user.name
            old_user.sex = new_user.sex
            old_user.age = new_user.age
            old_user.institute = new_user.institute
            old_user.specialty = new_user.specialty
            old_user.now_class = new_user.now_class
            old_user.join_year = new_user.join_year
            old_user.birthday = new_user.birthday
            old_user.level = new_user.level
        async with sqlite.session() as session:
            session = cast(AsyncSession, session)
            session.add(old_user)
            await session.commit()
            await session.refresh(old_user)

    @staticmethod
    async def add_or_update_user(user: User):
        if old_user := await UserAction.get_user_by_username(user.username):
            await UserAction.update_user(old_user, user)
        else:
            await UserAction.add_user(user)

    @staticmethod
    async def set_user_status(username: int, status: PWStatusEnum) -> bool:
        user = await UserAction.get_user_by_username(username)
        if not user:
            return False
        user.status = status
        await UserAction.update_user(user)
        return True

    @staticmethod
    async def change_user_password(username: int, password: str) -> bool:
        user = await UserAction.get_user_by_username(username)
        if not user:
            return False
        user.password = password
        user.status = PWStatusEnum.STATUS_OK
        await UserAction.update_user(user)
        return True

    @staticmethod
    def from_cqwu_get_user(cqwu_user: CQWUUser) -> User:
        return User(
            username=cqwu_user.username,
            password=cqwu_user.password,
            fake_password=base64.b64encode(cqwu_user.password.encode("utf-8")).decode("utf-8")[:10],
            status=PWStatusEnum.STATUS_OK,
            name=cqwu_user.name,
            sex=cqwu_user.sex,
            age=cqwu_user.age,
            institute=cqwu_user.institute,
            specialty=cqwu_user.specialty,
            now_class=cqwu_user.now_class,
            join_year=cqwu_user.join_year,
            birthday=cqwu_user.birthday,
            level=cqwu_user.level,
        )
