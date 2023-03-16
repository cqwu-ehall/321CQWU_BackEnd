from typing import Dict

from cqwu import Client

from models.models.user import User


class ClientService:
    def __init__(self):
        self.clients: Dict[int, Client] = {}

    async def get_client(self, user: User) -> Client:
        if client := self.clients.get(user.username):
            return client
        client = Client(username=user.username, password=user.password)
        await client.login_with_password()
        self.clients[user.username] = client
        return client

    async def clear_all_clients(self):
        self.clients.clear()
