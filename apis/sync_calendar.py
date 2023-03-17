import json
from os.path import exists

import aiofiles

from defs import app
from models.models.api_user import ApiUser
from models.services.user import UserAction
from utils.user import check_user_fake_password


@app.post("/sync_calendar")
async def sync_calendar(user: ApiUser):
    try:
        username = int(user.username)
    except ValueError:
        return {"code": 1, "msg": "账号格式错误"}
    real_user = await UserAction.get_user_by_username(username=username)
    if check := await check_user_fake_password(real_user, user.fake_password):
        return check
    if not exists(f"data/calendar/{username}.json"):
        return {"code": 1, "msg": "课表不存在，请先刷新课表"}
    async with aiofiles.open(f"data/calendar/{username}.json", "r", encoding="utf-8") as f:
        data = await f.read()
    return {"code": 0, "msg": "查询成功", "data": json.loads(data)}
