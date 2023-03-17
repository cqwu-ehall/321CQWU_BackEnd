from typing import cast, Optional

from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession

from defs import sqlite
from models.models.open_id import OpenId


class OpenIdAction:
    @staticmethod
    async def add_open_id(open_id: OpenId):
        async with sqlite.session() as session:
            session = cast(AsyncSession, session)
            session.add(open_id)
            await session.commit()

    @staticmethod
    async def get_open_id_by_username(username: int) -> Optional[OpenId]:
        async with sqlite.session() as session:
            session = cast(AsyncSession, session)
            statement = select(OpenId).where(OpenId.username == username)
            results = await session.exec(statement)
            return open_id[0] if (open_id := results.first()) else None

    @staticmethod
    async def update_open_id(old_open_id: OpenId, open_id: str):
        old_open_id.open_id = open_id
        async with sqlite.session() as session:
            session = cast(AsyncSession, session)
            session.add(old_open_id)
            await session.commit()
            await session.refresh(old_open_id)

    @staticmethod
    async def add_or_update_open_id(username: int, open_id: str):
        if old_user := await OpenIdAction.get_open_id_by_username(username):
            await OpenIdAction.update_open_id(old_user, open_id)
        else:
            await OpenIdAction.add_open_id(OpenId(username=username, open_id=open_id))
