from cqwu import Client
from cqwu.errors import NeedCaptchaError, UsernameOrPasswordError

from pydantic import BaseModel

from defs import app
from models.services.user import UserAction


class User(BaseModel):
    username: str
    password: str


@app.post("/login")
async def login(user: User):
    try:
        username = int(user.username)
    except ValueError:
        return {"code": 1, "msg": "账号格式错误"}
    client = Client(username=username, password=user.password)
    try:
        await client.login_with_password(show_qrcode=False)
        me = await client.get_me()
        user = UserAction.from_cqwu_get_user(me)
        await UserAction.add_or_update_user(user)
    except UsernameOrPasswordError:
        return {"code": 1, "msg": "用户名或密码错误"}
    except NeedCaptchaError:
        return {"code": 1, "msg": "需要验证码"}
    except Exception as e:
        return {"code": 1, "msg": e.__class__.__name__}
    return {"code": 0, "msg": "登录成功"}
