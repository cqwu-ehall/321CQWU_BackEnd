from sqlmodel import SQLModel, Field


class OpenId(SQLModel, table=True):
    __table_args__ = dict(mysql_charset="utf8mb4", mysql_collate="utf8mb4_general_ci")

    username: int = Field(primary_key=True)
    open_id: str = Field(default="")
