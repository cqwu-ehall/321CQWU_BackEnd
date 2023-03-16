import base64

from cqwu import Client
from cqwu.errors import EPayQrCodeError

from defs import app
from models.listener import listener
from models.models.api_user import ApiUser
from models.services.user import UserAction
from utils.client import get_client
from utils.user import check_user_fake_password


@listener()
async def gen_pay_qrcode(client: Client):
    try:
        await client.gen_pay_qrcode(show_qrcode=False)
    except EPayQrCodeError as e:
        return {"code": 0, "msg": "查询成功", "data": base64.b64encode(e.qrcode).decode("utf-8")}
    return {"code": 1, "msg": "查询失败，未知错误"}


@app.post("/epay_qrcode")
async def epay_qrcode(user: ApiUser):
    try:
        username = int(user.username)
    except ValueError:
        return {"code": 1, "msg": "账号格式错误"}
    real_user = await UserAction.get_user_by_username(username=username)
    if check := await check_user_fake_password(real_user, user.fake_password):
        return check
    client = await get_client(real_user)
    try:
        return await gen_pay_qrcode(client)
    except Exception as e:
        return {"code": 1, "msg": type(e)}
