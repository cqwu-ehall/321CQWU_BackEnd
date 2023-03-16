import enum

from sqlmodel import SQLModel, Field, Column, Enum


class PWStatusEnum(int, enum.Enum):
    STATUS_OK = 0  # 正常
    INVALID_PASSWORD = 1  # 密码错误
    NEED_CAPTCHA = 2  # 需要验证码


class User(SQLModel, table=True):
    __table_args__ = dict(mysql_charset="utf8mb4", mysql_collate="utf8mb4_general_ci")

    username: int = Field(primary_key=True)
    password: str = Field(default="")
    fake_password: str = Field(default="")
    status: PWStatusEnum = Field(sa_column=Column(Enum(PWStatusEnum)))
    name: str = Field(default="")
    sex: str = Field(default="")
    age: int = Field(default=0)
    institute: str = Field(default="")
    specialty: str = Field(default="")
    now_class: str = Field(default="")
    join_year: int = Field(default=0)
    birthday: str = Field(default="")
    level: str = Field(default="")
