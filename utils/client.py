from cqwu import Client

from defs import client_service
from models.models.user import User


async def get_client(user: User) -> Client:
    return await client_service.get_client(user)
