import asyncio
import importlib
import os

import uvicorn
from defs import app, sqlite, client_service
from models.services.scheduler import scheduler

# 遍历 apis 文件夹下的所有文件，并且使用 importlib 导入
# 从而实现自动导入
for filename in os.listdir("apis"):
    if filename.endswith(".py"):
        importlib.import_module(f"apis.{filename[:-3]}")


async def main():
    if not scheduler.running:
        scheduler.start()
    await sqlite.create_db_and_tables()
    scheduler.add_job(client_service.clear_all_clients, "cron", hour=0, minute=0, second=0)
    server = uvicorn.Server(
        config=uvicorn.Config(app, host="0.0.0.0")
    )
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
