from cqwu import Client

from defs import client_service
from models.models.user import User


async def get_client(user: User, timeout: int = 10) -> Client:
    client = await client_service.get_client(user)
    client.request.timeout = timeout
    return client
