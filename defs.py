from fastapi import FastAPI

from models.services.client import ClientService
from models.sqlite import Sqlite

app = FastAPI()
sqlite = Sqlite()
client_service = ClientService()
