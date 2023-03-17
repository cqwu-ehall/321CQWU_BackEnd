from defs import app, loop
from models.models.api_user import ApiUser
from models.services.user import UserAction
from models.services.open_id import OpenIdAction
from utils.calendar import run_background_task
from utils.user import check_user_fake_password
from utils.open_id import code_to_session


class OpenUser(ApiUser):
    code: str


@app.post("/save_open_id")
async def save_open_id(user: OpenUser):
    try:
        username = int(user.username)
    except ValueError:
        return {"code": 1, "msg": "账号格式错误"}
    real_user = await UserAction.get_user_by_username(username=username)
    if check := await check_user_fake_password(real_user, user.fake_password):
        return check
    data = await code_to_session(user.code)
    if data.get("errcode", 0) != 0:
        return {"code": 1, "msg": "code错误"}
    await OpenIdAction.add_or_update_open_id(username=username, open_id=data["openid"])
    loop.create_task(run_background_task(real_user, data["openid"]))
    return {"code": 0, "msg": "登录成功"}
