from httpx import AsyncClient
from datetime import datetime
from settings import APP_ID, APP_SECRET, TASK_TEMPLATE_ID, TASK_TEMPLATE_FAIL_ID


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


async def send_task_success_message(open_id: str, title: str, msg: str):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    async with AsyncClient() as client:
        req = await client.post(
            f'https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token={global_weixin_data["access_token"]}',
            json={
                "touser": open_id,
                "template_id": TASK_TEMPLATE_ID,
                "page": "/pages/index/index",
                "miniprogram_state": "formal",
                "lang": "zh_CN",
                "data": {
                    "character_string1": {
                        "value": title
                    },
                    "phrase3": {
                        "value": msg
                    },
                    "time4": {
                        "value": time
                    },
                },
            },
        )
        print(req.json())


async def send_task_fail_message(open_id: str, title: str, msg: str, detail: str):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    async with AsyncClient() as client:
        req = await client.post(
            f'https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token={global_weixin_data["access_token"]}',
            json={
                "touser": open_id,
                "template_id": TASK_TEMPLATE_FAIL_ID,
                "page": "/pages/index/index",
                "miniprogram_state": "formal",
                "lang": "zh_CN",
                "data": {
                    "character_string1": {
                        "value": title
                    },
                    "phrase3": {
                        "value": msg
                    },
                    "time4": {
                        "value": time
                    },
                    "thing5": {
                        "value": detail
                    }
                },
            },
        )
        print(req.json())
