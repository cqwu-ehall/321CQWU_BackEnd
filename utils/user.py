from typing import Optional, Dict

from models.models.user import User
from models.services.user import UserAction


async def get_user(username: int) -> Optional[User]:
    return await UserAction.get_user_by_username(username=username)


async def check_user_fake_password(user: User, fake_password: str) -> Optional[Dict]:
    if user is None:
        return {"code": 1, "msg": "未绑定，请先绑定账号"}
    if user.fake_password != fake_password:
        return {"code": 1, "msg": "密码错误"}
    return None
