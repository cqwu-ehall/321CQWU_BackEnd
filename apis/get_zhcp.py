from cqwu import Client

from defs import app
from models.listener import listener
from models.models.api_user import ApiUser
from models.services.user import UserAction
from utils.client import get_client
from utils.user import check_user_fake_password


@listener()
async def get_zhcp(client: Client):
    cp = await client.get_cp()
    return {"code": 0, "msg": "查询成功", "data": cp.dict()}


@app.post("/get_zhcp")
async def get_zhcps(user: ApiUser):
    try:
        username = int(user.username)
    except ValueError:
        return {"code": 1, "msg": "账号格式错误"}
    real_user = await UserAction.get_user_by_username(username=username)
    if check := await check_user_fake_password(real_user, user.fake_password):
        return check
    client = await get_client(real_user)
    try:
        return await get_zhcp(client)
    except Exception as e:
        return {"code": 1, "msg": e.__class__.__name__}
