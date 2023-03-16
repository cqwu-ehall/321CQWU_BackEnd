import datetime

from fastapi import Request
from fastapi.responses import JSONResponse

from defs import app

start_time = "07:00"
end_time = "23:55"


@app.middleware("http")
async def restrict_access_middleware(request: Request, call_next):
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")
    if start_time <= current_time <= end_time or now.weekday() >= 5:
        return await call_next(request)
    else:
        return JSONResponse({"code": 1, "msg": "定时维护时间，禁止使用"}, status_code=200)
