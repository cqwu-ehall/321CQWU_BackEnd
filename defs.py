import asyncio

from fastapi import FastAPI

from models.services.client import ClientService
from models.sqlite import Sqlite

loop = asyncio.get_event_loop()
app = FastAPI()
sqlite = Sqlite()
client_service = ClientService()
