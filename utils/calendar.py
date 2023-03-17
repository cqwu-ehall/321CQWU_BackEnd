import json
from typing import List
from pathlib import Path

import aiofiles
from cqwu import Client
from cqwu.types.calendar import AiCourse

from models.listener import listener
from models.models.user import User
from utils.client import get_client
from utils.open_id import send_task_message

DATA_PATH = Path("data/calendar")
DATA_PATH.mkdir(parents=True, exist_ok=True)


@listener(web_vpn=True)
async def get_calendar(client: Client):
    courses = await client.get_calendar(use_model=True)
    return {"code": 0, "msg": "查询成功", "data": courses}


async def send_fail_message(open_id: str, msg: str):
    await send_task_message(open_id, "更新课表", f"更新失败，{msg}")


async def send_success_message(open_id: str):
    await send_task_message(open_id, "更新课表", "更新成功，请前往小程序同步课表")


async def run_background_task(user: User, open_id: str):
    client = await get_client(user, timeout=30)
    try:
        data = await get_calendar(client)
    except Exception as e:
        data = {"code": 1, "msg": str(type(e))}
    if data.get("code") != 0:
        return await send_fail_message(open_id, data.get("msg"))
    courses: List[AiCourse] = data.get("data")
    datas = {str(i): [j.dict() for j in courses if i in j.weeks] for i in range(1, 21)}
    async with aiofiles.open(DATA_PATH / f"{client.username}.json", "w", encoding="utf-8") as f:
        await f.write(json.dumps(datas, ensure_ascii=False, indent=4))
    return await send_success_message(open_id)
