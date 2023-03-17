import importlib
import os

import uvicorn
from settings import HOST, PORT
from defs import app, sqlite, client_service, loop
from models.services.scheduler import scheduler
from utils.open_id import refresh_access_token

# 遍历 apis 文件夹下的所有文件，并且使用 importlib 导入
# 从而实现自动导入
for filename in os.listdir("apis"):
    if filename.endswith(".py"):
        importlib.import_module(f"apis.{filename[:-3]}")


async def main():
    if not scheduler.running:
        scheduler.start()
    await sqlite.create_db_and_tables()
    await refresh_access_token()
    scheduler.add_job(refresh_access_token, "interval", seconds=7000)
    scheduler.add_job(client_service.clear_all_clients, "cron", hour=0, minute=0, second=0)
    server = uvicorn.Server(
        config=uvicorn.Config(app, host=HOST, port=PORT)
    )
    await server.serve()


if __name__ == "__main__":
    loop.run_until_complete(main())
