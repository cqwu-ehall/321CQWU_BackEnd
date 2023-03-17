from httpx import AsyncClient
from datetime import datetime
from settings import APP_ID, APP_SECRET, TASK_TEMPLATE_ID


global_weixin_data = {"access_token": ""}


async def refresh_access_token():
    async with AsyncClient() as client:
        response = await client.get(
            "https://api.weixin.qq.com/cgi-bin/token",
            params={
                "grant_type": "client_credential",
                "appid": APP_ID,
                "secret": APP_SECRET,
            },
        )
        global_weixin_data["access_token"] = response.json()["access_token"]


async def code_to_session(js_code: str):
    async with AsyncClient() as client:
        response = await client.get(
            "https://api.weixin.qq.com/sns/jscode2session",
            params={
                "appid": APP_ID,
                "secret": APP_SECRET,
                "js_code": js_code,
                "grant_type": "authorization_code",
            },
        )
        return response.json()


async def send_task_message(open_id: str, title: str, msg: str):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    async with AsyncClient() as client:
        await client.post(
            f'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={global_weixin_data["access_token"]}',
            json={
                "touser": open_id,
                "template_id": TASK_TEMPLATE_ID,
                "page": "/pages/index/index",
                "miniprogram_state": "formal",
                "lang": "zh_CN",
                "data": {
                    "character_string1": title,
                    "phrase3": msg,
                    "time4": time,
                },
            },
        )
