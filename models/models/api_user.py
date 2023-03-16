from pydantic import BaseModel


class ApiUser(BaseModel):
    username: str
    fake_password: str
