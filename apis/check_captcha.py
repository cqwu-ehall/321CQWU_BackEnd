import base64

from cqwu import Client
from cqwu.errors import NeedCaptchaError
from pydantic import BaseModel

from defs import app


class User(BaseModel):
    username: str


@app.post("/check_captcha")
async def check_captcha(user: User):
    try:
        username = int(user.username)
    except ValueError:
        return {"code": 1, "data": None, "msg": "账号格式错误"}
    client = Client(username=username, password="")
    try:
        await client.check_captcha(show_qrcode=False)
    except NeedCaptchaError as e:
        return {"code": 1, "data": base64.b64encode(e.captcha).decode('utf-8'), "msg": "需要验证码"}
    return {"code": 0, "data": None, "msg": "不需要验证码"}
